---
title: "Copilot Session Checkpoint: Sharper shader, adaptive labels, wiki popup"
type: text
captured: 2026-04-22T13:27:57.872553Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: failed
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sharper shader, adaptive labels, wiki popup
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/008-sharper-shader-adaptive-labels.md`
**Checkpoint timestamp:** 2026-04-22T13:25:52.044709Z
**Exported:** 2026-04-22T13:27:57.872553Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User wants three improvements to the labs-wiki WebGL graph UI: (1) sharper, higher-contrast nodes optimized for mobile (currently look out of focus), (2) adaptive node titles that show/hide based on zoom and density in clusters, and (3) clickable nodes that pop up the full wiki page contents in a mobile-friendly way. Approach: tighten the GLSL shader for crisp 3-band lighting, add an HTML overlay for adaptive labels driven by camera transform events, add a server endpoint for raw markdown bodies, and render markdown into the existing side panel with wikilink-aware in-graph navigation.
</overview>

<history>
1. User requested mobile sharpness, adaptive labels, and click-to-popup wiki contents.
   - Created 7 todos in SQL (shader-sharpen, renderer-transform-events, label-overlay, api-page-endpoint, wiki-popup, deploy-validate, ship)
   - Inspected `webgl-renderer.js` (658 lines), `app.js` (~1262 lines), `index.html`, `styles.css`, and `wiki-graph-api/main.py` route table
   - Confirmed node schema includes `path` (e.g. `concepts/aaak-compression-dialect.md`) — relative to `WIKI_PATH`
   - Implemented all three features:
     - **API**: added `GET /graph/page/{node_id:path}` that resolves WIKI_PATH/node.path with traversal guard and returns body+metadata
     - **Shader**: replaced fragment shader with 3-band lighting (crisp coreMask via `smoothstep(0.30, 0.42, d)`, mid-band, halo, anti-aliased rim, specular highlight at upper-left, premultiplied alpha output)
     - **Renderer transform API**: added `getCamera()` returning `{x, y, scale, viewW, viewH, worldToScreen, screenToWorld}`, `onTransform(cb)` subscriber set, `getNodes()`, and `notifyTransform()` call at end of every draw
     - **Label overlay**: new file `labels-overlay.js` — absolutely-positioned `<button class="webgl-label">` elements with greedy collision avoidance (spatial buckets), zoom-scaled budget (20–220 visible), pinned set always rendered, click delegated to `onLabelClick`
     - **Markdown renderer**: new file `markdown.js` — minimal safe HTML escape + headings/lists/code/blockquotes/links/wikilinks, frontmatter strip, fenced code preserved via placeholders
     - **app.js wiring**: imported `renderMarkdown`, added `gpuLabels` state, init label overlay with click-to-select, fed `setNodes`/`setPinned`/`layout` from `syncData`/`syncGpuStyle`, expanded `showNodePanel` to fetch `/graph/page/{id}` and render into new `#node-content` div with wikilink click interception
     - **HTML**: added `<div id="node-content" class="node-content">` between summary and neighbors
     - **CSS**: appended ~130 lines for `.webgl-label` (.pinned, hover, mobile sizes) and `.node-content` (typography, code blocks, blockquotes, wikilinks, mobile sheet scroll)
   - Was about to rebuild containers and run Playwright validation when compaction triggered
</history>

<work_done>
Files modified:
- `wiki-graph-api/main.py` — new `/graph/page/{node_id:path}` endpoint right after `/graph/nodes` (path-traversal guarded with `target.relative_to(wiki_root)`)
- `wiki-graph-ui/webgl-renderer.js` — new fragment shader (3-band: core/mid/halo + rim + specular), new transform observer system (`onTransform`, `getCamera`, `getNodes`), `notifyTransform()` at end of draw, `transformObservers.clear()` in destroy
- `wiki-graph-ui/app.js` — imports `renderMarkdown` from `./markdown.js`, added `gpuLabels` global, label overlay init in `initWebgl` (click → `selectNode`/`handlePathClick`, subscribed to transform), `syncData` block now feeds labels and triggers layout, `syncGpuStyle` calls `gpuLabels.setPinned(sel)` and `layout()`, `showNodePanel` fetches `/graph/page/{id}` → `renderMarkdown` → injects into `#node-content`, intercepts `.wikilink` clicks to navigate within graph by matching title/id/slug
- `wiki-graph-ui/index.html` — added `<div id="node-content" class="node-content"></div>` between `<p id="node-summary">` and `<h3>Neighbors</h3>`
- `wiki-graph-ui/styles.css` — appended ~130 lines: `.webgl-label`/`.pinned`/`.hidden` + mobile sizes; `.node-content` typography (h1-h4, p, ul/ol, code, pre, blockquote, a.wikilink, hr) + mobile scroll override

Files created:
- `wiki-graph-ui/labels-overlay.js` — `createLabelOverlay({container, renderer})` returns `{setNodes, setPinned, setOnLabelClick, layout, destroy}`. Spatial-bucket O(N) collision check, importance = degree + pinned-bonus + tier-core-bonus
- `wiki-graph-ui/markdown.js` — `renderMarkdown(src)` → safe HTML; supports headings, **bold**, *italic*, `code`, fenced ```code```, lists, blockquotes, links, `[[wikilinks]]`, frontmatter strip

Work completed:
- [x] shader-sharpen
- [x] renderer-transform-events
- [x] label-overlay
- [x] api-page-endpoint
- [x] wiki-popup
- [ ] deploy-validate (NEXT — rebuild + Playwright)
- [ ] ship (commit, PR, merge)
</work_done>

<technical_details>
- **Shader change** in `webgl-renderer.js` `POINT_FS`: was `core = pow(fall, 4.0)` + `halo = pow(fall, 1.5) * 0.55` (too soft). Now: `coreMask = 1 - smoothstep(0.30, 0.42, d)` (crisp inner disc), `midMask`, `halo = pow(1-d, 2.6) * 0.32`, `rim = smoothstep(0.90, 0.98, d) * (1 - smoothstep(0.98, 1.0, d))`, plus specular `pow(max(0, 1 - len(uv - vec2(-0.28, -0.32)) * 1.55), 5.0) * 0.9 * coreMask`. Mixes `hot = mix(base*1.55, white, 0.30)` for the bright tinted core.

- **Transform observer pattern**: renderer maintains `transformObservers = new Set()`, calls them after every draw. Wraps each cb in try/catch. Returns unsubscribe function. Critical: the camera object passed to observers exposes `worldToScreen` and `screenToWorld` closures — overlays don't need to recompute matrices.

- **Label collision algorithm**: greedy by importance (degree + pinned-bonus 1e9 + core-tier +5). For each candidate compute screen pos, build label rect (x = sx - w/2, y = sy + nodeRadius*0.55 + 4), bucket-test against claimed rects (BUCKET=96px), claim if free. Pinned labels skip the budget cap. Budget = `28 * (zoom/0.5)^0.85`, clamped 20..220.

- **Off-screen culling** in label layout: skip nodes with `sx < -120 || sx > W + 120 || sy < -40 || sy > H + 40` (label might extend past node center).

- **DOM perf**: labels use `transform: translate3d(x,y,0)` (GPU-composited), `contain: strict` on container, `pointer-events: none` on layer + `auto` on labels. Backdrop-filter blur(2px) for legibility over glow.

- **API path resolution**: `(WIKI_PATH / node.path).resolve()` then `target.relative_to(WIKI_PATH.resolve())` — raises ValueError on traversal. Returns 404 if `node.get("path")` is empty (some nodes might not have files), 400 on invalid path, 500 on read errors.

- **Markdown safety**: every line passes through `escapeHTML` BEFORE inline regex transforms run. Wikilink regex `\[\[([^\]|]+)(?:\|([^\]]+))?\]\]` runs on already-escaped text so `data-target` is safe. Link href validated `^(https?://|/|#|mailto:)` — anything else becomes `#`. Code blocks pulled out FIRST (before line processing) using `\u0000CODEBLOCK{n}\u0000` placeholders so their content isn't mangled by inline regex.

- **Wikilink in-graph navigation**: `showNodePanel` matches `data-target` against `state.graph.nodes` by title, id, `endsWith("/" + target + ".md")`, or slugified `target.toLowerCase().replace(/\s+/g, "-")`. If a candidate exists and is in `state.filtered.nodes`, calls `selectNode(local)`.

- **Mobile node-panel**: existing `#node-panel` has `max-height: min(48dvh, 380px)` on phones. New CSS overrides with `min(70dvh, 600px)` + `overflow-y: auto` + `-webkit-overflow-scrolling: touch` so the markdown body is scrollable.

- **Label budget gotcha**: when all 737 nodes are visible at fit-zoom (~0.4), budget computes to ~22. As user zooms in (scale → 4), budget → ~140. Tested formula in head; may need tuning if too sparse at default zoom.

- **Untested**: container rebuild, Playwright headless probe, mobile touch on labels, wikilink resolution against actual wiki content.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/webgl-renderer.js`
  - Custom WebGL2 renderer (now ~720 lines). Sharpened shader + transform observer API.
  - Key sections: `POINT_FS` shader (lines ~103-150), `transformObservers` set + `onTransform`/`getCamera`/`notifyTransform` (around lines 248-280), `notifyTransform()` call at end of `draw()`, public API export now includes `getCamera, onTransform, getNodes`

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/labels-overlay.js` (NEW)
  - Adaptive HTML label overlay. Module exports `createLabelOverlay({container, renderer})`.
  - Returns `{setNodes, setPinned, setOnLabelClick, layout, destroy}`. `layout(cam)` is called from renderer's `onTransform`.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/markdown.js` (NEW)
  - Safe markdown→HTML for the wiki popup. Exports `renderMarkdown(src)`. Supports wikilinks `[[Page]]` as `<a class="wikilink" data-target="...">` for in-graph navigation.

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js`
  - Wiring: import `renderMarkdown` (line ~16), `gpuLabels` global (line ~34), `initWebgl` adds label overlay block (~lines 102-135), `syncData` feeds labels (~line 254-266), `syncGpuStyle` pins selection set + triggers layout (~lines 165-180), `showNodePanel` fetches `/graph/page/` and renders into `#node-content` (~lines 1045-1095)

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/index.html`
  - Added `<div id="node-content" class="node-content"></div>` inside `#node-panel` between summary and neighbors (line ~104)

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/styles.css`
  - Appended ~130 lines at EOF: `.webgl-label` (+ `.pinned`, `.hidden`, mobile media query), `.node-content` (typography for h1-h4/p/ul/ol/code/pre/blockquote/a.wikilink/hr + mobile scroll override)

- `/home/jbl/projects/labs-wiki/wiki-graph-api/main.py`
  - New `/graph/page/{node_id:path}` endpoint just after `/graph/nodes` (line ~208). Path-traversal guarded.

- `/home/jbl/projects/homelab/compose/compose.wiki-graph.yml`
  - Build context = `${WIKI_INGEST_PATH}` (= `../../labs-wiki`). Always invoke from `compose/` dir with `--env-file ../.env`.

- `/tmp/validate_webgl.py`
  - Existing Playwright validation script. Probes for canvas, webgl2 context, samples center pixels, takes screenshot at `/tmp/wiki-graph-webgl.png`. Uses `wait_until="domcontentloaded"` (NOT `networkidle` — SSE keeps connection open). Knows the false-negative pattern: `brightCenterPx: 0` may just mean canvas center is sparse; visual inspection of screenshot is authoritative.

- `/tmp/pwenv/bin/python` — Playwright venv with chromium 145 installed
</important_files>

<next_steps>
Immediate (resume here):

1. **Rebuild + deploy container**:
   ```bash
   cd /home/jbl/projects/homelab/compose && \
     docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui wiki-graph-api
   ```
   Both services need rebuilding (api got new endpoint, ui got new files).

2. **Quick syntax check before deploy** (recommended):
   ```bash
   cd /home/jbl/projects/labs-wiki && \
     node --check wiki-graph-ui/webgl-renderer.js && \
     node --check wiki-graph-ui/labels-overlay.js && \
     node --check wiki-graph-ui/markdown.js && \
     node --check wiki-graph-ui/app.js
   ```

3. **Validate**:
   - Run `/tmp/pwenv/bin/python /tmp/validate_webgl.py` (existing script); inspect `/tmp/wiki-graph-webgl.png`
   - Probe new endpoint: `curl -s 'http://172.20.1.25:3000/api/graph/page/concepts%2Faaak-compression-dialect.md' | head -50` (or via container)
   - Probe label overlay: extend validator to `document.querySelectorAll('#webgl-labels .webgl-label:not(.hidden)').length` — expect 20+
   - Take a mobile-sized screenshot too (viewport 414×900) and inspect

4. **Likely issues to check**:
   - Label overlay css `contain: strict` may clip labels; verify visible
   - `gpuLabels.layout(cam)` might be called before `setNodes()` if transform fires first — already guarded by `if (!cam || !nodes.length) return`
   - Wikilink slug matching may miss many cases — acceptable for v1
   - `GET /graph/page/` for `id` containing `/` — FastAPI handles via `:path` converter; encoding done via `encodeURIComponent` may need `encodeURI` instead since slashes get encoded. Check: `encodeURIComponent("concepts/foo.md")` = `"concepts%2Ffoo.md"` — FastAPI `:path` will receive this as-is and pass it; should still match `state.nodes_by_id["concepts/foo.md"]` after URL decode. **Verify with curl**.

5. **Commit + PR + merge**:
   ```bash
   cd /home/jbl/projects/labs-wiki && \
     git checkout -b feature/sharper-labels-popup && \
     git add wiki-graph-ui/ wiki-graph-api/main.py && \
     git commit -m "feat(graph-ui): sharp 3-band shader, adaptive labels, wiki popup
   
   - Shader: crisp coreMask + specular for high-contrast mobile rendering
   - New labels-overlay.js: adaptive HTML labels with greedy collision avoidance
   - New markdown.js: safe md→HTML with wikilink in-graph navigation
   - New /graph/page/{id} endpoint serves wiki body for the side panel
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" && \
     git push -u origin feature/sharper-labels-popup && \
     gh pr create ... && gh pr merge --squash --delete-branch
   ```

6. **Update SQL todos**: mark deploy-validate and ship as done.

7. **MemPalace drawer** for `labs_wiki` wing: note new endpoint + label overlay + popup architecture.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
