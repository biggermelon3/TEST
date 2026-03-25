from __future__ import annotations

import argparse
from typing import Any

from app.config import ResearchConfig
from app.graph.builder import run_one_round
from app.storage.db import connect, init_db
from app.storage.repositories import ResearchRepository


def _base_state(session_id: str, search_mode: str) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "round_index": 1,
        "baseline_strategy_id": "",
        "search_mode": search_mode,
        "candidate_batch": [],
        "validated_candidates": [],
        "rejected_candidates": [],
        "unique_candidates": [],
        "backtest_results": [],
        "ranked_results": [],
        "round_summary": {},
        "next_round_plan": {},
        "tried_hashes": [],
        "top_results": [],
        "stop_reason": None,
    }


def cmd_init_db() -> None:
    cfg = ResearchConfig()
    conn = connect(cfg.db_path)
    init_db(conn)
    print(f"Initialized DB at {cfg.db_path}")


def cmd_new_session(strategy: str, search_mode: str) -> None:
    cfg = ResearchConfig(search_mode=search_mode)
    conn = connect(cfg.db_path)
    init_db(conn)
    repo = ResearchRepository(conn)
    sid = repo.create_session(strategy, search_mode)
    repo.save_snapshot(sid, _base_state(sid, search_mode))
    print(sid)


def cmd_run_round(session: str) -> None:
    cfg = ResearchConfig()
    conn = connect(cfg.db_path)
    repo = ResearchRepository(conn)
    state = repo.load_snapshot(session) or _base_state(session, cfg.search_mode)
    state = run_one_round(state, repo, cfg)
    state["round_index"] += 1
    repo.save_snapshot(session, state)
    print(state["round_summary"].get("markdown", "done"))


def cmd_run_loop(session: str) -> None:
    cfg = ResearchConfig()
    conn = connect(cfg.db_path)
    repo = ResearchRepository(conn)
    state = repo.load_snapshot(session) or _base_state(session, cfg.search_mode)
    while True:
        state = run_one_round(state, repo, cfg)
        if state["next_round_plan"]["decision"] == "stop":
            break
        state["round_index"] += 1
    repo.save_snapshot(session, state)
    print(f"Stopped: {state.get('stop_reason')}")


def cmd_top_results(session: str, top: int) -> None:
    cfg = ResearchConfig()
    conn = connect(cfg.db_path)
    repo = ResearchRepository(conn)
    for row in repo.top_results(session, top):
        print(row)


def cmd_export_report(session: str) -> None:
    cfg = ResearchConfig()
    conn = connect(cfg.db_path)
    repo = ResearchRepository(conn)
    snapshot = repo.load_snapshot(session)
    if not snapshot:
        raise SystemExit(1)
    print(snapshot.get("round_summary", {}).get("markdown", "No report"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m app.main")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db")

    ns = sub.add_parser("new-session")
    ns.add_argument("--strategy", default="macd_obv_vwap")
    ns.add_argument("--search-mode", default="random")

    rr = sub.add_parser("run-round")
    rr.add_argument("--session", required=True)

    rl = sub.add_parser("run-loop")
    rl.add_argument("--session", required=True)

    tr = sub.add_parser("top-results")
    tr.add_argument("--session", required=True)
    tr.add_argument("--top", type=int, default=10)

    er = sub.add_parser("export-report")
    er.add_argument("--session", required=True)

    args = parser.parse_args()
    if args.command == "init-db":
        cmd_init_db()
    elif args.command == "new-session":
        cmd_new_session(args.strategy, args.search_mode)
    elif args.command == "run-round":
        cmd_run_round(args.session)
    elif args.command == "run-loop":
        cmd_run_loop(args.session)
    elif args.command == "top-results":
        cmd_top_results(args.session, args.top)
    elif args.command == "export-report":
        cmd_export_report(args.session)


if __name__ == "__main__":
    main()
