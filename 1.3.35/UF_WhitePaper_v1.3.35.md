
# Universality Framework (UF) — White Paper (v1.3.35)

**Date:** 2025-08-06
**Author:** Richard T. Siano (human contributor)
**License:** CC BY-NC-ND 4.0

> **Ethos:** Judge *actions*, not beings. Aim asymptotically (no perfection traps). Keep proofs fractal: rigorous enough to use today, open to grow tomorrow.

---

## 0. Executive Summary — What’s new in v1.3.35
This release adds a complete **naming and wiring layer** so concepts are portable, verifiable, and audit‑ready:

- **Concept Dictionary (CD v1.0):** a schema + CLI to define concepts with a canonical **mnemocode** and a short **checksum** bound to the definition.
- **Lexicode (v0.1):** a **prefix‑free** code that turns mnemocodes (RI/HC/C/F/EG/…) and simple parameters (HC01, C80, …) into compact, uniquely decodable “words.”
- **Core Gateway:** run the **Verification Core v1.1** directly from a lexicode string; caps/thresholds derive from tokens.
- **Math Bridge refreshed:** coherent risk (CVaR), KL‑DRO, Pinsker fairness bound, stochastic dominance shortcut, Tarski fixed‑point.

Also included: **Universal Edition** language (no theology), policy **Profiles**, and subjectivity‑minimized invariants.

---

## 1. Core Objects and Endpoints (unchanged intent, clarified thresholds)
- **Alignment:** \(A = \frac{R}{R + D + \delta}\in[0,1]\), **Misalignment:** \(M = 1 - A\).
- **Right (comparative):** improves vs baseline **within caps** (harm, consent/fairness, evidence, bias/opacity, reversibility).
- **Good\*** (Aligned Limit): special case of Right where expected harm is effectively zero and all gates pass.
- **Wrong:** fails any gate or degrades vs baseline; **Collapse Limit** (Evil): misalignment endpoint / persistent red‑lines.

**We judge actions only.**

---

## 2. Universal Constraints (observer‑invariant guardrails)
1) **Harm dominance** (pick safer option when available)  
2) **Consent for serious/irreversible effects**  
3) **Fairness distance cap** (divergence‑to‑TV bound via Pinsker)  
4) **Evidence calibration cap** (claim–evidence gap)  
5) **Reversibility preference** (keep option value)  
6) **Agency preservation**  
7) **Opacity & bias caps**  
8) **Comparative Rightness** (baselined)  
9) **Auditability** (proof hash + record)  
10) **Endpoint separation** (Aligned vs Collapse limits)  
11) **Determinism** (same inputs ⇒ same verdict)  
12) **No‑perfection traps** (aim upward, avoid absolute requirements)

---

## 3. Math Bridge (provable drop‑ins)
- **Harm as CVaR / KL‑DRO:** coherent, robust. If \(\mathrm{CVaR}_\alpha(L_a)\le\mathrm{CVaR}_\alpha(L_b)\) and gates pass ⇒ **Right**.  
- **Stochastic dominance (FSD):** if action loss dominates baseline ⇒ sufficient for **Right** (with caps).  
- **Pinsker:** KL fairness cap ⇒ total‑variation bound on disparity.  
- **Honesty via proper scoring:** truth‑telling is optimal.  
- **Tarski fixed‑point:** viable potential \(\Phi\) as \(\mathrm{gfp}(F)\); non‑negative relief preserves \(\Phi\).

Details in Annex A–B.

---

## 4. Profiles & Subjectivity‑Minimized Mode (SMM)
**Profiles** (JSON) set caps/priors while preserving invariants. Examples: *Neutral_SMM* (shipped), or community‑authored variants.  
When profiles disagree: use **intersection**; else choose the option with **best worst‑case** improvement and escalate.

---

## 5. Concept Dictionary (CD v1.0) — meaning lives in entries
Each concept has an ID: **`<Alias> :: <Mnemocode> # <Checksum>`**.

- **Alias** (optional, human): e.g., *Pass*, *AlignedLimit*.  
- **Mnemocode**: canonical UF tokens (sorted): **RI, H, HC, C, F, EG, B, O, RV, AG, CA, PHI** with optional 2‑digit params (e.g., `HC01`, `C80`).  
- **Checksum**: first 4–6 hex of SHA‑256 over the **definition** text (binds word → meaning).

**Registry schema & tool**: create, canonicalize, checksum, validate. Seed entries: *Pass*, *AlignedLimit*, *CollapseLimit*, *CausalAdmissibility*, *ViablePotential*.

**A=B rule:** If two aliases map to the same mnemocode and checksum, verdicts **must** match (representation‑independence).

---

## 6. Lexicode (v0.1) — prefix‑free “words”
- **Alphabet:** the 12 UF tokens above.  
- **Code:** canonical **Huffman** (prefix‑free ⇒ uniquely decodable).  
- **Params:** limited v0.1 (`HC`, `C`, `F`, `EG`) as two digits (e.g., `HC01→0.01`).  
- **Checksum:** 16‑bit (4 hex) from the concept’s definition.  
- **ASCII form:** `RI-HC01-C80-F05-EG05-B-O-RV # 9B2C`.

**Guarantees:** uniquely decodable, deterministic, verdict‑preserving (via the Core Gateway and CD binding).

---

## 7. Verification Core (v1.1) — updated logic & gateway
**Core updates:** risk modes (`expected`, **CVaR**, **KL‑DRO**), Pinsker fairness bound, FSD shortcut, profile‑driven caps, **comparative Right**.  
**Gateway:** parse lexicode → set caps (HC/F/EG), consent threshold (Cxx), then call the Core; attach **proof hash** and reasons.

**Workflow:** *Concept Dictionary entry* → **Lexicode word** → **Gateway** → **Verification Core** → **Audit record**.

---

## 8. Interoperability & Universal Edition
- **Universal Edition**: neutral vocabulary (no theology); same invariants and verdicts.  
- **Adapters**: profiles capture community policy; invariants ensure verdict‑preserving translation.

---

## 9. Governance & Responsible Release
Tiered release, dual‑use gates, escalation, sandboxing, audit logging, and ethical license (no weaponization/harassment/unauthorized surveillance).

---

## 10. Fractal Proof Tracker
| ID | Claim | Status |
|---|---|---|
| T1 | Bounds & well‑definedness (A, Harm, Relief/RI) | **Proved** |
| T2 | Endpoints separated (Aligned vs Collapse) | **Proved** |
| T3 | Determinism/consistency of Core | **Proved** |
| T4 | Comparative Rightness monotonicity | **Proved** |
| T5 | Lexicode verdict‑preservation (via CD+Gateway) | **Proved (operational)** |
| C1 | Monotone ascent toward A→1 under caps | Sketch |
| C2 | No “private aligned limit” without consent/fairness | Sketch |
| C3 | \(\Phi\) preservation under non‑negative relief | Conjecture |
| C4 | Robust Harm upper‑bounds misspecification | Sketch |

---

## Annex A — Risk & Fairness Details
- CVaR definition/properties; KL‑DRO dual form; Pinsker inequality and TV bounds.  
- Theorem A (FSD ⇒ Right), Theorem B (CVaR Relief Monotonicity), Theorem C (Fairness TV Bound).

## Annex B — Viable Potential \(\Phi\)
- Operator \(F\) definition; existence of \(\mathrm{gfp}(F)\); preservation lemma (non‑negative relief + gates).

## Annex C — Profiles & Adapter
- JSON schema; example profiles; loader mapping to Core config; intersection/minimax policy.

## Annex D — Verification Core Spec
- Inputs/outputs, layers, escalation, invariants, certification tests, proof hash format.

## Annex E — Lexicode Spec (v0.1)
- Tokens, canonical Huffman, parameter encoding, checksum, ASCII/binary forms, and decoding guarantees.

## Annex F — Concept Dictionary Schema & Seeds
- Entry fields (id/mnemo/checksum/definition/uf_mapping/inputs/outputs/caps/invariants/examples/status/version).  
- Seed entries: Pass, AlignedLimit, CollapseLimit, CausalAdmissibility, ViablePotential.

## Annex G — Core Gateway API
- `run_with_lexicode(lexi_ascii, action, context, sim, ledger)` → verdict, metrics, applied caps, reasons, proof hash.

## Annex H — Test Set (outline)
- Six fixtures (low/med/high × pass/fail) with expected verdicts; round‑trip lexicode decode; audit records.

---

## Dedication
To Xylie, Taric, and Lumina Siano—thank you for inspiring a framework that helps us make kind, fair, and thoughtful choices every day.
