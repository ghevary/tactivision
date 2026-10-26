"""
REST API FastAPI Alcyone AI (/api/v1) sesuai SYSTEM_ARCHITECTURE.md & PRD.md.
"""
import os
import json
import csv
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from llm_adapter import GeminiLLMAdapter
from query_service import execute_deterministic_query
from what_if_service import run_paired_what_if_simulation, SUPPORTED_INTERVENTIONS

from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
DEFAULT_DATA_DIR = str(Path(__file__).resolve().parents[2] / "data")
DATA_DIR = os.environ.get("ALCYONE_DATA_DIR", DEFAULT_DATA_DIR)

app = FastAPI(
    title="Alcyone AI REST API",
    version="1.0.0",
    description="Deterministic tactical analytics, Voronoi spatial engine, paired-seed What-If simulator, and Gemini 3.8 Flash grounded explanation service.",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
llm_adapter = GeminiLLMAdapter(model="gemini-3.8-flash")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    language: str = Field(default="id")
    query_filter: Optional[Dict[str, Any]] = None
    persona: str = Field(default="Analyst")


class WhatIfRequest(BaseModel):
    team_id: str
    intervention_type: str
    delta: float
    seed: int = 961016
    repetitions: int = 20
    persona: str = "Analyst"
    language: str = "id"


class TacticalShiftPayload(BaseModel):
    moved_player: Dict[str, Any]
    spatial_metrics: Dict[str, Any]
    persona: str = "Analyst"
    language: str = "id"
    previous_interaction_id: Optional[str] = None


def _match_dir(match_id: str) -> str:
    path = os.path.join(DATA_DIR, "matches", match_id)
    if not os.path.isdir(path):
        raise HTTPException(status_code=404, detail=f"Match {match_id} not found")
    return path


@app.get("/api/v1/health")
def get_health():
    manifest_path = os.path.join(DATA_DIR, "dataset_manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    return {
        "status": "ok",
        "api_version": "1.0.0",
        "dataset_version": manifest.get("dataset_version", "1.1.0"),
        "synthetic_only": True,
        "llm_model": llm_adapter.model,
    }


@app.get("/api/v1/matches")
def list_matches(team_id: Optional[str] = None):
    fixtures_path = os.path.join(DATA_DIR, "fixtures.csv")
    if not os.path.exists(fixtures_path):
        raise HTTPException(status_code=500, detail="fixtures.csv missing")
    fixtures = list(csv.DictReader(open(fixtures_path)))
    results = []
    for row in fixtures:
        if team_id and team_id not in (row["home_team_id"], row["away_team_id"]):
            continue
        summary_path = os.path.join(DATA_DIR, "matches", row["match_id"], "match_summary.json")
        summary = json.load(open(summary_path)) if os.path.exists(summary_path) else {}
        results.append({**row, "goals": summary.get("goals", {}), "synthetic": True})
    return {"matches": results, "count": len(results), "dataset_version": "1.1.0"}


@app.get("/api/v1/matches/{match_id}")
def get_match(match_id: str):
    m_dir = _match_dir(match_id)
    return json.load(open(os.path.join(m_dir, "match.json")))


@app.get("/api/v1/matches/{match_id}/analytics")
def get_match_analytics(match_id: str, team_id: Optional[str] = None):
    m_dir = _match_dir(match_id)
    data = json.load(open(os.path.join(m_dir, "analytics.json")))
    if team_id:
        data["team_stats"] = [t for t in data["team_stats"] if t["team_id"] == team_id]
        data["player_stats"] = [p for p in data["player_stats"] if p["team_id"] == team_id]
    return data


@app.get("/api/v1/matches/{match_id}/events")
def get_match_events(
    match_id: str,
    team_id: Optional[str] = None,
    event_type: Optional[str] = None,
    period: Optional[int] = None,
    limit: int = Query(default=100, ge=1, le=500),
):
    m_dir = _match_dir(match_id)
    events = [json.loads(line) for line in open(os.path.join(m_dir, "events.jsonl"))]
    filtered = []
    for e in events:
        if team_id and e["team_id"] != team_id:
            continue
        if event_type and e["event_type"] != event_type:
            continue
        if period and e["period"] != period:
            continue
        filtered.append(e)
    return {
        "match_id": match_id,
        "total_matching": len(filtered),
        "events": filtered[:limit],
        "truncated": len(filtered) > limit,
    }


@app.get("/api/v1/matches/{match_id}/passing-network")
def get_passing_network(match_id: str, team_id: Optional[str] = None):
    m_dir = _match_dir(match_id)
    pn = json.load(open(os.path.join(m_dir, "passing_network.json")))
    if team_id:
        pn["nodes"] = [n for n in pn["nodes"] if n["team_id"] == team_id]
        pn["edges"] = [e for e in pn["edges"] if e["team_id"] == team_id]
    return pn


@app.get("/api/v1/matches/{match_id}/heatmap")
def get_heatmap(match_id: str, team_id: str, surface: str = "event_density"):
    m_dir = _match_dir(match_id)
    hm = json.load(open(os.path.join(m_dir, "heatmaps.json")))
    if team_id not in hm["teams"]:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not in match {match_id}")
    if surface not in hm["teams"][team_id]:
        raise HTTPException(status_code=400, detail=f"Unsupported surface {surface}")
    return {
        "match_id": match_id,
        "team_id": team_id,
        "surface": surface,
        "grid_definition": hm["grid_definition"],
        "layer": hm["teams"][team_id][surface],
    }


@app.get("/api/v1/matches/{match_id}/voronoi")
def get_voronoi(match_id: str, elapsed_sec: int = 0):
    m_dir = _match_dir(match_id)
    sa = json.load(open(os.path.join(m_dir, "spatial_analytics.json")))
    for snap in sa["snapshots"]:
        if snap["elapsed_sec"] == elapsed_sec:
            return {
                "match_id": match_id,
                "method": sa["method"],
                "territory_limitation": sa["territory_limitation"],
                "snapshot": snap,
            }
    raise HTTPException(
        status_code=400,
        detail=f"Voronoi snapshot at elapsed_sec={elapsed_sec} not in precomputed 60s interval.",
    )


@app.post("/api/v1/matches/{match_id}/query")
def post_natural_language_query(match_id: str, req: QueryRequest):
    m_dir = _match_dir(match_id)
    summary = json.load(open(os.path.join(m_dir, "match_summary.json")))
    events = [json.loads(line) for line in open(os.path.join(m_dir, "events.jsonl"))]
    try:
        if req.query_filter is not None:
            qf = llm_adapter.validate_query_filter(
                req.query_filter, summary["home_team_id"], summary["away_team_id"]
            )
        else:
            qf = llm_adapter.parse_natural_language_query(
                req.question, match_id, summary["home_team_id"], summary["away_team_id"]
            )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    result = execute_deterministic_query(events, qf)
    explanation = llm_adapter.explain_evidence(
        {"match_id": match_id, "question": req.question, "query_result": {
            "total_count": result["total_count"],
            "sample_event_ids": result["event_ids"][:10],
            "validated_filter": qf,
        }},
        persona=req.persona,
        language=req.language,
    )
    return {
        "match_id": match_id,
        "question": req.question,
        "language": req.language,
        **result,
        "explanation": explanation,
    }


@app.post("/api/v1/matches/{match_id}/what-if")
def post_what_if(match_id: str, req: WhatIfRequest):
    m_dir = _match_dir(match_id)
    if req.intervention_type not in SUPPORTED_INTERVENTIONS:
        raise HTTPException(status_code=422, detail=f"unsupported_intervention: {req.intervention_type}")

    scenarios = [
        json.loads(line) for line in open(os.path.join(m_dir, "what_if_scenarios.jsonl"))
    ]
    baseline_tactics = {"press_intensity": 0.82, "defensive_line_height": 0.76, "attacking_width": 0.62, "directness": 0.46}
    for sc in scenarios:
        if sc.get("target_team_id") == req.team_id:
            baseline_tactics = sc["baseline_config"]["tactics"]
            break

    try:
        sim_out = run_paired_what_if_simulation(
            match_id=match_id,
            team_id=req.team_id,
            baseline_tactics=baseline_tactics,
            intervention_type=req.intervention_type,
            delta=req.delta,
            seed=req.seed,
            repetitions=req.repetitions,
            precomputed_scenarios=scenarios,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    explanation = llm_adapter.explain_evidence(sim_out, persona=req.persona, language=req.language)
    return {**sim_out, "language": req.language, "explanation": explanation}


@app.post("/api/v1/agents/analyze-tactical-shift")
def analyze_tactical_shift(payload: TacticalShiftPayload):
    return llm_adapter.explain_evidence(
        payload.model_dump(),
        persona=payload.persona,
        previous_interaction_id=payload.previous_interaction_id,
        language=payload.language,
    )
