from __future__ import annotations

from app.graph.state import ResearchState
from app.ranking.constraints import RankingConstraints
from app.ranking.scorer import score_candidates


def run(state: ResearchState, constraints: RankingConstraints) -> ResearchState:
    ranked = score_candidates(state["ranked_results"], constraints)
    state["ranked_results"] = ranked
    state["top_results"] = ranked[:10]
    return state
