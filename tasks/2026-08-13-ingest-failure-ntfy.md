# Detailed auto-ingest failure notifications and pending-source processing

## Goal

Send an ntfy alert with actionable error details whenever automatic source processing fails, then deploy the updated watcher and process the current pending raw files.

## Tasks

1. Add regression coverage for agent-backend failures, transactional failures, and unexpected pending-loop exceptions.
2. Implement bounded/redacted failure-detail formatting and notification calls without changing successful-ingest behavior.
3. Run focused and broader tests, rebuild/recreate `wiki-auto-ingest`, and verify its auth mount and health.
4. Process all currently pending top-level `raw/*.md` sources and verify raw status, generated pages, logs, and runtime output.

## Safety / side effects

- Live side effects requested by the user: rebuild/recreate `wiki-auto-ingest`, execute pending ingests, and send normal success/failure ntfy messages.
- Do not modify or restart unrelated services.
- Preserve the existing dirty Labs-Wiki worktree and commit only through the ingest pipeline's manifest-scoped behavior.

## Results

- Added detailed failure notifications for agent-result failures, transactional publish failures, malformed raw sources, watcher parse/classification/processing exceptions, pending discovery/processing exceptions, and direct single-file CLI exceptions. Unexpected pre-agent exceptions leave sources pending for retry; handled deterministic proposal/publish failures already return `False` and also preserve pending status.
- Failure bodies include source/backend/error context, retain both the beginning and final transport error when truncated, cap payloads at 3,500 UTF-8 bytes, redact Authorization, GitHub/OpenAI, generic token/secret/password/session, cookie, URL-userinfo/query, and AWS access-key forms, and remain suppressed for validation runs.
- Added regression tests for agent failure notification, pending-discovery, watcher-classification, direct-CLI exceptions, and validation-run suppression, strict structured-output schema compatibility, redaction, and UTF-8 payload bounds.
- Fixed two runtime blockers exposed during deployment: normalized non-root read access for image-owned prompts/templates, and made `valid_from` required-nullable for Codex/OpenAI strict JSON Schema.
- Rebuilt/recreated only `wiki-auto-ingest`; final container is healthy and uses image `sha256:129ccd4e490edbb86505079470d07e3a899f435387b5ddc332af1a91bd6b404b`. Failed sources remain pending so corrected transient/runtime failures can retry on restart or modification.
- Startup processed both pending sources successfully; both now have `status: ingested`, and top-level pending count is zero. The arXiv survey produced a source page, two new concept pages (`Memory Substrates in Foundation Agents`, `Memory Operations in Foundation Agents`), and an update to `Agent Memory Frameworks`; the earlier Cloudflare source produced its source page and three MCP concept pages.
- Full container test suite: 51 passed, 1 skipped (graph API runtime-only test dependency gate).
- The generated source/concept pages pass the shared page schema, the Labs-Wiki MCP can read the new arXiv source page, and the source commits are `c7e242a` (arXiv) and `9559b74` (Cloudflare).
- Compose validation and `git diff --check` passed. Live ntfy POSTs returned HTTP 200 for observed failures and both successful ingests.
