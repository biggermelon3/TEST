from __future__ import annotations

from typing import Any


def compute_basic_metrics(result: dict[str, Any]) -> dict[str, float]:
    trades = max(result["trades"], 1)
    pnl_after_fee = result["gross_pnl"] - result["fee_total"]
    win_rate = result["wins"] / trades
    avg_win = max(result["gross_pnl"], 0) / max(result["wins"], 1)
    avg_loss = min(result["gross_pnl"], 0) / max(result["losses"], 1)
    profit_factor = (avg_win * max(result["wins"], 1)) / abs(avg_loss * max(result["losses"], 1) or 1)
    expectancy = pnl_after_fee / trades
    drawdown = min(0.95, abs(min(result["equity_curve"]) - max(result["equity_curve"])) / max(result["equity_curve"]))
    sharpe = pnl_after_fee / 10000
    sortino = sharpe * 1.1
    return {
        "total_pnl": result["gross_pnl"],
        "annualized_return": pnl_after_fee / 100000,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": drawdown,
        "calmar": (pnl_after_fee / 100000) / max(drawdown, 1e-6),
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_factor": profit_factor,
        "expectancy": expectancy,
        "number_of_trades": result["trades"],
        "avg_trade_duration": result["avg_trade_duration"],
        "exposure": min(1.0, result["trades"] / 100),
        "turnover": result["trades"] * 2,
        "fee_total": result["fee_total"],
        "pnl_after_fee": pnl_after_fee,
    }
