#!/usr/bin/env python3
"""Normalize wikilinks across the existing wiki corpus.

This applies the same post-processing used for newly created pages to the
legacy wiki so broken wikilinks and invalid related: entries are cleaned up
consistently.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from auto_ingest import postprocess_created_pages

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path, default=ROOT / "wiki")
    args = parser.parse_args()

    wiki_dir = args.wiki_dir.resolve()
    if not wiki_dir.is_dir():
        raise SystemExit(f"wiki dir not found: {wiki_dir}")

    pages: list[str] = []
    for category in ("sources", "concepts", "entities", "synthesis"):
        cat_dir = wiki_dir / category
        if not cat_dir.exists():
            continue
        for page in sorted(cat_dir.glob("*.md")):
            if page.name in {"index.md", "hot.md", "log.md", ".gitkeep"}:
                continue
            pages.append(str(page.relative_to(ROOT)))

    postprocess_created_pages(wiki_dir, pages, ROOT)
    print(f"Normalized wikilinks on {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
