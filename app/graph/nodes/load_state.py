from __future__ import annotations

from app.graph.state import ResearchState


def run(state: ResearchState, repo) -> ResearchState:
    snapshot = repo.load_snapshot(state["session_id"])
    if snapshot:
        return snapshot
    state["tried_hashes"] = list(repo.list_hashes(state["session_id"]))
    return state
