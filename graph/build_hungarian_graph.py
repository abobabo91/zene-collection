"""Incremental scanner for the Hungarian area (`_magyar rap`, `_magyar trap`).

Usage: python build_hungarian_graph.py [--dry-run]

Why this is not just another `build_other_graph.py` area
--------------------------------------------------------
Two things make the Hungarian area different, and both are destructive if ignored:

1. **`song_id` is load-bearing.** `groups.json` and `labels.json` reference songs by id
   (`h-00507`), and those two files carry curation - 37 crews with their line-ups, 9 label
   rosters - that nothing else on disk records. A from-scratch scan renumbers every song in
   path order, so after a re-sort the ids still resolve but point at *different songs*. The
   graph would look healthy and be wrong. This builder therefore keeps the id of every file
   it can still identify and only mints ids for genuinely new ones.

2. **Region is curated, not derived.** The US area reads a city off the folder tree
   (`_rap/atlanta/...`); the Hungarian folders are sorted by artist, so an artist's home
   town exists only because someone wrote it down. It lives in the `region:` field of a
   Person entry and in `## Group regions`.

A file that moved is re-identified by its basename, which is what a re-sort preserves.
Matches are only accepted when exactly one unseen file on disk carries that basename -
two candidates means guessing, and guessing here silently reattributes a song.

Songs, groups, labels and region overrides are all **derived** from
`hungarian_rap_mappings.md` plus the disk. Edit the markdown, not the JSON.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from build_other_graph import infer_credit_and_title, prefer_display
from common import (
    AUDIO_EXTS, DATA_ROOT, FEAT_RE, ZENE,
    extract_primary_and_features, load_mappings_file, normalize_key,
)

AREA = "hungarian"
DATA_DIR = DATA_ROOT / AREA
MAPPINGS_PATH = DATA_DIR / "hungarian_rap_mappings.md"
NORMALIZED_DIR = DATA_DIR / "normalized"
ID_PREFIX = "h"

SCAN_ROOTS = [ZENE / "_magyar rap", ZENE / "_magyar trap"]

#: `km.` / `közr.` = közreműködik = featuring. `extract_primary_and_features` only knows the
#: English markers, so these are rewritten to `feat.` before credits are parsed.
HU_FEAT_RE = re.compile(r"\s+(?:km\.?|közr\.?|kozr\.?)\s+", re.IGNORECASE)

#: Names that two different artists share, resolved by which tree the file sits in.
#: `Filo` (IFS, Szeged) and `FILO` (`_magyar trap`) differ only in case, so `normalize_key`
#: cannot separate them and neither can an alias - an alias line for `filo` would map both
#: spellings onto one person again. The folder is the only thing that actually knows.
AMBIGUOUS_BY_ROOT = {
    "filo": {"_magyar rap": "Filo", "_magyar trap": "FILO"},
}

CONFIG = {
    "generic_folders": {
        "_magyar rap", "_magyar trap", "_random", "random", "_other", "misc",
        "videos", "youtube", "music - youtube", "album", "albums", "cd1", "cd2",
        "magyar rap", "magyar trap", "_cigany", "_magyar", "_other country random",
        # Label folders. They hold their whole roster, so read as an artist the label
        # collects the files sitting loose at its root - SCBP 3 songs, Bloose Broavaz 2,
        # Vicc Beatz 1. The label itself is tracked in labels.json, not as a person.
        # `IFS` is deliberately absent: it is a label *and* a group, and making it generic
        # would strip the group's folder context from its own songs.
        "scbp", "bloose broavaz", "vicc beatz",
    },
    "blocklist": {
        "n/a", "unknown", "various", "nothing", "you", "me", "lyrics", "audio",
        "music", "official", "official music video", "official video", "subscribe",
        "premium studio", "open stage", "hivatalos", "videoklip", "teljes album",
    },
    "split_groups": set(),
}


# ── helpers ────────────────────────────────────────────────────────────────────

def norm_path(p) -> str:
    return str(p).replace("/", "\\").lower()


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def scan_disk() -> dict[str, Path]:
    """Every audio file under the Hungarian roots, keyed by normalized relative path."""
    found: dict[str, Path] = {}
    for root in SCAN_ROOTS:
        if not root.exists():
            print(f"  !! scan root missing: {root}")
            continue
        for p in root.rglob("*"):
            # `is_file()` is not redundant with the suffix test: `_magyar rap/el bago/
            # ultimohombre/ultimohombre.mp3` is a *directory* holding four real tracks.
            if p.is_file() and p.suffix.lower() in AUDIO_EXTS:
                found[norm_path(p.relative_to(ZENE))] = p.relative_to(ZENE)
    return found


def next_id_factory(existing_ids: set[str]):
    highest = 0
    for sid in existing_ids:
        try:
            highest = max(highest, int(sid.split("-")[1]))
        except (IndexError, ValueError):
            continue
    counter = {"n": highest}

    def mint() -> str:
        counter["n"] += 1
        return f"{ID_PREFIX}-{counter['n']:05d}"

    return mint


def attribute(rel: Path, mappings: dict) -> dict:
    """Build a song record for a file the curated data has never seen."""
    parts = list(rel.parts)
    filename = HU_FEAT_RE.sub(" feat. ", rel.name)
    credit_str, title = infer_credit_and_title(parts, filename, mappings, CONFIG)

    primary_raw, feat_raw = extract_primary_and_features(credit_str) if credit_str else ([], [])
    if not feat_raw:
        _, feat_from_title = extract_primary_and_features(title)
        if feat_from_title:
            feat_raw = feat_from_title
            title = FEAT_RE.split(title)[0].strip(" -,")

    root = parts[0]

    def resolve(names):
        out = []
        for n in names:
            display = prefer_display(n, mappings, CONFIG)
            by_root = AMBIGUOUS_BY_ROOT.get(normalize_key(display))
            if by_root:
                display = by_root.get(root, display)
            if display != "N/A" and display not in out:
                out.append(display)
        return out

    primary = resolve(primary_raw)
    featuring = resolve(feat_raw)

    primary_artists, primary_groups, featuring_artists, featuring_groups = [], [], [], []
    credits, artists = [], []
    for name in primary:
        group = mappings["group_lookup"].get(normalize_key(name))
        if group:
            primary_groups.append(group)
            credits.append({"entity": group, "entity_type": "group", "role": "primary"})
        else:
            primary_artists.append(name)
            credits.append({"entity": name, "entity_type": "person", "role": "primary"})
            if name not in artists:
                artists.append(name)
    already = {normalize_key(x) for x in primary_artists + primary_groups}
    for name in featuring:
        group = mappings["group_lookup"].get(normalize_key(name))
        # A folder-derived primary and a filename-derived feature can be the same act:
        # `Akkezdet Phiai/Bankos Fárasztó remix feat Akkezdet Phiai.mp3` credited the group
        # as both. A feature credit for whoever is already the primary is noise.
        if normalize_key(group or name) in already:
            continue
        if group:
            featuring_groups.append(group)
            credits.append({"entity": group, "entity_type": "group", "role": "feature"})
        else:
            featuring_artists.append(name)
            credits.append({"entity": name, "entity_type": "person", "role": "feature"})
            if name not in artists:
                artists.append(name)

    return {
        "song_id": None,                       # assigned by the caller
        "file": str(rel),
        "title": title,
        "title_variants": [],
        "source_root": parts[0],
        "folder_region": None,
        "regions": [],
        "primary_artists": primary_artists,
        "primary_groups": primary_groups,
        "featuring_artists": featuring_artists,
        "featuring_groups": featuring_groups,
        "artists": artists,
        "credits": credits,
    }


# ── reconciliation ─────────────────────────────────────────────────────────────

def needs_reattribution(song: dict, mappings: dict) -> bool:
    """Should this song's credits be re-derived rather than carried forward?

    The scanner keeps existing credits, which is the point - they are curated. But a credit
    that is *invalid under the current config* is not curation worth keeping, and carrying
    it forward means a fix to `generic_folders` or the attribution rules never reaches the
    songs it was written for. Two cases qualify, both safe because neither preserves real
    information: a song credited to nobody, and a song credited to a name the config now
    says is a folder rather than a person (the SCBP / Bloose Broavaz / Vicc Beatz label
    folders).
    """
    primary = song.get("primary_artists") or []
    groups = song.get("primary_groups") or []
    if not primary and not groups:
        return True
    generic = {normalize_key(g) for g in CONFIG["generic_folders"]}
    blocked = {normalize_key(b) for b in CONFIG["blocklist"]}
    return any(normalize_key(p) in generic or normalize_key(p) in blocked
               for p in primary + groups)


def reconcile(existing: list[dict], disk: dict[str, Path], mappings: dict) -> tuple[list[dict], dict]:
    by_path = {norm_path(s["file"]): s for s in existing}
    mint = next_id_factory({s["song_id"] for s in existing})

    songs: list[dict] = []
    used_existing: set[str] = set()
    redone: list[dict] = []

    # 1. files whose path is unchanged
    for key, rel in disk.items():
        s = by_path.get(key)
        if s is not None:
            if needs_reattribution(s, mappings):
                fresh = attribute(rel, mappings)
                fresh["song_id"] = s["song_id"]          # the id is what must not move
                fresh["title_variants"] = s.get("title_variants", [])
                if fresh["primary_artists"] or fresh["primary_groups"]:
                    redone.append((s, fresh))
                    s = fresh
                else:
                    s = dict(s)
                    s["file"] = str(rel)
            else:
                s = dict(s)
                s["file"] = str(rel)           # adopt the on-disk casing
            songs.append(s)
            used_existing.add(s["song_id"])

    # 2. curated songs that live outside the scan roots but are still on disk.
    #    14 Hungarian-rap tracks sit under `_other/_magyar/_cigany` on purpose; dropping
    #    them because the scan root does not reach them would be a silent regression.
    outside = []
    for s in existing:
        if s["song_id"] in used_existing:
            continue
        if norm_path(s["file"]) in disk:
            continue
        if (ZENE / s["file"]).is_file():      # not .exists(): a directory can be named `.mp3`
            songs.append(dict(s))
            used_existing.add(s["song_id"])
            outside.append(s)

    # 3. match what is left: dead curated entries against unseen files, by basename
    dead = [s for s in existing if s["song_id"] not in used_existing]
    unseen = {k: rel for k, rel in disk.items() if k not in by_path}

    unseen_by_base: dict[str, list[str]] = defaultdict(list)
    for k, rel in unseen.items():
        unseen_by_base[rel.name.lower()].append(k)

    moved, ambiguous, dropped = [], [], []
    claimed: set[str] = set()
    for s in dead:
        base = Path(s["file"]).name.lower()
        candidates = [k for k in unseen_by_base.get(base, []) if k not in claimed]
        if len(candidates) == 1:
            key = candidates[0]
            claimed.add(key)
            moved_song = dict(s)
            rel = unseen[key]
            moved_song["file"] = str(rel)
            moved_song["source_root"] = rel.parts[0]
            songs.append(moved_song)
            moved.append((s["file"], str(rel)))
        elif len(candidates) > 1:
            ambiguous.append((s["file"], [str(unseen[k]) for k in candidates]))
            dropped.append(s)
        else:
            dropped.append(s)

    # 4. everything still unclaimed on disk is genuinely new
    fresh = []
    for key, rel in sorted(unseen.items()):
        if key in claimed:
            continue
        song = attribute(rel, mappings)
        song["song_id"] = mint()
        songs.append(song)
        fresh.append(song)

    songs.sort(key=lambda s: norm_path(s["file"]))
    stats = {"kept": len(used_existing) - len(outside), "outside": outside, "moved": moved,
             "ambiguous": ambiguous, "dropped": dropped, "new": fresh, "redone": redone}
    return songs, stats


# ── derived indexes ────────────────────────────────────────────────────────────

def build_persons(songs: list[dict], mappings: dict) -> dict:
    entries = mappings["person_entries"]
    by_key = {normalize_key(n): n for n in entries}
    persons: dict[str, dict] = {}

    def slot(name: str) -> dict:
        return persons.setdefault(name, {
            "type": "person", "labels": [], "groups": [], "regions": [],
            "song_ids": [], "primary_song_ids": [], "feature_song_ids": [],
        })

    group_members = mappings["groups"]
    for s in songs:
        for credit in s["credits"]:
            entity, role = credit["entity"], credit["role"]
            if credit["entity_type"] == "person":
                # `Unknown` is a placeholder the hand-curation left behind on 3 songs, not
                # a person. It ranked in the area's artist list.
                if entity in ("N/A", "Unknown"):
                    continue
                p = slot(entity)
                if s["song_id"] not in p["song_ids"]:
                    p["song_ids"].append(s["song_id"])
                bucket = "primary_song_ids" if role == "primary" else "feature_song_ids"
                if s["song_id"] not in p[bucket]:
                    p[bucket].append(s["song_id"])
            else:
                # a group credit reaches its members as `via_group`
                for member in group_members.get(entity, []):
                    p = slot(member)
                    p.setdefault("via_group_song_ids", [])
                    if s["song_id"] not in p["song_ids"]:
                        p["song_ids"].append(s["song_id"])
                    if s["song_id"] not in p["via_group_song_ids"]:
                        p["via_group_song_ids"].append(s["song_id"])

    # curated attributes from the mappings file
    for name, p in persons.items():
        entry = entries.get(name) or entries.get(by_key.get(normalize_key(name), ""), None)
        if not entry:
            continue
        p["labels"] = list(entry.get("labels", []))
        p["groups"] = list(entry.get("groups", []))
        region = entry.get("region", "")
        p["regions"] = [region] if region else []
    return dict(sorted(persons.items(), key=lambda kv: kv[0].lower()))


def build_groups(songs: list[dict], mappings: dict) -> dict:
    # A group's label comes from `## Group labels`, never from what its members are signed
    # to. Deriving it both loses and invents: `Nevenincs` is a goldsoul act with no member
    # list (label and 13 songs lost), while `Hősök` and `Gruppen Family` would pick up
    # Bloose Broavaz purely because Eckü and Siska Finuccsi are signed there.
    label_of = mappings["group_labels"]

    groups: dict[str, dict] = {}
    for gname, members in mappings["groups"].items():
        groups[gname] = {
            "type": "group",
            "members": list(members),
            "labels": sorted(label_of.get(gname, []), key=str.lower),
            "regions": [mappings["group_regions"][gname]] if gname in mappings["group_regions"] else [],
            "song_ids": [],
        }
    for s in songs:
        for credit in s["credits"]:
            if credit["entity_type"] == "group":
                g = groups.get(credit["entity"])
                if g is not None and s["song_id"] not in g["song_ids"]:
                    g["song_ids"].append(s["song_id"])
    return dict(sorted(groups.items(), key=lambda kv: kv[0].lower()))


def build_labels(songs: list[dict], mappings: dict, persons: dict, groups: dict) -> dict:
    labels: dict[str, dict] = {}
    for lname, roster in mappings["labels"].items():
        member_groups = sorted((g for g, d in groups.items() if lname in d["labels"]), key=str.lower)
        song_ids: list[str] = []
        for person in roster:
            for sid in persons.get(person, {}).get("song_ids", []):
                if sid not in song_ids:
                    song_ids.append(sid)
        for g in member_groups:
            for sid in groups[g]["song_ids"]:
                if sid not in song_ids:
                    song_ids.append(sid)
        labels[lname] = {
            "type": "label",
            "persons": list(roster),
            "groups": member_groups,
            "regions": [],
            "song_ids": sorted(song_ids),
        }
    return dict(sorted(labels.items(), key=lambda kv: kv[0].lower()))


def build_region_overrides(mappings: dict) -> dict:
    return {
        "_doc": ("Generated by build_hungarian_graph.py from hungarian_rap_mappings.md - "
                 "edit the `region:` field of a Person entry or the `## Group regions` "
                 "section there, not this file."),
        "persons": {name: entry["region"]
                    for name, entry in sorted(mappings["person_entries"].items(),
                                              key=lambda kv: kv[0].lower())
                    if entry.get("region")},
        "groups": dict(sorted(mappings["group_regions"].items(), key=lambda kv: kv[0].lower())),
    }


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    dry_run = "--dry-run" in sys.argv
    mappings = load_mappings_file(MAPPINGS_PATH)
    existing = load_json(NORMALIZED_DIR / "songs.json", [])
    disk = scan_disk()

    songs, stats = reconcile(existing, disk, mappings)
    persons = build_persons(songs, mappings)
    groups = build_groups(songs, mappings)
    labels = build_labels(songs, mappings, persons, groups)
    overrides = build_region_overrides(mappings)

    unattributed = [s for s in songs
                    if not s["primary_artists"] and not s["primary_groups"]]

    print(f"[{AREA}] disk {len(disk)} files -> {len(songs)} songs "
          f"({len(existing)} before)")
    print(f"  path unchanged   {stats['kept']}")
    print(f"  outside roots    {len(stats['outside'])}  (kept: still on disk)")
    print(f"  moved, re-matched{len(stats['moved']):>4}")
    print(f"  ambiguous        {len(stats['ambiguous'])}")
    print(f"  dropped (gone)   {len(stats['dropped'])}")
    print(f"  new              {len(stats['new'])}")
    print(f"  re-attributed    {len(stats['redone'])}  (were unattributed or credited to a folder)")
    print(f"  persons {len(persons)}  groups {len(groups)}  labels {len(labels)}  "
          f"unattributed {len(unattributed)}")

    for old, new in stats["moved"][:10]:
        print(f"    moved: {old}\n        -> {new}")
    for old, cands in stats["ambiguous"]:
        print(f"    AMBIGUOUS, left dropped: {old}\n        candidates: {cands}")
    for s in stats["new"][:15]:
        who = s["primary_artists"] or s["primary_groups"] or ["<unattributed>"]
        print(f"    new: {s['song_id']}  {'/'.join(who)} - {s['title']}")
        print(f"         {s['file']}")

    if dry_run:
        print("\n--dry-run: nothing written.")
        return 0

    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {
        "source_format": "hungarian_incremental_scan",
        "schema_version": 1,
        "counts": {
            "songs": len(songs), "persons": len(persons), "groups": len(groups),
            "labels": len(labels), "unattributed_songs": len(unattributed),
        },
        "notes": [
            "Songs are the source of truth; persons, groups and labels are derived indexes.",
            "song_id is stable across rebuilds - groups.json and labels.json reference it.",
            "Curation lives in hungarian_rap_mappings.md, not in these files.",
        ],
    }
    for filename, payload in [
        ("songs.json", songs), ("persons.json", persons), ("groups.json", groups),
        ("labels.json", labels), ("region_overrides.json", overrides),
        ("metadata.json", metadata),
    ]:
        (NORMALIZED_DIR / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {NORMALIZED_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
