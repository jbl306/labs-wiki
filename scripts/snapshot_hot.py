#!/usr/bin/env python3
"""
snapshot_hot.py — Copy the ephemeral wiki/hot.md to wiki/meta/hot-snapshot.md.

Per proposed-answer Part 5 Q2 of the claude-obsidian integration plan:
`wiki/hot.md` is gitignored (rewritten frequently); an externally scheduled
snapshot can still be committed so git history preserves the evolution of
"what was hot" without the hourly churn.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "wiki" / "hot.md"
DST = REPO / "wiki" / "meta" / "hot-snapshot.md"


def main() -> int:
    if not SRC.exists():
        print(f"source missing: {SRC}", file=sys.stderr)
        return 1
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    # Prepend a notice so readers don't confuse the snapshot with the live cache.
    content = DST.read_text()
    banner = (
        "<!-- Auto-generated snapshot of wiki/hot.md. "
        "The live cache is gitignored; this file is its committed history. -->\n\n"
    )
    if not content.startswith("<!-- Auto-generated"):
        DST.write_text(banner + content)
    print(f"snapshot → {DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
