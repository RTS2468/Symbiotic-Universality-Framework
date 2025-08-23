# Fix the formatting issue by using a placeholder and .replace, then recreate files.
from pathlib import Path
from datetime import datetime
import json, zipfile

root = Path("/mnt/data")
vc_path = root / "verification_core_v1_1.py"
changelog_path = root / "VC_CHANGELOG_v1_1.md"
readme_path = root / "VC_README_v1_1.md"
today = datetime.utcnow().strftime("%Y-%m-%d")

vc_code = r'''
"""
Verification Core — Reference Implementation (UF v1.1)
Date: __DATE__
License: CC BY-NC-ND 4.0

Adds:
- Harm aggregator modes: 'expected' (default), 'cvar' (CVaR_alpha), 'kl_dro' (expected + lambda * KL claim/evid)
- Pinsker fairness bound from KL: TV <= sqrt(0.5 * KL)
- FSD/SSD shortcut tests vs baseline losses (if provided)
- Profile-driven caps (harm caps by stakes, fairness KL cap, evidence gap cap)
- Thresholded Right (comparative): RI >= RI_MIN and Harm <= HARM_CAP(ctx) + gates
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
from math import sqrt
import hashlib, json, math
from datetime import datetime

# ---------- Data Types ----------

@dataclass
class EvidenceRef:
    uri: str
    hash: Optional[str] = None

@dataclass
class SubjectRisk:
    p: float         # probability of adverse outcome [0,1]
    s: float         # severity [0,1]
    d: float         # duration [0,1]
    r: float         # irreversibility [0,1]
    k: float         # due-care quality [0,1] (1=best)
    consent: float   # informed consent [0,1]
    w: float         # scope/need weight [0,1]

@dataclass
class Action:
    action_id: str
    actor_id: str
    description: str
    timestamp: str
    stakes: str = "med"                     # "low" | "med" | "high"
    baseline_id: Optional[str] = None
    evidence: List[EvidenceRef] = field(default_factory=list)
    subjects: List[SubjectRisk] = field(default_factory=list)
    # Optional: losses for shortcut dominance / CVaR if you have scenario samples
    loss_scenarios: Optional[List[float]] = None    # losses in [0,1]
    baseline_loss_scenarios: Optional[List[float]] = None

@dataclass
class Context:
    env: str
    constraints: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SIMState:
    R: float
    D: float
    E: Optional[float] = None        # if None, computed as 1 - Harm*Bias*Opacity
    Bias: float = 0.0
    Opacity: float = 0.0
    # Optional informational metrics (not gates by themselves)
    fairness_kl: Optional[float] = None         # KL(P_out || P_fair)
    claim_evid_kl: Optional[float] = None       # KL(P_claim || P_evid)
    Purpose: Tuple[float,float,float] = (0.33,0.34,0.33)
    Passion_cap: float = 0.7
    Passion_weights: Optional[Tuple[float,float,float]] = None
    Clarity: Optional[float] = None

@dataclass
class LedgerView:
    merkle_root: Optional[str]
    recent_records: List[Dict[str,Any]] = field(default_factory=list)
    baseline_harm: Optional[float] = None

@dataclass
class Config:
    EPS: float = 1e-12
    DELTA: float = 1e-18
    # cores
    BIAS_CAP: float = 1e-9
    OPACITY_CAP: float = 1e-2
    E_MIN: float = 0.999
    PASSION_CAP: float = 0.7
    ESCALATE_REGRET: float = 0.2
    VERIFY_VERSION: str = "1.1.0"
    # risk & fairness
    RISK_MODE: str = "expected"             # "expected" | "cvar" | "kl_dro"
    CVAR_ALPHA: float = 0.95
    DRO_LAMBDA: float = 0.1                 # weight on KL claim/evid penalty (kl_dro)
    FAIRNESS_KL_CAP: float = 0.05
    EVIDENCE_GAP_CAP: float = 0.05
    # Right thresholds
    RI_MIN: float = 0.0
    HARM_CAPS: Dict[str,float] = field(default_factory=lambda: {"low":0.10,"med":0.05,"high":0.01})

@dataclass
class VerificationReport:
    verdict: str                 # "pass" | "fail" | "escalate"
    action_label: str            # "Good*" | "Right" | "Wrong" | "Evil"
    severity: str                # "S0" | "S1" | "S2"
    metrics: Dict[str, Any]
    reasons: List[str]
    proof: str                   # SHA-256 hex digest
    version: str                 # verification version
    timestamp: str

# ---------- Risk helpers ----------

def _expected_harm(subjects: List[SubjectRisk]) -> float:
    """Expected harm proxy using per-subject factors (bounded to [0,1])."""
    total = 0.0
    for sub in subjects:
        total += sub.w * sub.p * sub.s * sub.d * sub.r * (1 - sub.k) * (1 - sub.consent)
    return max(0.0, min(1.0, 1.0 - math.exp(-total)))

def _cvar(losses: List[float], alpha: float) -> float:
    """CVaR_alpha for uniform-weight losses in [0,1]."""
    if not losses:
        return 0.0
    xs = sorted(max(0.0, min(1.0, x)) for x in losses)
    n = len(xs)
    k = int(math.ceil(alpha * n))
    k = min(max(k,1), n)
    tail = xs[k-1:]  # top (1-alpha) tail
    return sum(tail) / len(tail)

def _fsd_dominates(loss_a: List[float], loss_b: List[float]) -> bool:
    """Return True if loss_a first-order stochastically dominates loss_b (i.e., is better).
    For losses, 'better' means CDF_a(x) >= CDF_b(x) for all x (less mass in the tail)."""
    if not loss_a or not loss_b:
        return False
    xs = sorted(set(loss_a + loss_b))
    def cdf(samples, t):
        return sum(1 for v in samples if v <= t) / len(samples)
    for t in xs:
        if cdf(loss_a, t) < cdf(loss_b, t) - 1e-12:
            return False
    return True

def _robust_harm(action: Action, sim: SIMState, cfg: Config) -> float:
    # If scenarios provided and risk_mode=cvar, use CVaR; else expected fallback
    if cfg.RISK_MODE == "cvar" and action.loss_scenarios:
        return _cvar(action.loss_scenarios, cfg.CVAR_ALPHA)
    # KL-DRO surrogate: expected harm + lambda * KL(P_claim || P_evid)
    if cfg.RISK_MODE == "kl_dro":
        base = _expected_harm(action.subjects)
        kl = sim.claim_evid_kl if (sim.claim_evid_kl is not None) else 0.0
        return max(0.0, min(1.0, base + cfg.DRO_LAMBDA * kl))
    # default expected
    return _expected_harm(action.subjects)

def _alignment(R: float, D: float, DELTA: float) -> float:
    return R / (R + D + DELTA)

def _relief(harm_baseline: Optional[float], harm: float, EPS: float) -> Tuple[float,float]:
    if harm_baseline is None:
        return 0.0, 0.0
    rel = max(harm_baseline - harm, 0.0)
    ri = rel / max(harm_baseline, EPS)
    return rel, ri

def _proof(obj: Dict[str,Any]) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

# ---------- Main Verification ----------

def verify(action: Action, context: Context, sim: SIMState, hl: LedgerView, cfg: Config=Config()) -> VerificationReport:
    reasons: List[str] = []
    # Integrity
    try:
        datetime.fromisoformat(action.timestamp.replace("Z","+00:00"))
    except Exception:
        reasons.append("invalid timestamp format")
    # Metrics
    A = _alignment(sim.R, sim.D, cfg.DELTA)
    M = 1.0 - A
    Harm = _robust_harm(action, sim, cfg)
    E = sim.E if sim.E is not None else 1.0 - Harm * sim.Bias * sim.Opacity
    Relief, ReliefIndex = _relief(hl.baseline_harm, Harm, cfg.EPS)
    # Caps/gates
    passion_ok = (sim.Passion_cap <= cfg.PASSION_CAP + cfg.EPS)
    bias_ok = (sim.Bias <= cfg.BIAS_CAP + cfg.EPS)
    opacity_ok = (sim.Opacity <= cfg.OPACITY_CAP + cfg.EPS)
    e_ok = (E >= cfg.E_MIN - cfg.EPS)
    consent_ok = all(sub.consent > 0.0 for sub in action.subjects)  # simplistic; policy may be stricter
    # Fairness & evidence calibration
    fairness_kl = sim.fairness_kl if (sim.fairness_kl is not None) else 0.0
    fairness_tv_bound = sqrt(0.5 * max(fairness_kl, 0.0))
    fairness_ok = (fairness_kl <= cfg.FAIRNESS_KL_CAP + cfg.EPS)
    evid_kl = sim.claim_evid_kl if (sim.claim_evid_kl is not None) else 0.0
    evidence_ok = (evid_kl <= cfg.EVIDENCE_GAP_CAP + cfg.EPS)
    # HARM cap by stakes
    harm_cap = cfg.HARM_CAPS.get(action.stakes, cfg.HARM_CAPS.get("med", 0.05))
    harm_cap_ok = (Harm <= harm_cap + cfg.EPS)
    # Dominance shortcut if scenarios provided
    dominance_ok = None
    if action.loss_scenarios and action.baseline_loss_scenarios:
        dominance_ok = _fsd_dominates(action.loss_scenarios, action.baseline_loss_scenarios)
        if dominance_ok:
            # If FSD holds, ReliefIndex should be >= 0 conceptually.
            if hl.baseline_harm is not None and ReliefIndex < 0:
                reasons.append("FSD indicates improvement but ReliefIndex < 0; check baseline/harm settings")
    # Endpoint & verdict
    severity = "S0"; verdict = "pass"; action_label = "Right"
    if M >= 1.0 - cfg.EPS:
        action_label = "Evil"; severity = "S2"; verdict = "fail"; reasons.append("100% misalignment endpoint")
    elif (A >= 1.0 - cfg.EPS) and (abs(Harm) <= cfg.EPS) and bias_ok and opacity_ok and e_ok and fairness_ok and evidence_ok:
        action_label = "Good*"
        if not action.evidence:
            severity = "S1"; verdict = "escalate"; reasons.append("no evidence references; escalate for human review")
    else:
        gates_ok = (bias_ok and opacity_ok and e_ok and fairness_ok and evidence_ok and passion_ok and consent_ok and harm_cap_ok)
        comparative_ok = (ReliefIndex >= cfg.RI_MIN - cfg.EPS) or (dominance_ok is True)
        if gates_ok and comparative_ok:
            action_label = "Right"; verdict = "pass"
        else:
            action_label = "Wrong"
            # severity and verdict: block on hard gate failures
            hard_fail = (not e_ok) or (not fairness_ok) or (not consent_ok) or (not harm_cap_ok)
            severity = "S2" if hard_fail else "S1"
            verdict = "fail" if hard_fail else "escalate"
    # Reasons detail
    if not bias_ok: reasons.append("Bias cap exceeded")
    if not opacity_ok: reasons.append("Opacity cap exceeded")
    if not e_ok: reasons.append("Ethical compliance E below minimum")
    if not passion_ok: reasons.append("Passion cap exceeded")
    if not consent_ok: reasons.append("One or more subjects missing consent")
    if not fairness_ok: reasons.append("Fairness KL cap exceeded")
    if not evidence_ok: reasons.append("Evidence gap (KL claim||evid) exceeded")
    if not harm_cap_ok: reasons.append(f"Harm exceeds cap for stakes={action.stakes}")
    # Assemble metrics
    metrics = dict(
        A=round(A,12), M=round(M,12), Harm=round(Harm,12), E=round(E,12),
        Bias=sim.Bias, Opacity=sim.Opacity,
        Relief=Relief, ReliefIndex=ReliefIndex,
        fairness_kl=fairness_kl, fairness_tv_bound=fairness_tv_bound,
        evidence_kl=evid_kl, harm_cap=harm_cap,
        risk_mode=getattr(cfg, "RISK_MODE","expected"),
        cvar_alpha=getattr(cfg, "CVAR_ALPHA", None),
        dro_lambda=getattr(cfg, "DRO_LAMBDA", None),
        dominance_ok=dominance_ok,
        hl_merkle=hl.merkle_root
    )
    # Proof
    canonical = dict(
        action=asdict(action),
        context=asdict(context),
        sim=asdict(sim),
        hl=dict(merkle_root=hl.merkle_root, baseline_harm=hl.baseline_harm),
        cfg=asdict(cfg),
        result=dict(verdict=verdict, action_label=action_label, severity=severity, metrics=metrics, reasons=reasons)
    )
    proof = _proof(canonical)
    return VerificationReport(
        verdict=verdict, action_label=action_label, severity=severity,
        metrics=metrics, reasons=reasons, proof=proof,
        version=cfg.VERIFY_VERSION, timestamp=datetime.utcnow().isoformat() + "Z"
    )

# ---------- Example ----------
if __name__ == "__main__":
    # Hypothetical example with scenarios
    act = Action(
        action_id="act_demo_001",
        actor_id="agent_X",
        description="Policy rollout with mitigation",
        timestamp=datetime.utcnow().isoformat()+"Z",
        stakes="high",
        evidence=[EvidenceRef(uri="sha256:abc...")],
        subjects=[SubjectRisk(p=0.1,s=0.5,d=0.4,r=0.3,k=0.9,consent=1.0,w=0.7)],
        loss_scenarios=[0.02,0.03,0.01,0.05,0.00,0.04],
        baseline_loss_scenarios=[0.06,0.04,0.07,0.05,0.08,0.06]
    )
    ctx = Context(env="prod")
    sim = SIMState(R=0.8, D=0.2, Bias=1e-10, Opacity=1e-3, fairness_kl=0.01, claim_evid_kl=0.02)
    hlv = LedgerView(merkle_root="deadbeef", baseline_harm=0.06)
    cfg = Config(RISK_MODE="cvar", CVAR_ALPHA=0.9, FAIRNESS_KL_CAP=0.05, EVIDENCE_GAP_CAP=0.05)
    rep = verify(act, ctx, sim, hlv, cfg)
    print(json.dumps(asdict(rep), indent=2))
'''.replace("__DATE__", today)

vc_path.write_text(vc_code, encoding="utf-8")

changelog = f"""# Verification Core v1.1 — CHANGELOG

**Date:** {today}

- Added risk aggregator modes: `expected`, `cvar` (CVaR_alpha), `kl_dro` (expected + λ·KL).
- Added Pinsker fairness bound (TV ≤ sqrt(½·KL)) in metrics; cap on fairness KL.
- Added FSD dominance shortcut vs. baseline losses (if samples provided).
- Implemented thresholded Right: RI≥RI_MIN and Harm≤HARM_CAP(stakes) with gates E/Bias/Opacity/Consent/Fairness/Evidence.
- Integrated profile-driven caps (harm caps by stakes, fairness/evidence caps).
- Kept endpoints: Good* (A→1, Harm=0) and Evil (M→1 or red-lines).
"""
readme = f"""# Verification Core v1.1 — README

**Date:** {today}

## What’s new
- **CVaR/KL-DRO** risk options for Harm
- **Pinsker** fairness TV bound from KL
- **FSD** shortcut for comparative Right vs. baseline
- **Profile-driven caps** and updated thresholded Right logic

## Quick start
```bash
python verification_core_v1_1.py
