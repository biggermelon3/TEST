from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RankingConstraints:
    minimum_trades: int = 5
    allowed_max_drawdown: float = 0.4
    max_fee_ratio: float = 0.5
