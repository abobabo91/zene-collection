# My Music Collection

Song-by-song graph of a ~15,000-track personal music library. Parses filenames and folder structures to build structured artist credit data across 19 genre areas, with an interactive visualization dashboard.

**[Live Dashboard](https://abobabo91.github.io/zene-local-music-graph/)**

## What it does

1. Walks the local music folder tree (mp3/wma/m4a/flac)
2. Extracts artist names, song titles, and featuring credits from filenames and folder names
3. Resolves aliases, merges duplicates, expands group memberships
4. Computes normalized and adjusted song credit scores
5. Generates a self-contained HTML dashboard with interactive tables, maps, and folder browsers

## Areas

19 areas, 15,153 songs, rebuilt 2026-08-11. Every area is scanned from disk; none is
hand-maintained. No song is counted twice — 15,153 rows, 15,153 distinct paths.

| Area | Songs | Artists | Source folders |
|---|---|---|---|
| US Rap/Trap | 6,633 | 1,150 | `_rap/`, `_trap/` |
| Hungarian Rap/Trap | 2,193 | 486 | `_magyar rap/`, `_magyar trap/` |
| Electronic | 1,179 | 777 | `_other/_elektro/` |
| Pop | 1,041 | 410 | `_other/_pop/` |
| R&B | 799 | 211 | `_other/_rnb/` |
| Magyar (HU other) | 725 | 279 | `_other/_magyar/` |
| Rock | 646 | 165 | `_other/_rock/` |
| Alternative | 554 | 190 | `_other/_alternate/` |
| Latin | 277 | 138 | `_other/_latino/` |
| Intl. rap | 236 | 142 | `_rap/_other/` |
| Intl. trap | 230 | 127 | `_trap/_other country random/` |
| African | 229 | 152 | `_other/_african music/` |
| Reggae | 108 | 64 | `_other/_reggea/` |
| Romanian | 108 | 82 | `_other/_roman/` |
| Russian | 97 | 60 | `_other/_russian/` |
| Country & Jazz | 42 | 12 | `_other/_country_jazz/` |
| World music | 40 | 23 | `_other/_vilagzene/` |
| Classical | 8 | 7 | `_other/_classical/` |
| Mantra | 8 | 4 | `_other/_mantra/` |

## Visualization

The dashboard ([index.html](index.html)) is a self-contained HTML file with:
- **10 genre tabs** + combined R&B+Pop+Alt view
- **Sortable artist tables** with search, region filter, label filter
- **US and Hungary maps** with region bubbles and top artists per city
- **Click any artist** to browse their full folder/album/song tree on disk
- **Ctrl+click** hint on chart title for keyboard shortcuts

## How it was built

### Parsing pipeline

The core challenge: extract structured artist credits from messy, inconsistent filenames and folder names. The pipeline handles:

- **Track number stripping**: `05. 50 Cent - In Da Club.mp3` → artist: "50 Cent", title: "In Da Club" (without interpreting "50" as a track number and leaving "Cent" as the artist)
- **Feature extraction**: `Drake feat. Rihanna - Take Care.mp3` → primary: Drake, featuring: Rihanna
- **Folder context**: files in `_trap/atlanta/Young Thug/Punk/` inherit "Young Thug" as artist context
- **Compilation detection**: folders like `HIPHOPTXL`, `_random`, `Billboard`, `DatPiff` are recognized as compilations where each file's artist comes from the filename, not the folder
- **A YouTube-mix folder is a compilation the detector did not know about.** A folder named after whatever mix the download came from — `Mix – Yves LaRock - Rise Up`, `2000s Dance - YouTube`, `Legnépszerűbb számok -- Basshunter` — reads as artist context, so every file in it is credited to the artist in the *mix title*. In `_other/_elektro` that credited Bob Sinclar's "Sound Of Freedom" to Yves LaRock, twenty one pilots' "Stressed Out" to Lost Frequencies, and Chromatics to Desire, and it invented persons called `Club Dance`, `pop dance`, `Zyon - No Fate` and `Eliphino - More Than Me`. Dissolving those 43 folders (2026-08-08) dropped elektro from 787 persons to 774 and *raised* unattributed 158 → 168 — the count got worse and the data got better, because nine of the ten files that "lost" attribution had been credited to the wrong artist and only one (`German Haircut.mp3`, genuinely Flying Lotus) was real. It was fixed the way the tree should carry it: in the filename.
- **Scene-release naming**: `02-bad_meets_evil-fast_lane-fum.mp3` → artist: "Bad Meets Evil", title: "Fast Lane". The generic dash rule reads the leading track number as the artist, rejects it as numeric, and falls back to folder context — which credited a whole Bad Meets Evil EP to Eminem. Only names already known as a group or alias are accepted here, because dashes double as spaces in this style: `15-reel-why-sut` would otherwise invent an artist called "reel", and a bare `d12` would become a person entry competing with the D12 group.
- **YouTube artifact cleanup**: strip "(Official Video)", "[HD]", "WSHH Exclusive", "- YouTube" suffixes
- **Billboard catalog prefixes**: strip `2006-005 Shakira` → "Shakira"
- **Accent normalization**: Hungarian characters (á→a, ő→o, ű→u) for consistent matching

### Alias resolution

Each area has a mappings file (`data/<area>/<area>_mappings.md`) that defines:
- **Aliases**: `6ix9ine: 69tekashi, Tekashi69, TEKASHI69` — merged 6 separate entries into one (17→45 songs)
- **Groups**: `Migos: Quavo, Offset, Takeoff` — members get individual credit for group songs
- **Weight overrides**: `Scarface: Geto Boys → 1/2` — Scarface gets half credit for Geto Boys songs instead of the default 1/N

All mappings files share one format and one parser, `common.load_mappings_file`. Sections,
all optional: `## Alias normalization`, `## Groups`, `## Labels`, `## Group regions`,
`## Person entries`. The first four are `` - `key: a, b` `` bullet lists; person entries are
`### Name` blocks with `- aliases/groups/labels/region/notes:` lines.

The alias list is comma-separated, so **an alias containing a comma cannot be written
here** — `P_s = 3,14` would parse as two aliases, `3` and `14`, and any folder named either
would then be credited to that artist. Such a name goes in the person's `notes:`.

`region:` and `## Group regions` exist for areas whose region is curated rather than read
off the folder tree. The US tree encodes it (`_rap/atlanta/…`); the Hungarian one is sorted
by artist, so an artist's home town exists only because someone wrote it down.

### Cleanup process

4 rounds of parallel AI agent review (10 agents per round) identified and fixed:
- **601 junk/duplicate person entries removed** (track numbers as artists, album titles, concatenated names, compilation folder names, encoding artifacts)
- **213 duplicate audio files deleted** (verified by duration + file size + spectral audio analysis using librosa and chromaprint)
- **592 songs moved** from compilation/playlist folders to their correct artist folders
- **200+ alias mappings** across all areas
- **Accent normalization** for Hungarian names via transliteration map

### Scoring

Two scoring methods for artist rankings:
- **Normalized**: each song's credit is split equally among all credited persons (1/N per song)
- **Adjusted**: solo primary artists get full credit (1.0), group members divide, features get 1/N. Weight overrides customize this per artist-group pair (e.g., Eminem gets 1/3 for D12 songs, 50 Cent gets 1/2 for G-Unit songs)

Overrides live in `GROUP_WEIGHT_OVERRIDES` in `build_toplists.py` and only apply to declared **members** of that group. `Eminem: {D12: 1/3}` sat there inert from the initial commit until 2026-07-30, because the D12 line in the mappings listed Kuniva, Proof, Kon Artis, Bizarre and Swifty but not Eminem — so he had 0 group songs and the override had nothing to weight. When adding an override, check the member list actually contains that person.

## Scripts

| Script | Purpose |
|---|---|
| `common.py` | Shared constants, text utilities and the mappings-file parser |
| `build_us_graph.py` | Scan `_rap/` + `_trap/`, resolve aliases/groups/labels/regions |
| `build_other_graph.py <area>` | Generic scanner for any `_other/` subfolder |
| `build_hungarian_graph.py` | Incremental scanner for `_magyar rap/` + `_magyar trap/` |
| `build_toplists.py` | Rebuild `toplists.md` for every area |
| `build_visualization.py` | Build the `index.html` dashboard from all area data |
| `rebuild.py` | Rebuild only the areas that changed — **commits and pushes on its own** |

`rebuild.py` takes no arguments and always ends in `git add -A && commit && push`. To
rebuild without publishing, call the individual builders.

### Why Hungarian has its own scanner

`song_id` is load-bearing there: `groups.json` and `labels.json` reference songs by id
(`h-00507`), and those two files carry the only record of 38 crews' line-ups and 9 label
rosters. A from-scratch scan renumbers every song in path order, so after a re-sort the ids
still resolve but point at **different songs** — the graph looks healthy and is wrong.

`build_hungarian_graph.py` is therefore incremental. It keeps the id of every file whose
path is unchanged, re-identifies moved files by basename (only when exactly one unseen file
on disk carries that name — two candidates means guessing), mints ids only for genuinely new
files, and drops the rest. Songs, persons, groups, labels and `region_overrides.json` are
all derived from `hungarian_rap_mappings.md` plus the disk, so the markdown is the thing to
edit.

It also keeps curated songs that live **outside** the scan roots as long as they are still
on disk. That escape hatch is currently unused: 14 Hungarian-rap tracks used to sit under
`_other/_magyar/_cigany/` and were counted by both this area and `magyar`. On 2026-08-11 they
were moved to `_magyar rap/G.w.M/` and `_magyar rap/Teswér/` — one artist, one home, no
double count. Their mtimes were deliberately **not** touched: the timeline reads mtime as
"when did this enter the collection", and these are from 2016-2024.

Credits are carried forward, not re-derived — that is the point of an incremental scan. The
exception is a credit that is invalid under the current config: a song credited to nobody,
or to a name that `generic_folders` or `blocklist` now says is a folder. Those are
re-attributed on every run, so a fix to the rules actually reaches the songs it was written
for. 28 songs were repaired this way on 2026-08-11, taking the area's unattributed count
from 22 to 0.

The area had no scanner at all until 2026-08-11. Its JSONs were curated by hand, so every
re-sort of the folders left it pointing at paths that no longer existed and blind to
anything new, with nothing reporting it.

### Finding duplicates: title alone is not enough, and duration alone is not either

The 2026-08-11 dedupe removed **146 files (617 MB)** and is worth recording as a method,
because the obvious versions of it are both wrong.

Matching on *artist + normalized title* returned 214 groups, most of them junk: empty titles
from Cyrillic filenames, `Full Album` folders where the album name parses as the title, and
genuinely different songs — `Queen's Speech Ep.1 / Ep.3 / Ep.4`, `Temptation Pt. 1 / Pt. 2`,
`Trapaholics ... Track 11 / 12 / 15`, `HipHopTXLcom` tracks 03 and 25. Adding a duration
filter cut it to 100 but kept every one of those, because a numbered series runs to the same
length.

What worked was two independent passes that can each veto:

1. **Read every group.** 184 candidates, judged by eye: is this the same recording? That
   catches what no rule sees — a Radio Edit against an Original Mix, an Airscape remix
   against a Tiësto one, `ft. Lil Wayne` against the solo cut, the two genuinely different
   versions of Grimes' *REALiTi*. 39 groups were left alone on those grounds.
2. **A mechanical title check over the same groups**, stripping *only* upload noise
   (`Official Video`, `Lyrics`, `WSHH Exclusive`, `Prod. by …`) and never a marker that
   names a different recording. It refuses a group whose numbers differ once the leading
   track index and any number inside the artist's own name (`Sum 41`, `blink-182`) are
   discounted.

Run over the 39 groups the reading had already rejected, the mechanical check independently
caught 3 — the numbered series. Run over the 145 marked for removal, it agreed with all of
them. Neither pass is sufficient: the first cannot be trusted at scale, and the second
cannot tell a remix from an original.

Removals are **moved to `_dupes_removed/`**, mirroring their original path, never deleted.

### A genre folder read as an artist

A subgenre folder holding loose files becomes the area's top "artist": `_afrobeats` had 32
songs and `_amapiano` 28, `trance` 14, `electronic_pop` 13, `German` 7, `goldies` 5. The
parent folders were in `generic_folders`; the nested ones were not, and nothing reports the
difference — the fake artist just sits at the top of the leaderboard looking plausible.

Fixing it makes the *numbers worse and the data better*, the same trade as the YouTube-mix
folders: African went from 1 unattributed song to 42, because files like `_afrobeats/Joro.mp3`
and `_afrobeats/Call Back.mp3` carry no artist anywhere in the path. They were never really
attributed — they were attributed to a genre. The fix is to put the artist in the filename.

Related, and not junk despite looking it: `SCBP - Banga.mp3`, `Bloose Broavaz - Banda
Bloose.mp3` and `Vicc Beatz - Másé.mp3` credit a *label* as the performing act. Those are
posse cuts released under the label name, the credit comes from the filename rather than the
folder, and they are correct. The label folders are still in `generic_folders` so they never
act as artist *context* for everything else inside them.

### Two artists whose names differ only in case

`Filo` (IFS, Szeged) and `FILO` (`_magyar trap`) are different people — the mappings file
has said so since it was written. `normalize_key` lowercases, so both Person entries
produce the key `filo`, and registering both means the second silently wins. That credited
the IFS group's 19 songs to the trap FILO and took his count from 8 to 29.

`load_mappings_file` therefore registers an ambiguous key for **neither** name, and exposes
the clash in `ambiguous_person_keys`. Each spelling then resolves to itself. **An alias line
cannot fix this** — `` `FILO: filo` `` recreates the same colliding key.

What actually separates them is the folder, so `build_hungarian_graph.AMBIGUOUS_BY_ROOT`
resolves the name by which tree the file is in: `_magyar rap` → `Filo`, `_magyar trap` →
`FILO`. Verified 2026-08-11: Filo 37 songs, FILO 9, no stray lowercase third person.

### A group's label is carried, not derived

Deriving a group's label from what its members are signed to is wrong in both directions.
`Nevenincs` is a goldsoul act with **no member list**, so deriving dropped its label and
goldsoul lost 13 songs; `Hősök` and `Gruppen Family` gained a Bloose Broavaz tag they never
had, purely because Eckü and Siska Finuccsi are signed there. Group labels live in
`## Group labels` in the mappings file and are read verbatim.

### The curated JSONs had 163 dangling song ids

Before the 2026-08-11 rebuild, `labels.json` (19), `groups.json` (18) and `persons.json`
(126) referenced song ids that were not in `songs.json` at all. They accumulated because the
indexes were hand-edited alongside the songs. Deriving every index from the songs removes
them by construction — the rebuilt data has zero. Expect a label to "lose" songs on the
first rebuild that were never really there.

### A directory can be named `.mp3`

`_magyar rap/el bago/ultimohombre/ultimohombre.mp3` is a **folder** holding four real
tracks. `rglob("*")` plus a suffix test matches it as though it were a song, and PowerShell's
`Get-ChildItem -Filter *.mp3` returns it too. Every scanner here pairs the suffix test with
`is_file()`, and the timeline's CSV scan passes `-File`. `os.walk` was never affected, which
is why the catalog and the CSV disagreed by one row rather than obviously breaking.

## Collection layout the scanner expects

A folder should name an **artist** or a **release**, never the download it arrived in — see
the compilation note above for what a mix-title folder does to the credits. `_other/_elektro`
was reorganised to this shape on 2026-08-08 and is the reference; the per-folder decision
rules for that tree live next to the music, in `_other/_elektro/_HOVA_KERULJON.md`:

- an artist with **3 or more** files in a subgenre gets a folder (`trance_dance_rave/Ayla/`)
- fewer than that sits **loose at the subgenre root**, with the artist in the filename
- album folders are never opened, so a release stays intact
- nothing crosses a subgenre, so the folder-based YouTube playlists keep their membership

Moving files is not free: `zene-youtube`'s match cache and `overrides.json` are keyed by
collection-relative path, so a move has to carry the key with it or every match is orphaned
and every hand-made pin is lost. The videoId does not change just because the file did.

## Data layout

```
data/<area>/
  <area>_mappings.md          # aliases, groups, labels, regions, person entries
  normalized/
    songs.json                # song-by-song credits (source of truth)
    persons.json              # artist index with song references
    metadata.json             # counts
    groups.json               # group definitions (US/Hungarian only)
    labels.json               # label rosters (US/Hungarian only)
    regions.json              # US only
    region_overrides.json     # Hungarian only, generated from the mappings file
    toplists.md               # human-readable rankings (all areas)
```

## Tech

- Python (pathlib, json, re, collections)
- mutagen — audio metadata/duration reading
- librosa + chromaprint (fpcalc) — spectral audio fingerprinting for duplicate detection
- Chart.js — not used here but in the sibling genre-timeline project
- Zero external dependencies for the visualization (self-contained HTML + inline data)
