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
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from graph_builder import (
    EMBEDDING_FIELD,
    build as build_graph_artifact,
    compute_node_embeddings,
    embed_query,
)

log = logging.getLogger("wiki-graph-api")

WIKI_PATH = Path(os.environ.get("WIKI_PATH", "/app/wiki"))
CACHE_DIR = Path(os.environ.get("CACHE_DIR", "/data/cache"))
GRAPH_PATH = Path(os.environ.get("GRAPH_PATH", "/data/graph.json"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")


class GraphState:
    """In-memory graph snapshot; refreshed on rebuild."""

    def __init__(self) -> None:
        self.payload: dict[str, Any] = {}
        self.nodes_by_id: dict[str, dict[str, Any]] = {}
        self.adjacency: dict[str, list[dict[str, Any]]] = {}
        self.last_rebuild_iso: str = ""
        self.last_rebuild_seconds: float = 0.0
        self._lock = asyncio.Lock()
        self._subscribers: set[asyncio.Queue[str]] = set()

    def load_from_disk(self) -> bool:
        if not GRAPH_PATH.exists():
            return False
        try:
            payload = json.loads(GRAPH_PATH.read_text())
        except (OSError, json.JSONDecodeError) as e:
            log.warning("failed to load %s: %s", GRAPH_PATH, e)
            return False
        self._install(payload)
        return True

    def _install(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.nodes_by_id = {n["id"]: n for n in payload.get("nodes", [])}
        adjacency: dict[str, list[dict[str, Any]]] = {nid: [] for nid in self.nodes_by_id}
        for edge in payload.get("edges", []):
            s, t = edge["source"], edge["target"]
            adjacency.setdefault(s, []).append({"neighbor": t, **edge})
            adjacency.setdefault(t, []).append({"neighbor": s, **edge})
        self.adjacency = adjacency
        generated = payload.get("generated_at")
        if isinstance(generated, (int, float)):
            self.last_rebuild_iso = time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(generated)
            )
        self.last_rebuild_seconds = float(payload.get("build_seconds", 0.0))

    async def rebuild(self) -> dict[str, Any]:
        async with self._lock:
            loop = asyncio.get_running_loop()
            payload = await loop.run_in_executor(
                None, build_graph_artifact, WIKI_PATH, CACHE_DIR, GRAPH_PATH
            )
            self._install(payload)
            await self._broadcast("graph-updated")
            return payload

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
    else:
        log.info("no graph on disk; building initial snapshot")
        try:
            await state.rebuild()
        except Exception as e:  # pragma: no cover — defensive startup
            log.exception("initial build failed: %s", e)


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
    return {
        "node_count": state.payload.get("node_count", 0),
        "edge_count": state.payload.get("edge_count", 0),
        "communities": state.payload.get("community_count", 0),
        "last_rebuild": state.last_rebuild_iso,
        "build_seconds": state.last_rebuild_seconds,
        "extraction": state.payload.get("extraction_stats", {}),
    }


@app.get("/graph/nodes/{node_id:path}")
def graph_node(node_id: str) -> dict[str, Any]:
    node = state.nodes_by_id.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"unknown node {node_id}")
    return node


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
        {**state.nodes_by_id[nid], "depth": d}
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


@app.post("/graph/query")
async def graph_query(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Embed ``q`` and return the top-K nodes plus their 1-hop subgraph union.

    Body: ``{"q": "<text>", "k": 10}`` (k optional, default 10, capped at 50).
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

    scored: list[tuple[float, dict[str, Any]]] = []
    for n in state.payload.get("nodes", []):
        vec = n.get(EMBEDDING_FIELD)
        if not vec:
            continue
        s = _cosine(qvec, vec)
        scored.append((s, n))

    scored.sort(key=lambda r: r[0], reverse=True)
    top = scored[:k]
    top_ids = {n["id"] for _, n in top}

    # 1-hop subgraph: union of neighbours of every top-K hit.
    sub_node_ids: set[str] = set(top_ids)
    sub_edges: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for nid in list(top_ids):
        for adj in state.adjacency.get(nid, []):
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
            {**_strip(n), "score": round(score, 4)}
            for score, n in top
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
        "node_count": payload.get("node_count", 0),
        "edge_count": payload.get("edge_count", 0),
        "build_seconds": payload.get("build_seconds", 0.0),
    }


@app.get("/graph/rebuild")
async def graph_rebuild(x_admin_token: str | None = Header(default=None)) -> dict[str, Any]:
    _require_admin(x_admin_token)
    payload = await state.rebuild()
    return {"ok": True, "stats": payload.get("extraction_stats", {})}
