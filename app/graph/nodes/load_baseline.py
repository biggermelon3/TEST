from __future__ import annotations

from app.graph.state import ResearchState
from app.strategies.macd_obv_vwap import MacdObvVwapStrategy


def run(state: ResearchState) -> ResearchState:
    baseline = MacdObvVwapStrategy.default_config()
    state["baseline_strategy_id"] = baseline.strategy_name
    state["candidate_batch"] = []
    state["_baseline"] = {
        "strategy_name": baseline.strategy_name,
        "params": baseline.params,
        "logic_switches": baseline.logic_switches,
    }
    return state
