# My Music Collection Timeline

Interactive dashboard showing how a 15,000+ song music collection evolved over time, broken down by genre.

**[Live Dashboard](https://abobabo91.github.io/zene-genre-timeline/)**

## What it does

Scans a local music folder, classifies every mp3 by its folder structure into 20 genres with sub-genres, and generates an interactive timeline visualization. File modification dates serve as a proxy for "when was this added to the collection" — showing listening habits and genre discovery patterns over 20+ years.

## Dashboard features

- **Cumulative stacked area chart** (default) — see how genre proportions shifted over time
- **Three view modes**: absolute count, ratio (%), cumulative area
- **Adjustable smoothing** — moving average window from 1 to 12 periods
- **Monthly / Quarterly / Yearly** granularity
- **Genre pill filters** — click to isolate genres, see how they evolved
- **Genre drill-down** — click a single genre to see its sub-genres across all charts
- **Interactive legend** — click to toggle visibility, **Ctrl+click to solo** a genre
- **Hover tooltips** — in cumulative mode, hover any strip to see that genre's percentage
- **Date range** picker to focus on any time period
- **Genre donut** — click slices to filter
- **Sub-genre bars** — click any bar for the full file list
- **Right-click** any genre pill, donut slice, or sub-genre bar → modal with all files in that category
- **Recent additions** table — last 30 songs with genre and sub-genre tags

## Genre classification

Genres and sub-genres are derived purely from the folder structure:

| Main genre | Source folder | Sub-genres |
|---|---|---|
| rap | `_rap/` | region (new york, atlanta, california, etc.) |
| trap | `_trap/` | region |
| hungarian rap | `_magyar rap/` | — |
| hungarian trap | `_magyar trap/` | — |
| pop | `_other/_pop/` | billboard, kpop, modern, oldschool |
| electronic | `_other/_elektro/` | deep house, house & techno, psytrance, dnb, etc. |
| hungarian | `_other/_magyar/` | rock, pop, retro, nepzene, etc. |
| r&b | `_other/_rnb/` | — |
| rock | `_other/_rock/` | — |
| alternative | `_other/_alternate/` | — |
| latin | `_other/_latino/` | oldschool |
| african | `_other/_african music/` | — |
| romanian | `_other/_roman/` | manele, modern pop, old pop, trap |
| russian | `_other/_russian/` | trap |
| + 6 more | reggae, country & jazz, world music, mantra, classical, other | |

## How it was built

1. **Folder scanner** (`build_catalog.py`) walks the entire music folder tree, classifies each mp3 into main_genre + sub_genre based on the folder path, and writes `genre_catalog.json` with file path, genre, sub-genre, and modification timestamp

2. **Dashboard** (`index.html`) is a single self-contained HTML file using Chart.js. It fetches the JSON catalog and renders all charts client-side. Dark theme, responsive layout.

3. **Custom Chart.js interaction mode** (`stackedArea`) — built a custom interaction handler that detects which stacked area strip the cursor is inside (by checking cumulative band boundaries), instead of the default "nearest line" detection which picks the wrong genre when hovering between strips

4. **Keyword blocklist** for excluding specific files from the catalog without exposing filenames in the code

## Quick start (local)

```
python serve.py
```

Rebuilds the catalog from disk and opens the dashboard at http://localhost:8765.

## Files

| File | Purpose |
|---|---|
| `build_catalog.py` | Genre classifier — scans disk, writes `genre_catalog.json` |
| `index.html` | Dashboard — Chart.js, vanilla JS, dark theme |
| `serve.py` | Rebuild catalog + serve locally |
| `genre_catalog.json` | Generated catalog (~15k entries) |
| `build_mp3_timeline.py` | Generates `mp3_sorted_filtered.csv` (all mp3s sorted by date) |

## Tech

- Python (pathlib, os, json)
- Chart.js 4 (CDN) for all charts
- Vanilla JavaScript — no framework, no build step
- CSS custom properties for dark theme
- Self-contained HTML (no separate CSS/JS files)
