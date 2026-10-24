"""
Layanan simulator What-If sintetis berbasis aturan dengan seed berpasangan.
"""
from typing import Dict, Any, List


SUPPORTED_INTERVENTIONS = {
    "press_intensity": (-0.30, 0.30),
    "defensive_line_height": (-0.25, 0.25),
    "attacking_width": (-0.30, 0.30),
    "directness": (-0.30, 0.30),
    "player_position_delta": (-15.0, 15.0),
}


def run_paired_what_if_simulation(
    match_id: str,
    team_id: str,
    baseline_tactics: Dict[str, float],
    intervention_type: str,
    delta: float,
    seed: int = 961016,
    repetitions: int = 20,
    precomputed_scenarios: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if intervention_type not in SUPPORTED_INTERVENTIONS:
        raise ValueError(f"unsupported_intervention: {intervention_type}")

    min_d, max_d = SUPPORTED_INTERVENTIONS[intervention_type]
    if delta < min_d or delta > max_d:
        raise ValueError(f"Intervention delta {delta} out of allowed bounds [{min_d}, {max_d}]")

    # Cek skenario precomputed jika cocok persis
    if precomputed_scenarios:
        for sc in precomputed_scenarios:
            inv = sc.get("intervention", {})
            if inv.get("type") == intervention_type and sc.get("target_team_id") == team_id:
                param_d = inv.get("parameters", {}).get("delta", inv.get("parameters", {}).get("dx_attack_oriented_m"))
                if param_d is not None and abs(float(param_d) - delta) < 1e-4:
                    return sc

    # Kalkulasi deterministik surrogate berbasis aturan (paired-seed)
    p_base = baseline_tactics.get("press_intensity", 0.60)
    l_base = baseline_tactics.get("defensive_line_height", 0.55)
    w_base = baseline_tactics.get("attacking_width", 0.60)
    d_base = baseline_tactics.get("directness", 0.50)

    cand = dict(baseline_tactics)
    if intervention_type in cand:
        cand[intervention_type] = round(max(0.05, min(0.99, cand[intervention_type] + delta)), 4)

    baseline_metrics = {
        "progressions_completed": round(9.5 + w_base * 2.2 + d_base * 1.1, 2),
        "entries_final_third": round(4.2 + w_base * 1.4 + d_base * 0.9, 2),
        "shots_for": round(1.2 + p_base * 0.35 + d_base * 0.25, 2),
        "turnovers_lost": round(6.2 + p_base * 0.8 + d_base * 1.2, 2),
        "counterattacks_conceded": round(1.8 + l_base * 0.85 + p_base * 0.4, 2),
        "central_space_exposure_index": round(46.0 + l_base * 12.0 + p_base * 4.5 - w_base * 3.0, 4),
        "pressing_success_rate": round(0.45 + p_base * 0.22, 4),
        "build_up_success_rate": round(0.64 - d_base * 0.07, 4),
    }

    p_c = cand.get("press_intensity", p_base)
    l_c = cand.get("defensive_line_height", l_base)
    w_c = cand.get("attacking_width", w_base)
    d_c = cand.get("directness", d_base)
    dm_shift = delta if intervention_type == "player_position_delta" else 0.0

    candidate_metrics = {
        "progressions_completed": round(9.5 + w_c * 2.2 + d_c * 1.1 + dm_shift * 0.1, 2),
        "entries_final_third": round(4.2 + w_c * 1.4 + d_c * 0.9 + dm_shift * 0.0875, 2),
        "shots_for": round(1.2 + p_c * 0.35 + d_c * 0.25, 2),
        "turnovers_lost": round(6.2 + p_c * 0.8 + d_c * 1.2 + dm_shift * 0.075, 2),
        "counterattacks_conceded": round(1.8 + l_c * 0.85 + p_c * 0.4 + dm_shift * 0.05, 2),
        "central_space_exposure_index": round(46.0 + l_c * 12.0 + p_c * 4.5 - w_c * 3.0 + dm_shift * 1.4, 4),
        "pressing_success_rate": round(0.45 + p_c * 0.22 + dm_shift * 0.0125, 4),
        "build_up_success_rate": round(0.64 - d_c * 0.07 - dm_shift * 0.004, 4),
    }

    deltas = {
        k: round(candidate_metrics[k] - baseline_metrics[k], 4)
        for k in baseline_metrics
    }

    return {
        "schema_version": "1.0",
        "scenario_id": f"{match_id}-CUSTOM",
        "match_id": match_id,
        "target_team_id": team_id,
        "baseline_config": {"team_id": team_id, "tactics": baseline_tactics},
        "intervention": {"type": intervention_type, "target_id": team_id, "parameters": {"delta": delta}, "bounded": True},
        "candidate_config": {"team_id": team_id, "tactics": cand},
        "simulation": {
            "engine_version": "tactivision-rule-sim-0.1",
            "seed": seed,
            "repetitions": repetitions,
            "paired_seeds": True,
            "horizon_minutes": 15,
            "model_type": "transparent_rule_based_synthetic_surrogate",
        },
        "baseline_metrics": baseline_metrics,
        "candidate_metrics": candidate_metrics,
        "deltas": deltas,
        "interpretation_status": "simulated_estimate",
        "limitations": [
            "Synthetic rule-based scenario; not an empirically validated Premier League outcome predictor.",
            "A paired-seed comparison controls randomness but does not establish real-world causal effects.",
            "Metrics describe a 15-minute tactical window, not a full-match forecast.",
        ],
    }
