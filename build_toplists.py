from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from common import DATA_ROOT

AREA_DISPLAY = {
    "hungarian": "Hungarian", "us": "US", "rnb": "R&B", "rock": "Rock",
    "magyar": "Magyar", "elektro": "Electronic", "pop": "Pop",
    "alternate": "Alternative", "latino": "Latino", "african": "African",
    "roman": "Romani", "reggae": "Reggae", "russian": "Russian",
    "countryjazz": "Country & Jazz", "vilagzene": "World", "mantra": "Mantra",
    "classical": "Classical", "intlrap": "International Rap",
    "intltrap": "International Trap",
}


def discover_areas() -> list[str]:
    """Every area with normalized data, found on disk rather than listed here.

    This was a hardcoded ("hungarian", "us") and stayed that way while the graph grew to
    nineteen areas, so seventeen of them had no toplist and nothing said so. Reading the
    directory means a new area shows up the first time it is built.
    """
    if not DATA_ROOT.exists():
        return []
    found = [p.name for p in sorted(DATA_ROOT.iterdir())
             if (p / "normalized" / "persons.json").exists()]
    # Full-schema areas first - they carry groups, labels and regions.
    return sorted(found, key=lambda a: (a not in ("us", "hungarian"), a))


def area_counts(metadata: dict, persons: dict, songs: list) -> dict:
    """Counts from either metadata shape.

    build_us_graph writes {"counts": {...}}; build_other_graph writes flat song_count /
    person_count / unattributed_count. Reading only the first shape made this crash on
    every _other area, which is part of why they were never added.
    """
    if "counts" in metadata:
        return metadata["counts"]
    return {
        "songs": metadata.get("song_count", len(songs)),
        "persons": metadata.get("person_count", len(persons)),
        "unattributed_songs": metadata.get("unattributed_count"),
    }


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_region_overrides(area: str) -> tuple[dict[str, str], dict[str, str]]:
    """Load manual person->region and group->region overrides if the file exists."""
    path = DATA_ROOT / area / "normalized" / "region_overrides.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("persons", {}), data.get("groups", {})
    return {}, {}


def compute_top_region(
    name: str,
    song_ids: list[str],
    song_map: dict[str, dict],
    region_overrides: dict[str, str] | None = None,
) -> str:
    if region_overrides and name in region_overrides:
        return region_overrides[name]
    counts = Counter()
    for song_id in song_ids:
        song = song_map.get(song_id)
        if not song:
            continue
        region = song.get("folder_region")
        if region:
            counts[region] += 1
    return counts.most_common(1)[0][0] if counts else ""


def compute_normalized_scores(
    songs: list[dict], groups: dict[str, dict]
) -> dict[str, float]:
    """For each song, expand all credits to unique persons, give each 1/N."""
    scores: dict[str, float] = {}
    for song in songs:
        persons_on_song: set[str] = set()
        for credit in song.get("credits", []):
            if credit["entity_type"] == "person":
                persons_on_song.add(credit["entity"])
            elif credit["entity_type"] == "group":
                group_data = groups.get(credit["entity"])
                if group_data:
                    for member in group_data.get("members", []):
                        persons_on_song.add(member)
        if not persons_on_song:
            continue
        share = 1.0 / len(persons_on_song)
        for person in persons_on_song:
            scores[person] = scores.get(person, 0.0) + share
    return scores


# Adjusted v2 overrides: person -> group -> custom weight
# Other members keep their normal 1/N; the override person gets this instead.
GROUP_WEIGHT_OVERRIDES: dict[str, dict[str, float]] = {
    "Eminem": {"D12": 1 / 3},
    "50 Cent": {"G-Unit": 1 / 2},
    "Ketioz": {"Jam Balaya": 1 / 2},
    "Scarface": {"Geto Boys": 1 / 2},
    "Ice Cube": {"N.W.A": 1 / 3},
    "Dr. Dre": {"N.W.A": 1 / 3},
    "Eazy-E": {"N.W.A": 1 / 3},
    "Birdman": {"Big Tymers": 1 / 2},
    "Mannie Fresh": {"Big Tymers": 1 / 2},
}


def compute_adjusted_scores(
    songs: list[dict], groups: dict[str, dict]
) -> dict[str, float]:
    """Adjusted v2: solo/individual primary gets 1.0, group members divide, features get 1/N."""
    scores: dict[str, float] = {}
    # Build set of all group members for quick lookup
    all_group_members: dict[str, set[str]] = {}  # group_name -> members
    for gname, gdata in groups.items():
        all_group_members[gname] = set(gdata.get("members", []))

    for song in songs:
        primary_persons: set[str] = set()
        feature_persons: set[str] = set()
        credited_groups: dict[str, set[str]] = {}  # group_name -> members

        for credit in song.get("credits", []):
            if credit["entity_type"] == "person":
                if credit["role"] == "primary":
                    primary_persons.add(credit["entity"])
                else:
                    feature_persons.add(credit["entity"])
            elif credit["entity_type"] == "group":
                if credit["entity"] in all_group_members:
                    credited_groups[credit["entity"]] = all_group_members[credit["entity"]]

        # All unique persons on this song
        all_persons: set[str] = set()
        all_persons.update(primary_persons)
        all_persons.update(feature_persons)
        for members in credited_groups.values():
            all_persons.update(members)

        if not all_persons:
            continue

        n_total = len(all_persons)

        # Persons who are on this song via a credited group
        via_group_persons: set[str] = set()
        for members in credited_groups.values():
            via_group_persons.update(members)

        # Solo primary: exactly 1 primary person and no group credits
        solo_primary = (
            len(primary_persons - via_group_persons) == 1
            and len(credited_groups) == 0
        )

        for person in all_persons:
            if person in via_group_persons:
                # Group member: check for override, otherwise 1/N
                override_share = None
                for group_name, members in credited_groups.items():
                    if person in members:
                        overrides = GROUP_WEIGHT_OVERRIDES.get(person, {})
                        if group_name in overrides:
                            override_share = overrides[group_name]
                            break
                share = override_share if override_share is not None else 1.0 / n_total
            elif person in primary_persons and solo_primary:
                # Sole primary artist gets full credit
                share = 1.0
            else:
                # Co-primary or feature: 1/N
                share = 1.0 / n_total

            scores[person] = scores.get(person, 0.0) + share

    return scores


def person_rows(
    persons: dict[str, dict],
    song_map: dict[str, dict],
    norm_scores: dict[str, float],
    adj_scores: dict[str, float],
    region_overrides: dict[str, str] | None = None,
) -> list[str]:
    ranked = sorted(
        persons.items(),
        key=lambda item: (-adj_scores.get(item[0], 0.0), item[0].lower()),
    )
    rows = []
    for idx, (name, payload) in enumerate(ranked, start=1):
        groups = ", ".join(payload.get("groups", [])) or "-"
        labels = ", ".join(payload.get("labels", [])) or "-"
        norm = norm_scores.get(name, 0.0)
        adj = adj_scores.get(name, 0.0)
        rows.append(
            "| {idx} | {name} | {songs} | {norm} | {adj} | {primary} | {feature} | {via_group} | {region} | {labels} | {groups} |".format(
                idx=idx,
                name=name,
                songs=len(payload.get("song_ids", [])),
                norm=f"{norm:.1f}",
                adj=f"{adj:.1f}",
                primary=len(payload.get("primary_song_ids", [])),
                feature=len(payload.get("feature_song_ids", [])),
                via_group=len(payload.get("via_group_song_ids", [])),
                region=compute_top_region(name, payload.get("song_ids", []), song_map, region_overrides) or "-",
                labels=labels,
                groups=groups,
            )
        )
    return rows


def group_rows(
    groups: dict[str, dict],
    song_map: dict[str, dict],
    group_region_overrides: dict[str, str] | None = None,
) -> list[str]:
    ranked = sorted(
        groups.items(),
        key=lambda item: (-len(item[1].get("song_ids", [])), item[0].lower()),
    )
    rows = []
    for idx, (name, payload) in enumerate(ranked, start=1):
        region = (group_region_overrides or {}).get(name) or compute_top_region(
            name, payload.get("song_ids", []), song_map
        ) or "-"
        rows.append(
            "| {idx} | {name} | {songs} | {members} | {region} | {labels} |".format(
                idx=idx,
                name=name,
                songs=len(payload.get("song_ids", [])),
                members=", ".join(payload.get("members", [])) or "-",
                region=region,
                labels=", ".join(payload.get("labels", [])) or "-",
            )
        )
    return rows


def label_rows(labels: dict[str, dict]) -> list[str]:
    ranked = sorted(
        labels.items(),
        key=lambda item: (-len(item[1].get("song_ids", [])), item[0].lower()),
    )
    rows = []
    for idx, (name, payload) in enumerate(ranked, start=1):
        rows.append(
            "| {idx} | {name} | {songs} | {persons} | {groups} | {regions} |".format(
                idx=idx,
                name=name,
                songs=len(payload.get("song_ids", [])),
                persons=len(payload.get("persons", [])),
                groups=len(payload.get("groups", [])),
                regions=", ".join(payload.get("regions", [])) or "-",
            )
        )
    return rows


def region_rows(regions: dict[str, dict] | dict) -> list[str]:
    if isinstance(regions, dict) and regions.get("status"):
        return [
            f"Regions status: `{regions['status']}`",
            "",
            regions.get("note", ""),
        ]
    ranked = sorted(
        regions.items(),
        key=lambda item: (-len(item[1].get("song_ids", [])), item[0].lower()),
    )
    rows = []
    for idx, (name, payload) in enumerate(ranked, start=1):
        rows.append(
            "| {idx} | {name} | {songs} | {persons} | {groups} | {labels} | {sources} |".format(
                idx=idx,
                name=name,
                songs=len(payload.get("song_ids", [])),
                persons=len(payload.get("persons", [])),
                groups=len(payload.get("groups", [])),
                labels=len(payload.get("labels", [])),
                sources=", ".join(payload.get("sources", [])) or "-",
            )
        )
    return rows


def build_area_toplist(area: str) -> None:
    base = DATA_ROOT / area / "normalized"
    metadata = load_json(base / "metadata.json")
    songs = load_json(base / "songs.json")
    song_map = {song["song_id"]: song for song in songs}
    persons = load_json(base / "persons.json")
    # The _other areas have no group/label/region indexes at all - their sections are
    # skipped rather than faked, so the file says what the area actually knows.
    groups = load_json(base / "groups.json") if (base / "groups.json").exists() else {}
    labels = load_json(base / "labels.json") if (base / "labels.json").exists() else {}
    regions = load_json(base / "regions.json") if (base / "regions.json").exists() else {}

    counts = area_counts(metadata, persons, songs)
    lines = [
        f"# {AREA_DISPLAY.get(area, area.capitalize())} Local Music Toplists",
        "",
        f"Songs: `{counts.get('songs', len(songs))}`",
        f"Persons: `{counts.get('persons', len(persons))}`",
    ]
    if groups:
        lines.append(f"Groups: `{counts.get('groups', len(groups))}`")
    if labels:
        lines.append(f"Labels: `{counts.get('labels', len(labels))}`")
    if regions:
        lines.append(f"Regions: `{counts.get('regions', len(regions))}`")
    if counts.get("unattributed_songs") is not None:
        lines.append(f"Unattributed songs: `{counts['unattributed_songs']}`")
    norm_scores = compute_normalized_scores(songs, groups)
    adj_scores = compute_adjusted_scores(songs, groups)
    person_region_overrides, group_region_overrides = load_region_overrides(area)

    lines.extend(
        [
            "",
            "## Persons",
            "",
            "| # | Artist | Songs | Norm | Adj | Primary | Feature | Via Group | Top Region | Labels | Groups |",
            "|---|--------|-------|------|-----|---------|---------|-----------|------------|--------|--------|",
            *person_rows(persons, song_map, norm_scores, adj_scores, person_region_overrides),
        ]
    )

    if groups:
        lines.extend(
            [
                "",
                "## Groups",
                "",
                "| # | Group | Songs | Members | Top Region | Labels |",
                "|---|-------|-------|---------|------------|--------|",
                *group_rows(groups, song_map, group_region_overrides),
            ]
        )
    if labels:
        lines.extend(
            [
                "",
                "## Labels",
                "",
                "| # | Label | Songs | Persons | Groups | Regions |",
                "|---|-------|-------|---------|--------|---------|",
                *label_rows(labels),
            ]
        )
    if regions:
        lines.extend(["", "## Regions", ""])
        region_section = region_rows(regions)
        if region_section and region_section[0].startswith("|"):
            lines.extend(
                [
                    "| # | Region | Songs | Persons | Groups | Labels | Sources |",
                    "|---|--------|-------|---------|--------|--------|---------|",
                    *region_section,
                ]
            )
        else:
            lines.extend(region_section)

    (base / "toplists.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    areas = discover_areas()
    if not areas:
        print("no normalized areas found")
        return 1
    for area in areas:
        build_area_toplist(area)
    print(f"Wrote toplists for {len(areas)} areas: {', '.join(areas)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
