---
title: "Copilot Session Checkpoint: Custom WebGL renderer with glow shader"
type: text
captured: 2026-04-22T13:07:32.239400Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: failed
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Custom WebGL renderer with glow shader
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/007-custom-webgl-renderer-with-glo.md`
**Checkpoint timestamp:** 2026-04-22T13:04:33.444085Z
**Exported:** 2026-04-22T13:07:32.239400Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User wants the labs-wiki graph UI to render with rich glowing nodes that don't drift off-screen. After cosmos.gl iterations failed (nodes flew off bottom-left, drab colors), pivoted to a custom WebGL2 renderer that consumes the server's already-precomputed x/y layout and uses a glow shader. User requested validation post-deploy without forcing them to iterate.
</overview>

<history>
1. User: "nodes still falling off bottom-left, colors not rendering well, use custom WebGL, validate yourself after deploy"
   - Discovered API at `127.0.0.1:8765/graph/export/json` returns 737 nodes / 1998 edges with **server-precomputed x/y in [-1000, 1000]** for every node — no JS sim needed
   - Hypothesis: cosmos.gl 2.6.4 silently ignored my flat `simulationGravity`/`simulationCenter` config (likely needs `simulation: {...}` nesting in v2), so only its cluster force ran → drift
   - Decided to drop cosmos.gl entirely, write custom WebGL2 renderer using server x/y directly
   - Created `wiki-graph-ui/webgl-renderer.js` (custom WebGL2, ~580 lines) with glow shader (premultiplied alpha, bright core + soft halo, additive bloom on overlap), pan/zoom/pinch/click hit-test via spatial bins, ResizeObserver, auto-fit
   - Removed `cosmos-renderer.js`
   - Renamed app.js symbols `USE_COSMOS→USE_WEBGL`, `cosmos→gpuRenderer`, `syncCosmosStyle→syncGpuStyle`, `initCosmos→initWebgl` via sed
   - Updated `config.js` default to `renderer: "webgl"`; URL override now `?renderer=canvas`
   - Bumped node `sizeOf` range to 8..46 for richer halo bloom
   - Built + deployed container successfully (`app.js?v=...`)
   - Was setting up Playwright in venv `/tmp/pwenv` for headless validation when compaction triggered
</history>

<work_done>
Files created:
- `wiki-graph-ui/webgl-renderer.js` — full custom WebGL2 renderer with glow shader

Files deleted:
- `wiki-graph-ui/cosmos-renderer.js`

Files modified:
- `wiki-graph-ui/app.js` — header comment, `RENDERER` const accepts `"canvas"|"webgl"`, renamed all cosmos symbols, replaced `initCosmos`/`syncCosmosStyle` bodies with webgl equivalents, increased sizeOf range to 8..46
- `wiki-graph-ui/config.js` — default `renderer: "webgl"`

Work completed:
- [x] Custom WebGL2 renderer authored & syntax-validated (`node --check` clean)
- [x] App.js fully rewired off cosmos
- [x] Container rebuilt + deployed (Cloudflare cache-bust infra still in place)
- [x] Playwright + chromium installed in `/tmp/pwenv`
- [ ] Headless validation script written + run
- [ ] Screenshot capture for visual verification
- [ ] Commit, push, PR, merge to main
</work_done>

<technical_details>
- **Server already does the layout**: `/graph/export/json` returns node fields `id, title, page_type, tier, quality_score, tags, path, summary, last_verified, checkpoint_class, retention_mode, community, degree, content_hash, x, y` with x/y in [-1000, 1000] for ALL 737 nodes. Layout is computed by `wiki-graph-api/main.py`. **This makes JS simulation completely unnecessary** — the cosmos drift problem was self-inflicted by running a sim on top of a layout.

- **Why cosmos.gl failed**: Likely v2 config option restructure — `simulationGravity`, `simulationCenter`, etc. may need to be nested under `simulation: {...}` in v2.x (unverified). Either way, custom path is cleaner.

- **Glow shader technique** (in `webgl-renderer.js`):
  - WebGL2 context with `premultipliedAlpha: true, antialias: true`
  - Blend mode: `gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)` (premultiplied)
  - Fragment shader: `core = pow(fall, 4.0)`, `halo = pow(fall, 1.5) * 0.55`, output `vec4(col * a, a)` so overlapping halos additively brighten → bloom effect
  - Selection ring: thin annulus at d∈[0.78, 0.98] in PointCoord space
  - `gl_PointSize = size * dpr` for crisp rendering on retina/mobile

- **Camera/matrix**: 3x3 column-major view matrix, `sx = 2*scale/viewW`, `sy = -2*scale/viewH` (flip y for screen coords). `worldToScreen` and `screenToWorld` helpers handle picking.

- **Click hit-test**: spatial bins (BIN=64 world units), search ±span cells covering 24px-equivalent radius around cursor.

- **Pointer handling**: pointerdown/move/up + pinch (2-pointer pinchStartDist), wheel zoom anchored at cursor (re-anchor trick: get world coord at cursor before+after scale change, translate by delta).

- **VAO setup**: separate VAOs for points (5 attribs: pos, color, size, alpha, selected) and lines (pos, color). Buffers re-created in `syncData`, re-bound in `bindVAOs()`.

- **DOM host**: still uses `<div id="graph-cosmos">` in index.html (didn't rename — internal id, works fine; webgl renderer creates its own canvas inside it).

- **Cache-bust infra**: `?v=__BUILD_ID__` placeholders in app.js + html, sed-replaced by `entrypoint.sh` at container start with `BUILD_ID=$(date +%s)`. Combined with nginx `CDN-Cache-Control: no-store`, every deploy = fresh URLs at Cloudflare.

- **API endpoint**: container exposes `127.0.0.1:8765` → API port 8000. Public is `https://graph-api.jbl-lab.com`.

- **Container build**:
  ```
  cd /home/jbl/projects/homelab/compose && \
  docker compose -f compose.wiki-graph.yml --env-file ../.env up -d --build wiki-graph-ui
  ```

- **Validation approach**: Playwright in venv `/tmp/pwenv` with chromium 145. Plan: navigate to `http://172.20.1.25:3000/`, wait for `loadGraph()` complete (connection-state="connected"), check no console errors, verify `gpuRenderer` initialized, capture screenshot.

- **R1-R19 features still preserved**: filters, BFS path mode, NL ask, checkpoint health, side panel, /graph/health — all renderer-agnostic. selectNode/clearSelection/handlePathClick called from webgl renderer's onPointClick/onBackgroundClick.

- **iOS WebGL2 support**: WebGL2 requires iOS 15+ (released 2021). Should be fine for any modern phone. Fallback `?renderer=canvas` preserved for very old devices.

- **Untested**: Visual quality — hasn't been screenshotted yet. Performance at 737 nodes (should be trivial on GPU). Touch interactions on actual mobile.

- **Branch state**: Working tree has uncommitted changes. Currently on main (PR #25 merged). Need new branch for this work.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/webgl-renderer.js` (NEW, ~580 lines)
  - Custom WebGL2 renderer with glow shader
  - Exports `createWebglRenderer({container, onPointClick, onBackgroundClick})` returning `{syncData, syncStyle, focusNode, setSelectedNodes, fit, render, destroy}`
  - Uses server x/y directly, zero simulation
  - Premultiplied alpha + power-curve falloff = bloom on overlap
  - Spatial-bin hit-test for clicks
  - Self-contained pan/zoom/pinch/wheel handlers + ResizeObserver

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js` (MODIFIED)
  - Lines 1-33: header + `RENDERER`/`USE_WEBGL`/`gpuRenderer` constants
  - Lines 85-155: `initWebgl()` and `syncGpuStyle()` (replaced cosmos versions)
  - Line 88: still queries `#graph-cosmos` (host div, kept the id)
  - Sweep done via sed renaming all `USE_COSMOS→USE_WEBGL`, `cosmos.→gpuRenderer.`, etc.
  - sizeOf range bumped to 8..46 in `syncGpuStyle` for richer halos

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/config.js` (MODIFIED)
  - `renderer: "webgl"` default

- `/home/jbl/projects/labs-wiki/wiki-graph-ui/index.html` + `styles.css` (UNCHANGED)
  - Still uses `<div id="graph-cosmos" hidden>` host — webgl renderer creates canvas inside

- `/home/jbl/projects/labs-wiki/wiki-graph-api/main.py`
  - Computes server-side layout (FR), ships x/y via `/graph/export/json`
  - Range [-1000, 1000]; this is the source of truth for positions

- `/home/jbl/projects/homelab/compose/compose.wiki-graph.yml`
  - Build context = `${WIKI_INGEST_PATH}` (=`../../labs-wiki`)
  - Always invoke from `compose/` dir with `--env-file ../.env`

- `/tmp/pwenv/` — Playwright venv with chromium installed; ready for validation script
</important_files>

<next_steps>
Immediate (resume here after compaction):

1. **Write + run Playwright validation script**:
   ```python
   # /tmp/validate_wiki.py
   from playwright.sync_api import sync_playwright
   import sys
   with sync_playwright() as p:
       browser = p.chromium.launch()
       ctx = browser.new_context(viewport={"width":1280,"height":900}, device_scale_factor=2)
       page = ctx.new_page()
       errors = []
       page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
       page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
       page.goto("http://172.20.1.25:3000/", wait_until="networkidle", timeout=30000)
       page.wait_for_function("document.getElementById('connection-state').textContent === 'connected'", timeout=15000)
       page.wait_for_timeout(2000)  # let renderer settle
       state = page.evaluate("""() => ({
         hasGpu: !!window.gpuRenderer,
         canvasHidden: document.getElementById('graph').style.display === 'none',
         hostVisible: !document.getElementById('graph-cosmos').hidden,
         hasWebGL2: !!document.querySelector('#graph-cosmos canvas')?.getContext('webgl2'),
       })""")
       page.screenshot(path="/tmp/wiki-webgl.png", full_page=False)
       print("STATE:", state)
       print("ERRORS:", errors)
       sys.exit(0 if not errors else 1)
   ```
   Run with `/tmp/pwenv/bin/python /tmp/validate_wiki.py`

2. **Inspect screenshot** at `/tmp/wiki-webgl.png` (use `view` tool — it returns image base64).

3. **Fix any issues found** (likely candidates: `gpuRenderer` not exposed on window so use a different probe like `document.querySelector('#graph-cosmos canvas')`; possible shader compile errors visible in console).

4. **Commit, push, PR, merge**:
   ```bash
   cd /home/jbl/projects/labs-wiki && git checkout -b feature/custom-webgl-renderer
   git add wiki-graph-ui/
   git commit -m "feat(graph-ui): custom WebGL2 renderer with glow shader, drop cosmos.gl
   
   - Uses server-precomputed x/y from /graph/export/json — no JS sim, no drift
   - Premultiplied-alpha glow shader (core+halo) for bloom on overlap
   - Larger size range (8..46) so hubs read as bright blooms
   - Self-owned pan/zoom/pinch/click; spatial-bin hit-test
   - Falls back to ?renderer=canvas
   
   Replaces cosmos.gl integration from PR #24/#25 which drifted nodes off-screen.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   git push -u origin feature/custom-webgl-renderer
   gh pr create ... && gh pr merge --squash --delete-branch
   ```

5. **Update MemPalace** drawer for `labs_wiki` wing noting renderer is now custom WebGL2, not cosmos.gl.

Open question: Should `gpuRenderer` be exposed on `window` for easier debugging? Currently it's a module-scope `let` — Playwright probe needs to use DOM-based detection instead (`document.querySelector('#graph-cosmos canvas')` and check `getContext('webgl2')`).
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
