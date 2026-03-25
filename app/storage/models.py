from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Session:
    session_id: str
    created_at: str
    status: str
    baseline_strategy_id: str
    search_mode: str
    notes: str = ""
