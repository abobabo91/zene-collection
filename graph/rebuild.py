"""Rebuild all graph areas, toplists, and visualization. Only rebuilds what changed.

    python rebuild.py              # rebuild the changed areas
    python rebuild.py --dry-run    # say what would rebuild, touch nothing

**This is a builder, not an entry point.** It writes files and returns an exit code; it does
not touch git. Run `../rebuild.py` to rebuild the graph, timeline and dashboard together and
commit them as one change - they are one repo and one logical unit.

The argument parsing matters: the script used to ignore argv entirely, so
`python rebuild.py --help` - the obvious way to find out what it does - ran a full rebuild
and pushed to GitHub instead of printing usage.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from common import AUDIO_EXTS, DATA_ROOT, PROJECT_ROOT, ZENE

STATE_FILE = PROJECT_ROOT / ".last_rebuild"

SCAN_ROOTS = {
    "us": [ZENE / "_rap", ZENE / "_trap"],
    # Added 2026-08-11. Hungarian had no scanner at all: its normalized JSONs were curated
    # by hand, so every re-sort of the folders left the graph pointing at paths that no
    # longer existed and blind to anything new, with nothing reporting it.
    # `build_hungarian_graph.py` is incremental rather than from-scratch because
    # groups.json and labels.json reference songs by song_id.
    "hungarian": [ZENE / "_magyar rap", ZENE / "_magyar trap"],
    "rnb": [ZENE / "_other" / "_rnb"],
    "rock": [ZENE / "_other" / "_rock"],
    "magyar": [ZENE / "_other" / "_magyar"],
    "elektro": [ZENE / "_other" / "_elektro"],
    "pop": [ZENE / "_other" / "_pop"],
    "alternate": [ZENE / "_other" / "_alternate"],
    "latino": [ZENE / "_other" / "_latino"],
    # Added 2026-08-03. Missing from this list meant missing from the graph entirely -
    # 653 files, whole genres, never scanned rather than badly attributed. A folder that
    # is not here is invisible, and nothing reports it.
    "african": [ZENE / "_other" / "_african music"],
    "roman": [ZENE / "_other" / "_roman"],
    "reggae": [ZENE / "_other" / "_reggea"],
    "russian": [ZENE / "_other" / "_russian"],
    "countryjazz": [ZENE / "_other" / "_country_jazz"],
    "vilagzene": [ZENE / "_other" / "_vilagzene"],
    "mantra": [ZENE / "_other" / "_mantra"],
    "classical": [ZENE / "_other" / "_classical"],
    # Excluded from the US graph on purpose (it is the US graph), but they still need an
    # owner - non-US rap and trap, 472 files.
    "intlrap": [ZENE / "_rap" / "_other"],
    "intltrap": [ZENE / "_trap" / "_other country random"],
}


def get_last_rebuild() -> float:
    if STATE_FILE.exists():
        return float(STATE_FILE.read_text().strip())
    return 0.0


def save_rebuild_time(t: float):
    STATE_FILE.write_text(str(t))


def has_changes(roots: list[Path], since: float, area: str) -> bool:
    # Check for new/modified files
    for root in roots:
        if not root.exists():
            continue
        for dirpath, _, files in os.walk(root):
            for f in files:
                if Path(f).suffix.lower() in AUDIO_EXTS:
                    full = Path(dirpath) / f
                    try:
                        if full.stat().st_mtime > since:
                            return True
                    except OSError:
                        continue
    # Check for moved/deleted files (paths in songs.json that no longer exist on disk)
    songs_path = DATA_ROOT / area / "normalized" / "songs.json"
    if songs_path.exists():
        songs = json.loads(songs_path.read_text(encoding="utf-8"))
        for s in songs:
            if not (ZENE / s["file"]).exists():
                return True  # a file was moved or deleted
    return False


def run(cmd: list[str], desc: str):
    """Always decode as UTF-8. `text=True` alone decodes with the Windows locale codepage,
    cp1250 here, which cannot represent what the builders print - artist names carry Hungarian
    and Spanish accents. That raised UnicodeDecodeError inside subprocess's reader thread and
    aborted the whole rebuild partway through `magyar` on 2026-08-12."""
    print(f"  {desc}...")
    r = subprocess.run([sys.executable] + cmd, cwd=str(PROJECT_ROOT), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"    ERROR: {(r.stderr or '')[:300]}")
        return False
    first = r.stdout.strip().split("\n")[0] if (r.stdout or "").strip() else "done"
    print(f"    {first}")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    # --no-push is accepted and ignored: this is a pure builder now, git lives in the root
    # rebuild.py. Kept so older invocations and notes do not fail on an unknown flag.
    ap.add_argument("--no-push", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--dry-run", action="store_true",
                    help="report which areas changed and exit")
    args = ap.parse_args()

    last = get_last_rebuild()
    import time
    now = time.time()

    if last > 0:
        from datetime import datetime
        print(f"Last rebuild: {datetime.fromtimestamp(last).strftime('%Y-%m-%d %H:%M')}")
    else:
        print("First run — rebuilding everything.")

    changed = []
    for area, roots in SCAN_ROOTS.items():
        if last == 0 or has_changes(roots, last, area):
            changed.append(area)

    if not changed:
        print("No changes detected. Nothing to rebuild.")
        return

    print(f"Changes detected in: {', '.join(changed)}")
    if args.dry_run:
        print("(dry run - nothing rebuilt, nothing committed)")
        return

    # Rebuild changed areas
    failed = []
    for area in changed:
        if area == "us":
            ok = run(["build_us_graph.py"], "US rap/trap")
        elif area == "hungarian":
            ok = run(["build_hungarian_graph.py"], "Hungarian rap/trap")
        else:
            ok = run(["build_other_graph.py", area], f"{area}")
        if not ok:
            failed.append(area)

    # Always rebuild toplists + visualization if anything changed
    for script, label in (("build_toplists.py", "Toplists"),
                          ("build_visualization.py", "Visualization")):
        if not run([script], label):
            failed.append(label.lower())

    # A partial rebuild must not look like a finished one. Saving the timestamp would tell
    # the next run those areas are current, so a build that died halfway would never be
    # retried, and the dashboard would publish a graph that is half old and half new.
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        print("Not saving the rebuild timestamp - rerun after fixing, so the failed areas "
              "are picked up again.")
        return 1

    save_rebuild_time(now)
    print(f"\nrebuilt: {', '.join(changed)}")
    return 0


if __name__ == "__main__":
    # Propagate the exit code: the root rebuild.py stops the pipeline on it, and refresh.py
    # in the youtube repo stops before the playlists. A failed rebuild that returns 0 is how
    # a half-built graph reaches everything downstream.
    raise SystemExit(main() or 0)
