---
title: "Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow"
type: source
created: 2026-04-11
last_verified: 2026-04-21
source_hash: "bb401f462b2e63524f82f4333d7d7a4473910a60cefc4b4025c3ece7601e0153"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
quality_score: 90
concepts:
  - book-then-retry-booking-flow-optimization
related:
  - "[[Book-Then-Retry Booking Flow Optimization]]"
  - "[[Galloping-Bot]]"
  - "[[EZLinks API]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, booking, automation, retry-strategy, golf, copilot]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow

## Summary

The user discovered that their golf tee-time sniping bot (galloping-bot) failed to book an Ash Brook GC tee time for 4/26. Investigation revealed the snipe retry loop broke out too early when only Galloping Hill times were available, missing Ash Brook. The fix evolved from a simple retry-before-booking approach to a more optimal book-then-retry strategy that books available courses immediately and retries only for missing ones.

## Key Points

- Root cause identified: retry loop broke early when only one course returned results
- Homelab repo cleaned (reset to 4043d04, crontab restored to original)
- Initial fix committed and pushed to galloping-bot (commit fe16dd2) — but this is now STALE
- Docker image rebuilt on server
- Refactored `_search_and_book` to return `dict[int, int]` (booked_by_course), accept `booked_by_course` param for multi-pass accumulation
- Replaced snipe retry loop with book-then-retry two-pass approach

## Execution Snapshot

**Files updated:**
- `~/projects/galloping-bot/src/booking.py`: Major refactor of snipe flow (IN PROGRESS)

**Work completed:**
- [x] Root cause identified: retry loop broke early when only one course returned results
- [x] Homelab repo cleaned (reset to 4043d04, crontab restored to original)
- [x] Initial fix committed and pushed to galloping-bot (commit fe16dd2) — but this is now STALE
- [x] Docker image rebuilt on server
- [x] Refactored `_search_and_book` to return `dict[int, int]` (booked_by_course), accept `booked_by_course` param for multi-pass accumulation
- [x] Replaced snipe retry loop with book-then-retry two-pass approach
- [ ] Need to update the immediate-mode caller of `_search_and_book` (line ~163) to handle the new return type
- [ ] Need to update `.env` GALLOPING_SNIPE_RETRIES from 5 to 1
- [ ] Need to validate syntax, push, and rebuild

**Current state:**
- `booking.py` has been edited with both changes but NOT yet validated or committed
- The immediate-mode `book_tee_time()` function (around line 163) still calls `_search_and_book` with old `await` pattern (no return capture) — needs a minor update to add `booked = ` and the Done log line
- The old `logger.info("Done —...")` line was inside `_search_and_book` but was removed — it's now in the snipe function but needs to be added to the immediate-mode path too

## Technical Details

- **Booking system**: EZLinks API at `unioncountygolf.ezlinksgolf.com`. Single search endpoint returns tee times for multiple courses. Bot filters by course ID, time window, access type (Player Card 14day).
- **Course IDs**: 4549 = Galloping Hill GC, 4545 = Ash Brook GC. Order in COURSE_IDS determines booking priority.
- **MAX_BOOKINGS=1** applies per course (not total). So with 2 courses, bot books up to 2 total (1 each).
- **SNIPE_RETRIES in .env is currently 5** — user wants it set to 1.
- **SNIPE_DELAY_SECONDS=2** in .env — used both for initial post-release delay and as the retry wait.
- **Release timing**: `calculate_release_time()` uses `play_date - 15 days` at noon for 14-day cards. The cron schedule (Fri for Sat, Sat for Sun) and +15 day offset in `galloping-snipe.sh` are CORRECT — do not change them.
- **`_search_and_book` refactor**: Now returns `dict[int, int]` (course_id → booking count). Accepts optional `booked_by_course` to accumulate across passes. Filters out courses already at their cap.
- **Python deps (nodriver, etc.) only exist in Docker** — `import` validation outside container will fail on session/browser modules. Use `py_compile` or `ast.parse` for syntax checks.
- **Galloping-bot repo**: `~/projects/galloping-bot/`, separate from homelab. Docker build context is `${GALLOPING_BOT_PATH:-../../galloping-bot}` relative to compose dir.
- **Homelab repo is clean** at commit 4043d04 on main. No pending changes there.
- **Crontab is correct**: `30 11 * * 5` (Fri) for Saturday times, `30 11 * * 6` (Sat) for Sunday times.

## Important Files

- `~/projects/galloping-bot/src/booking.py`
- Core booking orchestrator — contains `snipe_tee_time()`, `_search_and_book()`, `filter_tee_times()`, `book_tee_time()` (immediate mode)
- ACTIVELY BEING EDITED — `_search_and_book` refactored (returns dict, accepts booked_by_course), snipe loop replaced with two-pass
- `_search_and_book`: ~line 303-402 (refactored)
- `snipe_tee_time`: ~line 460+ (two-pass logic replaces old retry loop around line 538+)
- `book_tee_time` (immediate mode): ~line 108-171 — needs `Done` log line added after `_search_and_book` call at ~163

- `~/projects/galloping-bot/src/config.py`
- Config loading — SNIPE_RETRIES from env var `SNIPE_RETRIES` (line 120), default "5"
- Per-course time windows for Ash Brook (lines 81-92)

- `~/projects/galloping-bot/src/api_client.py`
- EZLinks API client — `search_tee_times()` takes course_ids list, returns SearchResult

- `~/projects/galloping-bot/src/models.py`
- Data models: TeeTime, SearchResult, BookingResult, etc.

- `~/projects/homelab/compose/compose.jobs.yml`
- Docker compose for galloping-bot — env var passthrough, no changes needed

- `~/projects/homelab/scripts/ops/galloping-snipe.sh`
- Cron helper — calculates target date (+15 days), launches container. CORRECT, no changes needed.

- `~/projects/homelab/.env`
- Contains GALLOPING_SNIPE_RETRIES=5 — needs to change to 1

## Next Steps

**Remaining work:**
1. Fix immediate-mode caller in `book_tee_time()` (~line 163) — capture return value, add "Done" log line
2. Validate syntax with `python3 -c "import ast; ast.parse(...)"`
3. Update `~/projects/homelab/.env`: set `GALLOPING_SNIPE_RETRIES=1`
4. Commit the booking.py changes in galloping-bot repo
5. Push galloping-bot to GitHub
6. Rebuild Docker image: `docker compose -f compose/compose.jobs.yml --env-file .env build --no-cache galloping-bot`
7. Verify the image built successfully

**Immediate next action:**
- View line ~163 of booking.py to fix the immediate-mode `_search_and_book` call (add return capture + Done log), then validate and deploy

## Related Wiki Pages

- [[Book-Then-Retry Booking Flow Optimization]]
- [[Galloping-Bot]]
- [[EZLinks API]]
- [[Durable Copilot Session Checkpoint]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-11 |
| URL | N/A |
