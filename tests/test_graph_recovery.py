from app.config import ResearchConfig
from app.graph.builder import run_one_round
from app.storage.db import connect, init_db
from app.storage.repositories import ResearchRepository


def test_graph_can_resume(tmp_path):
    conn = connect(tmp_path / "resume.db")
    init_db(conn)
    repo = ResearchRepository(conn)
    sid = repo.create_session("macd_obv_vwap", "random")
    state = {
        "session_id": sid,
        "round_index": 1,
        "baseline_strategy_id": "",
        "search_mode": "random",
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
    repo.save_snapshot(sid, state)
    out = run_one_round(state, repo, ResearchConfig(batch_size=10))
    repo.save_snapshot(sid, out)
    resumed = repo.load_snapshot(sid)
    assert resumed["session_id"] == sid
    assert len(resumed["candidate_batch"]) == 10
