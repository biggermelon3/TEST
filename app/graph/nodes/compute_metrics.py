from __future__ import annotations

from app.backtest.analyzers import compute_basic_metrics
from app.graph.state import ResearchState


def run(state: ResearchState) -> ResearchState:
    metrics_rows = []
    for b in state["backtest_results"]:
        if b["status"] != "success":
            continue
        m = compute_basic_metrics(b)
        m["candidate_id"] = b["candidate_id"]
        metrics_rows.append(m)
    state["ranked_results"] = metrics_rows
    return state
