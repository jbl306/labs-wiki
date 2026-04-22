---
title: "Copilot Session Checkpoint: Cosmograph renderer scaffold"
type: text
captured: 2026-04-22T12:44:16.176889Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, graph]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: failed
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Cosmograph renderer scaffold
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/006-cosmograph-renderer-scaffold.md`
**Checkpoint timestamp:** 2026-04-22T12:40:29.505742Z
**Exported:** 2026-04-22T12:44:16.176889Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User wants the labs-wiki graph UI to look more polished after multiple disappointing attempts. Strategy: accept R1-R19 as the functional baseline (already live), swap the renderer to Cosmograph (`@cosmos.gl/graph` via esm.sh CDN) per spec recommendation R15 to get organized clusters + GPU rendering, and save a net-new visual treatment plan as a fallback if user rejects Cosmograph. Constraint: zero-build-step (static files behind nginx), keep all R12-R19 features (filters, BFS path mode, NL ask, checkpoint health, side panel) working.
</overview>

<history>
1. User said graph still looked flat/simple after PR #21 (Cloudflare cache bust)
   - Reverted glow rendering (PR #20 e401df0) — branch `revert/glow-rendering` → PR #22 squash-merged
   - Container redeployed with `app.js?v=1776858128`

2. User said still flat, wanted ALL UI changes reverted to R1-R19 baseline (commit 2acc3ff), keep functional improvements
   - `git checkout 2acc3ff -- wiki-graph-ui/ wiki-graph-api/main.py wiki-graph-api/requirements.txt`
   - Re-applied cache-bust infra (`?v=__BUILD_ID__` placeholders + entrypoint sed + CDN-Cache-Control headers) since these are infra not UI
   - Branch `revert/ui-to-r1-r19` → PR #23 squash-merged
   - Container redeployed with `app.js?v=1776858541`

3. User said still completely flat — asked for review of plans/reports vs live implementation
   - Audited `plans/*.md` and `reports/full-review-2026-04-21.md` against current code
   - Found NO mention of glow/halo/gradients/shadows/3D anywhere in any spec ever
   - Verified R12, R13, R14, R16, R17, R19 all live; only **R15 (Cosmograph swap or server-side precomputed layout) is unshipped** — this explains the "circle layout" complaint
   - Reported to user: their "polished after R1-R19" memory doesn't match any commit history; current state IS the spec'd target

4. User: "swap to cosmograph and accept r1-r19. save the net new visual plan if i dont like the change."
   - Created `plans/graph-ui-visual-pass.md` (fallback design doc with halo+disc+specular treatment, mobile bottom sheet, edge tier-weighting, phasing)
   - Created branch `feature/cosmograph-renderer`
   - Researched Cosmograph: `@cosmograph/cosmograph` is too heavy (DuckDB WASM, Mosaic, Apache Arrow). Used lower-level **`@cosmos.gl/graph@2.6.4`** instead (the standalone WebGL force-graph engine that powers Cosmograph) — single dep via esm.sh
   - Created `wiki-graph-ui/cosmos-renderer.js` with `createCosmosRenderer({container, onPointClick, onBackgroundClick})` exposing `syncData`, `syncStyle`, `focusNode`, `setSelectedNodes`, `fit`, `render`
   - Edited `config.js` to add `renderer: "cosmos"` flag
   - Edited `index.html` to add `<div id="graph-cosmos" hidden></div>` next to canvas
   - Edited `styles.css` to add `#graph-cosmos` sizing rules
   - **Compaction triggered before wiring `app.js` to use the cosmos renderer**
</history>

<work_done>
Files created:
- `plans/graph-ui-visual-pass.md` — fallback visual design plan (halo+disc+specular, mobile bottom sheet, phased rollout, references commit `da26467` for reusable glow code)
- `wiki-graph-ui/cosmos-renderer.js` — wraps `@cosmos.gl/graph@2.6.4` from esm.sh, handles id↔index mapping, color parsing (hsl/hex/rgba → Float32Array RGBA), point clusters by community, click→node lookup callback

Files modified (uncommitted on `feature/cosmograph-renderer` branch):
- `wiki-graph-ui/config.js` — added `renderer: "cosmos"` field with URL-param override comment
- `wiki-graph-ui/index.html` — added `<div id="graph-cosmos" hidden></div>` after canvas
- `wiki-graph-ui/styles.css` — added `#graph-cosmos` rules (full size, hidden when [hidden] attr present)

Merged to main this session:
- [x] PR #22 (`revert/glow-rendering`) — dropped 78 lines of halo/disc/specular code
- [x] PR #23 (`revert/ui-to-r1-r19`) — restored entire `wiki-graph-ui/` + `wiki-graph-api/main.py` to commit 2acc3ff, kept cache-bust infra

Pending (compaction interrupted mid-task):
- [ ] Wire `app.js` to consume `cosmos-renderer.js` when `RENDERER === "cosmos"`
- [ ] Commit + PR + merge `feature/cosmograph-renderer`
- [ ] Rebuild container + smoke test
</work_done>

<technical_details>
- **Cosmograph package choice**: `@cosmograph/cosmograph@2.2.1` pulls DuckDB WASM, Mosaic, Apache Arrow, Supabase — way too heavy. **Use `@cosmos.gl/graph@2.6.4` instead** — pure WebGL force-graph engine (formerly `@cosmograph/cosmos`), what we actually need. ESM via `https://esm.sh/@cosmos.gl/graph@2.6.4?bundle`.

- **`@cosmos.gl/graph` API** (v2.x, NOT v3 — v3 has async init that complicates things):
  - `new Graph(divElement, config)` — synchronous
  - `setPointPositions(Float32Array[x1,y1,...])` — initial positions; sim runs from these
  - `setLinks(Float32Array[srcIdx, tgtIdx, ...])` — index-based, not id-based
  - `setPointColors(Float32Array[r,g,b,a, ...])` — values 0..1
  - `setPointSizes(Float32Array[size, ...])` — pixel sizes
  - `setPointClusters(Float32Array[clusterId, ...])` — cluster force pulls same-cluster nodes together
  - `onClick: (pointIndex) => ...` — `pointIndex < 0` or null = background click
  - `render()`, `fitView(durationMs)`, `zoomToPointByIndex(idx, ms, scale, animate)`, `selectPointsByIndices`, `unselectPoints`
  - Supports `fitViewOnInit`, `simulationFriction`, `simulationGravity`, `simulationRepulsion`, `simulationLinkSpring`, `simulationLinkDistance`, `simulationDecay`, `pointGreyoutOpacity`, `linkGreyoutOpacity`

- **Renderer abstraction strategy** chosen for the swap (not yet executed in app.js):
  1. Top of `app.js`: `const RENDERER = (new URLSearchParams(location.search).get("renderer")) || cfg.renderer || "canvas"`
  2. If cosmos: hide `#graph` canvas, mount cosmos in `#graph-cosmos` div, register `onPointClick` → existing `selectNode(node)` flow
  3. Wrap `draw()` body with `if (RENDERER === "cosmos") { cosmosRenderer.syncStyle({colorOf, sizeOf, dimOf}); return; }` before existing canvas code
  4. Wrap `positionNodes()` call site in `applyFilters()` (line 123) with cosmos check → call `cosmosRenderer.syncData(nodes, edges)` instead
  5. Make `fitViewToNodes` / `centerNodeInView` / `setScale` / `resize` cosmos-aware (no-op or route to cosmos APIs)
  6. Skip pointer handler wiring in cosmos mode (cosmos owns pan/zoom/click)

- **App.js call sites** (line numbers, R1-R19 baseline):
  - `applyFilters()` line 94, calls `positionNodes()` line 123 + `fitViewToNodes()` line 124
  - `positionNodes()` line 129 (FR layout, supports R15 server-precomputed via `__server_layout` flag)
  - canvas/ctx setup line 191-192
  - `view = {scale, tx, ty}` line 194
  - `resize()` line 212 (calls `draw()`)
  - `fitViewToNodes()` line 275, `centerNodeInView()` line 305
  - `draw()` line 608 (~130 lines)
  - `bindUI()` line 1013, pointer handlers line 770+, `loadGraph()` line 997
  - bootstrap at bottom: `bindUI(); loadGraph().then(subscribeSSE);`

- **Color parsing in cosmos-renderer.js** handles `hsl(h s% l%)` (space-separated, current `colorForCommunity` output), `hsla(h, s%, l%, a)`, `#rrggbb`, `rgb()`/`rgba()`. Returns `[r,g,b,a]` floats 0..1.

- **Cluster force is the key win** — `setPointClusters(Float32Array[community, ...])` makes Cosmograph pull same-community nodes toward shared centroids. This is what fixes the "clusters not organized, sitting in a circle" complaint that pure FR misses with only 120 iterations.

- **All R12-R19 features verified live in current main**:
  - R12 filters: `app.js:1032`, `index.html:76` (stale-only-toggle)
  - R13 path mode: `app.js:35,353,360,362` (`pathMode`, `pathNodes`, `path-mode-toggle`)
  - R14 NL query: `app.js:425,448` (POST `/graph/query`, state.ask)
  - R16 MCP graph tools: `scripts/wiki_mcp_server.py:14-16,251,270`
  - R17 checkpoint health: `app.js:58` (CHECKPOINT_CLASS_COLORS), `:509-515`
  - R19 `/graph/health`: `wiki-graph-api/main.py:418,434,445`

- **Git state**: branch `feature/cosmograph-renderer` checked out, has uncommitted changes (config.js, index.html, styles.css edits + new cosmos-renderer.js). Main is up to date with origin.

- **Cloudflare cache-bust infra still active**: `?v=__BUILD_ID__` on all asset URLs + module imports, `entrypoint.sh` does `BUILD_ID=$(date +%s)` + sed substitution, nginx emits `CDN-Cache-Control: no-store` + `Cloudflare-CDN-Cache-Control: no-store`. Each rebuild = unique URLs = guaranteed CF MISS.

- **iOS WebGL caveat from cosmos.gl readme**: iOS 15.4+ broke `EXT_float_blend` extension that powers Many-Body force; latest iOS works again. Some Android devices without `OES_texture_float` won't work at all. **The feature flag fallback to canvas renderer is essential for these cases.**
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/cosmos-renderer.js` (CREATED)
   - 6.4KB ES module wrapping `@cosmos.gl/graph` from esm.sh
   - Exports `createCosmosRenderer({container, onPointClick, onBackgroundClick})` returning `{syncData, syncStyle, focusNode, setSelectedNodes, fit, render, raw}`
   - `syncData(nodes, edges)` — builds Float32Array positions (initial circle layout for sim), links (index pairs), and clusters (community ids)
   - `syncStyle({colorOf, sizeOf, dimOf})` — re-applies per-node colors/sizes/alpha when state changes (health mode, dim non-path, etc.)
   - `parseColor()` handles hsl/hex/rgba → [r,g,b,a] floats; `hslToRgb()` helper

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js` (UNMODIFIED in this session — needs the cosmos wiring)
   - 1130 lines, R1-R19 baseline (commit 2acc3ff)
   - Key insertion points listed in technical details above
   - Already has `?v=__BUILD_ID__` cache-bust on imports (lines 7, 11)

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/config.js` (MODIFIED)
   - Added `renderer: "cosmos"` field
   - URL param override: `?renderer=canvas` for instant fallback without rebuild

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/index.html` (MODIFIED)
   - Added `<div id="graph-cosmos" hidden></div>` after `<canvas id="graph"></canvas>` (line ~120)

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/styles.css` (MODIFIED)
   - Added `#graph-cosmos` block (full size, [hidden] support, canvas display:block) after line 141

- `/home/jbl/projects/labs-wiki/plans/graph-ui-visual-pass.md` (CREATED)
   - 4KB fallback design doc
   - Halo+disc+specular treatment; mobile bottom sheet; phased rollout V1-V3
   - References commit `da26467` for reusable glow code
   - Loaded if user rejects Cosmograph

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/entrypoint.sh`
   - Stamps `BUILD_ID=$(date +%s)` into all html/js/css via find+sed
   - Already includes the new files since they live under `/usr/share/nginx/html/`

- `/home/jbl/projects/labs-wiki/reports/full-review-2026-04-21.md`
   - Section 4.3 has R12-R19; **R15 is the only unshipped rec** = Cosmograph or server-side precomputed layout

- `/home/jbl/projects/homelab/compose/compose.wiki-graph.yml`
   - Build context = `${WIKI_INGEST_PATH}` (=`../../labs-wiki`)
   - Always invoke from `compose/` dir with `--env-file ../.env`
   - `docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui`
</important_files>

<next_steps>
Immediate (resume after compaction) — wire `app.js` to use cosmos renderer:

1. **Add to top of `app.js`** (after line 11 imports):
   ```js
   import { createCosmosRenderer } from "./cosmos-renderer.js?v=__BUILD_ID__";
   const urlRenderer = new URLSearchParams(location.search).get("renderer");
   const RENDERER = urlRenderer || cfg.renderer || "canvas";
   let cosmosRenderer = null;
   ```

2. **Hide canvas, mount cosmos** in `loadGraph()` or before `bindUI()` call:
   ```js
   if (RENDERER === "cosmos") {
     document.getElementById("graph").hidden = true;
     const cosmosDiv = document.getElementById("graph-cosmos");
     cosmosDiv.hidden = false;
     cosmosRenderer = createCosmosRenderer({
       container: cosmosDiv,
       onPointClick: (node) => selectNode(node),
       onBackgroundClick: () => clearSelection(),
     });
   }
   ```

3. **Patch `applyFilters()` line 123**:
   ```js
   if (RENDERER === "cosmos" && cosmosRenderer) {
     cosmosRenderer.syncData(state.filtered.nodes, state.filtered.edges);
     draw(); // becomes syncStyle internally
   } else {
     positionNodes(state.filtered.nodes, state.filtered.edges);
     fitViewToNodes(state.filtered.nodes);
   }
   ```

4. **Wrap `draw()` body** at line 609:
   ```js
   function draw() {
     if (RENDERER === "cosmos" && cosmosRenderer) {
       const healthActive = state.health.active;
       const dimNonPath = state.pathMode && state.pathNodes.size > 0;
       const askActive = state.ask.active && state.ask.subgraphIds.size > 0;
       cosmosRenderer.syncStyle({
         colorOf: (n) => healthActive
           ? (CHECKPOINT_CLASS_COLORS[n.checkpoint_class] || CHECKPOINT_DEFAULT_COLOR)
           : colorForCommunity(n.community),
         sizeOf: (n) => Math.max(4, nodeRadius(n) * 1.2),
         dimOf: (n) => {
           const onPath = state.pathNodes.has(n.id);
           const inAskSub = askActive && state.ask.subgraphIds.has(n.id);
           return (dimNonPath && !onPath) || (askActive && !inAskSub);
         },
       });
       return;
     }
     // existing canvas body unchanged
     ctx.clearRect(...);
     ...
   }
   ```

5. **Patch `fitViewToNodes`, `centerNodeInView`, `resize`, `setScale`** to no-op or route to cosmos when `RENDERER === "cosmos"`.

6. **Patch pointer handler binding** (line 770+) to skip when cosmos active.

7. **Build, deploy, verify**:
   ```bash
   cd /home/jbl/projects/homelab/compose && \
   docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui
   ```
   Smoke test: `curl -sI http://172.20.1.25:3000/index.html` shows new BUILD_ID; user hard-refreshes phone, expects organized clusters via cosmos GPU layout.

8. **If smoke test passes**: commit, push `feature/cosmograph-renderer`, open PR, squash-merge, delete branch.

9. **If smoke test fails on mobile**: tell user to append `?renderer=canvas` to URL for instant rollback to R1-R19; load `plans/graph-ui-visual-pass.md` for the next plan.

Open questions / risks:
- esm.sh CDN reachability from user's phone (CF + Cosmograph from a third-party CDN — should work but worth verifying)
- iOS Safari WebGL extension support — fallback to `?renderer=canvas` if broken
- Cosmograph's built-in zoom may conflict with existing `#view-controls` zoom buttons — those buttons should be hidden in cosmos mode or rewired to call cosmos zoom APIs
- Side panel + path mode panel + checkpoint detail panel are independent of renderer — should keep working as-is since `selectNode(node)` is called in both modes
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
