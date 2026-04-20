#!/usr/bin/env python3
"""Inject wiki pages into MemPalace as drawers in the labs_wiki_knowledge wing.

Reads wiki/concepts/, wiki/synthesis/, and wiki/entities/ pages and upserts
them into MemPalace's ChromaDB collection. Safe to re-run — uses upsert with
stable IDs derived from file paths and prunes orphaned drawers when pages are
deleted or renamed.

Usage:
    python3 scripts/wiki_to_mempalace.py [--dry-run] [--wing WING]
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"
PALACE_PATH = Path.home() / ".mempalace" / "palace"
COLLECTION_NAME = "mempalace_drawers"

INJECT_DIRS = ["concepts", "synthesis", "entities"]
DEFAULT_WING = "labs_wiki_knowledge"


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    result: dict = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def get_body(path: Path) -> str:
    """Extract body content after frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    return text[end + 3:].strip()


def stable_id(wing: str, filepath: Path) -> str:
    """Generate a stable drawer ID from wing + relative path."""
    rel = filepath.relative_to(WIKI_DIR)
    raw = f"{wing}:{rel}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def collect_pages() -> list[Path]:
    """Collect all wiki pages from target directories."""
    pages: list[Path] = []
    for subdir in INJECT_DIRS:
        d = WIKI_DIR / subdir
        if d.is_dir():
            pages.extend(sorted(d.glob("*.md")))
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description="Inject wiki pages into MemPalace")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be injected")
    parser.add_argument("--wing", default=DEFAULT_WING, help=f"Wing name (default: {DEFAULT_WING})")
    parser.add_argument("--palace", type=Path, default=PALACE_PATH, help="Palace path")
    args = parser.parse_args()

    pages = collect_pages()
    if not pages:
        print("No wiki pages found to inject.")
        return 0

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Wiki → MemPalace Injection")
    print(f"  Wing:   {args.wing}")
    print(f"  Palace: {args.palace}")
    print(f"  Pages:  {len(pages)}")
    print("-" * 50)

    # Import ChromaDB from mempalace's venv so dry-runs can still report the
    # orphan-cleanup delta without mutating the collection.
    sys.path.insert(0, str(Path.home() / ".local/share/pipx/venvs/mempalace/lib/python3.12/site-packages"))
    import chromadb
    client = chromadb.PersistentClient(path=str(args.palace))
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        collection = None if args.dry_run else client.create_collection(COLLECTION_NAME)

    stats: dict[str, int] = {}
    ids_batch: list[str] = []
    docs_batch: list[str] = []
    metas_batch: list[dict] = []
    desired_ids: set[str] = set()

    now = datetime.now(timezone.utc).isoformat()

    for page in pages:
        fm = parse_frontmatter(page)
        body = get_body(page)
        title = fm.get("title", page.stem.replace("-", " ").title())
        page_type = fm.get("type", "unknown")
        subdir = page.parent.name

        # Room = page type directory (concepts, synthesis, entities)
        room = subdir

        drawer_id = stable_id(args.wing, page)
        desired_ids.add(drawer_id)
        content = f"# {title}\n\n{body}"

        # Truncate to ~8000 chars for embedding efficiency
        if len(content) > 8000:
            content = content[:8000] + "\n\n[truncated]"

        metadata = {
            "wing": args.wing,
            "room": room,
            "source_file": str(page.relative_to(WIKI_ROOT)),
            "title": title[:200],
            "page_type": page_type,
            "injected_at": now,
            "agent": "wiki_to_mempalace",
        }

        stats[room] = stats.get(room, 0) + 1

        if args.dry_run:
            print(f"  [DRY RUN] {page.relative_to(WIKI_DIR)} → {args.wing}/{room}")
        else:
            ids_batch.append(drawer_id)
            docs_batch.append(content)
            metas_batch.append(metadata)

    deleted_orphans = 0

    # Batch upsert (ChromaDB handles batching internally up to ~41666)
    if not args.dry_run and ids_batch and collection is not None:
        # Upsert in chunks of 500 for safety
        chunk_size = 500
        for i in range(0, len(ids_batch), chunk_size):
            collection.upsert(
                ids=ids_batch[i:i + chunk_size],
                documents=docs_batch[i:i + chunk_size],
                metadatas=metas_batch[i:i + chunk_size],
            )

    if collection is not None:
        existing = collection.get(where={"wing": args.wing}, include=[])
        existing_ids = set(existing.get("ids", []))
        stale_ids = sorted(existing_ids - desired_ids)
        deleted_orphans = len(stale_ids)

        if stale_ids and not args.dry_run:
            chunk_size = 500
            for i in range(0, len(stale_ids), chunk_size):
                collection.delete(ids=stale_ids[i:i + chunk_size])

    print("-" * 50)
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Done. {len(pages)} pages processed.")
    print(f"  {'Would prune' if args.dry_run else 'Pruned'} orphaned drawers: {deleted_orphans}")
    print(f"\n  By room:")
    for room, count in sorted(stats.items()):
        print(f"    {room:<20} {count} pages")

    if not args.dry_run:
        print(f"\n  Verify: mempalace search 'your query' --wing {args.wing}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
