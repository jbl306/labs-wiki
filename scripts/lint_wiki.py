#!/usr/bin/env python3
"""Lint wiki pages for health issues: broken links, orphans, staleness, quality."""

import argparse
import re
import sys
from collections import Counter
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

# R3: rubric tunables — kept module-level so they can be adjusted in one place.
INBOUND_SATURATION = 5
OUTBOUND_SATURATION = 5
SOURCES_SATURATION = 3
WORDCOUNT_BAND = (300, 4000)
STALENESS_FULL_DAYS = 30
STALENESS_ZERO_DAYS = 180

KNOWLEDGE_STATE_POINTS = {
    "validated": 10,
    "executed": 6,
    "planned": 3,
}
KNOWLEDGE_STATE_NEUTRAL = 5  # awarded when the field is absent

# Regex hits that count as a "specific claim": numeric tokens, fenced code,
# block-quoted lines.
_NUM_RE = re.compile(r"\b\d[\d,\.]*\b")
_CODE_FENCE_RE = re.compile(r"^```", re.MULTILINE)
_BLOCKQUOTE_RE = re.compile(r"^>", re.MULTILINE)


def slugify_wikilink(text: str) -> str:
    """Normalize a wikilink target similarly to the graph builder."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


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


def parse_frontmatter_full(path: Path) -> tuple[dict, str, str]:
    """Return (frontmatter_dict, frontmatter_text, body) for a markdown file.

    Used by --write-scores to round-trip the file without losing keys.
    """
    content = path.read_text()
    if not content.startswith("---"):
        return {}, "", content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, "", content
    fm: dict = {}
    for line in parts[1].strip().split("\n"):
        s = line.strip()
        if ":" in s and not s.startswith("-") and not s.startswith("#"):
            key, _, value = s.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, parts[1], parts[2]


def _count_sources(fm: dict, body: str) -> int:
    """Count source entries — frontmatter list lines starting with `- `."""
    # We cannot count list items from the simplified `parse_frontmatter` above
    # (it overwrites with "present"), so re-parse from the file body context
    # supplied by the caller. Since the simplified fm collapses lists, callers
    # that need exact counts should pass `body` plus a re-parse from the file.
    # Default behavior here: any non-empty `sources` value counts as 1.
    val = fm.get("sources", "")
    if not val:
        return 0
    if val == "present":
        return 1
    return 1


def count_sources_from_text(fm_text: str) -> int:
    """Count `- ` entries in the `sources:` block of raw frontmatter text."""
    if not fm_text:
        return 0
    in_block = False
    count = 0
    for raw in fm_text.strip().split("\n"):
        s = raw.strip()
        if s.startswith("sources:"):
            in_block = True
            tail = s.split(":", 1)[1].strip()
            if tail.startswith("[") and tail.endswith("]"):
                inner = tail[1:-1].strip()
                return 0 if not inner else len([x for x in inner.split(",") if x.strip()])
            continue
        if in_block:
            if s.startswith("- "):
                count += 1
                continue
            if not s or s.startswith("#"):
                continue
            # Hit the next key
            break
    return count


def _wordcount_score(words: int, max_pts: int) -> float:
    lo, hi = WORDCOUNT_BAND
    if words <= 0:
        return 0.0
    if lo <= words <= hi:
        return float(max_pts)
    if words < lo:
        # linear ramp 0 → max_pts as 0 → lo
        return max_pts * (words / lo)
    # words > hi: linear decay; zero credit at 2*hi
    overshoot = min(words - hi, hi)
    return max_pts * (1.0 - overshoot / hi)


def _staleness_score(last_verified: str, now: datetime, max_pts: int) -> float:
    if not last_verified:
        return 0.0
    try:
        d = datetime.strptime(last_verified, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return 0.0
    days = (now - d).days
    if days <= STALENESS_FULL_DAYS:
        return float(max_pts)
    if days >= STALENESS_ZERO_DAYS:
        return 0.0
    span = STALENESS_ZERO_DAYS - STALENESS_FULL_DAYS
    return max_pts * (1.0 - (days - STALENESS_FULL_DAYS) / span)


def has_specific_claim(body: str) -> bool:
    """True if the body has any numeric token, code fence, or block quote."""
    if not body:
        return False
    if _CODE_FENCE_RE.search(body):
        return True
    if _BLOCKQUOTE_RE.search(body):
        return True
    if _NUM_RE.search(body):
        return True
    return False


def compute_quality_score(
    fm: dict,
    body: str,
    wikilinks_out: int,
    wikilinks_in: int,
    has_claim: bool,
    now: datetime,
    sources_count: int | None = None,
) -> int:
    """Pure quality score (0–100). New rubric (R3).

    Signal contributions (max 100):
      - inbound wikilinks   (saturates at 5)        20
      - outbound wikilinks  (saturates at 5)        15
      - body word count in 300–4000 band            15 (linear ramp/decay)
      - sources count       (saturates at 3)        15
      - staleness curve     (full ≤30d → 0 ≥180d)   15
      - knowledge_state     (validated/executed/…)  10
      - has specific claim  (numbers/code/quote)    10
    """
    score = 0.0

    # 1. Inbound wikilinks (graph degree from the corpus)
    score += 20.0 * min(wikilinks_in, INBOUND_SATURATION) / INBOUND_SATURATION

    # 2. Outbound wikilinks
    score += 15.0 * min(wikilinks_out, OUTBOUND_SATURATION) / OUTBOUND_SATURATION

    # 3. Body word count in band
    words = len((body or "").split())
    score += _wordcount_score(words, max_pts=15)

    # 4. Sources list length
    if sources_count is None:
        sources_count = _count_sources(fm, body)
    score += 15.0 * min(sources_count, SOURCES_SATURATION) / SOURCES_SATURATION

    # 5. Staleness curve
    score += _staleness_score(str(fm.get("last_verified", "")), now, max_pts=15)

    # 6. knowledge_state
    ks = str(fm.get("knowledge_state", "")).strip().lower()
    if not ks:
        score += KNOWLEDGE_STATE_NEUTRAL
    else:
        score += KNOWLEDGE_STATE_POINTS.get(ks, KNOWLEDGE_STATE_NEUTRAL)

    # 7. Specific claim
    if has_claim:
        score += 10.0

    return max(0, min(100, int(round(score))))


def build_inbound_counter(pages: list[Path]) -> Counter:
    """Walk every page, collect [[wikilink]] targets, return Counter keyed by slug."""
    counter: Counter = Counter()
    for p in pages:
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for target in re.findall(r"\[\[([^\]]+)\]\]", text):
            slug = slugify_wikilink(target)
            counter[slug] += 1
    return counter


def find_wikilinks(path: Path) -> list[str]:
    """Extract all [[wikilink]] targets from a file."""
    content = path.read_text()
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def build_wikilink_lookup(pages: list[Path]) -> tuple[set[str], set[str]]:
    """Build exact-title and slug lookups for valid wiki page targets."""
    page_titles: set[str] = set()
    page_slugs: set[str] = set()
    for p in pages:
        fm = parse_frontmatter(p)
        title = p.stem.replace("-", " ").title()
        if fm and "title" in fm:
            title = str(fm["title"])
        page_titles.add(title)
        page_slugs.add(slugify_wikilink(title))
        page_slugs.add(slugify_wikilink(p.stem))
    return page_titles, page_slugs


def wikilink_exists(link: str, page_titles: set[str], page_slugs: set[str]) -> bool:
    """Return True if the link resolves by exact title or filename slug."""
    return link in page_titles or slugify_wikilink(link) in page_slugs


def lint_wiki(
    wiki_dir: str = ".",
    write_scores: bool = False,
) -> tuple[list[str], list[str], dict[str, int]]:
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
    pages = [
        p for p in pages
        if p.name not in ("index.md", "log.md", "hot.md", "hot-snapshot.md")
        and "/meta/" not in str(p).replace("\\", "/")
    ]

    if not pages:
        return errors, warnings, scores

    page_titles, page_slugs = build_wikilink_lookup(pages)
    inbound_counter = build_inbound_counter(pages)

    index_path = wiki_path / "index.md"
    index_content = index_path.read_text() if index_path.exists() else ""

    now = datetime.now(timezone.utc)

    for page in pages:
        rel = page.relative_to(root)
        fm, fm_text, body = parse_frontmatter_full(page)

        if not fm:
            errors.append(f"{rel}: no valid frontmatter found")
            continue

        for field in REQUIRED_FIELDS:
            if field not in fm and not (field == "sources" and "sources:" in fm_text):
                errors.append(f"{rel}: missing required field '{field}'")

        page_type = fm.get("type", "")
        if page_type and page_type not in VALID_TYPES:
            errors.append(f"{rel}: invalid type '{page_type}' (must be: {', '.join(VALID_TYPES)})")

        if page_type in TYPE_DIR_MAP:
            expected_dir = TYPE_DIR_MAP[page_type]
            if expected_dir not in str(rel):
                errors.append(f"{rel}: type '{page_type}' should be in wiki/{expected_dir}/")

        wikilinks = re.findall(r"\[\[([^\]]+)\]\]", body)
        for link in wikilinks:
            if not wikilink_exists(link, page_titles, page_slugs):
                errors.append(f"{rel}: broken wikilink [[{link}]]")

        title = fm.get("title", "")
        if title and title not in index_content and str(rel) not in index_content:
            warnings.append(f"{rel}: orphan page (not found in index.md)")

        # Staleness warning (separate from score signal)
        last_verified = fm.get("last_verified", "")
        if last_verified:
            try:
                verified_date = datetime.strptime(last_verified, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                days_old = (now - verified_date).days
                if days_old > STALENESS_DAYS:
                    warnings.append(f"{rel}: stale (last verified {days_old} days ago)")
            except ValueError:
                pass

        # --- New quality score ---
        slug = page.stem
        wikilinks_in = inbound_counter.get(slug, 0)
        wikilinks_out = len(set(slugify_wikilink(w) for w in wikilinks))
        sources_count = count_sources_from_text(fm_text)
        claim = has_specific_claim(body)
        score = compute_quality_score(
            fm, body, wikilinks_out, wikilinks_in, claim, now, sources_count,
        )
        scores[str(rel)] = score

        if score < QUALITY_THRESHOLD:
            warnings.append(f"{rel}: quality score {score} (below {QUALITY_THRESHOLD} threshold)")

        if write_scores:
            _write_score_to_frontmatter(page, fm_text, body, score)

    return errors, warnings, scores


def _write_score_to_frontmatter(page: Path, fm_text: str, body: str, score: int) -> None:
    """Idempotently set `quality_score: <score>` in the page's frontmatter."""
    lines = fm_text.split("\n")
    found = False
    new_lines: list[str] = []
    for raw in lines:
        if raw.strip().startswith("quality_score:"):
            current = raw.split(":", 1)[1].strip()
            try:
                if int(current) == score:
                    return  # no change
            except ValueError:
                pass
            indent = raw[: len(raw) - len(raw.lstrip())]
            new_lines.append(f"{indent}quality_score: {score}")
            found = True
        else:
            new_lines.append(raw)
    if not found:
        # Insert before the closing `---`. fm_text is the inner block, so just
        # append at the end of the frontmatter section.
        if new_lines and new_lines[-1].strip() == "":
            new_lines.insert(len(new_lines) - 1, f"quality_score: {score}")
        else:
            new_lines.append(f"quality_score: {score}")
    new_fm = "\n".join(new_lines)
    page.write_text(f"---{new_fm}---{body}")


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
    parser.add_argument(
        "--write-scores",
        action="store_true",
        help="Persist computed quality_score back to each page's frontmatter (idempotent).",
    )
    args = parser.parse_args()

    if args.contradictions_only:
        hits = find_contradictions(args.wiki_dir)
        print(f"=== Contradictions ({len(hits)}) ===")
        for rel, lineno, title in hits:
            print(f"  🔻 {rel}:{lineno} — {title}")
        sys.exit(0 if not hits else 2)

    errors, warnings, scores = lint_wiki(args.wiki_dir, write_scores=args.write_scores)
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
        print("\nSCORE DISTRIBUTION:")
        dist = Counter(scores.values())
        for s in sorted(dist):
            bar = "█" * min(50, dist[s])
            print(f"  {s:3d}: {dist[s]:4d}  {bar}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
