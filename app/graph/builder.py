from __future__ import annotations

from app.config import ResearchConfig
from app.graph.nodes import (
    compute_metrics,
    decide_next_round,
    deduplicate,
    generate_candidates,
    load_baseline,
    load_state,
    persist_state,
    rank_candidates,
    run_backtests,
    summarize_round,
    validate_candidates,
)
from app.ranking.constraints import RankingConstraints


def run_one_round(state, repo, cfg: ResearchConfig):
    state = load_state.run(state, repo)
    state = load_baseline.run(state)
    state = generate_candidates.run(state, batch_size=cfg.batch_size)
    state = validate_candidates.run(state)
    state = deduplicate.run(state)
    state = run_backtests.run(state, cfg.backtest)
    state = compute_metrics.run(state)
    constraints = RankingConstraints(
        minimum_trades=cfg.minimum_trades,
        allowed_max_drawdown=cfg.max_drawdown_threshold,
        max_fee_ratio=cfg.max_fee_ratio,
    )
    state = rank_candidates.run(state, constraints)
    state = summarize_round.run(state)
    state = decide_next_round.run(state, cfg.max_rounds, cfg.max_total_experiments, cfg.target_score)
    state = persist_state.run(state, repo)
    return state
