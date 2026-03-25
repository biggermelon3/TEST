from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class StrategyConfig:
    strategy_name: str
    params: dict[str, Any]
    logic_switches: dict[str, Any]


class BaseStrategy:
    strategy_name = "base"

    @classmethod
    def default_config(cls) -> StrategyConfig:
        raise NotImplementedError
