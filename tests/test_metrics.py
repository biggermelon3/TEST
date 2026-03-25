from app.backtest.analyzers import compute_basic_metrics


def test_metrics_contains_required_fields():
    result = {
        "trades": 10,
        "wins": 6,
        "losses": 4,
        "gross_pnl": 1000,
        "fee_total": 10,
        "equity_curve": [100000, 101000],
        "avg_trade_duration": 5,
    }
    metrics = compute_basic_metrics(result)
    assert "sharpe" in metrics
    assert metrics["pnl_after_fee"] == 990
