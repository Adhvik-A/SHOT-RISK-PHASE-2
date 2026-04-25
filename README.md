## Shot Risk Efficiency API
A cricket analytics engine that evaluates whether a shot type is strategically efficient by balancing scoring probability, dismissal risk, and match context.

## API Objective
Quantifies the expected value of a cricket shot by combining scoring probability, dismissal risk, average reward, and wicket cost based on match situation, providing a normalized efficiency score and actionable classification.

Endpoint

POST /shot-risk
## Input Schema
```json
{
  "player_id": "string (required, unique batter identifier)",
  "match_id": "string (required, unique match identifier)",
  "innings_id": "string (required, unique innings identifier)",
  "shot_type": "string (required, enum: 'drive' | 'pull' | 'cut' | 'sweep' | 'flick' | 'glance' | 'defence' | 'loft' | 'reverse_sweep' | 'other')",
  "total_shots": "integer (required, > 0, total shots played)",
  "scoring_shots": "integer (required, ≥ 0, shots that resulted in runs)",
  "dismissals": "integer (required, 0-10, wickets lost from this shot)",
  "total_runs_from_shot": "float (required, ≥ 0, total runs scored from this shot type)",
  "current_batter_strike_rate": "float (required, ≥ 0, ≤ 500)",
  "incoming_batter_strike_rate": "float (required, ≥ 0, ≤ 500)",
  "balls_remaining": "integer (required, > 0, balls left in innings)",
  "phase": "string (required, enum: 'powerplay' | 'middle' | 'death')",
  "extra_type": "string (optional, enum: 'wide' | 'no_ball' | 'bye' | 'leg_bye')",
  "baseline_runs": "float (optional, > 0, default: 100, baseline run expectation)"
}
Output Schema

{
  "meta": {
    "api": "string",
    "version": "string",
    "status": "string"
  },
  "data": {
    "inputs": {
      "player_id": "string",
      "match_id": "string",
      "innings_id": "string",
      "shot_type": "string",
      "total_shots": "integer",
      "scoring_shots": "integer",
      "dismissals": "integer",
      "total_runs_from_shot": "float",
      "current_batter_strike_rate": "float",
      "incoming_batter_strike_rate": "float",
      "balls_remaining": "integer",
      "phase": "string",
      "extra_type": "string or null",
      "baseline_runs": "float"
    },
    "derived": {
      "p_scoring_probability": "float (0-1)",
      "q_dismissal_probability": "float (0-1)",
      "r_average_reward": "float (runs per shot)",
      "s_wicket_cost": "float (normalized wicket impact)"
    },
    "results": {
      "expected_value_t": "float",
      "shot_efficiency_score": "float (0-100)",
      "classification": "string"
    }
  },
  "errors": "string or null"
}
Classification Values
t ≥ 0.25 → "High Efficiency Shot"

0.1 ≤ t < 0.25 → "Good Shot"

0 ≤ t < 0.1 → "Marginal / Situational Shot"

t < 0 → "High Risk / Poor Shot"

Example Request

{
  "player_id": "VIRAT_KOHLI_018",
  "match_id": "IPL_2024_FINAL",
  "innings_id": "RCB_INN_2",
  "shot_type": "loft",
  "total_shots": 30,
  "scoring_shots": 24,
  "dismissals": 2,
  "total_runs_from_shot": 95,
  "current_batter_strike_rate": 158.3,
  "incoming_batter_strike_rate": 135.0,
  "balls_remaining": 30,
  "phase": "death",
  "extra_type": null,
  "baseline_runs": 100
}

Example Response

{
  "meta": {
    "api": "shot-risk",
    "version": "2.0",
    "status": "success"
  },
  "data": {
    "inputs": {
      "player_id": "VIRAT_KOHLI_018",
      "match_id": "IPL_2024_FINAL",
      "innings_id": "RCB_INN_2",
      "shot_type": "loft",
      "total_shots": 30,
      "scoring_shots": 24,
      "dismissals": 2,
      "total_runs_from_shot": 95,
      "current_batter_strike_rate": 158.3,
      "incoming_batter_strike_rate": 135.0,
      "balls_remaining": 30,
      "phase": "death",
      "extra_type": null,
      "baseline_runs": 100
    },
    "derived": {
      "p_scoring_probability": 0.8,
      "q_dismissal_probability": 0.067,
      "r_average_reward": 3.167,
      "s_wicket_cost": 0.078
    },
    "results": {
      "expected_value_t": 0.256,
      "shot_efficiency_score": 62.8,
      "classification": "High Efficiency Shot"
    }
  },
  "errors": null
}
Validation Errors
scoring_shots Exceeds total_shots
json
{
  "detail": "scoring_shots (20) cannot exceed total_shots (15)"
}
Status: 422 Unprocessable Entity

dismissals Exceeds total_shots
json
{
  "detail": "dismissals (8) cannot exceed total_shots (5)"
}
Status: 422 Unprocessable Entity

Empty ID Fields
json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "player_id"],
      "msg": "Value error, ID fields cannot be blank or whitespace",
      "input": ""
    }
  ]
}
Status: 422 Unprocessable Entity

Strike Rate Exceeds 500
json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "current_batter_strike_rate"],
      "msg": "Value error, Strike rate cannot exceed 500",
      "input": 600.0
    }
  ]
}
Status: 422 Unprocessable Entity

Integration Usage
Python
python
import requests

url = "http://your-api.com/shot-risk"

payload = {
    "player_id": "VIRAT_KOHLI_018",
    "match_id": "IPL_2024_FINAL",
    "innings_id": "RCB_INN_2",
    "shot_type": "loft",
    "total_shots": 30,
    "scoring_shots": 24,
    "dismissals": 2,
    "total_runs_from_shot": 95,
    "current_batter_strike_rate": 158.3,
    "incoming_batter_strike_rate": 135.0,
    "balls_remaining": 30,
    "phase": "death",
    "extra_type": None,
    "baseline_runs": 100
}

response = requests.post(url, json=payload)
print(response.json())
JavaScript / Node.js
javascript
const payload = {
    player_id: "VIRAT_KOHLI_018",
    match_id: "IPL_2024_FINAL",
    innings_id: "RCB_INN_2",
    shot_type: "loft",
    total_shots: 30,
    scoring_shots: 24,
    dismissals: 2,
    total_runs_from_shot: 95,
    current_batter_strike_rate: 158.3,
    incoming_batter_strike_rate: 135.0,
    balls_remaining: 30,
    phase: "death",
    extra_type: null,
    baseline_runs: 100
};

const response = await fetch("http://your-api.com/shot-risk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
});

const data = await response.json();
console.log(data);
cURL
bash
curl -X POST http://your-api.com/shot-risk \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": "VIRAT_KOHLI_018",
    "match_id": "IPL_2024_FINAL",
    "innings_id": "RCB_INN_2",
    "shot_type": "loft",
    "total_shots": 30,
    "scoring_shots": 24,
    "dismissals": 2,
    "total_runs_from_shot": 95,
    "current_batter_strike_rate": 158.3,
    "incoming_batter_strike_rate": 135.0,
    "balls_remaining": 30,
    "phase": "death",
    "extra_type": null,
    "baseline_runs": 100
  }'



## Conclusion
The Shot Risk Efficiency API provides a sophisticated, data-driven framework for evaluating shot selection in cricket. By combining scoring probability (p), dismissal risk (q), average reward (r), and context-aware wicket cost (s), the engine calculates an expected value (t) that reflects the true strategic worth of a shot type. The non-linear dismissal penalty and phase-adjusted wicket impact ensure that high-risk shots in critical match situations are properly penalized. The final efficiency score (0-100) and classification ("High Efficiency Shot" to "High Risk / Poor Shot") offer immediate, actionable insights for players, coaches, and analysts to optimize batting strategy and shot selection.

