"""What the graph, timeline and dashboard builders share: where the collection is, which
top-level folders are not part of it, the "last rebuilt" stamp, and how to run a child script.

Each builder runs with its own directory as the working directory, so it puts this file's
folder on `sys.path` before importing it (`graph/common.py` and `timeline/*.py` do).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

#: The collection. Derived from the home directory, never a literal user name: the same
#: checkout runs on a second machine whose user is `abo`.
ZENE = Path.home() / "Desktop" / "zene"

#: Top-level folders that are not part of the collection. `_dupes_removed` is the holding pen
#: of a dedupe pass: anything left in it would be counted as music, and land in
#: `main_genre: other` because it matches no genre rule.
SKIP_ROOTS = {"new", "new good", "_music_scripts", "_playlists", "_dupes_removed"}


def last_rebuild(state_file: Path) -> float:
    """Unix time of the last finished rebuild, 0.0 if there never was one."""
    return float(state_file.read_text().strip()) if state_file.exists() else 0.0


def save_rebuild(state_file: Path, t: float) -> None:
    state_file.write_text(str(t))


def run_script(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run `python <args>` in `cwd` and capture its output as UTF-8.

    `encoding="utf-8"` is not optional: `text=True` alone decodes with the Windows locale
    codepage (cp1250 here), which cannot represent the accented artist names the builders
    print, and the UnicodeDecodeError lands in subprocess's reader thread mid-rebuild.
    """
    return subprocess.run([sys.executable, "-u"] + args, cwd=str(cwd), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
