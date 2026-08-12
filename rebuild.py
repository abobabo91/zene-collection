"""Rebuild everything the collection feeds, in the order the pieces depend on each other.

    python rebuild.py                # graph, timeline, dashboard, then one commit + push
    python rebuild.py --no-push      # same, but leave the push to the caller
    python rebuild.py --dry-run      # say what would rebuild, write nothing
    python rebuild.py --only graph   # one stage (graph | timeline | dashboard)

## Why this exists

The three used to be separate repos with a `rebuild.py` each. They were never independent:
`dashboard/build.py` reads the other two's output straight off disk, and every collection
change needs all three rebuilt in this order. Two consequences made the split actively
expensive - one logical change took three commits and three pushes, and the two rebuild
scripts drifted into near-copies of one another. The same two bugs had to be found and
fixed twice on 2026-08-12: output decoded with the Windows locale codepage instead of
UTF-8, which died on accented artist names, and an unconditional `git push` that fired as a
side effect of any run.

So the stages are now plain builders that write files and return an exit code, and **this
script is the only thing that touches git.**

## Order

1. `graph/rebuild.py`      scans the collection, rebuilds changed areas, toplists, index.html
2. `timeline/rebuild.py`   rebuilds the genre catalog and the mp3 CSV
3. `dashboard/build.py`    copies both outputs together and injects the shared nav

A stage that fails stops the run: the dashboard would otherwise publish a graph that is
half old and half new, and the timestamp files would record a build that did not happen.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

#: (name, working dir, command). Order matters - see the module docstring.
STAGES = [
    ("graph", HERE / "graph", ["rebuild.py"]),
    ("timeline", HERE / "timeline", ["rebuild.py"]),
    ("dashboard", HERE / "dashboard", ["build.py"]),
]


def run(name: str, cwd: Path, cmd: list[str], dry: bool) -> bool:
    """`encoding="utf-8"` is not optional: `text=True` alone decodes with the Windows locale
    codepage (cp1250 here), which cannot represent the accented artist names the builders
    print, and the UnicodeDecodeError lands in subprocess's reader thread mid-rebuild."""
    argv = [sys.executable, "-u"] + cmd + (["--dry-run"] if dry else [])
    t0 = time.time()
    proc = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    lines = [l.rstrip() for l in (proc.stdout or "").splitlines() if l.strip()]
    ok = proc.returncode == 0
    print(f"  [{'OK ' if ok else 'FAIL'}] {name:<10} {time.time() - t0:6.1f}s  "
          f"{lines[-1][:88] if lines else ''}", flush=True)
    if not ok:
        for line in (lines[-8:] or []):
            print(f"          {line[:110]}", flush=True)
        for line in (proc.stderr or "").strip().splitlines()[-8:]:
            print(f"          {line[:110]}", flush=True)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-push", action="store_true", help="commit but do not push")
    ap.add_argument("--dry-run", action="store_true", help="write nothing, commit nothing")
    ap.add_argument("--only", choices=[s[0] for s in STAGES], help="run a single stage")
    a = ap.parse_args()

    stages = [s for s in STAGES if not a.only or s[0] == a.only]
    print(f"rebuilding: {', '.join(s[0] for s in stages)}"
          + ("   (dry run)" if a.dry_run else ""))

    for name, cwd, cmd in stages:
        if not run(name, cwd, cmd, a.dry_run):
            print(f"\nstopping at '{name}'. Nothing is committed, and the stage's own "
                  f"timestamp file is untouched, so a rerun picks it up again.")
            return 1

    if a.dry_run:
        print("\ndry run - nothing written, nothing committed")
        return 0

    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(HERE),
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not (status.stdout or "").strip():
        print("\nno data changes to commit")
        return 0

    changed = len((status.stdout or "").strip().splitlines())
    subprocess.run(["git", "add", "-A"], cwd=str(HERE))
    subprocess.run(["git", "commit", "-m", f"Rebuild: {', '.join(s[0] for s in stages)}"],
                   cwd=str(HERE), capture_output=True)
    print(f"\ncommitted {changed} changed file(s)")
    if a.no_push:
        print("--no-push: the caller owns the push")
    else:
        push = subprocess.run(["git", "push"], cwd=str(HERE), capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        print("pushed to GitHub" if push.returncode == 0
              else f"push FAILED: {(push.stderr or '')[:200]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
