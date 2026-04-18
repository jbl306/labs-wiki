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
    - ``merge``: shares a community with >=2 other checkpoints AND overlaps on
      concept neighbours — candidate for a synthesis page.

    Returns a dict with per-checkpoint records plus aggregate counters.
    """
    checkpoints: list[dict[str, Any]] = []
    rec_counts: Counter[str] = Counter()
    community_checkpoints: dict[int, list[str]] = {}

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
            recommendation = "merge"
        else:
            recommendation = "compress"

        rec_counts[recommendation] += 1
        community_checkpoints.setdefault(community, []).append(node)

        checkpoints.append(
            {
                "node_id": node,
                "title": title,
                "tier": data.get("tier", ""),
                "quality_score": data.get("quality_score", 0.0),
                "degree": degree,
                "synthesis_neighbors": synthesis_n,
                "concept_neighbors": concept_n,
                "source_neighbors": source_n,
                "community": community,
                "recommendation": recommendation,
            }
        )

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


def build(
    wiki_dir: Path,
    cache_dir: Path | None,
    out_path: Path,
) -> dict[str, Any]:
    """Full pipeline: extract → build graph → detect communities → analyze → write.

    Returns the serialised node-link dict (also written to `out_path`).
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
    return payload


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Build the labs-wiki knowledge graph.")
    ap.add_argument("--wiki", default="wiki", help="Path to wiki/ root")
    ap.add_argument("--cache", default=".graph_cache", help="Extraction cache directory")
    ap.add_argument("--out", default="wiki/graph/graph.json", help="Output graph.json path")
    args = ap.parse_args()

    build(Path(args.wiki), Path(args.cache), Path(args.out))
