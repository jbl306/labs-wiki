#!/usr/bin/env python3
"""Lint wiki pages for health issues: broken links, orphans, staleness, quality."""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = ["title", "type", "created", "sources"]
VALID_TYPES = {"source", "concept", "entity", "synthesis"}
TYPE_DIR_MAP = {
    "source": "sources",
    "concept": "concepts",
    "entity": "entities",
    "synthesis": "synthesis",
}
STALENESS_DAYS = 90
QUALITY_THRESHOLD = 50


def parse_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = path.read_text()
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    fm: dict = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-") and not line.startswith("#"):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")

    if "sources" not in fm:
        for line in parts[1].strip().split("\n"):
            if line.strip() == "sources:":
                fm["sources"] = "present"

    return fm


def find_wikilinks(path: Path) -> list[str]:
    """Extract all [[wikilink]] targets from a file."""
    content = path.read_text()
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def compute_quality_score(
    fm: dict,
    has_wikilinks: bool,
    has_related: bool,
    staleness_ok: bool,
) -> int:
    """Compute 0-100 quality score for a page."""
    score = 0

    required_present = sum(1 for f in REQUIRED_FIELDS if f in fm)
    score += int(25 * required_present / len(REQUIRED_FIELDS))

    if has_wikilinks or has_related:
        score += 25
    elif has_wikilinks or has_related:
        score += 12

    if fm.get("sources") and fm["sources"] != "":
        score += 25

    if staleness_ok:
        score += 25
    elif fm.get("last_verified"):
        score += 12

    return score


def lint_wiki(wiki_dir: str = ".") -> tuple[list[str], list[str], dict[str, int]]:
    """Lint all wiki pages. Returns (errors, warnings, scores)."""
    root = Path(wiki_dir)
    wiki_path = root / "wiki"
    errors: list[str] = []
    warnings: list[str] = []
    scores: dict[str, int] = {}

    if not wiki_path.exists():
        errors.append("wiki/ directory does not exist")
        return errors, warnings, scores

    pages = list(wiki_path.rglob("*.md"))
    pages = [p for p in pages if p.name not in ("index.md", "log.md")]

    if not pages:
        return errors, warnings, scores

    page_titles: set[str] = set()
    for p in pages:
        fm = parse_frontmatter(p)
        if fm and "title" in fm:
            page_titles.add(fm["title"])

    index_path = wiki_path / "index.md"
    index_content = index_path.read_text() if index_path.exists() else ""

    now = datetime.now(timezone.utc)

    for page in pages:
        rel = page.relative_to(root)
        fm = parse_frontmatter(page)

        if fm is None:
            errors.append(f"{rel}: no valid frontmatter found")
            continue

        for field in REQUIRED_FIELDS:
            if field not in fm:
                errors.append(f"{rel}: missing required field '{field}'")

        page_type = fm.get("type", "")
        if page_type and page_type not in VALID_TYPES:
            errors.append(f"{rel}: invalid type '{page_type}' (must be: {', '.join(VALID_TYPES)})")

        if page_type in TYPE_DIR_MAP:
            expected_dir = TYPE_DIR_MAP[page_type]
            if expected_dir not in str(rel):
                errors.append(f"{rel}: type '{page_type}' should be in wiki/{expected_dir}/")

        wikilinks = find_wikilinks(page)
        for link in wikilinks:
            if link not in page_titles:
                errors.append(f"{rel}: broken wikilink [[{link}]]")

        title = fm.get("title", "")
        if title and title not in index_content and str(rel) not in index_content:
            warnings.append(f"{rel}: orphan page (not found in index.md)")

        staleness_ok = True
        last_verified = fm.get("last_verified", "")
        if last_verified:
            try:
                verified_date = datetime.strptime(last_verified, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                days_old = (now - verified_date).days
                if days_old > STALENESS_DAYS:
                    warnings.append(f"{rel}: stale (last verified {days_old} days ago)")
                    staleness_ok = False
            except ValueError:
                pass

        has_related = "related" in fm
        has_wikilinks = len(wikilinks) > 0
        score = compute_quality_score(fm, has_wikilinks, has_related, staleness_ok)
        scores[str(rel)] = score

        if score < QUALITY_THRESHOLD:
            warnings.append(f"{rel}: quality score {score} (below {QUALITY_THRESHOLD} threshold)")

    return errors, warnings, scores


# ---------------------------------------------------------------------------
# Contradiction detection (claude-obsidian pattern, Phase B P1)
# ---------------------------------------------------------------------------

# Obsidian-style callout block: `> [!contradiction] optional title`
_CONTRADICTION_CALLOUT = re.compile(
    r"^>\s*\[!contradiction\](.*?)$", re.IGNORECASE | re.MULTILINE
)


def find_contradictions(wiki_dir: str = ".") -> list[tuple[str, int, str]]:
    """Return [(relpath, line_number, callout_title), ...] for every
    `> [!contradiction]` callout found in the wiki.

    These are authored by `auto_ingest.py` (and can be added by hand) when
    a newly-ingested source conflicts with an existing page. The lint
    surfaces them so the user can adjudicate and clean up the wiki.
    """
    root = Path(wiki_dir)
    wiki_path = root / "wiki"
    results: list[tuple[str, int, str]] = []
    if not wiki_path.exists():
        return results

    for page in wiki_path.rglob("*.md"):
        if page.name in {"hot.md"}:
            continue
        try:
            text = page.read_text(errors="ignore")
        except OSError:
            continue
        if "[!contradiction]" not in text.lower():
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            m = _CONTRADICTION_CALLOUT.match(line)
            if m:
                title = m.group(1).strip() or "(untitled)"
                rel = str(page.relative_to(root))
                results.append((rel, lineno, title))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint labs-wiki pages")
    parser.add_argument(
        "--wiki-dir",
        default=".",
        help="Root directory of the wiki (default: current directory)",
    )
    parser.add_argument(
        "--contradictions-only",
        action="store_true",
        help="Only scan for [!contradiction] callouts and print them",
    )
    args = parser.parse_args()

    if args.contradictions_only:
        hits = find_contradictions(args.wiki_dir)
        print(f"=== Contradictions ({len(hits)}) ===")
        for rel, lineno, title in hits:
            print(f"  🔻 {rel}:{lineno} — {title}")
        sys.exit(0 if not hits else 2)

    errors, warnings, scores = lint_wiki(args.wiki_dir)
    contradictions = find_contradictions(args.wiki_dir)

    print("=== Wiki Lint Report ===")
    page_count = len(scores) + (1 if any("no valid frontmatter" in e for e in errors) else 0)
    print(f"Pages scanned: {max(page_count, len(scores))}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Contradictions: {len(contradictions)}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  ❌ {e}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠️  {w}")

    if contradictions:
        print("\nCONTRADICTIONS:")
        for rel, lineno, title in contradictions:
            print(f"  🔻 {rel}:{lineno} — {title}")

    if scores:
        print("\nSCORES:")
        for path, score in sorted(scores.items()):
            print(f"  {path}: {score}/100")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
