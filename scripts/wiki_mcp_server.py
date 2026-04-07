#!/usr/bin/env python3
"""
Wiki MCP Server — exposes labs-wiki as searchable tools for all AI agents.

Provides three tools:
  - wiki_search: Full-text search across wiki pages
  - wiki_read:   Read a specific wiki page by name or path
  - wiki_list:   List all wiki pages from the index

Transport: stdio (works with VS Code Copilot, Copilot CLI, OpenCode)
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", Path(__file__).parent.parent))
WIKI_DIR = WIKI_ROOT / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

mcp = FastMCP("labs-wiki")


def _find_pages() -> list[Path]:
    """Return all .md files in wiki/ excluding index.md and log.md."""
    if not WIKI_DIR.exists():
        return []
    return sorted(
        p
        for p in WIKI_DIR.rglob("*.md")
        if p.name not in ("index.md", "log.md")
    )


def _extract_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter as a simple key-value dict."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _page_summary(path: Path) -> str:
    """Return a one-line summary: relative path, title, type."""
    text = path.read_text(errors="replace")
    fm = _extract_frontmatter(text)
    rel = path.relative_to(WIKI_ROOT)
    title = fm.get("title", path.stem.replace("-", " ").title())
    ptype = fm.get("type", "unknown")
    return f"{rel} — {title} ({ptype})"


@mcp.tool()
def wiki_list() -> str:
    """List all pages in the labs-wiki knowledge base.

    Returns a catalog of every wiki page with its path, title, and type.
    Use this to discover what knowledge is available before searching or reading.
    """
    pages = _find_pages()
    if not pages:
        return "No wiki pages found."

    lines = [f"# Labs-Wiki — {len(pages)} pages\n"]
    by_type: dict[str, list[str]] = {}
    for p in pages:
        text = p.read_text(errors="replace")
        fm = _extract_frontmatter(text)
        ptype = fm.get("type", "other")
        title = fm.get("title", p.stem.replace("-", " ").title())
        rel = str(p.relative_to(WIKI_ROOT))
        by_type.setdefault(ptype, []).append(f"- **{title}** — `{rel}`")

    for ptype in ["concept", "entity", "source", "synthesis", "other"]:
        items = by_type.get(ptype, [])
        if items:
            lines.append(f"\n## {ptype.title()}s ({len(items)})")
            lines.extend(sorted(items))

    return "\n".join(lines)


@mcp.tool()
def wiki_search(query: str) -> str:
    """Search labs-wiki pages for a topic or keyword.

    Performs case-insensitive full-text search across all wiki page titles,
    content, and frontmatter. Returns matching excerpts with context.

    Args:
        query: Search term or phrase (e.g., "attention mechanism", "transformer")
    """
    pages = _find_pages()
    if not pages:
        return "No wiki pages found."

    query_lower = query.lower()
    terms = query_lower.split()
    results: list[tuple[int, str]] = []

    for p in pages:
        text = p.read_text(errors="replace")
        text_lower = text.lower()

        # Score: title match (high), frontmatter match (medium), body match (low)
        score = 0
        fm = _extract_frontmatter(text)
        title = fm.get("title", "").lower()

        for term in terms:
            if term in title:
                score += 10
            if term in text_lower:
                score += 1
                score += text_lower.count(term)

        if score == 0:
            continue

        # Extract relevant excerpt
        rel = str(p.relative_to(WIKI_ROOT))
        page_title = fm.get("title", p.stem.replace("-", " ").title())
        ptype = fm.get("type", "unknown")

        # Find best matching paragraph
        paragraphs = text.split("\n\n")
        best_para = ""
        best_score = 0
        for para in paragraphs:
            if para.startswith("---"):
                continue
            para_score = sum(para.lower().count(t) for t in terms)
            if para_score > best_score:
                best_score = para_score
                best_para = para.strip()

        excerpt = best_para[:500] + ("..." if len(best_para) > 500 else "")
        entry = f"### {page_title} ({ptype})\n`{rel}`\n\n{excerpt}"
        results.append((score, entry))

    if not results:
        return f'No wiki pages match "{query}". Use wiki_list to see available pages.'

    results.sort(key=lambda x: -x[0])
    top = results[:10]

    header = f'# Search: "{query}" — {len(results)} match{"es" if len(results) != 1 else ""}\n'
    return header + "\n\n---\n\n".join(entry for _, entry in top)


@mcp.tool()
def wiki_read(page: str) -> str:
    """Read a specific wiki page by name or path.

    Args:
        page: Page name (e.g., "attention-mechanisms"), title (e.g., "Attention Mechanisms"),
              or relative path (e.g., "wiki/concepts/attention-mechanisms.md")
    """
    # Try direct path first
    candidates = [
        WIKI_ROOT / page,
        WIKI_DIR / page,
        WIKI_DIR / f"{page}.md",
    ]

    # Try slug matching across all subdirs
    slug = page.lower().replace(" ", "-").replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    for subdir in ["concepts", "entities", "sources", "synthesis"]:
        candidates.append(WIKI_DIR / subdir / f"{slug}.md")

    # Try title matching
    for p in _find_pages():
        text = p.read_text(errors="replace")
        fm = _extract_frontmatter(text)
        title = fm.get("title", "").lower()
        if title == page.lower() or p.stem == slug:
            candidates.insert(0, p)

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            rel = str(candidate.relative_to(WIKI_ROOT))
            content = candidate.read_text(errors="replace")
            return f"# {rel}\n\n{content}"

    # Fuzzy: search for partial matches
    matches = []
    for p in _find_pages():
        if slug in p.stem:
            matches.append(str(p.relative_to(WIKI_ROOT)))

    if matches:
        return f'Page "{page}" not found. Did you mean:\n' + "\n".join(
            f"- {m}" for m in matches
        )

    return f'Page "{page}" not found. Use wiki_list to see available pages.'


if __name__ == "__main__":
    mcp.run(transport="stdio")
