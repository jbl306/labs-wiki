---
title: "Copilot Session Checkpoint: Diagnosing offscreen popup containing-block bug"
type: text
captured: 2026-04-22T14:30:50.186278Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph]
checkpoint_class: durable-debugging
checkpoint_class_rule: "body:root cause"
retention_mode: retain
status: failed
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Diagnosing offscreen popup containing-block bug
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/010-diagnosing-offscreen-popup-con.md`
**Checkpoint timestamp:** 2026-04-22T14:18:12.445242Z
**Exported:** 2026-04-22T14:30:50.186278Z
**Checkpoint class:** `durable-debugging` (rule: `body:root cause`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User is iterating on the labs-wiki WebGL graph UI on a Galaxy S25+ (Chrome Android). After PR #30 (touch tap slop, pan clamp, +/- buttons, sparser labels) two issues remain unfixed in real device testing: (1) single drag still moves the graph too fast and far, and (2) clicking nodes still doesn't open the wiki popup anywhere. Approach: tighten the camera clamp + enforce minimum zoom = fit-scale to limit how fast/far drag feels, and find the actual root cause of popup-not-opening (likely a CSS containing-block bug where `#node-panel` is `position: fixed` inside `<aside id="sidebar">` which has `transform: translateX(-100%)` on mobile — `position:fixed` becomes positioned relative to the transformed ancestor instead of the viewport, so the panel renders OFF-SCREEN to the left when sidebar is closed).
</overview>

<history>
1. User reported on Galaxy S25+: "single drag still moves too fast" and "clicking on nodes still don't pop up wiki info anywhere"
   - Logged 2 fresh todos in SQL.
   - Inspected node-panel mobile CSS: it's `position: fixed; bottom: 12px; left/right: 12px` on mobile.
   - Inspected `.hidden` class — uses `display: none !important`. Confirmed showNodePanel removes it.
   - Looked at index.html — discovered `#node-panel` lives INSIDE `<aside id="sidebar">`.
   - Looked at sidebar styles — confirmed mobile sidebar has `transform: translateX(-100%)` (line 292).
   - **Root cause identified for popup**: `position: fixed` inside an ancestor with `transform` is positioned RELATIVE TO THAT ANCESTOR (CSS spec). When sidebar is `translateX(-100%)`, the "fixed" panel is also translated -100%, rendering completely off-screen to the left. The panel IS being shown — user just can't see it because it's offscreen.
   - Compaction triggered before implementing fix.

Pre-compaction context: Just finished investigating, was about to lift `#node-panel` out of `<aside>` (or move via JS) AND tighten the pan clamp.
</history>

<work_done>
This round (post-PR #30):
- Investigated only — NO files edited yet.
- SQL todos added: `mob-popup-css-fix`, `mob-pan-tighten` (both pending, in_progress not set yet).

Recent merged work (PR #30, already deployed):
- wiki-graph-ui/webgl-renderer.js — touch-aware tap slop (12px touch / 4px mouse via pressType), bbox cache + clampCamera() in pan/pinch/wheel/zoomAt, zoomBy(factor) export, fat pickAt radius (36px touch).
- wiki-graph-ui/app.js — wired +/- buttons to gpuRenderer.zoomBy, exposed `__pwCam`/`__pwNodes` debug hooks, popup fetch has `?_=${Date.now()}` cache-bust.
- wiki-graph-ui/labels-overlay.js — labels offset r*1.6+8 (clears halo), mobile budget 22→10.
- wiki-graph-ui/styles.css — label bg 0.78→0.55, removed backdrop-filter blur.

Headless validator passed all checks but does NOT catch the off-screen panel bug because Playwright reads `display: none` correctly — the panel IS technically "visible" in the DOM, just translated off-viewport.
</work_done>

<technical_details>
- **CSS containing-block gotcha (THE popup bug)**: `position: fixed` is normally relative to the viewport, but if ANY ancestor has `transform`, `filter`, `perspective`, or `will-change: transform`, that ancestor becomes the containing block instead. `<aside id="sidebar">` on mobile has `transform: translateX(-100%)` (styles.css line 292) — so `#node-panel` at `position: fixed; left: 12px` actually renders at `viewport_left + (-100% of sidebar width) + 12px` ≈ off-screen to the left. The validator passes because `.hidden` class is removed correctly; the panel just isn't visible to the human eye.
  - Fix options: (a) move `#node-panel` element out of `<aside>` in index.html so it's a direct body child; (b) JavaScript: `document.body.appendChild(panel)` once at init; (c) restructure CSS to not transform the sidebar (use `left: -360px` + transition instead). Option (a) is cleanest.

- **Drag-too-fast root cause**: `cam.x -= dx / cam.scale`. At fit-scale ~0.4, 1 finger px = 2.5 world units. The math is geometrically correct (graph moves 1:1 under finger), but at low zoom the bbox is small relative to viewport, so a small swipe moves the graph a large fraction of bbox.size. The MIN_SCALE clamp is currently 0.05 (line ~708 webgl-renderer.js zoomAt). Fix: cache fit scale and use it as effective minimum (you should never zoom out further than fit). Also tighten clampCamera slack — currently `bbox.size*0.15 + halfViewport*0.5` is too generous; should be `bbox.size*0.1 + halfViewport*0.2` so user can't pan more than 20% past the bbox edge.

- **Galaxy S25+ details**: DPR ~3.0, 6.7" 1440×3120 screen (CSS px ~480×1066 effective). Chrome Android. Pointer events fire normally; `touch-action: none` on canvas is honored.

- **Pre-existing PR #30 fixes that DID work** (verified by validator): zoom buttons + bbox-clamp + touch-slop + pickAt-fat-radius. These are solid.

- **Why the headless validator missed the popup bug**: it polls `document.getElementById('node-panel').classList.contains('hidden')` — that returns false correctly. It never checks `getBoundingClientRect()` to verify the panel is actually within the viewport. Validator needs: `const r = panel.getBoundingClientRect(); expect(r.left >= 0 && r.right <= window.innerWidth).true`.

- **Build/deploy**: `cd /home/jbl/projects/homelab/compose && docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui`. Build cache-bust via `__BUILD_ID__` in script imports — entrypoint replaces with epoch. Hard-refresh required.

- **Branch hygiene**: PRs #27, #28, #29, #30 all merged via squash + delete-branch to main. Working from main.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/index.html` (line 93)
  - Contains `<section id="node-panel" class="hidden">` INSIDE `<aside id="sidebar">` (line 18 opens, panel at line 93). This is the structural bug.
  - Fix: move the entire `<section id="node-panel">...</section>` block (lines 93-107) OUT of `<aside>` to be a direct child of `<body>`. Same for `#path-panel` and `#checkpoint-detail` if they have similar position:fixed mobile styling.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/styles.css`
  - Line 292: `aside#sidebar { transform: translateX(-100%); }` — the cause of the containing-block bug. Don't change this; instead move the panel out of aside.
  - Lines 309-321: `@media (max-width: 900px) { #node-panel { position: fixed; ... } }` — the styles assume viewport positioning, which only works if the element isn't in a transformed ancestor.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/webgl-renderer.js`
  - Line ~473 fit(): set `bbox` and ALSO need to cache `fitScale`. Use as effective MIN_SCALE in zoomAt.
  - Line ~708 zoomAt: `const clamped = Math.max(0.05, Math.min(20, nextScale));` — change 0.05 to `Math.max(0.05, fitScale * 0.85)` so user can only zoom out 15% past fit.
  - clampCamera slack (lines ~520-525): tighten from `0.15 + halfViewport*0.5` to `0.05 + halfViewport*0.15`.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js`
  - selectNode → showNodePanel (line ~921, ~1077). showNodePanel calls `closeSidebar()` then `openNodePanel()` on coarse-pointer. After moving `#node-panel` out of aside, openNodePanel's `body.classList.add("node-panel-open")` should still work.

- `/home/jbl/projects/homelab/compose/compose.wiki-graph.yml`
  - Build/deploy command stays the same.

- `/tmp/validate_v5.py` (deleted at end of last round; need fresh `validate_v6.py`)
  - Must add: after click + wait, `getBoundingClientRect()` on `#node-panel`, assert `left >= 0 && right <= window.innerWidth && top >= 0 && bottom <= window.innerHeight + 50`.
</important_files>

<next_steps>
Remaining work (in order):

1. **Fix popup off-screen bug** (the actual root cause):
   - Edit `wiki-graph-ui/index.html`: cut `<section id="node-panel" class="hidden">...</section>` (lines 93-107) and paste as a direct child of `<body>`, somewhere after `<aside>` closes. Same evaluation for `#path-panel` and `#checkpoint-detail` if they're in the aside and have fixed-position mobile styles.
   - OR alternative: in app.js init, do `document.body.appendChild(document.getElementById('node-panel'))` once.

2. **Tighten pan/zoom**:
   - In webgl-renderer.js fit(): cache `fitScale = Math.min(sx, sy)` alongside bbox.
   - In zoomAt(): change MIN_SCALE from 0.05 to `Math.max(0.05, (fitScale || 0.05) * 0.85)`.
   - In clampCamera(): reduce slack constants from `0.15 + 0.5` to `0.05 + 0.15`.

3. **Update validator (`/tmp/validate_v6.py`)**:
   - Add panel-in-viewport check via `getBoundingClientRect()` after click.
   - Add pan-then-tap test: pan a bit, tap a node, verify panel appears within viewport.

4. **Rebuild + validate + commit**:
   ```
   cd /home/jbl/projects/homelab/compose && docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui
   /tmp/pwenv/bin/python /tmp/validate_v6.py
   cd /home/jbl/projects/labs-wiki && git checkout -b fix/popup-offscreen-tighter-pan
   git add wiki-graph-ui/ && git commit + push + gh pr create + merge --squash --delete-branch
   ```

5. **Update MemPalace** drawer for labs_wiki/graph-ui-mobile with the containing-block lesson — this is a high-value gotcha worth recording.

6. **Mark SQL todos done** for `mob-popup-css-fix` and `mob-pan-tighten`.

Open question: are there OTHER position:fixed elements inside `<aside>` that have the same bug? Worth grepping for during the fix.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
