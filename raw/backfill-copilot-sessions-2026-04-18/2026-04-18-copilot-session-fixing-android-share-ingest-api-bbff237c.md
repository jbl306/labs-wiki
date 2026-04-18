---
title: "Copilot Session Checkpoint: Fixing Android share ingest API"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Fixing Android share ingest API
**Session ID:** `7ccd0122-adc4-4b81-b65b-098fa0804cde`
**Checkpoint file:** `/home/jbl/.copilot/session-state/7ccd0122-adc4-4b81-b65b-098fa0804cde/checkpoints/001-fixing-android-share-ingest-ap.md`
**Checkpoint timestamp:** 2026-04-07T23:04:45.145464Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user reported a 422 Unprocessable Entity error when sharing URLs from Android (HTTP Shortcuts app) to the labs-wiki ingest API. The debugging process involved multiple iterations: adding a form endpoint, then a universal parsing endpoint, adding debug logging, and discovering that HTTP Shortcuts' `sendHttpRequest()` sends empty bodies. The server-side fixes (universal body parsing, auto-type-detection) are deployed and working. The docs were ultimately reverted to the original scripting shortcut approach after the user realized they had been tapping the wrong share button.
</overview>

<history>
1. User reported 422 error from HTTP Shortcuts Android share to wiki-ingest-api
   - Error: `{"detail":[{"type":"missing","loc":["body"],"msg":"Field required","input":null}]}`
   - Root cause identified: `/api/ingest` expects JSON Pydantic body (`IngestRequest`), but HTTP Shortcuts wasn't sending valid JSON
   - Added `/api/ingest/form` endpoint accepting form-encoded data
   - Committed, pushed, rebuilt and redeployed container
   - Updated docs in `capture-sources.md` to reference form endpoint

2. User reported same 422 error persisted with the form endpoint
   - Both JSON and form-encoded bodies arrived as `null` from `sendHttpRequest()`
   - Replaced both endpoints with a single universal handler that parses: query params → JSON → form → raw body fallback
   - Both `/api/ingest` and `/api/ingest/form` now route to the same universal handler
   - Rebuilt, redeployed, tested all 5 formats successfully
   - Updated docs to use query params approach

3. User reported 400 error: `"type must be: url, text, or note"`
   - This confirmed body parsing was now working (past 422), but `type` field was empty
   - Added `/api/debug` endpoint to dump raw requests
   - Added comprehensive request logging (`INGEST DEBUG`) to the `_parse_ingest_params` function
   - Rebuilt and redeployed

4. User shared from Android to debug endpoint
   - Logs revealed: `POST /api/debug?type=text&content=&title=&source=android-share` — the script was executing but `shared_text` variable was empty
   - User mentioned they had added "JSON encode" option to the variable
   - Advised to disable JSON encode; user got "tried to set variable of value that doesn't exist" error

5. Researched HTTP Shortcuts scripting API
   - Fetched official docs from http-shortcuts.rmy.ch/scripting
   - `getVariable()` raises error if variable doesn't exist; shared text access through global variables requires exact key match
   - Proposed simplifying to Regular Shortcut with `text/plain` body and `{shared_text}` placeholder
   - Added auto-type-detection in `_do_ingest()` (URL vs text from content)
   - Rewrote docs for Regular Shortcut approach
   - Committed, pushed, rebuilt, redeployed

6. User asked to revert docs to scripting — was clicking wrong share button the whole time
   - Restored docs from commit `ac13076` (original scripting shortcut version)
   - Committed and pushed
   - Server-side improvements (universal parsing, auto-type-detection, debug logging) remain deployed
</history>

<work_done>
Files updated:
- `wiki-ingest-api/app.py`: Major refactor — universal ingest handler, debug endpoint, auto-type-detection, request logging
- `wiki-ingest-api/README.md`: Updated endpoint table (added `/api/ingest/form`)
- `docs/capture-sources.md`: Reverted to original scripting shortcut docs (net: no change from original)

Commits pushed to main (chronological):
- `ac13076` feat(api): add /api/ingest/form endpoint
- `c0a0d8f` docs: update Android share to use /api/ingest/form
- `ef7d062` fix(api): universal ingest endpoint — handles any body format
- `c866964` docs: use query params for HTTP Shortcuts script
- `f871ed5` fix(api): auto-detect type, simplify Android share
- `a14b255` docs: revert Android share docs back to scripting shortcut

Current deployed state:
- wiki-ingest-api container is running with all server-side improvements
- `/api/ingest` and `/api/ingest/form` both use universal parser
- `/api/debug` endpoint exists for request inspection (no auth needed)
- Auto-type-detection active (type field now optional)
- Debug logging active on all ingest requests
- Docs are back to original scripting shortcut approach
</work_done>

<technical_details>
- **HTTP Shortcuts `sendHttpRequest()` body behavior**: Both JSON and form-encoded bodies arrive as completely empty (`body_len=0`). This is a known quirk of the scripting API. The built-in Regular Shortcut HTTP client may behave differently.
- **Universal parser priority**: query params → JSON body → form-encoded body → raw body fallback (auto-detects URL vs text)
- **Auto-type-detection**: If `type` field is omitted, server checks if content starts with `http://` or `https://` → "url", else → "text"
- **Homelab deployment**: `docker compose --env-file ../.env` is required when running from `compose/` dir. The `.env` lives at `/home/jbl/projects/homelab/.env`, not in `compose/`.
- **Compose structure**: `compose.wiki.yml` is included from `docker-compose.yml` via `include:`. Services: `wiki-ingest-api` (FastAPI on port 8000) and `wiki-auto-ingest` (file watcher sidecar).
- **Caddy proxy**: wiki-ingest-api is proxied at `wiki-ingest.jbl-lab.com` through Cloudflare → Caddy. Requests from Caddy arrive from `172.20.1.2`.
- **Auto-ingest side effect**: Test files written to `raw/` get auto-processed by the wiki-auto-ingest sidecar within seconds, creating wiki pages. Must clean up both `raw/` test files AND any generated `wiki/` pages.
- **The actual user issue**: User was clicking the wrong share button in Android, not the HTTP Shortcuts share target. The scripting shortcut with `sendHttpRequest()` + JSON body works fine when properly triggered.
- **Debug endpoint** (`/api/debug`): Still deployed, returns full request dump (method, URL, query params, headers, body). No auth required. Useful for future debugging.
- **IngestRequest Pydantic model**: Still defined in app.py but no longer used by any endpoint (universal handler reads raw Request). Could be cleaned up.
</technical_details>

<important_files>
- `wiki-ingest-api/app.py`
   - Core API server — all ingest endpoints
   - Major changes: universal `_parse_ingest_params()` (lines ~148-232), `_do_ingest()` with auto-type-detection (lines ~235-260), debug endpoint `/api/debug` (lines ~135-147), combined route handler for `/api/ingest` and `/api/ingest/form` (lines ~262-290)
   - Has verbose `INGEST DEBUG` logging on every ingest request

- `docs/capture-sources.md`
   - User-facing docs for all capture channels (CLI, browser, iOS, Android, GitHub Issues, ntfy, direct API)
   - Android section (line ~132) documents Scripting Shortcut with `sendHttpRequest()` + JSON body
   - Currently restored to original version from `ac13076`

- `wiki-ingest-api/README.md`
   - API endpoint reference
   - Updated to include `/api/ingest/form` endpoint in table

- `/home/jbl/projects/homelab/compose/compose.wiki.yml`
   - Docker compose for wiki services (not in labs-wiki repo)
   - References `${WIKI_INGEST_PATH}` from homelab `.env`
   - Two services: `wiki-ingest-api`, `wiki-auto-ingest`
</important_files>

<next_steps>
No pending tasks — user's issue was resolved (wrong share button). All server improvements are deployed and working.

Potential cleanup if desired:
- Remove `/api/debug` endpoint and verbose `INGEST DEBUG` logging once Android share is confirmed working
- Remove unused `IngestRequest` Pydantic model from app.py (no longer referenced by any endpoint)
- The `docs/capture-sources.md` still references `YOUR_API_URL` and `YOUR_TOKEN` placeholders in the Android section — could mention the actual URL `wiki-ingest.jbl-lab.com`
- Update `tasks/lessons.md` with the HTTP Shortcuts debugging lesson
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
