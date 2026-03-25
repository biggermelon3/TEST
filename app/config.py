from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class BacktestConfig:
    symbol: str = "DEMO"
    timeframe: str = "1D"
    start_date: str = "2020-01-01"
    end_date: str = "2022-12-31"
    initial_cash: float = 100_000.0
    commission: float = 0.0005
    slippage: float = 0.0002
    margin: float = 1.0
    multiplier: float = 1.0
    allow_long: bool = True
    allow_short: bool = False


@dataclass(slots=True)
class ResearchConfig:
    db_path: Path = Path("data/research.db")
    artifacts_dir: Path = Path("artifacts")
    batch_size: int = 12
    max_rounds: int = 5
    max_total_experiments: int = 100
    stale_rounds_stop: int = 2
    target_score: float = 0.9
    minimum_trades: int = 5
    max_drawdown_threshold: float = 0.4
    max_fee_ratio: float = 0.5
    search_mode: str = "random"
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
