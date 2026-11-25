#!/usr/bin/env python3
"""Compile wiki/index.md from all wiki pages, clustered by page type."""

import argparse
from pathlib import Path

from wiki_links import wiki_markdown_pages
from wiki_schema import parse_page_text


def parse_frontmatter_simple(path: Path) -> dict | None:
    """Extract key frontmatter fields from a markdown file."""
    fm, body, error = parse_page_text(path.read_text())
    if error:
        return None
    first_para = body.split("\n\n")[0] if body else ""
    first_para = first_para.replace("#", "").strip()
    if len(first_para) > 120:
        first_para = first_para[:117] + "..."
    fm["_summary"] = first_para

    return fm


def compile_index(wiki_dir: str = ".") -> str:
    """Generate index.md content from all wiki pages."""
    root = Path(wiki_dir)
    wiki_path = root / "wiki"

    categories: dict[str, list[dict]] = {
        "concepts": [],
        "entities": [],
        "sources": [],
        "synthesis": [],
    }

    for category in categories:
        cat_dir = wiki_path / category
        if not cat_dir.exists():
            continue
        for page in wiki_markdown_pages(cat_dir):
            if page.name == "hot-snapshot.md":
                continue
            fm = parse_frontmatter_simple(page)
            if fm:
                categories[category].append({
                    "title": fm.get("title", page.stem.replace("-", " ").title()),
                    "summary": fm.get("_summary", ""),
                    "tier": fm.get("tier", ""),
                    "score": fm.get("quality_score", ""),
                })

    lines = [
        "# Wiki Index",
        "",
        "> Auto-generated catalog of all wiki pages. Do not edit manually.",
        "> Rebuild with `python3 scripts/compile_index.py`.",
        "",
    ]

    total = sum(len(v) for v in categories.values())
    if total == 0:
        lines.append("*No pages yet. Add a source to `raw/` for ingest.*")
        return "\n".join(lines) + "\n"

    section_names = {
        "concepts": "Concepts",
        "entities": "Entities",
        "sources": "Sources",
        "synthesis": "Synthesis",
    }

    for cat_key, cat_name in section_names.items():
        pages = categories[cat_key]
        if not pages:
            continue
        lines.append(f"## {cat_name}")
        lines.append("")
        for p in sorted(pages, key=lambda x: x["title"]):
            tier = f"T:{p['tier']}" if p["tier"] else ""
            score = f"score: {p['score']}" if p["score"] != "" else ""
            meta = ", ".join(filter(None, [tier, score]))
            meta_str = f" ({meta})" if meta else ""
            summary = f" — {p['summary']}" if p["summary"] else ""
            lines.append(f"- [[{p['title']}]]{summary}{meta_str}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile wiki index from pages")
    parser.add_argument(
        "--wiki-dir",
        default=".",
        help="Root directory of the wiki (default: current directory)",
    )
    args = parser.parse_args()

    content = compile_index(args.wiki_dir)

    index_path = Path(args.wiki_dir) / "wiki" / "index.md"
    index_path.write_text(content)

    page_count = content.count("- [[")
    print(f"✅ Rebuilt wiki/index.md with {page_count} entries")


if __name__ == "__main__":
    main()
