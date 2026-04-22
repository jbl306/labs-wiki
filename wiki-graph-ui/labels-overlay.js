// Adaptive HTML label overlay for the WebGL graph renderer.
//
// Why HTML and not in-shader text: text in WebGL is hard to do well (atlases,
// kerning, AA). The browser's native text rasteriser is faster, sharper, and
// re-uses our existing CSS theme. A few hundred absolutely-positioned divs
// over a canvas is essentially free.
//
// Strategy:
//   1. Pick candidates by importance (degree, plus pinned: highlighted,
//      hovered, selected).
//   2. Show progressively more labels as zoom increases.
//   3. Greedy collision avoidance in screen space — sort by importance,
//      claim a bounding box, skip later labels that intersect a claimed box.
//   4. Re-layout on every transform notification (rAF-throttled internally
//      by the renderer's draw loop).

export function createLabelOverlay({ container, renderer }) {
  const layer = document.createElement("div");
  layer.id = "webgl-labels";
  layer.style.cssText = [
    "position:absolute",
    "inset:0",
    "pointer-events:none",
    "overflow:hidden",
    "contain:strict",
    "z-index:5",
  ].join(";");
  container.appendChild(layer);

  // node id -> { el, w, h }
  const cache = new Map();
  let nodes = [];
  let pinned = new Set(); // ids that must always render (selected/highlighted)
  let onLabelClick = null;

  // ---------- Perf: throttle + interaction-aware --------------------------
  // Two failure modes we must avoid on mobile:
  //   1. Re-laying out 700 candidates + DOM transform writes on every
  //      animation frame during a pinch -> 60 Hz of jank.
  //   2. Labels visually lagging behind the GPU during gestures (since
  //      we're DOM-positioned, not in the same draw call as the canvas).
  // Fix: hide the label layer entirely while the user is actively
  // interacting (pinch/drag/wheel), and throttle steady-state layout to
  // ~25 Hz. This restores buttery pinch performance and labels snap back
  // crisply once the gesture settles.
  let activePointers = 0;
  let interacting = false;
  let settleTimer = null;
  let lastLayoutTs = 0;
  let pendingCam = null;
  let pendingTimer = null;
  const LAYOUT_INTERVAL_MS = 40; // ~25 Hz cap
  const SETTLE_MS = 140;         // grace period after gesture ends

  function setInteracting(on) {
    if (interacting === on) return;
    interacting = on;
    layer.classList.toggle("interacting", on);
    if (!on && pendingCam) {
      // Layout once with the freshest camera now that the gesture stopped.
      const cam = pendingCam;
      pendingCam = null;
      runLayout(cam);
    }
  }

  function bumpInteraction() {
    setInteracting(true);
    if (settleTimer) clearTimeout(settleTimer);
    settleTimer = setTimeout(() => setInteracting(false), SETTLE_MS);
  }

  // Track gestures on the container so any pointer/wheel inside the graph
  // host triggers the "interacting" state.
  container.addEventListener("pointerdown", (e) => {
    activePointers += 1;
    bumpInteraction();
  }, { passive: true });
  const releasePointer = () => {
    activePointers = Math.max(0, activePointers - 1);
    if (activePointers === 0) bumpInteraction(); // start the settle timer
  };
  container.addEventListener("pointerup", releasePointer, { passive: true });
  container.addEventListener("pointercancel", releasePointer, { passive: true });
  container.addEventListener("wheel", () => bumpInteraction(), { passive: true });

  function setNodes(newNodes) {
    nodes = newNodes || [];
  }

  function setPinned(idSet) {
    pinned = idSet ? new Set(idSet) : new Set();
  }

  function setOnLabelClick(cb) {
    onLabelClick = cb;
  }

  function makeEl(node) {
    const el = document.createElement("button");
    el.type = "button";
    el.className = "webgl-label";
    el.textContent = node.title || node.id;
    el.dataset.id = node.id;
    el.style.pointerEvents = "auto";
    el.addEventListener("click", (e) => {
      e.stopPropagation();
      if (onLabelClick) onLabelClick(node);
    });
    layer.appendChild(el);
    // Measure once. Subsequent style/zoom changes don't change the box much
    // because we don't scale font with zoom — labels stay readable.
    const r = el.getBoundingClientRect();
    return { el, w: Math.ceil(r.width) || 60, h: Math.ceil(r.height) || 16 };
  }

  function getEl(node) {
    let entry = cache.get(node.id);
    if (!entry) {
      entry = makeEl(node);
      cache.set(node.id, entry);
    }
    return entry;
  }

  // Public layout entry — throttled + interaction-aware. Renderer fires this
  // on every notifyTransform() (roughly every drawn frame).
  function layout(cam) {
    if (!cam || !nodes.length) return;
    // While the user is actively gesturing, drop layout work entirely and
    // keep the label layer hidden via CSS. We just remember the latest
    // camera so we can lay out once on settle.
    if (interacting) {
      pendingCam = cam;
      return;
    }
    const now = performance.now();
    const since = now - lastLayoutTs;
    if (since >= LAYOUT_INTERVAL_MS) {
      runLayout(cam);
      return;
    }
    // Schedule a trailing layout so the final frame after a wheel/pan is
    // always fresh, even if the renderer stops issuing transform events.
    pendingCam = cam;
    if (pendingTimer) return;
    pendingTimer = setTimeout(() => {
      pendingTimer = null;
      const c = pendingCam;
      pendingCam = null;
      if (c) runLayout(c);
    }, LAYOUT_INTERVAL_MS - since);
  }

  function runLayout(cam) {
    lastLayoutTs = performance.now();
    const W = cam.viewW, H = cam.viewH;

    // How many labels to show scales with zoom. At wide-zoom we want only the
    // hubs visible; as the user zooms in we relax the budget.
    // scale ~ 0.4 = wide; scale ~ 4 = tight.
    const zoomFactor = Math.min(4, Math.max(0.3, cam.scale));
    const baseBudget = 28;
    let budget = Math.round(baseBudget * Math.pow(zoomFactor / 0.5, 0.85));
    budget = Math.max(20, Math.min(220, budget));

    // Build candidate list. Importance = degree, with a big boost for pinned.
    const candidates = [];
    for (const n of nodes) {
      const sx = (n.x - cam.x) * cam.scale + W / 2;
      const sy = (n.y - cam.y) * cam.scale + H / 2;
      // Cull off-screen with a small margin.
      if (sx < -120 || sx > W + 120 || sy < -40 || sy > H + 40) continue;
      const isPinned = pinned.has(n.id);
      // Importance: pinned nodes always sort first.
      const imp = (isPinned ? 1e9 : 0) + (n.degree || 0) + (n.tier === "core" ? 5 : 0);
      candidates.push({ node: n, sx, sy, imp, pinned: isPinned });
    }
    candidates.sort((a, b) => b.imp - a.imp);

    // Greedy collision: walk in importance order, claim screen rects.
    const claimed = []; // rects {x,y,w,h}
    const visible = new Set();

    // Spatial buckets for O(N) collision check.
    const BUCKET = 96;
    const buckets = new Map();
    function bucketKey(bx, by) { return bx + "," + by; }
    function intersects(rect) {
      const minBx = Math.floor(rect.x / BUCKET);
      const maxBx = Math.floor((rect.x + rect.w) / BUCKET);
      const minBy = Math.floor(rect.y / BUCKET);
      const maxBy = Math.floor((rect.y + rect.h) / BUCKET);
      for (let bx = minBx; bx <= maxBx; bx++) {
        for (let by = minBy; by <= maxBy; by++) {
          const arr = buckets.get(bucketKey(bx, by));
          if (!arr) continue;
          for (const r of arr) {
            if (rect.x < r.x + r.w && rect.x + rect.w > r.x &&
                rect.y < r.y + r.h && rect.y + rect.h > r.y) return true;
          }
        }
      }
      return false;
    }
    function addToBuckets(rect) {
      const minBx = Math.floor(rect.x / BUCKET);
      const maxBx = Math.floor((rect.x + rect.w) / BUCKET);
      const minBy = Math.floor(rect.y / BUCKET);
      const maxBy = Math.floor((rect.y + rect.h) / BUCKET);
      for (let bx = minBx; bx <= maxBx; bx++) {
        for (let by = minBy; by <= maxBy; by++) {
          const k = bucketKey(bx, by);
          let arr = buckets.get(k);
          if (!arr) { arr = []; buckets.set(k, arr); }
          arr.push(rect);
        }
      }
    }

    for (const c of candidates) {
      if (visible.size >= budget && !c.pinned) break;
      const entry = getEl(c.node);
      // Position label below node by a small offset proportional to the
      // node's rendered radius (approx).
      const deg = Math.max(1, c.node.degree || 1);
      const r = Math.min(28, 4.5 + Math.log2(deg + 1) * 3.2);
      // Center horizontally on node, sit below the glow.
      const labelX = Math.round(c.sx - entry.w / 2);
      const labelY = Math.round(c.sy + r * 0.55 + 4);
      const rect = { x: labelX - 2, y: labelY - 2, w: entry.w + 4, h: entry.h + 4 };
      if (!c.pinned && intersects(rect)) continue;
      addToBuckets(rect);
      claimed.push(rect);
      visible.add(c.node.id);
      entry.x = labelX; entry.y = labelY;
      entry.el.style.transform = `translate3d(${labelX}px, ${labelY}px, 0)`;
      entry.el.classList.toggle("pinned", c.pinned);
      entry.el.classList.remove("hidden");
    }

    // Hide everything we didn't claim this frame.
    for (const [id, entry] of cache) {
      if (!visible.has(id)) entry.el.classList.add("hidden");
    }
  }

  function destroy() {
    cache.clear();
    layer.remove();
  }

  return { setNodes, setPinned, setOnLabelClick, layout, destroy };
}
