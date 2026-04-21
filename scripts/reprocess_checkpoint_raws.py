#!/usr/bin/env python3
"""Reprocess Copilot checkpoint raws into wiki source pages without LLM calls.

This manual path is intended for backlog refreshes where raw checkpoint exports
already contain durable structured summaries. It refreshes or creates
``wiki/sources/copilot-session-checkpoint-*.md`` pages, preserves existing wiki
linkage where possible, updates raw status, appends audit-log entries, rebuilds
the index, and runs the same post-processing used by the main ingest pipeline.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from auto_ingest import (  # noqa: E402
    append_log,
    compute_sha256,
    parse_frontmatter,
    postprocess_created_pages,
    rebuild_index,
    slugify,
    update_raw_status,
)
from checkpoint_classifier import COMPRESS, RETAIN, classify_checkpoint, resolve_retention  # noqa: E402
from checkpoint_state import derive_knowledge_state  # noqa: E402

CHECKPOINT_GLOB = "raw/backfill-copilot-sessions-*/**/*.md"
SECTION_NAMES = (
    "overview",
    "history",
    "work_done",
    "technical_details",
    "important_files",
    "next_steps",
)
MAX_KEY_POINTS = 6
MAX_QUOTES = 3
MAX_RELATED = 8
POSITIVE_KEYPOINT_RE = re.compile(
    r"\b(implement|created|create|fix|fixed|purge|purged|add|added|convert|converted|"
    r"commit|committed|push|pushed|merge|merged|install|installed|"
    r"test|tested|deploy|deployed|force-pushed|recreated)\b",
    re.IGNORECASE,
)


@dataclass
class CheckpointRender:
    raw_path: Path
    page_path: Path
    page_rel: str
    raw_rel: str
    created: bool
    updated: bool


def _clean_block(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if cleaned and not blank:
                cleaned.append("")
            blank = True
            continue
        cleaned.append(stripped)
        blank = False
    return "\n".join(cleaned).strip()


def _extract_section(body: str, name: str) -> str:
    pattern = rf"<{re.escape(name)}>\s*(.*?)\s*</{re.escape(name)}>"
    match = re.search(pattern, body, flags=re.S | re.I)
    if match:
        return _clean_block(match.group(1))
    return ""


def _extract_checkpoint_title(body: str, fm: dict, raw_path: Path) -> str:
    match = re.search(r"\*\*Checkpoint title:\*\*\s*(.+)", body)
    if match:
        return match.group(1).strip()

    title = str(fm.get("title") or "").strip()
    prefix = "Copilot Session Checkpoint:"
    if title.startswith(prefix):
        return title[len(prefix):].strip()
    if title:
        return title
    return raw_path.stem.replace("-", " ").title()


def _extract_checkpoint_timestamp(body: str, fm: dict) -> str:
    for pattern in (
        r"\*\*Checkpoint timestamp:\*\*\s*([0-9T:\-.+Z]+)",
        r"\*\*Exported:\*\*\s*([0-9T:\-.+Z]+)",
    ):
        match = re.search(pattern, body)
        if match:
            return match.group(1)[:10]

    captured = str(fm.get("captured") or "").strip()
    if captured:
        return captured[:10]
    return datetime.now(timezone.utc).date().isoformat()


def _collect_list_items(block: str) -> list[str]:
    if not block:
        return []

    items: list[str] = []
    current: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.match(r"^(\d+\.\s+|- \[[ xX]\]\s+|- )", line):
            if current:
                items.append(" ".join(current).strip())
            item = re.sub(r"^(\d+\.\s+|- \[[ xX]\]\s+|- )", "", line).strip()
            current = [item] if item else []
            continue
        if current:
            current.append(line)
    if current:
        items.append(" ".join(current).strip())
    return [item for item in items if item]


def _derive_key_points(sections: dict[str, str]) -> list[str]:
    candidates: list[str] = []

    work_done = sections.get("work_done", "")
    for raw_line in work_done.splitlines():
        line = raw_line.strip()
        if not line.startswith("- [x]"):
            continue
        item = re.sub(r"^- \[[xX]\]\s+", "", line).strip()
        if item:
            candidates.append(item)

    for name in ("history", "technical_details", "next_steps"):
        for item in _collect_list_items(sections.get(name, "")):
            if POSITIVE_KEYPOINT_RE.search(item):
                candidates.append(item)

    deduped: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        normalized = item.casefold()
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(item)
        if len(deduped) >= MAX_KEY_POINTS:
            break

    if len(deduped) < 3:
        overview = sections.get("overview", "")
        if overview:
            overview_line = re.sub(r"\s+", " ", overview).strip()
            if overview_line and overview_line.casefold() not in seen:
                deduped.insert(0, overview_line)
    return deduped


def _fallback_summary(body: str) -> str:
    lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("**"):
            continue
        if line.startswith("<") and line.endswith(">"):
            continue
        if re.match(r"^(- |\d+\.)", line):
            continue
        lines.append(line)
        if len("\n".join(lines)) >= 360:
            break
    summary = " ".join(lines).strip()
    return re.sub(r"\s+", " ", summary)[:400].strip()


def _derive_quotes(body: str) -> list[str]:
    quotes: list[str] = []
    seen: set[str] = set()
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line.startswith(">"):
            continue
        cleaned = re.sub(r"^>+\s*", "", line).strip().strip('"')
        if (
            cleaned.count(" ") < 5
            or "`" in cleaned
            or not cleaned
            or not re.match(r"^[A-Za-z0-9]", cleaned)
            or cleaned.endswith(":")
        ):
            continue
        if cleaned.casefold() in seen:
            continue
        seen.add(cleaned.casefold())
        quotes.append(cleaned)
        if len(quotes) >= MAX_QUOTES:
            break
    return quotes


def _format_list_section(items: Iterable[str], empty: str) -> str:
    items = [item for item in items if item]
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def _format_related_section(related_titles: list[str]) -> str:
    if not related_titles:
        return "No existing wiki links preserved."
    return "\n".join(f"- [[{title}]]" for title in related_titles)


def _format_important_files(block: str) -> str:
    return _format_structured_block(block, "No important files recorded.")


def _format_structured_block(block: str, empty: str) -> str:
    block = _clean_block(block)
    if not block:
        return empty

    lines: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if line.endswith(":") and not re.match(r"^(\d+\.\s+|- )", line):
            if lines and lines[-1] != "":
                lines.append("")
            lines.append(f"**{line}**")
            continue
        lines.append(line)

    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) if lines else empty


def _format_technical_details(block: str) -> str:
    items = _collect_list_items(block)
    if not items:
        return "No technical details recorded."
    return "\n".join(f"- {item}" for item in items)


def _existing_source_pages(project_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    sources_dir = project_root / "wiki" / "sources"
    for path in sorted(sources_dir.glob("*.md")):
        fm, _ = parse_frontmatter(path)
        sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
        for source in sources:
            mapping[str(source)] = path
    return mapping


def _title_catalog(project_root: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    wiki_dir = project_root / "wiki"
    for category in ("concepts", "entities", "sources", "synthesis"):
        for path in sorted((wiki_dir / category).glob("*.md")):
            if path.name in {"index.md", "log.md", "hot.md", ".gitkeep"}:
                continue
            fm, _ = parse_frontmatter(path)
            title = str(fm.get("title") or path.stem.replace("-", " ").title())
            titles[_slug_key(title)] = title
            titles[_slug_key(path.stem)] = title
    return titles


def _slug_key(value: str) -> str:
    return slugify(value).replace(".", "-")


def _merge_preserved_list(*lists: Iterable[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for values in lists:
        for value in values:
            clean = value.strip()
            if not clean:
                continue
            key = clean.casefold()
            if key in seen:
                continue
            seen.add(key)
            merged.append(clean)
    return merged


def _related_from_tags(tags: list[str], title_catalog: dict[str, str], page_title: str) -> list[str]:
    related: list[str] = []
    for tag in tags:
        title = title_catalog.get(_slug_key(tag))
        if not title or title == page_title:
            continue
        related.append(title)
        if len(related) >= MAX_RELATED:
            break
    return related


def _render_source_page(
    *,
    page_title: str,
    created_date: str,
    source_hash: str,
    raw_rel: str,
    raw_tags: list[str],
    checkpoint_class: str,
    retention_mode: str,
    knowledge_state: str,
    concepts: list[str],
    related_titles: list[str],
    summary: str,
    key_points: list[str],
    execution_snapshot: str,
    technical_details: str,
    important_files: str,
    next_steps: str,
    quotes: list[str],
) -> str:
    concept_block = "\n".join(f"  - {slug}" for slug in concepts) if concepts else "  []"
    related_block = (
        "\n".join(f'  - "[[{title}]]"' for title in related_titles)
        if related_titles
        else "  []"
    )
    page_tier = "archive" if retention_mode == COMPRESS else "hot"
    tags_block = ", ".join(raw_tags)

    quotes_section = (
        "\n".join(f'> "{quote}" — Session Checkpoint Export' for quote in quotes)
        if quotes
        else "No notable quotes extracted."
    )

    return f"""---
title: "{page_title}"
type: source
created: {created_date}
last_verified: {datetime.now(timezone.utc).date().isoformat()}
source_hash: "{source_hash}"
sources:
  - {raw_rel}
quality_score: 0
concepts:
{concept_block}
related:
{related_block}
tier: {page_tier}
tags: [{tags_block}]
checkpoint_class: {checkpoint_class}
retention_mode: {retention_mode}
knowledge_state: {knowledge_state}
---

# {page_title}

## Summary

{summary or "No summary available."}

## Key Points

{_format_list_section(key_points, "- No key points extracted.")}

## Execution Snapshot

{execution_snapshot}

## Technical Details

{technical_details}

## Important Files

{important_files}

## Next Steps

{next_steps}

## Related Wiki Pages

{_format_related_section(related_titles)}

## Notable Quotes

{quotes_section}

## Source Details

| Field | Value |
|-------|-------|
| Original | `{raw_rel}` |
| Type | checkpoint |
| Author | Unknown |
| Date | {created_date} |
| URL | N/A |
"""


def _parse_page_lists(page_path: Path) -> tuple[list[str], list[str], list[str]]:
    if not page_path.exists():
        return [], [], []
    fm, _ = parse_frontmatter(page_path)
    tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
    concepts = fm.get("concepts") if isinstance(fm.get("concepts"), list) else []
    related = fm.get("related") if isinstance(fm.get("related"), list) else []

    related_titles: list[str] = []
    for entry in related:
        match = re.search(r"\[\[([^\]]+)\]\]", entry)
        related_titles.append(match.group(1) if match else entry)
    return [str(tag) for tag in tags], [str(concept) for concept in concepts], related_titles


def _parse_frontmatter_text(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    fm: dict[str, str] = {}
    for raw_line in parts[1].strip().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("- ") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def _preserve_tracked_title(page_path: Path, project_root: Path, fallback: str) -> str:
    rel = str(page_path.relative_to(project_root))
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD:{rel}"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return fallback

    tracked_title = _parse_frontmatter_text(result.stdout).get("title", "").strip()
    return tracked_title or fallback


def _should_process(path: Path, *, only_pending: bool) -> bool:
    if not only_pending:
        return True
    fm, _ = parse_frontmatter(path)
    return str(fm.get("status") or "").strip().lower() == "pending"


def _resolve_page_path(
    *,
    project_root: Path,
    raw_rel: str,
    existing_sources: dict[str, Path],
    page_title: str,
) -> Path:
    if raw_rel in existing_sources:
        return existing_sources[raw_rel]

    candidate = project_root / "wiki" / "sources" / f"{slugify(page_title)}.md"
    if not candidate.exists():
        return candidate

    fm, _ = parse_frontmatter(candidate)
    sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
    if raw_rel in sources:
        return candidate

    suffix = compute_sha256(raw_rel)[:8]
    return candidate.with_name(f"{candidate.stem}-{suffix}.md")


def process_checkpoint_raws(
    *,
    project_root: Path,
    paths: list[Path],
    dry_run: bool,
) -> tuple[list[CheckpointRender], Counter[str]]:
    existing_sources = _existing_source_pages(project_root)
    title_catalog = _title_catalog(project_root)
    log_path = project_root / "wiki" / "log.md"
    wiki_dir = project_root / "wiki"

    results: list[CheckpointRender] = []
    stats: Counter[str] = Counter()

    for raw_path in paths:
        fm, body = parse_frontmatter(raw_path)
        raw_rel = str(raw_path.relative_to(project_root))
        checkpoint_title = _extract_checkpoint_title(body, fm, raw_path)
        page_title = f"Copilot Session Checkpoint: {checkpoint_title}"
        page_path = _resolve_page_path(
            project_root=project_root,
            raw_rel=raw_rel,
            existing_sources=existing_sources,
            page_title=page_title,
        )
        if page_path.exists():
            page_title = _preserve_tracked_title(page_path, project_root, page_title)
        page_rel = str(page_path.relative_to(project_root))

        body_hash = compute_sha256(body)
        created_date = _extract_checkpoint_timestamp(body, fm)
        raw_tags = [str(tag) for tag in fm.get("tags", [])] if isinstance(fm.get("tags"), list) else []
        raw_tags = _merge_preserved_list(raw_tags)

        sections = {name: _extract_section(body, name) for name in SECTION_NAMES}
        summary = sections.get("overview", "") or _fallback_summary(body)
        key_points = _derive_key_points(sections)
        execution_snapshot = _format_structured_block(
            sections.get("work_done", ""),
            "No execution details recorded.",
        )
        technical_details = _format_technical_details(sections.get("technical_details", ""))
        next_steps = _format_structured_block(
            sections.get("next_steps", ""),
            "No next steps recorded.",
        )
        important_files = _format_important_files(sections.get("important_files", ""))
        quotes = _derive_quotes(body)

        classification = classify_checkpoint(page_title, body)
        checkpoint_class = classification.cls
        retention_mode = resolve_retention(checkpoint_class)
        knowledge_state = derive_knowledge_state(page_title, body, checkpoint_class, retention_mode)

        existing_tags, existing_concepts, existing_related = _parse_page_lists(page_path)
        merged_tags = _merge_preserved_list(raw_tags, existing_tags)
        related_titles = _merge_preserved_list(
            existing_related,
            _related_from_tags(merged_tags, title_catalog, page_title),
        )[:MAX_RELATED]
        concept_slugs = _merge_preserved_list(existing_concepts)

        rendered = _render_source_page(
            page_title=page_title,
            created_date=created_date,
            source_hash=body_hash,
            raw_rel=raw_rel,
            raw_tags=merged_tags,
            checkpoint_class=checkpoint_class,
            retention_mode=retention_mode,
            knowledge_state=knowledge_state,
            concepts=concept_slugs,
            related_titles=related_titles,
            summary=summary,
            key_points=key_points,
            execution_snapshot=execution_snapshot,
            technical_details=technical_details,
            important_files=important_files,
            next_steps=next_steps,
            quotes=quotes,
        )

        prior = page_path.read_text() if page_path.exists() else None
        changed = prior != rendered
        created = not page_path.exists()

        if dry_run:
            results.append(
                CheckpointRender(
                    raw_path=raw_path,
                    page_path=page_path,
                    page_rel=page_rel,
                    raw_rel=raw_rel,
                    created=created,
                    updated=changed and not created,
                )
            )
            stats["created" if created else "updated" if changed else "unchanged"] += 1
            continue

        page_path.parent.mkdir(parents=True, exist_ok=True)
        if changed or created:
            page_path.write_text(rendered)
            stats["created" if created else "updated"] += 1
        else:
            stats["unchanged"] += 1

        update_raw_status(raw_path, "ingested")
        append_log(
            log_path,
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": "ingest",
                "agent": "manual-checkpoint-reprocess",
                "targets": [page_rel],
                "source": raw_rel,
                "status": "success",
                "notes": "Refreshed checkpoint source page from durable raw summary",
            },
        )
        existing_sources[raw_rel] = page_path
        results.append(
            CheckpointRender(
                raw_path=raw_path,
                page_path=page_path,
                page_rel=page_rel,
                raw_rel=raw_rel,
                created=created,
                updated=changed and not created,
            )
        )

    if not dry_run and results:
        touched_pages = sorted({result.page_rel for result in results})
        postprocess_created_pages(wiki_dir, touched_pages, project_root)
        rebuild_index(project_root)

    return results, stats


def _discover_paths(project_root: Path, only_pending: bool) -> list[Path]:
    paths = sorted(project_root.glob(CHECKPOINT_GLOB))
    return [path for path in paths if _should_process(path, only_pending=only_pending)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh Copilot checkpoint raws into wiki source pages without LLM calls"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional explicit raw files to process (defaults to checkpoint backlog)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=ROOT,
        help="Repository root (defaults to this checkout)",
    )
    parser.add_argument(
        "--only-pending",
        action="store_true",
        help="Process only raws whose frontmatter status is pending",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview page updates without writing files",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    paths = [path.resolve() for path in args.paths] if args.paths else _discover_paths(
        project_root,
        only_pending=args.only_pending,
    )
    if not paths:
        print("No checkpoint raws matched the requested selection.")
        return 0

    results, stats = process_checkpoint_raws(
        project_root=project_root,
        paths=paths,
        dry_run=args.dry_run,
    )

    action = "Would refresh" if args.dry_run else "Refreshed"
    print(
        f"{action} {len(results)} checkpoint raws "
        f"(created={stats['created']}, updated={stats['updated']}, unchanged={stats['unchanged']})"
    )
    for result in results[:10]:
        status = "create" if result.created else "update" if result.updated else "skip"
        print(f"- {status}: {result.raw_rel} -> {result.page_rel}")
    if len(results) > 10:
        print(f"- ... {len(results) - 10} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
