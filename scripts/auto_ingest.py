#!/usr/bin/env python3
"""
Auto-ingest: Process raw wiki sources through an LLM pipeline.

Reads a raw markdown source from raw/, extracts concepts/entities via
GitHub Models API (GPT-4o), generates wiki pages, and updates the index.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import httpx
from openai import OpenAI

log = logging.getLogger("auto-ingest")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_MODELS_URL = os.environ.get(
    "GITHUB_MODELS_URL", "https://models.inference.ai.azure.com"
)
DEFAULT_MODEL = "gpt-4o"
MAX_RETRIES = 3
URL_FETCH_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from a markdown file."""
    content = path.read_text()
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm: dict = {}
    current_key: str | None = None
    current_list: list[str] | None = None

    for line in parts[1].strip().split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item under a key
        if stripped.startswith("- ") and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            fm[current_key] = current_list
            continue

        # Key: value line
        if ":" in stripped:
            # Save pending list
            if current_list is not None:
                current_list = None

            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "" or value == "[]":
                current_key = key
                if value == "[]":
                    fm[key] = []
                    current_list = None
                else:
                    current_list = []
                continue

            # Inline list: [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                items = [
                    v.strip().strip('"').strip("'")
                    for v in value[1:-1].split(",")
                    if v.strip()
                ]
                fm[key] = items
                current_key = key
                current_list = None
                continue

            fm[key] = value.strip('"').strip("'")
            current_key = key
            current_list = None

    return fm, parts[2].strip()


def slugify(title: str) -> str:
    """Convert a title to a kebab-case filename slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:80]


def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# URL content fetching
# ---------------------------------------------------------------------------


def fetch_url_content(url: str) -> str:
    """Fetch text content from a URL. Handles GitHub gists specially."""
    # GitHub gist → fetch raw content
    gist_match = re.match(
        r"https://gist\.github\.com/([^/]+)/([a-f0-9]+)", url
    )
    if gist_match:
        user, gist_id = gist_match.groups()
        raw_url = f"https://gist.githubusercontent.com/{user}/{gist_id}/raw"
        log.info("Fetching GitHub gist raw content: %s", raw_url)
        resp = httpx.get(raw_url, follow_redirects=True, timeout=URL_FETCH_TIMEOUT)
        resp.raise_for_status()
        return resp.text

    log.info("Fetching URL content: %s", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; labs-wiki-bot/1.0)",
        "Accept": "text/html,text/plain,application/json",
    }
    resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=URL_FETCH_TIMEOUT)
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")
    if "html" in content_type:
        # Strip HTML tags for a rough text extraction
        text = re.sub(r"<script[^>]*>.*?</script>", "", resp.text, flags=re.S)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:50_000]

    return resp.text[:50_000]


# ---------------------------------------------------------------------------
# Existing wiki state
# ---------------------------------------------------------------------------


def get_existing_pages(wiki_dir: Path) -> dict[str, str]:
    """Return {title: relative_path} for all existing wiki pages."""
    pages: dict[str, str] = {}
    for category in ("sources", "concepts", "entities", "synthesis"):
        cat_dir = wiki_dir / category
        if not cat_dir.exists():
            continue
        for page in cat_dir.glob("*.md"):
            if page.name in ("index.md", "log.md", ".gitkeep"):
                continue
            fm, _ = parse_frontmatter(page)
            title = fm.get("title", page.stem.replace("-", " ").title())
            pages[title] = str(page.relative_to(wiki_dir.parent))
    return pages


def check_already_processed(wiki_dir: Path, source_hash: str) -> bool:
    """Check if a source with this hash has already been processed."""
    sources_dir = wiki_dir / "sources"
    if not sources_dir.exists():
        return False
    for page in sources_dir.glob("*.md"):
        fm, _ = parse_frontmatter(page)
        if fm.get("source_hash") == source_hash:
            log.info("Source already processed (hash match): %s", page.name)
            return True
    return False


# ---------------------------------------------------------------------------
# LLM extraction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a knowledge extraction agent for a personal wiki system.
    Given a source document, you extract structured knowledge.

    ## Rules
    1. Extract CONCEPTS — ideas, techniques, patterns, methodologies
    2. Extract ENTITIES — tools, people, organizations, datasets, models
    3. Write a SOURCE SUMMARY — concise overview of the document
    4. Every claim must be grounded in the source — no hallucination
    5. Use Title Case for all titles (e.g., "Rotary Position Embedding")
    6. Slugs are kebab-case (e.g., "rotary-position-embedding")
    7. Keep descriptions concise but informative
    8. If the source is short or is just a link/stub, extract what you can — it's OK to have few or no concepts/entities

    ## Output Format
    Return ONLY valid JSON matching this schema (no markdown fencing):
    {
      "source_summary": {
        "title": "Source Title",
        "summary": "2-3 sentence summary of the source",
        "key_points": ["point 1", "point 2", "point 3"],
        "author": "Author name or null",
        "publication_date": "Date or null",
        "source_type": "article|paper|video|note|gist|guide",
        "notable_quotes": [{"quote": "...", "attribution": "..."}]
      },
      "concepts": [
        {
          "title": "Concept Title",
          "slug": "concept-slug",
          "overview": "2-3 sentence explanation",
          "how_it_works": "Detailed explanation paragraph",
          "key_properties": [{"name": "Property", "description": "..."}],
          "related_concepts": [{"title": "Other Concept", "relationship": "how they relate"}],
          "practical_applications": "Where/how this is used",
          "tags": ["tag1", "tag2"]
        }
      ],
      "entities": [
        {
          "title": "Entity Name",
          "slug": "entity-slug",
          "overview": "2-3 sentence description",
          "entity_type": "Tool|Person|Organization|Dataset|Model|Framework",
          "created_year": "Year or null",
          "creator": "Creator or null",
          "url": "Official URL or null",
          "status": "Active|Deprecated|Historical",
          "relevance": "Why this matters",
          "associated_concepts": [{"title": "...", "relationship": "..."}],
          "tags": ["tag1", "tag2"]
        }
      ],
      "tags": ["tag1", "tag2"]
    }
""")


def call_llm(
    content: str,
    source_title: str,
    source_url: str | None,
    existing_pages: dict[str, str],
    token: str,
    model: str,
) -> dict:
    """Call GitHub Models API to extract knowledge from source content."""
    client = OpenAI(base_url=GITHUB_MODELS_URL, api_key=token)

    existing_list = "\n".join(
        f"- {title} ({path})" for title, path in sorted(existing_pages.items())
    )
    if not existing_list:
        existing_list = "(no existing pages yet)"

    user_prompt = f"""## Source Document
Title: {source_title}
{"URL: " + source_url if source_url else ""}

## Existing Wiki Pages (for cross-referencing, avoid duplicates)
{existing_list}

## Content
{content[:30_000]}"""

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info("LLM call attempt %d/%d (model: %s)", attempt, MAX_RETRIES, model)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=8000,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            return json.loads(raw)
        except Exception as e:
            last_error = e
            log.warning("LLM call attempt %d failed: %s", attempt, e)
            if attempt < MAX_RETRIES:
                import time
                time.sleep(2 ** attempt)

    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts: {last_error}")


# ---------------------------------------------------------------------------
# Wiki page generation
# ---------------------------------------------------------------------------


def generate_source_page(
    extraction: dict,
    raw_path: str,
    source_hash: str,
    source_url: str | None,
    today: str,
    raw_tags: list[str],
) -> tuple[str, str]:
    """Generate source summary page. Returns (filename, content)."""
    ss = extraction["source_summary"]
    title = ss["title"]
    slug = slugify(title)
    filename = f"{slug}.md"

    concept_slugs = [c["slug"] for c in extraction.get("concepts", [])]
    concept_links = [
        f'  - "[[{c["title"]}]]"' for c in extraction.get("concepts", [])
    ]
    entity_links = [
        f'  - "[[{e["title"]}]]"' for e in extraction.get("entities", [])
    ]
    related = concept_links + entity_links

    tags = list(set(raw_tags + extraction.get("tags", [])))

    # Key points
    key_points = "\n".join(f"- {p}" for p in ss.get("key_points", []))

    # Concepts extracted
    concepts_section = "\n".join(
        f'- **[[{c["title"]}]]** — {c["overview"]}'
        for c in extraction.get("concepts", [])
    )

    # Entities mentioned
    entities_section = "\n".join(
        f'- **[[{e["title"]}]]** — {e["overview"]}'
        for e in extraction.get("entities", [])
    )

    # Quotes
    quotes_section = "\n".join(
        f'> "{q["quote"]}" — {q["attribution"]}'
        for q in ss.get("notable_quotes", [])
    )

    content = f"""---
title: "{title}"
type: source
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
{chr(10).join('  - ' + s for s in concept_slugs) if concept_slugs else '  []'}
related:
{chr(10).join(related) if related else '  []'}
tier: hot
tags: [{', '.join(tags)}]
---

# {title}

## Summary

{ss.get("summary", "No summary available.")}

## Key Points

{key_points or "- No key points extracted."}

## Concepts Extracted

{concepts_section or "No concepts extracted."}

## Entities Mentioned

{entities_section or "No entities mentioned."}

## Notable Quotes

{quotes_section or "No notable quotes."}

## Source Details

| Field | Value |
|-------|-------|
| Original | `{raw_path}` |
| Type | {ss.get("source_type", "unknown")} |
| Author | {ss.get("author") or "Unknown"} |
| Date | {ss.get("publication_date") or "Unknown"} |
| URL | {source_url or "N/A"} |
"""
    return filename, content


def generate_concept_page(
    concept: dict,
    raw_path: str,
    source_hash: str,
    source_title: str,
    today: str,
) -> tuple[str, str]:
    """Generate a concept wiki page. Returns (filename, content)."""
    title = concept["title"]
    slug = concept["slug"]
    filename = f"{slug}.md"

    related_concepts = concept.get("related_concepts", [])
    related_links = [f'  - "[[{r["title"]}]]"' for r in related_concepts]
    related_links.append(f'  - "[[{source_title}]]"')

    relationships = "\n".join(
        f'- **[[{r["title"]}]]** — {r["relationship"]}'
        for r in related_concepts
    )

    properties = "\n".join(
        f'- **{p["name"]}:** {p["description"]}'
        for p in concept.get("key_properties", [])
    )

    content = f"""---
title: "{title}"
type: concept
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
  - {slug}
related:
{chr(10).join(related_links)}
tier: hot
tags: [{', '.join(concept.get("tags", []))}]
---

# {title}

## Overview

{concept.get("overview", "No overview available.")}

## How It Works

{concept.get("how_it_works", "Details not yet available.")}

## Key Properties

{properties or "No key properties identified."}

## Relationship to Other Concepts

{relationships or "No relationships identified yet."}

## Practical Applications

{concept.get("practical_applications", "Applications not yet documented.")}

## Sources

- [[{source_title}]] — primary source for this concept
"""
    return filename, content


def generate_entity_page(
    entity: dict,
    raw_path: str,
    source_hash: str,
    source_title: str,
    today: str,
) -> tuple[str, str]:
    """Generate an entity wiki page. Returns (filename, content)."""
    title = entity["title"]
    slug = entity["slug"]
    filename = f"{slug}.md"

    assoc = entity.get("associated_concepts", [])
    related_links = [f'  - "[[{a["title"]}]]"' for a in assoc]
    related_links.append(f'  - "[[{source_title}]]"')

    assoc_section = "\n".join(
        f'- **[[{a["title"]}]]** — {a["relationship"]}' for a in assoc
    )

    content = f"""---
title: "{title}"
type: entity
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
  - {slug}
related:
{chr(10).join(related_links)}
tier: hot
tags: [{', '.join(entity.get("tags", []))}]
---

# {title}

## Overview

{entity.get("overview", "No overview available.")}

## Key Facts

| Field | Value |
|-------|-------|
| Type | {entity.get("entity_type", "Unknown")} |
| Created | {entity.get("created_year") or "Unknown"} |
| Creator | {entity.get("creator") or "Unknown"} |
| URL | {entity.get("url") or "N/A"} |
| Status | {entity.get("status", "Unknown")} |

## Relevance

{entity.get("relevance", "Relevance not yet documented.")}

## Associated Concepts

{assoc_section or "No associated concepts documented."}

## Related Entities

No related entities documented yet.

## Sources

- [[{source_title}]] — where this entity was mentioned
"""
    return filename, content


# ---------------------------------------------------------------------------
# Log + index
# ---------------------------------------------------------------------------


def append_log(log_path: Path, entry: dict) -> None:
    """Append a YAML log entry to wiki/log.md."""
    content = log_path.read_text() if log_path.exists() else ""
    # Strip trailing ``` if present (the log wraps entries in a yaml block)
    content = content.rstrip()
    if content.endswith("```"):
        content = content[:-3].rstrip()

    targets_yaml = "\n".join(f"    - {t}" for t in entry["targets"])
    block = f"""
- timestamp: {entry["timestamp"]}
  operation: {entry["operation"]}
  agent: auto-ingest
  targets:
{targets_yaml}
  source: {entry["source"]}
  status: {entry["status"]}
  notes: "{entry["notes"]}"
```
"""
    log_path.write_text(content + "\n" + block)


def rebuild_index(project_root: Path) -> None:
    """Run compile_index.py to rebuild wiki/index.md."""
    script = project_root / "scripts" / "compile_index.py"
    if script.exists():
        log.info("Rebuilding wiki/index.md")
        subprocess.run(
            [sys.executable, str(script), "--wiki-dir", str(project_root)],
            check=True,
        )
    else:
        log.warning("compile_index.py not found at %s", script)


def update_raw_status(raw_path: Path, new_status: str) -> None:
    """Update the status field in a raw source's frontmatter."""
    content = raw_path.read_text()
    updated = re.sub(
        r"^(status:\s*).*$",
        f"\\g<1>{new_status}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    raw_path.write_text(updated)


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------


def send_ntfy(title: str, message: str, tags: str = "books") -> None:
    """Send a notification via ntfy if configured."""
    server = os.environ.get("NTFY_SERVER", "")
    topic = os.environ.get("NTFY_TOPIC", "")
    if not server or not topic:
        return
    try:
        httpx.post(
            f"{server}/{topic}",
            content=message.encode("utf-8"),
            headers={"Title": title.encode("utf-8").decode("ascii", errors="replace"), "Tags": tags},
            timeout=10,
        )
    except Exception as e:
        log.warning("ntfy notification failed: %s", e)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def ingest_raw_source(
    raw_path: Path,
    project_root: Path,
    token: str,
    model: str = DEFAULT_MODEL,
) -> bool:
    """Process a single raw source file. Returns True on success."""
    log.info("Processing: %s", raw_path)

    # Parse raw source
    fm, body = parse_frontmatter(raw_path)
    if not fm:
        log.error("No frontmatter found in %s", raw_path)
        return False

    status = fm.get("status", "pending")
    if status != "pending":
        log.info("Skipping %s (status: %s)", raw_path.name, status)
        return False

    title = fm.get("title", raw_path.stem)
    source_type = fm.get("type", "text")
    source_url = fm.get("url")
    raw_tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []

    # For URL sources, fetch the actual content
    content = body
    if source_type == "url" and source_url:
        try:
            content = fetch_url_content(source_url)
            log.info("Fetched %d chars from URL", len(content))
        except Exception as e:
            log.error("Failed to fetch URL %s: %s", source_url, e)
            content = body  # Fall back to body text

    if not content or len(content.strip()) < 10:
        log.warning("Source content too short for meaningful extraction")

    # Compute hash & check incremental
    source_hash = compute_sha256(content)
    wiki_dir = project_root / "wiki"

    if check_already_processed(wiki_dir, source_hash):
        log.info("Already processed, updating status only")
        update_raw_status(raw_path, "ingested")
        return True

    # Get existing wiki state
    existing_pages = get_existing_pages(wiki_dir)

    # LLM extraction
    log.info("Calling LLM for extraction...")
    extraction = call_llm(content, title, source_url, existing_pages, token, model)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_rel = str(raw_path.relative_to(project_root))
    source_title = extraction["source_summary"]["title"]

    created_pages: list[str] = []

    # Generate source summary page
    src_filename, src_content = generate_source_page(
        extraction, raw_rel, source_hash, source_url, today, raw_tags,
    )
    src_path = wiki_dir / "sources" / src_filename
    src_path.parent.mkdir(parents=True, exist_ok=True)
    src_path.write_text(src_content)
    created_pages.append(f"wiki/sources/{src_filename}")
    log.info("Created: wiki/sources/%s", src_filename)

    # Generate concept pages
    for concept in extraction.get("concepts", []):
        filename, page_content = generate_concept_page(
            concept, raw_rel, source_hash, source_title, today,
        )
        concept_path = wiki_dir / "concepts" / filename
        concept_path.parent.mkdir(parents=True, exist_ok=True)

        if concept_path.exists():
            # Merge: append source reference to existing page
            existing = concept_path.read_text()
            if raw_rel not in existing:
                merge_line = f"\n- [[{source_title}]] — additional source\n"
                existing = existing.rstrip() + merge_line
                # Add raw path to sources in frontmatter
                existing = existing.replace(
                    "sources:", f"sources:\n  - {raw_rel}", 1
                )
                concept_path.write_text(existing)
                log.info("Merged into existing: wiki/concepts/%s", filename)
        else:
            concept_path.write_text(page_content)
            log.info("Created: wiki/concepts/%s", filename)

        created_pages.append(f"wiki/concepts/{filename}")

    # Generate entity pages
    for entity in extraction.get("entities", []):
        filename, page_content = generate_entity_page(
            entity, raw_rel, source_hash, source_title, today,
        )
        entity_path = wiki_dir / "entities" / filename
        entity_path.parent.mkdir(parents=True, exist_ok=True)

        if entity_path.exists():
            existing = entity_path.read_text()
            if raw_rel not in existing:
                merge_line = f"\n- [[{source_title}]] — additional source\n"
                existing = existing.rstrip() + merge_line
                existing = existing.replace(
                    "sources:", f"sources:\n  - {raw_rel}", 1
                )
                entity_path.write_text(existing)
                log.info("Merged into existing: wiki/entities/%s", filename)
        else:
            entity_path.write_text(page_content)
            log.info("Created: wiki/entities/%s", filename)

        created_pages.append(f"wiki/entities/{filename}")

    # Append to log
    log_path = wiki_dir / "log.md"
    append_log(log_path, {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "operation": "ingest",
        "targets": created_pages,
        "source": raw_rel,
        "status": "success",
        "notes": f"Auto-ingested {len(created_pages)} pages ({len(extraction.get('concepts', []))} concepts, {len(extraction.get('entities', []))} entities)",
    })

    # Rebuild index
    rebuild_index(project_root)

    # Mark raw source as ingested
    update_raw_status(raw_path, "ingested")

    # Notify
    send_ntfy(
        f"Wiki: {source_title}",
        f"Ingested {len(created_pages)} pages from {raw_path.name}",
        tags="books,white_check_mark",
    )

    log.info(
        "✅ Ingested %s → %d pages created",
        raw_path.name,
        len(created_pages),
    )
    return True


def process_all_pending(project_root: Path, token: str, model: str) -> int:
    """Process all pending raw sources. Returns count of processed files."""
    raw_dir = project_root / "raw"
    count = 0
    for raw_file in sorted(raw_dir.glob("*.md")):
        fm, _ = parse_frontmatter(raw_file)
        if fm.get("status") == "pending":
            try:
                if ingest_raw_source(raw_file, project_root, token, model):
                    count += 1
            except Exception:
                log.exception("Failed to process %s", raw_file.name)
                update_raw_status(raw_file, "failed")
                send_ntfy(
                    f"❌ Wiki ingest failed: {raw_file.name}",
                    f"Error processing {raw_file.name}. Check logs.",
                    tags="warning",
                )
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-ingest raw wiki sources via LLM")
    parser.add_argument(
        "raw_file",
        nargs="?",
        help="Specific raw file to process (default: process all pending)",
    )
    parser.add_argument(
        "--project-root",
        default=os.environ.get("PROJECT_ROOT", "."),
        help="Root of the labs-wiki project",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("GITHUB_MODELS_MODEL", DEFAULT_MODEL),
        help="GitHub Models model ID",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", "")),
        help="GitHub Models API token",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not args.token:
        log.error("No API token. Set GITHUB_MODELS_TOKEN or pass --token")
        sys.exit(1)

    project_root = Path(args.project_root).resolve()

    if args.raw_file:
        raw_path = Path(args.raw_file).resolve()
        ok = ingest_raw_source(raw_path, project_root, args.token, args.model)
        sys.exit(0 if ok else 1)
    else:
        count = process_all_pending(project_root, args.token, args.model)
        log.info("Processed %d pending source(s)", count)


if __name__ == "__main__":
    main()
