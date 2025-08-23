#!/usr/bin/env python3
"""
UF LPM PNG Decoder — extract CBOR wire payload from a PNG that may carry it:
(1) In PNG text metadata (iTXt) as base64, and/or
(2) Pixel-embedded (RGB) with a "UFWIRE" magic header + uint32 length.

Optionally decode the CBOR to JSON (for inspection) using a minimal decoder
that covers the subset used by uf.pxir.wire.v1.
"""
import argparse, base64, struct, json, sys
from hashlib import sha256
from PIL import Image

MAGIC = b"UFWIRE"

def decode_from_png(png_path: str):
    im = Image.open(png_path).convert("RGB")
    # 1) Try metadata (preferred)
    meta = {}
    # Pillow exposes PNG textual metadata in im.info and im.text (depending on version)
    if hasattr(im, "text") and isinstance(im.text, dict):
        meta.update(im.text)
    if isinstance(im.info, dict):
        meta.update({k: v for k, v in im.info.items() if isinstance(v, str)})
    schema = meta.get("uf.schema")
    b64 = meta.get("uf.pxir.wire.b64")
    sha_meta = meta.get("uf.sha256")

    if b64:
        try:
            data = base64.b64decode(b64)
            sha = sha256(data).hexdigest()
            if sha_meta and sha != sha_meta:
                raise ValueError(f"Metadata sha256 mismatch: got {sha}, expected {sha_meta}")
            return {"src":"metadata", "schema": schema or "unknown", "wire": data, "sha256": sha}
        except Exception as e:
            # fall through to pixel path
            pass

    # 2) Pixel-embedded fallback
    raw = im.tobytes()  # row-major RGB
    if len(raw) >= 10 and raw[:6] == MAGIC:
        length = struct.unpack(">I", raw[6:10])[0]
        if 10 + length <= len(raw):
            data = raw[10:10+length]
            return {"src":"pixels", "schema": schema or "uf.pxir.wire.v1", "wire": data, "sha256": sha256(data).hexdigest()}
        else:
            raise ValueError("Pixel payload length exceeds image data")
    raise RuntimeError("No decodable UF wire payload found in PNG")

# --- Minimal CBOR decoder for our subset (ints, floats, bytes, text, arrays, maps, bool, null) ---
class CBORReader:
    def __init__(self, b: bytes):
        self.b = b; self.i = 0
    def read(self, n):
        if self.i + n > len(self.b):
            raise ValueError("Unexpected end of CBOR data")
        chunk = self.b[self.i:self.i+n]; self.i += n; return chunk
    def read_uint_ai(self, ai):
        if ai < 24: return ai
        if ai == 24: return int.from_bytes(self.read(1), "big")
        if ai == 25: return int.from_bytes(self.read(2), "big")
        if ai == 26: return int.from_bytes(self.read(4), "big")
        if ai == 27: return int.from_bytes(self.read(8), "big")
        raise ValueError(f"Unsupported additional info: {ai}")
    def decode(self):
        b = self.read(1)[0]
        mt, ai = b >> 5, b & 0x1f
        if mt == 0:  # unsigned int
            return self.read_uint_ai(ai)
        if mt == 1:  # negative int
            n = self.read_uint_ai(ai); return -1 - n
        if mt == 2:  # bytes
            n = self.read_uint_ai(ai); return self.read(n)
        if mt == 3:  # text
            n = self.read_uint_ai(ai); return self.read(n).decode("utf-8")
        if mt == 4:  # array
            n = self.read_uint_ai(ai); return [self.decode() for _ in range(n)]
        if mt == 5:  # map
            n = self.read_uint_ai(ai); m = {}
            for _ in range(n):
                k = self.decode(); v = self.decode(); m[k] = v
            return m
        if mt == 6:  # tag (unused)
            self.read_uint_ai(ai); return self.decode()
        if mt == 7:
            if ai == 20: return False
            if ai == 21: return True
            if ai == 22: return None
            if ai == 27:  # float64
                import struct
                return struct.unpack(">d", self.read(8))[0]
            raise ValueError(f"Unsupported simple/float AI {ai}")
        raise ValueError(f"Unsupported major type {mt}")

def main():
    ap = argparse.ArgumentParser(description="Decode UF LPM wire payload from PNG (metadata or pixel-embedded).")
    ap.add_argument("png", help="Input PNG with embedded UF wire payload")
    ap.add_argument("--out-cbor", help="Write recovered CBOR to this path", default=None)
    ap.add_argument("--out-json", help="Decode CBOR to JSON and write here", default=None)
    args = ap.parse_args()

    res = decode_from_png(args.png)
    print(json.dumps({"status":"ok", "source": res["src"], "schema": res["schema"], "sha256": res["sha256"]}, indent=2))

    if args.out_cbor:
        with open(args.out_cbor, "wb") as f:
            f.write(res["wire"])
    if args.out_json:
        obj = CBORReader(res["wire"]).decode()
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

if __name__ == "__main__":
    main()
