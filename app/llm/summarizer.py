from __future__ import annotations


def summarize_with_llm(payload: dict) -> dict:
    return {"summary": "LLM summary disabled in phase 1", "input_size": len(str(payload))}
