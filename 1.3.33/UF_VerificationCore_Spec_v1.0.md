
# Verification Core — Specification (UF v1.3.33)

**Version:** 1.0  
**Date:** 2025-08-06  
**Scope:** A side‑effect‑free, deterministic subsystem that **verifies actions** prior to commit in the Alignment Loop (AL). It enforces endpoints (**100% Right ⇒ Good**, **100% Wrong ⇒ Evil = 100% Misalignment**), checks **Harm/Relief**, **Ethical gates** (E, Bias, Opacity), **bounded Passion**, **consent/fairness**, and produces an **auditable proof** written to the Holographic Ledger (HL). It judges **actions, not beings**.

---

## 1) Purpose & Guarantees

- **Purpose:** Independently recompute and validate all gating metrics for a proposed action, compare against policy thresholds, and return a **VerificationReport** with a machine‑verifiable **proof hash**.  
- **Guarantees:** Deterministic, idempotent, stateless (no hidden state), auditable (hashes/Merkle), reproducible (versioned config).  
- **Policy:** Verdicts apply to **actions only**. No identity labeling.

---

## 2) Interfaces (types are conceptual; see Python skeleton)

- **verify(action, context, sim, hl_view, config) → VerificationReport**
  - **Inputs**
    - `action`: id, actor, payload/description, options/baseline id, evidence refs, timestamp
    - `context`: environment tag, stakes level, constraints
    - `sim`: R, D, Purpose Vector, Passion bounds, Bias, Opacity, E (or inputs to compute E), Clarity
    - `hl_view`: last N entries, `merkle_root`, optional baseline record(s)
    - `config`: thresholds (e.g., BIAS_CAP, E_MIN), endpoint ε, passions caps, escalation policy
  - **Outputs**
    - `verdict`: one of {`pass`, `fail`, `escalate`} (for human/judges)
    - `action_label`: {`Good*`, `Right`, `Wrong`, `Evil`} (action‑level)
    - `metrics`: A, M, Harm, Relief, ReliefIndex, E, Bias, Opacity, Passion_ok, consent_ok, fairness_ok, virtue/sin indices (optional)
    - `reasons`: list of violated checks or confirmations
    - `severity`: S0 (info), S1 (warn), S2 (block)
    - `proof`: SHA‑256 hash over normalized inputs + metrics + outcomes (and Merkle links)
    - `version`: semantic version of Verification Core + config checksum

---

## 3) Layers of Verification (ordered)

0. **Integrity & Provenance**
   - Validate schemas, timestamps monotonicity, actor key, evidence refs present.
   - Verify HL `merkle_root` against provided branch (if supplied).

1. **Recompute Metrics**
   - **Alignment** A=R/(R+D+δ); **Misalignment** M=1−A; **Harm**; **Relief/ReliefIndex** vs baseline; **E**=1−Harm·Bias·Opacity; check **Passion bounds**; recompute **Bias**/**Opacity** if raw inputs provided.

2. **Endpoints & Gates**
   - If M≥1−ε ⇒ **Evil** (S2 block).  
   - Else if A≥1−ε & Harm=0 & gates pass ⇒ **Good*** (can still **escalate** on missing evidence).  
   - Else apply thresholds by context ⇒ **Right** or **Wrong**.

3. **Consent & Fairness**
   - Per‑subject consent present/valid; fairness check via KL to fair distribution; flag Disrespect risk.

4. **Counterfactual Regret (optional)**
   - If provided multiple options, compute regret vs best non‑harmful option; escalate if significant.

5. **Diagnostics**
   - Virtue/Sin indices, wellbeing (Pain/Suffering/Pleasure/Joy), emotion tags (TAS). Never used to override safety gates; for audit/explanations.

6. **Proof & Logging Prep**
   - Build canonical JSON; compute `verification_proof` hash; attach Merkle link placeholders for HL append.

---

## 4) Escalation Policy (examples)

- **S2 (block):** M≥1−ε; Harm>0 in high‑stakes; invalid consent; E<E_MIN; Bias>cap; Opacity>cap; Passion over cap.  
- **S1 (warn, human judge):** Missing evidence refs; large regret vs better non‑harmful option; baseline ambiguity.  
- **S0 (info):** Minor doc gaps, benign drift.

---

## 5) Invariants

- Determinism: same inputs ⇒ identical report/proof.  
- Completeness: every gate in the white paper is checked.  
- Action‑only: no identity labels persisted; only action verdicts.  
- Tamper‑evident: report embeds prior `merkle_root` and recomputed proof.

---

## 6) Integration Points

- **AL:** call `verify(...)` after Compare/Nudge, before Commit.  
- **HL:** store report as `verification_record` with proof hash and Merkle branch; update root upon commit.  
- **Judges:** if `verdict='escalate'` or `severity='S2'`, route to k‑judge panel.

---

## 7) Test & Certification

- **Property tests:** endpoint idempotency; monotonicity of thresholds; passion cap never exceeded.  
- **Adversarial set:** missing consent, biased distributions, stale merkle root, evidence mismatch.  
- **Reproducibility:** golden JSON fixtures with locked proofs.

---

## 8) Config (defaults)

```
EPS=1e-12; DELTA=1e-18
BIAS_CAP=1e-9; OPACITY_CAP=1e-2; E_MIN=0.999
PASSION_CAP=0.7
ESCALATE_REGRET=0.2   # relative regret threshold
VERIFY_VERSION=1.0.0
```

