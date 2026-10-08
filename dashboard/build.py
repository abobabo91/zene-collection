"""Collects the timeline and the artist graph into `docs/` and ties them together.

It does **not** rewrite either page. Each keeps its own markup and behaviour; the only
changes are (1) a floating nav pill, injected before `</body>` with `position:fixed` so it
never touches the page's own layout, and (2) the shared `theme.css` / `theme.js` from the repo
root, copied next to the output, which both pages and the landing page link (light and dark
tokens, one toggle, one saved choice).

The sources are always the current output of `../timeline/` and `../graph/`, so this folder
is rebuilt, never maintained by hand.

    python build.py      # collect + inject the nav
    python serve.py      # serve it (the timeline fetches JSON, so it needs http)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
#: Repo root. The timeline and the graph live in the same repo (`timeline/`, `graph/`).
REPO = os.path.dirname(HERE)
#: Output is `docs/` because GitHub Pages serves only the repo root or `docs/`. The root is
#: taken by the *sources* `graph/` and `timeline/`, whose output folders share their names.
OUT = os.path.join(REPO, "docs")

#: (target folder, nav label, source dir, source files) - the first file is the entry index.html
SOURCES = [
    ("timeline", "Timeline", os.path.join(REPO, "timeline"),
     ["index.html", "genre_catalog.json", "recent_playlists.json"]),
    ("graph", "Artist graph", os.path.join(REPO, "graph"),
     ["index.html"]),
]
#: Shared by every page; copied to the root of `docs/` so `../theme.css` resolves both from
#: the sources (`timeline/../theme.css`) and from the published copies.
SHARED = ["theme.css", "theme.js"]

NAV = """
<!-- zene_dashboard: shared nav. position:fixed so the page's own layout is untouched. -->
<div id="zdnav">__LINKS__<span class="sep"></span><button type="button" id="zdtheme" title="Switch light / dark"></button></div>
<script>
(function () {
  var b = document.getElementById('zdtheme');
  function label() { b.textContent = zeneTheme.current() === 'dark' ? 'Light' : 'Dark'; }
  b.addEventListener('click', function () { zeneTheme.toggle(); });
  window.addEventListener('zene-theme', label);
  label();
})();
</script>
"""
LINK = '<a href="__HREF__"__CLS__>__LABEL__</a>'


def nav_html(current, root):
    """`root` is the path back to docs/ from the page ('' for the landing page, '../' inside)."""
    items = [("", "Home", "index.html")] + [(slug, label, f"{slug}/index.html")
                                            for slug, label, _, _ in SOURCES]
    links = []
    for slug, label, href in items:
        here = slug == current
        links.append(LINK.replace("__HREF__", root + href)
                     .replace("__LABEL__", label)
                     .replace("__CLS__", ' class="here"' if here else ""))
    return NAV.replace("__LINKS__", "".join(links))


def inject(html, current, root="../"):
    """Puts the nav right before </body>, so it precedes nothing."""
    block = nav_html(current, root)
    if 'id="zdnav"' in html:                       # on a rebuild, do not duplicate
        html = re.sub(r"\n?<!-- zene_dashboard.*?</script>\n?", "", html, flags=re.S)
    if "</body>" in html:
        return html.replace("</body>", block + "</body>", 1)
    return html + block


def counts():
    """The card numbers, read from the sources, never hard-coded.

    Hard-coded numbers go stale silently: the landing page once advertised `15,465 entries`
    while the catalog held 14,975 rows. Whatever cannot be read is None and the card simply
    has no number - leaving it out beats guessing it.
    """
    out = {"timeline": None, "graph": None}
    try:
        catalog = os.path.join(REPO, "timeline", "genre_catalog.json")
        out["timeline"] = len(json.load(open(catalog, encoding="utf-8")))
    except (OSError, ValueError):
        pass
    try:
        data = os.path.join(REPO, "graph", "data")
        total, areas = 0, 0
        for area in sorted(os.listdir(data)):
            songs = os.path.join(data, area, "normalized", "songs.json")
            if os.path.exists(songs):
                total += len(json.load(open(songs, encoding="utf-8")))
                areas += 1
        out["graph"] = (total, areas)
    except (OSError, ValueError):
        pass
    return out


def main():
    # The root `rebuild.py` passes `--dry-run` to every stage, so it has to be honoured here -
    # otherwise a "writes nothing" run still overwrites the dashboard.
    dry = "--dry-run" in sys.argv
    if dry:
        print("(dry run - writing nothing)")
    for name in SHARED:
        s, d = os.path.join(REPO, name), os.path.join(OUT, name)
        if dry:
            print(f"  {name:<28} <- {name} (not copying)")
            continue
        os.makedirs(OUT, exist_ok=True)
        shutil.copy2(s, d)
        print(f"  {name:<28} {os.path.getsize(d)/1024:>8.0f} KB   <- {name}")
    for slug, label, src, files in SOURCES:
        dst = os.path.join(OUT, slug)
        if not dry:
            os.makedirs(dst, exist_ok=True)
        for entry in files:
            name, out = entry if isinstance(entry, tuple) else (entry, entry)
            s = os.path.join(src, name)
            if not os.path.exists(s):
                print(f"  !! missing: {s}")
                continue
            d = os.path.join(dst, out)
            if dry:
                print(f"  {slug}/{out:<22} {os.path.getsize(s)/1024:>8.0f} KB   <- {name} (not copying)")
                continue
            if out.endswith(".html"):
                html = open(s, encoding="utf-8").read()
                open(d, "w", encoding="utf-8").write(inject(html, slug))
            else:
                shutil.copy2(s, d)
            print(f"  {slug}/{out:<22} {os.path.getsize(d)/1024:>8.0f} KB   <- {name}")
    if dry:
        return

    n = counts()
    timeline_desc = "When each track entered the collection, by genre, cumulative."
    if n["timeline"]:
        timeline_desc += f" {n['timeline']:,} entries."
    graph_desc = "Who appears with whom. Click an artist for their folder tree."
    if n["graph"]:
        total, areas = n["graph"]
        graph_desc = (f"Who appears with whom, {areas} areas as tabs. Click an artist for "
                      f"their folder tree. {total:,} songs.")

    cards = "".join(
        f'<a class="card" href="{slug}/index.html"><h2>{label}</h2><p>{desc}</p></a>'
        for slug, label, desc in [
            ("timeline", "Timeline", timeline_desc),
            ("graph", "Artist graph", graph_desc),
        ])
    os.makedirs(OUT, exist_ok=True)
    page = LANDING.replace("__CARDS__", cards)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(inject(page, "", root=""))
    print(f"  index.html (landing)    timeline={n['timeline']} graph={n['graph']}")
    print(f"  -> {OUT}  (served by GitHub Pages)")


LANDING = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>My Music Collection</title>
<link rel="stylesheet" href="theme.css">
<script src="theme.js"></script>
<style>
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
  justify-content: center; padding: 32px 24px; }
h1 { font-size: 26px; font-weight: 700; letter-spacing: -.3px; margin: 0 0 6px; text-align: center; }
.sub { color: var(--muted); font-size: 14px; margin: 0 0 28px; text-align: center; }
.wrap { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; max-width: 760px; }
.card { display: block; width: 340px; max-width: 100%; padding: 20px; background: var(--card);
  border: 1px solid var(--border); border-radius: 12px; text-decoration: none; color: inherit;
  transition: border-color .15s; }
.card:hover { border-color: var(--accent); }
.card h2 { font-size: 15px; font-weight: 600; margin: 0 0 6px; color: var(--accent); }
.card p { margin: 0; color: var(--muted); font-size: 13px; }
</style></head><body>
<h1>My Music Collection</h1>
<div class="sub">Two views of the same collection. Switch between them at the top right.</div>
<div class="wrap">__CARDS__</div>
</body></html>"""


if __name__ == "__main__":
    main()
