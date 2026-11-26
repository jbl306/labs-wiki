// Minimal labs-wiki graph viewer.
// Two renderers ship in this image:
//   - "canvas":  the R1-R19 zero-dependency Canvas + Fruchterman-Reingold path
//   - "webgl":   custom WebGL2 renderer (default).
//                Uses server-precomputed x/y from /graph/overview — zero JS
//                simulation, no drift. See webgl-renderer.js.
// Pick at runtime via ?renderer=canvas in the URL or by editing config.js.
// Everything below the renderer abstraction (filters, BFS path mode, NL ask,
// checkpoint health, side panel, R12-R19 features) is renderer-agnostic.

import { buildLabelTargets, graphBounds, pickNodeAtScreenPoint } from "./interaction-targets.js?v=__BUILD_ID__";
import {
  hasPointerMovedEnough,
  shouldUseCoarsePointerTapSlop,
} from "./pointer-gesture.js?v=__BUILD_ID__";
import { renderMarkdown } from "./markdown.js?v=__BUILD_ID__";

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
    if (u === "canvas" || u === "webgl") return u;
  } catch (_) {}
  return cfg.renderer === "canvas" ? "canvas" : "webgl";
})();
let tryWebgl = RENDERER === "webgl";
let gpuRenderer = null;
let gpuLabels = null;   // adaptive HTML label overlay (webgl mode only)

// Map of community id -> short human-friendly label, computed in
// enrichGraph() from the most-frequent tag(s) inside each community.
// Used by populateCommunities() and updateLegend() so the filter shows
// "Wiki & Knowledge Mgmt" instead of "cluster 0".
const clusterLabels = new Map();
const overviewLabels = new Map();
function clusterLabel(c) {
  if (c == null || c === "") return "";
  const lbl = clusterLabels.get(String(c));
  return lbl ? lbl : `cluster ${c}`;
}

function overviewClusterLabel(c) {
  return overviewLabels.get(String(c)) || clusterLabel(c);
}

// Trim verbose ingestion-source prefixes so labels in the graph and
// neighbour lists read as the actual gist, not the pipeline boilerplate
// that put them there. Matches: "Copilot Session Checkpoint:",
// "Copilot Session:", "Copilot CLI Session:", "Recurring checkpoint
// patterns:", and the AI-generated cluster-summary cruft.
const TITLE_PREFIX_RE = /^(?:copilot(?:\s+cli)?\s+session(?:\s+checkpoint)?\s*:|recurring\s+checkpoint\s+patterns?\s*:|cluster\s+summary\s*:)\s*/i;
function displayTitle(title) {
  if (!title) return title;
  let t = String(title).replace(TITLE_PREFIX_RE, "").trim();
  // Common second-pass: titles like "Checkpoint: Foo" → "Foo"
  t = t.replace(/^checkpoint\s*:\s*/i, "");
  return t || title;
}

// Run once after the graph overview arrives. (1) shorten every node title
// for display, keeping the original under `original_title` for search; and
// (2) auto-name every community by its top tag.
function enrichGraph(graph) {
  if (!graph || !Array.isArray(graph.nodes)) return;
  for (const n of graph.nodes) {
    if (!n.original_title) n.original_title = n.title;
    n.title = displayTitle(n.title);
  }
  // Tally tag frequency per community, weighted by node degree so hubs
  // anchor the cluster identity.
  const tally = new Map(); // community -> Map(tag -> weight)
  for (const n of graph.nodes) {
    const c = n.community;
    if (c == null || c === "") continue;
    const tags = Array.isArray(n.tags) ? n.tags : [];
    if (!tags.length) continue;
    const w = 1 + Math.log2(1 + (n.degree || 0));
    let m = tally.get(c);
    if (!m) { m = new Map(); tally.set(c, m); }
    for (const tag of tags) {
      if (!tag) continue;
      m.set(tag, (m.get(tag) || 0) + w);
    }
  }
  clusterLabels.clear();
  // Track which tags are already "claimed" by a higher-weight cluster so
  // we don't end up with three "ml-engine" clusters.
  const claimed = new Set();
  // Sort communities by total weight so the biggest ones get first pick.
  const ordered = Array.from(tally.entries()).sort((a, b) => {
    const sa = Array.from(a[1].values()).reduce((s, v) => s + v, 0);
    const sb = Array.from(b[1].values()).reduce((s, v) => s + v, 0);
    return sb - sa;
  });
  for (const [c, m] of ordered) {
    const sorted = Array.from(m.entries()).sort((a, b) => b[1] - a[1]);
    let primary = sorted.find(([t]) => !claimed.has(t));
    if (!primary) primary = sorted[0];
    if (!primary) continue;
    claimed.add(primary[0]);
    // Pick a secondary tag for richer naming, also unclaimed if possible.
    const secondary = sorted.find(([t]) => t !== primary[0] && !claimed.has(t));
    const parts = [primary[0]];
    if (secondary && secondary[1] >= primary[1] * 0.4) {
      parts.push(secondary[0]);
      claimed.add(secondary[0]);
    }
    clusterLabels.set(String(c), parts.map(prettyTag).join(" · "));
  }
  const nameCounts = new Map();
  for (const name of clusterLabels.values()) {
    for (const part of new Set([name, name.split(" · ")[0]])) {
      nameCounts.set(part, 1 + (nameCounts.get(part) || 0));
    }
  }
  overviewLabels.clear();
  for (const [id, name] of clusterLabels) {
    const primary = name.split(" · ")[0];
    const shortName = nameCounts.get(primary) === 1 ? primary : name;
    overviewLabels.set(id, nameCounts.get(shortName) === 1 ? shortName : `${shortName} (${id})`);
  }
}

const tagSpellings = new Map([["nba", "NBA"], ["ml", "ML"], ["llm", "LLM"], ["mcp", "MCP"], ["nextjs", "Next.js"]]);
function prettyTag(tag) {
  return String(tag)
    .replace(/[-_]+/g, " ")
    .replace(/\b\w+/g, word => tagSpellings.get(word.toLowerCase()) || word[0].toUpperCase() + word.slice(1));
}

const state = {
  graph: null,
  filtered: { nodes: [], edges: [], communityCounts: new Map() },
  highlightedId: null,
  adjacency: new Map(),
  search: "",
  typeFilter: "",
  tierFilter: "",
  communityFilter: "",
  checkpointClassFilter: "",
  staleOnly: false,
  includeArchived: false,
  beforeSearch: null,
  selectionVersion: 0,
  askVersion: 0,
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
    trackerStatus: "idle",
    disagreements: [],          // raw rows from /graph/checkpoint-tracker
    disagreeNodeIds: new Set(), // node ids with current!=recommended
    rowsByNodeId: new Map(),    // node id → tracker row (for the side panel)
  },
};

const COMMUNITY_PALETTE = ["#00ffd5", "#ffad00", "#009dff", "#ff16bd", "#9cff00", "#ff5326"];
const OTHER_COMMUNITIES_COLOR = "#9760ff";
const NEUTRAL = "#879ba5";
const classColors = new Map();

function nodeColor(node) {
  if (state.health.active) return classColors.get(node.checkpoint_class) || NEUTRAL;
  if (node.community == null || node.community === "") return NEUTRAL;
  return state.communityColors.get(node.community) || OTHER_COMMUNITIES_COLOR;
}

function isArchived(node) {
  return node.tier?.trim().toLowerCase() === "archive" ||
    node.retention_mode?.trim().toLowerCase() === "archive" ||
    /(?:^|\/)_?archiv(?:e|es|ed)\//i.test(node.path || node.id);
}

function scopeNodes() {
  return state.graph.nodes.filter(n => state.includeArchived || !isArchived(n));
}

const STALE_DAYS_THRESHOLD = 90;
const STALE_MS_THRESHOLD = STALE_DAYS_THRESHOLD * 24 * 60 * 60 * 1000;

// ---------- WebGL2 renderer wiring ---------------------------------------
// initWebgl() is called from loadGraph() once on first successful fetch.
async function initWebgl() {
  if (gpuRenderer) return gpuRenderer;
  const host = document.getElementById("graph-cosmos");
  if (!host) return null;
  host.removeAttribute("hidden");
  const canvasEl = document.getElementById("graph");
  if (canvasEl) canvasEl.style.display = "none";
  try {
    const mod = await import("./webgl-renderer.js?v=__BUILD_ID__");
    gpuRenderer = mod.createWebglRenderer({
      container: host,
      onPointClick: (node) => {
        if (state.pathMode) {
          handlePathClick(node);
        } else {
          selectNode(node);
        }
      },
      onBackgroundClick: () => {
        if (!state.pathMode) clearSelection();
      },
    });
    // Adaptive HTML label overlay over the canvas.
    try {
      const lblMod = await import("./labels-overlay.js?v=__BUILD_ID__");
      gpuLabels = lblMod.createLabelOverlay({
        container: host, renderer: gpuRenderer, communityLabel: overviewClusterLabel,
        colorOf: nodeColor, nodeRadiusPx: node => nodeDiameter(node) / 2,
      });
      gpuLabels.setOnLabelClick((node) => {
        if (state.pathMode) handlePathClick(node);
        else selectNode(node);
      });

    } catch (e) {
      console.warn("label overlay init failed:", e);
      gpuLabels = null;
    }
    gpuRenderer.onTransform((cam) => {
      gpuLabels?.layout(cam);
      document.getElementById("zoom-level").textContent = `${Math.round(cam.scale * 100)}%`;
    });
    // Debug hooks for headless tests + manual console inspection.
    window.__pwCam = () => gpuRenderer.getCamera();
    window.__pwNodes = () => gpuRenderer.getNodes();
    window.__pwBbox = () => gpuRenderer.getBbox && gpuRenderer.getBbox();
    window.__pwFit = () => gpuRenderer.fit && gpuRenderer.fit();
    window.__pwSampleNode = () => {
      // Find the node whose CSS-pixel screen position is closest to the
      // centre of the canvas (so a tap will reliably land on it).
      const cam = gpuRenderer.getCamera();
      const nodes = gpuRenderer.getNodes ? gpuRenderer.getNodes() : null;
      const canvas = host.querySelector("canvas");
      if (!nodes || !nodes.length || !canvas) return null;
      const rect = canvas.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      let best = null, bestD = Infinity;
      for (const n of nodes) {
        const sx = rect.left + rect.width / 2 + (n.x - cam.x) * cam.scale;
        const sy = rect.top + rect.height / 2 + (n.y - cam.y) * cam.scale;
        if (sx < rect.left + 30 || sx > rect.right - 30) continue;
        if (sy < rect.top + 80 || sy > rect.bottom - 100) continue;
        const d = (sx - cx) ** 2 + (sy - cy) ** 2;
        if (d < bestD) { bestD = d; best = { n, sx, sy }; }
      }
      if (!best) return null;
      return { x: Math.round(best.sx), y: Math.round(best.sy), id: best.n.id, title: best.n.title };
    };
    return gpuRenderer;
  } catch (e) {
    console.error("webgl renderer failed, falling back to canvas:", e);
    tryWebgl = false;
    gpuRenderer = null;
    host.replaceChildren();
    if (canvasEl) canvasEl.style.display = "";
    host.setAttribute("hidden", "");
    return null;
  }
}

function nodeDiameter(node) {
  const base = state.communityColors.has(node.community) ? 3 : 2.1;
  return Math.min(16, base + 1.05 * Math.sqrt(node.degree || 0));
}

function edgeStyle(r, g, b, alpha, width) {
  return { rgba: [r / 255, g / 255, b / 255, alpha], stroke: `rgba(${r},${g},${b},${alpha})`, width };
}
const edgeStyles = {
  normal: edgeStyle(151, 181, 184, 0.10, 0.75),
  dim: edgeStyle(129, 150, 156, 0.035, 0.75),
  neighbor: edgeStyle(120, 212, 192, 0.58, 1.2),
  path: edgeStyle(105, 240, 212, 0.93, 2.3),
  cross: edgeStyle(238, 161, 135, 0.75, 1.2),
};

function graphStyle() {
  const askActive = state.ask.active && state.ask.subgraphIds.size > 0;
  const dimNonPath = state.pathMode && state.pathNodes.size > 0;
  const selected = new Set(state.pathNodes);
  if (state.highlightedId) selected.add(state.highlightedId);
  if (askActive) for (const id of state.ask.nodeIds) selected.add(id);
  const pathEdges = new Set(state.pathEdges.map(e => askEdgeKey(e.source, e.target)));
  const neighborhood = state.adjacency.get(state.highlightedId);
  return {
    selected, neighborhood,
    focused: Boolean(state.search.trim() || selected.size || state.communityFilter),
    alphaOf(n) {
      if ((dimNonPath && !state.pathNodes.has(n.id)) || (askActive && !state.ask.subgraphIds.has(n.id)) ||
          (state.highlightedId && n.id !== state.highlightedId && !neighborhood?.has(n.id))) return 0.16;
      if (selected.has(n.id) || neighborhood?.has(n.id) || state.health.active) return 1;
      const base = state.communityColors.has(n.community) ? 0.87 : 0.77;
      return Math.min(1, base + 0.05 * Math.sqrt(n.degree || 0));
    },
    ringOf(n) {
      if (state.health.active && state.health.disagreeNodeIds.has(n.id)) return -1;
      return Number(selected.has(n.id));
    },
    edgeOf(e) {
      if (pathEdges.size || askActive) {
        const key = askEdgeKey(e.source, e.target);
        if (pathEdges.has(key) || (askActive && state.ask.edgeKeys.has(key))) return edgeStyles.path;
      }
      if (dimNonPath || askActive) return edgeStyles.dim;
      if (state.highlightedId) return e.source === state.highlightedId || e.target === state.highlightedId
        ? edgeStyles.neighbor : edgeStyles.dim;
      if (state.surprises && e.cross_community) return edgeStyles.cross;
      return edgeStyles.normal;
    },
  };
}

function syncGpuStyle() {
  const style = graphStyle();
  gpuRenderer.syncStyle({
    colorOf: nodeColor, sizeOf: nodeDiameter, alphaOf: style.alphaOf,
    ringOf: style.ringOf, edgeColorOf: edge => style.edgeOf(edge).rgba,
  });
  gpuLabels?.setPinned(style.selected, state.highlightedId, style.neighborhood, style.focused);
}

function isNodeStale(node, now = Date.now()) {
  const lv = (node.last_verified || "").trim();
  if (!lv) return true;
  const t = Date.parse(lv);
  if (Number.isNaN(t)) return true;
  return now - t > STALE_MS_THRESHOLD;
}

// Encode a node id (which may contain slashes like "concepts/foo") for use
// as a URL path segment. We keep literal slashes so origin-side routing
// + intermediaries (Cloudflare, Caddy) treat each segment as a real path
// component instead of a URL-encoded blob, while still escaping any other
// reserved characters in the slug.
function encodePathId(id) {
  return String(id).split("/").map(encodeURIComponent).join("/");
}

async function fetchJSON(path) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { credentials: "include" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
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

  const candidates = scopeNodes().filter((n) => {
    if (typeF && n.page_type !== typeF) return false;
    if (tierF && n.tier !== tierF) return false;
    if (ckptClassF && (n.checkpoint_class || "") !== ckptClassF) return false;
    if (staleOnly && !isNodeStale(n, now)) return false;
    if (!q) return true;
    const hay = (n.title + " " + (n.original_title || "") + " " + (n.tags || []).join(" ")).toLowerCase();
    return hay.includes(q);
  });
  const communityCounts = new Map();
  for (const node of candidates) {
    const id = String(node.community ?? "");
    communityCounts.set(id, (communityCounts.get(id) || 0) + 1);
  }
  const nodes = communityF ? candidates.filter(n => String(n.community) === communityF) : candidates;
  const ids = new Set(nodes.map((n) => n.id));
  const edges = state.graph.edges.filter((e) => ids.has(e.source) && ids.has(e.target));

  if (state.highlightedId && !ids.has(state.highlightedId)) {
    clearSelection({ redraw: false });
  }

  state.filtered = { nodes, edges, communityCounts };
  state.adjacency = buildAdjacency(edges);
  if (state.pathStart && (!ids.has(state.pathStart) || (state.pathEnd && !ids.has(state.pathEnd)) ||
      [...state.pathNodes].some(id => !ids.has(id)))) clearPathSelection({ redraw: false });
  if (gpuRenderer) {
    gpuRenderer.syncData(nodes, edges);
    gpuLabels?.setNodes(nodes);
  }
  fitViewToNodes({ all: Boolean(q) });
  if (!q && state.beforeSearch) {
    if (gpuRenderer) gpuRenderer.restoreCamera(state.beforeSearch);
    else { Object.assign(view, state.beforeSearch); updateZoomLevel(); }
    state.beforeSearch = null;
  }
  updateSearchResults(q);
  updateAskResultsList();
  updateStats();
  document.getElementById("scope-clear").hidden = !(q || typeF || tierF || communityF || ckptClassF || staleOnly || state.includeArchived);
  updateLegend();
  document.getElementById("empty-graph").hidden = nodes.length > 0;
  document.getElementById("empty-message").textContent = state.graph.nodes.length ? "No matching pages" : "The graph has no pages";
  document.getElementById("empty-clear").hidden = !state.graph.nodes.length;
  draw();
}

// ---------- Simple force-directed layout (Fruchterman-Reingold-ish) ---------

function positionNodes(nodes, edges) {
  const W = 2000, H = 2000;
  const k = Math.sqrt((W * H) / Math.max(nodes.length, 1)) * 0.8;

  const byId = new Map(nodes.map((n) => [n.id, n]));

  // Keep exported coordinates stable across searches and camera restoration.
  if (nodes.every(n => Number.isFinite(n.x) && Number.isFinite(n.y))) return;

  for (const n of nodes) {
    if (n.x == null || n.y == null) {
      n.x = Math.random() * W - W / 2;
      n.y = Math.random() * H - H / 2;
    }
    n.vx = 0; n.vy = 0;
  }

  const ITER = 120;
  let t = W / 10;
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
const view = { scale: 0.35, fitScale: 0.35, tx: 0, ty: 0 };
const MIN_SCALE = 0.05;
const MAX_SCALE = isCoarsePointer ? 6 : 4.5;
const ZOOM_STEP = 1.22;
let canvasFitExtent;

function clampScale(nextScale) {
  return Math.max(Math.min(MIN_SCALE, view.fitScale), Math.min(MAX_SCALE, nextScale));
}

function updateZoomLevel() {
  const label = document.getElementById("zoom-level");
  if (label) label.textContent = `${Math.round(view.scale * 100)}%`;
}

function nodeRadius(node) {
  return nodeDiameter(node) / (2 * view.scale);
}

function resize() {
  if (gpuRenderer) return; // webgl renderer manages its own canvas sizing
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const width = Math.round(canvas.clientWidth * dpr), height = Math.round(canvas.clientHeight * dpr);
  if (canvas.width === width && canvas.height === height) return;
  canvas.width = width;
  canvas.height = height;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  if (canvasFitExtent && width && height) {
    const oldScale = view.scale;
    const zoomRatio = oldScale / view.fitScale;
    view.fitScale = canvasFitScale();
    view.scale = clampScale(view.fitScale * zoomRatio);
    view.tx *= view.scale / oldScale;
    view.ty *= view.scale / oldScale;
  }
  updateZoomLevel();
  scheduleCanvasDraw();
}
new ResizeObserver(resize).observe(canvas);
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
  if (gpuRenderer) return;
  const worldPoint = screenToWorld(anchorX, anchorY);
  const clampedScale = clampScale(nextScale);
  view.scale = clampedScale;
  view.tx = anchorX - canvas.clientWidth / 2 - worldPoint.x * clampedScale;
  view.ty = anchorY - canvas.clientHeight / 2 - worldPoint.y * clampedScale;
  updateZoomLevel();
  scheduleCanvasDraw();
}

function canvasFitScale() {
  const gutter = isCoarsePointer ? 56 : 80;
  const width = canvas.clientWidth - 2 * Math.min(gutter, canvas.clientWidth * 0.14);
  const height = canvas.clientHeight - 2 * Math.min(gutter, canvas.clientHeight * 0.14);
  return Math.min(MAX_SCALE, width / canvasFitExtent.width, height / canvasFitExtent.height);
}

function fitViewToNodes({ all = true } = {}) {
  if (gpuRenderer) { gpuRenderer.fit({ all }); return; }
  const nodes = state.filtered.nodes;
  if (!nodes.length || !canvas.clientWidth || !canvas.clientHeight) return;

  const bounds = graphBounds(nodes, all);
  if (!bounds) return;
  const { minX, maxX, minY, maxY } = bounds.view;

  canvasFitExtent = { width: Math.max(maxX - minX, 120), height: Math.max(maxY - minY, 120) };
  const nextScale = canvasFitScale();
  const targetX = canvas.clientWidth / 2;
  const targetY = !all && isCoarsePointer ? canvas.clientHeight * 0.46 : canvas.clientHeight / 2;
  const centerX = (minX + maxX) / 2;
  const centerY = (minY + maxY) / 2;

  view.fitScale = nextScale;
  view.scale = nextScale;
  view.tx = targetX - canvas.clientWidth / 2 - centerX * nextScale;
  view.ty = targetY - canvas.clientHeight / 2 - centerY * nextScale;
  updateZoomLevel();
  scheduleCanvasDraw();
}

function centerNodeInView(node) {
  const stage = document.getElementById("graph-stage").getBoundingClientRect();
  const panel = document.getElementById("node-panel");
  const reader = panel.getBoundingClientRect();
  let targetX = stage.width / 2, targetY = stage.height / 2;
  if (reader.left <= stage.left && reader.right >= stage.right) {
    // The sheet can grow after the page and neighbors finish loading.
    const top = reader.bottom - parseFloat(getComputedStyle(panel).maxHeight);
    targetY = Math.max(26, (top - stage.top) / 2);
  } else {
    targetX = Math.min(targetX, Math.max(26, (reader.left - stage.left) / 2));
  }
  if (gpuRenderer) { gpuRenderer.focusNode(node.id, targetX, targetY); return; }
  view.tx = targetX - stage.width / 2 - node.x * view.scale;
  view.ty = targetY - stage.height / 2 - node.y * view.scale;
}

// ---------- Path mode (R13) -----------------------------------------------

function buildAdjacency(edges) {
  const adj = new Map();
  for (const e of edges) {
    if (!adj.has(e.source)) adj.set(e.source, new Set());
    if (!adj.has(e.target)) adj.set(e.target, new Set());
    adj.get(e.source).add(e.target);
    adj.get(e.target).add(e.source);
  }
  return adj;
}

function bfsShortestPath(startId, endId, adj) {
  if (startId === endId) return [startId];
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

function appendPageButton(list, node, text, onClick) {
  const li = document.createElement("li");
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = text;
  button.title = node.title || node.id;
  button.addEventListener("click", () => onClick(node));
  li.appendChild(button);
  list.appendChild(li);
  return button;
}

function clearAskResults({ redraw = true } = {}) {
  state.askVersion++;
  state.ask.active = false;
  state.ask.nodeIds.clear();
  state.ask.subgraphIds.clear();
  state.ask.edgeKeys.clear();
  state.ask.results = [];
  document.getElementById("ask-results").classList.add("hidden");
  document.getElementById("ask-results-list").replaceChildren();
  document.getElementById("ask-graph-clear").classList.add("hidden");
  if (redraw) draw();
}

function updateAskResultsList() {
  if (!state.ask.active) return;
  const list = document.getElementById("ask-results-list");
  list.replaceChildren();
  const known = new Map(scopeNodes().map(n => [n.id, n]));
  const results = state.ask.results.filter(result => known.has(result.id));
  document.getElementById("ask-meta").textContent = results.length
    ? `${results.length} matching ${results.length === 1 ? "page" : "pages"} · ${state.ask.backend}`
    : "No matching pages.";
  for (const result of results) {
    const node = known.get(result.id);
    appendPageButton(list, node, node.title, navigateToNode);
  }
}

async function runAskGraph(q) {
  clearAskResults();
  const text = (q || "").trim();
  if (!text) return;
  const version = state.askVersion;
  const meta = document.getElementById("ask-meta");
  document.getElementById("ask-results").classList.remove("hidden");
  document.getElementById("ask-graph-clear").classList.remove("hidden");
  meta.textContent = "Searching…";
  try {
    const res = await fetch(`${API_BASE}/graph/query`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ q: text, k: 10, include_archived: state.includeArchived }),
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = await res.json();
    if (version !== state.askVersion) return;
    if (data.error) throw new Error(data.error);
    state.ask.active = true;
    state.ask.backend = data.backend;
    state.ask.results = data.nodes || [];
    state.ask.nodeIds = new Set(state.ask.results.map(n => n.id));
    if (state.ask.nodeIds.size) {
      state.ask.subgraphIds = new Set([...state.ask.nodeIds, ...(data.subgraph?.nodes || []).map(n => n.id)]);
      state.ask.edgeKeys = new Set((data.subgraph?.edges || []).map(e => askEdgeKey(e.source, e.target)));
    }
    updateAskResultsList();
    draw();
  } catch (e) {
    if (version === state.askVersion) meta.textContent = `Query unavailable: ${e.message}`;
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
      state.health.trackerStatus = "unavailable";
      state.health.disagreements = [];
      state.health.disagreeNodeIds = new Set();
      state.health.rowsByNodeId = new Map();
      return;
    }
    state.health.trackerStatus = "available";
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
    state.health.trackerStatus = "unavailable";
    state.health.disagreements = [];
    state.health.disagreeNodeIds = new Set();
    state.health.rowsByNodeId = new Map();
  }
}

function enterCheckpointHealth() {
  state.health.active = true;
  document.getElementById("checkpoint-health-toggle")?.setAttribute("aria-pressed", "true");
  // Lazy-load the tracker the first time we enter the overlay.
  if (["idle", "unavailable"].includes(state.health.trackerStatus)) {
    state.health.trackerStatus = "loading";
    loadCheckpointTracker().then(() => {
      if (!state.health.active) return;
      if (state.highlightedId) showCheckpointDetail({ id: state.highlightedId });
      updateLegend();
      draw();
    });
  }
  updateLegend();
  draw();
}
function exitCheckpointHealth() {
  state.health.active = false;
  document.getElementById("checkpoint-health-toggle")?.setAttribute("aria-pressed", "false");
  document.getElementById("checkpoint-detail")?.classList.add("hidden");
  updateLegend();
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
    const path = bfsShortestPath(state.pathStart, state.pathEnd, state.adjacency);
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

let canvasFrame = 0;
let canvasStyle;
let edgePaths;

function scheduleCanvasDraw() {
  if (!canvasFrame) canvasFrame = requestAnimationFrame(drawCanvas);
}

function draw() {
  if (gpuRenderer) { syncGpuStyle(); return; }
  canvasStyle = null;
  scheduleCanvasDraw();
}

function buildEdgePaths(nodes, edges, style) {
  const byId = new Map(nodes.map(node => [node.id, node]));
  const paths = new Map();
  for (const edge of edges) {
    const a = byId.get(edge.source), b = byId.get(edge.target);
    if (!a || !b) continue;
    const paint = style.edgeOf(edge);
    if (!paths.has(paint)) paths.set(paint, new Path2D());
    const path = paths.get(paint);
    path.moveTo(a.x, a.y);
    path.lineTo(b.x, b.y);
  }
  return paths;
}

// Rasterize each hue once so panning does not rebuild a blur for every node.
const glowSprites = new Map();
function glowSprite(color) {
  if (glowSprites.has(color)) return glowSprites.get(color);
  const sprite = document.createElement("canvas");
  sprite.width = sprite.height = 80;
  const paint = sprite.getContext("2d");
  const glow = paint.createRadialGradient(40, 40, 0, 40, 40, 40);
  for (const [position, opacity] of [[0, 1], [0.42, 1], [0.47, 0.26], [0.62, 0.13], [0.82, 0.035], [1, 0]]) {
    glow.addColorStop(position, `rgba(255,255,255,${opacity})`);
  }
  paint.fillStyle = glow;
  paint.fillRect(0, 0, 80, 80);
  paint.globalCompositeOperation = "source-in";
  paint.fillStyle = color;
  paint.fillRect(0, 0, 80, 80);
  paint.globalCompositeOperation = "source-over";
  const core = paint.createRadialGradient(40, 40, 0, 40, 40, 8);
  core.addColorStop(0, "rgba(255,255,255,0.86)");
  core.addColorStop(1, "rgba(255,255,255,0)");
  paint.fillStyle = core;
  paint.fillRect(32, 32, 16, 16);
  glowSprites.set(color, sprite);
  return sprite;
}

function drawCanvas() {
  canvasFrame = 0;
  if (gpuRenderer) return;
  const width = canvas.clientWidth, height = canvas.clientHeight;
  ctx.clearRect(0, 0, width, height);
  const { nodes, edges } = state.filtered;
  state.visibleNodes = [];
  state.labelTargets = [];
  if (!nodes.length || !width || !height) return;

  if (!canvasStyle) {
    canvasStyle = graphStyle();
    edgePaths = buildEdgePaths(nodes, edges, canvasStyle);
  }
  const bounds = visibleWorldBounds();
  const visibleNodes = nodes.filter(node => isNodeVisible(node, bounds, 20 / view.scale));
  state.visibleNodes = visibleNodes;
  ctx.save();
  ctx.translate(width / 2 + view.tx, height / 2 + view.ty);
  ctx.scale(view.scale, view.scale);
  // Draw highlighted connections above the rest, regardless of export order.
  for (const paint of [edgeStyles.normal, edgeStyles.dim, edgeStyles.cross, edgeStyles.neighbor, edgeStyles.path]) {
    const path = edgePaths.get(paint);
    if (!path) continue;
    ctx.strokeStyle = paint.stroke;
    ctx.lineWidth = paint.width / view.scale;
    ctx.stroke(path);
  }

  for (const n of visibleNodes) {
    const r = nodeRadius(n);
    const selected = canvasStyle.selected.has(n.id);
    const disagreement = state.health.active && state.health.disagreeNodeIds.has(n.id);
    ctx.globalAlpha = canvasStyle.alphaOf(n);
    const glowRadius = 2.2 * r;
    ctx.drawImage(glowSprite(nodeColor(n)), n.x - glowRadius, n.y - glowRadius, 2 * glowRadius, 2 * glowRadius);
    if (selected || disagreement) {
      ctx.lineWidth = 1.6 / view.scale;
      ctx.strokeStyle = disagreement ? "#ff6969" : "#c6fff2";
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 2 / view.scale, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
  ctx.globalAlpha = 1;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  state.labelTargets = buildLabelTargets({
    nodes, highlightedId: state.highlightedId, pinnedIds: canvasStyle.selected,
    neighbors: canvasStyle.neighborhood, focused: canvasStyle.focused, communityLabel: overviewClusterLabel,
    canvasSize: { width, height }, view, nodeRadius,
    measureText(label, fontWorldPx) {
      ctx.font = `500 ${fontWorldPx}px sans-serif`;
      return ctx.measureText(label).width;
    },
  });

  for (const target of state.labelTargets) {
    const { node, label, highlighted, community, fontWorldPx, chipRadius, worldRect } = target;
    ctx.font = `500 ${fontWorldPx}px sans-serif`;
    ctx.fillStyle = highlighted ? "rgba(20,46,48,.98)" : "rgba(16,29,33,.92)";
    ctx.strokeStyle = highlighted ? "#66d2bb" : "rgba(121,160,157,.34)";
    ctx.lineWidth = (highlighted ? 1.5 : 1) / view.scale;
    pathRoundedRect(worldRect.x, worldRect.y, worldRect.w, worldRect.h, chipRadius);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = community ? nodeColor(node) : "#e5efee";
    ctx.fillText(label, node.x, worldRect.y + worldRect.h / 2);
  }

  ctx.restore();
}

function findNode(id) {
  return state.filtered.nodes.find((n) => n.id === id);
}

let detailOpener = null;
function clearSelection({ redraw = true } = {}) {
  state.selectionVersion++;
  const panel = document.getElementById("node-panel");
  const restoreFocus = panel.contains(document.activeElement);
  state.highlightedId = null;
  panel.classList.add("hidden");
  document.getElementById("checkpoint-detail").classList.add("hidden");
  if (restoreFocus) {
    const fallback = document.getElementById(mobileDrawer.matches ? "sidebar-toggle" : "search");
    (detailOpener?.matches("button, a, input, select, [tabindex]") && detailOpener.isConnected && detailOpener.getClientRects().length && !detailOpener.closest("[inert]") ? detailOpener : fallback).focus();
  }
  detailOpener = null;
  if (redraw) draw();
}

function navigateToNode(node) {
  if (!findNode(node.id)) resetFilters({ includeArchived: state.includeArchived });
  if (state.pathMode) {
    if (mobileDrawer.matches) closeSidebar();
    handlePathClick(node);
  } else {
    selectNode(node);
  }
}

function selectNode(node) {
  const panel = document.getElementById("node-panel");
  if (!panel.contains(document.activeElement)) detailOpener = document.activeElement;
  if (mobileDrawer.matches && document.body.classList.contains("sidebar-open")) closeSidebar(false);
  state.highlightedId = node.id;
  showNodePanel(node);
  centerNodeInView(node);
  if (state.health.active) showCheckpointDetail(node);
  draw();
}

// ---------- Interactions ---------------------------------------------------

// Unified pointer handling so mouse, touch, and pen all share one code path.
// We track active pointers in a Map to support pinch-to-zoom on touch devices.
const activePointers = new Map(); // pointerId -> {x, y}
let previousPinch;
let panPointerId = null;
let panLastX = 0, panLastY = 0;
let pointerDownAt = 0;
let pointerDownX = 0, pointerDownY = 0;
let pointerMoved = false;
const TAP_MAX_MS = 500;

function pinchGeometry() {
  const [a, b] = activePointers.values();
  const rect = canvas.getBoundingClientRect();
  return { x: (a.x + b.x) / 2 - rect.left, y: (a.y + b.y) / 2 - rect.top,
    distance: Math.hypot(a.x - b.x, a.y - b.y) };
}

canvas.addEventListener("pointerdown", (e) => {
  if (gpuRenderer || e.button !== 0) return;
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
    pointerMoved = true;
    previousPinch = pinchGeometry();
    panPointerId = null; // Pinch mode — disable single-finger pan.
  }
});

canvas.addEventListener("pointermove", (e) => {
  if (gpuRenderer) return;
  if (!activePointers.has(e.pointerId)) return;
  activePointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

  if (activePointers.size >= 2 && previousPinch) {
    const pinch = pinchGeometry();
    view.tx += pinch.x - previousPinch.x;
    view.ty += pinch.y - previousPinch.y;
    const factor = previousPinch.distance > 0 ? pinch.distance / previousPinch.distance : 1;
    setScale(view.scale * factor, pinch.x, pinch.y);
    previousPinch = pinch;
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
    scheduleCanvasDraw();
  }
});

function endPointer(e) {
  if (gpuRenderer) return;
  if (!activePointers.has(e.pointerId)) return;
  activePointers.delete(e.pointerId);

  // If this was a quick, near-stationary press, treat it as a tap.
  if (
    e.type === "pointerup" && e.pointerId === panPointerId &&
    !pointerMoved &&
    performance.now() - pointerDownAt < TAP_MAX_MS
  ) {
    handleTap(e.clientX, e.clientY);
  }

  previousPinch = activePointers.size >= 2 ? pinchGeometry() : null;
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
  if (gpuRenderer) return;
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

function showNodePanel(node, { focus = true } = {}) {
  const version = ++state.selectionVersion;
  const panel = document.getElementById("node-panel");
  panel.classList.remove("hidden");
  if (focus) panel.querySelector(".reader-body").scrollTop = 0;
  document.getElementById("node-title").textContent = node.title;
  if (focus) document.getElementById("node-title").focus({ preventScroll: true });
  document.getElementById("node-meta").textContent = [node.page_type, node.tier,
    Number.isFinite(node.degree) && `${node.degree} links`, clusterLabel(node.community)].filter(Boolean).join(" · ");
  const summary = document.getElementById("node-summary");
  summary.textContent = "";
  fetchPage();
  fetchNeighbors();

  async function fetchPage() {
    const content = document.getElementById("node-content");
    content.textContent = "Loading page…";
    try {
      const data = await fetchJSON(`/graph/page/${encodePathId(node.id)}`);
      if (version !== state.selectionVersion) return;
      content.innerHTML = renderMarkdown(data.body || "");
      const heading = content.firstElementChild;
      if (heading?.tagName === "H1" && displayTitle(heading.textContent.trim()) === node.title) heading.remove();
      // The page summary is often the (possibly truncated) opening paragraph.
      // Keep the full rendered paragraph and its links when they overlap.
      const opening = content.querySelector("p")?.textContent.trim();
      summary.textContent = data.summary || "";
      const intro = (data.summary || "").replace(/(?:\.\.\.|…)$/, "").trim();
      const plainIntro = document.createElement("div");
      plainIntro.innerHTML = renderMarkdown(intro);
      if (intro && opening?.startsWith(plainIntro.textContent.trim())) summary.textContent = "";
      const pages = scopeNodes();
      const titles = new Map();
      for (const page of pages) {
        titles.set(page.title.toLowerCase(), page);
        titles.set(page.original_title.toLowerCase(), page);
      }
      for (const link of content.querySelectorAll("a.wikilink")) {
        const raw = link.dataset.target;
        let target = raw;
        let local;
        while (target) {
          local = titles.get(target.toLowerCase());
          if (local) break;
          const separator = Math.max(target.lastIndexOf("|"), target.lastIndexOf("#"));
          if (separator < 0) break;
          target = target.slice(0, separator).trimEnd();
        }
        if (local && raw.slice(target.length).indexOf("|") === -1) link.textContent = local.title;
        if (!local) {
          const slug = target.toLowerCase().replace(/\s+/g, "-").replace(/\.md$/, "");
          local = raw.startsWith("#") ? node : pages.find(n => n.id === target || n.id.endsWith("/" + slug));
        }
        if (local) link.addEventListener("click", e => { e.preventDefault(); navigateToNode(local); });
        else link.replaceWith(document.createTextNode(link.textContent));
      }
    } catch (e) {
      if (version === state.selectionVersion) content.textContent = `Page unavailable: ${e.message}`;
    }
  }

  async function fetchNeighbors() {
    const list = document.getElementById("node-neighbors");
    list.textContent = "Loading…";
    try {
      const data = await fetchJSON(`/graph/neighbors/${encodePathId(node.id)}?depth=1`);
      if (version !== state.selectionVersion) return;
      const known = new Map(scopeNodes().map(n => [n.id, n]));
      list.replaceChildren();
      for (const item of data.nodes) {
        const neighbor = known.get(item.id);
        if (neighbor && neighbor.id !== node.id) appendPageButton(list, neighbor, neighbor.title, navigateToNode);
      }
      if (!list.childElementCount) list.textContent = "No neighbors in this view.";
    } catch (e) {
      if (version === state.selectionVersion) list.textContent = `Neighbors unavailable: ${e.message}`;
    }
  }
}

// ---------- UI wiring ------------------------------------------------------

function countsBy(nodes, field) {
  const counts = new Map();
  for (const n of nodes) {
    const value = n[field];
    if (value !== "" && value != null) counts.set(value, 1 + (counts.get(value) || 0));
  }
  return [...counts].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])));
}

function populateFilters() {
  const nodes = scopeNodes();
  enrichGraph({ nodes });
  function options(id, key, values, label = String) {
    const select = document.getElementById(id);
    select.length = 1;
    for (const [value] of values) select.add(new Option(label(value), String(value)));
    select.value = state[key];
    state[key] = select.value;
  }
  const communities = countsBy(nodes, "community");
  state.communityColors = new Map(communities.slice(0, COMMUNITY_PALETTE.length).map(([c], i) => [c, COMMUNITY_PALETTE[i]]));
  const classes = countsBy(nodes, "checkpoint_class");
  classColors.clear();
  classes.forEach(([name], i) => classColors.set(name, COMMUNITY_PALETTE[i] || `hsl(${Math.round(i * 137.5) % 360} 85% 68%)`));
  options("type-filter", "typeFilter", countsBy(nodes, "page_type"));
  options("tier-filter", "tierFilter", countsBy(nodes, "tier"));
  options("community-filter", "communityFilter", communities, clusterLabel);
  options("checkpoint-class-filter", "checkpointClassFilter", classes);
}

const SEARCH_BATCH_SIZE = 24;
let searchScope = "";
let searchResultLimit = SEARCH_BATCH_SIZE;

function updateSearchResults(q) {
  const list = document.getElementById("search-results");
  const meta = document.getElementById("search-meta");
  const scope = JSON.stringify([q, state.typeFilter, state.tierFilter, state.communityFilter,
    state.checkpointClassFilter, state.staleOnly, state.includeArchived]);
  const sameScope = scope === searchScope;
  if (!sameScope) searchResultLimit = SEARCH_BATCH_SIZE;
  searchScope = scope;
  const active = list.contains(document.activeElement) ? document.activeElement : null;
  const oldIndex = active ? [...list.children].indexOf(active.parentElement) : -1;
  const scrollTop = sameScope ? list.scrollTop : 0;
  list.replaceChildren();
  list.hidden = !q || !state.filtered.nodes.length;
  if (list.hidden) {
    meta.textContent = q ? "0 matching pages" : "";
    if (active) document.getElementById("search").focus();
    return;
  }
  const nodes = [...state.filtered.nodes].sort((a, b) => a.title.localeCompare(b.title));
  meta.textContent = `${nodes.length} matching ${nodes.length === 1 ? "page" : "pages"}`;
  const activeId = sameScope && active?.dataset.nodeId;
  const focusedIndex = activeId ? nodes.findIndex(n => n.id === activeId) : -1;
  searchResultLimit = Math.max(searchResultLimit, focusedIndex + 1);

  let shown = 0;
  const moreRow = document.createElement("li");
  const more = document.createElement("button");
  more.type = "button";
  more.className = "search-more";
  moreRow.appendChild(more);
  more.addEventListener("click", () => {
    searchResultLimit = shown + SEARCH_BATCH_SIZE;
    appendBatch().focus();
  });

  function appendBatch() {
    moreRow.remove();
    const batch = document.createDocumentFragment();
    const end = Math.min(searchResultLimit, nodes.length);
    for (; shown < end; shown++) {
      const node = nodes[shown];
      appendPageButton(batch, node, node.title, navigateToNode).dataset.nodeId = node.id;
    }
    const firstNew = batch.querySelector("button");
    list.appendChild(batch);
    if (shown < nodes.length) {
      more.textContent = `Show more (${nodes.length - shown} remaining)`;
      list.appendChild(moreRow);
    }
    return firstNew;
  }
  appendBatch();
  list.scrollTop = scrollTop;
  if (active) {
    const nearest = Math.min(shown - 1, Math.max(0, focusedIndex < 0 ? oldIndex : focusedIndex));
    const keepMore = sameScope && active.classList.contains("search-more") && more.isConnected;
    (keepMore ? more : list.children[nearest].firstElementChild).focus();
  }
}

function updateStats() {
  const {nodes, edges} = state.filtered;
  for (const [unit, singular, count] of [
    ["pages", "page", nodes.length],
    ["edges", "edge", edges.length],
    ["communities", "community", countsBy(nodes, "community").length],
  ]) {
    const number = document.getElementById(`stat-${unit}`);
    number.textContent = count.toLocaleString();
    number.nextElementSibling.textContent = count === 1 ? singular : unit;
  }
}

function updateLegend() {
  if (!state.graph) return;
  const el = document.getElementById("legend");
  const focusedCommunity = document.activeElement?.dataset.community;
  el.replaceChildren();
  const { nodes, communityCounts } = state.filtered;
  const health = state.health.active;
  const heading = document.createElement("h3");
  heading.textContent = health ? "Checkpoint health" : "Communities";
  el.setAttribute("aria-label", health ? "Checkpoint health of visible pages" : "Filter by community, with page counts matching the other filters");
  el.appendChild(heading);
  function row(label, count, color, community = null) {
    const item = document.createElement(community === null ? "div" : "button");
    item.className = "legend-row";
    if (community !== null) {
      const pressed = state.communityFilter === community;
      item.type = "button";
      item.dataset.community = community;
      item.setAttribute("aria-pressed", String(pressed));
      item.disabled = !count && !pressed;
      item.addEventListener("click", () => {
        const select = document.getElementById("community-filter");
        select.value = pressed ? "" : community;
        select.dispatchEvent(new Event("change", { bubbles: true }));
      });
    }
    const swatch = document.createElement("span");
    swatch.className = "swatch";
    swatch.style.backgroundColor = color;
    const name = document.createElement("span");
    name.className = "legend-name";
    name.textContent = label;
    const number = document.createElement("span");
    number.className = "count";
    number.textContent = count.toLocaleString();
    item.append(swatch, name, number);
    el.appendChild(item);
    if (focusedCommunity === community) item.focus({ preventScroll: true });
    return item;
  }
  if (!health) {
    const remaining = new Map(communityCounts);
    const communities = new Map([...state.communityColors].map(([value, color]) => [String(value), color]));
    if (state.communityFilter && !communities.has(state.communityFilter)) {
      communities.set(state.communityFilter, OTHER_COMMUNITIES_COLOR);
    }
    for (const [value, color] of communities) {
      row(clusterLabel(value), remaining.get(value) || 0, color, value);
      remaining.delete(value);
    }
    const unassigned = remaining.get("") || 0;
    remaining.delete("");
    const other = [...remaining.values()].reduce((sum, count) => sum + count, 0);
    if (other) row("Other communities", other, OTHER_COMMUNITIES_COLOR);
    if (unassigned) row("No community", unassigned, NEUTRAL);
    if (focusedCommunity && !communities.has(focusedCommunity)) {
      const select = document.getElementById("community-filter");
      const fallback = el.querySelector("button:enabled") || document.getElementById("search");
      (select.checkVisibility() ? select : fallback).focus();
    }
    return;
  }

  let unclassified = nodes.length;
  for (const [value, count] of countsBy(nodes, "checkpoint_class")) {
    row(value, count, classColors.get(value));
    unclassified -= count;
  }
  if (unclassified) row("Unclassified", unclassified, NEUTRAL);
  if (state.health.trackerStatus === "available") {
    row("Disagreement ring", nodes.filter(n => state.health.disagreeNodeIds.has(n.id)).length, "#ef6666").classList.add("disagreement");
  } else {
    const status = document.createElement("span");
    status.className = "muted";
    status.textContent = state.health.trackerStatus === "loading" ? "Loading disagreements…" : "Disagreement data unavailable";
    el.appendChild(status);
  }
}

// Export freshness and the update stream have separate failure modes.
let graphStatus = "Loading graph";
let streamStatus = "Connected";
function updateConnection() {
  const text = graphStatus || streamStatus;
  const el = document.getElementById("connection-state");
  el.textContent = text;
  el.dataset.state = text === "Live" ? "live" : text === "Loading graph" || text === "Connected" ? "loading" : "warning";
}

let loadVersion = 0;
async function loadGraph() {
  const version = ++loadVersion;
  graphStatus = "Loading graph";
  updateConnection();
  if (!state.graph) {
    document.getElementById("empty-graph").hidden = false;
    document.getElementById("empty-message").textContent = "Loading graph…";
    document.getElementById("empty-clear").hidden = true;
  }
  try {
    const overview = await fetchJSON("/graph/overview");
    if (version !== loadVersion) return;
    const { nodes, links } = overview;
    if (!Array.isArray(nodes) || !Array.isArray(links) ||
        !nodes.every(n => typeof n?.id === "string" && typeof n.title === "string")) {
      throw new Error("Invalid graph overview");
    }
    const edges = links.map(([a, b, cross_community]) => {
      if (!Number.isInteger(a) || !Number.isInteger(b) || !nodes[a] || !nodes[b]) {
        throw new Error("Invalid graph edge");
      }
      return { source: nodes[a].id, target: nodes[b].id, cross_community };
    });
    const graph = { nodes, edges };
    state.graph = graph;
    if (tryWebgl) await initWebgl();
    if (version !== loadVersion) return;
    if (!gpuRenderer) positionNodes(graph.nodes, graph.edges);
    populateFilters();
    resize();
    applyFilters();
    if (state.highlightedId) showNodePanel(findNode(state.highlightedId), { focus: false });
    graphStatus = "";
    updateConnection();
  } catch {
    if (version !== loadVersion) return;
    graphStatus = state.graph ? "Reload failed" : "Graph unavailable";
    updateConnection();
    if (!state.graph) document.getElementById("empty-message").textContent = "Graph unavailable. Reload to try again.";
    return;
  }
  const buildTime = document.getElementById("build-time");
  try {
    const stats = await fetchJSON("/graph/stats");
    if (version !== loadVersion) return;
    const timestamp = Date.parse(stats.last_rebuild);
    buildTime.textContent = Number.isFinite(timestamp)
      ? `Last rebuild ${new Date(timestamp).toLocaleString()}` : "Last rebuild unavailable";
    if (stats.sync_status === "error") {
      graphStatus = "Graph refresh failed";
      updateConnection();
    }
  } catch {
    if (version === loadVersion) buildTime.textContent = "Last rebuild unavailable";
  }
}

function resetFilters({ includeArchived = false } = {}) {
  const archiveChanged = state.includeArchived !== includeArchived;
  state.includeArchived = includeArchived;
  state.search = state.typeFilter = state.tierFilter = state.communityFilter = state.checkpointClassFilter = "";
  state.staleOnly = state.surprises = false;
  for (const id of ["search", "type-filter", "tier-filter", "community-filter", "checkpoint-class-filter"]) {
    document.getElementById(id).value = "";
  }
  document.getElementById("stale-only-toggle").checked = false;
  document.getElementById("surprises-toggle").checked = false;
  document.getElementById("archive-toggle").checked = includeArchived;
  if (archiveChanged && state.graph) {
    populateFilters();
    clearAskResults({ redraw: false });
  }
  applyFilters();
}

function bindUI() {
  const search = document.getElementById("search");
  search.addEventListener("input", (e) => {
    if (state.graph && !state.search.trim() && e.target.value.trim()) {
      state.beforeSearch = gpuRenderer ? gpuRenderer.getCamera() : { ...view };
    }
    state.search = e.target.value;
    applyFilters();
  });
  search.addEventListener("keydown", e => {
    const first = document.querySelector("#search-results button");
    if (e.key === "ArrowDown" && first) { e.preventDefault(); first.focus(); }
    if (e.key === "Enter" && first) { e.preventDefault(); first.click(); }
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
  document.getElementById("archive-toggle").addEventListener("change", e => {
    state.includeArchived = e.target.checked;
    if (!state.graph) return;
    populateFilters();
    clearAskResults({ redraw: false });
    applyFilters();
    if (state.highlightedId) showNodePanel(findNode(state.highlightedId), { focus: false });
  });
  document.getElementById("clear-filters").addEventListener("click", () => resetFilters());
  for (const id of ["empty-clear", "scope-clear"]) {
    document.getElementById(id).addEventListener("click", () => {
      resetFilters();
      document.getElementById(mobileDrawer.matches ? "sidebar-toggle" : "search").focus({ preventScroll: true });
    });
  }
  document.getElementById("rebuild-btn").addEventListener("click", () => loadGraph());
  document.getElementById("zoom-in").addEventListener("click", () => {
    if (gpuRenderer) gpuRenderer.zoomBy(1.5);
    else setScale(view.scale * ZOOM_STEP);
  });
  document.getElementById("zoom-out").addEventListener("click", () => {
    if (gpuRenderer) gpuRenderer.zoomBy(1 / 1.5);
    else setScale(view.scale / ZOOM_STEP);
  });
  document.getElementById("zoom-fit").addEventListener("click", () => fitViewToNodes());
  document.getElementById("path-mode-toggle")?.addEventListener("click", () => {
    if (state.pathMode) exitPathMode(); else enterPathMode();
  });
  document.getElementById("path-panel-close")?.addEventListener("click", () => exitPathMode());
  document.getElementById("ask-graph").addEventListener("input", () => clearAskResults());
  document.getElementById("ask-form").addEventListener("submit", e => {
    e.preventDefault();
    runAskGraph(document.getElementById("ask-graph").value);
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
  closeBtn?.addEventListener("click", () => closeSidebar());
  backdrop?.addEventListener("click", () => closeSidebar());
  mobileDrawer.addEventListener("change", () => closeSidebar(false));
  closeSidebar(false);
  // Allow Esc to dismiss the drawer for keyboard users.
  document.addEventListener("keydown", (e) => {
    if (e.key === "Tab" && document.body.classList.contains("sidebar-open")) {
      const focusable = [...document.querySelectorAll("#sidebar button, #sidebar input, #sidebar select, #sidebar summary")]
        .filter(el => !el.disabled && el.checkVisibility());
      const first = focusable[0], last = focusable.at(-1);
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    } else if (e.key === "Escape" && document.body.classList.contains("sidebar-open")) {
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

const mobileDrawer = window.matchMedia("(max-width: 900px)");
function openSidebar() {
  if (!mobileDrawer.matches) return;
  document.body.classList.add("sidebar-open");
  const sidebar = document.getElementById("sidebar");
  sidebar.inert = false;
  sidebar.setAttribute("role", "dialog");
  sidebar.setAttribute("aria-modal", "true");
  document.querySelector(".masthead").inert = true;
  document.getElementById("canvas-host").inert = true;
  document.getElementById("node-panel").inert = true;
  document.getElementById("sidebar-backdrop").hidden = false;
  document.getElementById("sidebar-toggle").setAttribute("aria-expanded", "true");
  document.getElementById("search").focus({ preventScroll: true });
}
function closeSidebar(restoreFocus = true) {
  const sidebar = document.getElementById("sidebar");
  const toggle = document.getElementById("sidebar-toggle");
  const hadFocus = sidebar.contains(document.activeElement);
  document.body.classList.remove("sidebar-open");
  sidebar.removeAttribute("role");
  sidebar.removeAttribute("aria-modal");
  sidebar.inert = mobileDrawer.matches;
  document.querySelector(".masthead").inert = false;
  document.getElementById("canvas-host").inert = false;
  document.getElementById("node-panel").inert = false;
  document.getElementById("sidebar-backdrop").hidden = true;
  toggle.setAttribute("aria-expanded", "false");
  if (mobileDrawer.matches && (restoreFocus || hadFocus)) toggle.focus();
}

function subscribeSSE() {
  try {
    const src = new EventSource(`${API_BASE}/events`, { withCredentials: true });
    src.addEventListener("graph-updated", () => loadGraph());
    src.addEventListener("hello", () => {
      streamStatus = "Live";
      updateConnection();
    });
    src.onerror = () => {
      streamStatus = "Reconnecting";
      updateConnection();
    };
  } catch (e) {
    // SSE unsupported; static load is still fine.
  }
}

bindUI();
loadGraph().then(subscribeSSE);
