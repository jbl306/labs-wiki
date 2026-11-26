"""wiki-graph-api — FastAPI service exposing the labs-wiki knowledge graph.

Endpoints:
    GET  /health                 — liveness
    GET  /graph/stats            — node/edge/community counts, last rebuild ts
    GET  /graph/nodes/{id}       — full node record
    GET  /graph/neighbors/{id}   — neighbours up to depth N (default 1)
    GET  /graph/communities      — community summary
    GET  /graph/god-nodes        — top-degree "load-bearing" nodes
    GET  /graph/surprises        — cross-community edges
    GET  /graph/export/json      — raw node-link JSON
    GET  /graph/rebuild          — admin-gated full rebuild
    POST /internal/rebuild       — watcher webhook (admin-gated, Docker-network-only)
    GET  /events                 — SSE stream; emits `graph-updated` after each rebuild

Security:
    `X-Admin-Token` header required for rebuild endpoints.
    Caddy additionally blocks `/internal/*` and `/graph/rebuild` at the edge for
    anything reaching the public hostname — see compose.wiki-graph.yml.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import time
from collections import Counter
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse

from graph_builder import (
    EMBEDDING_FIELD,
    atomic_write_text,
    build as build_graph_artifact,
    compute_node_embeddings,
    compute_wiki_signature,
    embed_query,
)

log = logging.getLogger("wiki-graph-api")

WIKI_PATH = Path(os.environ.get("WIKI_PATH", "/app/wiki"))
CACHE_DIR = Path(os.environ.get("CACHE_DIR", "/data/cache"))
GRAPH_PATH = Path(os.environ.get("GRAPH_PATH", "/data/graph.json"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
# R17 — checkpoint tracker markdown path. The graph builder writes this on
# every rebuild via reports/checkpoint-graph-tracker.md (relative to repo
# root). The default resolves the repo root from WIKI_PATH's parent.
TRACKER_PATH = Path(
    os.environ.get(
        "CHECKPOINT_TRACKER_PATH",
        str(WIKI_PATH.parent / "reports" / "checkpoint-graph-tracker.md"),
    )
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _receipt_path() -> Path:
    return GRAPH_PATH.with_suffix(".build-receipt.json")


def _publication_marker() -> tuple[int, int, int] | None:
    try:
        stat = (WIKI_PATH / "graph" / "graph.json").stat()
    except FileNotFoundError:
        return None
    return stat.st_ino, stat.st_mtime_ns, stat.st_size


# Page-only repairs may leave the published artifact unchanged. Periodically
# verify its source tree as well as watching the ingest publication marker.
PUBLICATION_POLL_SECONDS = 15
SOURCE_CHECK_SECONDS = 300


class GraphState:
    """In-memory graph snapshot; refreshed on rebuild."""

    def __init__(self) -> None:
        self.payload: dict[str, Any] = {}
        self.nodes_by_id: dict[str, dict[str, Any]] = {}
        self.adjacency: dict[str, list[dict[str, Any]]] = {}
        self.overview: tuple[bytes, str] | None = None
        self.receipt: dict[str, Any] | None = None
        self.observed_source_signature: str | None = None
        self.checked_at: str | None = None
        self.sync_status = "unknown"
        self.sync_error: str | None = None
        self._checked_monotonic = 0.0
        self._published_marker: tuple[int, int, int] | None = None
        self._lock = asyncio.Lock()
        self._subscribers: set[asyncio.Queue[str]] = set()

    def load_from_disk(self) -> bool:
        try:
            payload = json.loads(GRAPH_PATH.read_text())
            self._install(payload)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            log.warning("cannot load graph snapshot %s: %s", GRAPH_PATH, exc)
            return False
        self.receipt = None
        try:
            receipt = json.loads(_receipt_path().read_text())
            if (
                isinstance(receipt, dict)
                and receipt.get("source_signature") == payload.get("source_signature")
                and isinstance(receipt.get("built_at"), str)
                and isinstance(receipt.get("build_seconds"), (int, float))
                and isinstance(receipt.get("source_counts"), dict)
            ):
                self.receipt = receipt
        except (OSError, ValueError) as exc:
            log.info("no usable build receipt: %s", exc)
        return True

    def _install(self, payload: dict[str, Any]) -> None:
        if not isinstance(payload, dict) or not isinstance(payload.get("nodes"), list):
            raise ValueError("graph has no node list")
        nodes = payload["nodes"]
        nodes_by_id = {node["id"]: node for node in nodes}
        if len(nodes_by_id) != len(nodes) or len(nodes) != payload.get("node_count"):
            raise ValueError("graph node count mismatch")
        adjacency: dict[str, list[dict[str, Any]]] = {nid: [] for nid in nodes_by_id}
        for edge in payload["edges"]:
            source, target = edge["source"], edge["target"]
            adjacency[source].append({"neighbor": target, **edge})
            adjacency[target].append({"neighbor": source, **edge})
        # The map only needs layout, searchable metadata and the edge endpoints.
        # Build its wire representation once, from this same snapshot.
        fields = ("id", "title", "page_type", "tier", "tags", "last_verified",
                  "checkpoint_class", "retention_mode", "community", "degree", "x", "y")
        map_nodes = [{key: node[key] for key in fields if key in node} for node in nodes]
        for node, compact in zip(nodes, map_nodes):
            if node.get("path") and node["path"] != node["id"] + ".md":
                compact["path"] = node["path"]
        indices = {node["id"]: i for i, node in enumerate(nodes)}
        links = [[indices[e["source"]], indices[e["target"]], bool(e.get("cross_community"))]
                 for e in payload["edges"]]
        overview = JSONResponse({"nodes": map_nodes, "links": links}).body
        etag = '"' + hashlib.sha256(overview).hexdigest() + '"'
        self._refresh_query_embeddings(payload)
        self.overview = (overview, etag)
        self.payload = payload
        self.nodes_by_id = nodes_by_id
        self.adjacency = adjacency

    def _refresh_query_embeddings(self, payload: dict[str, Any]) -> None:
        """Restore the query backend before making the snapshot available."""
        nodes = payload["nodes"]
        embeddings, backend = compute_node_embeddings(nodes, CACHE_DIR)
        for node in nodes:
            vec = embeddings.get(node.get("id"))
            if vec is None:
                node.pop(EMBEDDING_FIELD, None)
            else:
                node[EMBEDDING_FIELD] = vec
        payload["embedding_backend"] = backend
        log.info("query embeddings ready: backend=%s vectors=%d", backend, len(embeddings))

    async def _build_from_source(self, signature: str) -> dict[str, Any]:
        self.sync_status = "rebuilding"
        started = time.monotonic()
        payload = await asyncio.to_thread(
            build_graph_artifact, WIKI_PATH, CACHE_DIR, GRAPH_PATH,
            tracker_path=TRACKER_PATH, expected_source_signature=signature,
        )
        counts = Counter(node["page_type"] for node in payload["nodes"])
        receipt = {
            "built_at": _utc_now(),
            "build_seconds": time.monotonic() - started,
            "source_signature": signature,
            "source_revision": None,  # Mounted pages can change independently of the image.
            "source_counts": {
                "wiki_pages": len(payload["nodes"]),
                "by_page_type": dict(sorted(counts.items())),
            },
        }
        atomic_write_text(_receipt_path(), json.dumps(receipt, indent=2))
        self._install(payload)
        self.receipt = receipt
        await self._broadcast("graph-updated")
        return payload

    async def rebuild(self, *, if_due: bool = False) -> dict[str, Any]:
        async with self._lock:
            try:
                # Read the publication marker before scanning. If ingest
                # publishes again during the scan, the next poll sees it.
                marker = _publication_marker()
                if (
                    if_due and self.sync_status == "current"
                    and marker == self._published_marker
                    and time.monotonic() - self._checked_monotonic < SOURCE_CHECK_SECONDS
                ):
                    return {"rebuild_skipped": True, **self.payload}

                self.sync_status = "checking"
                self.observed_source_signature = None
                signature = await asyncio.to_thread(compute_wiki_signature, WIKI_PATH)
                self.observed_source_signature = signature
                self.checked_at = _utc_now()
                if (
                    self.receipt and "broken_link_count" in self.payload
                    and self.payload.get("source_signature") == signature
                    and TRACKER_PATH.is_file()
                ):
                    result = {"rebuild_skipped": True, **self.payload}
                else:
                    result = await self._build_from_source(signature)
                self._published_marker = marker
                self._checked_monotonic = time.monotonic()
                self.sync_status = "current"
                self.sync_error = None
                return result
            except Exception as exc:
                self.sync_status = "error"
                self.sync_error = str(exc)
                raise

    async def poll_publication(self) -> None:
        while True:
            await asyncio.sleep(PUBLICATION_POLL_SECONDS)
            try:
                await self.rebuild(if_due=True)
            except Exception:
                log.exception("graph refresh failed; will retry")

    async def subscribe(self) -> asyncio.Queue[str]:
        q: asyncio.Queue[str] = asyncio.Queue(maxsize=16)
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[str]) -> None:
        self._subscribers.discard(q)

    async def _broadcast(self, event: str) -> None:
        for q in list(self._subscribers):
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                log.warning("SSE subscriber queue full; dropping event")


state = GraphState()

app = FastAPI(
    title="wiki-graph-api",
    description="labs-wiki knowledge graph service",
    version="0.1.0",
)

# CORS: echo the request origin rather than "*" — required because the UI sends
# credentialed fetches (Cloudflare Access CF_Authorization cookie). "*" +
# credentials is rejected by browsers per the Fetch spec.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def _require_admin(token: str | None) -> None:
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN not configured")
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="admin token mismatch")


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def _startup() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if state.load_from_disk():
        log.info(
            "loaded graph from %s (%d nodes, %d edges)",
            GRAPH_PATH,
            state.payload.get("node_count", 0),
            state.payload.get("edge_count", 0),
        )
    try:
        # Verify the mounted source even when the persistent graph volume loads.
        await state.rebuild()
    except Exception:
        log.exception("initial graph refresh failed; will retry")
    app.state.graph_poll = asyncio.create_task(state.poll_publication())


@app.on_event("shutdown")
async def _shutdown() -> None:
    app.state.graph_poll.cancel()
    with suppress(asyncio.CancelledError):
        await app.state.graph_poll


# ---------------------------------------------------------------------------
# Public read endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok" if state.nodes_by_id else "empty",
        "nodes": len(state.nodes_by_id),
        "edges": state.payload.get("edge_count", 0),
    }


@app.get("/graph/stats")
def graph_stats() -> dict[str, Any]:
    receipt = state.receipt or {}
    content_time = state.payload.get("generated_at")
    return {
        "node_count": state.payload.get("node_count", 0),
        "edge_count": state.payload.get("edge_count", 0),
        "communities": state.payload.get("community_count", 0),
        "last_rebuild": receipt.get("built_at"),
        "build_seconds": receipt.get("build_seconds"),
        "build_receipt": state.receipt,
        "content_as_of": datetime.fromtimestamp(content_time, timezone.utc).isoformat() if content_time else None,
        "source_signature": state.payload.get("source_signature"),
        "observed_source_signature": state.observed_source_signature,
        "sync_status": state.sync_status,
        "checked_at": state.checked_at,
        "sync_error": state.sync_error,
        "extraction": state.payload.get("extraction_stats", {}),
    }


@app.get("/graph/nodes/{node_id:path}")
def graph_node(node_id: str) -> dict[str, Any]:
    node = state.nodes_by_id.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"unknown node {node_id}")
    return node


@app.get("/graph/page/{node_id:path}")
def graph_page(node_id: str) -> dict[str, Any]:
    """Return the raw markdown body of a wiki page for in-graph preview.

    The node's `path` field is trusted because it was populated by the graph
    builder from filesystem walks under WIKI_PATH. We still resolve it
    relative to WIKI_PATH and verify the resolved path stays inside the
    wiki root before reading, defending against a poisoned graph.json.
    """
    node = state.nodes_by_id.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"unknown node {node_id}")
    rel = (node.get("path") or "").strip()
    if not rel:
        raise HTTPException(status_code=404, detail="node has no path")
    try:
        target = (WIKI_PATH / rel).resolve()
        wiki_root = WIKI_PATH.resolve()
        target.relative_to(wiki_root)
    except (ValueError, OSError):
        raise HTTPException(status_code=400, detail="invalid path")
    if not target.is_file():
        raise HTTPException(status_code=404, detail="page file missing")
    try:
        body = target.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "id": node_id,
        "title": node.get("title", ""),
        "path": rel,
        "page_type": node.get("page_type", ""),
        "tier": node.get("tier", ""),
        "tags": node.get("tags", []),
        "last_verified": node.get("last_verified", ""),
        "body": body,
        "bytes": len(body),
        "summary": node.get("summary", ""),
    }


@app.get("/graph/neighbors/{node_id:path}")
def graph_neighbors(
    node_id: str,
    depth: int = Query(1, ge=1, le=3),
) -> dict[str, Any]:
    if node_id not in state.nodes_by_id:
        raise HTTPException(status_code=404, detail=f"unknown node {node_id}")

    visited: dict[str, int] = {node_id: 0}
    frontier = [node_id]
    edges_seen: list[dict[str, Any]] = []

    for current_depth in range(1, depth + 1):
        next_frontier: list[str] = []
        for node in frontier:
            for edge in state.adjacency.get(node, []):
                neighbor = edge["neighbor"]
                edges_seen.append(
                    {
                        "source": edge["source"],
                        "target": edge["target"],
                        "weight": edge.get("weight", 1),
                        "confidence": edge.get("confidence", "EXTRACTED"),
                    }
                )
                if neighbor not in visited:
                    visited[neighbor] = current_depth
                    next_frontier.append(neighbor)
        frontier = next_frontier

    nodes = [
        {
            **{key: state.nodes_by_id[nid].get(key) for key in (
                "id", "path", "title", "page_type", "tier", "degree", "community",
            )},
            "depth": d,
        }
        for nid, d in visited.items()
        if nid in state.nodes_by_id
    ]
    # De-dup edges by (sorted_pair)
    seen_pairs = set()
    unique_edges = []
    for e in edges_seen:
        pair = tuple(sorted((e["source"], e["target"])))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        unique_edges.append(e)

    return {"root": node_id, "depth": depth, "nodes": nodes, "edges": unique_edges}


@app.get("/graph/communities")
def graph_communities() -> dict[str, Any]:
    return {"communities": state.payload.get("communities", [])}


@app.get("/graph/shortest_path")
def graph_shortest_path(
    a: str = Query(..., description="source node id"),
    b: str = Query(..., description="target node id"),
) -> dict[str, Any]:
    """Undirected BFS shortest path between two node ids (R16).

    Returns ``{"path": [<node ids>], "length": <edge count>}`` where ``length``
    is 0 when ``a == b`` and -1 (with empty path) when no path exists.
    """
    if a not in state.nodes_by_id:
        raise HTTPException(status_code=404, detail=f"unknown node {a}")
    if b not in state.nodes_by_id:
        raise HTTPException(status_code=404, detail=f"unknown node {b}")
    if a == b:
        return {"path": [a], "length": 0}

    prev: dict[str, str | None] = {a: None}
    queue: list[str] = [a]
    while queue:
        cur = queue.pop(0)
        if cur == b:
            break
        for edge in state.adjacency.get(cur, []):
            nb = edge["neighbor"]
            if nb not in prev:
                prev[nb] = cur
                queue.append(nb)

    if b not in prev:
        return {"path": [], "length": -1, "source": a, "target": b}

    path: list[str] = []
    n: str | None = b
    while n is not None:
        path.append(n)
        n = prev[n]
    path.reverse()
    return {"path": path, "length": len(path) - 1, "source": a, "target": b}


# ---------------------------------------------------------------------------
# R17 — Checkpoint tracker (parses reports/checkpoint-graph-tracker.md)
# ---------------------------------------------------------------------------

# In-memory cache keyed by file mtime so successive callers don't re-parse.
_tracker_cache: dict[str, Any] = {"mtime": 0.0, "payload": None}


def _parse_tracker(md_text: str) -> dict[str, Any]:
    """Convert the auto-generated checkpoint-graph-tracker.md into JSON.

    Looks for the two key tables ('Disagreement detail' and 'Merge-signal
    checkpoints') and emits one row dict per table line. Header parsing is
    intentionally tolerant — column order in the markdown is the source of
    truth so we read the first header row of each table to learn keys.
    """
    lines = md_text.splitlines()
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def _parse_table(block: list[str]) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        header: list[str] | None = None
        for raw in block:
            stripped = raw.strip()
            if not stripped.startswith("|"):
                if header is not None:
                    break  # table ended
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Skip alignment rows like | --- | --- |.
            if all(set(c) <= set("-: ") and c for c in cells):
                continue
            if header is None:
                header = [c.lower().replace(" ", "_").replace("(", "").replace(")", "")
                          for c in cells]
                continue
            if len(cells) < len(header):
                cells += [""] * (len(header) - len(cells))
            rows.append(dict(zip(header, cells)))
        return rows

    disagreements = _parse_table(sections.get("Disagreement detail", []))
    merge_signal = _parse_table(sections.get("Merge-signal checkpoints", []))

    # Pull the summary counts via simple regex; keeps the response useful even
    # when the raw tables are empty.
    counts: dict[str, int] = {}
    for line in sections.get("Graph recommendation counts", []):
        m = re.match(r"\|\s*`(\w+)`\s*\|\s*(\d+)\s*\|", line)
        if m:
            counts[m.group(1)] = int(m.group(2))

    breakdown: dict[str, int] = {}
    for line in sections.get("Disagreement summary", []):
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|", line)
        if m:
            breakdown[m.group(1)] = int(m.group(2))

    return {
        "recommendation_counts": counts,
        "disagreement_breakdown": breakdown,
        "disagreements": disagreements,
        "merge_signal": merge_signal,
        "disagreement_count": len(disagreements),
        "merge_signal_count": len(merge_signal),
    }


@app.get("/graph/checkpoint-tracker")
def graph_checkpoint_tracker() -> dict[str, Any]:
    """Parsed JSON view of reports/checkpoint-graph-tracker.md (R17).

    Cached in memory by file mtime so repeated polls from the UI are cheap.
    Returns ``{"available": false, ...}`` when the markdown report is missing
    (e.g. fresh deploy with no graph build yet).
    """
    if not TRACKER_PATH.exists():
        return {
            "available": False,
            "path": str(TRACKER_PATH),
            "disagreements": [],
            "merge_signal": [],
        }
    try:
        mtime = TRACKER_PATH.stat().st_mtime
    except OSError as e:
        return {"available": False, "error": str(e), "disagreements": [], "merge_signal": []}

    if _tracker_cache["payload"] is not None and _tracker_cache["mtime"] == mtime:
        return _tracker_cache["payload"]

    try:
        md = TRACKER_PATH.read_text()
        parsed = _parse_tracker(md)
    except Exception as e:
        return {"available": False, "error": str(e), "disagreements": [], "merge_signal": []}

    payload = {
        "available": True,
        "path": str(TRACKER_PATH),
        "mtime": mtime,
        **parsed,
    }
    _tracker_cache["payload"] = payload
    _tracker_cache["mtime"] = mtime
    return payload


# ---------------------------------------------------------------------------
# R19 — /graph/health (data-quality observability; distinct from /health)
# ---------------------------------------------------------------------------

def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return float(s[0])
    rank = (pct / 100.0) * (len(s) - 1)
    low = int(rank)
    high = min(low + 1, len(s) - 1)
    frac = rank - low
    return float(s[low] + (s[high] - s[low]) * frac)


@app.get("/graph/health")
def graph_health() -> dict[str, Any]:
    """Data-quality snapshot of the loaded graph (R19).

    Independent of /health (liveness). Surfaces signals the wiki team uses
    to decide whether to trigger ingest, dedupe, or curation passes.
    """
    nodes = state.payload.get("nodes", [])
    orphan_count = sum(1 for n in nodes if int(n.get("degree", 0)) == 0)
    broken_link_count = state.payload.get("broken_link_count")

    dedupe_count = None
    dedupe_note = None
    dedupe_path = WIKI_PATH.parent / "reports" / "dedupe-candidates-latest.json"
    try:
        data = json.loads(dedupe_path.read_text())
        if isinstance(data, list):
            dedupe_count = len(data)
        elif isinstance(data, dict) and type(data.get("candidate_count")) is int and data["candidate_count"] >= 0:
            dedupe_count = data["candidate_count"]
        elif isinstance(data, dict) and isinstance(data.get("candidates"), list):
            dedupe_count = len(data["candidates"])
        else:
            dedupe_note = "dedupe report contains no valid candidate count"
    except FileNotFoundError:
        dedupe_note = "dedupe report unavailable"
    except (OSError, ValueError) as exc:
        dedupe_note = f"dedupe report unreadable: {exc}"

    qs = [float(n.get("quality_score", 0.0)) for n in nodes if "quality_score" in n]
    avg_quality = round(sum(qs) / len(qs), 4) if qs else 0.0

    tier_keys = ("hot", "warm", "established", "core", "archive", "workflow")
    tier_distribution: dict[str, int] = {k: 0 for k in tier_keys}
    for n in nodes:
        tier = (n.get("tier") or "").strip().lower()
        if tier in tier_distribution:
            tier_distribution[tier] += 1
        elif tier:
            tier_distribution.setdefault("other", 0)
            tier_distribution["other"] += 1

    now_ts = time.time()
    fallback_ts = float(state.payload.get("generated_at") or now_ts)
    hot_ages_days: list[float] = []
    for n in nodes:
        if (n.get("tier") or "").strip().lower() != "hot":
            continue
        lv = (n.get("last_verified") or "").strip()
        when_ts: float | None = None
        if lv:
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
                try:
                    when_ts = time.mktime(time.strptime(lv[: len(time.strftime(fmt))], fmt))
                    break
                except (ValueError, OverflowError):
                    continue
        if when_ts is None:
            when_ts = fallback_ts
        hot_ages_days.append(max(0.0, (now_ts - when_ts) / 86400.0))

    return {
        "orphan_count": orphan_count,
        "broken_link_count": broken_link_count,
        "broken_link_note": "unresolved targets per page before graph construction" if broken_link_count is not None else "measurement unavailable",
        "dedupe_candidate_count": dedupe_count,
        "dedupe_note": dedupe_note,
        "avg_quality_score": avg_quality,
        "tier_distribution": tier_distribution,
        "hot_age_p50_days": round(_percentile(hot_ages_days, 50), 2),
        "hot_age_p95_days": round(_percentile(hot_ages_days, 95), 2),
        "hot_node_count": len(hot_ages_days),
    }


@app.get("/graph/god-nodes")
def graph_god_nodes(limit: int = Query(15, ge=1, le=100)) -> dict[str, Any]:
    return {"god_nodes": state.payload.get("god_nodes", [])[:limit]}


@app.get("/graph/surprises")
def graph_surprises(
    limit: int = Query(50, ge=1, le=500),
    min_confidence: str = Query("EXTRACTED", pattern="^(EXTRACTED|INFERRED|AMBIGUOUS)$"),
) -> dict[str, Any]:
    order = {"AMBIGUOUS": 0, "INFERRED": 1, "EXTRACTED": 2}
    threshold = order.get(min_confidence, 0)
    filtered = [
        s
        for s in state.payload.get("surprises", [])
        if order.get(s.get("confidence", "EXTRACTED"), 2) >= threshold
    ]
    return {"surprises": filtered[:limit]}


@app.get("/graph/checkpoints")
def graph_checkpoints(
    recommendation: str | None = Query(
        None, pattern="^(keep|compress|archive|merge)$",
    ),
    limit: int = Query(200, ge=1, le=1000),
) -> dict[str, Any]:
    """Per-checkpoint health report with curation recommendations.

    Filter by ``recommendation`` to focus on candidates for one action
    (e.g. ``?recommendation=archive`` for orphaned checkpoints).
    """
    health = state.payload.get("checkpoint_health") or {}
    items = health.get("checkpoints", [])
    if recommendation:
        items = [c for c in items if c.get("recommendation") == recommendation]
    return {
        "total_checkpoints": health.get("total_checkpoints", 0),
        "recommendations": health.get("recommendations", {}),
        "synthesis_neighbor_ratio": health.get("synthesis_neighbor_ratio", 0.0),
        "merge_clusters": health.get("merge_clusters", []),
        "returned": len(items[:limit]),
        "checkpoints": items[:limit],
    }


@app.get("/graph/overview")
def graph_overview(if_none_match: str = Header(default="")) -> Response:
    if state.overview is None:
        raise HTTPException(status_code=503, detail="graph unavailable")
    body, etag = state.overview
    headers = {"ETag": etag, "Cache-Control": "private, no-cache"}
    if any(tag.strip().removeprefix("W/") in (etag, "*") for tag in if_none_match.split(",")):
        return Response(status_code=304, headers=headers)
    return Response(body, media_type="application/json", headers=headers)


@app.get("/graph/export/json")
def graph_export_json() -> JSONResponse:
    # Embeddings are kept in state.payload for /graph/query but stripped from
    # the public export to keep the UI download small (R14 — MiniLM dim 384
    # would otherwise add ~2 MB on a 700-node graph).
    payload = state.payload
    nodes = payload.get("nodes", [])
    if nodes and any(EMBEDDING_FIELD in n for n in nodes):
        slim_nodes = [
            {k: v for k, v in n.items() if k != EMBEDDING_FIELD}
            for n in nodes
        ]
        payload = {**payload, "nodes": slim_nodes}
    return JSONResponse(payload)


# ---------------------------------------------------------------------------
# R14 — POST /graph/query : NL query over node embeddings
# ---------------------------------------------------------------------------

def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na <= 0 or nb <= 0:
        return 0.0
    import math
    return dot / (math.sqrt(na) * math.sqrt(nb))


def _archived_node(node: dict[str, Any]) -> bool:
    archives = {"archive", "archives", "archived", "_archive", "_archives", "_archived"}
    path = node.get("path") or node["id"]
    return (
        (node.get("tier") or "").strip().lower() == "archive"
        or (node.get("retention_mode") or "").strip().lower() == "archive"
        or any(part.lower() in archives for part in Path(path).parts[:-1])
    )


@app.post("/graph/query")
async def graph_query(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Embed ``q`` and return the top-K nodes plus their 1-hop subgraph union.

    Body: ``{"q": "<text>", "k": 10, "include_archived": true}``.
    k defaults to 10 and is capped at 50. Disable include_archived to restrict
    both ranked results and their neighboring subgraph to active pages. An exact
    title ranks first even when its tokens are absent from the embedding
    vocabulary. Each hit reports its match type and measured cosine score.
    Response::

        {
          "q": "...",
          "k": 10,
          "backend": "sentence-transformers" | "tfidf" | "none",
          "nodes": [<full node records ranked by similarity>],
          "subgraph": {"nodes": [...], "edges": [...]}
        }

    If no embedding backend is available (build had ``embedding_backend=none``),
    the response includes ``"error": "embedding backend unavailable"`` and an
    empty result set.
    """
    q = (payload or {}).get("q", "")
    if not isinstance(q, str) or not q.strip():
        raise HTTPException(status_code=400, detail="missing 'q' (non-empty string)")
    include_archived = payload.get("include_archived", True)
    if not isinstance(include_archived, bool):
        raise HTTPException(status_code=400, detail="include_archived must be a boolean")
    k_raw = (payload or {}).get("k", 10)
    try:
        k = max(1, min(int(k_raw), 50))
    except (TypeError, ValueError):
        k = 10

    backend = state.payload.get("embedding_backend", "none")
    qvec = embed_query(q)
    if qvec is None or backend == "none":
        return {
            "q": q,
            "k": k,
            "backend": backend,
            "error": "embedding backend unavailable",
            "nodes": [],
            "subgraph": {"nodes": [], "edges": []},
        }

    title_query = q.strip().casefold()
    has_query_signal = any(qvec)
    scored: list[tuple[bool, float, dict[str, Any]]] = []
    for n in state.payload.get("nodes", []):
        if not include_archived and _archived_node(n):
            continue
        exact_title = n["title"].strip().casefold() == title_query
        score = _cosine(qvec, n.get(EMBEDDING_FIELD, [])) if has_query_signal else 0.0
        if exact_title or score > 0:
            scored.append((exact_title, score, n))

    scored.sort(key=lambda hit: (hit[0], hit[1]), reverse=True)
    top = scored[:k]
    top_ids = {node["id"] for _, _, node in top}

    # 1-hop subgraph: union of neighbours of every top-K hit.
    sub_node_ids: set[str] = set(top_ids)
    sub_edges: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for nid in list(top_ids):
        for adj in state.adjacency.get(nid, []):
            if not include_archived and _archived_node(state.nodes_by_id[adj["neighbor"]]):
                continue
            sub_node_ids.add(adj["neighbor"])
            pair = tuple(sorted((adj["source"], adj["target"])))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            sub_edges.append(
                {
                    "source": adj["source"],
                    "target": adj["target"],
                    "weight": adj.get("weight", 1),
                    "confidence": adj.get("confidence", "EXTRACTED"),
                }
            )

    sub_nodes = [state.nodes_by_id[nid] for nid in sub_node_ids if nid in state.nodes_by_id]

    # Strip embedding vectors from the response — they are only useful server-
    # side and would balloon the JSON payload (~12kB/node for MiniLM dim 384).
    def _strip(n: dict[str, Any]) -> dict[str, Any]:
        if EMBEDDING_FIELD in n:
            n = {k: v for k, v in n.items() if k != EMBEDDING_FIELD}
        return n

    return {
        "q": q,
        "k": k,
        "backend": backend,
        "nodes": [
            {**_strip(n), "score": round(score, 4), "match_type": "exact_title" if exact else "semantic"}
            for exact, score, n in top
        ],
        "subgraph": {
            "nodes": [_strip(n) for n in sub_nodes],
            "edges": sub_edges,
        },
    }


@app.get("/events")
async def sse_events() -> StreamingResponse:
    """Server-Sent Events stream. Emits `graph-updated` on every rebuild."""

    async def event_stream():
        q = await state.subscribe()
        try:
            # Initial hello so clients know they're connected.
            yield "event: hello\ndata: {}\n\n"
            while True:
                try:
                    msg = await asyncio.wait_for(q.get(), timeout=30.0)
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    continue
                yield f"event: {msg}\ndata: {{}}\n\n"
        finally:
            state.unsubscribe(q)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# Admin endpoints (blocked at Caddy for public traffic; token-gated here)
# ---------------------------------------------------------------------------

@app.post("/internal/rebuild")
async def internal_rebuild(x_admin_token: str | None = Header(default=None)) -> dict[str, Any]:
    _require_admin(x_admin_token)
    log.info("rebuild triggered via /internal/rebuild")
    payload = await state.rebuild()
    return {
        "ok": True,
        "rebuild_skipped": payload.get("rebuild_skipped", False),
        "node_count": payload.get("node_count", 0),
        "edge_count": payload.get("edge_count", 0),
        "build_seconds": (state.receipt or {}).get("build_seconds"),
    }


@app.get("/graph/rebuild")
async def graph_rebuild(x_admin_token: str | None = Header(default=None)) -> dict[str, Any]:
    _require_admin(x_admin_token)
    payload = await state.rebuild()
    return {
        "ok": True,
        "rebuild_skipped": payload.get("rebuild_skipped", False),
        "stats": payload.get("extraction_stats", {}),
    }
