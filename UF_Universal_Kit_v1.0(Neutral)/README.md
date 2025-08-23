# UF Universal Kit (v1.0)

**Date:** 2025-08-06

This kit removes theological language and ships a **neutral, universal** version of the framework.

## Contents
- `UF_WhitePaper_Simplified_Universal.md` + `.pdf`
- `Universal_Lexicon.md` (term mapping to neutral language)
- `verification_core_v1_1.py` (optional checker, if present)
- `policy_profile.schema.json` and `example_profile_neutral.json`
- `adapter_universal.py` (validate a profile)

## Quick Start
1. Read the Simplified Universal White Paper.
2. Edit `example_profile_neutral.json` if needed.
3. Validate: `python adapter_universal.py validate example_profile_neutral.json`
4. Integrate caps into your app via the Verification Core config (optional).

**Principle:** judge actions, not people; prefer improvements vs baseline within caps; enforce consent/fairness; keep decisions auditable.
