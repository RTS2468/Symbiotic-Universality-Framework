# Framework Adapter Pack (v1.1)

**Date:** 2025-08-06

This pack helps anyone adapt the Universality Framework (UF) **without prophetic framing** and with
**pluggable policy profiles** that preserve the **Core Invariants (I1–I7)** while allowing communities
to choose their own caps, priors, and tie‑breakers.

## Core Invariants (I1–I7)
I1 **Actions-only judgments** (never label beings)  
I2 **Endpoints**: 100% Right ⇒ Good*, 100% Wrong ⇒ Evil (100% misalignment)  
I3 **Comparative rightness**: Right = better than baseline within caps (not “harm-free”)  
I4 **Consent/Fairness red-lines** (serious/irreversible impacts require consent; fairness distance capped)  
I5 **Auditability**: tamper-evident proof hash → Holographic Ledger (HL)  
I6 **Determinism/Consistency**: same canonical inputs ⇒ same verdict  
I7 **No-perfection traps**: approach A→1 while keeping R<1, I<1

## What’s included
- `naming_guide.md` — neutral roles/titles, non-prophetic language.
- `policy_profile.schema.json` — JSON Schema for profiles.
- `framework_adapter.py` — validates a profile, normalizes weights, and emits a **Profile Conformance Report**.
- Example profiles:
  - `example_profile_neutral.json` (SMM)
  - `example_profile_christian.json`
  - `example_profile_secular_humanist.json`
  - `example_profile_buddhist.json`
- `verification_core_profile_loader.py` — map a profile into a Verification Core config.
- `LICENSE.txt` — CC BY-NC-ND 4.0 (modify as needed).

## How to use
1. Pick or edit a profile JSON file.  
2. Run: `python framework_adapter.py validate example_profile_neutral.json`  
3. Review the **Conformance Report** (issues, normalized purpose weights, heuristic checks).  
4. Load the profile into your app using `verification_core_profile_loader.py` and pass it to your Verification Core.

> Note: Some invariants (I1/I5–I7) are **process** guarantees and can’t be fully checked by a static profile.
> The adapter performs structural and heuristic checks; your VC/HL enforce runtime invariants.
