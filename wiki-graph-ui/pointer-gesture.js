const COARSE_POINTER_TAP_SLOP_PX = 16;
const FINE_POINTER_TAP_SLOP_PX = 8;

export function shouldUseCoarsePointerTapSlop({
  pointerType,
  fallbackIsCoarsePointer,
}) {
  if (pointerType === "touch") return true;
  if (pointerType === "mouse") return false;
  return fallbackIsCoarsePointer;
}

export function hasPointerMovedEnough({
  startX,
  startY,
  currentX,
  currentY,
  isCoarsePointer,
}) {
  const dx = currentX - startX;
  const dy = currentY - startY;
  const distance = Math.hypot(dx, dy);
  const slop = isCoarsePointer ? COARSE_POINTER_TAP_SLOP_PX : FINE_POINTER_TAP_SLOP_PX;
  return distance > slop;
}
