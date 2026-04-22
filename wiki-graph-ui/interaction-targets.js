function lerp(start, end, amount) {
  return start + (end - start) * amount;
}

function zoomProgressForScale(scale) {
  return Math.max(0, Math.min(1, (scale - 0.55) / 2.75));
}

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

export function buildLabelTargets({
  nodes,
  highlightedId,
  canvasSize,
  view,
  nodeRadius,
  measureText,
}) {
  const zoomT = zoomProgressForScale(view.scale);
  const labelDegreeThreshold = view.scale >= 1.8 ? 0 : view.scale >= 1.05 ? 2 : 5;
  const labelMaxChars = view.scale >= 2.1 ? 56 : view.scale >= 1.4 ? 42 : 32;
  const maxLabels = view.scale >= 2.3 ? 150 : view.scale >= 1.35 ? 95 : 40;
  const occupiedLabelRects = [];
  const labelTargets = [];
  const labelCandidates = nodes
    .filter((node) => node.degree >= labelDegreeThreshold || highlightedId === node.id)
    .sort((a, b) => {
      const aHighlighted = highlightedId === a.id ? 1 : 0;
      const bHighlighted = highlightedId === b.id ? 1 : 0;
      return bHighlighted - aHighlighted || b.degree - a.degree;
    });

  for (const node of labelCandidates) {
    const highlighted = highlightedId === node.id;
    if (!highlighted && occupiedLabelRects.length >= maxLabels) break;

    const label = node.title.slice(0, labelMaxChars);
    const screenFontPx = highlighted
      ? Math.round(lerp(13, 21, zoomT))
      : Math.round(lerp(10, 18, zoomT));
    const fontWorldPx = screenFontPx / view.scale;
    const padX = (highlighted ? 8 : 6) / view.scale;
    const padY = (highlighted ? 5 : 4) / view.scale;
    const chipRadius = 10 / view.scale;
    const offsetY = (highlighted ? 11 : 8) / view.scale;
    const labelWidth = measureText(label, fontWorldPx) + padX * 2;
    const labelHeight = fontWorldPx + padY * 2;
    const x = node.x - labelWidth / 2;
    const y = node.y - nodeRadius(node) - labelHeight - offsetY;
    const screenRect = {
      x: canvasSize.width / 2 + view.tx + x * view.scale,
      y: canvasSize.height / 2 + view.ty + y * view.scale,
      w: labelWidth * view.scale,
      h: labelHeight * view.scale,
    };

    if (!highlighted && occupiedLabelRects.some((rect) => rectOverlaps(rect, screenRect, 6))) {
      continue;
    }
    occupiedLabelRects.push(screenRect);
    labelTargets.push({
      node,
      label,
      highlighted,
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
