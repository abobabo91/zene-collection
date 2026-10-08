"""
Scan the full music library and produce a JSON catalog with genre tags
derived from the folder structure.

Excludes the folders in `buildkit.SKIP_ROOTS`.
"""

import json
import os
import sys
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from buildkit import SKIP_ROOTS, ZENE, is_blocked  # noqa: E402
OUTPUT = Path(__file__).parent / "genre_catalog.json"

REGION_NORM = {
    "_usa other": "usa",
    "_usa random": "usa",
    "_other random": None,
    "luisiana": "louisiana",
    "philly": "philadelphia",
    "phily": "philadelphia",
    "dc": "dc",
    "2Pac": "california",
}

ELEKTRO_SUB = {
    "deep_house": "deep house",
    "dnb_dubstep": "dnb & dubstep",
    "edm_electronic_pop": "edm",
    "experimental": "experimental",
    "experimental_chill": "experimental chill",
    "goa_psytrance": "psytrance",
    "hardcore_hardstyle": "hardcore & hardstyle",
    "house_afro_organic": "afro & organic house",
    "house_techno": "house & techno",
    "trance_dance_rave": "trance & rave",
}

MAGYAR_SUB = {
    "_alternativ": "alternative",
    "_cigany": "cigany",
    "_modern_pop": "modern pop",
    "_nepzene": "nepzene",
    "_pop": "pop",
    "_random": None,
    "_retro": "retro",
    "_rock": "rock",
}

POP_SUB = {
    "_billboard": "billboard",
    "_kpop": "kpop",
    "_modern": "modern",
    "_oldschool_pop": "oldschool",
    "_random": None,
}

LATINO_SUB = {
    "_oldschool": "oldschool",
    "_random": None,
}

RAP_OTHER_SUB = {
    "_german random": "german",
    "_other random": None,
    "_roman": "romanian",
    "_uk rap grime": "uk",
}


def classify(rel: str) -> tuple[str | None, str | None]:
    parts = Path(rel).parts

    root = parts[0]

    if root == "_rap":
        if len(parts) < 2:
            return ("rap", None)
        region = parts[1]
        if region == "_other":
            if len(parts) >= 3:
                return ("rap", RAP_OTHER_SUB.get(parts[2]))
            return ("rap", None)
        return ("rap", REGION_NORM.get(region, region))

    if root == "_trap":
        if len(parts) < 2:
            return ("trap", None)
        region = parts[1]
        if region == "_other country random":
            return ("trap", None)
        return ("trap", REGION_NORM.get(region, region))

    if root == "_magyar rap":
        return ("hungarian rap", None)
    if root == "_magyar trap":
        return ("hungarian trap", None)

    if root == "_other":
        if len(parts) < 2:
            return ("other", None)
        cat = parts[1]

        if cat == "_african music":
            return ("african", None)
        if cat == "_alternate":
            return ("alternative", None)
        if cat == "_classical":
            return ("classical", None)
        if cat == "_country_jazz":
            return ("country & jazz", None)
        if cat == "_mantra":
            return ("mantra", None)
        if cat == "_reggea":
            return ("reggae", None)
        if cat == "_rnb":
            return ("r&b", None)
        if cat == "_rock":
            return ("rock", None)
        if cat == "_vilagzene":
            return ("world music", None)

        if cat == "_elektro":
            if len(parts) >= 3:
                sub = ELEKTRO_SUB.get(parts[2])
                if sub is not None:
                    return ("electronic", sub)
            return ("electronic", None)

        if cat == "_magyar":
            if len(parts) >= 3:
                return ("hungarian", MAGYAR_SUB.get(parts[2]))
            return ("hungarian", None)

        if cat == "_pop":
            if len(parts) >= 3:
                sub = POP_SUB.get(parts[2])
                if sub is not None:
                    return ("pop", sub)
            return ("pop", None)

        if cat == "_latino":
            if len(parts) >= 3:
                sub = LATINO_SUB.get(parts[2])
                if sub is not None:
                    return ("latin", sub)
            return ("latin", None)

        if cat == "_roman":
            if len(parts) >= 3:
                sub = parts[2].lstrip("_")
                return ("romanian", sub)
            return ("romanian", None)

        if cat in ("_russian", "_orosz"):
            if len(parts) >= 3:
                sub = parts[2].lstrip("_")
                return ("russian", sub if sub == "trap" else None)
            return ("russian", None)

        return ("other", None)

    return ("other", None)


def main():
    entries = []
    for dirpath, _dirs, files in os.walk(ZENE):
        for f in files:
            if not f.lower().endswith(".mp3"):
                continue
            full = Path(dirpath) / f
            rel = full.relative_to(ZENE)
            if rel.parts[0] in SKIP_ROOTS:
                continue
            if is_blocked(rel):
                continue

            main_genre, sub_genre = classify(str(rel))
            mtime = os.path.getmtime(full)

            entries.append({
                "file": str(rel),
                "main_genre": main_genre,
                "sub_genre": sub_genre,
                # UTC, not local time. `fromtimestamp` without a tz renders in whatever
                # zone the machine is set to, so moving the laptop rewrites all 15,296 rows
                # by the offset: the move to US Eastern on 2026-09-22 shifted every one by
                # six hours, produced a 46,081-line diff in which no song had changed, and
                # walks anything near midnight into the previous day, quarter or year.
                "modified": datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            })

    entries.sort(key=lambda e: e["modified"], reverse=True)
    OUTPUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {OUTPUT}")

    mains = Counter(e["main_genre"] for e in entries)
    print("\nMain genre distribution:")
    for g, c in mains.most_common():
        print(f"  {g}: {c}")


if __name__ == "__main__":
    main()
