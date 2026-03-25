from app.graph.nodes.validate_candidates import run


def test_validation_rejects_invalid_macd():
    state = {
        "candidate_batch": [
            {
                "candidate_id": "1",
                "strategy_name": "s",
                "param_dict": {
                    "macd_fast": 30,
                    "macd_slow": 20,
                    "vwap_window": 20,
                    "vwap_stdev_window": 20,
                    "target_deviation_multiplier": 1.0,
                    "stop_buffer": 0.5,
                    "safety_exit_opposing_bars": 2,
                },
                "logic_switches": {},
            }
        ],
        "validated_candidates": [],
        "rejected_candidates": [],
    }
    out = run(state)
    assert len(out["validated_candidates"]) == 0
    assert len(out["rejected_candidates"]) == 1
