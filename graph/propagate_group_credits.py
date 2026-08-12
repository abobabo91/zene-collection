"""Give group members credit for their group's songs, for areas built without a scanner.

`build_us_graph.py` does this while scanning: every member of a declared group gets the
group's songs in `via_group_song_ids`. The Hungarian area has no scanner - its normalized
JSONs are maintained by hand - so the field was never populated there, and 581 songs
across 37 groups reached none of their members. Ketioz, for one, is correctly listed in
Jam Balaya and Egyenlok yet had 0 group songs.

Not run for R&B: those groups are deliberately treated as single entities (except
Destiny's Child), so splitting them to members would be wrong.

    python propagate_group_credits.py hungarian [--dry-run]

Idempotent - re-running changes nothing.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import DATA_ROOT


def propagate(area: str, dry_run: bool = False) -> dict:
    base = DATA_ROOT / area / "normalized"
    persons_path = base / "persons.json"
    groups_path = base / "groups.json"
    if not groups_path.exists():
        raise SystemExit(f"{area}: no groups.json, nothing to propagate")

    persons = json.loads(persons_path.read_text(encoding="utf-8"))
    groups = json.loads(groups_path.read_text(encoding="utf-8"))

    changed = {}
    for group_name, group in groups.items():
        song_ids = list(group.get("song_ids") or [])
        if not song_ids:
            continue
        for member in group.get("members") or []:
            person = persons.get(member)
            if person is None:
                changed.setdefault("_missing_persons", set()).add(member)
                continue
            via = list(person.get("via_group_song_ids") or [])
            known = set(via)
            added = [song_id for song_id in song_ids if song_id not in known]
            if not added:
                continue
            person["via_group_song_ids"] = via + added

            # song_ids is the union of every credit, so it has to grow too
            all_ids = list(person.get("song_ids") or [])
            seen = set(all_ids)
            person["song_ids"] = all_ids + [sid for sid in added if sid not in seen]
            changed[member] = changed.get(member, 0) + len(added)

    missing = changed.pop("_missing_persons", set())
    if not dry_run:
        persons_path.write_text(json.dumps(persons, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"changed": changed, "missing_persons": sorted(missing)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("area")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = propagate(args.area, dry_run=args.dry_run)
    changed = result["changed"]
    total = sum(changed.values())
    print(f"{args.area}: {len(changed)} persons gained {total} group song credits"
          + (" (dry run)" if args.dry_run else ""))
    for member, count in sorted(changed.items(), key=lambda kv: -kv[1])[:20]:
        print(f"  {count:>4}  {member}")
    if result["missing_persons"]:
        print(f"\ngroup members with no person entry ({len(result['missing_persons'])}): "
              f"{', '.join(result['missing_persons'][:10])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
