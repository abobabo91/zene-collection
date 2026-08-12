"""Rebuild genre catalog and mp3 timeline. Only rebuilds if files changed since last run.

    python rebuild.py              # rebuild, then commit and push
    python rebuild.py --no-push    # rebuild and commit, leave pushing to the caller

`--no-push` is for callers that own the push, so a push never happens as an unapproved side
effect of a rebuild step.
"""
import argparse
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
ZENE = Path(r"C:\Users\abele\Desktop\zene")
STATE_FILE = HERE / ".last_rebuild"
SKIP = {"new", "new good", "_music_scripts", "_playlists", "_dupes_removed"}


def get_last_rebuild() -> float:
    if STATE_FILE.exists():
        return float(STATE_FILE.read_text().strip())
    return 0.0


def has_changes(since: float) -> bool:
    import json
    catalog_path = HERE / "genre_catalog.json"
    cataloged = set()
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        cataloged = {entry["file"] for entry in catalog}
        # Cataloged file moved/deleted from disk → rebuild
        for f in cataloged:
            if not (ZENE / f).exists():
                return True

    for dirpath, dirs, files in os.walk(ZENE):
        rel = Path(dirpath).relative_to(ZENE)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        for f in files:
            if not f.lower().endswith(".mp3"):
                continue
            full = Path(dirpath) / f
            try:
                if full.stat().st_mtime > since:
                    return True
            except OSError:
                continue
            # On-disk mp3 missing from catalog (moved in with old mtime) → rebuild
            rel_str = str(full.relative_to(ZENE))
            if cataloged and rel_str not in cataloged:
                return True
    return False


def rebuild_catalog():
    """`encoding="utf-8"` is required: `text=True` alone decodes with the Windows locale
    codepage (cp1250), which cannot represent the accented artist names the catalog prints,
    and the resulting UnicodeDecodeError aborts the rebuild partway."""
    print("  Rebuilding genre catalog...")
    r = subprocess.run([sys.executable, "build_catalog.py"], cwd=str(HERE), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"    ERROR: {(r.stderr or '')[:300]}")
        return False
    first = r.stdout.strip().split("\n")[0] if (r.stdout or "").strip() else "done"
    print(f"    {first}")
    return True


def rebuild_csv():
    print("  Rebuilding mp3_sorted_filtered.csv...")
    # The exclusion list is derived from SKIP rather than repeated. It used to be spelled
    # out here and had already drifted - `_playlists` was excluded from the catalog but
    # counted in the CSV, so the two views of the same collection disagreed.
    clauses = " -and ".join(
        f"$_.FullName -notlike '{ZENE}\\{name}\\*'" for name in sorted(SKIP)
    )
    # `-File` matters: `_magyar rap/el bago/ultimohombre/ultimohombre.mp3` is a directory
    # whose name ends in .mp3, so `-Filter *.mp3` alone returns it as if it were a track.
    ps_cmd = (
        f"Get-ChildItem -Path '{ZENE}' -Filter *.mp3 -Recurse -File | "
        f"Where-Object {{ {clauses} }} | "
        "Sort-Object LastWriteTime -Descending | "
        "Select-Object FullName, @{Name='LastWriteTime';Expression={$_.LastWriteTime.ToString('yyyy. MM. dd. H:mm:ss')}} | "
        "Export-Csv -Path '" + str(HERE / "mp3_sorted_filtered_raw.csv") + "' -NoTypeInformation -Encoding UTF8"
    )
    subprocess.run(["powershell.exe", "-Command", ps_cmd], capture_output=True)

    # Clean BOM and normalize quoting
    raw = HERE / "mp3_sorted_filtered_raw.csv"
    out = HERE / "mp3_sorted_filtered.csv"
    if raw.exists():
        text = raw.read_text(encoding="utf-8-sig")
        lines = text.strip().split("\n")
        reader = csv.reader(lines)
        rows = list(reader)
        with open(out, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                writer.writerow(row)
        raw.unlink()
        print(f"    {len(rows)-1} entries")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-push", action="store_true",
                    help="commit but do not push; for callers that own the push")
    args = ap.parse_args()

    last = get_last_rebuild()
    now = time.time()

    if last > 0:
        from datetime import datetime
        print(f"Last rebuild: {datetime.fromtimestamp(last).strftime('%Y-%m-%d %H:%M')}")
    else:
        print("First run — rebuilding everything.")

    if last > 0 and not has_changes(last):
        print("No new mp3s since last rebuild. Nothing to do.")
        return 0

    print("Changes detected. Rebuilding...")
    if not rebuild_catalog():
        # Not saving the timestamp: a failed catalog must be retried, and the CSV built
        # beside it would describe a collection the catalog does not.
        print("\nFAILED: the catalog did not build. Not saving the timestamp, not committing.")
        return 1
    rebuild_csv()

    STATE_FILE.write_text(str(now))

    # Git commit + push
    r = subprocess.run(["git", "status", "--porcelain"], cwd=str(HERE), capture_output=True, text=True)
    if r.stdout.strip():
        subprocess.run(["git", "add", "-A"], cwd=str(HERE))
        subprocess.run(["git", "commit", "-m", "Rebuild: new music added"], cwd=str(HERE))
        if args.no_push:
            print("\nCommitted. --no-push: the caller owns the push.")
        else:
            subprocess.run(["git", "push"], cwd=str(HERE))
            print("Pushed to GitHub Pages.")
    else:
        print("\nNo data changes to commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
