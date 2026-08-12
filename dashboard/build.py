"""Összegyűjti a három dashboardot egy helyre, és összeköti őket.

Szándékosan **nem** írja át egyiket sem: mindegyik pontosan úgy néz ki és úgy működik,
ahogy a saját repójában. Az egyetlen beavatkozás egy lebegő navigációs pirula a jobb felső
sarokban, `position:fixed`-del, ami nem nyúl bele a lap elrendezésébe - az idővonal
teljes-magasságú grafikonja és a gráf tab-szerkezete így érintetlen marad.

A forrás mindig a másik két repó aktuális kimenete, tehát ez a mappa újraépíthető, nem
kézzel karbantartott másolat.

    python build.py      # begyűjt + navigációt injektál
    python serve.py      # kiszolgálja (a timeline fetch-el, ahhoz http kell)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
#: A repó gyökere. Az idővonal és a gráf 2026-08-12 óta ide, ugyanebbe a repóba tartozik
#: (`timeline/`, `graph/`), így a forrásuk testvérmappa, nem külön repó.
REPO = os.path.dirname(HERE)
SCRIPTS = os.path.dirname(REPO)
#: Az audio profilok külön projekt: a `_elektro_classifier` 2026-08-12-én beolvadt a
#: `music-generation` repóba `projects/library-classifier` néven. Amíg a régi helyre
#: mutattunk, az audio fül 404-elt az élő oldalon. Ha nincs meg, a begyűjtés kihagyja.
AUDIO_SRC = os.path.join(os.path.dirname(SCRIPTS), "music-generation",
                         "projects", "library-classifier", "data")
#: A kimenet a `docs/`, mert a GitHub Pages csak a repó gyökeréből vagy a `docs/`-ból tud
#: kiszolgálni. A gyökér nem jöhet szóba: a `graph/` és a `timeline/` ott már a *forrás*, a
#: dashboard pedig ugyanilyen nevű almappákba másol, tehát ütköznének.
OUT = os.path.join(REPO, "docs")

#: (célmappa, cím, forrásfájlok) - az első fájl mindig a belépő index.html
SOURCES = [
    ("timeline", "Idővonal", os.path.join(REPO, "timeline"),
     ["index.html", "genre_catalog.json", "recent_playlists.json"]),
    ("graph", "Előadó-gráf", os.path.join(REPO, "graph"),
     ["index.html"]),
    ("audio", "Audio profilok", AUDIO_SRC,
     [("zene_library.html", "index.html")]),
]

NAV = """
<!-- zene_dashboard: közös navigáció. position:fixed, hogy a lap saját elrendezését
     ne befolyásolja - se az idővonal 100vh-s grafikonját, se a gráf füleit. -->
<div id="zdnav" style="position:fixed;top:8px;right:10px;z-index:2147483000;
  display:flex;gap:2px;background:rgba(14,17,22,.92);border:1px solid #2a323d;
  border-radius:999px;padding:3px;font:12px/1.4 ui-sans-serif,system-ui,Segoe UI,sans-serif;
  box-shadow:0 2px 10px rgba(0,0,0,.45);backdrop-filter:blur(4px)">__LINKS__</div>
"""
LINK = ('<a href="__HREF__" style="color:__COLOR__;text-decoration:none;padding:4px 11px;'
        'border-radius:999px;__BG__">__LABEL__</a>')


def nav_html(current):
    links = []
    for slug, label, _, _ in SOURCES:
        here = slug == current
        links.append(LINK
                     .replace("__HREF__", "../index.html" if False else f"../{slug}/index.html")
                     .replace("__LABEL__", label)
                     .replace("__COLOR__", "#e6edf3" if here else "#8b949e")
                     .replace("__BG__", "background:#1b2735;" if here else ""))
    return NAV.replace("__LINKS__", "".join(links))


def inject(html, current):
    """A navigációt közvetlenül a </body> elé teszi, hogy semmit ne előzzön meg."""
    block = nav_html(current)
    if 'id="zdnav"' in html:                       # újraépítésnél ne duplázzuk
        html = re.sub(r"\n?<!-- zene_dashboard.*?</div>\n?", "", html, flags=re.S)
    if "</body>" in html:
        return html.replace("</body>", block + "</body>", 1)
    return html + block


def counts():
    """A kártyák számai a forrásokból, nem beégetve.

    Beégetve elavulnak, és csendben: a nyitólap `15,465 bejegyzés`-t hirdetett, miközben a
    katalógusban már csak 14,975 sor volt. Ami nem olvasható ki, az None, és a kártya
    egyszerűen szám nélkül jelenik meg - kitalálni rosszabb, mint elhagyni.
    """
    out = {"timeline": None, "graph": None, "audio": None}
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
    try:
        feats = os.path.join(AUDIO_SRC, "features_long.json")
        rows = json.load(open(feats, encoding="utf-8"))
        out["audio"] = sum(1 for v in rows.values()
                           if isinstance(v, dict) and "feature_vector" in v)
    except (OSError, ValueError, AttributeError):
        pass
    return out


def main():
    # A gyökér `rebuild.py` minden szakaszra ráadja a `--dry-run`-t, tehát ezt itt tényleg
    # be kell tartani - különben a "semmit nem ír" futás mégis felülírja a dashboardot.
    dry = "--dry-run" in sys.argv
    if dry:
        print("(dry run - semmit nem írok)")
    for slug, label, src, files in SOURCES:
        dst = os.path.join(OUT, slug)
        if not dry:
            os.makedirs(dst, exist_ok=True)
        for entry in files:
            name, out = entry if isinstance(entry, tuple) else (entry, entry)
            s = os.path.join(src, name)
            if not os.path.exists(s):
                print(f"  !! hiányzik: {s}")
                continue
            d = os.path.join(dst, out)
            if dry:
                print(f"  {slug}/{out:<22} {os.path.getsize(s)/1024:>8.0f} KB   <- {name} (nem másolom)")
                continue
            if out.endswith(".html"):
                html = open(s, encoding="utf-8").read()
                open(d, "w", encoding="utf-8").write(inject(html, slug))
            else:
                shutil.copy2(s, d)
            print(f"  {slug}/{out:<22} {os.path.getsize(d)/1024:>8.0f} KB   <- {name}")
    if dry:
        return

    # Magyar ezres elválasztó a szóköz. Csak a számra kell alkalmazni - a `,`-t a teljes
    # mondaton lecserélve a tagmondatok vesszői is eltűnnek.
    hu = lambda v: f"{v:,}".replace(",", " ")

    n = counts()
    timeline_desc = "Mikor került be mi a gyűjteménybe, műfajonként, kumulált nézetben."
    if n["timeline"]:
        timeline_desc += f" {hu(n['timeline'])} bejegyzés."
    graph_desc = "Ki kivel szerepel, előadóra kattintva a mappafája."
    if n["graph"]:
        total, areas = n["graph"]
        graph_desc = (f"Ki kivel szerepel, {areas} terület fülenként, előadóra kattintva "
                      f"a mappafája. {hu(total)} szám.")
    audio_desc = "Az audióból kinyert metrikák: trackenkénti profil, stílusok, térkép."
    if n["audio"]:
        audio_desc += (f" Csak az elektro fa: {hu(n['audio'])} track, "
                       "a többi műfajra még nem futott le.")

    cards = "".join(
        f'<a class="card" href="{slug}/index.html"><h2>{label}</h2><p>{desc}</p></a>'
        for slug, label, desc in [
            ("timeline", "Idővonal", timeline_desc),
            ("graph", "Előadó-gráf", graph_desc),
            ("audio", "Audio profilok", audio_desc),
        ])
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        LANDING.replace("__CARDS__", cards))
    print(f"  index.html (nyitólap)   idővonal={n['timeline']} gráf={n['graph']} "
          f"audio={n['audio']}")
    print(f"  -> {OUT}  (ezt szolgálja ki a GitHub Pages)")


LANDING = """<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><title>Zene dashboard</title>
<style>
body{margin:0;background:#0e1116;color:#e6edf3;font:14px/1.6 ui-sans-serif,system-ui,Segoe UI,sans-serif;
 display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh}
h1{font-size:20px;font-weight:600;margin:0 0 4px}
.sub{color:#8b949e;font-size:13px;margin-bottom:26px}
.wrap{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;max-width:900px}
.card{display:block;width:250px;padding:18px 20px;border:1px solid #232a33;border-radius:12px;
 text-decoration:none;color:inherit;background:#11161d;transition:border-color .15s}
.card:hover{border-color:#5aa9e6}
.card h2{font-size:15px;margin:0 0 6px;color:#5aa9e6}
.card p{margin:0;color:#8b949e;font-size:12.5px}
</style></head><body>
<h1>Zene dashboard</h1>
<div class="sub">a gyűjtemény három nézete — a lapok közt jobb felül lehet váltani</div>
<div class="wrap">__CARDS__</div>
</body></html>"""


if __name__ == "__main__":
    main()
