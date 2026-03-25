from __future__ import annotations

from typing import Any

from app.ranking.constraints import RankingConstraints


def normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


def score_candidates(metrics_rows: list[dict[str, Any]], constraints: RankingConstraints) -> list[dict[str, Any]]:
    if not metrics_rows:
        return []
    sharpe_vals = [m["sharpe"] for m in metrics_rows]
    pnl_vals = [m["pnl_after_fee"] for m in metrics_rows]
    pf_vals = [m["profit_factor"] for m in metrics_rows]
    dd_vals = [m["max_drawdown"] for m in metrics_rows]

    for row in metrics_rows:
        fee_ratio = row["fee_total"] / (abs(row["total_pnl"]) + 1e-6)
        low_conf = row["number_of_trades"] < constraints.minimum_trades
        hard_fail = (
            row["number_of_trades"] < constraints.minimum_trades
            or row["max_drawdown"] > constraints.allowed_max_drawdown
            or fee_ratio > constraints.max_fee_ratio
        )
        overtrade_penalty = min(1.0, row["number_of_trades"] / 500)
        score = (
            0.35 * normalize(row["sharpe"], min(sharpe_vals), max(sharpe_vals))
            + 0.30 * normalize(row["pnl_after_fee"], min(pnl_vals), max(pnl_vals))
            + 0.15 * normalize(row["profit_factor"], min(pf_vals), max(pf_vals))
            - 0.15 * normalize(row["max_drawdown"], min(dd_vals), max(dd_vals))
            - 0.05 * overtrade_penalty
        )
        row["score"] = -1.0 if hard_fail else score
        row["low_confidence"] = low_conf
        row["score_breakdown"] = {
            "fee_ratio": fee_ratio,
            "overtrading_penalty": overtrade_penalty,
            "hard_fail": hard_fail,
        }
    return sorted(metrics_rows, key=lambda x: x["score"], reverse=True)
