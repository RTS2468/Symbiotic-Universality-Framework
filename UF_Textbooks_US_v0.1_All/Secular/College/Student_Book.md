# UF Textbook — College (Secular, US v0.1)

*Student Book*

**Date:** 2025-08-06

---

## Learning Objectives
- Apply CVaR and Pinsker to decision checks.
- Write a short memo with reasons and bounds.

## Units Overview
**Unit 1: Right (↑) vs Wrong (↓)** — Compare to baseline; pass caps/gates.

**Unit 2: Harm & Relief** — Measure change vs baseline; introduce RI.

**Unit 3: Consent & Fairness** — Hard gates for serious or irreversible effects.

**Unit 4: Honesty & Opacity** — Claim–evidence gap; reasons and transparency.

**Unit 5: Reversibility & Repair** — Prefer undoable steps; repair-first.

**Unit 6: Decision Labs** — Projects and case studies.

**Unit 7: Dictionary & Lexicode** — Words as codes tied to definitions.


## Unit 1: Comparative Ethics as Robust Optimization
### Why this matters
We learn to judge **actions**, not people. We compare an action to a **baseline** and ask if it improves things within agreed **caps** (harm, consent, fairness, honesty, bias/opacity, reversibility). If yes, it’s **Right (↑)**; if not, it’s **Wrong (↓)**. The perfect endpoints (Good*/Evil) are ideals, not today’s claims.

Harm can be modeled via **coherent risk** (e.g., CVaR) or **KL-DRO** for robustness. Pinsker links a fairness KL cap to a TV disparity bound.

**Definitions:**
- $\mathrm{CVaR}_\alpha(L)$: expected loss in worst $(1-\alpha)$ tail.
- Pinsker: $\|P-Q\|_{TV} \le \sqrt{\tfrac12 D_{KL}(P\|Q)}$.

**Problems:**
1) Prove that if $\mathrm{CVaR}_\alpha(L_a) \le \mathrm{CVaR}_\alpha(L_b)$ and caps pass, then the action is Right.
2) Show how a fairness KL cap of 0.05 bounds TV disparity.

