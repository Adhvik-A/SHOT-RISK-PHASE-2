from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Optional
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class PhaseEnum(str, Enum):
    powerplay = "powerplay"
    middle    = "middle"
    death     = "death"


class ExtraTypeEnum(str, Enum):
    wide     = "wide"
    no_ball  = "no_ball"
    bye      = "bye"
    leg_bye  = "leg_bye"


class ShotTypeEnum(str, Enum):
    drive         = "drive"
    pull          = "pull"
    cut           = "cut"
    sweep         = "sweep"
    flick         = "flick"
    glance        = "glance"
    defence       = "defence"
    loft          = "loft"
    reverse_sweep = "reverse_sweep"
    other         = "other"


# ─── Request ──────────────────────────────────────────────────────────────────

class ShotRiskRequest(BaseModel):

    # Identifiers
    player_id:  str = Field(..., description="Unique identifier for the batter")
    match_id:   str = Field(..., description="Unique identifier for the match")
    innings_id: str = Field(..., description="Unique identifier for the innings")

    # Shot classification
    shot_type: ShotTypeEnum = Field(
        ..., description="Type of shot played (drive | pull | cut | sweep | …)"
    )

    # Shot stats
    total_shots:          int   = Field(..., gt=0,        description="Total shots played — must be > 0")
    scoring_shots:        int   = Field(..., ge=0,        description="Shots that resulted in runs")
    dismissals:           int   = Field(..., ge=0, le=10, description="Wickets lost — max 10")
    total_runs_from_shot: float = Field(..., ge=0,        description="Total runs scored from this shot type")

    # Context
    current_batter_strike_rate:  float     = Field(..., ge=0)
    incoming_batter_strike_rate: float     = Field(..., ge=0)
    balls_remaining:             int       = Field(..., gt=0, description="Balls left — must be > 0")
    phase:                       PhaseEnum = Field(...,       description="powerplay | middle | death")

    # Optional
    extra_type:    Optional[ExtraTypeEnum] = Field(None, description="wide | no_ball | bye | leg_bye")
    baseline_runs: float                   = Field(100,  gt=0, description="Baseline run expectation (default 100)")

    # ── Field-level validators ────────────────────────────────────────────────

    @field_validator("player_id", "match_id", "innings_id")
    @classmethod
    def ids_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("ID fields cannot be blank or whitespace")
        return v.strip()

    @field_validator("current_batter_strike_rate", "incoming_batter_strike_rate")
    @classmethod
    def strike_rate_ceiling(cls, v: float) -> float:
        if v > 500:
            raise ValueError("Strike rate cannot exceed 500")
        return v

    # ── Cross-field (model-level) validators ──────────────────────────────────

    @model_validator(mode="after")
    def check_shot_logic_consistency(self) -> "ShotRiskRequest":
        if self.scoring_shots > self.total_shots:
            raise ValueError(
                f"scoring_shots ({self.scoring_shots}) cannot exceed "
                f"total_shots ({self.total_shots})"
            )
        if self.dismissals > self.total_shots:
            raise ValueError(
                f"dismissals ({self.dismissals}) cannot exceed "
                f"total_shots ({self.total_shots})"
            )
        return self


# ─── Derived / Result sub-models ──────────────────────────────────────────────

class DerivedMetrics(BaseModel):
    p_scoring_probability:   float
    q_dismissal_probability: float
    r_average_reward:        float
    s_wicket_cost:           float


class ShotRiskResult(BaseModel):
    expected_value_t:      float
    shot_efficiency_score: float
    classification:        str


# ─── Inner data payload  { inputs, derived, results } ────────────────────────

class ShotRiskData(BaseModel):
    inputs:  Dict
    derived: DerivedMetrics
    results: ShotRiskResult


# ─── Standard response wrapper ───────────────────────────────────────────────
#
#  {
#    "meta":   { "api": "...", "version": "...", "status": "..." },
#    "data":   { "inputs": {}, "derived": {}, "results": {} },
#    "errors": null
#  }

class Meta(BaseModel):
    api:     str
    version: str
    status:  str


class ShotRiskResponse(BaseModel):
    meta:   Meta
    data:   ShotRiskData
    errors: Optional[str] = None