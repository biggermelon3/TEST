from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExitMode = Literal["vwap", "deviation_band", "dynamic_target"]


@dataclass(slots=True)
class StrategyParameters:
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    obv_threshold: float = 0.0
    vwap_window: int = 20
    vwap_stdev_window: int = 20
    stop_buffer: float = 0.5
    safety_exit_opposing_bars: int = 2
    target_deviation_multiplier: float = 1.5
    cooldown_bars: int = 0
    exit_mode: ExitMode = "vwap"


@dataclass(slots=True)
class StrategySwitches:
    entry_macd_on: bool = True
    entry_obv_filter_on: bool = True
    entry_vwap_distance_filter_on: bool = False
    exit_stop_loss_on: bool = True
    exit_safety_on: bool = True
    max_one_position: bool = True
