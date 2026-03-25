from __future__ import annotations


def commission_model(rate: float) -> dict[str, float]:
    return {"type": "percent", "rate": rate}
