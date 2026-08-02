#!/usr/bin/env python3
"""Generate synthesis pages for backlog checkpoint merge clusters.

This is the Phase 5 follow-up batch for the pre-existing checkpoint corpus.
It reuses the synthesis helpers from ``auto_ingest.py`` but drives them from
the current graph's ``checkpoint_health.merge_clusters`` instead of waiting for
new ingests to trigger Phase 3 family synthesis.
"""

from __future__ import annotations

import argparse
import hashlib
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


def collect_cluster_inputs(
    cluster_paths: list[Path],
) -> tuple[list[str], list[str], Counter[str], Counter[str], dict[str, tuple[str, list[str]]]]:
    source_titles: list[str] = []
    raw_paths: list[str] = []
    concept_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    source_pages: dict[str, tuple[str, list[str]]] = {}

    for path in cluster_paths:
        fm, body = parse_frontmatter(path)
        title = str(fm.get("title") or path.stem.replace("-", " ").title())
        source_titles.append(title)

        sources_value = fm.get("sources")
        sources = list(sources_value) if isinstance(sources_value, list) else []
        normalized_sources = [str(source) for source in sources if str(source).strip()]
        source_pages[title] = (body, normalized_sources)
        for raw_path in normalized_sources:
            if raw_path not in raw_paths:
                raw_paths.append(raw_path)

        concepts = fm.get("concepts") if isinstance(fm.get("concepts"), list) else []
        concept_counts.update(str(slug) for slug in concepts if str(slug).strip())

        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        tag_counts.update(str(tag) for tag in tags if str(tag).strip())

    return source_titles, raw_paths, concept_counts, tag_counts, source_pages


def resolve_compare_pages(
    wiki_dir: Path,
    concept_counts: Counter[str],
    source_pages: dict[str, tuple[str, list[str]]],
) -> tuple[dict[str, str], list[str], list[str], dict[str, list[str]]]:
    compare_pages: dict[str, str] = {}
    compare_labels: list[str] = []
    evidence_raw_paths: list[str] = []
    source_provenance: dict[str, list[str]] = {}

    def add_evidence_sources(label: str, sources: object) -> None:
        if not isinstance(sources, list):
            return
        page_sources: list[str] = []
        for source in sources:
            source_text = str(source).strip()
            if not source_text.startswith("raw/"):
                continue
            if source_text not in evidence_raw_paths:
                evidence_raw_paths.append(source_text)
            if source_text not in page_sources:
                page_sources.append(source_text)
        source_provenance[label] = page_sources

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
            add_evidence_sources(title, fm.get("sources"))
            break
        if len(compare_pages) >= MAX_COMPARE_PAGES:
            break

    if len(compare_pages) >= MIN_COMPARE_PAGES:
        return compare_pages, compare_labels, evidence_raw_paths, source_provenance

    for title, (body, sources) in source_pages.items():
        if title in compare_pages:
            continue
        compare_pages[title] = body
        compare_labels.append(title)
        add_evidence_sources(title, sources)
        if len(compare_pages) >= MIN_COMPARE_PAGES:
            break

    return compare_pages, compare_labels, evidence_raw_paths, source_provenance


def strict_synthesis_gate(page_path: Path, repo_root: Path = ROOT) -> tuple[bool, str]:
    """Apply the deterministic strict contract before accepting a generated page."""
    from audit_synthesis import audit_page

    result = audit_page(page_path, repo_root, strict=True)
    if result.passed:
        return True, ""
    codes = ", ".join(finding.code for finding in result.findings)
    return False, f"strict audit failed: score={result.score}; findings={codes}"


def truncate_title(text: str, max_length: int = 100) -> str:
    """Trim a generated title at a word boundary without leaving punctuation."""
    if len(text) <= max_length:
        return text
    shortened = text[: max_length + 1].rsplit(" ", 1)[0].rstrip(" :,-")
    return shortened or text[:max_length].rstrip(" :,-")


def build_synthesis_title(community: int, compare_labels: list[str]) -> str:
    if len(compare_labels) >= 2:
        return truncate_title(f"{compare_labels[0]} vs. {compare_labels[1]}: Shared Patterns and Trade-offs")
    if compare_labels:
        return truncate_title(f"Durable Patterns Around {compare_labels[0]}")
    return f"Cross-Checkpoint Synthesis for Community {community}"


def ensure_unique_title(wiki_dir: Path, title: str, community: int) -> str:
    path = wiki_dir / "synthesis" / f"{slugify(title)}.md"
    if not path.exists():
        return title
    fallback = f"{title} (Cluster {community})"
    fallback_path = wiki_dir / "synthesis" / f"{slugify(fallback)}.md"
    if not fallback_path.exists():
        return fallback
    return f"{fallback} {datetime.now(timezone.utc).strftime('%H%M%S')}"


def build_cluster_signature(raw_paths: list[str]) -> str:
    payload = "checkpoint-cluster:v2\n" + "\n".join(sorted(raw_paths))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def load_existing_cluster_syntheses(wiki_dir: Path) -> list[dict[str, Any]]:
    synth_dir = wiki_dir / "synthesis"
    if not synth_dir.is_dir():
        return []

    pages: list[dict[str, Any]] = []
    for path in sorted(synth_dir.glob("*.md")):
        fm, _ = parse_frontmatter(path)
        title = str(fm.get("title") or path.stem)
        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        tags_lower = {str(tag).strip().lower() for tag in tags}
        if not title.lower().startswith("recurring checkpoint patterns:") and "checkpoint-synthesis" not in tags_lower:
            continue
        sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
        if not sources:
            continue
        raw_community = str(fm.get("checkpoint_cluster_community", "")).strip()
        community = int(raw_community) if raw_community.lstrip("-").isdigit() else None
        pages.append(
            {
                "path": path,
                "community": community,
                "signature": str(fm.get("checkpoint_cluster_signature", "")).strip(),
                "sources": [str(source) for source in sources],
            }
        )
    return pages


def find_existing_cluster_synthesis(
    existing_pages: list[dict[str, Any]],
    community: int,
    raw_paths: list[str],
) -> tuple[dict[str, Any], str] | None:
    desired_sources = sorted(raw_paths)
    desired_signature = build_cluster_signature(raw_paths)
    for page in existing_pages:
        if page["signature"] and page["signature"] == desired_signature:
            return page, "signature"
        if sorted(page["sources"]) == desired_sources:
            return page, "sources"
    return None


def stamp_cluster_metadata(
    page_path: Path,
    community: int,
    checkpoint_count: int,
    raw_paths: list[str],
) -> bool:
    content = page_path.read_text()
    if not content.startswith("---"):
        return False

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    frontmatter_lines = parts[1].strip().split("\n")
    body = parts[2]
    desired = {
        "checkpoint_cluster_community": str(community),
        "checkpoint_cluster_checkpoint_count": str(checkpoint_count),
        "checkpoint_cluster_signature": build_cluster_signature(raw_paths),
    }

    def upsert(lines: list[str], key: str, value: str) -> list[str]:
        prefix = f"{key}:"
        for idx, line in enumerate(lines):
            if line.strip().startswith(prefix):
                lines[idx] = f"{key}: {value}"
                return lines
        insert_at = len(lines)
        for idx, line in enumerate(lines):
            if line.strip().startswith("tags:"):
                insert_at = idx
                break
        lines.insert(insert_at, f"{key}: {value}")
        return lines

    updated_lines = list(frontmatter_lines)
    for key, value in desired.items():
        updated_lines = upsert(updated_lines, key, value)

    normalized = "---\n" + "\n".join(updated_lines) + "\n---" + body
    if normalized == content:
        return False
    page_path.write_text(normalized)
    return True


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
    existing_syntheses = load_existing_cluster_syntheses(wiki_dir)
    llm_needed = False
    if not args.dry_run:
        preflight_consumed_paths: set[Path] = set()
        for cluster in clusters:
            community = int(cluster.get("community", -1))
            cluster_paths = resolve_cluster_paths(wiki_dir, list(cluster.get("checkpoints", [])))
            _, raw_paths, _, _, _ = collect_cluster_inputs(cluster_paths)
            match = find_existing_cluster_synthesis(existing_syntheses, community, raw_paths)
            if match and match[0]["path"] not in preflight_consumed_paths:
                preflight_consumed_paths.add(match[0]["path"])
            else:
                llm_needed = True
                break
        if llm_needed and not args.token:
            print("No API token. Set GITHUB_MODELS_TOKEN or pass --token.", file=sys.stderr)
            return 1

    consumed_existing_paths: set[Path] = set()
    for cluster in clusters:
        community = int(cluster.get("community", -1))
        cluster_paths = resolve_cluster_paths(wiki_dir, list(cluster.get("checkpoints", [])))
        source_titles, raw_paths, concept_counts, tag_counts, source_pages = collect_cluster_inputs(cluster_paths)
        compare_pages, compare_labels, evidence_raw_paths, source_provenance = resolve_compare_pages(
            wiki_dir, concept_counts, source_pages
        )

        title = ensure_unique_title(wiki_dir, build_synthesis_title(community, compare_labels), community)
        cluster_info = cluster_summary(community, cluster_paths, source_titles, compare_labels, title)
        cluster_info["raw_paths"] = raw_paths
        cluster_info["signature"] = build_cluster_signature(raw_paths)
        cluster_info["mode"] = "dry-run" if args.dry_run else "run"

        existing = find_existing_cluster_synthesis(existing_syntheses, community, raw_paths)
        if existing and existing[0]["path"] in consumed_existing_paths:
            existing = None
        if existing:
            existing_page, matched_by = existing
            consumed_existing_paths.add(existing_page["path"])
            rel_path = str(existing_page["path"].relative_to(ROOT))
            cluster_info["status"] = "existing"
            cluster_info["matched_by"] = matched_by
            cluster_info["output"] = rel_path
            if not args.dry_run:
                cluster_info["metadata_updated"] = stamp_cluster_metadata(
                    existing_page["path"],
                    community,
                    len(cluster_paths),
                    raw_paths,
                )
            report["clusters"].append(cluster_info)
            print(
                f"[existing] community={community} checkpoints={len(cluster_paths)} "
                f"matched_by={matched_by} -> {rel_path}"
            )
            continue

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

        # `compare_pages` is the complete bounded packet supplied to the model.
        # Do not present every checkpoint in the broader graph cluster as model
        # evidence: that would make frontmatter breadth exceed actual context.
        if not evidence_raw_paths:
            cluster_info["status"] = "skipped"
            cluster_info["reason"] = "model evidence packet has no raw provenance"
            report["clusters"].append(cluster_info)
            continue

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename, content = generate_synthesis_page(
            synthesis,
            evidence_raw_paths,
            compare_labels,
            today,
            extra_frontmatter={
                "checkpoint_cluster_community": str(community),
                "checkpoint_cluster_checkpoint_count": str(len(cluster_paths)),
                "checkpoint_cluster_signature": cluster_info["signature"],
                "checkpoint_cluster_evidence_input_count": str(len(compare_pages)),
            },
            source_provenance=source_provenance,
        )
        rel_path = f"wiki/synthesis/{filename}"
        out_path = ROOT / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        audit_passed, audit_reason = strict_synthesis_gate(out_path, ROOT)
        if not audit_passed:
            out_path.unlink(missing_ok=True)
            cluster_info["status"] = "skipped"
            cluster_info["reason"] = audit_reason
            report["clusters"].append(cluster_info)
            print(f"[skipped] community={community}: {audit_reason}")
            continue
        created_pages.append(rel_path)
        existing_syntheses.append(
            {
                "path": out_path,
                "community": community,
                "signature": cluster_info["signature"],
                "sources": list(raw_paths),
            }
        )

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
                "agent": f"github-models:{args.model}",
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
