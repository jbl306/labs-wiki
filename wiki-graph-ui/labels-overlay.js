import { buildLabelTargets } from "./interaction-targets.js?v=__BUILD_ID__";

export function createLabelOverlay({ container, renderer, communityLabel }) {
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

  const labels = new Map();
  const measure = document.createElement("canvas").getContext("2d");
  const fontFamily = getComputedStyle(container).fontFamily;
  let nodes = [];
  let pinned = new Set();
  let selected = null;
  let neighbors;
  let focused = false;
  let onLabelClick = null;

  // Snapshot of the camera *at the time labels were last laid out*.
  // The stage transform is computed against this so labels can ride along
  // with the camera without per-label work.
  let layoutCam = null;

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
    if (!on) {
      // Reset stage to identity and force a fresh layout in the new
      // screen frame.
      stage.style.transform = "";

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

  function setNodes(newNodes) {
    nodes = newNodes;
    runLayout(renderer.getCamera());
  }
  function setPinned(ids, selectedId, neighborhood, focus) {
    pinned = ids;
    selected = selectedId;
    neighbors = neighborhood;
    focused = focus;
  }
  function setOnLabelClick(cb) { onLabelClick = cb; }

  // The renderer fires this every drawn frame. During an active gesture we
  // *do not* re-layout; we just transform the stage to ride along with the
  // camera. On settle we'll do a real layout once.
  function layout(cam) {
    if (!cam) return;
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

    const view = { scale: cam.scale, fitScale: cam.fitScale, tx: -cam.x * cam.scale, ty: -cam.y * cam.scale };
    const targets = buildLabelTargets({
      nodes, highlightedId: selected, pinnedIds: pinned, neighbors, focused, communityLabel,
      canvasSize: { width: W, height: H }, view,
      nodeRadius: () => 4 / cam.scale,
      measureText(label, worldFont) {
        measure.font = `500 ${Math.round(worldFont * cam.scale)}px ${fontFamily}`;
        return measure.measureText(label).width / cam.scale;
      },
    });
    const visible = new Set();
    for (const { node, label, highlighted, screenRect } of targets) {
      visible.add(node.id);
      let button = labels.get(node.id);
      if (!button) {
        button = document.createElement("button");
        button.type = "button";
        button.className = "webgl-label";
        button.dataset.id = node.id;
        stage.appendChild(button);
        labels.set(node.id, button);
      }
      button.onclick = () => onLabelClick?.(node);
      button.setAttribute("aria-label", node.title || node.id);
      button.title = node.title || node.id;
      button.textContent = label;
      button.classList.toggle("pinned", highlighted);
      button.style.width = `${Math.ceil(screenRect.w)}px`;
      button.style.height = `${Math.ceil(screenRect.h)}px`;
      button.style.transform = `translate3d(${Math.round(screenRect.x)}px, ${Math.round(screenRect.y)}px, 0)`;
    }
    for (const [id, button] of labels) {
      if (!visible.has(id)) { button.remove(); labels.delete(id); }
    }
  }

  function destroy() {
    clearTimeout(settleTimer);
    clearTimeout(pendingTimer);
    labels.clear();
    layer.remove();
  }

  return { setNodes, setPinned, setOnLabelClick, layout, destroy };
}
