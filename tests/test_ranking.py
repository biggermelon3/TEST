from app.ranking.constraints import RankingConstraints
from app.ranking.scorer import score_candidates


def test_ranking_is_deterministic():
    rows = [
        {"candidate_id": "a", "sharpe": 1.0, "pnl_after_fee": 100, "profit_factor": 1.3, "max_drawdown": 0.1, "number_of_trades": 10, "fee_total": 2, "total_pnl": 120, "sortino": 1.1, "win_rate": 0.5, "avg_win": 2, "avg_loss": -1, "expectancy": 0.5, "exposure": 0.1},
        {"candidate_id": "b", "sharpe": 0.5, "pnl_after_fee": 50, "profit_factor": 1.1, "max_drawdown": 0.2, "number_of_trades": 10, "fee_total": 2, "total_pnl": 60, "sortino": 0.7, "win_rate": 0.4, "avg_win": 1.5, "avg_loss": -1.2, "expectancy": 0.2, "exposure": 0.2},
    ]
    ranked = score_candidates(rows, RankingConstraints())
    assert ranked[0]["candidate_id"] == "a"
