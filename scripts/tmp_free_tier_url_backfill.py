#!/usr/bin/env python3
"""Preview and run a small free-tier-safe URL raw backfill batch.

Default mode is dry-run. The script targets legacy URL raws that:

1. are already ingested,
2. do not yet contain a persisted fetched-content block, and
3. already back an active non-archive source page in the wiki.

This implements the "high-value targeted backfill" lane from
reports/url-raw-backfill-strategy.md:

- keep AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0,
- refresh a small ranked batch,
- inspect results rather than sweeping the whole corpus.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from auto_ingest import (  # noqa: E402
    FETCHED_CONTENT_START,
    classify_ingest_route,
    parse_frontmatter,
)

DEFAULT_LIMIT = 3
STOP_AFTER_RATE_LIMITS = 2
TIER_SCORES = {
    "core": 40,
    "established": 30,
    "hot": 20,
    "workflow": 10,
    "archive": -20,
}


@dataclass
class SourcePageMeta:
    path: str
    tier: str
    concepts_count: int
    related_count: int
    tags_count: int


@dataclass
class Candidate:
    raw_path: str
    title: str
    url: str
    score: int
    source_page: str
    tier: str
    concepts_count: int
    related_count: int
    tags_count: int
    route_class: str
    lane: str
    model: str
    reasons: list[str]


def _list_count(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def build_source_page_lookup(project_root: Path) -> dict[str, SourcePageMeta]:
    lookup: dict[str, SourcePageMeta] = {}
    sources_dir = project_root / "wiki" / "sources"
    if not sources_dir.exists():
        return lookup

    for page in sorted(sources_dir.glob("*.md")):
        fm, _ = parse_frontmatter(page)
        source_entries = fm.get("sources", [])
        if not isinstance(source_entries, list):
            continue
        meta = SourcePageMeta(
            path=str(page.relative_to(project_root)),
            tier=str(fm.get("tier", "hot") or "hot"),
            concepts_count=_list_count(fm.get("concepts")),
            related_count=_list_count(fm.get("related")),
            tags_count=_list_count(fm.get("tags")),
        )
        for raw_rel in source_entries:
            if isinstance(raw_rel, str):
                lookup[raw_rel] = meta
    return lookup


def resolve_target_paths(raw_dir: Path, requested: list[str], limit: int, project_root: Path) -> list[Path]:
    if not requested:
        paths = sorted(raw_dir.glob("*.md"))
        return paths[:limit] if limit > 0 else paths

    resolved: list[Path] = []
    seen: set[Path] = set()
    for raw in requested:
        candidate_strings = (
            raw,
            str(project_root / raw),
            str(raw_dir / raw),
            str(raw_dir / Path(raw).name),
        )
        match: Path | None = None
        for candidate_str in candidate_strings:
            candidate = Path(candidate_str)
            if candidate.exists() and candidate.is_file():
                match = candidate.resolve()
                break
        if match is None:
            basename_matches = sorted(raw_dir.glob(Path(raw).name))
            if len(basename_matches) == 1:
                match = basename_matches[0].resolve()
        if match is None:
            raise SystemExit(f"raw source not found: {raw}")
        if match not in seen:
            resolved.append(match)
            seen.add(match)
    return resolved[:limit] if limit > 0 else resolved


def score_candidate(raw_rel: str, source_page: SourcePageMeta) -> tuple[int, list[str]]:
    reasons = [f"tier={source_page.tier}"]
    score = TIER_SCORES.get(source_page.tier, 0)

    concept_points = min(source_page.concepts_count * 4, 16)
    related_points = min(source_page.related_count * 2, 16)
    tag_points = min(source_page.tags_count, 8)

    if concept_points:
        score += concept_points
        reasons.append(f"concepts={source_page.concepts_count}")
    if related_points:
        score += related_points
        reasons.append(f"related={source_page.related_count}")
    if tag_points:
        score += tag_points
        reasons.append(f"tags={source_page.tags_count}")

    reasons.append(f"source_page={source_page.path}")
    return score, reasons


def collect_candidates(
    project_root: Path,
    targets: list[str],
    limit: int,
    min_score: int | None,
    max_score: int | None,
) -> tuple[list[Candidate], dict[str, int]]:
    raw_dir = project_root / "raw"
    source_lookup = build_source_page_lookup(project_root)
    stats = {
        "scanned": 0,
        "non_url": 0,
        "not_ingested": 0,
        "already_enriched": 0,
        "missing_source_page": 0,
        "archive_source_page": 0,
        "score_filtered": 0,
        "selected": 0,
    }
    candidates: list[Candidate] = []

    for raw_path in resolve_target_paths(raw_dir, targets, 0, project_root):
        stats["scanned"] += 1
        raw_text = raw_path.read_text()
        fm, body = parse_frontmatter(raw_path)
        if fm.get("type") != "url" or not fm.get("url"):
            stats["non_url"] += 1
            continue
        if fm.get("status") != "ingested":
            stats["not_ingested"] += 1
            continue
        if FETCHED_CONTENT_START in raw_text:
            stats["already_enriched"] += 1
            continue

        raw_rel = str(raw_path.relative_to(project_root))
        source_page = source_lookup.get(raw_rel)
        if source_page is None:
            stats["missing_source_page"] += 1
            continue
        if source_page.tier == "archive":
            stats["archive_source_page"] += 1
            continue

        route = classify_ingest_route(fm, body=body)
        score, reasons = score_candidate(raw_rel, source_page)
        if min_score is not None and score < min_score:
            stats["score_filtered"] += 1
            continue
        if max_score is not None and score > max_score:
            stats["score_filtered"] += 1
            continue
        candidates.append(
            Candidate(
                raw_path=raw_rel,
                title=str(fm.get("title", raw_path.stem)),
                url=str(fm["url"]),
                score=score,
                source_page=source_page.path,
                tier=source_page.tier,
                concepts_count=source_page.concepts_count,
                related_count=source_page.related_count,
                tags_count=source_page.tags_count,
                route_class=route.source_class,
                lane=route.lane,
                model=route.model,
                reasons=reasons,
            )
        )

    candidates.sort(key=lambda item: (-item.score, item.raw_path))
    if limit > 0:
        candidates = candidates[:limit]
    stats["selected"] = len(candidates)
    return candidates, stats


def build_ingest_command(project_root: Path, raw_rel: str, validation_run: bool) -> list[str]:
    cmd = [
        sys.executable,
        str(project_root / "scripts" / "auto_ingest.py"),
        raw_rel,
        "--project-root",
        str(project_root),
        "--force",
        "--refresh-fetch",
    ]
    if validation_run:
        cmd.append("--validation-run")
    return cmd


def run_batch(
    project_root: Path,
    candidates: list[Candidate],
        token: str,
        validation_run: bool,
        stop_after_rate_limits: int,
) -> list[dict[str, Any]]:
    env = os.environ.copy()
    env["AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST"] = "0"
    env["GITHUB_MODELS_TOKEN"] = token
    results: list[dict[str, Any]] = []
    consecutive_rate_limits = 0

    for candidate in candidates:
        cmd = build_ingest_command(project_root, candidate.raw_path, validation_run)
        proc = subprocess.run(
            cmd,
            cwd=project_root,
            env=env,
            capture_output=True,
            text=True,
        )
        combined_output = "\n".join(part for part in (proc.stdout, proc.stderr) if part).strip()
        rate_limited = "429" in combined_output or "rate limit" in combined_output.lower()
        if rate_limited:
            consecutive_rate_limits += 1
        else:
            consecutive_rate_limits = 0

        result = {
            "raw_path": candidate.raw_path,
            "score": candidate.score,
            "returncode": proc.returncode,
            "rate_limited": rate_limited,
            "stdout_tail": proc.stdout.strip().splitlines()[-20:],
            "stderr_tail": proc.stderr.strip().splitlines()[-20:],
            "command": cmd,
        }
        results.append(result)

        if proc.returncode != 0:
            break
        if consecutive_rate_limits >= stop_after_rate_limits:
            break

    return results


def print_preview(candidates: list[Candidate], validation_run: bool) -> None:
    if not candidates:
        print("No eligible free-tier backfill candidates found.")
        return

    print("Free-tier URL backfill preview")
    print("=" * 80)
    for idx, candidate in enumerate(candidates, start=1):
        mode = "validation" if validation_run else "live"
        print(
            f"{idx}. score={candidate.score} lane={candidate.lane} mode={mode} "
            f"raw={candidate.raw_path}"
        )
        print(f"   title: {candidate.title}")
        print(f"   source_page: {candidate.source_page}")
        print(f"   reasons: {', '.join(candidate.reasons)}")
        print(f"   url: {candidate.url}")


def write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preview and run a small free-tier URL raw backfill batch.",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional repo-relative raw paths or basenames to constrain the batch.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Root of the labs-wiki project.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum number of candidates to preview/run (default: {DEFAULT_LIMIT}).",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the selected batch. Default is dry-run preview only.",
    )
    parser.add_argument(
        "--validation-run",
        action="store_true",
        help="Execute through auto_ingest.py in validation-run mode instead of live ingest mode.",
    )
    parser.add_argument(
        "--report",
        help="Optional path to write a JSON preview/run report.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=None,
        help="Optional minimum candidate score filter.",
    )
    parser.add_argument(
        "--max-score",
        type=int,
        default=None,
        help="Optional maximum candidate score filter.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", "")),
        help="GitHub Models API token (required with --execute).",
    )
    parser.add_argument(
        "--stop-after-rate-limits",
        type=int,
        default=STOP_AFTER_RATE_LIMITS,
        help="Stop after this many consecutive rate-limited executions.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if args.min_score is not None and args.max_score is not None and args.min_score > args.max_score:
        raise SystemExit("--min-score cannot be greater than --max-score")

    candidates, stats = collect_candidates(
        project_root,
        args.targets,
        args.limit,
        args.min_score,
        args.max_score,
    )

    payload: dict[str, Any] = {
        "project_root": str(project_root),
        "limit": args.limit,
        "execute": args.execute,
        "validation_run": args.validation_run,
        "min_score": args.min_score,
        "max_score": args.max_score,
        "stats": stats,
        "candidates": [asdict(candidate) for candidate in candidates],
    }

    print_preview(candidates, args.validation_run)

    if not args.execute:
        if args.report:
            write_report(Path(args.report), payload)
        return

    if not args.token:
        raise SystemExit("--execute requires --token or GITHUB_MODELS_TOKEN")
    if not candidates:
        raise SystemExit("no eligible candidates to execute")

    results = run_batch(
        project_root=project_root,
        candidates=candidates,
        token=args.token,
        validation_run=args.validation_run,
        stop_after_rate_limits=args.stop_after_rate_limits,
    )
    payload["results"] = results
    succeeded = sum(1 for result in results if result["returncode"] == 0)
    payload["succeeded"] = succeeded
    payload["failed"] = len(results) - succeeded

    print()
    print("Execution results")
    print("=" * 80)
    for result in results:
        status = "ok" if result["returncode"] == 0 else "failed"
        rate = " rate-limited" if result["rate_limited"] else ""
        print(f"- {status}{rate}: {result['raw_path']}")

    if args.report:
        write_report(Path(args.report), payload)

    if any(result["returncode"] != 0 for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
