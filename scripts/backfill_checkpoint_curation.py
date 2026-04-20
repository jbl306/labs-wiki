#!/usr/bin/env python3
"""Phase 5 backfill — bring the existing checkpoint corpus up to the new standard.

For every ``wiki/sources/copilot-session-checkpoint-*.md`` page:

1. Classify with ``checkpoint_classifier.classify_checkpoint``.
2. Stamp ``checkpoint_class`` and ``retention_mode`` into the frontmatter
   (idempotent — existing values are overwritten with the freshly classified
   ones).
3. If retention is ``compress``, demote ``tier: hot`` → ``tier: archive`` so the
   page drops out of ``hot.md`` and ``snapshot_hot.py`` lists.
4. Recompute ``quality_score`` using the same heuristic
   ``auto_ingest._compute_quality_score`` uses (presence of required fields,
   wikilinks, sources, freshness/last_verified).

Idempotent. Run with ``--dry-run`` to preview changes without writing.

Usage::

    python3 scripts/backfill_checkpoint_curation.py [--dry-run] [--report PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from checkpoint_classifier import (  # noqa: E402
    COMPRESS,
    RETAIN,
    SKIP,
    classify_checkpoint,
    resolve_retention,
)
from checkpoint_state import derive_knowledge_state  # noqa: E402

CHECKPOINT_GLOB = "copilot-session-checkpoint-*.md"
REQUIRED_FIELDS = ("title", "type", "created", "sources")
STALENESS_DAYS = 90


# ---------------------------------------------------------------------------
# Lightweight YAML reader/writer (preserves comments, ordering, lists)
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm_block = parts[1]
    body = parts[2]
    return fm_block.strip("\n").split("\n"), body


def parse_simple_fm(lines: list[str]) -> dict[str, Any]:
    """Parse a small, well-formed frontmatter block; lists are joined with len."""
    fm: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            fm[current_key] = current_list
            continue
        if ":" in stripped:
            if current_list is not None:
                current_list = None
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if value:
                fm[key] = value.strip('"').strip("'")
                current_list = None
            else:
                fm[key] = ""
    return fm


def upsert_fm_field(lines: list[str], key: str, value: str) -> list[str]:
    """Replace the line for ``key`` (or append at the end) with ``key: value``.

    Skips list-style values (we don't currently need to set lists)."""
    pat = re.compile(rf"^\s*{re.escape(key)}\s*:")
    new_lines: list[str] = []
    found = False
    for line in lines:
        if pat.match(line) and not line.lstrip().startswith("- "):
            new_lines.append(f"{key}: {value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{key}: {value}")
    return new_lines


# ---------------------------------------------------------------------------
# Quality score (mirror of auto_ingest._compute_quality_score)
# ---------------------------------------------------------------------------


def compute_quality_score(fm: dict, has_wikilinks: bool, has_related: bool) -> int:
    score = 0
    required_present = sum(1 for f in REQUIRED_FIELDS if f in fm and fm[f])
    score += int(25 * required_present / len(REQUIRED_FIELDS))

    if has_wikilinks or has_related:
        score += 25

    if fm.get("sources"):
        score += 25

    # Freshness: last_verified within STALENESS_DAYS
    lv = fm.get("last_verified") or fm.get("created")
    fresh = False
    if lv:
        try:
            d = datetime.strptime(str(lv)[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - d).days
            fresh = age <= STALENESS_DAYS
        except Exception:
            pass
    if fresh:
        score += 25
    elif lv:
        score += 12
    return score


# ---------------------------------------------------------------------------
# Per-page operation
# ---------------------------------------------------------------------------


def process_page(path: Path) -> dict[str, Any]:
    text = path.read_text()
    parts = split_frontmatter(text)
    if parts is None:
        return {"path": str(path), "skipped": "no-frontmatter"}
    fm_lines, body = parts
    fm = parse_simple_fm(fm_lines)

    title = fm.get("title", path.stem)
    checkpoint_body = body
    sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
    for source in sources:
        raw_path = ROOT / str(source)
        if not raw_path.exists():
            continue
        raw_parts = split_frontmatter(raw_path.read_text())
        checkpoint_body = raw_parts[1] if raw_parts is not None else raw_path.read_text()
        break

    cls = classify_checkpoint(title, checkpoint_body)
    retention = resolve_retention(cls.cls)
    knowledge_state = derive_knowledge_state(title, checkpoint_body, cls.cls, retention)

    has_related = bool(fm.get("related")) and fm.get("related") != "[]"
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", body)
    has_wikilinks = len(wikilinks) > 0
    score = compute_quality_score(fm, has_wikilinks, has_related)

    desired_tier = "archive" if retention == COMPRESS else "hot"
    if retention == SKIP:
        # We never had skip pages historically, but be defensive.
        desired_tier = "archive"

    old_class = fm.get("checkpoint_class", "")
    old_retention = fm.get("retention_mode", "")
    old_tier = fm.get("tier", "hot") or "hot"
    old_score = fm.get("quality_score", "0")
    old_knowledge_state = fm.get("knowledge_state", "")

    new_lines = list(fm_lines)
    new_lines = upsert_fm_field(new_lines, "checkpoint_class", cls.cls)
    new_lines = upsert_fm_field(new_lines, "retention_mode", retention)
    new_lines = upsert_fm_field(new_lines, "tier", desired_tier)
    new_lines = upsert_fm_field(new_lines, "knowledge_state", knowledge_state)
    new_lines = upsert_fm_field(new_lines, "quality_score", str(score))

    new_text = "---\n" + "\n".join(new_lines) + "\n---" + body
    changed = new_text != text

    return {
        "path": str(path.relative_to(ROOT)),
        "title": title,
        "checkpoint_class": cls.cls,
        "retention_mode": retention,
        "tier_before": old_tier,
        "tier_after": desired_tier,
        "knowledge_state": knowledge_state,
        "score_before": str(old_score),
        "score_after": score,
        "wikilinks": len(wikilinks),
        "has_related": has_related,
        "rule": cls.matched_rule,
        "changed": changed,
        "new_text": new_text if changed else None,
        "class_before": old_class,
        "retention_before": old_retention,
        "knowledge_state_before": old_knowledge_state,
    }


def resolve_target_paths(sources_dir: Path, requested: list[str], limit: int) -> list[Path]:
    """Resolve repo-relative or basename checkpoint targets."""
    if not requested:
        paths = sorted(sources_dir.glob(CHECKPOINT_GLOB))
        return paths[:limit] if limit > 0 else paths

    resolved: list[Path] = []
    seen: set[Path] = set()
    for raw in requested:
        candidate_strings = (
            raw,
            str(ROOT / raw),
            str(sources_dir / raw),
            str(sources_dir / Path(raw).name),
        )
        match: Path | None = None
        for candidate_str in candidate_strings:
            candidate = Path(candidate_str)
            if candidate.exists() and candidate.is_file():
                match = candidate.resolve()
                break
        if match is None:
            basename_matches = sorted(sources_dir.glob(Path(raw).name))
            if len(basename_matches) == 1:
                match = basename_matches[0].resolve()
        if match is None:
            raise SystemExit(f"checkpoint page not found: {raw}")
        if match not in seen:
            resolved.append(match)
            seen.add(match)

    return resolved[:limit] if limit > 0 else resolved


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", type=Path, default=None,
                    help="Write a JSON report of all changes")
    ap.add_argument("--wiki", type=Path, default=ROOT / "wiki")
    ap.add_argument(
        "--path",
        action="append",
        default=[],
        help="Only process the given checkpoint page (repeatable; basename or repo-relative path)",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit processed checkpoint pages after filtering (0 = all)",
    )
    args = ap.parse_args()

    sources_dir = args.wiki / "sources"
    if not sources_dir.is_dir():
        print(f"sources dir not found: {sources_dir}", file=sys.stderr)
        return 1

    target_paths = resolve_target_paths(sources_dir, args.path, args.limit)
    results: list[dict[str, Any]] = []
    for p in target_paths:
        r = process_page(p)
        results.append(r)
        if r.get("changed") and not args.dry_run:
            Path(r["path"]).resolve()  # safety: ensure resolved
            (ROOT / r["path"]).write_text(r.pop("new_text"))
        else:
            r.pop("new_text", None)

    cls_counts = Counter(r["checkpoint_class"] for r in results)
    knowledge_state_counts = Counter(r["knowledge_state"] for r in results)
    ret_counts = Counter(r["retention_mode"] for r in results)
    tier_after = Counter(r["tier_after"] for r in results)
    score_dist = Counter()
    for r in results:
        s = r["score_after"]
        bucket = "0" if s == 0 else "1-49" if s < 50 else "50-74" if s < 75 else "75-100"
        score_dist[bucket] += 1
    changed_count = sum(1 for r in results if r["changed"])

    print(
        f"== Phase 5 backfill ({len(results)} checkpoints, dry_run={args.dry_run}, "
        f"filtered={bool(args.path or args.limit)}) =="
    )
    print()
    print("Class distribution:")
    for k in ("durable-architecture", "durable-debugging", "durable-workflow",
              "project-progress", "low-signal"):
        print(f"  {k:24s} = {cls_counts.get(k,0):3d}")
    print()
    print("Retention distribution:")
    for k in (RETAIN, COMPRESS, SKIP):
        print(f"  {k:10s} = {ret_counts.get(k,0):3d}")
    print()
    print("Knowledge-state distribution:")
    for k in ("planned", "executed", "validated"):
        print(f"  {k:10s} = {knowledge_state_counts.get(k,0):3d}")
    print()
    print("Tier (after):")
    for k, v in tier_after.most_common():
        print(f"  {k:10s} = {v:3d}")
    print()
    print("Quality score distribution (after):")
    for k in ("0", "1-49", "50-74", "75-100"):
        print(f"  {k:6s} = {score_dist.get(k,0):3d}")
    print()
    print(f"Pages changed: {changed_count}/{len(results)}")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total": len(results),
            "changed": changed_count,
            "dry_run": args.dry_run,
            "class_distribution": dict(cls_counts),
            "knowledge_state_distribution": dict(knowledge_state_counts),
            "retention_distribution": dict(ret_counts),
            "tier_after": dict(tier_after),
            "quality_score_buckets": dict(score_dist),
            "results": results,
        }, indent=2))
        print(f"\nReport written: {args.report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
