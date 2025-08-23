# UF Lexicode — v0.1 (Prefix‑Free Concept Words)

Date: 2025-08-06

**Goal:** A compact, logical coding for UF concepts where each "word" is a **prefix‑free**
string that uniquely maps to UF primitives (RI, HC, C, F, EG, B, O, RV, AG, CA, PHI),
optional parameters (e.g., HC=0.01), and a checksum of the formal definition.

**Design summary**
- **Alphabet:** tokens = [RI, H, HC, C, F, EG, B, O, RV, AG, CA, PHI].
- **Code:** canonical **Huffman** code over tokens (prefix‑free, uniquely decodable).
- **Order:** tokens sorted lexicographically before encoding (canonicalization).
- **Parameters:** optional, limited v0.1: {HC, C, F, EG} — encoded as two‑digit integers (e.g., HC01 → 0.01, C80 → 0.80).
- **Checksum:** 16‑bit (first 4 hex chars) of SHA‑256 over the **normalized definition** string.
- **ASCII form:** `Alias :: MNEMO # CCCC` (human); **Binary form:** concatenated Huffman codes + 16‑bit checksum + param trailer.

**Guarantees**
- **Uniquely decodable:** prefix‑free ⇒ by Kraft–McMillan, each token stream decodes uniquely.
- **Deterministic:** same inputs ⇒ same bitstring.
- **Verdict‑preserving:** if two lexicodes decode to the same normalized UF concept (same tokens/params) and checksum, they map to the same Verification Core gates; verdicts match (representation independence).

See `lexicode_spec_tests.md` for examples and `lexicode.py` for encoder/decoder.
