"""
verification_core_profile_loader.py
Map a Policy Profile JSON into a Verification Core config (dict).

Usage:
  python verification_core_profile_loader.py example_profile_neutral.json
"""
import json, sys, os

try:
    import verification_core as VC
except Exception:
    VC = None  # Optional

def load_profile(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def make_config_from_profile(profile: dict) -> dict:
    cfg = {
        "EPS": 1e-12, "DELTA": 1e-18,
        "BIAS_CAP": profile.get("bias_cap", 1e-9),
        "OPACITY_CAP": profile.get("opacity_cap", 1e-2),
        "E_MIN": 0.999,
        "PASSION_CAP": 0.7,
        "ESCALATE_REGRET": 0.2,
        "VERIFY_VERSION": "1.0.0",
        # App-level: use stakes to look up harm caps at decision time.
        "HARM_CAPS": profile.get("harm_caps", {"low":0.1,"med":0.05,"high":0.01}),
        "CONSENT_RULE": profile.get("consent_thresholds", {"sr_tau":0.6,"consent_tau":0.8}),
        "FAIRNESS": {
            "prior": profile.get("fairness_prior"),
            "params": profile.get("fairness_params",{})
        },
        "REVERSIBILITY_WEIGHT": profile.get("reversibility_weight", 0.7),
        "RED_LINES": profile.get("red_lines", []),
        "PURPOSE_WEIGHTS": profile.get("purpose_weights", {}),
        "EVIDENCE_GAP_CAP": profile.get("evidence_gap_cap", 0.05),
    }
    return cfg

def main():
    if len(sys.argv) < 2:
        print("usage: python verification_core_profile_loader.py <profile.json>")
        sys.exit(2)
    prof = load_profile(sys.argv[1])
    cfg = make_config_from_profile(prof)
    print(json.dumps(cfg, indent=2))

if __name__ == "__main__":
    main()
