# Genre Timeline

Interactive dashboard for visualizing a personal music collection by genre over time.

## Features

- **Genre catalog builder** — scans ~15k mp3s on disk, classifies by folder structure into 20 genres with sub-genres
- **Timeline visualization** — three modes: absolute count, ratio, cumulative stacked area (default)
- **Smoothing** — adjustable moving average (default: 10-quarter window)
- **Genre drill-down** — click a single genre pill to see sub-genre breakdown across all charts
- **Interactive legend** — click to toggle, Ctrl+click to solo a genre
- **File list modal** — right-click any genre/sub-genre to browse its songs
- **Date range filter** — focus on any time period
- **Donut + sub-genre bars** — genre distribution and top sub-genres

## Quick start

```
python serve.py
```

Rebuilds the catalog from disk and opens the dashboard at http://localhost:8765.

## Files

- `build_catalog.py` — genre classifier and JSON generator
- `index.html` — single-file dashboard (Chart.js, vanilla JS, dark theme)
- `serve.py` — rebuild + serve
- `genre_catalog.json` — generated catalog (15k entries)
- `build_mp3_timeline.py` — generates `mp3_sorted_filtered.csv` (all mp3s by date)
- `mp3_sorted_filtered.csv` — generated CSV sorted by file modification time
