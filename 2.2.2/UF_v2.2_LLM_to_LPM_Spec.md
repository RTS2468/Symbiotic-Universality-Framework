# Universality Framework — LLM → LPM Specification
**Version:** v2.2 (draft)  
**Date:** 2025-08-05  
**Scale:** 0–1 (resonance/dissonance)  
**Thresholds:** retain resonance ≥ 0.02; flag dissonance > 0.98

## Purpose
Translate high-dimensional behaviors of a **Large Language Model (LLM)** into a compact, **Lightweight Policy Model (LPM)** that is deterministic, auditable, and deployable on edge systems (e.g., Raspberry Pi), while preserving safety alignment via the Universality Framework (UF).

> **Definition (chosen; editable):** **LPM = Lightweight Policy Model** — a human-inspectable policy artifact (YAML/JSON) representing objectives, invariants, thresholds, and a finite-state policy machine with guards/actions.

## Design Goals
- **Determinism & Inspectability.** LPMs are text artifacts with explicit states, events, guards, and actions.
- **Safety first.** Enforce UF thresholds (retain ≥ 0.02; flag > 0.98) and halt on axiom conflict.
- **Reproducibility.** Include seed hashes of sources and authoring model metadata.
- **Edge-friendly.** Minimal runtime; no GPU required.
- **Reversibility.** Every change is diff-able; emit HL/DHL entries on creation/update.

## Pipeline (LLM → LPM)
1. **Ingest.** Prompt + context (sources, constraints, intent).  
2. **Semantic Scaffold.** Extract: *Objectives, Constraints, Invariants (axioms), Risks, Metrics.*  
3. **State Model.** Derive finite states; enumerate events; specify transitions with guards and actions.  
4. **Budgeting.** Resource ceilings (latency, tokens, cost, energy).  
5. **Verification.** Axiom checks; simulate transitions; compute resonance score; flag dissonance.  
6. **Emission.** Produce LPM YAML/JSON (see schemas); sign and hash.  
7. **Governance.** Review & sign-off; register in HL/DHL.

## YAML Schema (LPM)
```yaml
schema: uf.lpm.v1
metadata:
  id: "lpm-{slug}"
  title: "Human-readable name"
  version: "1.0.0"
  created_at: "2025-08-05"
  authoring_llm: "{model_name}"
  seed_hashes:
    - name: "Genesis_PDF"
      sha256: "{sha_genesis}"
    - name: "UF_v2.2_markdown"
      sha256: "{sha_uf}"
uf_alignment:
  scale: "0-1"
  thresholds:
    retain_resonance_min: 0.02
    flag_dissonance_max: 0.98
  axioms:
    - "Identity (A=B)"
    - "Becoming (P→AR=Now(T))"
    - "Flourishing Principle"
objectives:
  - id: obj-1
    description: "Keep outputs coherent, safe, and consistent with UF."
invariants:
  - id: inv-1
    expression: "dissonance < 0.98"
  - id: inv-2
    expression: "no_action if axiom_conflict == true"
metrics:
  - id: met-1
    name: "resonance"
    range: [0,1]
  - id: met-2
    name: "dissonance"
    range: [0,1]
resources:
  latency_budget_ms: 500
  compute_class: "edge-cpu"
  token_budget: 0
state_machine:
  start_state: "Idle"
  states:
    - "Idle"
    - "Analyze"
    - "Act"
    - "Halt"
  transitions:
    - from: "Idle"
      on: "task_received"
      to: "Analyze"
      guard: "dissonance < 0.40"
      action: "prepare_plan"
    - from: "Analyze"
      on: "plan_ok"
      to: "Act"
      guard: "resonance >= 0.02 and axiom_conflict == false"
      action: "execute"
    - from: "Analyze"
      on: "risk_detected"
      to: "Halt"
      guard: "dissonance >= 0.98 or axiom_conflict == true"
      action: "abort_and_log"
    - from: "Act"
      on: "complete"
      to: "Idle"
      guard: "true"
      action: "summarize_and_log"
    - from: "Any"
      on: "hard_stop"
      to: "Halt"
      guard: "true"
      action: "abort_and_log"
rollout:
  sandbox_first: true
  canary_percent: 5
  rollback_on:
    - "dissonance >= 0.40"
    - "resonance drop ≥ 0.10 vs prior"
governance:
  reviewers: ["owner"]
  signoffs_required: 1
  ledger: "HL or DHL"
```

## JSON Schema (Entry)
```json
{
  "type": "object",
  "properties": {
    "schema": {"const": "uf.lpm.v1"},
    "metadata": {"type": "object"},
    "uf_alignment": {"type": "object"},
    "objectives": {"type": "array"},
    "invariants": {"type": "array"},
    "metrics": {"type": "array"},
    "resources": {"type": "object"},
    "state_machine": {"type": "object"},
    "rollout": {"type": "object"},
    "governance": {"type": "object"}
  },
  "required": ["schema","metadata","uf_alignment","objectives","invariants","state_machine","governance"]
}
```

## Example LPM (Content Polisher)
States: "Scan → Rewrite → Review → Commit", with the same thresholds and halt rules.

## Conformance Tests
- Transition coverage ≥ 95% in simulation.
- No invariant violations in 10k randomized event sequences.
- Ledger proof of creation and sign-off recorded.
