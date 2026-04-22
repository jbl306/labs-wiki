import assert from "node:assert/strict";
import test from "node:test";

import {
  hasPointerMovedEnough,
  shouldUseCoarsePointerTapSlop,
} from "../pointer-gesture.js";

test("coarse-pointer touches tolerate small finger drift", () => {
  const movedEnough = hasPointerMovedEnough({
    startX: 124,
    startY: 320,
    currentX: 134,
    currentY: 322,
    isCoarsePointer: true,
  });

  assert.equal(movedEnough, false);
});

test("coarse-pointer touches still become pans once drift is clearly intentional", () => {
  const movedEnough = hasPointerMovedEnough({
    startX: 124,
    startY: 320,
    currentX: 146,
    currentY: 324,
    isCoarsePointer: true,
  });

  assert.equal(movedEnough, true);
});

test("touch pointers use coarse tap slop even on hybrid devices", () => {
  const coarse = shouldUseCoarsePointerTapSlop({
    pointerType: "touch",
    fallbackIsCoarsePointer: false,
  });

  assert.equal(coarse, true);
});
