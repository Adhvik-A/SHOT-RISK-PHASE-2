from pydantic import BaseModel, Field
from typing import Dict


class ShotRiskRequest(BaseModel):
    total_shots: int = Field(..., gt=0)
    scoring_shots: int = Field(..., ge=0)
    dismissals: int = Field(..., ge=0)
    total_runs_from_shot: float = Field(..., ge=0)

    current_batter_strike_rate: float = Field(..., ge=0)
    incoming_batter_strike_rate: float = Field(..., ge=0)
    balls_remaining: int = Field(..., ge=0)
    phase: str = Field(...)

    baseline_runs: float = Field(100, gt=0)


class DerivedMetrics(BaseModel):
    p_scoring_probability: float
    q_dismissal_probability: float
    r_average_reward: float
    s_wicket_cost: float


class ShotRiskResult(BaseModel):
    expected_value_t: float
    shot_efficiency_score: float
    classification: str


class ShotRiskResponse(BaseModel):
    inputs: Dict
    derived: DerivedMetrics
    results: ShotRiskResult