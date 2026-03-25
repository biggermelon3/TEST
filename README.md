# strategy-rnd-agent

Phase-1 research loop for strategy R&D using Python 3.11+, SQLite, and a LangGraph-style node workflow.

## Features
- Session-based experiment tracking with resume support.
- Candidate generation, validation, deduplication (stable hash).
- Deterministic backtest engine stub (pluggable with Backtrader).
- Metrics computation, multi-objective ranking, round summaries.
- SQLite persistence for sessions/rounds/candidates/backtests/metrics/state snapshots.
- CLI for init, session management, run-round, run-loop, top-results, export-report.
- Phase-2 placeholders: IBKR adapter, TradingView webhook, paper loop.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quick start
```bash
python -m app.main init-db
SESSION_ID=$(python -m app.main new-session --strategy macd_obv_vwap)
python -m app.main run-round --session "$SESSION_ID"
python -m app.main top-results --session "$SESSION_ID" --top 5
python -m app.main export-report --session "$SESSION_ID"
```

## Notes
- Current phase uses a deterministic simulator in `app/backtest/engine.py` to keep tests fast and reproducible.
- Architecture is organized so this engine can be swapped for Backtrader integration later.
