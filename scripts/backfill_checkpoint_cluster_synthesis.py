#!/usr/bin/env python3
"""Generate synthesis pages for backlog checkpoint merge clusters.

This is the Phase 5 follow-up batch for the pre-existing checkpoint corpus.
It reuses the synthesis helpers from ``auto_ingest.py`` but drives them from
the current graph's ``checkpoint_health.merge_clusters`` instead of waiting for
new ingests to trigger Phase 3 family synthesis.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "wiki-graph-api"))

from auto_ingest import (  # noqa: E402
    DEFAULT_MODEL,
    append_log,
    call_llm_synthesis,
    generate_synthesis_page,
    parse_frontmatter,
    postprocess_created_pages,
    rebuild_index,
    slugify,
)

LOG = logging.getLogger("checkpoint_cluster_synthesis")
DEFAULT_DIMENSIONS = ["Themes", "Approach", "Outcome", "Lessons"]
MAX_COMPARE_PAGES = 4
MIN_COMPARE_PAGES = 2


def load_checkpoint_health(wiki_dir: Path, graph_path: Path | None) -> dict[str, Any]:
    """Load checkpoint health from graph.json, or rebuild if needed."""
    if graph_path and graph_path.exists():
        payload = json.loads(graph_path.read_text())
        health = payload.get("checkpoint_health")
        if isinstance(health, dict):
            return health

    try:
        from graph_builder import build  # noqa: WPS433
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "graph_builder dependencies are unavailable. Re-run with an existing "
            "wiki/graph/graph.json or use an environment with networkx installed."
        ) from exc

    with tempfile.TemporaryDirectory() as tmp:
        payload = build(
            wiki_dir,
            Path(tmp) / "cache",
            Path(tmp) / "graph.json",
        )
    return payload.get("checkpoint_health", {})


def resolve_cluster_paths(wiki_dir: Path, node_ids: list[str]) -> list[Path]:
    paths: list[Path] = []
    for node_id in node_ids:
        path = wiki_dir / f"{node_id}.md"
        if path.exists():
            paths.append(path)
        else:
            LOG.warning("Skipping missing cluster page: %s", path)
    return paths


def collect_cluster_inputs(cluster_paths: list[Path]) -> tuple[list[str], list[str], Counter[str], Counter[str], dict[str, str]]:
    source_titles: list[str] = []
    raw_paths: list[str] = []
    concept_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    source_pages: dict[str, str] = {}

    for path in cluster_paths:
        fm, body = parse_frontmatter(path)
        title = str(fm.get("title") or path.stem.replace("-", " ").title())
        source_titles.append(title)
        source_pages[title] = body

        sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
        for raw_path in sources:
            if raw_path not in raw_paths:
                raw_paths.append(raw_path)

        concepts = fm.get("concepts") if isinstance(fm.get("concepts"), list) else []
        concept_counts.update(str(slug) for slug in concepts if str(slug).strip())

        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        tag_counts.update(str(tag) for tag in tags if str(tag).strip())

    return source_titles, raw_paths, concept_counts, tag_counts, source_pages


def resolve_compare_pages(wiki_dir: Path, concept_counts: Counter[str], source_pages: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    compare_pages: dict[str, str] = {}
    compare_labels: list[str] = []

    for slug, _ in concept_counts.most_common():
        for category in ("concepts", "entities"):
            candidate = wiki_dir / category / f"{slug}.md"
            if not candidate.exists():
                continue
            fm, body = parse_frontmatter(candidate)
            title = str(fm.get("title") or slug.replace("-", " ").title())
            if title in compare_pages:
                break
            compare_pages[title] = body
            compare_labels.append(title)
            break
        if len(compare_pages) >= MAX_COMPARE_PAGES:
            break

    if len(compare_pages) >= MIN_COMPARE_PAGES:
        return compare_pages, compare_labels

    for title, body in source_pages.items():
        if title in compare_pages:
            continue
        compare_pages[title] = body
        compare_labels.append(title)
        if len(compare_pages) >= MIN_COMPARE_PAGES:
            break

    return compare_pages, compare_labels


def build_synthesis_title(community: int, compare_labels: list[str]) -> str:
    if compare_labels:
        anchor = ", ".join(compare_labels[:3])
        return f"Recurring checkpoint patterns: {anchor}"
    return f"Recurring checkpoint patterns: Cluster {community}"


def ensure_unique_title(wiki_dir: Path, title: str, community: int) -> str:
    path = wiki_dir / "synthesis" / f"{slugify(title)}.md"
    if not path.exists():
        return title
    fallback = f"{title} (Cluster {community})"
    fallback_path = wiki_dir / "synthesis" / f"{slugify(fallback)}.md"
    if not fallback_path.exists():
        return fallback
    return f"{fallback} {datetime.now(timezone.utc).strftime('%H%M%S')}"


def render_question(source_titles: list[str], compare_labels: list[str]) -> str:
    focus = ", ".join(compare_labels[:3]) if compare_labels else "the shared themes"
    return (
        f"What recurring decisions, fixes, and durable patterns appear across the "
        f"{len(source_titles)} session checkpoints in this cluster, especially around {focus}?"
    )


def cluster_summary(
    community: int,
    cluster_paths: list[Path],
    source_titles: list[str],
    compare_labels: list[str],
    title: str,
) -> dict[str, Any]:
    return {
        "community": community,
        "checkpoint_count": len(cluster_paths),
        "checkpoint_paths": [str(path.relative_to(ROOT)) for path in cluster_paths],
        "source_titles": source_titles,
        "compare_pages": compare_labels,
        "title": title,
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path, default=ROOT / "wiki")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Limit clusters processed (0 = all)")
    parser.add_argument(
        "--community",
        action="append",
        type=int,
        default=[],
        help="Only process the given cluster community id (repeatable)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", "")),
        help="GitHub Models API token",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument(
        "--graph-path",
        type=Path,
        default=ROOT / "wiki" / "graph" / "graph.json",
        help="Existing graph artifact to read checkpoint_health from before rebuilding",
    )
    args = parser.parse_args()

    wiki_dir = args.wiki_dir.resolve()
    if not wiki_dir.is_dir():
        print(f"wiki dir not found: {wiki_dir}", file=sys.stderr)
        return 1

    checkpoint_health = load_checkpoint_health(wiki_dir, args.graph_path)
    clusters = list(checkpoint_health.get("merge_clusters", []))
    if args.community:
        wanted = set(args.community)
        clusters = [cluster for cluster in clusters if cluster.get("community") in wanted]
    if args.limit > 0:
        clusters = clusters[:args.limit]

    if not clusters:
        print("No merge clusters to process.")
        return 0

    if not args.dry_run and not args.token:
        print("No API token. Set GITHUB_MODELS_TOKEN or pass --token.", file=sys.stderr)
        return 1

    created_pages: list[str] = []
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "model": args.model,
        "cluster_count": len(clusters),
        "health_before": {
            "total_checkpoints": checkpoint_health.get("total_checkpoints", 0),
            "recommendations": checkpoint_health.get("recommendations", {}),
            "synthesis_neighbor_ratio": checkpoint_health.get("synthesis_neighbor_ratio", 0.0),
        },
        "clusters": [],
        "created_pages": created_pages,
    }

    for cluster in clusters:
        community = int(cluster.get("community", -1))
        cluster_paths = resolve_cluster_paths(wiki_dir, list(cluster.get("checkpoints", [])))
        source_titles, raw_paths, concept_counts, tag_counts, source_pages = collect_cluster_inputs(cluster_paths)
        compare_pages, compare_labels = resolve_compare_pages(wiki_dir, concept_counts, source_pages)

        title = ensure_unique_title(wiki_dir, build_synthesis_title(community, compare_labels), community)
        cluster_info = cluster_summary(community, cluster_paths, source_titles, compare_labels, title)
        cluster_info["raw_paths"] = raw_paths
        cluster_info["mode"] = "dry-run" if args.dry_run else "run"

        if len(compare_pages) < MIN_COMPARE_PAGES:
            cluster_info["status"] = "skipped"
            cluster_info["reason"] = "fewer than two comparable pages resolved"
            report["clusters"].append(cluster_info)
            continue

        if args.dry_run:
            cluster_info["status"] = "planned"
            report["clusters"].append(cluster_info)
            print(
                f"[dry-run] community={community} checkpoints={len(cluster_paths)} "
                f"compare={len(compare_pages)} -> {title}"
            )
            continue

        question = render_question(source_titles, compare_labels)
        synthesis = call_llm_synthesis(
            concept_pages=compare_pages,
            question=question,
            dimensions=DEFAULT_DIMENSIONS,
            token=args.token,
            model=args.model,
        )
        if not synthesis:
            cluster_info["status"] = "skipped"
            cluster_info["reason"] = "llm synthesis failed"
            report["clusters"].append(cluster_info)
            continue

        synthesis["title"] = title
        synthesis["question"] = question
        tags = sorted(
            {
                "copilot-session",
                "checkpoint-synthesis",
                "durable-knowledge",
                *[tag for tag, _ in tag_counts.most_common(8)],
            }
        )
        synthesis["tags"] = tags

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename, content = generate_synthesis_page(synthesis, raw_paths, source_titles, today)
        rel_path = f"wiki/synthesis/{filename}"
        out_path = ROOT / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        created_pages.append(rel_path)

        cluster_info["status"] = "created"
        cluster_info["output"] = rel_path
        report["clusters"].append(cluster_info)
        print(
            f"[created] community={community} checkpoints={len(cluster_paths)} "
            f"compare={len(compare_pages)} -> {rel_path}"
        )

    if not args.dry_run and created_pages:
        postprocess_created_pages(wiki_dir, created_pages, ROOT)
        append_log(
            wiki_dir / "log.md",
            {
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "operation": "checkpoint-cluster-synthesis",
                "targets": created_pages,
                "source": "plans/checkpoint-curation-phase5-report.md",
                "status": "success",
                "notes": "Backfill synthesis pages for checkpoint merge clusters",
            },
        )
        rebuild_index(ROOT)

    if args.report:
        write_report(args.report, report)

    print(
        f"Processed {len(clusters)} clusters; "
        f"created {len(created_pages)} synthesis page(s); dry_run={args.dry_run}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
