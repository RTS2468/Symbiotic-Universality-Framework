# Distributed Holographic Ledger (DHL) — Spec (Images & Artifacts Aware)
**Version:** v2.2.1 (draft)  
**Date:** 2025-08-05  
**Scale:** 0–1  
**Thresholds:** retain resonance ≥ 0.02; flag dissonance > 0.98

## Purpose
Extend the single-node HL into a distributed, **artifact-aware** ledger that handles **image payloads** (plans, previews, finals) with integrity and selective transparency.

## Entry Types
- `INIT`, `SPEC_CREATE`, `SPEC_UPDATE`
- `DECISION` (include resonance/dissonance)
- `RENDER_PLAN`, `PREVIEW`, `FINAL_ASSET` (image-specific)
- `CHECKPOINT` (braid anchor), `ALERT`, `HALT`

## Entry Wire Format (JSON Lines)
```json
{
  "schema": "uf.dhl.entry.v1",
  "ledger_id": "dhl-{slug}",
  "seq": 7,
  "timestamp": "2025-08-05T12:00:00Z",
  "author": "{key_id}",
  "prev_hash": "{sha256_prev}",
  "type": "FINAL_ASSET",
  "resonance": 0.14,
  "dissonance": 0.05,
  "artifact": {
    "kind": "image",
    "ref": "sha256:{blob}",
    "mime": "image/png",
    "width": 1920,
    "height": 1080
  },
  "related": [
    {"type":"RENDER_PLAN","ref":"sha256:{plan_hash}"},
    {"type":"PREVIEW","ref":"sha256:{preview_hash}"}
  ],
  "signatures": [{"alg":"ed25519","sig":"{b64}"}]
}
```

## Storage & Proofs
- **Content addressed.** Payloads referenced by `sha256:` URIs; de-duplicate automatically.
- **Merkle-DAG.** Braid anchors via **CHECKPOINT** entries contain Merkle roots over included items.
- **Proof of inclusion.** Return minimal Merkle paths for entries to latest anchor.

## Sync (Gossip)
Exchange tips → fetch ranges → validate `prev_hash` and Merkle proofs → resolve branches by anchor recency, sign-off weight, and lowest dissonance.

## Privacy
- **Envelope encryption** for payloads; metadata in clear.
- **Red-level** forces disclosure of full reasoning appendix; green/amber follow disclosure policy.

## Governance
Roles: Author, Reviewer, Observer. Sign-off thresholds per project. Red-level requires explicit re-activation entry after HALT.

## Migration (HL → DHL)
Import HL as a branch; first **CHECKPOINT** becomes the initial braid anchor.
