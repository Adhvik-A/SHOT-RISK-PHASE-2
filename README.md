#  Shot Risk Efficiency API
---

##  Objective

This API evaluates whether a cricket shot is **strategically worth playing** using principles from **Expected Value and Decision Theory**.

Instead of judging outcomes (runs or dismissal), it evaluates the **quality of the decision** behind a shot.

---

##  Core Principle

Every shot is a trade-off between:

**Reward** → Runs scored
 **Risk** → Probability and cost of dismissal

The API computes whether the **long-term payoff outweighs the danger**.

---

##  Final Formula

###  Expected Value

```
t = (p × r) − (q × s × 2) − (q²)
```

---



```
p = scoring_shots / total_shots  
q = dismissals / total_shots  
r = total_runs / scoring_shots  

s = ((SR_current − SR_new) × balls_remaining × phase_multiplier) / (100 × baseline)
```

With constraints:

 If incoming batter is better → reduced cost (not zero)
 Minimum wicket cost applied

---

## 📊 Variable Definitions

 Variable  Meaning                            

p        Scoring probability                
q        Dismissal probability              
r        Average reward per successful shot 
s        Context-aware wicket cost          
t        Net expected value                 

---

##  Wicket Cost Model (Advanced)



```
s = max( ((SR_diff × balls_remaining × phase_multiplier) / 100) / baseline , 0.05 )
```



##  Decision Logic (FINAL)

Shot classification is based on **Expected Value (t)**:

 t Range    Classification              

 ≥ 0.4      High Efficiency Shot        
 0.2 → 0.4 Good Shot                   
 0 → 0.2   Marginal / Situational Shot 
 < 0       High Risk / Poor Shot       

---

##  Input Schema

```json
{
  "total_shots": 50,
  "scoring_shots": 31,
  "dismissals": 7,
  "total_runs_from_shot": 186,

  "current_batter_strike_rate": 140,
  "incoming_batter_strike_rate": 110,
  "balls_remaining": 60,
  "phase": "middle",

  "baseline_runs": 100
}
```

---

##  Output Schema
```json
{
  "inputs": {},
  "derived": {
    "p_scoring_probability": 0.62,
    "q_dismissal_probability": 0.14,
    "r_average_reward": 6.0,
    "s_wicket_cost": 0.18
  },
  "results": {
    "expected_value_t": 0.26,
    "shot_efficiency_score": 63.0,
    "classification": "Good Shot"
  }
}
```

---

##  API Endpoints

###  `GET /`

Basic API status

---

###  `GET /health`

Health check

```
{
  "status": "healthy"
}
```

---

###  `GET /description`

Explains formulas, variables, and logic


###  `POST /shot-risk`

Main endpoint to evaluate shot efficiency



##  Validation Rules

* `total_shots > 0`
* `scoring_shots ≤ total_shots`
* `dismissals ≤ total_shots`
* `scoring_shots > 0`
* All numeric inputs must be non-negative


##  Key Insights

* A shot is judged by **expected value**, not outcome
* High reward alone does not justify high risk
* Frequent dismissals are heavily penalized
* Wicket cost is **context-aware**, not constant





##  Use Cases

* Shot selection analysis
* Player decision evaluation
* Coaching & performance insights
* Cricket analytics platforms
* Simulation engines


## Interpretation Guide

* **High t** → Shot is consistently profitable
* **t ≈ 0** → Risk not justified
* **Negative t** → Bad long-term decision



##  Conclusion

This API transforms shot evaluation from **outcome-based thinking** to **decision-based intelligence**, providing a realistic and scalable way to analyze cricket strategy.


