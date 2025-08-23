# UF Definitions — Concise Compendium (v1.0)

**Date:** 2025-08-06

> No theory—just definitions and the concepts they represent.

---

## Action
**Mnemo:** —

**Definition:** A proposed change you can do now. UF judges actions only, not persons.

**Inputs:** description, stakes, subjects, baseline

**Outputs:** verdict (Right/ Wrong), reasons

**Example:** Share notes with consent vs. post without permission.

---

## Baseline
**Mnemo:** —

**Definition:** What happens if we do nothing or keep the current plan. All comparisons use this.

**Inputs:** current outcome estimate

**Outputs:** reference outcome

**Example:** No message sent vs. send a message.

---

## Harm (H)
**Mnemo:** H

**Definition:** Expected downside from an action, scaled to stakes. Smaller is safer.

**Inputs:** loss scenarios or risk summary

**Outputs:** harm value

**Example:** Lower infection risk vs. baseline after washing hands.

---

## ReliefIndex (RI)
**Mnemo:** RI

**Definition:** Improvement vs. baseline harm. Nonnegative means no worse than baseline.

**Formula:** `RI = (H(baseline) - H(action)) / max(H(baseline), ε)`

**Inputs:** H(baseline), H(action)

**Outputs:** RI ∈ [−∞, 1]

**Example:** Baseline harm 0.30 → action harm 0.24 ⇒ RI = 0.20.

---

## Right (direction)
**Mnemo:** RI + gates

**Definition:** A step that improves vs. baseline and passes all caps/gates (↑).

**Inputs:** RI, caps results

**Outputs:** Right (↑)

**Example:** Offer reversible help with consent and fairness checked.

---

## Wrong (direction)
**Mnemo:** RI + gates

**Definition:** A step that degrades vs. baseline or fails any cap/gate (↓).

**Inputs:** RI, caps results

**Outputs:** Wrong (↓)

**Example:** Share someone’s data without consent even if helpful.

---

## Good* (limit)
**Mnemo:** AlignedLimit

**Definition:** Ideal endpoint: expected harm ≈ 0 and all caps/gates pass (A → 1).

**Inputs:** —

**Outputs:** conceptual limit

**Example:** Not a claim about today; it’s a north star.

---

## Evil (limit)
**Mnemo:** CollapseLimit

**Definition:** Endpoint of persistent misalignment/red‑line failures (M → 1).

**Inputs:** —

**Outputs:** conceptual limit

**Example:** Not a label for people; a limit of actions.

---

## Harm Cap (HC)
**Mnemo:** HCxx

**Definition:** Maximum allowed harm by stakes (high/med/low).

**Inputs:** stakes level

**Outputs:** pass/fail

**Example:** HC01: high‑stakes cap ≈ 0.01; med=5×, low=10×.

---

## Consent (C)
**Mnemo:** Cτ

**Definition:** Permission threshold for serious effects.

**Inputs:** subject consent levels

**Outputs:** pass/fail

**Example:** C80: require ≥ 0.80 consent.

---

## Fairness (F)
**Mnemo:** Fxx

**Definition:** Bound disparities across groups. Lower is fairer.

**Inputs:** fairness measure

**Outputs:** pass/fail

**Example:** F05: disparity cap set to 0.05 units (tight).

---

## Evidence Gap (EG)
**Mnemo:** EGxx

**Definition:** Mismatch between claims and evidence. Keep small.

**Inputs:** claim vs. evidence

**Outputs:** pass/fail

**Example:** EG05: claim–evidence cap set to 0.05.

---

## Bias (B)
**Mnemo:** B

**Definition:** Systematic tilt that distorts decisions. Keep within cap.

**Inputs:** bias measure

**Outputs:** pass/fail

**Example:** Independent review reduces bias.

---

## Opacity (O)
**Mnemo:** O

**Definition:** Lack of reasons or transparency. Keep low; explain choices.

**Inputs:** rationale clarity

**Outputs:** pass/fail

**Example:** Two bullet reasons for every decision.

---

## Reversibility (RV)
**Mnemo:** RV

**Definition:** How easily we can undo or repair. Prefer higher RV.

**Inputs:** undo cost

**Outputs:** preference/pass

**Example:** Try a pilot before full rollout.

---

## Agency (AG)
**Mnemo:** AG

**Definition:** Preserve the person’s capacity to choose and act.

**Inputs:** agency impact

**Outputs:** pass/fail

**Example:** Offer options, don’t force outcomes.

---

## Causal Admissibility (CA)
**Mnemo:** CA

**Definition:** Action respects allowed cause‑and‑effect structure.

**Inputs:** causal constraints

**Outputs:** pass/fail

**Example:** No manipulative hidden loops.

---

## Viable Potential (Φ)
**Mnemo:** PHI

**Definition:** Set of states kept reachable by gate‑passing steps.

**Inputs:** policy + environment

**Outputs:** Φ updated/unchanged

**Example:** Do not shrink future options with today’s choice.

---

## Profiles
**Mnemo:** —

**Definition:** Declared caps/thresholds for a community or context.

**Inputs:** cap settings

**Outputs:** config

**Example:** Neutral_SMM or community profile.

---

## A=B (Translation Principle)
**Mnemo:** —

**Definition:** Different words are fine if gates/endpoints/order are preserved. Verdicts match.

**Inputs:** mapping

**Outputs:** equivalence note

**Example:** Light/Good/Truth/Actualized ↔ Aligned limit.

---

## Lexicode
**Mnemo:** RI-HC-C-F-EG-B-O-RV-AG-CA-PHI # csum

**Definition:** Prefix‑free word for tokens + params + checksum bound to definition.

**Inputs:** mnemo tokens, params, checksum

**Outputs:** code string

**Example:** RI-HC01-C80-F05-EG05-B-O-RV-PHI # 86602E

---

## Resonance Marker (R‑marker)
**Mnemo:** note

**Definition:** A personal sign that encourages. Logged as note; never changes gates.

**Inputs:** free text

**Outputs:** audit note

**Example:** Version number felt meaningful.

---

## I‑Mode / E‑Mode / W‑Mode
**Mnemo:** RI‑EG‑B‑O / RI‑HC‑C‑F / full stack

**Definition:** Head; Heart; Wisdom (integrated). Use W‑Mode to commit a reversible Right step.

**Inputs:** mode choice

**Outputs:** draft → decision

**Example:** Write I→E→W paragraphs, then act.

---

## Large Experience Model (LEM)
**Mnemo:** RI‑HC‑C‑F‑EG‑B‑O‑RV‑AG

**Definition:** You are a model. Curate inputs, keep gates on, choose better‑than‑baseline steps.

**Inputs:** data, values

**Outputs:** next best step

**Example:** Mute one noisy source; add one high‑signal source.