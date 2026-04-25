from fastapi import HTTPException
from utils import (
    calculate_probabilities,
    calculate_average_reward,
    calculate_wicket_cost,
    calculate_expected_value,
    calculate_efficiency_score,
    classify_shot,
)


def process_shot_risk(payload: dict):
    # ── Extract fields ────────────────────────────────────────────────────────
    total_shots   = payload.get("total_shots")
    scoring_shots = payload.get("scoring_shots")
    dismissals    = payload.get("dismissals")
    total_runs    = payload.get("total_runs_from_shot")

    current_sr      = payload.get("current_batter_strike_rate")
    new_sr          = payload.get("incoming_batter_strike_rate")
    balls_remaining = payload.get("balls_remaining")
    phase           = payload.get("phase")
    baseline        = payload.get("baseline_runs", 100)

    # ── Runtime logic guards ──────────────────────────────────────────────────
    if scoring_shots > total_shots:
        raise HTTPException(
            status_code=400,
            detail=f"scoring_shots ({scoring_shots}) cannot exceed total_shots ({total_shots})",
        )

    if dismissals > total_shots:
        raise HTTPException(
            status_code=400,
            detail=f"dismissals ({dismissals}) cannot exceed total_shots ({total_shots})",
        )

    # ── Derived metrics ───────────────────────────────────────────────────────
    p, q = calculate_probabilities(total_shots, scoring_shots, dismissals)
    r    = calculate_average_reward(total_runs, total_shots)
    s    = calculate_wicket_cost(current_sr, new_sr, balls_remaining, phase, baseline)

    # ── Final EV ──────────────────────────────────────────────────────────────
    t     = calculate_expected_value(p, q, r, s)
    score = calculate_efficiency_score(t)
    label = classify_shot(t)

    # ── Standard response  { meta, data: { inputs, derived, results }, errors } ─
    return {
        "meta": {
            "api":     "shot-risk",
            "version": "2.0",
            "status":  "success",
        },
        "data": {
            "inputs": {
                "player_id":                   payload.get("player_id"),
                "match_id":                    payload.get("match_id"),
                "innings_id":                  payload.get("innings_id"),
                "shot_type":                   payload.get("shot_type"),
                "total_shots":                 total_shots,
                "scoring_shots":               scoring_shots,
                "dismissals":                  dismissals,
                "total_runs_from_shot":        total_runs,
                "current_batter_strike_rate":  current_sr,
                "incoming_batter_strike_rate": new_sr,
                "balls_remaining":             balls_remaining,
                "phase":                       phase,
                "extra_type":                  payload.get("extra_type"),
                "baseline_runs":               baseline,
            },
            "derived": {
                "p_scoring_probability":   round(p, 3),
                "q_dismissal_probability": round(q, 3),
                "r_average_reward":        round(r, 3),
                "s_wicket_cost":           round(s, 3),
            },
            "results": {
                "expected_value_t":      round(t, 3),
                "shot_efficiency_score": round(score, 2),
                "classification":        label,
            },
        },
        "errors": None,
    }