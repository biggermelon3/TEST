from __future__ import annotations


def slippage_model(rate: float) -> dict[str, float]:
    return {"type": "percent", "rate": rate}
