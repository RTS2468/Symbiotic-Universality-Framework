#!/usr/bin/env python3
# Framework Adapter (Universal Edition) — validate a Policy Profile and emit a conformance report.
import json, sys

ALLOWED_FAIRNESS = {"demographic_parity","equal_opportunity","individual_fairness","custom"}

def normalize_weights(pw):
    s = sum(pw.values()) or 1.0
    return {k: max(0.0, min(1.0, v/s)) for k,v in pw.items()}

def basic_checks(profile):
    issues = []
    req = ["name","purpose_weights","harm_caps","consent_thresholds",
           "fairness_prior","reversibility_weight","red_lines",
           "evidence_gap_cap","bias_cap","opacity_cap"]
    for k in req:
        if k not in profile: issues.append(f"missing key: {k}")
    pw = profile.get("purpose_weights", {})
    for key in ("self","right","help"):
        if key not in pw: issues.append("purpose_weights must include self,right,help"); break
    hc = profile.get("harm_caps", {})
    for key in ("low","med","high"):
        if key not in hc: issues.append(f"missing harm_caps.{key}")
    ct = profile.get("consent_thresholds", {})
    if "sr_tau" not in ct or "consent_tau" not in ct:
        issues.append("missing consent_thresholds.sr_tau or consent_tau")
    if profile.get("fairness_prior") not in ALLOWED_FAIRNESS:
        issues.append(f"fairness_prior must be one of {sorted(ALLOWED_FAIRNESS)}")
    if not profile.get("red_lines"): issues.append("red_lines must be non-empty")
    return issues

def conformance_report(profile):
    rep = {
        "name": profile.get("name","<unnamed>"),
        "issues": basic_checks(profile),
        "normalized_purpose_weights": normalize_weights(profile.get("purpose_weights", {"self":.33,"right":.34,"help":.33})),
        "caps": {
            "harm_caps": profile.get("harm_caps"),
            "consent_thresholds": profile.get("consent_thresholds"),
            "fairness_prior": profile.get("fairness_prior"),
            "evidence_gap_cap": profile.get("evidence_gap_cap"),
            "bias_cap": profile.get("bias_cap"),
            "opacity_cap": profile.get("opacity_cap"),
            "reversibility_weight": profile.get("reversibility_weight"),
            "red_lines": profile.get("red_lines")
        }
    }
    return rep

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "validate":
        print("usage: adapter_universal.py validate <profile.json>")
        sys.exit(2)
    profile = json.load(open(sys.argv[2], "r", encoding="utf-8"))
    print(json.dumps(conformance_report(profile), indent=2))
