---
title: "Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox"
type: text
captured: 2026-05-28T19:49:46.835213Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:integration"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Swapping Real-Debrid for Comet+TorBox
**Session ID:** `fdc9646b-f502-4a0b-9333-5c8edd4ac947`
**Checkpoint file:** `/home/jbl/.copilot/session-state/fdc9646b-f502-4a0b-9333-5c8edd4ac947/checkpoints/001-swapping-real-debrid-for-comet.md`
**Checkpoint timestamp:** 2026-05-28T19:40:12.193043Z
**Exported:** 2026-05-28T19:49:46.835213Z
**Checkpoint class:** `durable-architecture` (rule: `body:integration`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user wants to update the `debrid-downloader-web` Nuxt app (at `/home/jbl/projects/debrid-downloader-web`) to use their self-hosted **Comet** Stremio addon (configured with the homelab **TorBox** API key) instead of **Real-Debrid**. After clarification, the chosen approach is the **Comet resolver**: query Comet (TorBox-configured) for ready-to-download URLs and drop the entire RD `addMagnet → selectFiles → poll → unrestrict` pipeline. The work is being done in autopilot mode following an approved plan in `/home/jbl/.copilot/session-state/fdc9646b-f502-4a0b-9333-5c8edd4ac947/plan.md`.
</overview>

<history>
1. The user requested: "update debrid downloader to use my self hosted comet with torbox api key in homelab .env instead of real debrid."
   - Ran MemPalace session protocol (`mempalace_status`, searched homelab wing) — found Comet is already deployed and documented.
   - Explored the codebase: only `debrid-downloader-web/` exists (no separate `debrid-downloader/`). Mapped the full RD pipeline across `server/utils/real-debrid.ts`, `server/api/downloads/index.post.ts`, `server/api/downloads/[id]/status.get.ts`, torrent source utils (`torrentio.ts`, `stremthru.ts`, `mediafusion.ts`, `torrent-parsers.ts`).
   - Found `homelab/.env` already has `TORBOX_API_TOKEN=45189240-fe4a-486b-a5b4-934411b961ea` and Comet is deployed in `homelab/compose/compose.stremio.yml` with `SCRAPE_TORBOX: live`, `TORBOX_API_KEY: ${TORBOX_API_TOKEN}`. The web app's `compose/compose.web.yml` already lists `comet=https://comet.${DOMAIN}` as a torrent source, but the app still uses RD.

2. Asked the user to choose between two integration approaches (Comet resolver vs. TorBox direct API).
   - User selected: **Comet resolver** — query self-hosted Comet for ready URLs, drop the RD pipeline entirely.

3. Researched Comet's API against the live instance (we are running ON the beelink-gti13 homelab server, hostname confirmed).
   - Studied `g0ldyy/comet` source on GitHub (config_validation.py, models.py, stream.py).
   - Discovered Comet's API is token-gated because `CONFIGURE_PAGE_PASSWORD` is set → `STREMIO_API_PREFIX = /s/<PUBLIC_API_TOKEN>`. Token retrieved via `docker exec comet cat /app/data/public_api_token.txt` = `Npt64q4VxSpMqy1he2dh1Z85-iztk-r86bqN5DPxwiw`.
   - Verified live: stream endpoint returns streams with resolved playback URLs; a playback URL 302-redirects to TorBox CDN (`https://nexus-087.enam.tb-cdn.io/dld/...?token=...`).

4. Wrote plan.md, presented via exit_plan_mode → user approved with **autopilot** mode.

5. Began implementation (in progress when compaction occurred): created episode-matching util, comet util, updated types, rewrote search endpoint, rewrote downloads POST endpoint.
</history>

<work_done>
Files created:
- `server/utils/episode-matching.ts`: Moved `parseEpisodesFromFilename` and `parseEpisodeFromFilename` (plus `RANGE_RE`, `EPISODE_PATTERNS`, `inferSeasonFromPath`) out of the deleted real-debrid.ts.
- `server/utils/comet.ts`: New Comet client with `getCometSettings()`, `buildCometConfig()`, `cometStreamUrl()`, `chooseStream()`, `cometSearch()`, and `parseCometStreams()` (private). Parses cached flag (`⚡`), quality, size, seeders, info_hash (from `/playback/<hash>/` path), and resolved `url`.

Files deleted:
- `server/utils/real-debrid.ts` (RD client removed)
- `server/api/torrents/search.get.ts` (then recreated with Comet)
- `server/api/downloads/index.post.ts` (then recreated with Comet)
- `server/api/downloads/[id]/status.get.ts` (deleted, NOT yet recreated — THIS IS PENDING)

Files modified:
- `app/types/index.ts`: Added `url?` and `cached?` to `TorrentResult`; made `magnet`/`rd_torrent_id` optional + added `info_hash?` on `DownloadTask`; rewrote `DownloadRequest` with `url?/filename?/size?/info_hash?/cached?`; replaced RD entry in `API_KEY_CONFIGS` with `TORBOX_API_TOKEN` + `COMET_URL` + `COMET_API_TOKEN` entries.
- `server/api/torrents/search.get.ts`: Recreated — queries Comet only via `cometSearch()`.
- `server/api/downloads/index.post.ts`: Recreated — movie/single-episode uses client-passed resolved URL (or re-resolves via Comet); multi-episode re-queries Comet per episode preferring same release; cached→`ready`, uncached→`debrid`. Stores info_hash as `magnet:?xt=urn:btih:<hash>`.

Todo status (SQL session db): done = comet-util, episode-util, types, search-api; in_progress = downloads-post; pending = status-api, settings-api, frontend, docs, homelab, verify.
</work_done>

<technical_details>
- **Comet stream URL format**: `https://comet.jbl-lab.com/s/<TOKEN>/<b64config>/stream/{movie|series}/{imdbId[:s:e]}.json`. `b64config` = `base64(JSON {"debridService":"torbox","debridApiKey":"<TORBOX key>"})` (legacy fields accepted; minimal config proven to work).
- **Comet stream response**: each stream has `name` (e.g. `[TB⚡] Comet 2160p`; ⚡=cached, ⬇️=uncached), `description` (📄filename / 💾size / 👤seeders), `behaviorHints.{filename, videoSize}`, and `url` = playback proxy. Debrid streams have NO `infoHash` field (hash is in the url path `/playback/<40-hex-hash>/...`). Torrent (P2P) streams DO have `infoHash` — these must be skipped (filter on url containing `/playback/`).
- **Playback URL = download link**: hitting the playback URL 302-redirects to the TorBox CDN. No polling/unrestricting needed for cached content.
- **Token gating**: `STREMIO_API_PREFIX=/s/<PUBLIC_API_TOKEN>` because `CONFIGURE_PAGE_PASSWORD` is set. Plan is to pin `PUBLIC_API_TOKEN` in homelab compose via new `COMET_PUBLIC_API_TOKEN=Npt64q4VxSpMqy1he2dh1Z85-iztk-r86bqN5DPxwiw` env var (preserving current value so existing Stremio installs keep working).
- **Settings storage**: `server/utils/supabase.ts` wraps `local-store.ts` (SQLite, active backend via `DEBRID_DB_PATH`). `SENSITIVE_KEYS` set in supabase.ts (line ~52) gates encryption/masking — must add `TORBOX_API_TOKEN`, `COMET_API_TOKEN` and remove/keep `RD_API_TOKEN`. Helpers: `getUserSetting`, `getUserSettings`, `setUserSetting`, `getAllSettingsForUI` (all auto-imported by Nitro).
- **DB schema** (`local-store.ts`): `download_tasks` table has `magnet TEXT NOT NULL`, `rd_torrent_id`, no `info_hash` column. Decision: store info_hash inside `magnet` as a magnet URI (no schema change needed). `mapDownloadTask` (line ~112) maps rows; `createDownloadTask` (line ~161); `updateDownloadTask` (line ~206) supports status/rd_torrent_id/magnet/quality/download_urls/error.
- **Config approach**: env-first (`NUXT_COMET_URL`, `NUXT_COMET_API_TOKEN`, `TORBOX_API_TOKEN`), then user-settings fallback (`COMET_URL`, `COMET_API_TOKEN`, `TORBOX_API_TOKEN`).
- **Reused parsers** from `torrent-parsers.ts`: `parseQuality`, `parseSizeBytes` (matches `💾 X GB`), `parseSeeders` (matches `👤 N`), `QUALITY_RANK`.
- **`rtk` tool**: A workspace CLI wrapper — `rtk ls/read/grep/curl/sql/find/docker` work; plain `cat`/`ssh` from this env need care. `ssh beelink-gti13` failed (publickey) but we're already on the server, so `docker exec` works directly.
- **JSON parsing gotcha**: Comet responses contain newlines in descriptions; parse with care (use file save + `json.load`, not inline strict parsing).
</technical_details>

<important_files>
- `server/utils/comet.ts`
   - Core new Comet client. Exports `getCometSettings`, `buildCometConfig`, `cometStreamUrl`, `chooseStream`, `cometSearch`.
   - `chooseStream(streams, preferInfoHash?, preferQuality?)` prefers matching info_hash → cached+quality → first cached → first.
   - `cometSearch` uses 60s timeout; filters by quality; sorts cached-first.
- `server/api/downloads/index.post.ts`
   - Recreated. Handles movie/single/multi-episode. Stores `magnet:?xt=urn:btih:<info_hash>`.
- `server/api/downloads/[id]/status.get.ts`
   - **DELETED, NOT YET RECREATED** — this is the immediate next task. Must re-query Comet for `debrid` (uncached) tasks (parse info_hash from stored magnet, use task season/episode) and flip to `ready` once cached. Drop all RD imports. For non-`debrid` terminal/ready tasks, return as-is.
- `app/types/index.ts`
   - Type contracts updated (TorrentResult, DownloadRequest, DownloadTask, API_KEY_CONFIGS).
- `server/utils/local-store.ts`
   - SQLite backend; schema and task CRUD. No changes needed (info_hash stored via magnet).
- `server/api/user.get.ts`
   - Still references `rdGetUser` + `RD_API_TOKEN` — WILL BREAK BUILD, needs updating (remove RD or point at Comet/TorBox; likely simplest to return minimal info or remove RD dependency).
- `app/stores/settingsStore.ts`, `app/components/OnboardingWizard.vue`, `app/components/SettingsPanel.vue`, `app/components/DownloadCard.vue`, `app/stores/downloadStore.ts`, `app/pages/media/[type]/[id].vue`
   - Frontend files needing RD→Comet/TorBox copy changes and download-trigger contract update (send `url/filename/size/info_hash/cached/quality`).
- `homelab/compose/compose.web.yml` (debrid-downloader-web service ~line 31), `homelab/compose/compose.stremio.yml` (comet ~line 51), `homelab/.env`
   - Need env updates: replace `NUXT_TORRENTIO_SOURCES` with `NUXT_COMET_URL`/`NUXT_COMET_API_TOKEN`/`TORBOX_API_TOKEN`; pin `PUBLIC_API_TOKEN: ${COMET_PUBLIC_API_TOKEN}` on comet; add `COMET_PUBLIC_API_TOKEN=` to .env.
- `/home/jbl/.copilot/session-state/fdc9646b-f502-4a0b-9333-5c8edd4ac947/plan.md`
   - The approved plan with full detail.
</important_files>

<next_steps>
Immediate next step (was in progress):
1. **Recreate `server/api/downloads/[id]/status.get.ts`** — remove RD; for `debrid` tasks parse info_hash from stored `magnet`, re-query Comet via `cometSearch` (using task.season/episode for TV), use `chooseStream` to find the matching hash; if now cached, update download_urls + status `ready`; else return as-is. For ready/done/error/cancelled, return as-is. Note: `getCometSettings` needed.

Remaining tasks (todo ids):
- `settings-api`: Update `server/api/settings/index.put.ts` ALLOWED_KEYS (replace `RD_API_TOKEN` with `TORBOX_API_TOKEN`, add `COMET_URL`, `COMET_API_TOKEN`). Update `SENSITIVE_KEYS` in supabase.ts. Surface env-provided config in settings GET so onboarding doesn't nag when configured via env. Update `server/api/user.get.ts` (remove RD dependency).
- `frontend`: Update `settingsStore.ts` (isSetupComplete/requiredKeysMissing/keyStatus → TORBOX_API_TOKEN + COMET_URL instead of RD); `media/[type]/[id].vue` `startDownload` to send `url/filename/size/info_hash/cached/quality` (multi-ep sends episodes[] + chosen info_hash); `TorrentPicker.vue` (key rows by url, show ⚡ cached badge); `OnboardingWizard.vue`, `SettingsPanel.vue`, `DownloadCard.vue`, `downloadStore.ts` (RD→Comet/TorBox copy; timeout message wording).
- `docs`: Update `.env.example` and `README.md` (RD→Comet/TorBox).
- `homelab`: Update `compose/compose.web.yml`, `compose/compose.stremio.yml`, `.env` as noted.
- `verify`: Add `tests/smoke/comet.spec.ts` parsing test; update existing `tests/smoke/download-card.collapsible.spec.ts` if it references RD; run `npm run build` + `npm test`; live-check a movie + episode Comet query.

Also: `nuxt.config.ts` app.head meta description mentions "Real-Debrid" (~line 18) — update copy. Update `mempalace_diary_write` at session end.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
