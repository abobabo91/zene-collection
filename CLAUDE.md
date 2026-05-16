# zene-genre-timeline

Genre catalog builder and interactive timeline visualization for a personal music collection (~15k mp3s).

## First read

- `build_catalog.py` — scans the full music library, classifies each mp3 by folder structure into main_genre + sub_genre, outputs `genre_catalog.json`
- `index.html` — interactive dashboard (Chart.js): cumulative stacked area, donut, sub-genre bars, file list modal
- `serve.py` — rebuilds catalog and serves the dashboard at localhost:8765
- `build_mp3_timeline.py` — separate utility: generates `mp3_sorted_filtered.csv` (all mp3s sorted by date, excluding `new/`)

## How to run

```
python serve.py
```

This rebuilds `genre_catalog.json` from disk and opens the dashboard.

## Critical rules

- Never commit secrets.
- `genre_catalog.json` and `mp3_sorted_filtered.csv` are generated artifacts — safe to commit but will be overwritten on rebuild.
- The `BLOCKLIST` in `build_catalog.py` permanently excludes specific files from the catalog.

## Genre classification

Genres are derived from the folder structure under `C:\Users\abele\Desktop\zene\`:
- `_rap/`, `_trap/` — main: rap/trap, sub: region
- `_magyar rap/`, `_magyar trap/` — main: hungarian rap / hungarian trap
- `_other/_elektro/` — main: electronic, sub: subgenre folder
- `_other/_magyar/` — main: hungarian, sub: style folder
- `_other/_roman/` — main: romanian, sub: style folder
- `_other/_russian/` — main: russian, sub: trap (if applicable)
- etc. (see `classify()` in `build_catalog.py` for full mapping)

Folders excluded from scan: `new/`, `new good/`, `_music_scripts/`, `_playlists/`.
