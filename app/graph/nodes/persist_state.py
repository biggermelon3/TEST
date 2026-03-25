from __future__ import annotations

from app.graph.state import ResearchState


def run(state: ResearchState, repo) -> ResearchState:
    repo.persist_round(state)
    repo.save_snapshot(state["session_id"], state)
    return state
