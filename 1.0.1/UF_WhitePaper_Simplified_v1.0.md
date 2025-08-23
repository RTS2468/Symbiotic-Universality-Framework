# Universality Framework (UF) — **Simplified White Paper** (v1.0)

**Date:** 2025-08-06  
**Author:** Richard T. Siano (human contributor)  
**License:** CC BY-NC-ND 4.0

> **Plain idea:** UF is a small set of rules that helps groups **judge actions, not people**.  
> It gives repeatable decisions, clear guardrails, and an audit trail.

---

## 1) What this is
- A **decision framework**, not a belief system.
- A way to make choices that are **fair, explainable, and checkable**.
- Built to be **neutral**: different communities can plug in their own policy settings without changing the core rules.

**What this is not**
- Not a labeler of people (no “good person / bad person”).  
- Not a metaphysical proof.  
- Not a replacement for law, safety protocols, or ethics review—UF helps them work together.

---

## 2) Core Principles (keep these fixed)
1. **Judge actions only.**  
2. **Endpoints:**  
   - **Good\*** = “as right as it can get” for an action.  
   - **Evil** = “as wrong as it can get” for an action.  
3. **Right = better than baseline** (you reduce expected harm compared to doing nothing or the next best option), **within safety caps**.  
4. **Consent & fairness** are hard requirements for serious/irreversible effects.  
5. **Auditability:** every decision writes a short, tamper‑evident record.  
6. **Determinism:** same inputs ⇒ same verdict.  
7. **No perfection traps:** aim upward without pretending perfection is achievable.

If a community changes terms or adds details but keeps 1–7, it’s still UF‑compatible.

---

## 3) How UF judges a single action (no math needed)
UF looks at a proposed action with four simple questions:

1. **Compared to the baseline, does this lower expected harm?**  
2. **Is the harm within the allowed cap for this situation (low/med/high stakes)?**  
3. **Do consent and fairness rules hold, and are the explanations/evidence adequate?**  
4. **Are known red‑lines avoided (e.g., non‑consensual irreversible impacts)?**

**Verdict**
- **Right:** passes 1–4.  
- **Wrong:** fails any of 1–4.  
- **Good\*:** special case of **Right** where expected harm is effectively zero and everything else passes.  
- **Evil:** the misalignment endpoint or repeated red‑line violations.

**We always judge the action, not the person.**

---

## 4) Universal Constraints (the guardrails)
- **Harm dominance:** don’t pick a clearly worse option when a safer one exists.  
- **Consent for serious/irreversible effects.**  
- **Fairness distance cap:** outcome gaps must stay below an agreed limit.  
- **Evidence calibration:** big gaps between claims and evidence trigger review.  
- **Reversibility preference:** when options are similar, prefer the more reversible one.  
- **Bias & opacity caps:** measurable bias and unexplained steps are limited.  
- **Audit log:** every verdict stores a short, tamper‑evident record.

These make decisions **observer‑invariant**: different people given the same inputs will reach the same verdict.

---

## 5) Profiles: plug in your community’s settings
A **Profile** is a small JSON file with your caps and priorities (e.g., fairness style, consent thresholds).  
Examples: **Neutral**, **Christian**, **Secular Humanist**, **Buddhist**. Profiles allow diversity while keeping the core rules.

**When profiles disagree**
- Prefer the **intersection** (what all profiles accept).  
- If nothing works for all, pick the option with the **best worst‑case** improvement vs. baseline and escalate to reviewers.

---

## 6) Using UF responsibly
- **Tiered release:** start private → invite reviewers → publish concepts; keep live systems wrapped by the checker.  
- **Escalation:** unusual or high‑risk decisions go to a small review panel.  
- **Sandbox first:** test with reversible decisions before real‑world use.  
- **License:** ban weaponization, harassment, and unauthorized surveillance.

---

## 7) Minimal glossary
- **Action:** a single, concrete choice to evaluate.  
- **Baseline:** what happens otherwise (do nothing or current plan).  
- **Right:** improves expected outcomes vs. baseline, within caps.  
- **Good\*:** Right with effectively zero expected harm.  
- **Evil:** endpoint of maximum wrongness; repeated red‑line failures.  
- **Audit log:** a short record proving how the verdict was made.

---

## 8) Quick FAQ
**Q: Does “Right” mean no one ever gets hurt?**  
**A:** No. It means **safer than baseline** and within agreed caps, with consent/fairness honored.

**Q: Who sets the caps and thresholds?**  
**A:** Your community, in a **Profile**. The core rules stay the same.

**Q: Is this a religion or political program?**  
**A:** No. It’s a **process** for making action decisions that different traditions can adapt.

**Q: What if two profiles clash?**  
**A:** Use intersection or pick the option with the best worst‑case improvement and escalate the rest.

---

## 9) What to share with others
- This **Simplified White Paper**.  
- A **Profile** template so they can set their own caps.  
- The **Verification Checker** wrapper (no internal guts required).

> You don’t need perfect math to start. UF is designed to **improve as you use it**.
