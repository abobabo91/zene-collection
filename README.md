# zene-collection

Everything that reads the music collection at `C:\Users\abele\Desktop\zene` and turns it
into something you can look at: the artist graph, the genre timeline, and the dashboard that
puts them side by side.

**Live:** <https://abobabo91.github.io/zene-collection/>

```
python rebuild.py                # graph -> timeline -> dashboard, then one commit + push
python rebuild.py --no-push      # same, but leave the push to the caller
python rebuild.py --dry-run      # say what would rebuild, write nothing
python rebuild.py --only graph   # one stage (graph | timeline | dashboard)
```

| directory | what it is | entry point |
|---|---|---|
| `graph/` | Artist rankings and credits across 19 areas, scanned from disk. Click an artist for their folder tree. | `graph/rebuild.py` |
| `timeline/` | When each track entered the collection, by genre, cumulative. | `timeline/rebuild.py` |
| `dashboard/` | Collects the other two into one site and injects the shared nav. | `dashboard/build.py` |
| `docs/` | **Generated.** The published site — this is what GitHub Pages serves. | — |

## Why these are one repo

They were three (`zene-local-music-graph`, `zene-genre-timeline`, `zene-dashboard`) until
2026-08-12, and the split was never real. `dashboard/build.py` reads the other two's output
straight off disk, and any change to the collection has to rebuild all three in that exact
order. Splitting them bought nothing and cost two things:

- **Three commits and three pushes for one logical change**, with the three able to drift
  out of step in between.
- **Duplicated logic that drifted.** The two `rebuild.py` scripts became near-copies, and
  the same two bugs had to be found and fixed twice on the same day: output decoded with the
  Windows locale codepage (cp1250) instead of UTF-8, which died on accented artist names
  mid-rebuild; and an unconditional `git push` that fired as a side effect of any run,
  including `--help`.

The old repositories are redirect stubs now. Their history came along with the merge — the
subtree merges kept every commit reachable, so `git log` here reaches back through all three.

## The rules that hold it together

- **The root `rebuild.py` is the only thing that touches git.** The stage scripts are plain
  builders: they write files and return an exit code. This is the fix for the duplicated
  push logic, not a style preference.
- **A failed stage stops the run.** Otherwise the dashboard publishes a graph that is half
  old and half new, and the stage's timestamp file records a build that did not finish, so
  it never gets retried.
- **`--dry-run` is honoured by every stage.** It has to be: the orchestrator passes it down,
  and `build.py` used to ignore argv entirely and write the dashboard anyway.
- **`docs/` is generated — never edit it.** It exists because GitHub Pages only serves from
  the repository root or `docs/`, and the root is already taken by the *sources* `graph/`
  and `timeline/`, which would collide with the dashboard's same-named output folders.

## Where the collection numbers come from

As of 2026-08-12 the collection is 15,147 mp3s and nothing else — 323 `.m4a`/`.wma`/`.wav`
files were transcoded that day. The graph indexes all 15,147; the timeline catalog holds
15,146, the one difference being a `bizarring` blocklist entry the graph does not carry.

The scanners are the source of truth for those numbers. Re-derive from
`graph/data/*/normalized/songs.json` rather than trusting a figure written down anywhere,
including here.

## Related

- `../youtube/` — playlist and download pipelines. Its `refresh.py` calls `graph/rebuild.py`
  and reads `graph/data/`, so a change to this repo's layout has to be reflected there.
