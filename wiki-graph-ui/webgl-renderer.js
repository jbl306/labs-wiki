// Custom WebGL2 renderer for labs-wiki/wiki-graph-ui.
//
// Why custom: cosmos.gl ran its own force sim on top of the server's
// precomputed Fruchterman-Reingold layout (x/y already shipped on every
// node) which caused positions to drift off-screen, and its flat point
// dots looked drab. This renderer:
//
//   1. Uses the server's x/y directly — zero JS simulation, zero drift.
//   2. Draws each node with a premultiplied-alpha glow shader (bright
//      core + soft halo) that overlaps additively to read as bloom.
//   3. Tracers thin links underneath in a single line draw call.
//   4. Owns its own pan/zoom (wheel + drag + pinch) and click hit-test.
//
// Public API:
//   const r = createWebglRenderer({ container, onPointClick, onBackgroundClick });
//   r.syncData(nodes, edges);
//   r.syncStyle({ colorOf, sizeOf, dimOf });
//   r.focusNode(id);
//   r.setSelectedNodes(idSet);
//   r.fit();
//   r.render();          // request a redraw
//   r.destroy();

// ---------- Color parsing ------------------------------------------------

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
  const hex3 = c.match(/^#([0-9a-f]{3})$/i);
  if (hex3) {
    const r = parseInt(hex3[1][0] + hex3[1][0], 16);
    const g = parseInt(hex3[1][1] + hex3[1][1], 16);
    const b = parseInt(hex3[1][2] + hex3[1][2], 16);
    return [r / 255, g / 255, b / 255, 1];
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

// ---------- Shaders ------------------------------------------------------

// Points: gl_PointSize discs textured via gl_PointCoord with a
// power-curve falloff that yields a tight bright core + wide soft halo.
// Output is premultiplied alpha so additive overlap reads as bloom.
const POINT_VS = `#version 300 es
precision highp float;
in vec2 a_pos;
in vec4 a_color;
in float a_size;
in float a_alpha;
in float a_selected;
uniform mat3 u_view;
uniform float u_dpr;
out vec4 v_color;
out float v_alpha;
out float v_selected;
void main() {
  vec3 p = u_view * vec3(a_pos, 1.0);
  gl_Position = vec4(p.xy, 0.0, 1.0);
  // Inflate selected nodes slightly so their ring reads at any zoom.
  float s = a_size * (a_selected > 0.5 ? 1.35 : 1.0);
  gl_PointSize = s * u_dpr;
  v_color = a_color;
  v_alpha = a_alpha;
  v_selected = a_selected;
}`;

const POINT_FS = `#version 300 es
precision highp float;
in vec4 v_color;
in float v_alpha;
in float v_selected;
out vec4 fragColor;
void main() {
  // gl_PointCoord is in [0,1]; remap to [-1,1] disc.
  vec2 uv = gl_PointCoord * 2.0 - 1.0;
  float d = length(uv);
  if (d > 1.0) discard;

  // Tight core (pow=4) + wide halo (pow=1.5) — overlapping halos brighten.
  float fall = 1.0 - smoothstep(0.0, 1.0, d);
  float core = pow(fall, 4.0);
  float halo = pow(fall, 1.5) * 0.55;

  // Selection ring: bright thin annulus near r ~ 0.85.
  float ring = v_selected * smoothstep(0.78, 0.84, d) * (1.0 - smoothstep(0.92, 0.98, d));

  vec3 col = v_color.rgb * (core * 1.4 + halo * 0.8) + vec3(0.95, 0.95, 1.0) * ring * 1.2;
  float a = clamp((core + halo * 0.65 + ring * 0.9) * v_alpha, 0.0, 1.0);

  // Premultiplied alpha so overlapping halos add into bloom under
  // gl.blendFunc(ONE, ONE_MINUS_SRC_ALPHA).
  fragColor = vec4(col * a, a);
}`;

const LINE_VS = `#version 300 es
precision highp float;
in vec2 a_pos;
in vec4 a_color;
uniform mat3 u_view;
out vec4 v_color;
void main() {
  vec3 p = u_view * vec3(a_pos, 1.0);
  gl_Position = vec4(p.xy, 0.0, 1.0);
  v_color = a_color;
}`;

const LINE_FS = `#version 300 es
precision highp float;
in vec4 v_color;
out vec4 fragColor;
void main() {
  fragColor = vec4(v_color.rgb * v_color.a, v_color.a);
}`;

// ---------- GL helpers ---------------------------------------------------

function compile(gl, type, src) {
  const sh = gl.createShader(type);
  gl.shaderSource(sh, src);
  gl.compileShader(sh);
  if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(sh);
    gl.deleteShader(sh);
    throw new Error("shader compile failed: " + log);
  }
  return sh;
}

function link(gl, vs, fs) {
  const p = gl.createProgram();
  gl.attachShader(p, compile(gl, gl.VERTEX_SHADER, vs));
  gl.attachShader(p, compile(gl, gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
    const log = gl.getProgramInfoLog(p);
    gl.deleteProgram(p);
    throw new Error("program link failed: " + log);
  }
  return p;
}

// ---------- Renderer -----------------------------------------------------

export function createWebglRenderer({ container, onPointClick, onBackgroundClick }) {
  // Build canvas inside container.
  const canvas = document.createElement("canvas");
  canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:none;cursor:grab;";
  container.style.position = container.style.position || "relative";
  container.appendChild(canvas);

  const gl = canvas.getContext("webgl2", {
    antialias: true,
    premultipliedAlpha: true,
    alpha: false,
    powerPreference: "high-performance",
  });
  if (!gl) throw new Error("webgl2 unavailable");

  const pointProg = link(gl, POINT_VS, POINT_FS);
  const lineProg = link(gl, LINE_VS, LINE_FS);

  const A_pt_pos = gl.getAttribLocation(pointProg, "a_pos");
  const A_pt_color = gl.getAttribLocation(pointProg, "a_color");
  const A_pt_size = gl.getAttribLocation(pointProg, "a_size");
  const A_pt_alpha = gl.getAttribLocation(pointProg, "a_alpha");
  const A_pt_sel = gl.getAttribLocation(pointProg, "a_selected");
  const U_pt_view = gl.getUniformLocation(pointProg, "u_view");
  const U_pt_dpr = gl.getUniformLocation(pointProg, "u_dpr");

  const A_ln_pos = gl.getAttribLocation(lineProg, "a_pos");
  const A_ln_color = gl.getAttribLocation(lineProg, "a_color");
  const U_ln_view = gl.getUniformLocation(lineProg, "u_view");

  const ptVAO = gl.createVertexArray();
  const lnVAO = gl.createVertexArray();
  const ptPosBuf = gl.createBuffer();
  const ptColBuf = gl.createBuffer();
  const ptSizeBuf = gl.createBuffer();
  const ptAlphaBuf = gl.createBuffer();
  const ptSelBuf = gl.createBuffer();
  const lnPosBuf = gl.createBuffer();
  const lnColBuf = gl.createBuffer();

  // Camera / state.
  let dpr = Math.max(1, window.devicePixelRatio || 1);
  let viewW = 0, viewH = 0;
  // Camera in world units. World x/y from server are in [-1000, 1000].
  let cam = { x: 0, y: 0, scale: 0.4 };

  let nodes = [];
  let edges = [];
  let idToIdx = new Map();
  let selectedSet = new Set();
  let needsRedraw = true;
  let rafPending = false;

  // Spatial bins for click hit-test (~50 world units per cell).
  const BIN = 64;
  let bins = new Map();
  function rebuildBins() {
    bins = new Map();
    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      const cx = Math.floor(n.x / BIN), cy = Math.floor(n.y / BIN);
      const k = cx + "," + cy;
      let arr = bins.get(k);
      if (!arr) { arr = []; bins.set(k, arr); }
      arr.push(i);
    }
  }

  // ---------- Resize / matrix --------------------------------------------

  function resize() {
    dpr = Math.max(1, window.devicePixelRatio || 1);
    const w = container.clientWidth | 0;
    const h = container.clientHeight | 0;
    if (w === viewW && h === viewH && canvas.width === w * dpr) return;
    viewW = w; viewH = h;
    canvas.width = Math.max(1, w * dpr);
    canvas.height = Math.max(1, h * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
    needsRedraw = true;
    schedule();
  }

  // 3x3 column-major view matrix mapping world → clip space.
  // clip = scale_world * (world - cam) translated into NDC by 2/viewport.
  function viewMatrix() {
    const sx = (2 * cam.scale) / Math.max(viewW, 1);
    const sy = -(2 * cam.scale) / Math.max(viewH, 1); // flip y to screen
    const tx = -cam.x * sx;
    const ty = -cam.y * sy;
    return new Float32Array([
      sx, 0, 0,
      0, sy, 0,
      tx, ty, 1,
    ]);
  }

  function worldToScreen(wx, wy) {
    const sx = (wx - cam.x) * cam.scale + viewW / 2;
    const sy = (wy - cam.y) * cam.scale + viewH / 2;
    return [sx, sy];
  }

  function screenToWorld(sx, sy) {
    const wx = (sx - viewW / 2) / cam.scale + cam.x;
    const wy = (sy - viewH / 2) / cam.scale + cam.y;
    return [wx, wy];
  }

  // ---------- Public API: data -------------------------------------------

  function syncData(newNodes, newEdges) {
    nodes = newNodes || [];
    edges = newEdges || [];
    idToIdx = new Map();
    nodes.forEach((n, i) => idToIdx.set(n.id, i));

    // Position buffer (Float32Array of x,y per node).
    const positions = new Float32Array(nodes.length * 2);
    for (let i = 0; i < nodes.length; i++) {
      // Server sometimes ships missing x/y for new nodes — fall back to (0,0).
      positions[i * 2] = Number.isFinite(nodes[i].x) ? nodes[i].x : 0;
      positions[i * 2 + 1] = Number.isFinite(nodes[i].y) ? nodes[i].y : 0;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, ptPosBuf);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

    // Edge geometry: pairs of endpoints expanded into a flat Float32Array.
    const linePos = new Float32Array(edges.length * 4);
    const lineCol = new Float32Array(edges.length * 8);
    let lp = 0, lc = 0;
    for (const e of edges) {
      const si = idToIdx.get(e.source);
      const ti = idToIdx.get(e.target);
      if (si == null || ti == null) continue;
      linePos[lp++] = positions[si * 2];
      linePos[lp++] = positions[si * 2 + 1];
      linePos[lp++] = positions[ti * 2];
      linePos[lp++] = positions[ti * 2 + 1];
      // Default link colour — overwritten by syncStyle if available.
      const baseA = e.cross_community ? 0.30 : 0.18;
      const r = 0.59, g = 0.67, b = 0.85;
      for (let k = 0; k < 2; k++) {
        lineCol[lc++] = r;
        lineCol[lc++] = g;
        lineCol[lc++] = b;
        lineCol[lc++] = baseA;
      }
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, lnPosBuf);
    gl.bufferData(gl.ARRAY_BUFFER, linePos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, lnColBuf);
    gl.bufferData(gl.ARRAY_BUFFER, lineCol, gl.STATIC_DRAW);

    // Pre-allocate styling buffers; syncStyle fills them.
    gl.bindBuffer(gl.ARRAY_BUFFER, ptColBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodes.length * 4), gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSizeBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodes.length), gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptAlphaBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodes.length), gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSelBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodes.length), gl.DYNAMIC_DRAW);

    // Wire VAOs once now that buffer sizes are known.
    bindVAOs();
    rebuildBins();
    fit();
    needsRedraw = true;
    schedule();
  }

  function bindVAOs() {
    gl.bindVertexArray(ptVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptPosBuf);
    gl.enableVertexAttribArray(A_pt_pos);
    gl.vertexAttribPointer(A_pt_pos, 2, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptColBuf);
    gl.enableVertexAttribArray(A_pt_color);
    gl.vertexAttribPointer(A_pt_color, 4, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSizeBuf);
    gl.enableVertexAttribArray(A_pt_size);
    gl.vertexAttribPointer(A_pt_size, 1, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptAlphaBuf);
    gl.enableVertexAttribArray(A_pt_alpha);
    gl.vertexAttribPointer(A_pt_alpha, 1, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSelBuf);
    gl.enableVertexAttribArray(A_pt_sel);
    gl.vertexAttribPointer(A_pt_sel, 1, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(lnVAO);
    gl.bindBuffer(gl.ARRAY_BUFFER, lnPosBuf);
    gl.enableVertexAttribArray(A_ln_pos);
    gl.vertexAttribPointer(A_ln_pos, 2, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, lnColBuf);
    gl.enableVertexAttribArray(A_ln_color);
    gl.vertexAttribPointer(A_ln_color, 4, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
  }

  // styleCache lets us re-upload only what changed.
  let lastSizes = null;
  function syncStyle({ colorOf, sizeOf, dimOf }) {
    if (!nodes.length) return;
    const colors = new Float32Array(nodes.length * 4);
    const sizes = new Float32Array(nodes.length);
    const alphas = new Float32Array(nodes.length);
    const sels = new Float32Array(nodes.length);
    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      const rgba = parseColor(colorOf(n));
      const dim = dimOf ? dimOf(n) : false;
      colors[i * 4] = rgba[0];
      colors[i * 4 + 1] = rgba[1];
      colors[i * 4 + 2] = rgba[2];
      colors[i * 4 + 3] = rgba[3];
      sizes[i] = Math.max(2, sizeOf(n));
      alphas[i] = dim ? 0.18 : 1.0;
      sels[i] = selectedSet.has(n.id) ? 1.0 : 0.0;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, ptColBuf);
    gl.bufferData(gl.ARRAY_BUFFER, colors, gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSizeBuf);
    gl.bufferData(gl.ARRAY_BUFFER, sizes, gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptAlphaBuf);
    gl.bufferData(gl.ARRAY_BUFFER, alphas, gl.DYNAMIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSelBuf);
    gl.bufferData(gl.ARRAY_BUFFER, sels, gl.DYNAMIC_DRAW);
    lastSizes = sizes;
    needsRedraw = true;
    schedule();
  }

  function setSelectedNodes(idSet) {
    selectedSet = idSet ? new Set(idSet) : new Set();
    if (!nodes.length) return;
    const sels = new Float32Array(nodes.length);
    for (let i = 0; i < nodes.length; i++) {
      sels[i] = selectedSet.has(nodes[i].id) ? 1.0 : 0.0;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, ptSelBuf);
    gl.bufferData(gl.ARRAY_BUFFER, sels, gl.DYNAMIC_DRAW);
    needsRedraw = true;
    schedule();
  }

  // ---------- Camera -----------------------------------------------------

  function fit() {
    if (!nodes.length || !viewW || !viewH) return;
    // Percentile-trimmed bbox so a handful of disconnected outliers don't
    // squash the dense core to a postage stamp. Server x/y range can be
    // [-1000, 1000] but 90% of nodes typically pack much tighter.
    const xs = new Float64Array(nodes.length);
    const ys = new Float64Array(nodes.length);
    let valid = 0;
    for (const n of nodes) {
      if (Number.isFinite(n.x) && Number.isFinite(n.y)) {
        xs[valid] = n.x;
        ys[valid] = n.y;
        valid++;
      }
    }
    if (!valid) return;
    const xsArr = xs.subarray(0, valid);
    const ysArr = ys.subarray(0, valid);
    const sortedX = Array.from(xsArr).sort((a, b) => a - b);
    const sortedY = Array.from(ysArr).sort((a, b) => a - b);
    const lo = Math.floor(valid * 0.03);
    const hi = Math.min(valid - 1, Math.ceil(valid * 0.97));
    const minX = sortedX[lo], maxX = sortedX[hi];
    const minY = sortedY[lo], maxY = sortedY[hi];
    const w = Math.max(maxX - minX, 1);
    const h = Math.max(maxY - minY, 1);
    const padding = 0.10;
    const sx = viewW * (1 - padding * 2) / w;
    const sy = viewH * (1 - padding * 2) / h;
    cam.scale = Math.min(sx, sy);
    cam.x = (minX + maxX) / 2;
    cam.y = (minY + maxY) / 2;
    needsRedraw = true;
    schedule();
  }

  function focusNode(id) {
    const i = idToIdx.get(id);
    if (i == null) return;
    cam.x = nodes[i].x;
    cam.y = nodes[i].y;
    cam.scale = Math.max(cam.scale, 1.6);
    needsRedraw = true;
    schedule();
  }

  // ---------- Hit-test (click) -------------------------------------------

  function pickAt(screenX, screenY) {
    const [wx, wy] = screenToWorld(screenX, screenY);
    // Search bins covering a small radius in world units.
    const r = 24 / cam.scale; // ~24px in world coords
    const cx = Math.floor(wx / BIN), cy = Math.floor(wy / BIN);
    const span = Math.max(1, Math.ceil(r / BIN));
    let best = -1, bestDist = r * r;
    for (let dx = -span; dx <= span; dx++) {
      for (let dy = -span; dy <= span; dy++) {
        const arr = bins.get((cx + dx) + "," + (cy + dy));
        if (!arr) continue;
        for (const i of arr) {
          const n = nodes[i];
          const ddx = n.x - wx, ddy = n.y - wy;
          const d2 = ddx * ddx + ddy * ddy;
          if (d2 < bestDist) { bestDist = d2; best = i; }
        }
      }
    }
    return best >= 0 ? nodes[best] : null;
  }

  // ---------- Pointer / wheel handlers -----------------------------------

  const pointers = new Map();
  let dragging = false;
  let pinchStartDist = 0;
  let pinchStartScale = 0;
  let pressX = 0, pressY = 0, moved = false;

  canvas.addEventListener("pointerdown", (e) => {
    canvas.setPointerCapture(e.pointerId);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    pressX = e.clientX; pressY = e.clientY; moved = false;
    if (pointers.size === 2) {
      const pts = Array.from(pointers.values());
      pinchStartDist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      pinchStartScale = cam.scale;
    } else if (pointers.size === 1) {
      dragging = true;
      canvas.style.cursor = "grabbing";
    }
  });

  canvas.addEventListener("pointermove", (e) => {
    const prev = pointers.get(e.pointerId);
    if (!prev) return;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

    if (pointers.size === 2 && pinchStartDist > 0) {
      const pts = Array.from(pointers.values());
      const d = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      const factor = d / pinchStartDist;
      const rect = canvas.getBoundingClientRect();
      const midX = (pts[0].x + pts[1].x) / 2 - rect.left;
      const midY = (pts[0].y + pts[1].y) / 2 - rect.top;
      zoomAt(pinchStartScale * factor, midX, midY);
      moved = true;
      return;
    }

    if (dragging) {
      const dx = e.clientX - prev.x;
      const dy = e.clientY - prev.y;
      if (Math.hypot(e.clientX - pressX, e.clientY - pressY) > 4) moved = true;
      cam.x -= dx / cam.scale;
      cam.y -= dy / cam.scale;
      needsRedraw = true;
      schedule();
    }
  });

  function endPointer(e) {
    if (!pointers.has(e.pointerId)) return;
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinchStartDist = 0;
    if (pointers.size === 0) {
      dragging = false;
      canvas.style.cursor = "grab";
      // Treat as click if not moved.
      if (!moved) {
        const rect = canvas.getBoundingClientRect();
        const px = e.clientX - rect.left;
        const py = e.clientY - rect.top;
        const node = pickAt(px, py);
        if (node) onPointClick && onPointClick(node);
        else onBackgroundClick && onBackgroundClick();
      }
    }
  }
  canvas.addEventListener("pointerup", endPointer);
  canvas.addEventListener("pointercancel", endPointer);

  function zoomAt(nextScale, anchorX, anchorY) {
    const clamped = Math.max(0.05, Math.min(20, nextScale));
    const [wx, wy] = screenToWorld(anchorX, anchorY);
    cam.scale = clamped;
    // Re-anchor so the anchor point stays under the cursor.
    const [wx2, wy2] = screenToWorld(anchorX, anchorY);
    cam.x += wx - wx2;
    cam.y += wy - wy2;
    needsRedraw = true;
    schedule();
  }

  canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const factor = Math.exp(-e.deltaY * 0.0015);
    const rect = canvas.getBoundingClientRect();
    zoomAt(cam.scale * factor, e.clientX - rect.left, e.clientY - rect.top);
  }, { passive: false });

  const ro = new ResizeObserver(() => resize());
  ro.observe(container);
  window.addEventListener("resize", resize);

  // ---------- Draw loop --------------------------------------------------

  function schedule() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(draw);
  }

  function draw() {
    rafPending = false;
    if (!needsRedraw) return;
    needsRedraw = false;
    resize();
    if (!viewW || !viewH) return;

    gl.clearColor(0.043, 0.055, 0.078, 1.0); // #0b0e14
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    const M = viewMatrix();

    // Edges first (under nodes).
    if (edges.length) {
      gl.useProgram(lineProg);
      gl.uniformMatrix3fv(U_ln_view, false, M);
      gl.bindVertexArray(lnVAO);
      gl.drawArrays(gl.LINES, 0, edges.length * 2);
    }

    // Points.
    if (nodes.length) {
      gl.useProgram(pointProg);
      gl.uniformMatrix3fv(U_pt_view, false, M);
      gl.uniform1f(U_pt_dpr, dpr);
      gl.bindVertexArray(ptVAO);
      gl.drawArrays(gl.POINTS, 0, nodes.length);
    }

    gl.bindVertexArray(null);
  }

  function render() {
    needsRedraw = true;
    schedule();
  }

  function destroy() {
    ro.disconnect();
    canvas.remove();
  }

  // Trigger initial sizing.
  resize();

  return {
    syncData,
    syncStyle,
    setSelectedNodes,
    focusNode,
    fit,
    render,
    destroy,
  };
}
