from __future__ import annotations

from app.graph.state import ResearchState
from app.utils.hashing import candidate_hash


def run(state: ResearchState) -> ResearchState:
    seen = set(state["tried_hashes"])
    unique = []
    for c in state["validated_candidates"]:
        h = candidate_hash(c["strategy_name"], c["param_dict"], c["logic_switches"])
        c["hash"] = h
        if h in seen:
            c["validation_status"] = "duplicate"
            c["validation_reason"] = "already tested"
            state["rejected_candidates"].append(c)
            continue
        seen.add(h)
        unique.append(c)
    state["unique_candidates"] = unique
    state["tried_hashes"] = list(seen)
    return state
