---
title: "Copilot Session Checkpoint: Fixing Android Share Ingest API"
type: source
created: 2026-04-07
last_verified: 2026-04-21
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 90
concepts:
  - universal-ingest-endpoint-for-flexible-api-request-parsing
  - http-shortcuts-android-app-scripting-api-quirks
  - auto-type-detection-in-api-ingest-requests
related:
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[HTTP Shortcuts Android App Scripting API Quirks]]"
  - "[[Auto-Type-Detection in API Ingest Requests]]"
  - "[[HTTP Shortcuts]]"
  - "[[Labs-Wiki Ingest API]]"
  - "[[Homelab]]"
  - "[[Labs-Wiki]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, Server-Side, Android, API, Debugging, HTTP Shortcuts, Ingest]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Fixing Android Share Ingest API

## Summary

The user reported a 422 Unprocessable Entity error when sharing URLs from Android (HTTP Shortcuts app) to the labs-wiki ingest API. The debugging process involved multiple iterations: adding a form endpoint, then a universal parsing endpoint, adding debug logging, and discovering that HTTP Shortcuts' `sendHttpRequest()` sends empty bodies. The server-side fixes (universal body parsing, auto-type-detection) are deployed and working. The docs were ultimately reverted to the original scripting shortcut approach after the user realized they had been tapping the wrong share button.

## Key Points

- Added `/api/ingest/form` endpoint accepting form-encoded data
- Committed, pushed, rebuilt and redeployed container
- Rebuilt, redeployed, tested all 5 formats successfully
- Added `/api/debug` endpoint to dump raw requests
- Added comprehensive request logging (`INGEST DEBUG`) to the `_parse_ingest_params` function
- User mentioned they had added "JSON encode" option to the variable

## Execution Snapshot

**Files updated:**
- `wiki-ingest-api/app.py`: Major refactor — universal ingest handler, debug endpoint, auto-type-detection, request logging
- `wiki-ingest-api/README.md`: Updated endpoint table (added `/api/ingest/form`)
- `docs/capture-sources.md`: Reverted to original scripting shortcut docs (net: no change from original)

**Commits pushed to main (chronological):**
- `ac13076` feat(api): add /api/ingest/form endpoint
- `c0a0d8f` docs: update Android share to use /api/ingest/form
- `ef7d062` fix(api): universal ingest endpoint — handles any body format
- `c866964` docs: use query params for HTTP Shortcuts script
- `f871ed5` fix(api): auto-detect type, simplify Android share
- `a14b255` docs: revert Android share docs back to scripting shortcut

**Current deployed state:**
- wiki-ingest-api container is running with all server-side improvements
- `/api/ingest` and `/api/ingest/form` both use universal parser
- `/api/debug` endpoint exists for request inspection (no auth needed)
- Auto-type-detection active (type field now optional)
- Debug logging active on all ingest requests
- Docs are back to original scripting shortcut approach

## Technical Details

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

## Important Files

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

## Next Steps

No pending tasks — user's issue was resolved (wrong share button). All server improvements are deployed and working.

**Potential cleanup if desired:**
- Remove `/api/debug` endpoint and verbose `INGEST DEBUG` logging once Android share is confirmed working
- Remove unused `IngestRequest` Pydantic model from app.py (no longer referenced by any endpoint)
- The `docs/capture-sources.md` still references `YOUR_API_URL` and `YOUR_TOKEN` placeholders in the Android section — could mention the actual URL `wiki-ingest.jbl-lab.com`
- Update `tasks/lessons.md` with the HTTP Shortcuts debugging lesson

## Related Wiki Pages

- [[Universal Ingest Endpoint for Flexible API Request Parsing]]
- [[HTTP Shortcuts Android App Scripting API Quirks]]
- [[Auto-Type-Detection in API Ingest Requests]]
- [[HTTP Shortcuts]]
- [[Labs-Wiki Ingest API]]
- [[Homelab]]
- [[Labs-Wiki]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-07 |
| URL | N/A |
