---
title: "Copilot Session Checkpoint: Knightcrawler TorBox Backend"
type: text
captured: 2026-05-18T16:06:43.690574Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace, agents, dashboard]
checkpoint_class: durable-debugging
checkpoint_class_rule: "body:root cause"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Knightcrawler TorBox Backend
**Session ID:** `616a8ca3-45dd-43c8-aa77-7af1035c637a`
**Checkpoint file:** `/home/jbl/.copilot/session-state/616a8ca3-45dd-43c8-aa77-7af1035c637a/checkpoints/001-knightcrawler-torbox-backend.md`
**Checkpoint timestamp:** 2026-05-18T15:55:55.874226Z
**Exported:** 2026-05-18T16:06:43.690574Z
**Checkpoint class:** `durable-debugging` (rule: `body:root cause`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user wanted the homelab Knightcrawler plan `knightcrawler-torbox-and-recent-scrape-reliability.md` implemented, deployed, validated, committed, and later pushed to GitHub `main`. The first implementation added TorBox backend/provider support and recent scrape reliability, but the user then reported a production UI bug: Knightcrawler’s configure UI has no TorBox dropdown/API-key field like Real-Debrid. The current active task is to debug that UI/config-provider registration issue, fix it, deploy, validate, commit, and push to GitHub `main`.
</overview>

<history>
1. The user asked to implement the homelab plan `knightcrawler-torbox-and-recent-scrape-reliability.md`.
   - Loaded required workflow skills: `task-observer`, `homelab-deploy`, `executing-plans`, `subagent-driven-development`, `using-git-worktrees`.
   - Created worktree `/home/jbl/projects/homelab/.worktrees/knightcrawler-torbox-reliability` on branch `feat/knightcrawler-torbox-reliability`.
   - Implemented TorBox env/config surface, provider runtime patch, recent importer refactor, durable scrape state, run tracking, targeted Redis invalidation, Homepage metrics, docs, tests, and setup state directory.
   - Deployed `stremio` and `web` stacks. Initial web deploy failed because worktree-relative sibling paths did not find `Spatial-Design-Studio`; fixed for deployment by temporary symlinks, then redeployed from canonical main.
   - Validated TorBox backend behavior and recent scrape metrics.
   - Committed `58e812c fix: add knightcrawler torbox reliability` and fast-forwarded homelab `main`.

2. Validation and deployment results from first implementation.
   - `pytest tests/knightcrawler -q` passed.
   - Python/Bash/Node syntax checks passed.
   - Compose config rendered with real `/home/jbl/projects/homelab/.env`.
   - Live addon contained TorBox marker: `shortName:"TB"` count 1.
   - Caddy access route: unauth `http://torrentio.${DOMAIN}/manifest.json` returned `404`; gated route with `${KC_ACCESS_TOKEN}` returned `200`.
   - TorBox stream lookup on an existing movie with files returned 14 streams.
   - TorBox resolve returned HTTP `302` with Location present.
   - Homepage metrics endpoint in `homepage-db-stats` returned structured recent scrape fields: `scrape_year_cutoff=2025`, `scrape_sources=torrentio`, `processed=1`, `no_streams=1`, `errors=0`.
   - `KC_LEGAL_TEST_IMDB_ID` was a 2026 `tvSeries` but had no `imdb_metadata_episodes`, so live playback validation used an existing movie with files instead.

3. The user then reported there is no TorBox dropdown/API-key field on the Knightcrawler UI.
   - Started a new debugging task with `task-observer`, `systematic-debugging`, and `homelab-deploy`.
   - Checked homelab git: on `main`, HEAD `58e812c`, origin/main still at `46af0ab`, so previous implementation has not yet been pushed.
   - Queried MemPalace for prior Knightcrawler/TorBox context.
   - Need to investigate root cause before making another fix.
</history>

<work_done>
Files changed and committed in `58e812c`:
- `.env.example`
  - Added `TORBOX_API_TOKEN`, `KC_LEGAL_TEST_IMDB_ID`, `KC_RECENT_YEAR_START`, `KC_RECENT_BATCH_SIZE`, `KC_RECENT_SOURCES`, `KC_RECENT_STATE_DIR`.
- `compose/compose.stremio.yml`
  - Injected `TORBOX_API_TOKEN` only into `knightcrawler-addon`.
- `config/knightcrawler/stack.env`
  - Set debrid collector disabled and removed stale RD collector assumptions.
- `scripts/knightcrawler/patches/patch-torbox-provider.js`
  - New runtime patch inserting TorBox provider into minified Knightcrawler addon bundle.
  - Current patch registers provider in runtime `ct` provider map but apparently did not expose it in the configure UI dropdown.
- `scripts/knightcrawler/provider-src/torbox.js`
  - Source-of-truth TorBox provider implementation.
- `scripts/knightcrawler/patches/apply-all.sh`
  - Runs `patch-torbox-provider.js` after existing addon patches.
- `scripts/knightcrawler/automation/kc_stream_sources.py`
  - New source adapter utilities for Torrentio parsing, sizing, seeders, dedupe.
- `scripts/knightcrawler/automation/kc_import_recent.py`
  - New multi-source importer.
- `scripts/knightcrawler/automation/kc-import-recent.py`
  - Kebab-case wrapper.
- `scripts/knightcrawler/automation/kc-import-torrentio.py`
  - Compatibility wrapper around new importer.
- `scripts/knightcrawler/automation/kc-scrape-recent.sh`
  - Durable cursor under `${KC_RECENT_STATE_DIR:-/opt/homelab/state/knightcrawler}`.
  - Defaults to 2025+ rolling window.
  - Adds `--sources`.
  - Applies migration `kc-scrape-status.sql`.
  - Records `automation_scrape_recent_runs`.
  - Targets partial series coverage.
  - Invalidates Redis keys matching `knightcrawler-addon|stream:${imdb_id}*`.
- `scripts/knightcrawler/sql/kc-scrape-status.sql`
  - Creates `automation_scrape_recent_runs`.
- `homepage-db-stats/app.py`
  - Adds recent scrape run/source/window/partial-series metrics.
- `config/homepage/services.yaml`
  - Updates KnightCrawler Automation widget labels to recent coverage/outcome counts.
- `scripts/ops/setup.sh`
  - Creates recent scrape state directory.
- `README.md`
  - Updates Knightcrawler service description.
- `docs/09-knightcrawler-guide.md`
  - Documents TorBox provider, verification commands, recent scrape behavior, run health commands.
- `tests/knightcrawler/test_recent_import.py`
  - Tests parser/dedupe.
- `tests/knightcrawler/test_torbox_provider_patch.py`
  - Tests patch markers and no embedded secrets.

Current state:
- Homelab `main` includes commit `58e812c`.
- `origin/main` is behind (`46af0ab`), user explicitly requested push to GitHub main after the UI fix.
- Stremio and web stacks are deployed from canonical `/home/jbl/projects/homelab` main.
- Current active issue: configure UI does not show TorBox dropdown/API-key field.
</work_done>

<technical_details>
- Knightcrawler addon image is `gabisonfire/knightcrawler-addon:2.0.28`; runtime bundle path is `/app/dist/index.cjs`.
- Existing patch strategy modifies `/app/dist/index.cjs` at container startup via `scripts/knightcrawler/patches/apply-all.sh`.
- Actual minified provider map in `index.cjs` looked like:
  - `var Dy0=2*60*1e3,jy0=15,UOe=[],ct={realdebrid:{...},premiumize:{...},alldebrid:{...},debridlink:{...},offcloud:{...},putio:{...}},VOe={};`
- `patch-torbox-provider.js` inserts a `homelabTorbox` module before that anchor and adds `torbox:{key:"torbox",instance:homelabTorbox,name:"TorBox",shortName:"TB",catalog:!1}` to `ct`.
- Backend stream/resolve works after patch, proving provider map integration is enough for runtime route behavior.
- UI dropdown likely depends on a separate configure-page schema/list, not just the runtime `ct` provider map. Need to inspect `index.cjs` configure UI strings/schema around `realdebrid`, `premiumize`, dropdown HTML/JS, or config builder.
- Do not print `TORBOX_API_TOKEN` or generated tokenized URLs. Prior validation sanitized token output and removed temp files.
- `KC_LEGAL_TEST_IMDB_ID` exists in DB as `tvSeries|2026`, but has no `imdb_metadata_episodes`; this affects validation if using series route.
- Redis cache key separator is confirmed literal pipe: `knightcrawler-addon|stream:tt...`, not colon.
- `.env.example` has mixed line endings in repo; avoid full-file line-ending churn. Previous fix restored original line endings and only inserted env vars.
- There were pre-existing CRLF-only dirty files in old worktree (`PROGRESS.md`, `compose/compose.runtime-test.yml`), but canonical main was clean after merge.
- Homelab deploy quirks:
  - `./scripts/ops/deploy.sh stremio web` deploys both stacks.
  - Worktree deploy can fail for sibling project relative paths; canonical main deploy works.
  - `homepage-db-stats` port 8001 may not be host-published; verify from inside container with `docker exec homepage-db-stats python -c ...`.
- Need to push after final commit: `git push origin main`.
</technical_details>

<important_files>
- `scripts/knightcrawler/patches/patch-torbox-provider.js`
  - Most important file for current UI bug.
  - Currently registers TorBox in runtime provider map and resolve/cache functions.
  - Needs investigation to also patch configure UI/dropdown/provider input schema.
- `scripts/knightcrawler/patches/apply-all.sh`
  - Applies patches on addon startup; ensure any new UI patch runs here or is included in TorBox provider patch.
- `compose/compose.stremio.yml`
  - Defines `knightcrawler-addon`, env injection, patch mount, Caddy access gating.
- `docs/09-knightcrawler-guide.md`
  - Documents TorBox usage and verification; may need update if UI dropdown route changes config instructions.
- `tests/knightcrawler/test_torbox_provider_patch.py`
  - Existing tests only check provider markers; should be extended to assert UI/dropdown/config markers for TorBox.
- `/tmp/kc-index.cjs` or fresh copied bundle from running addon
  - Use `docker cp knightcrawler-addon:/app/dist/index.cjs /tmp/kc-index.cjs` for investigation.
  - Search for configure UI/schema strings and compare working providers.
- `scripts/knightcrawler/provider-src/torbox.js`
  - Source reference for provider behavior; less likely relevant to UI dropdown.
- `README.md`, `.env.example`, `config/knightcrawler/stack.env`
  - Already updated for first implementation; probably no changes needed unless UI behavior changes docs/env.
</important_files>

<next_steps>
Immediate task:
1. Investigate root cause of missing TorBox dropdown.
   - Copy live addon bundle: `docker cp knightcrawler-addon:/app/dist/index.cjs /tmp/kc-index.cjs`.
   - Search for configure UI/provider schema strings:
     - `rg "realdebrid|premiumize|alldebrid|putio|configure|config|select|Moch|debrid" /tmp/kc-index.cjs`
     - Use Python snippets to inspect context around provider names and dropdown-related HTML/JS.
   - Compare what was patched (`ct` runtime provider map) against what UI uses.

2. Add failing/covering test.
   - Extend `tests/knightcrawler/test_torbox_provider_patch.py` to assert patch includes markers for configure UI/dropdown, not only runtime provider.
   - If feasible, add a smoke test that runs patch on copied bundle and verifies TorBox appears in the patched configure HTML/schema.

3. Fix root cause.
   - Update `scripts/knightcrawler/patches/patch-torbox-provider.js` to deterministically patch the configure UI/schema wherever existing provider dropdown/list is defined.
   - Keep patch idempotent for minified bundle.
   - Avoid logging or embedding secrets.

4. Validate locally.
   - `pytest tests/knightcrawler -q`
   - `node --check scripts/knightcrawler/patches/patch-torbox-provider.js`
   - Smoke patch on copied bundle and grep for TorBox UI marker.
   - Run compose render with real env.

5. Deploy and validate.
   - `./scripts/ops/deploy.sh stremio`
   - Verify live addon marker in `/app/dist/index.cjs`.
   - Fetch configure UI through gated route and confirm TorBox option/API key field appears. Use sanitized output; do not print token.
   - Recheck stream/resolve still work.
   - Recheck access gating: unauth 404, auth 200.

6. Commit and push.
   - Commit on `main` after validation, likely message: `fix: show torbox in knightcrawler configure ui`.
   - `git push origin main`.
   - Final response should mention commit SHAs and validation results.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
