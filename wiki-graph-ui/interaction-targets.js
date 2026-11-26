function rectOverlaps(a, b, padding = 0) {
  return !(
    a.x + a.w + padding < b.x ||
    b.x + b.w + padding < a.x ||
    a.y + a.h + padding < b.y ||
    b.y + b.h + padding < a.y
  );
}

function rectContainsPoint(rect, x, y, padding = 0) {
  return (
    x >= rect.x - padding &&
    x <= rect.x + rect.w + padding &&
    y >= rect.y - padding &&
    y <= rect.y + rect.h + padding
  );
}

export function getNodeScreenPosition(node, canvasSize, view) {
  return {
    x: canvasSize.width / 2 + view.tx + node.x * view.scale,
    y: canvasSize.height / 2 + view.ty + node.y * view.scale,
  };
}

const degreeOrders = new WeakMap();

function labelCandidates(nodes, highlightedId, pinnedIds, neighbors) {
  let order = degreeOrders.get(nodes);
  if (!order) {
    order = [...nodes].sort((a, b) => (b.degree || 0) - (a.degree || 0));
    degreeOrders.set(nodes, order);
  }
  if (highlightedId == null && !pinnedIds.size && !neighbors?.size) return order;
  const selected = [], pinned = [], nearby = [], rest = [];
  for (const node of order) {
    if (node.id === highlightedId) selected.push(node);
    else if (pinnedIds.has(node.id)) pinned.push(node);
    else if (neighbors?.has(node.id)) nearby.push(node);
    else rest.push(node);
  }
  return selected.concat(pinned, nearby, rest);
}

export function buildLabelTargets({
  nodes,
  highlightedId,
  canvasSize,
  view,
  nodeRadius,
  measureText,
  pinnedIds = new Set(),
  communityLabel = () => "",
  focused = false,
  neighbors,
}) {
  const mobile = canvasSize.width < 760;
  const zoom = view.scale / (view.fitScale || view.scale);
  const overview = zoom < 1.65 && !focused;
  const maxLabels = overview ? (mobile ? 4 : 9)
    : Math.min(mobile ? 12 : 40, Math.max(mobile ? 6 : 16, Math.round(zoom * 6)));
  const occupiedLabelRects = [];
  const labelTargets = [];
  const labeledCommunities = new Set();
  const widths = new Map();
  for (const node of labelCandidates(nodes, highlightedId, pinnedIds, neighbors)) {
    if (labelTargets.length >= maxLabels) break;
    const center = getNodeScreenPosition(node, canvasSize, view);
    if (center.x < 2 || center.x > canvasSize.width - 2 ||
        center.y < 2 || center.y > canvasSize.height - 2) continue;
    const highlighted = node.id === highlightedId || pinnedIds.has(node.id);
    const group = overview && !highlighted && node.community != null && communityLabel(node.community);
    if (group && labeledCommunities.has(node.community)) continue;
    const title = group || node.title || node.id;
    const limit = mobile ? 24 : 36;
    const label = title.length > limit ? title.slice(0, limit - 1).trimEnd() + "…" : title;
    const screenFontPx = highlighted ? 14 : 13;
    const fontWorldPx = screenFontPx / view.scale;
    const padX = (highlighted ? 8 : 6) / view.scale;
    const padY = (highlighted ? 5 : 4) / view.scale;
    const chipRadius = 5 / view.scale;
    const offsetY = (highlighted ? 11 : 8) / view.scale;
    const key = screenFontPx + " " + label;
    let labelWidth = widths.get(key);
    if (labelWidth == null) {
      labelWidth = measureText(label, fontWorldPx) + padX * 2 + 3 / view.scale;
      widths.set(key, labelWidth);
    }
    const labelHeight = fontWorldPx + padY * 2;
    const x = node.x - labelWidth / 2;
    let y = node.y - nodeRadius(node) - labelHeight - offsetY;
    const screenRect = {
      x: canvasSize.width / 2 + view.tx + x * view.scale,
      y: canvasSize.height / 2 + view.ty + y * view.scale,
      w: labelWidth * view.scale,
      h: labelHeight * view.scale,
    };

    if (screenRect.x < 2 || screenRect.x + screenRect.w > canvasSize.width - 2) continue;
    const blocked = () => screenRect.y < 2 || screenRect.y + screenRect.h > canvasSize.height - 2 ||
      occupiedLabelRects.some(rect => rectOverlaps(rect, screenRect, 6));
    if (blocked()) {
      y = node.y + nodeRadius(node) + offsetY;
      screenRect.y = center.y + (nodeRadius(node) + offsetY) * view.scale;
      if (blocked()) continue;
    }
    if (group) labeledCommunities.add(node.community);
    occupiedLabelRects.push(screenRect);
    labelTargets.push({
      node,
      label,
      highlighted,
      community: Boolean(group),
      fontWorldPx,
      chipRadius,
      worldRect: { x, y, w: labelWidth, h: labelHeight },
      screenRect,
    });
  }

  return labelTargets;
}

export function pickNodeAtScreenPoint({
  screenX,
  screenY,
  nodes,
  labelTargets,
  canvasSize,
  view,
  nodeRadius,
  isCoarsePointer,
}) {
  const labelPaddingPx = isCoarsePointer ? 8 : 4;
  for (let i = labelTargets.length - 1; i >= 0; i--) {
    const target = labelTargets[i];
    if (rectContainsPoint(target.screenRect, screenX, screenY, labelPaddingPx)) {
      return target.node;
    }
  }

  const minHitRadiusPx = isCoarsePointer ? 24 : 14;
  const hitRadiusScale = isCoarsePointer ? 4 : 2;
  let hit = null;
  let best = Infinity;

  for (const node of nodes) {
    const center = getNodeScreenPosition(node, canvasSize, view);
    const radiusPx = Math.max(nodeRadius(node) * view.scale * hitRadiusScale, minHitRadiusPx);
    const dist = Math.hypot(screenX - center.x, screenY - center.y);
    if (dist <= radiusPx && dist < best) {
      best = dist;
      hit = node;
    }
  }

  return hit;
}

// Ignore sparse outliers for the initial overview. Explicit Fit includes every page.
export function graphBounds(nodes, all) {
  const xs = [], ys = [];
  for (const { x, y } of nodes) {
    if (Number.isFinite(x) && Number.isFinite(y)) { xs.push(x); ys.push(y); }
  }
  if (!xs.length) return null;
  xs.sort((a, b) => a - b);
  ys.sort((a, b) => a - b);
  const last = xs.length - 1;
  const bounds = (lo, hi) => ({ minX: xs[lo], maxX: xs[hi], minY: ys[lo], maxY: ys[hi] });
  const full = bounds(0, last);
  return { full, view: all ? full : bounds(Math.floor(xs.length * 0.03), Math.min(last, Math.ceil(xs.length * 0.97))) };
}
