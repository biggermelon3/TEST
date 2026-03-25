from app.backtest.engine import run_candidate_backtest


def test_backtest_runs():
    candidate = {"candidate_id": "00000000-0000-0000-0000-000000000001"}
    cfg = {
        "symbol": "DEMO",
        "timeframe": "1D",
        "start_date": "2020-01-01",
        "end_date": "2020-12-31",
        "commission_model": {"rate": 0.001},
        "slippage_model": {"rate": 0.0},
    }
    res = run_candidate_backtest(candidate, cfg)
    assert res["status"] == "success"
