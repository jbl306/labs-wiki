"""labs-wiki knowledge graph builder.

Extracts nodes (wiki pages) and edges (wikilinks + type/tier co-occurrence) from
`wiki/**/*.md`, detects communities via greedy modularity, and persists
`graph.json` in node-link format suitable for Cosmograph / NetworkX reload.

Kept deliberately minimal and dependency-light:
  - NetworkX only (no leidenalg — greedy modularity is sub-second on <1k nodes).
  - No LLM calls. Edges come from explicit `[[wikilinks]]` and (optionally) from
    the Markdown body's same-tier references.
  - SHA256 per-page extraction cache so unchanged pages skip re-parsing.

Call ``build_graph(wiki_dir, cache_dir, out_path)`` to produce the artifact.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import logging
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

log = logging.getLogger("graph_builder")

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class Page:
    """A single wiki page extracted from a markdown file."""

    node_id: str           # relative path without extension, e.g. "concepts/rope"
    path: str              # relative path including extension
    title: str
    page_type: str         # concept | entity | source | synthesis | other
    tier: str              # hot | established | core | workflow | ""
    quality_score: float
    tags: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)  # target titles/slugs
    last_verified: str = ""
    summary: str = ""
    content_hash: str = ""
    checkpoint_class: str = ""   # durable-architecture | durable-debugging | project-progress | …
    retention_mode: str = ""     # retain | compress | archive


def _parse_frontmatter(text: str) -> dict[str, Any]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, Any] = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            out[key] = [p.strip().strip('"').strip("'") for p in inner.split(",") if p.strip()] if inner else []
        else:
            out[key] = value
    return out


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def parse_page(root: Path, md_path: Path) -> Page | None:
    """Parse a single markdown file into a Page, or return None on failure."""
    try:
        raw = md_path.read_text(encoding="utf-8")
    except OSError as e:
        log.warning("read failed %s: %s", md_path, e)
        return None

    fm = _parse_frontmatter(raw)
    body = _FRONTMATTER_RE.sub("", raw, count=1).strip()

    # node_id = relative path without extension, forward slashes
    rel = md_path.relative_to(root).with_suffix("")
    node_id = str(rel).replace("\\", "/")

    page_type = str(fm.get("type", "other")).strip() or "other"
    title = str(fm.get("title") or md_path.stem.replace("-", " ").title())
    tier = str(fm.get("tier", "")).strip()
    tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []

    try:
        quality = float(fm.get("quality_score", 0))
    except (TypeError, ValueError):
        quality = 0.0

    # Summary = first non-heading paragraph, capped.
    summary = ""
    for chunk in body.split("\n\n"):
        stripped = chunk.strip()
        if stripped and not stripped.startswith("#"):
            summary = stripped.replace("\n", " ")
            break
    if len(summary) > 240:
        summary = summary[:237] + "..."

    # Wikilinks come from BOTH the body AND any [[...]] inside the frontmatter
    # (notably the `related:` block-list). The primitive frontmatter parser
    # above only handles single-line YAML, so we just regex-scan the whole
    # frontmatter section for [[wikilinks]] — any duplication is deduped below.
    fm_text = _FRONTMATTER_RE.match(raw).group(1) if _FRONTMATTER_RE.match(raw) else ""
    body_links = _WIKILINK_RE.findall(body)
    fm_links = _WIKILINK_RE.findall(fm_text)
    seen: set[str] = set()
    wikilinks: list[str] = []
    for link in (*body_links, *fm_links):
        link = link.strip()
        if link and link not in seen:
            seen.add(link)
            wikilinks.append(link)

    content_hash = hashlib.sha256(raw.encode("utf-8", errors="ignore")).hexdigest()

    return Page(
        node_id=node_id,
        path=str(md_path.relative_to(root)).replace("\\", "/"),
        title=title,
        page_type=page_type,
        tier=tier,
        quality_score=quality,
        tags=[t for t in tags if isinstance(t, str)],
        wikilinks=wikilinks,
        last_verified=str(fm.get("last_verified", "")),
        summary=summary,
        content_hash=content_hash,
        checkpoint_class=str(fm.get("checkpoint_class", "")).strip(),
        retention_mode=str(fm.get("retention_mode", "")).strip(),
    )


# ---------------------------------------------------------------------------
# Extraction with cache
# ---------------------------------------------------------------------------

def _cache_path(cache_dir: Path, content_hash: str) -> Path:
    return cache_dir / f"{content_hash}.json"


def _page_to_cache_dict(p: Page) -> dict[str, Any]:
    return {
        "node_id": p.node_id,
        "path": p.path,
        "title": p.title,
        "page_type": p.page_type,
        "tier": p.tier,
        "quality_score": p.quality_score,
        "tags": p.tags,
        "wikilinks": p.wikilinks,
        "last_verified": p.last_verified,
        "summary": p.summary,
        "content_hash": p.content_hash,
        "checkpoint_class": p.checkpoint_class,
        "retention_mode": p.retention_mode,
    }


def _page_from_cache_dict(d: dict[str, Any]) -> Page:
    return Page(
        node_id=d["node_id"],
        path=d["path"],
        title=d["title"],
        page_type=d["page_type"],
        tier=d.get("tier", ""),
        quality_score=d.get("quality_score", 0.0),
        tags=d.get("tags", []),
        wikilinks=d.get("wikilinks", []),
        last_verified=d.get("last_verified", ""),
        summary=d.get("summary", ""),
        content_hash=d["content_hash"],
        checkpoint_class=d.get("checkpoint_class", ""),
        retention_mode=d.get("retention_mode", ""),
    )


def extract_pages(wiki_dir: Path, cache_dir: Path | None = None) -> tuple[list[Page], dict[str, int]]:
    """Walk `wiki_dir` for .md files, parse each, cache by content hash.

    Returns (pages, stats) where stats contains cache_hits / cache_misses / errors.
    """
    pages: list[Page] = []
    stats = Counter()

    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)

    for md in sorted(wiki_dir.rglob("*.md")):
        if md.name in {"index.md", "hot.md", "log.md"}:
            continue
        if "/.obsidian/" in str(md) or "/meta/" in str(md):
            continue

        # Hash the raw bytes first so we can skip parse on cache hit.
        try:
            raw = md.read_bytes()
        except OSError as e:
            log.warning("read failed %s: %s", md, e)
            stats["errors"] += 1
            continue
        content_hash = hashlib.sha256(raw).hexdigest()

        cache_file = _cache_path(cache_dir, content_hash) if cache_dir else None
        if cache_file and cache_file.exists():
            try:
                cached = json.loads(cache_file.read_text())
                pages.append(_page_from_cache_dict(cached))
                stats["cache_hits"] += 1
                continue
            except (OSError, json.JSONDecodeError, KeyError):
                pass  # fall through to re-parse

        page = parse_page(wiki_dir, md)
        if page is None:
            stats["errors"] += 1
            continue
        pages.append(page)
        stats["cache_misses"] += 1

        if cache_file:
            try:
                cache_file.write_text(json.dumps(_page_to_cache_dict(page)))
            except OSError as e:
                log.warning("cache write failed %s: %s", cache_file, e)

    return pages, dict(stats)


# ---------------------------------------------------------------------------
# Graph building
# ---------------------------------------------------------------------------

def _resolve_wikilink(target: str, by_title: dict[str, str], by_slug: dict[str, str]) -> str | None:
    """Resolve a [[wikilink]] target to a node_id. Returns None if unresolvable."""
    key = target.strip()
    if key in by_title:
        return by_title[key]
    slug = _slugify(key)
    if slug in by_slug:
        return by_slug[slug]
    # Also try matching the tail of a path, e.g. "rope" matches "concepts/rope".
    for node_id in by_slug.values():
        if node_id.rsplit("/", 1)[-1] == slug:
            return node_id
    return None


PUBLISHER_DEMOTION_WEIGHT = 0.1  # publisher entities are hosting hubs, not topical bridges
PUBLISHER_TAGS = {"publisher", "site", "platform", "host"}
PUBLISHER_NODE_TAILS = {
    "geeksforgeeks", "arxiv", "github", "youtube", "medium", "substack",
    "wikipedia", "reddit", "twitter", "x", "stackoverflow", "huggingface",
    "kaggle", "google-scholar", "papers-with-code",
}


def _is_publisher(page: Page) -> bool:
    """Identify entity pages that are publishers/hosts rather than topical concepts.

    These create false adjacency when the same publisher hosts many sources, and
    they distort community detection. We keep their edges but down-weight them so
    real topical edges dominate modularity-based clustering.
    """
    if page.page_type != "entity":
        return False
    tags_lower = {t.lower() for t in page.tags}
    if tags_lower & PUBLISHER_TAGS:
        return True
    tail = page.node_id.rsplit("/", 1)[-1].lower()
    return tail in PUBLISHER_NODE_TAILS


def build_graph(pages: list[Page]) -> nx.Graph:
    """Build an undirected NetworkX graph from extracted pages."""
    g = nx.Graph()

    by_title = {p.title: p.node_id for p in pages}
    by_slug = {_slugify(p.title): p.node_id for p in pages}
    # Also index by node_id tail for slug fallback.
    for p in pages:
        by_slug.setdefault(_slugify(p.node_id.rsplit("/", 1)[-1]), p.node_id)

    publisher_ids = {p.node_id for p in pages if _is_publisher(p)}

    for p in pages:
        g.add_node(
            p.node_id,
            title=p.title,
            page_type=p.page_type,
            tier=p.tier,
            quality_score=p.quality_score,
            tags=p.tags,
            path=p.path,
            summary=p.summary,
            last_verified=p.last_verified,
            is_publisher=p.node_id in publisher_ids,
            checkpoint_class=p.checkpoint_class,
            retention_mode=p.retention_mode,
        )

    for p in pages:
        for target in p.wikilinks:
            resolved = _resolve_wikilink(target, by_title, by_slug)
            if resolved and resolved != p.node_id:
                # Down-weight edges that touch a publisher entity — they are
                # hosting links, not topical bridges. Real concept↔concept edges
                # keep weight 1.0 and dominate community detection.
                edge_weight = (
                    PUBLISHER_DEMOTION_WEIGHT
                    if (p.node_id in publisher_ids or resolved in publisher_ids)
                    else 1.0
                )
                if g.has_edge(p.node_id, resolved):
                    g[p.node_id][resolved]["weight"] += edge_weight
                else:
                    g.add_edge(
                        p.node_id,
                        resolved,
                        weight=edge_weight,
                        confidence="EXTRACTED",
                        source="wikilink",
                    )

    return g


def detect_communities(g: nx.Graph) -> dict[str, int]:
    """Run greedy modularity; return {node_id: community_index}."""
    if g.number_of_nodes() == 0:
        return {}
    try:
        communities = list(greedy_modularity_communities(g, weight="weight"))
    except Exception as e:  # pragma: no cover — safety net, not a real code path
        log.warning("community detection failed: %s; falling back to connected components", e)
        communities = list(nx.connected_components(g))

    mapping: dict[str, int] = {}
    for idx, community in enumerate(communities):
        for node in community:
            mapping[node] = idx
    # Isolated nodes get their own singleton community so they still render.
    next_idx = len(communities)
    for node in g.nodes():
        if node not in mapping:
            mapping[node] = next_idx
            next_idx += 1
    return mapping


def analyze_graph(g: nx.Graph, communities: dict[str, int]) -> dict[str, Any]:
    """Compute god-nodes (top-degree) and surprises (cross-community edges)."""
    degrees = dict(g.degree())
    god_nodes = sorted(
        (
            {
                "node_id": n,
                "title": g.nodes[n].get("title", n),
                "degree": d,
                "community": communities.get(n, -1),
            }
            for n, d in degrees.items()
        ),
        key=lambda r: r["degree"],
        reverse=True,
    )[:15]

    surprises: list[dict[str, Any]] = []
    for u, v, data in g.edges(data=True):
        cu, cv = communities.get(u, -1), communities.get(v, -1)
        if cu != cv:
            surprises.append(
                {
                    "source": u,
                    "target": v,
                    "source_title": g.nodes[u].get("title", u),
                    "target_title": g.nodes[v].get("title", v),
                    "weight": data.get("weight", 1),
                    "confidence": data.get("confidence", "EXTRACTED"),
                    "source_community": cu,
                    "target_community": cv,
                }
            )
    surprises.sort(key=lambda r: r["weight"], reverse=True)

    community_sizes = Counter(communities.values())
    community_summary = [
        {"community": idx, "size": size}
        for idx, size in sorted(community_sizes.items(), key=lambda kv: kv[1], reverse=True)
    ]

    checkpoint_health = _checkpoint_health_report(g, communities)

    return {
        "god_nodes": god_nodes,
        "surprises": surprises[:50],
        "communities": community_summary,
        "checkpoint_health": checkpoint_health,
    }


_CHECKPOINT_TITLE_PREFIX = "Copilot Session Checkpoint"

# ---------------------------------------------------------------------------
# Heuristic baseline helpers
# ---------------------------------------------------------------------------

def _heuristic_recommendation(checkpoint_class: str, retention_mode: str) -> str:
    """Derive the heuristic editorial recommendation from frontmatter fields.

    Maps the existing curation policy to the same vocabulary used by the graph
    recommendation layer (keep / compress / archive).  When both fields are
    absent the checkpoint is treated as unclassified → compress (conservative).
    """
    if retention_mode == "retain":
        return "keep"
    if retention_mode == "compress":
        return "compress"
    if retention_mode == "archive":
        return "archive"
    # No retention_mode set — infer from checkpoint_class alone.
    if checkpoint_class.startswith("durable-"):
        return "keep"
    if checkpoint_class == "project-progress":
        return "compress"
    if checkpoint_class == "low-signal":
        return "archive"
    return "compress"  # conservative default for unclassified


def _checkpoint_health_report(
    g: nx.Graph, communities: dict[str, int]
) -> dict[str, Any]:
    """Score each Copilot session checkpoint by graph connectivity.

    For each checkpoint node, count neighbours by page_type and emit a
    recommendation:

    - ``keep``: well-connected to concepts/synthesis (degree>=4 and
      synthesis_neighbors>=1).
    - ``compress``: connected but no synthesis upstream — candidate for the
      archive tier so it stops surfacing in hot lists.
    - ``archive``: degree<=1 — the checkpoint is essentially orphaned.
    - ``merge``: concept-heavy (concept_neighbors>=2), no synthesis neighbor,
      AND the checkpoint belongs to a checkpoint community with at least 3
      members (itself + >=2 other checkpoints) — candidate for a synthesis page.

    ``merge`` is a pure structural graph signal.  The heuristic baseline never
    emits it, so graph-merge recommendations are tracked separately and are NOT
    counted in the heuristic-vs-graph disagreement metric.

    Returns a dict with per-checkpoint records plus aggregate counters.
    """
    checkpoints: list[dict[str, Any]] = []
    community_checkpoints: dict[int, list[str]] = {}

    # First pass: compute connectivity signals and tentative recommendations.
    # "merge" here is tentative — it is verified against community size in the
    # post-pass below.
    for node, data in g.nodes(data=True):
        title = data.get("title", "")
        if data.get("page_type") != "source":
            continue
        if not title.startswith(_CHECKPOINT_TITLE_PREFIX):
            continue

        neighbours = list(g.neighbors(node))
        by_type: Counter[str] = Counter()
        for nb in neighbours:
            by_type[g.nodes[nb].get("page_type", "other")] += 1

        degree = len(neighbours)
        synthesis_n = by_type.get("synthesis", 0)
        concept_n = by_type.get("concept", 0)
        source_n = by_type.get("source", 0)
        community = communities.get(node, -1)

        if degree <= 1:
            recommendation = "archive"
        elif synthesis_n >= 1 and degree >= 4:
            recommendation = "keep"
        elif concept_n >= 2 and synthesis_n == 0:
            recommendation = "merge"  # tentative; verified in post-pass
        else:
            recommendation = "compress"

        checkpoint_class = data.get("checkpoint_class", "")
        retention_mode = data.get("retention_mode", "")
        heuristic_rec = _heuristic_recommendation(checkpoint_class, retention_mode)

        community_checkpoints.setdefault(community, []).append(node)

        checkpoints.append(
            {
                "node_id": node,
                "title": title,
                "path": data.get("path", ""),
                "tier": data.get("tier", ""),
                "quality_score": data.get("quality_score", 0.0),
                "degree": degree,
                "synthesis_neighbors": synthesis_n,
                "concept_neighbors": concept_n,
                "source_neighbors": source_n,
                "community": community,
                "recommendation": recommendation,
                # Heuristic baseline from frontmatter
                "checkpoint_class": checkpoint_class,
                "retention_mode": retention_mode,
                "heuristic_recommendation": heuristic_rec,
                # Filled in the post-pass below
                "disagrees": False,
            }
        )

    # Post-pass 1: enforce community-size requirement for merge.
    # A checkpoint only gets "merge" if its community contains >= 3 checkpoints
    # (itself + at least 2 others).  Demote to "compress" when that is not met.
    cp_community_count = Counter(c["community"] for c in checkpoints)
    for c in checkpoints:
        if c["recommendation"] == "merge" and cp_community_count[c["community"]] < 3:
            c["recommendation"] = "compress"

    # Post-pass 2: compute disagreement flags and recommendation counts.
    # graph "merge" has no heuristic equivalent — counting it as a disagreement
    # would inflate the metric artificially.  It is excluded from disagrees.
    rec_counts: Counter[str] = Counter()
    disagreement_breakdown: Counter[str] = Counter()
    for c in checkpoints:
        rec = c["recommendation"]
        rec_counts[rec] += 1
        heuristic_rec = c["heuristic_recommendation"]
        disagrees = (heuristic_rec != rec) and (rec != "merge")
        c["disagrees"] = disagrees
        if disagrees:
            transition = f"{heuristic_rec}→{rec}"
            disagreement_breakdown[transition] += 1

    checkpoints.sort(key=lambda r: (r["recommendation"] != "archive", -r["degree"]))

    merge_clusters = [
        {"community": cid, "checkpoints": nodes}
        for cid, nodes in community_checkpoints.items()
        if len(nodes) >= 3
    ]

    return {
        "total_checkpoints": len(checkpoints),
        "recommendations": dict(rec_counts),
        "synthesis_neighbor_ratio": (
            round(
                sum(1 for c in checkpoints if c["synthesis_neighbors"] >= 1)
                / max(1, len(checkpoints)),
                3,
            )
        ),
        "disagreement_count": sum(1 for c in checkpoints if c["disagrees"]),
        "disagreement_breakdown": dict(disagreement_breakdown),
        "merge_clusters": merge_clusters,
        "checkpoints": checkpoints,
    }


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------

def to_node_link(
    g: nx.Graph,
    communities: dict[str, int],
    analysis: dict[str, Any],
    pages_by_id: dict[str, Page],
    extraction_stats: dict[str, int],
) -> dict[str, Any]:
    nodes = []
    for n, data in g.nodes(data=True):
        nodes.append(
            {
                "id": n,
                "title": data.get("title", n),
                "page_type": data.get("page_type", "other"),
                "tier": data.get("tier", ""),
                "quality_score": data.get("quality_score", 0.0),
                "tags": data.get("tags", []),
                "path": data.get("path", ""),
                "summary": data.get("summary", ""),
                "last_verified": data.get("last_verified", ""),
                "community": communities.get(n, -1),
                "degree": g.degree(n),
            }
        )

    edges = [
        {
            "source": u,
            "target": v,
            "weight": data.get("weight", 1),
            "confidence": data.get("confidence", "EXTRACTED"),
            "source_kind": data.get("source", "wikilink"),
            "cross_community": communities.get(u, -1) != communities.get(v, -1),
        }
        for u, v, data in g.edges(data=True)
    ]

    return {
        "generated_at": int(time.time()),
        "node_count": g.number_of_nodes(),
        "edge_count": g.number_of_edges(),
        "community_count": len(set(communities.values())) if communities else 0,
        "extraction_stats": extraction_stats,
        "nodes": nodes,
        "edges": edges,
        "god_nodes": analysis["god_nodes"],
        "surprises": analysis["surprises"],
        "communities": analysis["communities"],
        "checkpoint_health": analysis.get("checkpoint_health", {}),
    }


def write_checkpoint_tracker(health: dict[str, Any], out_path: Path) -> None:
    """Write a report-only markdown tracker for checkpoint graph recommendations.

    Compares the graph recommendation layer against the heuristic baseline from
    frontmatter (checkpoint_class + retention_mode) and surfaces disagreements.
    Does NOT modify any wiki page or retention setting.

    Graph ``merge`` is a structural signal (checkpoint belongs to a community
    with ≥ 3 checkpoints AND has concept_neighbors≥2 with no synthesis
    neighbor).  The heuristic baseline never emits ``merge``, so it is shown
    separately and excluded from the heuristic-vs-graph disagreement count.
    """
    checkpoints: list[dict[str, Any]] = health.get("checkpoints", [])
    total = health.get("total_checkpoints", len(checkpoints))
    recs: dict[str, int] = health.get("recommendations", {})
    disagree_count: int = health.get("disagreement_count", 0)
    disagree_breakdown: dict[str, int] = health.get("disagreement_breakdown", {})
    merge_clusters: list[dict[str, Any]] = health.get("merge_clusters", [])
    generated_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        "# Checkpoint Graph Tracker",
        "",
        "> **Report-only.** This file is auto-generated on every graph build.",
        "> It does not rewrite retention settings, tier values, or checkpoint",
        "> frontmatter. Its purpose is to surface disagreements between the",
        "> heuristic classifier and the graph recommendation layer so they can",
        "> be evaluated before any policy change is made.",
        "",
        f"**Generated:** {generated_ts}  ",
        f"**Total checkpoints:** {total}  ",
        "",
        "## Graph recommendation counts",
        "",
        "| Recommendation | Count |",
        "| --- | --- |",
    ]
    for rec in ("keep", "compress", "merge", "archive"):
        lines.append(f"| `{rec}` | {recs.get(rec, 0)} |")
    lines += [
        "",
        "## Disagreement summary",
        "",
        "> **Note:** Graph `merge` is a structural signal (checkpoint community ≥ 3 members,",
        "> concept-connected, no synthesis neighbor). The heuristic baseline never emits `merge`,",
        "> so graph-`merge` checkpoints are shown separately below and are **not** counted here.",
        "",
        f"**Disagreements (excluding merge):** {disagree_count} of {total}",
        "",
    ]
    if disagree_breakdown:
        lines += [
            "| Transition (heuristic→graph) | Count |",
            "| --- | --- |",
        ]
        for transition, count in sorted(disagree_breakdown.items(), key=lambda kv: -kv[1]):
            lines.append(f"| `{transition}` | {count} |")
    else:
        lines.append("_No disagreements detected._")
    lines += [""]

    # Disagreement detail table (excludes merge).
    disagreements = [c for c in checkpoints if c.get("disagrees")]
    if disagreements:
        lines += [
            "## Disagreement detail",
            "",
            "| Title | Path | Class | Retention | Heuristic rec | Graph rec | Degree | Concept nb | Synth nb | Tier |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for c in sorted(disagreements, key=lambda r: r.get("title", "")):
            title = c.get("title", "").replace("|", "\\|")
            path = c.get("path", "")
            cls = c.get("checkpoint_class", "")
            ret = c.get("retention_mode", "")
            hrec = c.get("heuristic_recommendation", "")
            grec = c.get("recommendation", "")
            deg = c.get("degree", 0)
            cnb = c.get("concept_neighbors", 0)
            snb = c.get("synthesis_neighbors", 0)
            tier = c.get("tier", "")
            lines.append(f"| {title} | `{path}` | {cls} | {ret} | `{hrec}` | `{grec}` | {deg} | {cnb} | {snb} | {tier} |")
        lines.append("")

    # Merge-signal checkpoints (separate from disagreements).
    merge_flagged = [c for c in checkpoints if c.get("recommendation") == "merge"]
    if merge_flagged:
        lines += [
            "## Merge-signal checkpoints",
            "",
            "> Structural candidates for a synthesis page: concept-connected (concept_nb ≥ 2),",
            "> no synthesis neighbor, and in a checkpoint community of ≥ 3 members.",
            "> These are not counted in the disagreement metric above.",
            "",
            "| Title | Path | Class | Community | Degree | Concept nb | Tier |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for c in sorted(merge_flagged, key=lambda r: r.get("title", "")):
            title = c.get("title", "").replace("|", "\\|")
            path = c.get("path", "")
            cls = c.get("checkpoint_class", "")
            comm = c.get("community", "")
            deg = c.get("degree", 0)
            cnb = c.get("concept_neighbors", 0)
            tier = c.get("tier", "")
            lines.append(f"| {title} | `{path}` | {cls} | {comm} | {deg} | {cnb} | {tier} |")
        lines.append("")

    # Merge-cluster candidates.
    lines += [
        "## Merge-cluster candidates",
        "",
    ]
    if merge_clusters:
        lines += [
            "Communities with ≥ 3 checkpoints are candidates for a synthesis page.",
            "",
            "| Community | Checkpoint node IDs |",
            "| --- | --- |",
        ]
        for mc in merge_clusters:
            nodes_str = ", ".join(f"`{n}`" for n in mc.get("checkpoints", []))
            lines.append(f"| {mc.get('community', '')} | {nodes_str} |")
    else:
        lines.append("_No merge-cluster candidates (no community contains ≥ 3 checkpoints)._")
    lines += [""]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


def build(
    wiki_dir: Path,
    cache_dir: Path | None,
    out_path: Path,
    tracker_path: Path | None = None,
) -> dict[str, Any]:
    """Full pipeline: extract → build graph → detect communities → analyze → write.

    Returns the serialised node-link dict (also written to `out_path`).
    If ``tracker_path`` is given, also writes reports/checkpoint-graph-tracker.md
    relative to repo root.  When omitted, the default resolves to
    ``<wiki_dir parent>/reports/checkpoint-graph-tracker.md``.
    """
    t0 = time.time()
    pages, stats = extract_pages(wiki_dir, cache_dir)
    log.info("extracted %d pages (%s)", len(pages), stats)

    g = build_graph(pages)
    log.info("graph: %d nodes, %d edges", g.number_of_nodes(), g.number_of_edges())

    communities = detect_communities(g)
    analysis = analyze_graph(g, communities)

    pages_by_id = {p.node_id: p for p in pages}
    payload = to_node_link(g, communities, analysis, pages_by_id, stats)
    payload["build_seconds"] = round(time.time() - t0, 3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2))
    log.info(
        "wrote %s in %.2fs (%d nodes, %d edges, %d communities)",
        out_path,
        payload["build_seconds"],
        payload["node_count"],
        payload["edge_count"],
        payload["community_count"],
    )

    # Write the checkpoint-graph tracker report.
    # Default: repo-root/reports/checkpoint-graph-tracker.md (wiki_dir.parent is repo root).
    resolved_tracker = tracker_path or wiki_dir.parent / "reports" / "checkpoint-graph-tracker.md"
    write_checkpoint_tracker(payload.get("checkpoint_health", {}), resolved_tracker)
    log.info("wrote checkpoint tracker %s", resolved_tracker)

    return payload


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Build the labs-wiki knowledge graph.")
    ap.add_argument("--wiki", default="wiki", help="Path to wiki/ root")
    ap.add_argument("--cache", default=".graph_cache", help="Extraction cache directory")
    ap.add_argument("--out", default="wiki/graph/graph.json", help="Output graph.json path")
    ap.add_argument("--tracker", default=None, help="Path for checkpoint-graph-tracker.md (default: reports/checkpoint-graph-tracker.md relative to repo root)")
    args = ap.parse_args()

    tracker = Path(args.tracker) if args.tracker else None
    build(Path(args.wiki), Path(args.cache), Path(args.out), tracker_path=tracker)
