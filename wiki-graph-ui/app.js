// Minimal labs-wiki graph viewer.
// Two renderers ship in this image:
//   - "canvas":  the R1-R19 zero-dependency Canvas + Fruchterman-Reingold path
//   - "cosmos":  WebGL via @cosmos.gl/graph (R15 — handles 1500+ nodes, gives
//                organized clusters via GPU force layout)
// Pick at runtime via ?renderer=canvas in the URL or by editing config.js.
// Everything below the renderer abstraction (filters, BFS path mode, NL ask,
// checkpoint health, side panel, R12-R19 features) is renderer-agnostic.

import { buildLabelTargets, pickNodeAtScreenPoint } from "./interaction-targets.js?v=__BUILD_ID__";
import {
  hasPointerMovedEnough,
  shouldUseCoarsePointerTapSlop,
} from "./pointer-gesture.js?v=__BUILD_ID__";

const cfg = window.__WIKI_GRAPH_CONFIG || {};
// If apiBase is literally the placeholder (image built but entrypoint didn't
// run), fall back to same-origin — the UI still works when served from the
// same host as the API.
const API_BASE = (cfg.apiBase && !cfg.apiBase.includes("__API_BASE__"))
  ? cfg.apiBase.replace(/\/$/, "")
  : "";

const RENDERER = (() => {
  try {
    const u = new URLSearchParams(window.location.search).get("renderer");
    if (u === "canvas" || u === "cosmos") return u;
  } catch (_) {}
  return cfg.renderer === "canvas" ? "canvas" : "cosmos";
})();
const USE_COSMOS = RENDERER === "cosmos";
let cosmos = null; // populated in initCosmos() if USE_COSMOS

const state = {
  graph: null,
  filtered: { nodes: [], edges: [] },
  highlightedId: null,
  search: "",
  typeFilter: "",
  tierFilter: "",
  communityFilter: "",
  checkpointClassFilter: "",
  staleOnly: false,
  surprises: false,
  communityColors: new Map(),
  visibleNodes: [],
  labelTargets: [],
  pathMode: false,
  pathStart: null,   // node id
  pathEnd: null,     // node id
  pathNodes: new Set(),  // node ids on shortest path
  pathEdges: [],     // [{source, target}] consecutive pairs on path
  // R14 — NL "ask the graph" results
  ask: {
    active: false,
    nodeIds: new Set(),  // top-K node ids
    subgraphIds: new Set(),  // top-K + 1-hop neighbours
    edgeKeys: new Set(),  // pathEdgeKey strings
    results: [],  // raw response list
  },
  // R17 — checkpoint health overlay
  health: {
    active: false,
    disagreements: [],          // raw rows from /graph/checkpoint-tracker
    disagreeNodeIds: new Set(), // node ids with current!=recommended
    rowsByNodeId: new Map(),    // node id → tracker row (for the side panel)
  },
};

// R17 — fixed color palette per checkpoint_class for the health overlay.
const CHECKPOINT_CLASS_COLORS = {
  planning: "#3b82f6",   // blue
  executed: "#f59e0b",   // amber
  validated: "#22c55e",  // green
  recurring: "#a855f7",  // purple
  incident: "#ef4444",   // red
};
const CHECKPOINT_DEFAULT_COLOR = "#9ca3af"; // gray fallback

const STALE_DAYS_THRESHOLD = 90;
const STALE_MS_THRESHOLD = STALE_DAYS_THRESHOLD * 24 * 60 * 60 * 1000;

// ---------- Cosmograph (cosmos.gl) renderer wiring ------------------------
// initCosmos() is called from loadGraph() once on first successful fetch.
async function initCosmos() {
  if (cosmos) return cosmos;
  const host = document.getElementById("graph-cosmos");
  if (!host) return null;
  host.removeAttribute("hidden");
  const canvasEl = document.getElementById("graph");
  if (canvasEl) canvasEl.style.display = "none";
  // The canvas-only view-controls (zoom in/out/fit) and label rendering are
  // not wired up for cosmos yet; leave them visible so users can still use
  // path/health toggles, but hide pan/zoom buttons (cosmos has its own).
  const viewControls = document.getElementById("view-controls");
  if (viewControls) {
    viewControls.querySelector("#zoom-in")?.setAttribute("hidden", "");
    viewControls.querySelector("#zoom-out")?.setAttribute("hidden", "");
    viewControls.querySelector("#zoom-fit")?.removeAttribute("hidden");
    viewControls.querySelector("#zoom-level")?.setAttribute("hidden", "");
  }
  try {
    const mod = await import("./cosmos-renderer.js?v=__BUILD_ID__");
    cosmos = mod.createCosmosRenderer({
      container: host,
      onPointClick: (node) => {
        if (state.pathMode) {
          // Path-mode click handling lives in handlePathClick.
          handlePathClick(node);
        } else {
          selectNode(node);
        }
      },
      onBackgroundClick: () => {
        if (!state.pathMode) clearSelection();
      },
    });
    return cosmos;
  } catch (e) {
    console.error("cosmos renderer failed, falling back to canvas:", e);
    cosmos = null;
    if (canvasEl) canvasEl.style.display = "";
    host.setAttribute("hidden", "");
    return null;
  }
}

function syncCosmosStyle() {
  if (!cosmos) return;
  const healthActive = state.health.active;
  const askActive = state.ask.active && state.ask.subgraphIds.size > 0;
  const dimNonPath = state.pathMode && state.pathNodes.size > 0;
  cosmos.syncStyle({
    colorOf: (n) => healthActive
      ? (CHECKPOINT_CLASS_COLORS[n.checkpoint_class] || CHECKPOINT_DEFAULT_COLOR)
      : colorForCommunity(n.community),
    sizeOf: (n) => {
      // Degree-scaled with a generous floor so even leaves register as
      // soft-edge dots (the antialiased disc reads as a halo at this size).
      const deg = Math.max(1, n.degree || 1);
      return Math.max(6, Math.min(28, 5 + Math.log2(deg + 1) * 3.4));
    },
    dimOf: (n) => {
      const onPath = state.pathNodes.has(n.id);
      const inAskSub = askActive && state.ask.subgraphIds.has(n.id);
      return (dimNonPath && !onPath) || (askActive && !inAskSub);
    },
  });
  cosmos.render();
  // Keep selection ring in sync with current highlight / path / ask set.
  const sel = new Set();
  if (state.highlightedId) sel.add(state.highlightedId);
  for (const id of state.pathNodes) sel.add(id);
  if (askActive) for (const id of state.ask.nodeIds) sel.add(id);
  cosmos.setSelectedNodes(sel);
}

function isNodeStale(node, now = Date.now()) {
  const lv = (node.last_verified || "").trim();
  if (!lv) return true;
  const t = Date.parse(lv);
  if (Number.isNaN(t)) return true;
  return now - t > STALE_MS_THRESHOLD;
}

async function fetchJSON(path) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { credentials: "include" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

// Curated 16-stop neon-on-dark palette inspired by Gephi/Cosmograph showcases
// and the Karpathy llm-graph aesthetic — high saturation, mid-high lightness,
// hue-cycled so adjacent communities read as distinct under WebGL antialiasing.
// Each entry is `hsl(h s% l%)` so cosmos-renderer's parseColor handles it.
const COMMUNITY_PALETTE = [
  "hsl(190 95% 62%)", // cyan
  "hsl(285 88% 70%)", // violet
  "hsl(48 100% 62%)", // amber
  "hsl(330 92% 68%)", // magenta-pink
  "hsl(155 80% 56%)", // mint
  "hsl(15 92% 64%)",  // coral
  "hsl(220 95% 70%)", // azure
  "hsl(95 78% 60%)",  // lime
  "hsl(270 90% 72%)", // lavender
  "hsl(35 100% 60%)", // tangerine
  "hsl(175 88% 55%)", // teal
  "hsl(310 88% 70%)", // orchid
  "hsl(75 85% 60%)",  // chartreuse
  "hsl(205 95% 66%)", // sky
  "hsl(355 90% 68%)", // rose
  "hsl(125 75% 58%)", // emerald
];

function colorForCommunity(community) {
  if (state.communityColors.has(community)) return state.communityColors.get(community);
  const safe = Number.isFinite(community) ? community : 0;
  // Stable bucket into the curated palette; falls back to golden-angle HSL
  // for very high community ids so we never collide visually for neighbours.
  let color;
  if (safe >= 0 && safe < COMMUNITY_PALETTE.length) {
    color = COMMUNITY_PALETTE[safe];
  } else {
    const hue = (safe * 137.508) % 360;
    color = `hsl(${hue} 88% 64%)`;
  }
  state.communityColors.set(community, color);
  return color;
}

function applyFilters() {
  if (!state.graph) return;
  const q = state.search.trim().toLowerCase();
  const typeF = state.typeFilter;
  const tierF = state.tierFilter;

  const communityF = state.communityFilter;
  const ckptClassF = state.checkpointClassFilter;
  const staleOnly = state.staleOnly;
  const now = Date.now();

  const nodes = state.graph.nodes.filter((n) => {
    if (typeF && n.page_type !== typeF) return false;
    if (tierF && n.tier !== tierF) return false;
    if (communityF !== "" && String(n.community) !== String(communityF)) return false;
    if (ckptClassF && (n.checkpoint_class || "") !== ckptClassF) return false;
    if (staleOnly && !isNodeStale(n, now)) return false;
    if (!q) return true;
    const hay = (n.title + " " + (n.tags || []).join(" ") + " " + (n.summary || "")).toLowerCase();
    return hay.includes(q);
  });
  const ids = new Set(nodes.map((n) => n.id));
  const edges = state.graph.edges.filter((e) => ids.has(e.source) && ids.has(e.target));

  if (state.highlightedId && !ids.has(state.highlightedId)) {
    clearSelection({ redraw: false });
  }

  state.filtered = { nodes, edges };
  if (USE_COSMOS) {
    // Cosmograph owns layout — no FR loop needed. Sync data, then re-style.
    cosmos && cosmos.syncData(nodes, edges);
    syncCosmosStyle();
    return;
  }
  positionNodes(state.filtered.nodes, state.filtered.edges);
  fitViewToNodes(state.filtered.nodes);
}

// ---------- Simple force-directed layout (Fruchterman-Reingold-ish) ---------

function positionNodes(nodes, edges) {
  const W = 2000, H = 2000;
  const k = Math.sqrt((W * H) / Math.max(nodes.length, 1)) * 0.8;

  const byId = new Map(nodes.map((n) => [n.id, n]));

  // R15 — when the server precomputed spring_layout (every node has x/y on
  // arrival from /graph/export/json), skip the full Fruchterman-Reingold loop.
  // Only the velocity scratch fields are reset, then we run a brief 5-iter
  // settle pass so any newly-filtered subset relaxes minor overlaps without
  // throwing away the global structure.
  const allPrecomputed = nodes.length > 0 && nodes.every(
    (n) => Number.isFinite(n.x) && Number.isFinite(n.y) && n.__server_layout !== false,
  );

  for (const n of nodes) {
    if (n.x == null || n.y == null) {
      n.x = Math.random() * W - W / 2;
      n.y = Math.random() * H - H / 2;
    }
    n.vx = 0; n.vy = 0;
  }

  const ITER = allPrecomputed ? 5 : 120;
  let t = (allPrecomputed ? W / 80 : W / 10);
  for (let it = 0; it < ITER; it++) {
    // Repulsive
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist2 = dx * dx + dy * dy + 0.01;
        const force = (k * k) / dist2;
        const fx = dx * force, fy = dy * force;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }
    }
    // Attractive
    for (const e of edges) {
      const a = byId.get(e.source), b = byId.get(e.target);
      if (!a || !b) continue;
      const dx = a.x - b.x, dy = a.y - b.y;
      const dist = Math.sqrt(dx * dx + dy * dy) + 0.01;
      const force = (dist * dist) / k;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      a.vx -= fx; a.vy -= fy;
      b.vx += fx; b.vy += fy;
    }
    for (const n of nodes) {
      const disp = Math.sqrt(n.vx * n.vx + n.vy * n.vy) + 0.01;
      n.x += (n.vx / disp) * Math.min(disp, t);
      n.y += (n.vy / disp) * Math.min(disp, t);
    }
    t *= 0.95;
  }
}

// ---------- Canvas rendering ----------------------------------------------

const canvas = document.getElementById("graph");
const ctx = canvas.getContext("2d");
const isCoarsePointer = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
const view = { scale: 0.35, tx: 0, ty: 0 };
const MIN_SCALE = 0.05;
const MAX_SCALE = isCoarsePointer ? 6 : 4.5;
const ZOOM_STEP = 1.22;

function clampScale(nextScale) {
  return Math.max(MIN_SCALE, Math.min(MAX_SCALE, nextScale));
}

function updateZoomLevel() {
  const label = document.getElementById("zoom-level");
  if (label) label.textContent = `${Math.round(view.scale * 100)}%`;
}

function nodeRadius(node) {
  return Math.max(3, 3 + Math.log2(1 + node.degree) * 2);
}

function resize() {
  if (USE_COSMOS) return; // cosmos manages its own canvas sizing
  const dpr = window.devicePixelRatio || 1;
  canvas.width = canvas.clientWidth * dpr;
  canvas.height = canvas.clientHeight * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  updateZoomLevel();
  draw();
}
window.addEventListener("resize", resize);

function screenToWorld(x, y) {
  return {
    x: (x - canvas.clientWidth / 2 - view.tx) / view.scale,
    y: (y - canvas.clientHeight / 2 - view.ty) / view.scale,
  };
}

function visibleWorldBounds() {
  const a = screenToWorld(0, 0);
  const b = screenToWorld(canvas.clientWidth, canvas.clientHeight);
  return {
    minX: Math.min(a.x, b.x),
    maxX: Math.max(a.x, b.x),
    minY: Math.min(a.y, b.y),
    maxY: Math.max(a.y, b.y),
  };
}

function isNodeVisible(node, bounds, padding = 0) {
  const r = nodeRadius(node) + padding;
  return (
    node.x + r >= bounds.minX &&
    node.x - r <= bounds.maxX &&
    node.y + r >= bounds.minY &&
    node.y - r <= bounds.maxY
  );
}

function pathRoundedRect(x, y, width, height, radius) {
  const r = Math.min(radius, width / 2, height / 2);
  ctx.beginPath();
  if (typeof ctx.roundRect === "function") {
    ctx.roundRect(x, y, width, height, r);
    return;
  }
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + width, y, x + width, y + height, r);
  ctx.arcTo(x + width, y + height, x, y + height, r);
  ctx.arcTo(x, y + height, x, y, r);
  ctx.arcTo(x, y, x + width, y, r);
  ctx.closePath();
}

function setScale(nextScale, anchorX = canvas.clientWidth / 2, anchorY = canvas.clientHeight / 2) {
  if (USE_COSMOS) return;
  const worldPoint = screenToWorld(anchorX, anchorY);
  const clampedScale = clampScale(nextScale);
  view.scale = clampedScale;
  view.tx = anchorX - canvas.clientWidth / 2 - worldPoint.x * clampedScale;
  view.ty = anchorY - canvas.clientHeight / 2 - worldPoint.y * clampedScale;
  updateZoomLevel();
  draw();
}

function fitViewToNodes(nodes = state.filtered.nodes) {
  if (USE_COSMOS) { cosmos && cosmos.fit(); return; }
  if (!nodes.length || !canvas.clientWidth || !canvas.clientHeight) return;

  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const node of nodes) {
    const r = nodeRadius(node);
    minX = Math.min(minX, node.x - r);
    minY = Math.min(minY, node.y - r);
    maxX = Math.max(maxX, node.x + r);
    maxY = Math.max(maxY, node.y + r);
  }

  const width = Math.max(maxX - minX, 120);
  const height = Math.max(maxY - minY, 120);
  const gutter = isCoarsePointer ? 56 : 80;
  const availableWidth = Math.max(canvas.clientWidth - gutter * 2, 120);
  const availableHeight = Math.max(canvas.clientHeight - gutter * 2, 120);
  const nextScale = clampScale(Math.min(availableWidth / width, availableHeight / height));
  const targetX = canvas.clientWidth / 2;
  const targetY = isCoarsePointer ? canvas.clientHeight * 0.46 : canvas.clientHeight / 2;
  const centerX = (minX + maxX) / 2;
  const centerY = (minY + maxY) / 2;

  view.scale = nextScale;
  view.tx = targetX - canvas.clientWidth / 2 - centerX * nextScale;
  view.ty = targetY - canvas.clientHeight / 2 - centerY * nextScale;
  updateZoomLevel();
  draw();
}

function centerNodeInView(node) {
  if (USE_COSMOS) { cosmos && cosmos.focusNode(node.id); return; }
  const targetX = canvas.clientWidth / 2;
  const targetY = isCoarsePointer ? canvas.clientHeight * 0.3 : canvas.clientHeight / 2;
  view.tx = targetX - canvas.clientWidth / 2 - node.x * view.scale;
  view.ty = targetY - canvas.clientHeight / 2 - node.y * view.scale;
}

// ---------- Path mode (R13) -----------------------------------------------

function buildAdjacency(edges) {
  const adj = new Map();
  for (const e of edges) {
    if (!adj.has(e.source)) adj.set(e.source, []);
    if (!adj.has(e.target)) adj.set(e.target, []);
    adj.get(e.source).push(e.target);
    adj.get(e.target).push(e.source);
  }
  return adj;
}

function bfsShortestPath(startId, endId, edges) {
  if (startId === endId) return [startId];
  const adj = buildAdjacency(edges);
  if (!adj.has(startId) || !adj.has(endId)) return null;
  const prev = new Map();
  prev.set(startId, null);
  const queue = [startId];
  while (queue.length) {
    const cur = queue.shift();
    if (cur === endId) {
      const path = [];
      let n = endId;
      while (n != null) { path.push(n); n = prev.get(n); }
      return path.reverse();
    }
    for (const nb of adj.get(cur) || []) {
      if (!prev.has(nb)) {
        prev.set(nb, cur);
        queue.push(nb);
      }
    }
  }
  return null;
}

function clearPathSelection({ redraw = true } = {}) {
  state.pathStart = null;
  state.pathEnd = null;
  state.pathNodes = new Set();
  state.pathEdges = [];
  updatePathPanel();
  if (redraw) draw();
}

function exitPathMode() {
  state.pathMode = false;
  clearPathSelection({ redraw: false });
  const btn = document.getElementById("path-mode-toggle");
  btn?.setAttribute("aria-pressed", "false");
  document.getElementById("path-panel")?.classList.add("hidden");
  draw();
}

function enterPathMode() {
  state.pathMode = true;
  // Path mode is mutually exclusive with the regular node-click selection.
  clearSelection({ redraw: false });
  const btn = document.getElementById("path-mode-toggle");
  btn?.setAttribute("aria-pressed", "true");
  document.getElementById("path-panel")?.classList.remove("hidden");
  updatePathPanel();
  draw();
}

function updatePathPanel() {
  const body = document.getElementById("path-panel-body");
  if (!body) return;
  if (!state.pathStart) {
    body.innerHTML = "<span class='muted'>Click a node to set the start.</span>";
    return;
  }
  const startNode = state.graph?.nodes.find((n) => n.id === state.pathStart);
  if (!state.pathEnd) {
    body.innerHTML = `Start: <strong>${escapeHTML(startNode?.title || state.pathStart)}</strong><br/><span class='muted'>Click another node to set the end.</span>`;
    return;
  }
  if (!state.pathNodes.size) {
    const endNode = state.graph?.nodes.find((n) => n.id === state.pathEnd);
    body.innerHTML = `No path found between <strong>${escapeHTML(startNode?.title || state.pathStart)}</strong> and <strong>${escapeHTML(endNode?.title || state.pathEnd)}</strong>.<br/><span class='muted'>Click again to reset.</span>`;
    return;
  }
  const nodeById = new Map(state.graph.nodes.map((n) => [n.id, n]));
  const titles = Array.from(state.pathNodes).map((id) => {
    const n = nodeById.get(id);
    return n ? n.title : id;
  });
  // pathNodes is a Set built from path order; preserve order using state.pathEdges.
  const ordered = [];
  if (state.pathEdges.length) {
    ordered.push(state.pathEdges[0].source);
    for (const e of state.pathEdges) ordered.push(e.target);
  } else {
    ordered.push(...titles);
  }
  const items = ordered.map((id) => {
    const n = nodeById.get(id);
    return `<li>${escapeHTML(n?.title || id)}</li>`;
  }).join("");
  body.innerHTML = `Path length: <strong>${state.pathEdges.length}</strong> edges (${state.pathNodes.size} nodes)<ol>${items}</ol><span class='muted'>Click any node to reset.</span>`;
}

function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

// ---------- "Ask the graph" NL query (R14) --------------------------------

const askEdgeKey = (s, t) => s < t ? `${s}|${t}` : `${t}|${s}`;

function clearAskResults({ redraw = true } = {}) {
  state.ask = {
    active: false,
    nodeIds: new Set(),
    subgraphIds: new Set(),
    edgeKeys: new Set(),
    results: [],
  };
  const panel = document.getElementById("ask-results");
  panel?.classList.add("hidden");
  document.getElementById("ask-graph-clear")?.classList.add("hidden");
  if (redraw) draw();
}

async function runAskGraph(q) {
  const text = (q || "").trim();
  if (!text) return;
  const meta = document.getElementById("ask-meta");
  const list = document.getElementById("ask-results-list");
  const panel = document.getElementById("ask-results");
  panel?.classList.remove("hidden");
  if (meta) meta.textContent = "querying…";
  if (list) list.innerHTML = "";
  try {
    const res = await fetch(`${API_BASE}/graph/query`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ q: text, k: 10 }),
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = await res.json();
    if (data.error) {
      if (meta) meta.textContent = `backend: ${data.backend} — ${data.error}`;
      return;
    }
    const top = data.nodes || [];
    const subNodes = (data.subgraph && data.subgraph.nodes) || [];
    const subEdges = (data.subgraph && data.subgraph.edges) || [];

    state.ask.active = true;
    state.ask.results = top;
    state.ask.nodeIds = new Set(top.map((n) => n.id));
    state.ask.subgraphIds = new Set(subNodes.map((n) => n.id));
    // Always include the top-K themselves in the subgraph set.
    for (const n of top) state.ask.subgraphIds.add(n.id);
    state.ask.edgeKeys = new Set(subEdges.map((e) => askEdgeKey(e.source, e.target)));

    if (meta) meta.textContent = `backend: ${data.backend} · top ${top.length} of ${data.k}`;
    if (list) {
      list.innerHTML = "";
      for (const n of top) {
        const li = document.createElement("li");
        li.textContent = `${n.title} (${n.page_type}, score ${n.score})`;
        li.title = n.id;
        li.addEventListener("click", () => {
          const local = state.filtered.nodes.find((x) => x.id === n.id);
          if (local) selectNode(local);
        });
        list.appendChild(li);
      }
    }
    document.getElementById("ask-graph-clear")?.classList.remove("hidden");
    draw();
  } catch (e) {
    if (meta) meta.textContent = `error: ${e.message}`;
  }
}

// ---------- Checkpoint health overlay (R17) -------------------------------

// Match a tracker row to a graph node id. The tracker reports paths relative
// to wiki/, e.g. "sources/foo.md"; node ids in the graph are stored as
// "<dir>/<slug>" (no .md extension). Normalise on both sides before compare.
function trackerPathToNodeId(p) {
  if (!p) return "";
  // Strip surrounding backticks (markdown code spans), the .md extension,
  // and any leading/trailing whitespace.
  return String(p).replace(/^`|`$/g, "").trim().replace(/\.md$/i, "");
}

async function loadCheckpointTracker() {
  try {
    const data = await fetchJSON("/graph/checkpoint-tracker");
    if (!data || !data.available) {
      state.health.disagreements = [];
      state.health.disagreeNodeIds = new Set();
      state.health.rowsByNodeId = new Map();
      return;
    }
    const rows = data.disagreements || [];
    state.health.disagreements = rows;
    const ids = new Set();
    const byId = new Map();
    for (const row of rows) {
      const nid = trackerPathToNodeId(row.path);
      if (!nid) continue;
      ids.add(nid);
      byId.set(nid, row);
    }
    state.health.disagreeNodeIds = ids;
    state.health.rowsByNodeId = byId;
  } catch (e) {
    state.health.disagreements = [];
    state.health.disagreeNodeIds = new Set();
    state.health.rowsByNodeId = new Map();
  }
}

function enterCheckpointHealth() {
  state.health.active = true;
  document.getElementById("checkpoint-health-toggle")?.setAttribute("aria-pressed", "true");
  // Lazy-load the tracker the first time we enter the overlay.
  if (!state.health.disagreements.length) {
    loadCheckpointTracker().then(() => draw());
  }
  draw();
}
function exitCheckpointHealth() {
  state.health.active = false;
  document.getElementById("checkpoint-health-toggle")?.setAttribute("aria-pressed", "false");
  document.getElementById("checkpoint-detail")?.classList.add("hidden");
  draw();
}
function showCheckpointDetail(node) {
  const row = state.health.rowsByNodeId.get(node.id);
  const panel = document.getElementById("checkpoint-detail");
  const body = document.getElementById("checkpoint-detail-body");
  if (!panel || !body) return;
  if (!row) {
    panel.classList.add("hidden");
    return;
  }
  panel.classList.remove("hidden");
  const fields = [
    ["Title", row.title],
    ["Class", row.class],
    ["Retention (current)", row.retention],
    ["Heuristic rec", row.heuristic_rec],
    ["Graph rec (recommended)", row.graph_rec],
    ["Tier", row.tier],
    ["Degree", row.degree],
    ["Concept neighbours", row.concept_nb],
    ["Synthesis neighbours", row.synth_nb],
    ["Path", row.path],
  ];
  body.innerHTML = fields
    .filter(([, v]) => v != null && v !== "")
    .map(([k, v]) => `<div><span class='muted'>${escapeHTML(k)}:</span> ${escapeHTML(String(v))}</div>`)
    .join("");
}

function handlePathClick(node) {
  if (!state.pathStart) {
    state.pathStart = node.id;
    state.pathEnd = null;
    state.pathNodes = new Set([node.id]);
    state.pathEdges = [];
    updatePathPanel();
    draw();
    return;
  }
  if (!state.pathEnd) {
    state.pathEnd = node.id;
    const path = bfsShortestPath(state.pathStart, state.pathEnd, state.graph?.edges || []);
    if (path && path.length) {
      state.pathNodes = new Set(path);
      const edges = [];
      for (let i = 0; i < path.length - 1; i++) {
        edges.push({ source: path[i], target: path[i + 1] });
      }
      state.pathEdges = edges;
    } else {
      state.pathNodes = new Set();
      state.pathEdges = [];
    }
    updatePathPanel();
    draw();
    return;
  }
  // Third click resets.
  clearPathSelection();
}

function draw() {
  if (USE_COSMOS) { syncCosmosStyle(); return; }
  ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
  const { nodes, edges } = state.filtered;
  state.visibleNodes = [];
  state.labelTargets = [];
  if (!nodes.length) return;

  const cx = canvas.clientWidth / 2;
  const cy = canvas.clientHeight / 2;
  const bounds = visibleWorldBounds();
  const viewportPadding = 160 / view.scale;
  const visibleNodes = nodes.filter((node) => isNodeVisible(node, bounds, viewportPadding));
  state.visibleNodes = visibleNodes;
  const visibleIds = new Set(visibleNodes.map((node) => node.id));
  const nodeById = new Map(nodes.map((node) => [node.id, node]));

  ctx.save();
  ctx.translate(cx + view.tx, cy + view.ty);
  ctx.scale(view.scale, view.scale);

  // Edges
  const pathEdgeKey = (s, t) => s < t ? `${s}|${t}` : `${t}|${s}`;
  const pathEdgeSet = state.pathMode && state.pathEdges.length
    ? new Set(state.pathEdges.map((e) => pathEdgeKey(e.source, e.target)))
    : null;
  const dimNonPath = state.pathMode && state.pathNodes.size > 0;
  const askActive = state.ask.active && state.ask.subgraphIds.size > 0;

  ctx.lineWidth = 0.8 / view.scale;
  for (const e of edges) {
    if (!visibleIds.has(e.source) && !visibleIds.has(e.target)) continue;
    const a = nodeById.get(e.source), b = nodeById.get(e.target);
    if (!a || !b) continue;
    let strokeStyle;
    const isOnPath = pathEdgeSet && pathEdgeSet.has(pathEdgeKey(e.source, e.target));
    const isAskEdge = askActive && state.ask.edgeKeys.has(pathEdgeKey(e.source, e.target));
    if (isOnPath) {
      strokeStyle = "rgba(94,234,212,0.95)";
    } else if (isAskEdge) {
      strokeStyle = "rgba(94,234,212,0.6)";
    } else if (dimNonPath || askActive) {
      strokeStyle = "rgba(120,130,150,0.06)";
    } else if (state.surprises && e.cross_community) {
      strokeStyle = "rgba(248,113,113,0.85)";
    } else {
      strokeStyle = "rgba(120,130,150,0.25)";
    }
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = (isOnPath || isAskEdge) ? 2.5 / view.scale : 0.8 / view.scale;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }
  ctx.lineWidth = 0.8 / view.scale;

  // Nodes
  const healthActive = state.health.active;
  for (const n of visibleNodes) {
    const r = nodeRadius(n);
    const onPath = state.pathNodes.has(n.id);
    const inAskTop = askActive && state.ask.nodeIds.has(n.id);
    const inAskSub = askActive && state.ask.subgraphIds.has(n.id);
    const dimNode = (dimNonPath && !onPath) || (askActive && !inAskSub);
    ctx.globalAlpha = dimNode ? 0.18 : 1.0;
    // R17 — checkpoint-health colors override community palette.
    const fillColor = healthActive
      ? (CHECKPOINT_CLASS_COLORS[n.checkpoint_class] || CHECKPOINT_DEFAULT_COLOR)
      : colorForCommunity(n.community);
    ctx.fillStyle = fillColor;
    if (state.highlightedId === n.id) {
      ctx.fillStyle = "rgba(94,234,212,0.18)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 9 / view.scale, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = fillColor;
    }
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fill();
    if (onPath || inAskTop) {
      ctx.strokeStyle = "#5eead4";
      ctx.lineWidth = 2.5 / view.scale;
      ctx.stroke();
    } else if (state.highlightedId === n.id) {
      ctx.strokeStyle = "#5eead4";
      ctx.lineWidth = 2 / view.scale;
      ctx.stroke();
    }
    // R17 — red disagreement ring.
    if (healthActive && state.health.disagreeNodeIds.has(n.id)) {
      ctx.strokeStyle = "#ef4444";
      ctx.lineWidth = 2.5 / view.scale;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 4 / view.scale, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1.0;
  }

  // As the user zooms in, relax the label threshold so mobile exploration
  // reveals more context without needing to tap every single node.
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  state.labelTargets = buildLabelTargets({
    nodes: visibleNodes,
    highlightedId: state.highlightedId,
    canvasSize: { width: canvas.clientWidth, height: canvas.clientHeight },
    view,
    nodeRadius,
    measureText(label, fontWorldPx) {
      ctx.font = `${fontWorldPx}px sans-serif`;
      return ctx.measureText(label).width;
    },
  });

  for (const target of state.labelTargets) {
    const { node, label, highlighted, fontWorldPx, chipRadius, worldRect } = target;
    ctx.font = `${fontWorldPx}px sans-serif`;
    ctx.fillStyle = highlighted ? "rgba(11,13,18,0.92)" : "rgba(11,13,18,0.76)";
    ctx.strokeStyle = highlighted ? "#5eead4" : "rgba(120,130,150,0.35)";
    ctx.lineWidth = (highlighted ? 1.5 : 1) / view.scale;
    pathRoundedRect(worldRect.x, worldRect.y, worldRect.w, worldRect.h, chipRadius);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = highlighted ? "#f8fafc" : "#e5e7eb";
    ctx.fillText(label, node.x, worldRect.y + worldRect.h / 2);
  }

  ctx.restore();
}

function findNode(id) {
  return state.filtered.nodes.find((n) => n.id === id);
}

function clearSelection({ redraw = true } = {}) {
  state.highlightedId = null;
  document.body.classList.remove("node-panel-open");
  document.getElementById("node-panel").classList.add("hidden");
  if (redraw) draw();
}

function openNodePanel() {
  document.body.classList.add("node-panel-open");
}

function selectNode(node) {
  state.highlightedId = node.id;
  centerNodeInView(node);
  showNodePanel(node);
  // R17 — when health overlay is active, show disagreement detail too.
  if (state.health.active && state.health.disagreeNodeIds.has(node.id)) {
    showCheckpointDetail(node);
  }
  draw();
}

// ---------- Interactions ---------------------------------------------------

// Unified pointer handling so mouse, touch, and pen all share one code path.
// We track active pointers in a Map to support pinch-to-zoom on touch devices.
const activePointers = new Map(); // pointerId -> {x, y}
let pinchStartDist = 0;
let pinchStartScale = 1;
let panPointerId = null;
let panLastX = 0, panLastY = 0;
let pointerDownAt = 0;
let pointerDownX = 0, pointerDownY = 0;
let pointerMoved = false;
const TAP_MAX_MS = 500;

function pinchDistance() {
  const pts = Array.from(activePointers.values());
  if (pts.length < 2) return 0;
  const dx = pts[0].x - pts[1].x;
  const dy = pts[0].y - pts[1].y;
  return Math.hypot(dx, dy);
}

canvas.addEventListener("pointerdown", (e) => {
  if (USE_COSMOS) return;
  canvas.setPointerCapture(e.pointerId);
  activePointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  pointerDownAt = performance.now();
  pointerDownX = e.clientX;
  pointerDownY = e.clientY;
  pointerMoved = false;

  if (activePointers.size === 1) {
    panPointerId = e.pointerId;
    panLastX = e.clientX;
    panLastY = e.clientY;
  } else if (activePointers.size === 2) {
    pinchStartDist = pinchDistance();
    pinchStartScale = view.scale;
    panPointerId = null; // Pinch mode — disable single-finger pan.
  }
});

canvas.addEventListener("pointermove", (e) => {
  if (USE_COSMOS) return;
  if (!activePointers.has(e.pointerId)) return;
  activePointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

  if (activePointers.size >= 2 && pinchStartDist > 0) {
    const dist = pinchDistance();
    const factor = dist / pinchStartDist;
    const pts = Array.from(activePointers.values());
    const rect = canvas.getBoundingClientRect();
    const midX = (pts[0].x + pts[1].x) / 2 - rect.left;
    const midY = (pts[0].y + pts[1].y) / 2 - rect.top;
    setScale(pinchStartScale * factor, midX, midY);
    pointerMoved = true;
    return;
  }

  if (e.pointerId === panPointerId) {
    const dx = e.clientX - panLastX;
    const dy = e.clientY - panLastY;
    if (!pointerMoved) {
      pointerMoved = hasPointerMovedEnough({
        startX: pointerDownX,
        startY: pointerDownY,
        currentX: e.clientX,
        currentY: e.clientY,
        isCoarsePointer: shouldUseCoarsePointerTapSlop({
          pointerType: e.pointerType,
          fallbackIsCoarsePointer: isCoarsePointer,
        }),
      });
    }
    if (!pointerMoved) {
      return;
    }
    view.tx += dx;
    view.ty += dy;
    panLastX = e.clientX;
    panLastY = e.clientY;
    draw();
  }
});

function endPointer(e) {
  if (USE_COSMOS) return;
  if (!activePointers.has(e.pointerId)) return;
  activePointers.delete(e.pointerId);

  // If this was a quick, near-stationary press, treat it as a tap.
  if (
    e.pointerId === panPointerId &&
    !pointerMoved &&
    performance.now() - pointerDownAt < TAP_MAX_MS
  ) {
    handleTap(e.clientX, e.clientY);
  }

  if (activePointers.size < 2) pinchStartDist = 0;
  if (activePointers.size === 0) panPointerId = null;
  else {
    // One finger lifted during a pinch — promote the remaining one to pan.
    const [id, pt] = activePointers.entries().next().value;
    panPointerId = id;
    panLastX = pt.x;
    panLastY = pt.y;
  }
}
canvas.addEventListener("pointerup", endPointer);
canvas.addEventListener("pointercancel", endPointer);

canvas.addEventListener("wheel", (e) => {
  if (USE_COSMOS) return;
  e.preventDefault();
  const factor = Math.exp(-e.deltaY * 0.001);
  const rect = canvas.getBoundingClientRect();
  setScale(view.scale * factor, e.clientX - rect.left, e.clientY - rect.top);
}, { passive: false });

function handleTap(clientX, clientY) {
  const rect = canvas.getBoundingClientRect();
  const px = clientX - rect.left;
  const py = clientY - rect.top;
  const hit = pickNodeAtScreenPoint({
    screenX: px,
    screenY: py,
    nodes: state.visibleNodes.length ? state.visibleNodes : state.filtered.nodes,
    labelTargets: state.labelTargets,
    canvasSize: { width: canvas.clientWidth, height: canvas.clientHeight },
    view,
    nodeRadius,
    isCoarsePointer,
  });
  if (hit) {
    if (state.pathMode) {
      handlePathClick(hit);
      return;
    }
    selectNode(hit);
  } else if (state.highlightedId) {
    clearSelection();
  }
}

async function showNodePanel(node) {
  document.getElementById("node-panel").classList.remove("hidden");
  if (isCoarsePointer) {
    closeSidebar();
    openNodePanel();
  }
  document.getElementById("node-title").textContent = node.title;
  document.getElementById("node-meta").textContent =
    `${node.page_type || "page"} · tier=${node.tier || "—"} · degree=${node.degree} · community=${node.community}`;
  document.getElementById("node-summary").textContent = node.summary || "";
  const ul = document.getElementById("node-neighbors");
  ul.innerHTML = "<li class='muted'>loading…</li>";
  try {
    const data = await fetchJSON(`/graph/neighbors/${encodeURIComponent(node.id)}?depth=1`);
    const neighbors = data.nodes.filter((n) => n.id !== node.id);
    ul.innerHTML = "";
    for (const n of neighbors) {
      const li = document.createElement("li");
      li.textContent = `${n.title}  · ${n.page_type}`;
      li.addEventListener("click", () => {
        const local = state.filtered.nodes.find((x) => x.id === n.id);
        if (local) {
          selectNode(local);
          return;
        }
        state.highlightedId = n.id;
        showNodePanel(n);
        draw();
      });
      ul.appendChild(li);
    }
    if (!neighbors.length) ul.innerHTML = "<li class='muted'>no neighbours</li>";
  } catch (e) {
    ul.innerHTML = `<li class='muted'>error: ${e.message}</li>`;
  }
}

// ---------- UI wiring ------------------------------------------------------

function populateTypes() {
  const select = document.getElementById("type-filter");
  select.innerHTML = "<option value=''>(any)</option>";
  const types = Array.from(new Set(state.graph.nodes.map((n) => n.page_type))).filter(Boolean).sort();
  for (const t of types) {
    const opt = document.createElement("option");
    opt.value = t; opt.textContent = t;
    select.appendChild(opt);
  }
}

function populateCommunities() {
  const select = document.getElementById("community-filter");
  if (!select) return;
  // Distinct community values from graph.nodes, sorted numerically.
  const communities = Array.from(
    new Set(
      state.graph.nodes
        .map((n) => n.community)
        .filter((c) => c != null && c !== ""),
    ),
  ).sort((a, b) => Number(a) - Number(b));
  // Preserve current selection if still valid.
  const current = select.value;
  select.innerHTML = "<option value=''>(any)</option>";
  for (const c of communities) {
    const opt = document.createElement("option");
    opt.value = String(c);
    opt.textContent = `cluster ${c}`;
    select.appendChild(opt);
  }
  if (current && communities.some((c) => String(c) === current)) {
    select.value = current;
  }
}

function updateStats() {
  const s = state.graph;
  document.getElementById("stats").textContent =
    `${s.node_count} nodes · ${s.edge_count} edges · ${s.community_count} clusters · updated ${s.generated_at ? new Date(s.generated_at * 1000).toLocaleString() : "—"}`;
}

function updateLegend() {
  const el = document.getElementById("legend");
  const top = (state.graph.communities || []).slice(0, 6);
  el.innerHTML = top
    .map((c) => `<span class='swatch' style='background:${colorForCommunity(c.community)}'></span>cluster ${c.community} · ${c.size}`)
    .join("<br/>");
}

async function loadGraph() {
  document.getElementById("connection-state").textContent = "loading graph…";
  try {
    state.graph = await fetchJSON("/graph/export/json");
    if (USE_COSMOS) await initCosmos();
    populateTypes();
    populateCommunities();
    updateStats();
    updateLegend();
    resize();
    applyFilters();
    document.getElementById("connection-state").textContent = "connected";
  } catch (e) {
    document.getElementById("connection-state").textContent = `error: ${e.message}`;
  }
}

function bindUI() {
  document.getElementById("search").addEventListener("input", (e) => {
    state.search = e.target.value; applyFilters();
  });
  document.getElementById("type-filter").addEventListener("change", (e) => {
    state.typeFilter = e.target.value; applyFilters();
  });
  document.getElementById("tier-filter").addEventListener("change", (e) => {
    state.tierFilter = e.target.value; applyFilters();
  });
  document.getElementById("surprises-toggle").addEventListener("change", (e) => {
    state.surprises = e.target.checked; draw();
  });
  document.getElementById("community-filter")?.addEventListener("change", (e) => {
    state.communityFilter = e.target.value; applyFilters();
  });
  document.getElementById("checkpoint-class-filter")?.addEventListener("change", (e) => {
    state.checkpointClassFilter = e.target.value; applyFilters();
  });
  document.getElementById("stale-only-toggle")?.addEventListener("change", (e) => {
    state.staleOnly = e.target.checked; applyFilters();
  });
  document.getElementById("clear-filters")?.addEventListener("click", () => {
    state.search = "";
    state.typeFilter = "";
    state.tierFilter = "";
    state.communityFilter = "";
    state.checkpointClassFilter = "";
    state.staleOnly = false;
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
    const setChecked = (id, val) => { const el = document.getElementById(id); if (el) el.checked = val; };
    setVal("search", "");
    setVal("type-filter", "");
    setVal("tier-filter", "");
    setVal("community-filter", "");
    setVal("checkpoint-class-filter", "");
    setChecked("stale-only-toggle", false);
    applyFilters();
  });
  document.getElementById("rebuild-btn").addEventListener("click", () => loadGraph());
  document.getElementById("zoom-in").addEventListener("click", () => setScale(view.scale * ZOOM_STEP));
  document.getElementById("zoom-out").addEventListener("click", () => setScale(view.scale / ZOOM_STEP));
  document.getElementById("zoom-fit").addEventListener("click", () => fitViewToNodes());
  document.getElementById("path-mode-toggle")?.addEventListener("click", () => {
    if (state.pathMode) exitPathMode(); else enterPathMode();
  });
  document.getElementById("path-panel-close")?.addEventListener("click", () => exitPathMode());
  document.getElementById("ask-graph")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      runAskGraph(e.target.value);
    }
  });
  document.getElementById("ask-graph-clear")?.addEventListener("click", () => {
    const el = document.getElementById("ask-graph");
    if (el) el.value = "";
    clearAskResults();
  });
  document.getElementById("checkpoint-health-toggle")?.addEventListener("click", () => {
    if (state.health.active) exitCheckpointHealth(); else enterCheckpointHealth();
  });
  document.getElementById("node-panel-close").addEventListener("click", () => clearSelection());

  // Mobile drawer wiring — these elements are always in the DOM but only
  // visible at narrow widths via CSS.
  const toggle = document.getElementById("sidebar-toggle");
  const closeBtn = document.getElementById("sidebar-close");
  const backdrop = document.getElementById("sidebar-backdrop");
  toggle?.addEventListener("click", () => {
    document.body.classList.contains("sidebar-open") ? closeSidebar() : openSidebar();
  });
  closeBtn?.addEventListener("click", closeSidebar);
  backdrop?.addEventListener("click", closeSidebar);
  // Allow Esc to dismiss the drawer for keyboard users.
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("sidebar-open")) {
      closeSidebar();
    } else if (e.key === "Escape" && state.pathMode) {
      exitPathMode();
    } else if (e.key === "Escape" && state.highlightedId) {
      clearSelection();
    }
  });
  // Canvas dimensions change when the visual viewport shifts (e.g. mobile
  // address bar showing/hiding) — keep the renderer in sync.
  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", resize);
  }
  window.addEventListener("orientationchange", () => setTimeout(resize, 100));
}

function openSidebar() {
  document.body.classList.remove("node-panel-open");
  document.body.classList.add("sidebar-open");
  document.getElementById("sidebar-toggle")?.setAttribute("aria-expanded", "true");
}
function closeSidebar() {
  document.body.classList.remove("sidebar-open");
  document.getElementById("sidebar-toggle")?.setAttribute("aria-expanded", "false");
}

function subscribeSSE() {
  try {
    const src = new EventSource(`${API_BASE}/events`, { withCredentials: true });
    src.addEventListener("graph-updated", () => loadGraph());
    src.addEventListener("hello", () => {
      document.getElementById("connection-state").textContent = "connected (live)";
    });
    src.onerror = () => {
      document.getElementById("connection-state").textContent = "reconnecting…";
    };
  } catch (e) {
    // SSE unsupported; static load is still fine.
  }
}

bindUI();
loadGraph().then(subscribeSSE);
