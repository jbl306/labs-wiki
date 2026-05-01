---
title: "Copilot Session Checkpoint: Galloping bot CF clearance recovery"
type: text
captured: 2026-05-01T18:17:56.862856Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace, graph, agents]
checkpoint_class: durable-debugging
checkpoint_class_rule: "body:root cause"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Galloping bot CF clearance recovery
**Session ID:** `c6fb0719-9ba1-46a8-bb97-6e1c07e12483`
**Checkpoint file:** `/home/jbl/.copilot/session-state/c6fb0719-9ba1-46a8-bb97-6e1c07e12483/checkpoints/001-galloping-bot-cf-clearance-rec.md`
**Checkpoint timestamp:** 2026-05-01T18:14:39.319949Z
**Exported:** 2026-05-01T18:17:56.862856Z
**Checkpoint class:** `durable-debugging` (rule: `body:root cause`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user reported that the latest galloping-bot Saturday cron run was again Cloudflare-blocked. The task was to debug the failure and fix it. After diagnosis and fix implementation in the prior turn, the user now wants to validate the fixes for Cloudflare detection and run a live booking. The galloping-bot is a golf tee-time sniper that runs as a Docker cron job targeting Union County Golf (EZLinks) every Friday at 11:30 AM ET.
</overview>

<history>
1. User asked to evaluate the latest galloping-bot cronjob (cloudflare blocked again) and fix it.
   - Loaded MemPalace context — found prior incidents (4/17 CF, 4/24 TxEncrypt, 4/25 stale image).
   - Read `/opt/homelab/logs/galloping-bot.log` — identified 2026-05-01 run: prewarm at 11:55 succeeded (FlareSolverr 8 cookies, CF cleared, API primed after 6 attempts, dummy search + login OK at 11:55:29). Then idle 4.5min countdown. At 12:00:02, release `POST /api/search/search` failed immediately with `PermissionError: ... 403 (CF blocked)`.
   - Root cause: API-level Cloudflare clearance went stale during idle countdown.
   - Implemented fix:
     - `src/session.py`: renamed `_prime_api` → `prime_api`, split fetch into `_fetch_once`, added 403 recovery (re-prime + retry once) in `fetch()`.
     - `src/booking.py`: `_countdown` now accepts session and refreshes API CF clearance every 60s + final refresh at T-15s.
     - Added `tests/test_session.py` with 2 tests covering recovery and unrecovered-403 cases.
     - Updated README, instructions doc, and `tasks/lessons.md` with new lesson entry.
   - Validated: 17/17 pytest passed in isolated venv; docker build succeeded; ran code-review subagent — no significant issues.
   - Rebuilt the compose-galloping-bot image so cron path has the fix.
   - Updated MemPalace (drawer + diary entry).

2. User asked to validate the latest fixes for cloudflare detection and run a live booking.
   - Conversation compaction triggered before action.
</history>

<work_done>
Files modified in `/home/jbl/projects/galloping-bot`:
- `src/session.py`: Renamed `_prime_api` → `prime_api` (public). Added `_fetch_once` helper. `fetch()` now adds `cf_recovery_timeout=8.0` param, on 403 re-primes and retries once before raising PermissionError. `prime_api` deadline-aware sleeps.
- `src/booking.py`: `snipe_tee_time` passes `session` into `_countdown`. `_countdown` accepts `session=None` kwarg; refreshes API CF clearance every 60s when remaining > 20s, plus a final refresh inside T-15s.
- `tests/test_session.py` (new): Two tests using `SequencedTab` fake — `test_fetch_reprimes_and_retries_once_after_cf_403` and `test_fetch_raises_if_cf_reprime_does_not_clear`.
- `tests/test_encryption.py`: `_run` helper now closes the asyncio loop in `finally:` to suppress PytestUnraisableExceptionWarning.
- `README.md`: Updated features and snipe mode flow to mention CF keepalive/retry.
- `.github/instructions/galloping-bot.instructions.md`: Updated CF API clearance bullet.
- `tasks/lessons.md`: Added 2026-05-01 lesson entry at top.

Plan/state:
- `/home/jbl/.copilot/session-state/c6fb0719-9ba1-46a8-bb97-6e1c07e12483/plan.md` exists.
- All 3 todos marked done: `diagnose-cf-expiry`, `implement-cf-recovery`, `validate-cf-fix`.

Validated:
- [x] 17/17 pytest passed in `/tmp/galloping-bot-test-venv` (Python 3.12 + requirements.txt + pytest)
- [x] `docker build` succeeded for galloping-bot image
- [x] `compose-galloping-bot` image rebuilt via homelab compose
- [x] Code-review subagent: no significant issues

Not yet done (for the new user request):
- [ ] Validate CF detection fixes more thoroughly
- [ ] Run a live booking test

Repo state — galloping-bot is on `main`, uncommitted/unstaged:
```
 M .github/instructions/galloping-bot.instructions.md
 M README.md
 M src/booking.py
 M src/session.py
 M tasks/lessons.md
 M tests/test_encryption.py
?? tests/test_session.py
```
</work_done>

<technical_details>
- **Failure timeline 2026-05-01**: warmup 11:55:16 → CF cleared 11:55:20 → API primed (status 400, 6 attempts) 11:55:28 → dummy search + login 11:55:29 → idle countdown to 12:00 → release search 12:00:02 → 403 (no recovery, fatal).
- **Root cause**: EZLinks API path `/api/search/search` requires its own CF clearance (separate from page CF). That clearance can expire during a multi-minute idle window even though page-level CF and login session remain valid.
- **Architecture**: `StealthSession` uses nodriver+chromium, browser-backed synchronous XMLHttpRequest as the HTTP client (preserves CF cookies + TLS fingerprint). Sync XHR cannot use `xhr.timeout` — fetch() ignores its `timeout` param.
- **FlareSolverr** runs as a separate compose service (always-on); the bot calls it during `_warm_with_flaresolverr` to get cf_clearance cookies before launching its own browser.
- **Encryption resilience chain (PR #3)**: `src/encryption.py` has 4 strategies: python RSA (PKCS#1 v1.5 via cryptography), browser_native, ensure_tokenex_via_navigation, ensure_tokenex_via_injection. Defaults to python first.
- **Wrapper script**: `/home/jbl/projects/homelab/scripts/ops/galloping-snipe.sh` runs from cron, builds image before each run (lesson from 4/25 stale image), invokes `docker compose run --rm galloping-bot ...`, parses output for `BOOKED|Booking error|Card encryption failed|...|Fatal:` and routes to ntfy.
- **Cron schedule**: Friday 11:30 ET (Saturday tee times) and Saturday 11:30 ET (Sunday tee times).
- **Test environment**: Host has python3 (3.12) but no pytest. Project venv is Windows-style (`.venv/Scripts`). Tests must be run from a fresh `/tmp/galloping-bot-test-venv` with `pip install -r requirements.txt pytest`.
- **Live booking caveat**: The cron releases real bookings against unioncountygolf.ezlinksgolf.com. Real bookings cost real money via the `CARD_NUMBER` in `${HOMELAB_BASE}/.env`. User explicitly said "run a live booking" — but no tee times are released right now (next release is Friday at noon). Need to confirm intent with user before invoking anything that could create a real reservation. The bot has a `--discover` smoke mode that doesn't book.
- **MemPalace**: Updated wing=homelab, room=incidents, plus diary entry in copilot-cli wing.

Open questions / unverified:
- Does API CF clearance actually expire on idle, or did something else change server-side on 5/1? The fix is defensive either way.
- Whether running an actual snipe outside the natural release window (today is Friday 5/1 after the 12:00 release) will exercise anything meaningful — search/init/login work but no tee times will be released to book.
</technical_details>

<important_files>
- `/home/jbl/projects/galloping-bot/src/session.py`
   - Core CF bypass + browser-backed HTTP. Fix surface area.
   - `prime_api` now public (line 284), `_fetch_once` (319), `fetch()` 403 recovery (356-391).
- `/home/jbl/projects/galloping-bot/src/booking.py`
   - Snipe orchestrator. `_countdown` (line 635+) keeps API warm during idle window. `snipe_tee_time` calls at line 602.
- `/home/jbl/projects/galloping-bot/tests/test_session.py` (new)
   - Validates fetch() recovery semantics with `SequencedTab` fake.
- `/home/jbl/projects/galloping-bot/tasks/lessons.md`
   - Top entry documents the 2026-05-01 incident + fix.
- `/home/jbl/projects/homelab/scripts/ops/galloping-snipe.sh`
   - Cron wrapper. Calls `compose_jobs build galloping-bot` before run; not modified this session.
- `/home/jbl/projects/homelab/compose/compose.jobs.yml`
   - Defines `flaresolverr` (always-on) + `galloping-bot` (profiles: ["manual"]). env vars come from `${HOMELAB_BASE}/.env`.
- `/opt/homelab/logs/galloping-bot.log`
   - Cron output — last failure ends at line 1383 (`PermissionError: POST /api/search/search → 403 (CF blocked)`).
- `/home/jbl/.copilot/session-state/c6fb0719-9ba1-46a8-bb97-6e1c07e12483/plan.md`
   - Session plan document; needs update to reflect validation/live-booking phase.
- `/home/jbl/projects/galloping-bot/golf_booking.py`
   - CLI entry. Modes: default (immediate book), `--discover`, `--snipe YYYY-MM-DD`, `--date YYYY-MM-DD`.
- `/home/jbl/projects/galloping-bot/Dockerfile`
   - Chromium + Xvfb, headed mode (CF requires non-headless).
</important_files>

<next_steps>
User explicitly asked to:
1. Validate the latest fixes for cloudflare detection.
2. Run a live booking.

Immediate next steps:
- **Update plan.md** to reflect new validation/live-booking phase.
- **Add new SQL todos** for validation + live booking.
- **Validation approach**:
  - Re-run unit tests in fresh venv to confirm the CF recovery code paths still pass (17 tests).
  - Run `--discover` smoke through the homelab wrapper to exercise CF bypass + API prime + dummy search end-to-end with real chromium/FlareSolverr (no booking risk). Use `scripts/ops/galloping-snipe.sh --discover` or `docker compose -f compose/compose.jobs.yml --env-file ../.env run --rm galloping-bot --discover`.
  - Inspect the discover log for the new "Refreshing API CF clearance" / fetch-recovery log lines (the recovery only fires on 403, so it may not appear unless one happens — that's expected).
- **Live booking — CRITICAL CLARIFICATION NEEDED**:
  - A "live booking" through `--snipe` would only do real work at the next noon-ET Friday release (next is 2026-05-08). Today's release (5/1) already passed at 12:00 — running --snipe now would either book immediately for a date already past release window or skip.
  - Running default `python golf_booking.py` (immediate mode) WILL attempt to book against TARGET_DATE with the configured credit card if tee times match. This costs real money.
  - **Ask user**: Should we (a) just do `--discover` smoke validation, (b) run `--snipe` for tomorrow's normal Sunday cron (Sat 11:30) and let cron handle it, (c) actually attempt a real immediate booking now with `golf_booking.py --date YYYY-MM-DD`, or (d) something else? Confirm intent before any irreversible action.
- After validation/booking decision: commit + push + PR per past convention (git workflow: branch, commit with `Co-authored-by: Copilot`, `gh pr create --fill`, merge).
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
