// Cosmograph (cosmos.gl) renderer for wiki-graph-ui.
//
// Wraps @cosmos.gl/graph (WebGL force-graph engine) so app.js can swap from
// the R1-R19 Canvas+Fruchterman-Reingold renderer to GPU layout/rendering
// without rewriting state, filters, BFS path mode, NL ask, checkpoint health,
// or the side panel.
//
// Loaded via esm.sh CDN — no build step. If the CDN is unreachable the caller
// should fall back to the canvas renderer.

import { Graph } from "https://esm.sh/@cosmos.gl/graph@2.6.4?bundle";

// Parse hsl() / hex / rgba() into a normalised [r,g,b,a] float quad in 0..1.
function parseColor(c) {
  if (!c) return [0.6, 0.6, 0.6, 1];
  const hsl = c.match(/^hsl\(\s*([\d.]+)\s+([\d.]+)%\s+([\d.]+)%\s*\)$/);
  if (hsl) return hslToRgb(+hsl[1], +hsl[2] / 100, +hsl[3] / 100, 1);
  const hsla = c.match(/^hsla\(\s*([\d.]+),\s*([\d.]+)%,\s*([\d.]+)%,\s*([\d.]+)\s*\)$/);
  if (hsla) return hslToRgb(+hsla[1], +hsla[2] / 100, +hsla[3] / 100, +hsla[4]);
  const hex6 = c.match(/^#([0-9a-f]{6})$/i);
  if (hex6) {
    const n = parseInt(hex6[1], 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255, 1];
  }
  const rgba = c.match(/^rgba?\(([^)]+)\)$/);
  if (rgba) {
    const parts = rgba[1].split(",").map((s) => parseFloat(s.trim()));
    return [parts[0] / 255, parts[1] / 255, parts[2] / 255, parts.length > 3 ? parts[3] : 1];
  }
  return [0.6, 0.6, 0.6, 1];
}

function hslToRgb(h, s, l, a) {
  h = ((h % 360) + 360) % 360 / 360;
  let r, g, b;
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }
  return [r, g, b, a];
}

export function createCosmosRenderer({ container, onPointClick, onBackgroundClick }) {
  // Node id ↔ index translation: cosmos.gl works on dense Float32Arrays
  // indexed by point/link position, so we maintain a parallel id↔idx map.
  let idToIndex = new Map();
  let indexToNode = [];
  let currentNodes = [];
  let currentEdges = [];

  const config = {
    backgroundColor: "#0b0e14",
    spaceSize: 4096,
    simulationFriction: 0.85,
    simulationGravity: 0.18,
    simulationRepulsion: 1.2,
    simulationLinkSpring: 0.7,
    simulationLinkDistance: 12,
    simulationDecay: 1500,
    pointSizeScale: 1.0,
    linkColor: "rgba(124,140,168,0.20)",
    linkWidth: 1.0,
    linkArrows: false,
    curvedLinks: false,
    fitViewOnInit: true,
    fitViewDelay: 800,
    fitViewPadding: 0.2,
    enableDrag: false,
    enableZoom: true,
    showFPSMonitor: false,
    pointGreyoutOpacity: 0.10,
    linkGreyoutOpacity: 0.06,
    hoveredPointRingColor: "#5eead4",
    focusedPointRingColor: "#5eead4",
    onClick: (pointIndex) => {
      if (pointIndex == null || pointIndex < 0) {
        onBackgroundClick && onBackgroundClick();
        return;
      }
      const node = indexToNode[pointIndex];
      if (node) onPointClick && onPointClick(node);
    },
  };

  const graph = new Graph(container, config);

  function syncData(nodes, edges) {
    currentNodes = nodes;
    currentEdges = edges;
    idToIndex = new Map();
    indexToNode = new Array(nodes.length);

    // Spread initial positions on a circle so the simulation starts from a
    // non-degenerate state. Cosmograph's force solver settles fast (~1s).
    const positions = new Float32Array(nodes.length * 2);
    const R = 1500;
    nodes.forEach((n, i) => {
      idToIndex.set(n.id, i);
      indexToNode[i] = n;
      const a = (i / nodes.length) * Math.PI * 2;
      positions[i * 2] = Math.cos(a) * R + (Math.random() - 0.5) * 30;
      positions[i * 2 + 1] = Math.sin(a) * R + (Math.random() - 0.5) * 30;
    });
    graph.setPointPositions(positions);

    // Build link index pairs.
    const linkPairs = [];
    for (const e of edges) {
      const s = idToIndex.get(e.source);
      const t = idToIndex.get(e.target);
      if (s == null || t == null) continue;
      linkPairs.push(s, t);
    }
    graph.setLinks(new Float32Array(linkPairs));

    // Cluster force: nodes in the same community pull toward a shared centroid
    // — this is the spec'd behaviour ("organized clusters") that pure FR misses.
    const clusters = new Float32Array(nodes.length);
    nodes.forEach((n, i) => {
      clusters[i] = Number.isFinite(n.community) ? n.community : -1;
    });
    if (typeof graph.setPointClusters === "function") {
      graph.setPointClusters(clusters);
    }
  }

  function syncStyle({ colorOf, sizeOf, dimOf }) {
    if (!currentNodes.length) return;
    const colors = new Float32Array(currentNodes.length * 4);
    const sizes = new Float32Array(currentNodes.length);
    for (let i = 0; i < currentNodes.length; i++) {
      const node = currentNodes[i];
      const rgb = parseColor(colorOf(node));
      const dim = dimOf ? dimOf(node) : false;
      const alpha = dim ? 0.18 : 1.0;
      colors[i * 4] = rgb[0];
      colors[i * 4 + 1] = rgb[1];
      colors[i * 4 + 2] = rgb[2];
      colors[i * 4 + 3] = alpha;
      sizes[i] = sizeOf(node);
    }
    graph.setPointColors(colors);
    graph.setPointSizes(sizes);
  }

  function focusNode(id) {
    const idx = idToIndex.get(id);
    if (idx == null) return;
    if (typeof graph.zoomToPointByIndex === "function") {
      graph.zoomToPointByIndex(idx, 700, 4, true);
    } else if (typeof graph.focusPointByIndex === "function") {
      graph.focusPointByIndex(idx);
    }
  }

  function setSelectedNodes(ids) {
    if (!ids || !ids.size) {
      if (typeof graph.unselectPoints === "function") graph.unselectPoints();
      return;
    }
    const indices = [];
    for (const id of ids) {
      const i = idToIndex.get(id);
      if (i != null) indices.push(i);
    }
    if (typeof graph.selectPointsByIndices === "function") {
      graph.selectPointsByIndices(indices);
    }
  }

  function fit() {
    if (typeof graph.fitView === "function") graph.fitView(800);
  }

  function render() {
    graph.render();
  }

  return {
    syncData,
    syncStyle,
    focusNode,
    setSelectedNodes,
    fit,
    render,
    raw: graph,
  };
}
