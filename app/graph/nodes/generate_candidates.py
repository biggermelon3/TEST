from __future__ import annotations

import random
import uuid

from app.graph.state import ResearchState
from app.strategies.mutations import random_mutation


def run(state: ResearchState, batch_size: int = 12) -> ResearchState:
    rng = random.Random(state["round_index"] + 7)
    base = state["_baseline"]
    candidates = []
    for _ in range(batch_size):
        cid = str(uuid.uuid4())
        candidates.append(
            {
                "candidate_id": cid,
                "parent_candidate_id": None,
                "strategy_name": base["strategy_name"],
                "param_dict": random_mutation(base["params"], rng),
                "logic_switches": dict(base["logic_switches"]),
                "rationale": "random neighborhood mutation",
                "proposed_by": "rule",
            }
        )
    state["candidate_batch"] = candidates
    return state
