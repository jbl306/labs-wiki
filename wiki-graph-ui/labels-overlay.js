// Adaptive HTML label overlay for the WebGL graph renderer.
//
// Architecture:
//   - Two nested <div>s. The outer (#webgl-labels) is layered over the
//     canvas and CSS-transformed to follow the camera *during* gestures
//     so labels move pixel-perfect with the GPU without any per-label
//     work. The inner (.webgl-label-stage) holds the actual labels with
//     their absolute positions in the **last laid-out screen frame**.
//   - On gesture start we snapshot cam0 (x0, y0, scale0). On every
//     transform during the gesture we compute the affine that maps
//     "where the labels were drawn" to "where they should appear now"
//     and apply it as a single CSS `transform: translate3d() scale()`
//     on the stage. Cheap. Smooth. No flash.
//   - When the gesture ends we re-layout once (positions become exact
//     in the new screen frame) and reset the stage transform to identity.
//   - Steady-state (no gesture) layout is throttled to ~25 Hz with a
//     trailing schedule.
//   - Font-size scales mildly with zoom so labels grow when you zoom in
//     and shrink when you zoom out — but capped so they never become
//     illegible or oversized.

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

  const stage = document.createElement("div");
  stage.className = "webgl-label-stage";
  stage.style.cssText = [
    "position:absolute",
    "inset:0",
    "pointer-events:none",
    "transform-origin:0 0",
    "will-change:transform",
  ].join(";");
  layer.appendChild(stage);
  container.appendChild(layer);

  // node id -> { el, w, h, measuredFontPx }
  // `w`/`h` are the label box dimensions in CSS pixels at `measuredFontPx`.
  // When the stage font-size changes we *scale* w/h by the ratio rather
  // than calling getBoundingClientRect — which would force a synchronous
  // reflow per label (layout thrash) and freeze the main thread on every
  // zoom settle. Width is linear in font-size for fixed text, so this is
  // pixel-accurate to within sub-pixel rounding.
  const cache = new Map();
  let nodes = [];
  let pinned = new Set();
  let onLabelClick = null;
  let currentFontPx = 0;

  // Snapshot of the camera *at the time labels were last laid out*.
  // The stage transform is computed against this so labels can ride along
  // with the camera without per-label work.
  let layoutCam = null;
  // Snapshot of the camera at the start of the *current* gesture. Used
  // to keep transforms numerically stable across long gestures.
  let gestureCam = null;

  // Interaction tracking — drives both the gesture-transform behaviour
  // and the throttled-layout behaviour.
  let activePointers = 0;
  let interacting = false;
  let settleTimer = null;
  let lastLayoutTs = 0;
  let pendingCam = null;
  let pendingTimer = null;
  // Settle quickly once the user lifts their finger / stops scrolling so
  // the labels snap to their final positions instead of lingering at the
  // pre-zoom transform for a noticeable beat.
  const LAYOUT_INTERVAL_MS = 30;
  const SETTLE_MS = 50;

  function setInteracting(on) {
    if (interacting === on) return;
    interacting = on;
    if (on) {
      // Snapshot the camera so subsequent transforms during this gesture
      // are computed relative to a stable origin.
      gestureCam = renderer.getCamera();
    } else {
      // Reset stage to identity and force a fresh layout in the new
      // screen frame.
      stage.style.transform = "";
      gestureCam = null;
      const cam = pendingCam || renderer.getCamera();
      pendingCam = null;
      runLayout(cam);
    }
  }

  function bumpInteraction() {
    setInteracting(true);
    if (settleTimer) clearTimeout(settleTimer);
    settleTimer = setTimeout(() => setInteracting(false), SETTLE_MS);
  }

  // We listen on the container so any gesture inside the graph host (touch,
  // mouse, wheel) triggers gesture mode. passive:true so we never fight the
  // canvas's own pointer handlers.
  container.addEventListener("pointerdown", () => {
    activePointers += 1;
    bumpInteraction();
  }, { passive: true });
  const releasePointer = () => {
    activePointers = Math.max(0, activePointers - 1);
    if (activePointers === 0) bumpInteraction();
  };
  container.addEventListener("pointerup", releasePointer, { passive: true });
  container.addEventListener("pointercancel", releasePointer, { passive: true });
  container.addEventListener("wheel", () => bumpInteraction(), { passive: true });

  function setNodes(newNodes) { nodes = newNodes || []; }
  function setPinned(idSet) { pinned = idSet ? new Set(idSet) : new Set(); }
  function setOnLabelClick(cb) { onLabelClick = cb; }

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
    stage.appendChild(el);
    // Defer measurement to the batched read pass in runLayout so we don't
    // interleave reads/writes and force per-label synchronous reflows.
    return { el, w: 0, h: 0, measuredFontPx: 0 };
  }

  function getEl(node) {
    let entry = cache.get(node.id);
    if (!entry) {
      entry = makeEl(node);
      cache.set(node.id, entry);
    }
    return entry;
  }

  // The renderer fires this every drawn frame. During an active gesture we
  // *do not* re-layout; we just transform the stage to ride along with the
  // camera. On settle we'll do a real layout once.
  function layout(cam) {
    if (!cam || !nodes.length) return;
    if (interacting) {
      pendingCam = cam;
      applyGestureTransform(cam);
      // Camera is still moving — push the settle deadline out.
      if (settleTimer) clearTimeout(settleTimer);
      settleTimer = setTimeout(() => setInteracting(false), SETTLE_MS);
      return;
    }
    const now = performance.now();
    const since = now - lastLayoutTs;
    if (since >= LAYOUT_INTERVAL_MS) {
      runLayout(cam);
      return;
    }
    pendingCam = cam;
    if (pendingTimer) return;
    pendingTimer = setTimeout(() => {
      pendingTimer = null;
      const c = pendingCam;
      pendingCam = null;
      if (c) runLayout(c);
    }, LAYOUT_INTERVAL_MS - since);
  }

  // Compute and apply the affine that maps the snapshot frame (when labels
  // were last laid out) to the current camera. Single CSS transform = GPU.
  function applyGestureTransform(cam) {
    if (!layoutCam) return;
    const W = cam.viewW || layoutCam.viewW;
    const H = cam.viewH || layoutCam.viewH;
    const k = cam.scale / layoutCam.scale;
    const tx = (W / 2) * (1 - k) + cam.scale * (layoutCam.x - cam.x);
    const ty = (H / 2) * (1 - k) + cam.scale * (layoutCam.y - cam.y);
    stage.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${k})`;
  }

  function runLayout(cam) {
    lastLayoutTs = performance.now();
    layoutCam = { x: cam.x, y: cam.y, scale: cam.scale, viewW: cam.viewW, viewH: cam.viewH };
    stage.style.transform = ""; // identity in the new frame
    const W = cam.viewW, H = cam.viewH;

    // Font scales mildly with zoom. clamp prevents either extreme.
    const fontPx = Math.max(9, Math.min(20, 10 + Math.log2(Math.max(0.35, cam.scale)) * 2.2));
    let fontChanged = false;
    if (fontPx !== currentFontPx) {
      stage.style.fontSize = fontPx + "px";
      // Width is linear in font-size for fixed text content, so we can
      // scale cached dimensions instead of forcing a per-label
      // getBoundingClientRect (which would reflow the page N times and
      // produce the multi-hundred-millisecond freeze users see when
      // zooming). Entries with measuredFontPx===0 are still pending
      // their first measurement and will be batched-measured below.
      for (const entry of cache.values()) {
        if (entry.measuredFontPx > 0) {
          const ratio = fontPx / entry.measuredFontPx;
          entry.w = Math.max(1, Math.ceil(entry.w * ratio));
          entry.h = Math.max(1, Math.ceil(entry.h * ratio));
          entry.measuredFontPx = fontPx;
        }
      }
      currentFontPx = fontPx;
      fontChanged = true;
    }

    // Budget grows with zoom so wide views stay sparse, zoomed-in views show
    // detail. Tighter on small screens so labels don't carpet the canvas.
    const isSmall = (cam.viewW || 0) < 760;
    const zoomFactor = Math.min(4, Math.max(0.3, cam.scale));
    const baseBudget = isSmall ? 10 : 22;
    let budget = Math.round(baseBudget * Math.pow(zoomFactor / 0.5, 0.9));
    budget = Math.max(isSmall ? 6 : 14, Math.min(isSmall ? 80 : 180, budget));

    const candidates = [];
    for (const n of nodes) {
      const sx = (n.x - cam.x) * cam.scale + W / 2;
      const sy = (n.y - cam.y) * cam.scale + H / 2;
      // Cull off-screen.
      if (sx < -120 || sx > W + 120 || sy < -40 || sy > H + 40) continue;
      const isPinned = pinned.has(n.id);
      const imp = (isPinned ? 1e9 : 0) + (n.degree || 0) + (n.tier === "core" ? 5 : 0);
      candidates.push({ node: n, sx, sy, imp, pinned: isPinned });
    }
    candidates.sort((a, b) => b.imp - a.imp);

    // ---- Read pass: measure any unmeasured labels in one batch.
    // Collect entries in candidate order so we touch only what we'll
    // probably draw. Reads happen here with no intervening style writes,
    // so the browser does at most one layout for the whole batch.
    const toMeasure = [];
    const entries = new Array(candidates.length);
    for (let i = 0; i < candidates.length; i++) {
      const entry = getEl(candidates[i].node);
      entries[i] = entry;
      if (entry.measuredFontPx === 0) toMeasure.push(entry);
    }
    if (toMeasure.length) {
      for (const entry of toMeasure) {
        const r = entry.el.getBoundingClientRect();
        entry.w = Math.ceil(r.width) || 60;
        entry.h = Math.ceil(r.height) || 16;
        entry.measuredFontPx = fontPx;
      }
    }

    // ---- Write pass: collision-test then position. No reads from here on.
    const BUCKET = 96;
    const buckets = new Map();
    const visible = new Set();

    function key(bx, by) { return bx + "," + by; }
    function intersects(rect) {
      const minBx = Math.floor(rect.x / BUCKET);
      const maxBx = Math.floor((rect.x + rect.w) / BUCKET);
      const minBy = Math.floor(rect.y / BUCKET);
      const maxBy = Math.floor((rect.y + rect.h) / BUCKET);
      for (let bx = minBx; bx <= maxBx; bx++) {
        for (let by = minBy; by <= maxBy; by++) {
          const arr = buckets.get(key(bx, by));
          if (!arr) continue;
          for (const r of arr) {
            if (rect.x < r.x + r.w && rect.x + rect.w > r.x &&
                rect.y < r.y + r.h && rect.y + rect.h > r.y) return true;
          }
        }
      }
      return false;
    }
    function add(rect) {
      const minBx = Math.floor(rect.x / BUCKET);
      const maxBx = Math.floor((rect.x + rect.w) / BUCKET);
      const minBy = Math.floor(rect.y / BUCKET);
      const maxBy = Math.floor((rect.y + rect.h) / BUCKET);
      for (let bx = minBx; bx <= maxBx; bx++) {
        for (let by = minBy; by <= maxBy; by++) {
          const k = key(bx, by);
          let arr = buckets.get(k);
          if (!arr) { arr = []; buckets.set(k, arr); }
          arr.push(rect);
        }
      }
    }

    for (let i = 0; i < candidates.length; i++) {
      const c = candidates[i];
      if (visible.size >= budget && !c.pinned) break;
      const entry = entries[i];
      // Position label below the node, beyond the bloomy halo. The halo
      // visible diameter ≈ 2.4× the dot radius for hub nodes, so we push
      // labels by `r * 1.6 + 8` to keep them clear of the node sprite.
      const deg = Math.max(1, c.node.degree || 1);
      const r = Math.min(16, 3 + Math.log2(deg + 1) * 2.4);
      const labelX = Math.round(c.sx - entry.w / 2);
      const labelY = Math.round(c.sy + r * 1.6 + 8);
      const rect = { x: labelX - 2, y: labelY - 2, w: entry.w + 4, h: entry.h + 4 };
      if (!c.pinned && intersects(rect)) continue;
      add(rect);
      visible.add(c.node.id);
      entry.el.style.transform = `translate3d(${labelX}px, ${labelY}px, 0)`;
      entry.el.classList.toggle("pinned", c.pinned);
      entry.el.classList.remove("hidden");
    }

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
