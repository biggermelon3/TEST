from __future__ import annotations

import random
from typing import Any


def run_candidate_backtest(candidate: dict[str, Any], config: dict[str, Any], seed: int = 42) -> dict[str, Any]:
    local_seed = seed + int(candidate["candidate_id"].split("-")[-1], 16) % 100_000
    rng = random.Random(local_seed)
    trades = rng.randint(0, 40)
    gross = rng.uniform(-5000, 12000)
    fee = abs(gross) * rng.uniform(0.001, 0.02)
    wins = int(trades * rng.uniform(0.2, 0.7)) if trades else 0
    losses = trades - wins
    status = "success"
    return {
        "candidate_id": candidate["candidate_id"],
        "status": status,
        "seed": local_seed,
        "config": config,
        "trades": trades,
        "wins": wins,
        "losses": losses,
        "gross_pnl": gross,
        "fee_total": fee,
        "equity_curve": [100000 + gross * (i / 10) for i in range(11)],
        "avg_trade_duration": rng.uniform(1.0, 20.0),
    }
