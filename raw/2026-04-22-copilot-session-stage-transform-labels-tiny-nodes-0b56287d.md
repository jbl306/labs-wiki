---
title: "Copilot Session Checkpoint: Stage-transform labels, tiny nodes"
type: text
captured: 2026-04-22T13:56:04.647033Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: failed
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Stage-transform labels, tiny nodes
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/009-stage-transform-labels-tiny-no.md`
**Checkpoint timestamp:** 2026-04-22T13:52:28.545538Z
**Exported:** 2026-04-22T13:56:04.647033Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User is iterating on labs-wiki WebGL graph UI. After PR #27 (sharper shader, adaptive labels, wiki popup) and PR #28 (perf throttle, color tuning, CDN-friendly path encoding), user reports four still-broken issues: pinch-to-zoom is choppy, nodes look too large/busy on first load, label text flashes after zoom and doesn't auto-scale, and click-to-popup still doesn't show info. Approach: aggressively shrink nodes (3..16 px), eliminate the label opacity-fade flash by riding labels along on a single CSS transform of the stage during gestures (instead of hide/show), zoom-scale the font, and re-verify popup over CDN.
</overview>

<history>
1. User reported PR #28 didn't fix issues — pinch still bad, nodes too large, labels flash, popups still don't open.
   - Investigated: confirmed `touch-action: none` already set on canvas (styles.css:140, webgl-renderer.js:202). CDN test failed (sandbox has no internet to graph.jbl-lab.com / graph-api.jbl-lab.com).
   - Verified Caddy routing in `compose.wiki-graph.yml` is direct (no path rewriting), so `/graph/page/<id>` should pass through to FastAPI's `{node_id:path}` route untouched.
   - Diagnosed root causes:
     - Sizes 5..28 → at DPR 2 = 10..56 px on screen, still bloomy.
     - Label flash = the 0.12s opacity transition on `.interacting` toggle = visible fade-out/fade-in.
     - No font scaling = labels feel static when zooming.
     - Pinch = math correct but each pointermove triggers a full draw + per-frame label layout (even if cheap, the iteration over 700 candidates plus DOM transforms costs).
   - Implemented:
     - Tightened `sizeOf` in app.js: floor 3, max 16, multiplier 2.4 (was 5/28/3.2).
     - Rewrote `labels-overlay.js` from scratch with a two-div architecture: outer `#webgl-labels` (positioned, clips), inner `.webgl-label-stage` (gets a single CSS `transform: translate3d() scale()` during gestures so labels track the camera mathematically without per-label re-layout).
     - On gesture start: snapshot `gestureCam`. On every transform during gesture: compute `k = cam.scale/layoutCam.scale`, `tx = (W/2)*(1-k) + cam.scale*(layoutCam.x - cam.x)`, `ty = (H/2)*(1-k) + cam.scale*(layoutCam.y - cam.y)`, apply as stage transform.
     - On settle: reset stage transform, run real layout in new screen frame.
     - Zoom-scaled font: `clamp(9, 10 + log2(max(0.35, scale)) * 2.2, 20)` px. When font size changes, mark all cached labels for re-measurement.
     - Layout throttle interval bumped to 60ms (~16 Hz) with trailing schedule. Settle reduced to 120ms.
     - Removed all `.hidden` / fade-out behavior — labels stay visible the entire time.

   - **STOPPED MID-WORK** before deploy and validate. The previous user message was the start of this round; compaction triggered after creating the new labels-overlay.js. Have NOT yet:
     - Removed the now-stale CSS `#webgl-labels.interacting { opacity: 0; pointer-events: none; }` rule (added in PR #28). It will incorrectly fade labels on the rare frame when interacting class might briefly attach via legacy code path — actually I removed the `layer.classList.toggle("interacting", on)` call in the rewrite, so this CSS rule is just dead code but won't cause harm.
     - Rebuilt the container.
     - Run Playwright validation.
     - Verified popup actually works through Cloudflare (still can't reach external from sandbox).
     - Committed/pushed/PR'd/merged.
</history>

<work_done>
Files modified this round:
- `wiki-graph-ui/app.js` — sizeOf floor/max/mult cut to 3/16/2.4 (~line 151-157)

Files rewritten this round:
- `wiki-graph-ui/labels-overlay.js` — completely replaced with two-div stage architecture, gesture-transform tracking, zoom-scaled font, no-fade UX. ~10.3KB, ~265 lines.

Work completed this round:
- [x] Aggressive node-size reduction
- [x] Rewrite labels-overlay with stage-transform gesture tracking
- [x] Zoom-scaled label font
- [ ] Remove dead `#webgl-labels.interacting` CSS rule (low priority; harmless)
- [ ] Sanity-check pinch math is robust on touch devices (might need to also drop `setPointerCapture` in webgl-renderer.js for multi-touch reliability — NOT done yet)
- [ ] Investigate "popups still don't work" — couldn't reproduce; my last validator showed popup loads ~5KB. May be browser cache for user. Have NOT added explicit cache-bust on the fetch.
- [ ] Rebuild container: `cd /home/jbl/projects/homelab/compose && docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui`
- [ ] Run Playwright validator (`/tmp/validate_v3.py` exists, can extend or reuse)
- [ ] Commit, push, PR, merge to main

Untested: ALL of the changes above. Container has not been rebuilt since the rewrite.
</work_done>

<technical_details>
- **Stage-transform math (gesture tracking)**: labels are positioned in absolute screen pixels at the time of `runLayout`. During a gesture, instead of re-laying out, apply one CSS transform on the stage div that maps "label positions in the snapshot frame" → "where they should appear now":
  - `k = cam.scale / layoutCam.scale`
  - `tx = (W/2)*(1-k) + cam.scale*(layoutCam.x - cam.x)`
  - `ty = (H/2)*(1-k) + cam.scale*(layoutCam.y - cam.y)`
  - `stage.style.transform = translate3d(tx, ty, 0) scale(k)`
  - This is exact for any pan + zoom-around-arbitrary-anchor. After gesture, reset to identity and re-layout.

- **Why the previous PR #28 fix flashed**: I had `layer.classList.toggle("interacting", on)` + CSS `#webgl-labels.interacting { opacity: 0; transition: 0.12s }`. The fade itself = the flash. New design has zero opacity transitions; labels are always opaque, they just ride along during gestures.

- **Font scaling**: `clamp(9, 10 + log2(max(0.35, cam.scale)) * 2.2, 20)`. At fit-zoom (~0.4) → ~7.1 → clamped 9. At 1.0 → 10. At 2.0 → 12.2. At 4.0 → 14.4. Caches need invalidation when font changes (width changes) — flagged via `entry._needsMeasure = true`.

- **Sizes timeline**: original PR #27 was 8/46/5.2; PR #28 was 5/28/3.2; current 3/16/2.4. At DPR 2 the actual gl_PointSize is doubled, so visible disc is 6..32 px. Hub halo extends to d=1.0 of the point sprite, so visible hub bloom ≈ 32 px wide. Should read clean at fit-zoom on a 700-node graph.

- **Cloudflare/popups**: per-segment encoding (`split('/').map(encodeURIComponent).join('/')`) was added in PR #28 and validator confirmed popup works locally over `http://172.20.1.25:3000`. Cannot test through `https://graph.jbl-lab.com` — sandbox network blocked. User reports "still don't work" — possibly stale browser cache (build IDs are baked in via `?v=__BUILD_ID__` so hard-refresh should bust). If still broken after this PR, next step is to add explicit `?ts=${Date.now()}` to the fetch and surface the actual HTTP status in the popup error message.

- **Layout interval bumped 40→60ms** (~16 Hz instead of 25 Hz). Steady-state is when the user is *not* gesturing, so 16 Hz is fine and saves work for the rare cases the renderer issues spurious frames.

- **Pinch reliability concern (not yet addressed)**: webgl-renderer.js uses `canvas.setPointerCapture(e.pointerId)` on every pointerdown including the second touch. Some browsers won't grant capture to a second pointer when the first is already captured, which can cause its pointermove events to fire on the original target instead of being captured. May need to switch to window-level pointermove listeners during gesture or stop calling setPointerCapture for non-primary pointers. Have NOT investigated whether this is the actual cause of "pinch doesn't work well" — user feedback is subjective and validator showed reasonable headless FPS.

- **Dead CSS**: `#webgl-labels.interacting { opacity: 0; pointer-events: none; transition: opacity 0.12s ease-out; }` in styles.css line ~342. Harmless because the rewrite never adds the `.interacting` class. Should be cleaned up for hygiene but not blocking.

- **Build cache-bust**: Dockerfile entrypoint rewrites `__BUILD_ID__` placeholder with epoch timestamp at container start. Imports in app.js use `?v=__BUILD_ID__` and get baked. Verified PR #28 build ID was `1776864277` and propagated through all dynamic imports. Hard-refresh required for users to pick up new build.

- **Validator**: `/tmp/validate_v3.py` does desktop+mobile probe with click-position scan and synthetic drag perf measurement. Headless chromium has no GPU so FPS numbers are conservative. `interactingDuringDrag` polling timing was buggy in v3 (polled after settle); separate inline test confirmed `.interacting` toggles correctly mid-gesture. With the new stage-transform design, there's no `.interacting` class anymore — validator needs updating to instead check that `stage.style.transform` becomes non-empty during a drag.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/labels-overlay.js`
  - Completely rewritten this round. Two-div architecture: outer `#webgl-labels` clips, inner `.webgl-label-stage` gets transformed during gestures.
  - Key sections: `setInteracting` (snapshots cam at gesture start, resets on end, line ~75), `applyGestureTransform` (the affine math, ~line 165), `runLayout` (stamps `layoutCam`, sets font-size, runs greedy collision, ~line 178), font-size formula (~line 184).
  - Public API unchanged: `{ setNodes, setPinned, setOnLabelClick, layout, destroy }`.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js`
  - sizeOf in syncGpuStyle reduced to 3..16 floor/max with mult 2.4 (~line 151).
  - encodePathId helper from PR #28 still in place (~line 186).
  - Wiring of label overlay unchanged (renderer.onTransform → gpuLabels.layout, ~line 127).

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/webgl-renderer.js`
  - Custom WebGL2 renderer with PR #28's tuned shader (white-blend 0.12, specular 0.35, mid-band/halo richer).
  - **Potential issue area for pinch**: `setPointerCapture` on every pointerdown (line ~548). Not yet modified.
  - `getCamera()` exposes `{x, y, scale, viewW, viewH, worldToScreen, screenToWorld}` — used by overlay's gesture-transform math.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/styles.css`
  - Has dead `#webgl-labels.interacting { opacity: 0 }` rule (~line 342). Stage will never get this class with the rewrite — harmless but should be removed for hygiene.
  - `#node-panel` mobile sizing intact from PR #27 (line 309 + 469 override).
  - `.webgl-label`, `.webgl-label.pinned`, `.webgl-label.hidden` rules preserved.

- `/home/jbl/projects/labs-wiki/wiki-graph-api/main.py`
  - `/graph/page/{node_id:path}` endpoint from PR #27 confirmed working locally with both encoded and unencoded paths. Returns `{id, title, path, page_type, tier, tags, last_verified, body}`.

- `/home/jbl/projects/homelab/compose/compose.wiki-graph.yml`
  - Build context = `${WIKI_INGEST_PATH}` (= `../../labs-wiki`). Always invoke from `compose/` dir with `--env-file ../.env`.

- `/tmp/validate_v3.py`
  - Playwright validator. Needs updating: change `.interacting` class check to `stage.style.transform !== ''` mid-drag.

- `/tmp/pwenv/bin/python` — Playwright venv with chromium 145.
</important_files>

<next_steps>
Immediate (resume here):

1. **Optionally clean dead CSS** in styles.css line ~342: remove `#webgl-labels.interacting { opacity: 0; pointer-events: none; }` (rewrite no longer adds that class).

2. **Syntax check & rebuild**:
   ```bash
   cd /home/jbl/projects/labs-wiki && \
     node --check wiki-graph-ui/labels-overlay.js && \
     node --check wiki-graph-ui/app.js && \
     cd /home/jbl/projects/homelab/compose && \
     docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui
   ```

3. **Update + run validator** (`/tmp/validate_v3.py`): replace `interactingDuringDrag` check with `stageTransformDuringDrag` checking `document.querySelector('.webgl-label-stage').style.transform !== ''`. Also extend to:
   - Verify font-size changes after wheel zoom in (read `stage.style.fontSize` before and after).
   - Take screenshots at fit-zoom AND zoomed-in (mouse wheel) to confirm sizes look reasonable in both.
   - Click multiple positions until popup opens; print contentLen.

4. **If validator passes**, commit + PR + merge:
   ```bash
   cd /home/jbl/projects/labs-wiki && git checkout -b fix/labels-stage-transform-tiny-nodes && \
     git add wiki-graph-ui/ && \
     git commit -m "fix(graph-ui): tiny nodes, stage-transform labels (no flash), zoom-scaled font" && \
     git push -u origin fix/labels-stage-transform-tiny-nodes && \
     gh pr create --fill --base main && gh pr merge --squash --delete-branch
   ```

5. **If pinch is still reported as bad**, next iteration should:
   - Remove `setPointerCapture` for non-primary pointers in webgl-renderer.js, OR move pointermove listening to window during active gesture.
   - Consider rAF-coalescing the renderer's pointermove → zoomAt → schedule(draw) chain so multiple pointermoves in one frame collapse to one zoom calculation.

6. **If popups still reported broken**, add explicit cache-bust + visible HTTP status on error in showNodePanel:
   ```js
   fetchJSON(`/graph/page/${encodePathId(node.id)}?_=${Date.now()}`)
     .catch((e) => { contentEl.innerHTML = `<div class='muted'>page unavailable: ${e.message}</div>`; });
   ```
   Then ask user to open DevTools Network tab and report the actual response.

7. **Update SQL todos** + MemPalace drawer for labs_wiki/graph-ui wing.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
