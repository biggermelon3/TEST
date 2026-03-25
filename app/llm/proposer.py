from __future__ import annotations


def propose_with_llm(history: dict) -> dict:
    return {"candidates": [], "fallback": "rule_generator"}
