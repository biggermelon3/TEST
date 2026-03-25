from __future__ import annotations

from dataclasses import asdict

from app.strategies.base import BaseStrategy, StrategyConfig
from app.strategies.parameter_schema import StrategyParameters, StrategySwitches


class MacdObvVwapStrategy(BaseStrategy):
    strategy_name = "macd_obv_vwap"

    @classmethod
    def default_config(cls) -> StrategyConfig:
        params = StrategyParameters()
        switches = StrategySwitches()
        return StrategyConfig(
            strategy_name=cls.strategy_name,
            params=asdict(params),
            logic_switches=asdict(switches),
        )
