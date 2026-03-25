from __future__ import annotations

from app.graph.state import ResearchState


def run(state: ResearchState, max_rounds: int, max_total_experiments: int, target_score: float) -> ResearchState:
    decision = "explore"
    stop_reason = None
    tested = len(state["tried_hashes"])
    best_score = state["ranked_results"][0]["score"] if state["ranked_results"] else -1
    if state["round_index"] >= max_rounds:
        decision = "stop"
        stop_reason = "max_rounds_reached"
    elif tested >= max_total_experiments:
        decision = "stop"
        stop_reason = "max_total_experiments_reached"
    elif best_score >= target_score:
        decision = "stop"
        stop_reason = "target_score_reached"
    elif best_score > 0.5:
        decision = "exploit"
    state["next_round_plan"] = {"decision": decision, "best_score": best_score}
    state["stop_reason"] = stop_reason
    return state
