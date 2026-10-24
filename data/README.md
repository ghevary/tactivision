# TactiVision AI — Standalone `data/` folder v1.1.0

This directory is the ready-to-use synthetic dataset for the TactiVision AI project. It contains five persistent fictional clubs, a stable 55-player registry, ten round-robin matches, canonical per-match JSON/JSONL, master dictionaries, global What-If/query files, and flat CSV exports.

## Master registries
- `clubs.csv`: five unique fictional clubs and default tactical archetypes.
- `player_registry.csv`: 55 stable player identities; IDs stay the same across matches.
- `fixtures.csv`: the ten unique home-away fixtures in a single round-robin.
- `dataset_manifest.json`: dataset version/counts and match summaries.

## Canonical sources
- `matches/SYN_001/` through `matches/SYN_010/`: each match has exactly two clubs and 22 tracked players.
- `events.jsonl`: events use persistent `CLUB_A`..`CLUB_E` IDs and stable player IDs such as `CLUB_A_P09`.
- `tracking.jsonl`: full synchronized snapshot at five-second intervals.
- `analytics.json`, `passing_network.json`, `heatmaps.json`, and `spatial_analytics.json`: computed derived features.
- `what_if_scenarios.jsonl`, `what_if_runs.jsonl`, and `query_examples.jsonl`: What-If and natural-language query fixtures.
- `flat/`: CSV convenience exports. Regenerate with `python src/export_flat.py` from the project root after changing canonical match data.

## Quick start
From the project root, validate the bundled data:

```bash
python -m pip install -r requirements.txt
python tools/validate_dataset.py
python examples/quickstart.py
```

All clubs, players, matches, and events are synthetic. What-If results are produced by a rule-based synthetic simulator; they are not empirically validated predictions about real football matches.
