#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path

CODEBOOK = json.loads(Path("codebook.json").read_text(encoding="utf-8"))
PARAM_TOKENS = ["HC","C","F","EG"]
TOKENS = ["RI","H","HC","C","F","EG","B","O","RV","AG","CA","PHI"]

def checksum16(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.strip().encode("utf-8")).hexdigest()[:4].upper()

def encode(mnemo_tokens, params, definition):
    base_tokens = [t for t in mnemo_tokens if t in TOKENS]
    base_tokens = sorted(set(base_tokens))
    def param_suffix(k):
        v = params.get(k, None)
        return f"{int(v):02d}" if v is not None else ""
    mnemo_parts = []
    for t in base_tokens:
        if t in PARAM_TOKENS:
            mnemo_parts.append(f"{t}{param_suffix(t)}")
        else:
            mnemo_parts.append(t)
    mnemo = "-".join(mnemo_parts)
    bitstring = "".join(CODEBOOK[t] for t in base_tokens)
    param_bits = ""
    for t in PARAM_TOKENS:
        if t in base_tokens:
            v = params.get(t, 0)
            if v < 0 or v > 99: raise ValueError("param out of range (0..99)")
            param_bits += format(int(v), "07b")
    csum_hex = checksum16(definition)
    csum_bits = format(int(csum_hex, 16), "016b")
    full_bits = bitstring + param_bits + csum_bits
    ascii_form = f"{mnemo} # {csum_hex}"
    return {"bitstring": full_bits, "ascii": ascii_form, "checksum": csum_hex, "mnemo": mnemo}

def decode(bitstring, tokens_present):
    inv = {v:k for k,v in CODEBOOK.items()}
    pos = 0; decoded = []
    # Decode tokens using greedy scan
    maxL = max(map(len, inv.keys()))
    target = len(set(tokens_present))
    while len(decoded) < target:
        matched = False
        for L in range(1, maxL+1):
            frag = bitstring[pos:pos+L]
            if frag in inv:
                decoded.append(inv[frag]); pos += L; matched = True; break
        if not matched: raise ValueError("decode error")
    base_tokens = sorted(set(decoded))
    # Params
    params = {}
    for t in PARAM_TOKENS:
        if t in base_tokens:
            val_bits = bitstring[pos:pos+7]; pos += 7
            params[t] = int(val_bits, 2)
    # checksum
    csum_bits = bitstring[pos:pos+16]; pos += 16
    csum_hex = format(int(csum_bits, 2), "04X")
    return base_tokens, params, csum_hex

def main():
    if len(sys.argv) < 2:
        print("Usage: lexicode.py encode|decode ..."); return
    cmd = sys.argv[1]
    if cmd == "encode":
        # Example: python lexicode.py encode "RI,HC,C,F,EG,B,O,RV" "HC=1,C=80,F=5,EG=5" "definition text"
        toks = sys.argv[2].split(",")
        param_str = sys.argv[3] if len(sys.argv) >= 4 else ""
        definition = sys.argv[4] if len(sys.argv) >= 5 else ""
        params = {}
        if param_str:
            for kv in param_str.split(","):
                if "=" in kv:
                    k,v = kv.split("="); params[k.strip()] = int(v.strip())
        res = encode(toks, params, definition)
        print(json.dumps(res, indent=2))
    elif cmd == "decode":
        # Example: python lexicode.py decode <bitstring> "RI,HC,C,F,EG,B,O,RV"
        bitstring = sys.argv[2]
        toks = sys.argv[3].split(",") if len(sys.argv) >= 4 else []
        tokens, params, csum = decode(bitstring, toks)
        print(json.dumps({"tokens":tokens, "params":params, "checksum":csum}, indent=2))
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
