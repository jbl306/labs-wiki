// Minimal labs-wiki graph viewer.
// Deliberately dependency-free: uses the browser's Canvas API and a small
// force-directed layout so the image ships as pure static HTML/CSS/JS behind
// nginx, with zero build step. If node counts grow past a few thousand, swap
// the renderer for @cosmograph/cosmograph per Phase G3.

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

  state.filtered = { nodes, edges };
  positionNodes(state.filtered.nodes, state.filtered.edges);
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
  draw();
}

// ---------- Canvas rendering ----------------------------------------------

const canvas = document.getElementById("graph");
const ctx = canvas.getContext("2d");
const view = { scale: 0.35, tx: 0, ty: 0 };

function resize() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = canvas.clientWidth * dpr;
  canvas.height = canvas.clientHeight * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  draw();
}
window.addEventListener("resize", resize);

function world(x, y) {
  return {
    x: (x - view.tx) / view.scale + canvas.clientWidth / 2,
    y: (y - view.ty) / view.scale + canvas.clientHeight / 2,
  };
}

function draw() {
  ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
  const { nodes, edges } = state.filtered;
  if (!nodes.length) return;

  const cx = canvas.clientWidth / 2;
  const cy = canvas.clientHeight / 2;

  ctx.save();
  ctx.translate(cx + view.tx, cy + view.ty);
  ctx.scale(view.scale, view.scale);

  // Edges
  ctx.lineWidth = 0.8 / view.scale;
  for (const e of edges) {
    const a = findNode(e.source), b = findNode(e.target);
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
  for (const n of nodes) {
    const r = Math.max(3, 3 + Math.log2(1 + n.degree) * 2);
    ctx.fillStyle = colorForCommunity(n.community);
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fill();
    if (state.highlightedId === n.id) {
      ctx.strokeStyle = "#5eead4";
      ctx.lineWidth = 2 / view.scale;
      ctx.stroke();
    }
  }

  // Labels for large nodes
  ctx.fillStyle = "#e5e7eb";
  ctx.font = `${Math.max(10, 10 / view.scale)}px sans-serif`;
  ctx.textAlign = "center";
  for (const n of nodes) {
    if (n.degree < 5 && state.highlightedId !== n.id) continue;
    ctx.fillText(n.title.slice(0, 32), n.x, n.y - 8);
  }

  ctx.restore();
}

function findNode(id) {
  return state.filtered.nodes.find((n) => n.id === id);
}

// ---------- Interactions ---------------------------------------------------

let dragging = false, lastX = 0, lastY = 0;
canvas.addEventListener("mousedown", (e) => { dragging = true; lastX = e.clientX; lastY = e.clientY; });
window.addEventListener("mouseup", () => { dragging = false; });
window.addEventListener("mousemove", (e) => {
  if (!dragging) return;
  view.tx += (e.clientX - lastX);
  view.ty += (e.clientY - lastY);
  lastX = e.clientX; lastY = e.clientY;
  draw();
});
canvas.addEventListener("wheel", (e) => {
  e.preventDefault();
  const factor = Math.exp(-e.deltaY * 0.001);
  view.scale = Math.max(0.05, Math.min(4, view.scale * factor));
  draw();
}, { passive: false });

canvas.addEventListener("click", async (e) => {
  const rect = canvas.getBoundingClientRect();
  const px = e.clientX - rect.left;
  const py = e.clientY - rect.top;
  const cx = canvas.clientWidth / 2;
  const cy = canvas.clientHeight / 2;
  const wx = (px - cx - view.tx) / view.scale;
  const wy = (py - cy - view.ty) / view.scale;

  let hit = null;
  let best = Infinity;
  for (const n of state.filtered.nodes) {
    const dx = n.x - wx, dy = n.y - wy;
    const d2 = dx * dx + dy * dy;
    const r = Math.max(3, 3 + Math.log2(1 + n.degree) * 2);
    if (d2 < r * r * 4 && d2 < best) { best = d2; hit = n; }
  }
  if (hit) {
    state.highlightedId = hit.id;
    showNodePanel(hit);
    draw();
  }
});

async function showNodePanel(node) {
  document.getElementById("node-panel").classList.remove("hidden");
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
        state.highlightedId = n.id;
        const local = state.filtered.nodes.find((x) => x.id === n.id);
        if (local) showNodePanel(local);
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
    applyFilters();
    resize();
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
