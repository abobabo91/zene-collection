# zene-collection / graph

Song-by-song music graph for a ~15k-song local library across 19 areas.

**This is a subdirectory of `zene-collection`, not its own repo** (merged 2026-08-12 with the
timeline and the dashboard). `rebuild.py` here is a plain builder: it writes files and returns
an exit code, and does **not** touch git. Run `../rebuild.py` to rebuild the graph, timeline
and dashboard together and commit them as one change.

## First read

Read `README.md` for areas, scripts, and workflow, and `../README.md` for how the three
pieces fit together.

## Scripts

- `common.py` — shared constants and text utilities (imported by all other scripts)
- `build_us_graph.py` — US rap/trap (has regions, groups, labels, weight overrides)
- `build_other_graph.py <area>` — all other areas: rnb, rock, magyar, elektro, pop, alternate, latino
- `build_toplists.py` — toplists for US + Hungarian
- `build_visualization.py` — builds `index.html` dashboard with folder browser

## Critical rules

- Never commit secrets, caches, or logs.
- Do not mix YouTube scraping/downloading logic into this project.
- **US:** `build_us_graph.py` regenerates from disk. Edit `data/us/us_rap_trap_mappings.md` for aliases/groups.
- **Hungarian Rap:** No scanner — edit `data/hungarian/normalized/` JSONs directly.
- **Other areas:** `build_other_graph.py` regenerates from disk. Edit `data/<area>/<area>_mappings.md`.
- R&B groups are treated as single entities except Destiny's Child (which splits to members).

## Git expectations

Good to commit: code, docs, graph outputs, mappings, visualization.

Do not commit: `__pycache__`, machine-specific temp files, one-time utility scripts.
