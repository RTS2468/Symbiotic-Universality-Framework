# Universality Framework — LPM ↔ LPM Interchange (Data-plane vs Control-plane)
**Version:** v2.2.2 (draft)  
**Date:** 2025-08-05  
**Scale:** 0–1  
**Thresholds:** retain resonance ≥ 0.02; flag dissonance > 0.98

## Separation of Concerns
- **Data-plane (wire):** compact, machine-only payload (**CBOR**) with determinism-critical fields: seed, noise schedule, sampler id, latent size, VAE/encoder fingerprints, control refs, tolerances, and output format/size.  
  - **Schema:** `uf.pxir.wire.v1` (binary)  
  - **Storage:** DHL/HL **hash only** (default).  
  - **Disclosure:** **Green**: store hash; **Amber/Red**: may store the payload or partial projection.
- **Control-plane (annotation):** optional human-readable JSON/YAML with intent, audience, names, and UF policy notes.  
  - **Schema:** `uf.pxir.annotation.v1` (text)  
  - **Storage:** DHL/HL **inline** for audits or when thresholds trip.

## Determinism Contract
Given identical Data-plane payloads, LPMs must produce equivalent previews within tolerance (**PSNR≥38**, **LPIPS≤0.08**) at 512px shortest side.

## Example Artifacts
- `UF_v2.2.2_pxir_wire.cbor` — binary wire payload (sha256:d1fb99ab9f32…)  
- `UF_v2.2.2_pxir_annotation.json` — human annotation (sha256:ea51ac4a5e0d…)

## DHL Logging Recommendations
- Log `WIRE_PAYLOAD` with `payload_ref = sha256` of the CBOR blob (no inline).
- Log `HUMAN_ANNOTATION` with JSON content or reference, per disclosure policy.
- Periodically emit `CHECKPOINT` braid anchors (Merkle-DAG) over recent entries.
