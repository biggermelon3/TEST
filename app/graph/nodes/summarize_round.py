from __future__ import annotations

from app.graph.state import ResearchState


def run(state: ResearchState) -> ResearchState:
    ranked = state["ranked_results"]
    if not ranked:
        state["round_summary"] = {"markdown": "No successful candidates.", "json": {"status": "empty"}}
        return state
    best, worst = ranked[0], ranked[-1]
    md = (
        f"# Round {state['round_index']} Summary\n"
        f"- Best candidate: `{best['candidate_id']}` score={best['score']:.4f}\n"
        f"- Worst candidate: `{worst['candidate_id']}` score={worst['score']:.4f}\n"
        "- Observation: prioritize higher sharpe with controlled drawdown.\n"
    )
    state["round_summary"] = {
        "markdown": md,
        "json": {
            "best_candidate_id": best["candidate_id"],
            "worst_candidate_id": worst["candidate_id"],
            "helpful_changes": ["lower stop buffer in moderate range", "balanced MACD fast/slow gap"],
            "harmful_changes": ["too few trades", "excessive drawdown"],
            "next_action": "exploit" if best["score"] > 0.5 else "explore",
        },
    }
    return state
