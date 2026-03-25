from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL,
  baseline_strategy_id TEXT NOT NULL,
  search_mode TEXT NOT NULL,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS rounds (
  round_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  round_index INTEGER NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  summary_markdown TEXT,
  summary_json TEXT,
  decision TEXT,
  stop_reason TEXT
);
CREATE TABLE IF NOT EXISTS candidates (
  candidate_id TEXT PRIMARY KEY,
  round_id TEXT NOT NULL,
  parent_candidate_id TEXT,
  hash TEXT NOT NULL,
  strategy_name TEXT NOT NULL,
  params_json TEXT NOT NULL,
  logic_switches_json TEXT NOT NULL,
  rationale TEXT,
  proposed_by TEXT NOT NULL,
  validation_status TEXT NOT NULL,
  validation_reason TEXT
);
CREATE TABLE IF NOT EXISTS backtests (
  backtest_id TEXT PRIMARY KEY,
  candidate_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  timeframe TEXT NOT NULL,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL,
  commission_model_json TEXT NOT NULL,
  slippage_model_json TEXT NOT NULL,
  seed INTEGER NOT NULL,
  status TEXT NOT NULL,
  error_message TEXT
);
CREATE TABLE IF NOT EXISTS metrics (
  metric_id TEXT PRIMARY KEY,
  candidate_id TEXT NOT NULL,
  total_pnl REAL,
  sharpe REAL,
  sortino REAL,
  max_drawdown REAL,
  win_rate REAL,
  avg_win REAL,
  avg_loss REAL,
  profit_factor REAL,
  expectancy REAL,
  num_trades INTEGER,
  exposure REAL,
  fee_total REAL,
  pnl_after_fee REAL,
  score REAL
);
CREATE TABLE IF NOT EXISTS artifacts (
  artifact_id TEXT PRIMARY KEY,
  candidate_id TEXT,
  artifact_type TEXT NOT NULL,
  path TEXT NOT NULL,
  metadata_json TEXT
);
CREATE TABLE IF NOT EXISTS state_snapshots (
  session_id TEXT PRIMARY KEY,
  state_json TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()
