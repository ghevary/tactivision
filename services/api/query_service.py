"""
Layanan eksekusi query deterministik terhadap events.jsonl kanonis.
"""
from typing import List, Dict, Any


def execute_deterministic_query(
    events: List[Dict[str, Any]], query_filter: Dict[str, Any], max_ids: int = 100
) -> Dict[str, Any]:
    matched_events: List[Dict[str, Any]] = []
    for e in events:
        if "event_types" in query_filter and e["event_type"] not in query_filter["event_types"]:
            continue
        if "team_id" in query_filter and e["team_id"] != query_filter["team_id"]:
            continue
        if "period" in query_filter and e["period"] != query_filter["period"]:
            continue
        if "outcome" in query_filter and e["outcome"] != query_filter["outcome"]:
            continue
        if "phase" in query_filter and e["phase"] != query_filter["phase"]:
            continue
        if "min_period_minute" in query_filter and e["period_minute"] < query_filter["min_period_minute"]:
            continue
        if "max_period_minute" in query_filter and e["period_minute"] > query_filter["max_period_minute"]:
            continue
        if query_filter.get("progressive_only"):
            if (e.get("progressive_distance_m") or 0) < 10.0 and "progressive" not in (e.get("tags") or []):
                continue
        if "min_shot_quality_proxy" in query_filter:
            if (e.get("shot_quality_proxy") or 0) < query_filter["min_shot_quality_proxy"]:
                continue
        if "min_end_attack_x" in query_filter:
            end_pos = e.get("end") or e.get("location") or {"x": 0.0, "y": 0.0}
            end_x = float(end_pos.get("x", 0.0))
            att_x = end_x if e.get("attacking_direction", 1) == 1 else (105.0 - end_x)
            if att_x < query_filter["min_end_attack_x"]:
                continue
        matched_events.append(e)

    all_ids = [e["event_id"] for e in matched_events]
    return {
        "validated_filter": query_filter,
        "total_count": len(matched_events),
        "event_ids": all_ids[:max_ids],
        "event_ids_truncated": len(all_ids) > max_ids,
        "events_preview": matched_events[:25],
        "provenance": "deterministic_python_executor_v1.1",
    }
