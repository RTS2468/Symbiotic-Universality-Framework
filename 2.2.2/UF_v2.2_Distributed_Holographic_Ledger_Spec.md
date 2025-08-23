# Distributed Holographic Ledger (DHL) — Specification
**Version:** v1.0 (draft)  
**Date:** 2025-08-05  
**Scale:** 0–1  
**Thresholds:** retain resonance ≥ 0.02; flag dissonance > 0.98

## Purpose
Generalize the single-node **Holographic Ledger (HL)** into a **Distributed Holographic Ledger (DHL)** for multi-agent/audience collaboration, with integrity, selective transparency, and offline-first merging—without the cost of a full blockchain.

## Design Principles
- **Append-only, hash-linked.** Every entry carries `prev_hash`; branches are allowed; merges create braid anchors.
- **Selective transparency.** Metadata stays public; payloads may be encrypted; proofs remain verifiable.
- **Edge & offline friendly.** Gossip sync; eventual consistency via Merkle-DAG + vector clocks.
- **UF-aligned disclosure.** Internal process is hidden unless thresholds trip; Red-level events force full disclosure.

## Entry Types
- `INIT` (initialize ledger)  
- `SPEC_CREATE` / `SPEC_UPDATE` (create/update specs like LPM)  
- `DECISION` (material decision with resonance/dissonance)  
- `CHECKPOINT` (periodic braid anchor)  
- `ALERT` (Amber) / `HALT` (Red)

## Entry Wire Format (JSON Lines)
```json
{
  "schema": "uf.dhl.entry.v1",
  "ledger_id": "dhl-{slug}",
  "seq": 42,
  "timestamp": "2025-08-05T12:00:00Z",
  "author": "{key_id}",
  "prev_hash": "{sha256_of_prev}",
  "type": "DECISION",
  "resonance": 0.12,
  "dissonance": 0.05,
  "axiom_flags": ["A=B", "P→AR=Now(T)", "Flourishing"],
  "payload_ref": "sha256:{blob_hash}",
  "signatures": [{"alg":"ed25519","sig":"{base64}"}]
}
```

## Merkle-DAG & Braid Anchors
- Each author maintains a tip; periodic **CHECKPOINT** merges multiple tips into a **braid anchor** with a Merkle root.  
- **Proof of inclusion** is a Merkle path from an entry to the nearest braid anchor.

## Sync Protocol (Gossip)
1. Exchange **tips** (ledger_id → (seq, hash)).  
2. Request missing ranges.  
3. Validate `prev_hash` chain and Merkle proofs.  
4. Resolve concurrent branches by: (a) most recent **CHECKPOINT**; (b) highest **sign-off weight**; (c) lowest **dissonance**.

## Security & Privacy
- **Hashing:** SHA-256 for links; content-addressed payloads.  
- **Signatures:** Ed25519 per author; multi-sign `CHECKPOINT`s.  
- **Privacy:** Envelope encryption for payloads; metadata stays in clear; selective disclosure via sharing keys.  
- **Replay & drift:** Nonces and bounded time drift checks.

## APIs (Reference)
- `POST /entry` — append valid entry  
- `GET /tip` — current tip(s)  
- `GET /range?from=..&to=..` — stream entries  
- `GET /proof/{hash}` — Merkle proof to latest anchor

## Example: Recording an LPM Creation
1) Author emits `SPEC_CREATE` with `payload_ref` = hash of LPM YAML.  
2) Reviewer emits `DECISION` with resonance/dissonance + sign-off.  
3) Anchor via `CHECKPOINT` combining both.

## Governance
- **Roles:** Author, Reviewer, Observer.  
- **Sign-offs:** Threshold signatures required for promotion from draft → active.  
- **Red-level events:** Automatic `HALT` broadcast; require explicit re-activation entry.

## JSON Schemas
- `uf.dhl.entry.v1` (entry)  
- `uf.dhl.checkpoint.v1` (anchor)

## Migration (HL → DHL)
- Import HL as a single-author branch.  
- First **CHECKPOINT** establishes the initial braid anchor; future entries follow DHL rules.
