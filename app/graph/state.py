from __future__ import annotations

from typing import Any, TypedDict


class ResearchState(TypedDict):
    session_id: str
    round_index: int
    baseline_strategy_id: str
    search_mode: str
    candidate_batch: list[dict[str, Any]]
    validated_candidates: list[dict[str, Any]]
    rejected_candidates: list[dict[str, Any]]
    unique_candidates: list[dict[str, Any]]
    backtest_results: list[dict[str, Any]]
    ranked_results: list[dict[str, Any]]
    round_summary: dict[str, Any]
    next_round_plan: dict[str, Any]
    tried_hashes: list[str]
    top_results: list[dict[str, Any]]
    stop_reason: str | None
