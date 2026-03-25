from __future__ import annotations

import hashlib
import json
from typing import Any


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _normalize(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    return value


def candidate_hash(strategy_name: str, params: dict[str, Any], logic_switches: dict[str, Any]) -> str:
    payload = {
        "strategy_name": strategy_name,
        "params": _normalize(params),
        "logic_switches": _normalize(logic_switches),
    }
    blob = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
