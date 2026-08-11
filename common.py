"""Shared constants and utilities for local-music-graph scripts."""
from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  (re-exported for type hints in load_mappings_file)

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"
ZENE = Path(r"C:\Users\abele\Desktop\zene")

# ── Constants ──────────────────────────────────────────────────────────────────
AUDIO_EXTS = {".mp3", ".wma", ".wav", ".m4a", ".flac"}

# ── Regexes ────────────────────────────────────────────────────────────────────
FEAT_RE = re.compile(r"\b(?:feat\.?|ft\.?|featuring|with|w\/)\b", re.IGNORECASE)
UNICODE_DASH_RE = re.compile(r"[–—]+")

NOISE_PATTERNS = [
    r"\(DatPiff\.com\)", r"\[DatPiff.*?\]", r"\[www\..*?\]",
    r"\bOfficial Music Video\b", r"\bOfficial Video\b", r"\bOfficial Audio\b",
    r"\bOfficial Lyric Video\b", r"\bOfficial Visualizer\b",
    r"\bOFFICIAL VIDEO\b", r"\bOFFICIAL AUDIO\b",
    r"\bWSHH\s+Exclusive\b.*", r"\bWSHH\s+Premiere\b.*", r"\bWSHH\b",
    r"\bHD\b", r"\bHQ\b", r"\[\d{3}\]", r"\(\d{3}\)",
    r"\bVideo Oficial\b", r"\bvideo oficial\b", r"\bClip Officiel\b",
    r"\bvideoclip oficial\b", r"\bOfficiel\b",
    r"\(Original Mix\)", r"\(Radio Edit\)", r"\(Extended Mix\)",
    r"\[NCS Release\]", r"\[NCS\]",
    r"\bOriginal Mix\b", r"\bRadio Edit\b",
    r"\bFull Version\b", r"\bLyric Video\b", r"\bLyrics\b",
]

_ACCENT_MAP = str.maketrans(
    "áàâäãåéèêëíìîïóòôöõőúùûüűýñçšž",
    "aaaaaaeeeeiiiioooooouuuuuyncsz",
)


# ── Text utilities ─────────────────────────────────────────────────────────────

def normalize_key(text: str) -> str:
    value = text.lower().replace("_", " ").replace("&", " and ")
    value = value.translate(_ACCENT_MAP)
    value = re.sub(r"[^a-z0-9+]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def squash_key(text: str) -> str:
    """normalize_key with the spaces removed, for folders that drop them.

    A folder called `50cent` never matched the person `50 Cent`, so the 79 files under
    `_rap/new york/G-Unit/50cent/` - five full solo albums - were credited to nobody and
    were invisible to everything downstream. Its siblings `Lloyd Banks` and `Young Buck`
    matched fine, which is why it went unnoticed: the failure is per-folder and silent.
    """
    return normalize_key(text).replace(" ", "")


def squashed_lookup(lookup: dict) -> dict:
    """Space-insensitive view of an alias lookup, ambiguous keys dropped.

    Only keys that squash to exactly one canonical name are kept. Two different artists
    collapsing onto the same spaceless string would otherwise silently reattribute one of
    them, which is a worse failure than the missing folder this exists to fix.
    """
    by_squashed: dict = {}
    for key, canonical in lookup.items():
        by_squashed.setdefault(key.replace(" ", ""), set()).add(canonical)
    return {key: next(iter(names)) for key, names in by_squashed.items() if len(names) == 1}


def clean_artist_text(text: str) -> str:
    value = UNICODE_DASH_RE.sub("-", text).replace("_", " ").strip()
    value = re.sub(r"\(.*?datpiff.*?\)", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\(.*?\)", "", value)
    value = re.sub(r"\[.*?\]", "", value)
    # Release-group tags come in braces too: `... Perfect Timing (2017) [Hunter] {786zx}`
    # kept its `{786zx}` and became part of the artist name.
    value = re.sub(r"\{.*?\}", "", value)
    value = value.replace("\u2019", "'")
    return re.sub(r"\s+", " ", value).strip(" .-_,")


def clean_title(filename: str) -> str:
    """Turn a filename into a display title.

    The leading-number strips assume a number at the front is a track number. When the
    title *is* that number the assumption is wrong and there is nothing left to show -
    `Baby Keem - 16 (Official Audio)` cleaned to `()`, then to nothing. So the stripped
    number is remembered and handed back when the rest evaporates.
    """
    stem = UNICODE_DASH_RE.sub("-", Path(filename).stem)
    title = _clean_title_body(stem)
    if not title:
        # Retry without the track-number strips; a number is a better title than nothing.
        title = _clean_title_body(stem, strip_leading_number=False)
    return title


def _clean_title_body(title: str, strip_leading_number: bool = True) -> str:
    if strip_leading_number:
        # Strip billboard-style "YYYY-NNN " or "NNN-" prefixes
        title = re.sub(r"^\d{4}[-_]\d{2,3}\s+", "", title)
        title = re.sub(r"^\d{2,3}[-._]\s*", "", title)
        title = re.sub(r"^\d{1,2}\s*[-._)]\s*", "", title)
        title = re.sub(r"^\d{1,2}\s+", "", title)
    for p in NOISE_PATTERNS:
        title = re.sub(p, "", title, flags=re.IGNORECASE)
    title = re.sub(r"\bprod\.?\s+by\b.*$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\bproduced by\b.*$", "", title, flags=re.IGNORECASE)
    title = title.replace("_", " ")
    # Only strip leading "NN - rest" if rest doesn't start with a digit and has
    # no further " - " (avoids mangling "50 Cent - In Da Club")
    m = re.match(r"^(\d{1,2})\s*-\s*(.+)$", title)
    if m:
        first_char = m.group(2).strip()[:1] if m.group(2).strip() else ""
        if not first_char.isdigit():
            remainder = m.group(2).strip()
            if " - " not in remainder:
                title = remainder
    # Stripping a noise phrase out of a bracket leaves the bracket behind:
    # `PAPARAZZI (OFFICIAL MUSIC VIDEO)` became `PAPARAZZI ()`, and `Chivas (ft. G.w.M)
    # (Official Music Video)` became `Chivas (`. Clear the empty pairs, then any bracket
    # left unclosed at the end.
    title = re.sub(r"[(\[]\s*[)\]]", "", title)
    title = re.sub(r"\s*[(\[]\s*$", "", title)
    return re.sub(r"\s+", " ", title).strip(" .-_,")


def folder_artist(name: str) -> str:
    value = clean_artist_text(name)
    lower = value.lower()
    # Strip " - YouTube" suffix
    if lower.endswith(" - youtube"):
        value = value[:-len(" - YouTube")].strip(" -_,")
        lower = value.lower()
    for suffix in [
        " music videos", " videos", " greatest hits", " essentials",
        " discography", " playlist", " mix", " top songs", " full album list",
        " top tracks playlist", " best songs", " official music videos",
        " videoklippek", " video klippek", " hivatalos videoklipek",
        " válogatás", " zenék", " dalai", " hivatalos", " vevo",
        # `zap mama best of` became an artist of its own. The " - " rule below already
        # knows "best of" as an album word, but only when the folder has a dash in it.
        " best of", " best hits", " full album",
    ]:
        if lower.endswith(suffix):
            value = value[:-len(suffix)].strip(" -_,")
            lower = value.lower()
    # Strip video-platform markers anywhere in the name
    for marker in [r"\bwshh exclusive\b", r"\bofficial video\b",
                   r"\bofficial music video\b"]:
        value = re.sub(marker, "", value, flags=re.IGNORECASE).strip(" -_,")
    lower = value.lower()
    # Strip "Mix – " prefix (YouTube autoplay folders)
    if lower.startswith("mix \u2013 ") or lower.startswith("mix - "):
        value = value[6:].strip(" -_,")
        lower = value.lower()
    # Strip the "Legnépszerűbb számok -- " / "Top-Titel - " prefix YouTube puts on an
    # artist's auto-generated channel section. The separator varies by locale and by how the
    # folder got named; the plain hyphen was missing, so `Legnépszerűbb számok - K Trap`
    # and `Top-Titel - Naptengeri` kept the prefix and became artists of their own.
    if "legnépszerűbb" in lower or "top-titel" in lower:
        for _sep in (" -- ", " \u2013 ", " - "):
            if _sep in value:
                value = value.split(_sep, 1)[1].strip(" -_,")
                break
        lower = value.lower()
    value = re.sub(r"\s*@\s*\d{3}\b.*$", "", value).strip(" -_,")
    value = re.sub(r"\s*\(\d{4}(?:-\d{4})?\)\s*(?:\(\d+\))?.*$", "", value).strip(" -_,")
    value = re.sub(r"\s*\(\d{4}\)\s*(?:Mp3|mp3).*$", "", value).strip(" -_,")
    if " - " in value:
        left, right = value.split(" - ", 1)
        if left and any(t in right.lower() for t in [
            "album", "mixtape", "greatest", "hits", "vol", "mp3", "320",
            "best of", "discography", "complete", "the best", "collection",
            "a legjobb", "válogatás", "full", "edition",
        ]):
            value = left.strip()
    return value.strip(" -_,")


def split_artists(text: str) -> list[str]:
    parts = re.split(r"\s*[,&/×]\s*|\s+x\s+|\s+and\s+", text, flags=re.IGNORECASE)
    return [clean_artist_text(p) for p in parts if clean_artist_text(p)]


def extract_primary_and_features(credit: str) -> tuple[list[str], list[str]]:
    credit = clean_artist_text(credit)
    if not credit:
        return [], []
    m = FEAT_RE.search(credit)
    if m:
        primary = credit[:m.start()].strip(" -")
        featured = credit[m.end():].strip(" -")
        return split_artists(primary), split_artists(featured)
    return split_artists(credit), []


# ── Mapping parser ─────────────────────────────────────────────────────────────

def parse_mapping_block(lines: list[str]) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}
    for raw in lines:
        line = raw.strip()
        if not line.startswith("-"):
            continue
        line = line[1:].strip()
        if line.startswith("`") and line.endswith("`"):
            line = line[1:-1]
        if ":" not in line:
            continue
        left, right = line.split(":", 1)
        left = left.strip()
        values = [v.strip() for v in right.split(",") if v.strip()]
        if left:
            results[left] = values
    return results


def split_md_sections(text: str) -> dict[str, list[str]]:
    """Split a mappings markdown file into its `## ` sections, keyed by lowercased title."""
    from collections import defaultdict
    sections: dict[str, list[str]] = defaultdict(list)
    current = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            continue
        if current:
            sections[current].append(line)
    return sections


def load_mappings_file(path: Path) -> dict:
    """Parse a mappings markdown file in the shared (US) format.

    Sections, all optional: `## Alias normalization`, `## Groups`, `## Labels`,
    `## Group regions`, `## Person entries`. The first four are `- \\`key: a, b\\`` bullet
    lists; person entries are `### Name` blocks with `- field: value` lines.

    `region` on a person and the whole `## Group regions` section exist for areas whose
    region is curated rather than read off the folder tree - the Hungarian folders are
    sorted by artist, so there is no city in the path to derive it from. The US file has
    neither, and parses to exactly what it did before they existed.
    """
    text = path.read_text(encoding="utf-8")
    sections = split_md_sections(text)

    alias_map = parse_mapping_block(sections.get("alias normalization", []))
    groups = parse_mapping_block(sections.get("groups", []))
    labels = parse_mapping_block(sections.get("labels", []))
    group_regions = {k: v[0] for k, v in
                     parse_mapping_block(sections.get("group regions", [])).items() if v}
    group_labels = parse_mapping_block(sections.get("group labels", []))

    person_entries: dict[str, dict] = {}
    current_person = None
    for raw in sections.get("person entries", []):
        line = raw.strip()
        if line.startswith("### "):
            current_person = line[4:].strip()
            person_entries[current_person] = {
                "aliases": [], "groups": [], "labels": [], "region": "", "notes": ""}
            continue
        if not current_person or not line.startswith("-"):
            continue
        field, _, value = line[1:].partition(":")
        key = field.strip().lower()
        value = value.strip()
        if key in {"aliases", "groups", "labels"}:
            person_entries[current_person][key] = [
                item.strip() for item in value.split(",") if item.strip()]
        elif key in {"notes", "region"}:
            person_entries[current_person][key] = value

    alias_lookup: dict[str, str] = {}
    for canonical, aliases in alias_map.items():
        alias_lookup[normalize_key(canonical)] = canonical
        for alias in aliases:
            alias_lookup[normalize_key(alias)] = canonical

    # Two person entries can normalize to the same key - `Filo` (IFS, Szeged) and `FILO`
    # (_magyar trap) are different people whose names differ only in case, and
    # `normalize_key` lowercases. Registering both means the second silently wins, and every
    # group member or folder spelled the other way is reattributed to them: it credited the
    # IFS group's 19 songs to the trap FILO. An ambiguous key is therefore registered for
    # neither, so each name resolves to its own literal spelling. Same policy as
    # `squashed_lookup` - refusing to guess beats guessing wrong.
    from collections import Counter
    entry_keys = Counter(normalize_key(p) for p in person_entries)
    for person, info in person_entries.items():
        if entry_keys[normalize_key(person)] == 1:
            alias_lookup[normalize_key(person)] = person
        for alias in info.get("aliases", []):
            alias_lookup[normalize_key(alias)] = person

    canonical_groups: dict[str, list[str]] = {}
    for group_name, members in groups.items():
        canonical_group = alias_lookup.get(normalize_key(group_name), group_name)
        canonical_members = []
        for member in members:
            canonical_member = alias_lookup.get(normalize_key(member), member)
            if canonical_member not in canonical_members:
                canonical_members.append(canonical_member)
        canonical_groups[canonical_group] = canonical_members

    canonical_labels: dict[str, list[str]] = {}
    for label_name, artists in labels.items():
        canonical_artists = []
        for artist in artists:
            canonical_artist = alias_lookup.get(normalize_key(artist), artist)
            if canonical_artist not in canonical_artists:
                canonical_artists.append(canonical_artist)
        canonical_labels[label_name] = canonical_artists

    return {
        "alias_lookup": alias_lookup,
        "alias_lookup_squashed": squashed_lookup(alias_lookup),
        "groups": canonical_groups,
        "group_lookup": {normalize_key(g): g for g in canonical_groups},
        "labels": canonical_labels,
        "group_regions": {alias_lookup.get(normalize_key(g), g): r
                          for g, r in group_regions.items()},
        # Carried explicitly, never derived from the members' labels: `Nevenincs` is on
        # goldsoul but has no members listed, so deriving lost its label and its 13 songs,
        # while `Hősök` and `Gruppen Family` gained a Bloose Broavaz tag they never had
        # just because one member is signed there.
        "group_labels": {alias_lookup.get(normalize_key(g), g): ls
                         for g, ls in group_labels.items()},
        "person_entries": person_entries,
        #: keys shared by two or more Person entries, so unresolvable by name alone. An
        #: area that can tell them apart another way (which folder tree the file is in)
        #: uses this to know which names need that treatment.
        "ambiguous_person_keys": {k: sorted(p for p in person_entries
                                            if normalize_key(p) == k)
                                  for k, n in entry_keys.items() if n > 1},
    }


# ── Junk detection ─────────────────────────────────────────────────────────────

def is_junk_name(name: str, key: str, blocklist: set[str]) -> bool:
    if key in blocklist:
        return True
    if re.match(r"^\d+$", key):
        return True
    if re.match(r"^\d{1,3}\s+", key):
        return True
    if re.match(r"^\d{1,3}\.\s+", key):
        return True
    if re.match(r"^\d{4}\s*-\s*\d{2,3}\s+", key):
        return True
    if "(" in name and ")" not in name:
        return True
    if re.match(r"^\d{1,2}\s*-\s*", key):
        return True
    if len(key) <= 1:
        return True
    if any(ord(c) > 8000 for c in name):
        return True
    return False
