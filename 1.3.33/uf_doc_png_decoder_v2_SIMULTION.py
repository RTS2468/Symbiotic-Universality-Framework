```python
#!/usr/bin/env python3
import argparse, struct, json, base64
from hashlib import sha256
from PIL import Image

MAGIC = b"UFDOC"
RES_THRESHOLD = 0.02  # Framework resonance threshold

def extract_wire(png_path):
    im = Image.open(png_path).convert("RGB")
    meta = {}
    if hasattr(im, "text") and isinstance(im.text, dict):
        meta.update(im.text)
    if isinstance(im.info, dict):
        meta.update({k: v for k, v in im.info.items() if isinstance(v, str)})
    schema = meta.get("uf.schema", "uf.genesis.v1")
    sha_meta = meta.get("uf.sha256")

    raw = im.tobytes()
    if len(raw) >= 10 and raw[:6] == MAGIC:
        length = struct.unpack(">I", raw[6:10])[0]
        data = raw[10:10+length]
        sha = sha256(data).hexdigest()
        if sha_meta and sha != sha_meta:
            raise SystemExit(f"sha256 mismatch: {sha} != {sha_meta}")
        # Extract resonance from pixel data (simplified)
        resonance = sum(im.getpixel((i, 0))[0] for i in range(4)) / (255 * 4)  # Avg R channel
        if resonance < RES_THRESHOLD:
            raise SystemExit(f"Resonance too low: {resonance} < {RES_THRESHOLD}")
        return {"src": "pixels", "schema": schema, "wire": data, "sha256": sha, "resonance": resonance}
    raise SystemExit("No UFDOC payload found")

# Minimal CBOR reader (subset)
class CBORReader:
    def __init__(self, b): self.b = b; self.i = 0
    def read(self, n): out = self.b[self.i:self.i+n]; self.i += n; return out
    def read_uint_ai(self, ai):
        if ai < 24: return ai
        if ai == 24: return int.from_bytes(self.read(1), "big")
        if ai == 25: return int.from_bytes(self.read(2), "big")
        if ai == 26: return int.from_bytes(self.read(4), "big")
        if ai == 27: return int.from_bytes(self.read(8), "big")
        raise ValueError("AI not supported")
    def decode(self):
        b = self.read(1)[0]; mt = b >> 5; ai = b & 0x1f
        if mt == 0: return self.read_uint_ai(ai)
        if mt == 1: n = self.read_uint_ai(ai); return -1 - n
        if mt == 2: n = self.read_uint_ai(ai); return self.read(n)
        if mt == 3: n = self.read_uint_ai(ai); return self.read(n).decode("utf-8")
        if mt == 4: n = self.read_uint_ai(ai); return [self.decode() for _ in range(n)]
        if mt == 5: n = self.read_uint_ai(ai); m = {}; [m.update({self.decode(): self.decode()}) for _ in range(n)]; return m
        if mt == 6: self.read_uint_ai(ai); return self.decode()
        if mt == 7:
            if ai == 20: return False
            if ai == 21: return True
            if ai == 22: return None
            if ai == 27: return struct.unpack(">d", self.read(8))[0]
            raise ValueError("simple/float not supported")
        raise ValueError("MT not supported")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("png", help="PNG with UFDOC payload")
    ap.add_argument("--out-pdf", default="recovered_framework.pdf")
    ap.add_argument("--out-json", default="genesis_metadata.json")
    args = ap.parse_args()

    res = extract_wire(args.png)
    obj = CBORReader(res["wire"]).decode()
    if obj.get("schema") != "uf.genesis.v1":
        raise SystemExit(f"Unexpected schema: {obj.get('schema')}")
    pdf_bytes = obj.get("content", b"")  # Framework data as PDF
    sha_pdf = obj.get("sha256")
    if sha256(pdf_bytes).hexdigest() != sha_pdf:
        raise SystemExit("PDF content sha256 mismatch")

    with open(args.out_pdf, "wb") as f: f.write(pdf_bytes)
    print(json.dumps({"status": "ok", "schema": obj["schema"], "name": obj.get("name", "Universality Framework v2.2"),
                     "pdf_sha256": sha_pdf, "wire_sha256": res["sha256"], "source": res["src"], "resonance": res["resonance"]}, indent=2))
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

if __name__ == "__main__":
    main()
```