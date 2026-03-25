from __future__ import annotations

from app.graph.state import ResearchState


def run(state: ResearchState) -> ResearchState:
    valid, rejected = [], []
    for c in state["candidate_batch"]:
        p = c["param_dict"]
        reasons = []
        if p["macd_fast"] >= p["macd_slow"]:
            reasons.append("macd_fast must be < macd_slow")
        if p["vwap_window"] <= 0 or p["vwap_stdev_window"] <= 0:
            reasons.append("windows must be > 0")
        if p["target_deviation_multiplier"] <= 0:
            reasons.append("deviation multiplier must be > 0")
        if p["stop_buffer"] < 0:
            reasons.append("stop buffer must be >= 0")
        if p["safety_exit_opposing_bars"] < 1:
            reasons.append("safety exit bars must be >= 1")
        if p["stop_buffer"] < 0.01:
            reasons.append("stop buffer below minimum tick multiple")

        if reasons:
            c["validation_status"] = "rejected"
            c["validation_reason"] = "; ".join(reasons)
            rejected.append(c)
        else:
            c["validation_status"] = "valid"
            c["validation_reason"] = ""
            valid.append(c)
    state["validated_candidates"] = valid
    state["rejected_candidates"] = rejected
    return state
