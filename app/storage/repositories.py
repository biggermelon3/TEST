from __future__ import annotations

import uuid
from typing import Any

from app.utils.serialization import from_json, to_json
from app.utils.time import utc_now_iso


class ResearchRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_session(self, strategy_id: str, search_mode: str) -> str:
        session_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO sessions(session_id, created_at, status, baseline_strategy_id, search_mode, notes) VALUES(?,?,?,?,?,?)",
            (session_id, utc_now_iso(), "active", strategy_id, search_mode, ""),
        )
        self.conn.commit()
        return session_id

    def session_exists(self, session_id: str) -> bool:
        row = self.conn.execute("SELECT session_id FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        return row is not None

    def load_snapshot(self, session_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT state_json FROM state_snapshots WHERE session_id=?", (session_id,)).fetchone()
        return from_json(row[0]) if row else None

    def save_snapshot(self, session_id: str, state: dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT INTO state_snapshots(session_id, state_json, updated_at) VALUES(?,?,?) "
            "ON CONFLICT(session_id) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at",
            (session_id, to_json(state), utc_now_iso()),
        )
        self.conn.commit()

    def list_hashes(self, session_id: str) -> set[str]:
        rows = self.conn.execute(
            "SELECT c.hash FROM candidates c JOIN rounds r ON c.round_id=r.round_id WHERE r.session_id=?",
            (session_id,),
        ).fetchall()
        return {r[0] for r in rows}

    def persist_round(self, state: dict[str, Any]) -> None:
        round_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO rounds(round_id, session_id, round_index, started_at, finished_at, summary_markdown, summary_json, decision, stop_reason) VALUES(?,?,?,?,?,?,?,?,?)",
            (
                round_id,
                state["session_id"],
                state["round_index"],
                utc_now_iso(),
                utc_now_iso(),
                state["round_summary"].get("markdown", ""),
                to_json(state["round_summary"]),
                state["next_round_plan"].get("decision", "explore"),
                state.get("stop_reason"),
            ),
        )
        for c in state["validated_candidates"] + state["rejected_candidates"]:
            self.conn.execute(
                "INSERT OR REPLACE INTO candidates(candidate_id, round_id, parent_candidate_id, hash, strategy_name, params_json, logic_switches_json, rationale, proposed_by, validation_status, validation_reason) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    c["candidate_id"],
                    round_id,
                    c.get("parent_candidate_id"),
                    c["hash"],
                    c["strategy_name"],
                    to_json(c["param_dict"]),
                    to_json(c["logic_switches"]),
                    c.get("rationale", ""),
                    c.get("proposed_by", "rule"),
                    c.get("validation_status", "valid"),
                    c.get("validation_reason", ""),
                ),
            )
        for b in state["backtest_results"]:
            self.conn.execute(
                "INSERT OR REPLACE INTO backtests(backtest_id, candidate_id, symbol, timeframe, start_date, end_date, commission_model_json, slippage_model_json, seed, status, error_message) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    str(uuid.uuid4()),
                    b["candidate_id"],
                    b["config"]["symbol"],
                    b["config"]["timeframe"],
                    b["config"]["start_date"],
                    b["config"]["end_date"],
                    to_json(b["config"]["commission_model"]),
                    to_json(b["config"]["slippage_model"]),
                    b["seed"],
                    b["status"],
                    b.get("error_message"),
                ),
            )
        for m in state["ranked_results"]:
            self.conn.execute(
                "INSERT OR REPLACE INTO metrics(metric_id, candidate_id, total_pnl, sharpe, sortino, max_drawdown, win_rate, avg_win, avg_loss, profit_factor, expectancy, num_trades, exposure, fee_total, pnl_after_fee, score) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    str(uuid.uuid4()),
                    m["candidate_id"],
                    m["total_pnl"],
                    m["sharpe"],
                    m["sortino"],
                    m["max_drawdown"],
                    m["win_rate"],
                    m["avg_win"],
                    m["avg_loss"],
                    m["profit_factor"],
                    m["expectancy"],
                    m["number_of_trades"],
                    m["exposure"],
                    m["fee_total"],
                    m["pnl_after_fee"],
                    m["score"],
                ),
            )
        self.conn.commit()

    def top_results(self, session_id: str, top_n: int = 10) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT m.candidate_id, m.score, m.pnl_after_fee, m.sharpe FROM metrics m "
            "JOIN candidates c ON m.candidate_id=c.candidate_id "
            "JOIN rounds r ON c.round_id=r.round_id WHERE r.session_id=? ORDER BY m.score DESC LIMIT ?",
            (session_id, top_n),
        ).fetchall()
        return [dict(r) for r in rows]
