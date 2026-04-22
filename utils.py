def calculate_probabilities(total_shots, scoring_shots, dismissals):
    p = scoring_shots / total_shots
    q = dismissals / total_shots
    return p, q


def calculate_average_reward(total_runs, total_shots):
    """
    FIXED:
    Reward is now runs per shot (not per scoring shot)
    This aligns reward with risk scale.
    """
    return total_runs / total_shots


def get_phase_multiplier(phase: str):
    return {
        "powerplay": 1.2,
        "middle": 1.0,
        "death": 0.8
    }.get(phase.lower(), 1.0)


def calculate_wicket_cost(current_sr, new_sr, balls_remaining, phase, baseline):
    """
    Advanced wicket cost:
    - Direction aware
    - Reduced if incoming batter is better
    - Never zero (floor applied)
    """

    sr_diff = current_sr - new_sr

    if sr_diff <= 0:
        sr_diff = abs(sr_diff) * 0.3

    phase_multiplier = get_phase_multiplier(phase)

    impact_runs = (sr_diff * balls_remaining) / 100
    adjusted = impact_runs * phase_multiplier

    s = adjusted / baseline

    return max(s, 0.05)  # minimum cost


def calculate_expected_value(p, q, r, s):
    """
    FINAL EV MODEL (BALANCED):
    """
    dismissal_penalty = q ** 2        # non-linear penalty
    risk_component = q * s * 2        # amplified wicket impact

    return (p * r) - risk_component - dismissal_penalty


def calculate_efficiency_score(t):
    """
    Only for UI display
    """
    score = (t + 1) * 50
    return max(0, min(score, 100))


def classify_shot(t):
    """
    FINAL classification using expected value (NOT score)
    """

    if t >= 0.25:
        return "High Efficiency Shot"
    elif t >= 0.1:
        return "Good Shot"
    elif t >= 0:
        return "Marginal / Situational Shot"
    else:
        return "High Risk / Poor Shot"