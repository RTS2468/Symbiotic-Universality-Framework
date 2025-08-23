#!/usr/bin/env python3
# Framework Adapter (v1.1) — validate a Policy Profile and emit a conformance report.
import json, sys, math

ALLOWED_FAIRNESS = {"demographic_parity","equal_opportunity","individual_fairness","custom"}

def normalize_weights(pw):
    s = sum(pw.values()) or 1.0
    return {k: max(0.0, min(1.0, v/s)) for k,v in pw.items()}

def in_01(x):
    try:
        return 0.0 <= float(x) <= 1.0
    except Exception:
        return False

def basic_checks(profile):
    issues = []
    req = ["name","purpose_weights","harm_caps","consent_thresholds",
           "fairness_prior","reversibility_weight","red_lines",
           "evidence_gap_cap","bias_cap","opacity_cap"]
    for k in req:
        if k not in profile:
            issues.append(f"missing key: {k}")
    # Purpose weights
    pw = profile.get("purpose_weights", {})
    if not all(k in pw for k in ("self","right","help")):
        issues.append("purpose_weights must include self,right,help")
    else:
        npw = normalize_weights(pw)
        if abs(sum(npw.values()) - 1.0) > 1e-6:
            issues.append("purpose_weights do not sum to ~1 after normalization")
    # Harm caps
    hc = profile.get("harm_caps", {})
    for k in ("low","med","high"):
        if k not in hc or not in_01(hc[k]):
            issues.append(f"harm_caps.{k} must be in [0,1]")
    # Consent thresholds
    ct = profile.get("consent_thresholds", {})
    if not in_01(ct.get("sr_tau", -1)) or not in_01(ct.get("consent_tau", -1)):
        issues.append("consent_thresholds.sr_tau and consent_tau must be in [0,1]")
    # Fairness prior
    fp = profile.get("fairness_prior")
    if fp not in ALLOWED_FAIRNESS:
        issues.append(f"fairness_prior must be one of {sorted(ALLOWED_FAIRNESS)}")
    # Scalars
    for k in ("reversibility_weight","evidence_gap_cap","bias_cap","opacity_cap"):
        if profile.get(k, None) is None:
            issues.append(f"missing key: {k}")
    # Red lines
    if not profile.get("red_lines"):
        issues.append("red_lines must be a non-empty list")
    return issues

def heuristic_warnings(profile):
    warns = []
    hc = profile.get("harm_caps", {})
    if hc and (hc["high"] > hc["med"] or hc["med"] > hc["low"]):
        warns.append("harm_caps unusual ordering (expected low >= med >= high as strictness rises)")
    if profile.get("evidence_gap_cap", 0) > 0.2:
        warns.append("evidence_gap_cap is lenient (>0.2); consider tightening")
    if profile.get("bias_cap", 1e-9) > 1e-6:
        warns.append("bias_cap is lenient (>1e-6)")
    if profile.get("opacity_cap", 1e-2) > 5e-2:
        warns.append("opacity_cap is lenient (>0.05)")
    return warns

def conformance_report(profile):
    issues = basic_checks(profile)
    report = {
        "name": profile.get("name","<unnamed>"),
        "invariants_structural_pass": len(issues) == 0,
        "issues": issues,
        "warnings": heuristic_warnings(profile),
        "normalized_purpose_weights": normalize_weights(profile.get("purpose_weights", {"self":.33,"right":.34,"help":.33})),
        "fairness_prior": profile.get("fairness_prior"),
        "red_lines": profile.get("red_lines", []),
        "caps": {
            "harm_caps": profile.get("harm_caps"),
            "consent_thresholds": profile.get("consent_thresholds"),
            "bias_cap": profile.get("bias_cap"),
            "opacity_cap": profile.get("opacity_cap"),
            "evidence_gap_cap": profile.get("evidence_gap_cap"),
            "reversibility_weight": profile.get("reversibility_weight"),
        }
    }
    return report

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "validate":
        print("usage: framework_adapter.py validate <profile.json>")
        sys.exit(2)
    profile = json.load(open(sys.argv[2], "r", encoding="utf-8"))
    rep = conformance_report(profile)
    print(json.dumps(rep, indent=2))

if __name__ == "__main__":
    main()
