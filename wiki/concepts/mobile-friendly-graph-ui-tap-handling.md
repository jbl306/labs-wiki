---
title: "Mobile-Friendly Graph UI Tap Handling"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b70af3041d4741db64a44777acc137226f83b7d150d6fbb3afbc693de05fc53a"
sources:
  - raw/2026-04-22-copilot-session-fixing-live-graph-taps-a2ede579.md
quality_score: 100
concepts:
  - mobile-friendly-graph-ui-tap-handling
related:
  - "[[Mobile-First Graph UI Design for Wiki Systems]]"
  - "[[Systematic Debugging and Test-Driven Development for UI Regression]]"
  - "[[Copilot Session Checkpoint: Fixing Live Graph Taps]]"
tier: hot
tags: [graph-ui, mobile, touch-interaction, usability, test-driven-development]
---

# Mobile-Friendly Graph UI Tap Handling

## Overview

Mobile-friendly graph UI tap handling refers to the design and implementation of touch interaction logic that reliably opens node details in a graph visualization, even when user taps are imprecise due to finger drift or device-specific quirks. This is critical for usability on mobile devices, where precise taps are difficult and zoomed views make small targets nearly impossible to hit.

## How It Works

The initial graph UI implementation rendered node labels in screen space but performed hit-testing only on tiny node circles in world space. At fit-to-screen zoom, the effective tap target was less than 2 pixels, causing most mobile taps to miss despite visually aligning with the label. To solve this, the session introduced a shared geometry module (`interaction-targets.js`) that aligned rendered label chips and tap targets, ensuring that visible elements could be reliably selected.

However, even after this fix, users reported that taps still failed to open node details on mobile. The root cause was traced to the touch gesture logic: the UI only counted a tap if the pointer movement stayed under a strict threshold (`TAP_SLOP_PX = 8`). Real human finger taps often drift slightly, especially on touchscreens, so the UI prematurely treated these as pan gestures instead of taps.

The solution involved several steps:
- A new module (`pointer-gesture.js`) was created to encapsulate touch gesture handling, specifically distinguishing between coarse (touch) and fine (mouse/stylus) pointers.
- The tap slop threshold was made pointer-type-specific: coarse pointers (touch) use a larger radial slop, while fine pointers retain the original threshold.
- Gesture handling was updated so panning only begins after the slop is truly exceeded, and taps are recognized even with slight drift.
- Regression tests (`pointer-gesture.test.mjs`) were added to verify that both perfect taps and slightly drifting touches open the same node.

This approach leverages pointer event APIs to dynamically determine the active pointer type, rather than relying solely on media queries. The result is a robust, mobile-friendly tap interaction model that tolerates real-world touch behavior while maintaining precise selection for mouse users.

Edge cases addressed include hybrid devices (e.g., laptops with touchscreens), zoomed views where label chips are much larger than node circles, and scenarios where users rapidly alternate between tap and pan gestures. The implementation ensures that label chips remain the primary tap target, and that the UI does not begin panning until the user intentionally moves beyond the slop radius.

Trade-offs include the need to balance tap tolerance (to avoid accidental pans) against the risk of misinterpreting intentional gestures. The use of pointer-type-specific thresholds mitigates this, but requires careful testing across devices. The session also highlights the importance of regression testing and deployment validation, as packaging errors (missing JS modules) can silently break the interaction logic.

## Key Properties

- **Pointer-Type-Specific Tap Slop:** Uses a larger radial slop for coarse/touch pointers, allowing slight finger drift to still count as a tap; fine pointers retain a stricter threshold.
- **Shared Geometry for Hit-Testing:** Label chips and tap targets use the same screen-space geometry, ensuring that visible elements are reliably selectable.
- **Regression Test Coverage:** Automated tests verify that both perfect taps and slightly drifting touches open node details, and that packaging errors are caught.

## Limitations

Requires careful calibration of tap slop thresholds to avoid accidental pans or missed taps. Hybrid devices may present ambiguous pointer types, necessitating dynamic detection. Packaging errors (e.g., missing JS modules in Docker image) can silently break tap handling if not guarded by regression tests.

## Example

```js
// pointer-gesture.js
export function hasPointerMovedEnough(start, current, pointerType) {
  const slop = pointerType === 'touch' ? 16 : 8;
  const dx = current.x - start.x;
  const dy = current.y - start.y;
  return Math.sqrt(dx*dx + dy*dy) > slop;
}

// app.js
if (!hasPointerMovedEnough(pointerStart, pointerCurrent, event.pointerType)) {
  handleTap(node);
}
```

## Visual

No explicit diagrams, but the code and tests describe label chips rendered in screen space, with tap targets matching their geometry. Regression tests simulate touch gestures with slight drift and verify node selection.

## Relationship to Other Concepts

- **[[Mobile-First Graph UI Design for Wiki Systems]]** — Both focus on usability and interaction reliability for graph UIs on mobile devices.
- **[[Systematic Debugging and Test-Driven Development for UI Regression]]** — Tap handling improvements were developed and validated using TDD and regression tests.

## Practical Applications

Used in knowledge graph UIs for wiki systems, ensuring that users can reliably open node details on mobile devices. Applicable to any interactive visualization where touch precision is limited and tap targets must be robust. Critical for dashboards, network maps, and educational tools accessed via smartphones or tablets.

## Sources

- [[Copilot Session Checkpoint: Fixing Live Graph Taps]] — primary source for this concept
