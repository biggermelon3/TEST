from app.utils.hashing import candidate_hash


def test_hash_stable_against_key_order():
    p1 = {"a": 1, "b": 2}
    p2 = {"b": 2, "a": 1}
    l1 = {"x": True, "y": False}
    l2 = {"y": False, "x": True}
    assert candidate_hash("s", p1, l1) == candidate_hash("s", p2, l2)
