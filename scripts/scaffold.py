#!/usr/bin/env python3
"""Scaffold the labs-wiki directory structure and seed initial files."""

import argparse
import sys
from pathlib import Path

REQUIRED_DIRS = [
    "raw",
    "raw/assets",
    "wiki/sources",
    "wiki/concepts",
    "wiki/entities",
    "wiki/synthesis",
    "agents",
    "templates",
    "scripts",
    "docs",
    ".github/skills",
    ".github/hooks",
]

INDEX_SEED = """# Wiki Index

> Auto-generated catalog of all wiki pages. Do not edit manually.
> Rebuilt by `/wiki-ingest`, `/wiki-update`, and `/wiki-orchestrate`.

*No pages yet. Run `/wiki-ingest` to process sources from `raw/`.*
"""

LOG_SEED = """# Wiki Audit Log

> Structured log of all wiki operations. Each entry is a YAML block.
> Appended by `/wiki-ingest`, `/wiki-update`, `/wiki-lint`, `/wiki-orchestrate`.

"""


def scaffold(wiki_dir: str = ".") -> dict[str, list[str]]:
    """Create missing directories and seed files. Returns actions taken."""
    root = Path(wiki_dir)
    actions: dict[str, list[str]] = {"created_dirs": [], "created_files": [], "skipped": []}

    for d in REQUIRED_DIRS:
        path = root / d
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            actions["created_dirs"].append(str(d))
            gitkeep = path / ".gitkeep"
            if not any(path.iterdir()):
                gitkeep.touch()
        else:
            actions["skipped"].append(f"dir: {d}")

    index_path = root / "wiki" / "index.md"
    if not index_path.exists():
        index_path.write_text(INDEX_SEED)
        actions["created_files"].append("wiki/index.md")
    else:
        actions["skipped"].append("wiki/index.md")

    log_path = root / "wiki" / "log.md"
    if not log_path.exists():
        log_path.write_text(LOG_SEED)
        actions["created_files"].append("wiki/log.md")
    else:
        actions["skipped"].append("wiki/log.md")

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold labs-wiki structure")
    parser.add_argument(
        "--wiki-dir",
        default=".",
        help="Root directory of the wiki (default: current directory)",
    )
    args = parser.parse_args()

    actions = scaffold(args.wiki_dir)

    print("=== labs-wiki scaffold ===")
    if actions["created_dirs"]:
        print(f"\nCreated {len(actions['created_dirs'])} directories:")
        for d in actions["created_dirs"]:
            print(f"  📁 {d}")

    if actions["created_files"]:
        print(f"\nCreated {len(actions['created_files'])} files:")
        for f in actions["created_files"]:
            print(f"  📄 {f}")

    if not actions["created_dirs"] and not actions["created_files"]:
        print("\n✅ All directories and files already exist. Nothing to do.")

    sys.exit(0)


if __name__ == "__main__":
    main()
