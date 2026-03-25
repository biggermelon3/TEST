from __future__ import annotations

import random
from typing import Any


def random_mutation(base_params: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    p = dict(base_params)
    p["macd_fast"] = max(2, p["macd_fast"] + rng.randint(-2, 2))
    p["macd_slow"] = max(p["macd_fast"] + 1, p["macd_slow"] + rng.randint(-3, 3))
    p["vwap_window"] = max(2, p["vwap_window"] + rng.randint(-4, 4))
    p["stop_buffer"] = max(0.0, round(p["stop_buffer"] + rng.uniform(-0.2, 0.2), 4))
    p["safety_exit_opposing_bars"] = max(1, p["safety_exit_opposing_bars"] + rng.randint(-1, 1))
    p["target_deviation_multiplier"] = max(0.1, round(p["target_deviation_multiplier"] + rng.uniform(-0.2, 0.2), 4))
    p["exit_mode"] = rng.choice(["vwap", "deviation_band", "dynamic_target"])
    return p
