// Minimal labs-wiki graph viewer.
// Deliberately dependency-free: uses the browser's Canvas API and a small
// force-directed layout so the image ships as pure static HTML/CSS/JS behind
// nginx, with zero build step. If node counts grow past a few thousand, swap
// the renderer for @cosmograph/cosmograph per Phase G3.

import { buildLabelTargets, pickNodeAtScreenPoint } from "./interaction-targets.js";
import {
  hasPointerMovedEnough,
  shouldUseCoarsePointerTapSlop,
} from "./pointer-gesture.js";

const cfg = window.__WIKI_GRAPH_CONFIG || {};
// If apiBase is literally the placeholder (image built but entrypoint didn't
// run), fall back to same-origin — the UI still works when served from the
// same host as the API.
const API_BASE = (cfg.apiBase && !cfg.apiBase.includes("__API_BASE__"))
  ? cfg.apiBase.replace(/\/$/, "")
  : "";

const state = {
  graph: null,
  filtered: { nodes: [], edges: [] },
  highlightedId: null,
  search: "",
  typeFilter: "",
  tierFilter: "",
  surprises: false,
  communityColors: new Map(),
  visibleNodes: [],
  labelTargets: [],
};

async function fetchJSON(path) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { credentials: "include" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

function colorForCommunity(community) {
  if (state.communityColors.has(community)) return state.communityColors.get(community);
  // Evenly spaced hues; golden-angle skip keeps adjacent communities visually distinct.
  const hue = (community * 137.508) % 360;
  const color = `hsl(${hue} 65% 58%)`;
  state.communityColors.set(community, color);
  return color;
}

function applyFilters() {
  if (!state.graph) return;
  const q = state.search.trim().toLowerCase();
  const typeF = state.typeFilter;
  const tierF = state.tierFilter;

  const nodes = state.graph.nodes.filter((n) => {
    if (typeF && n.page_type !== typeF) return false;
    if (tierF && n.tier !== tierF) return false;
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
  positionNodes(state.filtered.nodes, state.filtered.edges);
  fitViewToNodes(state.filtered.nodes);
}

// ---------- Simple force-directed layout (Fruchterman-Reingold-ish) ---------

function positionNodes(nodes, edges) {
  const W = 2000, H = 2000;
  const k = Math.sqrt((W * H) / Math.max(nodes.length, 1)) * 0.8;

  const byId = new Map(nodes.map((n) => [n.id, n]));
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
  const worldPoint = screenToWorld(anchorX, anchorY);
  const clampedScale = clampScale(nextScale);
  view.scale = clampedScale;
  view.tx = anchorX - canvas.clientWidth / 2 - worldPoint.x * clampedScale;
  view.ty = anchorY - canvas.clientHeight / 2 - worldPoint.y * clampedScale;
  updateZoomLevel();
  draw();
}

function fitViewToNodes(nodes = state.filtered.nodes) {
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
  const targetX = canvas.clientWidth / 2;
  const targetY = isCoarsePointer ? canvas.clientHeight * 0.3 : canvas.clientHeight / 2;
  view.tx = targetX - canvas.clientWidth / 2 - node.x * view.scale;
  view.ty = targetY - canvas.clientHeight / 2 - node.y * view.scale;
}

function draw() {
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
  ctx.lineWidth = 0.8 / view.scale;
  for (const e of edges) {
    if (!visibleIds.has(e.source) && !visibleIds.has(e.target)) continue;
    const a = nodeById.get(e.source), b = nodeById.get(e.target);
    if (!a || !b) continue;
    ctx.strokeStyle = state.surprises && e.cross_community
      ? "rgba(248,113,113,0.85)"
      : "rgba(120,130,150,0.25)";
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }

  // Nodes
  for (const n of visibleNodes) {
    const r = nodeRadius(n);
    ctx.fillStyle = colorForCommunity(n.community);
    if (state.highlightedId === n.id) {
      ctx.fillStyle = "rgba(94,234,212,0.18)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 9 / view.scale, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = colorForCommunity(n.community);
    }
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fill();
    if (state.highlightedId === n.id) {
      ctx.strokeStyle = "#5eead4";
      ctx.lineWidth = 2 / view.scale;
      ctx.stroke();
    }
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
    populateTypes();
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
  document.getElementById("rebuild-btn").addEventListener("click", () => loadGraph());
  document.getElementById("zoom-in").addEventListener("click", () => setScale(view.scale * ZOOM_STEP));
  document.getElementById("zoom-out").addEventListener("click", () => setScale(view.scale / ZOOM_STEP));
  document.getElementById("zoom-fit").addEventListener("click", () => fitViewToNodes());
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
