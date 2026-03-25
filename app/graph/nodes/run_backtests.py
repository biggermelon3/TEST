from __future__ import annotations

from app.backtest.commission import commission_model
from app.backtest.engine import run_candidate_backtest
from app.backtest.slippage import slippage_model
from app.graph.state import ResearchState


def run(state: ResearchState, bt_cfg) -> ResearchState:
    results = []
    for c in state["unique_candidates"]:
        try:
            cfg = {
                "symbol": bt_cfg.symbol,
                "timeframe": bt_cfg.timeframe,
                "start_date": bt_cfg.start_date,
                "end_date": bt_cfg.end_date,
                "commission_model": commission_model(bt_cfg.commission),
                "slippage_model": slippage_model(bt_cfg.slippage),
            }
            results.append(run_candidate_backtest(c, cfg, seed=42))
        except Exception as exc:  # noqa: BLE001
            results.append({"candidate_id": c["candidate_id"], "status": "failed", "error_message": str(exc), "seed": 42, "config": cfg})
    state["backtest_results"] = results
    return state
