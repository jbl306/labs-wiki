import { buildLabelTargets } from "./interaction-targets.js?v=__BUILD_ID__";

export function createLabelOverlay({ container, renderer, communityLabel, colorOf, nodeRadiusPx }) {
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

  let layoutCam = null;
  let dirty = true;
  let settleTimer;
  const pointers = new Set();

  // While the camera moves, the already positioned chips travel on one layer.
  // Recompute their screen-space sizes and collisions when the gesture settles.
  function settleSoon() {
    clearTimeout(settleTimer);
    settleTimer = setTimeout(() => {
      settleTimer = null;
      if (!pointers.size) layout(renderer.getCamera());
    }, 70);
  }
  const events = new AbortController();
  const listener = { passive: true, signal: events.signal };
  container.addEventListener("pointerdown", e => pointers.add(e.pointerId), listener);
  function release(e) {
    if (pointers.delete(e.pointerId) && !pointers.size) settleSoon();
  }
  window.addEventListener("pointerup", release, listener);
  window.addEventListener("pointercancel", release, listener);
  container.addEventListener("wheel", settleSoon, listener);

  stage.addEventListener("click", e => {
    const item = labels.get(e.target.dataset.id);
    if (item) onLabelClick?.(item.node);
  });

  function setNodes(newNodes) {
    nodes = newNodes;
    dirty = true;
  }
  function setPinned(ids, selectedId, neighborhood, focus) {
    pinned = ids;
    selected = selectedId;
    neighbors = neighborhood;
    focused = focus;
    dirty = true;
  }
  function setOnLabelClick(cb) { onLabelClick = cb; }

  function layout(cam) {
    if (!cam || !cam.viewW || !cam.viewH) return;
    if (!dirty && layoutCam && (pointers.size || settleTimer)) {
      applyGestureTransform(cam);
      return;
    }
    if (dirty || !layoutCam || cam.x !== layoutCam.x || cam.y !== layoutCam.y ||
        cam.scale !== layoutCam.scale || cam.viewW !== layoutCam.viewW || cam.viewH !== layoutCam.viewH) {
      runLayout(cam);
    }
  }

  // Compute and apply the affine that maps the snapshot frame (when labels
  // were last laid out) to the current camera. Single CSS transform = GPU.
  function applyGestureTransform(cam) {
    if (!layoutCam) return;
    const W = cam.viewW || layoutCam.viewW;
    const H = cam.viewH || layoutCam.viewH;
    const k = cam.scale / layoutCam.scale;
    const tx = (W - layoutCam.viewW * k) / 2 + cam.scale * (layoutCam.x - cam.x);
    const ty = (H - layoutCam.viewH * k) / 2 + cam.scale * (layoutCam.y - cam.y);
    stage.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${k})`;
  }

  function runLayout(cam) {
    dirty = false;
    layoutCam = { x: cam.x, y: cam.y, scale: cam.scale, viewW: cam.viewW, viewH: cam.viewH };
    stage.style.transform = ""; // identity in the new frame
    const W = cam.viewW, H = cam.viewH;

    const view = { scale: cam.scale, fitScale: cam.fitScale, tx: -cam.x * cam.scale, ty: -cam.y * cam.scale };
    const targets = buildLabelTargets({
      nodes, highlightedId: selected, pinnedIds: pinned, neighbors, focused, communityLabel,
      canvasSize: { width: W, height: H }, view,
      nodeRadius: node => nodeRadiusPx(node) / cam.scale,
      measureText(label, worldFont) {
        measure.font = `500 ${Math.round(worldFont * cam.scale)}px ${fontFamily}`;
        return measure.measureText(label).width / cam.scale;
      },
    });
    const visible = new Set();
    for (const { node, label, highlighted, community, screenRect } of targets) {
      visible.add(node.id);
      let item = labels.get(node.id);
      if (!item) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "webgl-label";
        button.dataset.id = node.id;
        stage.appendChild(button);
        item = { button, node };
        labels.set(node.id, item);
      }
      const { button } = item;
      item.node = node;
      const title = node.title || node.id;
      const description = community ? `${label} — open ${title}` : title;
      if (button.getAttribute("aria-label") !== description) button.setAttribute("aria-label", description);
      if (button.title !== title) button.title = title;
      if (button.textContent !== label) button.textContent = label;
      button.classList.toggle("community", community);
      button.style.setProperty("--label-color", colorOf(node));
      button.classList.toggle("pinned", highlighted);
      button.style.width = `${Math.ceil(screenRect.w)}px`;
      button.style.height = `${Math.ceil(screenRect.h)}px`;
      button.style.transform = `translate3d(${Math.round(screenRect.x)}px, ${Math.round(screenRect.y)}px, 0)`;
    }
    for (const [id, { button }] of labels) {
      if (!visible.has(id)) { button.remove(); labels.delete(id); }
    }
  }

  function destroy() {
    clearTimeout(settleTimer);
    events.abort();
    labels.clear();
    layer.remove();
  }

  return { setNodes, setPinned, setOnLabelClick, layout, destroy };
}
