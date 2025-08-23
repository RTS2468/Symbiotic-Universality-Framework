# Verification Core v1.1 — README

**Date:** 2025-08-06

## What’s new
- **CVaR/KL-DRO** risk options for Harm
- **Pinsker** fairness TV bound from KL
- **FSD** shortcut for comparative Right vs. baseline
- **Profile-driven caps** and updated thresholded Right logic

## Quick start
```bash
python verification_core_v1_1.py
```

Edit the `Config` in the example to switch `RISK_MODE` (`expected` | `cvar` | `kl_dro`) and adjust `CVAR_ALPHA` / `DRO_LAMBDA`.

## Integrating with Profiles
Use your `verification_core_profile_loader.py` (from the Adapter Pack) to map a profile JSON into caps and pass the resulting values
into `Config(...)`. The core remains deterministic: same canonical inputs ⇒ same verdict.
