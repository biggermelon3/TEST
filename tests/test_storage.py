from app.storage.db import connect, init_db
from app.storage.repositories import ResearchRepository


def test_sqlite_persistence(tmp_path):
    conn = connect(tmp_path / "t.db")
    init_db(conn)
    repo = ResearchRepository(conn)
    sid = repo.create_session("macd_obv_vwap", "random")
    state = {"session_id": sid, "round_index": 1}
    repo.save_snapshot(sid, state)
    assert repo.load_snapshot(sid)["round_index"] == 1
