import assert from "node:assert/strict";
import test from "node:test";

import {
  buildLabelTargets,
  getNodeScreenPosition,
  pickNodeAtScreenPoint,
} from "../interaction-targets.js";

const canvasSize = { width: 390, height: 844 };
const view = { scale: 0.05, tx: 0, ty: 0 };

function nodeRadius(node) {
  return Math.max(3, 3 + Math.log2(1 + node.degree) * 2);
}

function measureText(label, fontWorldPx) {
  return label.length * fontWorldPx * 0.62;
}

test("visible label chips select their node on mobile-sized viewports", () => {
  const node = {
    id: "concepts/lottery-ticket-hypothesis",
    title: "Lottery Ticket Hypothesis",
    degree: 8,
    x: 0,
    y: 0,
  };

  const [labelTarget] = buildLabelTargets({
    nodes: [node],
    highlightedId: null,
    canvasSize,
    view,
    nodeRadius,
    measureText,
  });

  assert.ok(labelTarget, "expected a visible label chip");

  const hit = pickNodeAtScreenPoint({
    screenX: labelTarget.screenRect.x + labelTarget.screenRect.w / 2,
    screenY: labelTarget.screenRect.y + labelTarget.screenRect.h / 2,
    nodes: [node],
    labelTargets: [labelTarget],
    canvasSize,
    view,
    nodeRadius,
    isCoarsePointer: true,
  });

  assert.equal(hit?.id, node.id);
});

test("mobile taps keep a usable minimum hit radius when fit-to-screen zoom is tiny", () => {
  const node = {
    id: "concepts/activation-functions",
    title: "Activation Functions",
    degree: 8,
    x: 0,
    y: 0,
  };
  const center = getNodeScreenPosition(node, canvasSize, view);

  const hit = pickNodeAtScreenPoint({
    screenX: center.x + 10,
    screenY: center.y,
    nodes: [node],
    labelTargets: [],
    canvasSize,
    view,
    nodeRadius,
    isCoarsePointer: true,
  });

  assert.equal(hit?.id, node.id);
});

test("overview labels choose one hub per community and phone zoom reveals page titles", () => {
  const nodes = [
    { id: "energy", title: "Energy model", degree: 18, community: 1, x: -75, y: 0 },
    { id: "coast", title: "Coastal model", degree: 10, community: 2, x: 70, y: 0 },
    { id: "wind", title: "Wind model", degree: 1, community: 1, x: 0, y: 90 },
  ];
  const options = {
    nodes, highlightedId: null, canvasSize, nodeRadius, measureText,
    view: { scale: 1, fitScale: 1, tx: 0, ty: 0 },
    communityLabel: community => community === 1 ? "Energy" : "Water",
  };
  const overview = buildLabelTargets(options);
  assert.deepEqual(overview.map(target => target.label), ["Energy", "Water"]);
  assert.ok(overview.every(target => target.fontWorldPx * options.view.scale >= 13));
  const detail = buildLabelTargets({ ...options, view: { ...options.view, scale: 2 } });
  assert.ok(detail.some(target => target.label === "Wind model"));
  assert.ok(detail.every(target => target.label === target.node.title));
});
