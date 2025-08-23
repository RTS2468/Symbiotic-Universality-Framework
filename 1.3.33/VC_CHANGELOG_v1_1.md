# Verification Core v1.1 — CHANGELOG

**Date:** 2025-08-06

- Added risk aggregator modes: `expected`, `cvar` (CVaR_alpha), `kl_dro` (expected + λ·KL).
- Added Pinsker fairness bound (TV ≤ sqrt(½·KL)) in metrics; cap on fairness KL.
- Added FSD dominance shortcut vs. baseline losses (if samples provided).
- Implemented thresholded Right: RI≥RI_MIN and Harm≤HARM_CAP(stakes) with gates E/Bias/Opacity/Consent/Fairness/Evidence.
- Integrated profile-driven caps (harm caps by stakes, fairness/evidence caps).
- Kept endpoints: Good* (A→1, Harm=0) and Evil (M→1 or red-lines).
