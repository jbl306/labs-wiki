---
title: "Copilot Session Checkpoint: Direct Sportsbook Sources"
type: text
captured: 2026-04-25T16:51:38.391130Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:integration"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Direct Sportsbook Sources
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/006-direct-sportsbook-sources.md`
**Checkpoint timestamp:** 2026-04-25T16:49:08.439234Z
**Exported:** 2026-04-25T16:51:38.391130Z
**Checkpoint class:** `durable-architecture` (rule: `body:integration`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is hardening NBA ML prop-line accuracy after discovering a serious Josh Hart steals mismatch: DraftKings UI reportedly showed `2+`, while the dashboard showed `SGO_DK 0.5`. The work shifted from documenting the SGO contamination issue to discovering direct FanDuel/DraftKings prop sources, documenting an integration plan, and testing browser-backed access paths for both books.
</overview>

<history>
1. Earlier context before this compaction segment: the user asked to audit the Josh Hart steals mismatch and create a fix report.
   - Live `/api/props`, production `prop_lines`, `prop_line_snapshots`, and `mv_prop_lines_primary` all showed Josh Hart `SGO_DK stl=0.5` and `SGO_FD stl=1.5` for 2026-04-25.
   - Raw SportsGameOdds showed the SGO DK O/U row was internally suspicious: consensus and FanDuel were `1.5`, but DraftKings `byBookmaker.overUnder` was `0.5`, and DK `-226/+168` prices matched a separate yes/no market.
   - Created and pushed `reports/2026-04-25-prop-line-integrity-audit.md`.
   - Commit pushed to `main`: `83bff35 docs: audit prop line integrity issue`.

2. The user then asked: “discover how we can directly get the props from fd/dk. we have flaresolverr for cloudflare challenges if needed.”
   - Invoked `data-researcher` and launched two background researcher agents for DraftKings and FanDuel.
   - Queried MemPalace and found prior context: The Odds API is already integrated but limited by quota; SGO has known alternate-line/market contamination.
   - Research findings:
     - The Odds API already returns bookmaker-specific DK/FD props through a production-safe API, but current account quota was exhausted.
     - DraftKings old web JSON candidate endpoints use `/sites/{SITE}/api/v5/eventgroups/42648?format=json`.
     - FanDuel uses state-specific `sbapi.{state}.sportsbook.fanduel.com` JSON APIs.
     - FlareSolverr is useful only for true Cloudflare challenges; DK/FD blocks are likely Akamai/TLS/region/session, not Cloudflare.

3. Tested direct HTTP and FlareSolverr endpoints.
   - Confirmed homelab FlareSolverr is running, healthy, and internal-only:
     - `flaresolverr` container up, version `3.4.6`, internal port `8191`.
   - DraftKings old endpoints returned Akamai `403 Access Denied` with plain `requests`, browser headers, `curl_cffi` Chrome impersonation, and FlareSolverr:
     - `https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/42648?format=json`
     - `https://sportsbook.draftkings.com/sites/US-NJ-SB/api/v5/eventgroups/42648?format=json`
     - `https://sportsbook-nash.draftkings.com/sites/US-SB/api/v5/eventgroups/42648?format=json`
     - `https://sportsbook-nash.draftkings.com/sites/US-NJ-SB/api/v5/eventgroups/42648?format=json`
   - FlareSolverr returned cookies, but the body was still Akamai `Access Denied`; concluded FlareSolverr does not solve DK’s old endpoint block.
   - FanDuel direct JSON worked from local environment for `nj`, `ny`, and `pa` hosts.
   - Confirmed FanDuel Knicks/Hawks event:
     - `eventId=35517728`
     - `name="New York Knicks @ Atlanta Hawks"`

4. Drilled into FanDuel direct JSON.
   - Discovery endpoint:
     ```text
     GET https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page
       ?page=CUSTOM
       &customPageId=nba
       &pbHorizontal=false
       &timezone=America/New_York
       &_ak=FhMFpcPWXMeyZxOx
     ```
   - Event-page endpoint:
     ```text
     GET https://sbapi.nj.sportsbook.fanduel.com/api/event-page
       ?_ak=FhMFpcPWXMeyZxOx
       &eventId=35517728
       &tab=player-defense
       &timezone=America/New_York
     ```
   - Found working FanDuel tab slugs:
     - `player-points`
     - `player-rebounds`
     - `player-assists`
     - `player-threes`
     - `player-defense`
   - Confirmed FanDuel standard O/U market:
     ```text
     Josh Hart - Steals
     marketId=734.165832700
     marketType=PLAYER_E_TOTAL_STEALS
     bettingType=MOVING_HANDICAP
     marketStatus=OPEN
     Over 1.5 +178
     Under 1.5 -245
     ```
   - Confirmed FanDuel also returns milestone ladder markets like `To Record 2+ Steals`, which must be rejected for standard O/U ingestion.

5. The user then asked: “document this plan then try option 4 for both fd and dk.”
   - Interpreted “option 4” as browser-backed fetch/XHR capture.
   - Invoked `stealth-browser` and `writing-clearly-and-concisely`.
   - No local Chrome/Chromium and no Playwright/Selenium/nodriver were initially available.
   - Created a temporary Playwright venv under `/tmp/sportsbook-browser-venv`, installed Playwright, and installed Chromium there.
   - Added report `reports/2026-04-25-direct-sportsbook-props-plan.md`.
   - Browser-backed FanDuel probe succeeded and confirmed the same Josh Hart steals O/U market from Chromium:
     ```json
     {
       "marketId": "734.165832700",
       "marketName": "Josh Hart - Steals",
       "marketType": "PLAYER_E_TOTAL_STEALS",
       "bettingType": "MOVING_HANDICAP",
       "marketStatus": "OPEN",
       "runners": [
         {"runnerName": "Josh Hart Over", "handicap": 1.5, "odds": 178, "runnerStatus": "ACTIVE"},
         {"runnerName": "Josh Hart Under", "handicap": 1.5, "odds": -245, "runnerStatus": "ACTIVE"}
       ]
     }
     ```
   - Browser-backed DraftKings old JSON endpoint still returned Akamai `403`.
   - However, the live DK page loaded in Chromium and revealed a newer working endpoint:
     ```text
     https://sportsbook-nash.draftkings.com/sites/US-NJ-SB/api/sportscontent/controldata/...
     ```
   - The initial NBA league page called:
     ```text
     /sites/US-NJ-SB/api/sportscontent/controldata/league/leagueSubcategory/v1/markets
       ?isBatchable=false
       &templateVars=42648
       &eventsQuery=$filter=leagueId eq '42648' AND clientMetadata/Subcategories/any(s: s/Id eq '4511')
       &marketsQuery=$filter=clientMetadata/subCategoryId eq '4511' AND tags/all(t: t ne 'SportcastBetBuilder')
       &include=Events
       &entity=events
     ```
   - Opening `https://sportsbook.draftkings.com/page/nba-player-props` captured a better endpoint:
     ```text
     /sites/US-NJ-SB/api/sportscontent/controldata/standalone/leagueSubcategory/v1/markets
     ```
   - Clicking `Player Defense` then `Steals O/U` captured the DK steals O/U subcategory:
     - `subcategoryId=13508`
     - `marketType.name="Steals O/U"`
   - The rendered DraftKings body showed Josh Hart:
     ```text
     Josh Hart STLPG 1.2
     O 0.5 -226
     U 0.5 +168
     ```
   - Parsed DK JSON confirmed:
     ```text
     market id: 328789167
     market name: Josh Hart Steals O/U
     eventId: 34041275
     subcategoryId: 13508
     marketType.name: Steals O/U
     over: points 0.5, odds -226
     under: points 0.5, odds +168
     ```
   - This means the original dashboard `SGO_DK=0.5` was actually aligned with DraftKings’ current O/U table at the time of browser capture; the user’s “2+” observation corresponds to a ladder/milestone market, not the standard DK O/U.

6. Compaction interrupted while reading the captured DK output.
   - Important captured output is in `/tmp/copilot-tool-output-1777135686268-najpa0.txt`.
   - Lines 1-8 show the rendered DK Josh Hart snippet and captured endpoints.
   - Lines 35 and 77-78 show the DK Josh Hart market and selections:
     - line 35: `MARKET_MATCH ... "name": "Josh Hart Steals O/U" ... "id": "328789167" ... "subcategoryId": "13508"`
     - line 77: `Over`, `points: 0.5`, `american: −226`, `participant: Josh Hart`
     - line 78: `Under`, `points: 0.5`, `american: +168`, `participant: Josh Hart`
</history>

<work_done>
Files created:
- `reports/2026-04-25-prop-line-integrity-audit.md`
  - Final report for the SGO/Josh Hart line-integrity incident.
  - Committed and pushed to GitHub `main` at `83bff35`.
- `reports/2026-04-25-direct-sportsbook-props-plan.md`
  - New report documenting direct FD/DK source plan, FanDuel endpoints, DraftKings old endpoint failures, source priority, and browser-backed validation plan.
  - Created but not yet committed/pushed at compaction time.

Session artifacts / temporary files:
- `/tmp/sportsbook-browser-venv`
  - Temporary Playwright environment used to install Chromium and run browser-backed tests.
  - Not yet cleaned up at compaction time.
- `/tmp/copilot-tool-output-1777135686268-najpa0.txt`
  - Large DK browser capture after clicking `Steals O/U`.
  - Contains critical parsed DK JSON for Josh Hart steals.
- `/tmp/copilot-tool-output-1777135692536-9ft208.txt` and `/tmp/copilot-tool-output-1777135698172-u3kkaj.txt`
  - Grep/summarized extraction artifacts for DK capture.

SQL todos created and status:
- `document-direct-plan`: in_progress at creation; likely should be marked `done` after confirming the report file.
- `browser-fetch-fd`: pending at creation; should be marked `done` because browser-backed FD succeeded.
- `browser-fetch-dk`: pending at creation; should be marked `done` because browser-backed DK succeeded via sportscontent endpoint.
- `summarize-browser-results`: pending; still needs final summary/report update and likely commit/push.

Current repo state:
- Working tree should have one uncommitted file:
  - `reports/2026-04-25-direct-sportsbook-props-plan.md`
- Branch/worktree:
  - `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
  - branch `feature/dashboard-accuracy-final`
  - `origin/main` includes prior commit `83bff35`
- Need to run `git status` after compaction to confirm.

What works:
- FanDuel direct `sbapi` works via direct HTTP and browser-backed Chromium.
- DraftKings old `/api/v5/eventgroups` endpoint does not work.
- DraftKings newer `sportscontent/controldata/standalone/leagueSubcategory/v1/markets` works through browser-discovered URL and likely direct HTTP once endpoint and subcategory IDs are known.
- Browser-backed DK captured the actual standard O/U Josh Hart steals market.

What is incomplete:
- `reports/2026-04-25-direct-sportsbook-props-plan.md` needs updating with the new DK `sportscontent` endpoint discovery and the conclusion that DK standard O/U was `0.5`, while `2+` is a milestone/ladder market.
- Need to commit and push that report.
- Need to clean up `/tmp/sportsbook-browser-venv`.
- Need to save final DK/FD browser-backed findings to MemPalace after report update.
</work_done>

<technical_details>
Key discoveries:
- FanDuel direct API:
  - Host pattern: `https://sbapi.{state}.sportsbook.fanduel.com/api/...`
  - Tested states: `nj`, `ny`, `pa`; all returned content-managed NBA pages.
  - Public app key used by FD web: `_ak=FhMFpcPWXMeyZxOx`.
  - NBA event discovery for Knicks/Hawks:
    - `eventId=35517728`
    - `competitionId=10547864`
    - `eventTypeId=7522`
  - Standard O/U event-page tabs:
    - `player-points`
    - `player-rebounds`
    - `player-assists`
    - `player-threes`
    - `player-defense`
  - For standard O/U accept only:
    - `bettingType=MOVING_HANDICAP`
    - `marketStatus=OPEN`
    - exactly two active runners
    - `runnerName` ends in `Over`/`Under`
    - same `handicap` for both sides
    - reject `To Record N+`, ladder, milestone, SGP, quick bets, quarter-specific markets.
  - Josh Hart FD standard steals:
    - `marketId=734.165832700`
    - `marketName="Josh Hart - Steals"`
    - `marketType=PLAYER_E_TOTAL_STEALS`
    - `Over 1.5 +178`
    - `Under 1.5 -245`

- DraftKings endpoint situation:
  - Old endpoint blocked by Akamai:
    - `/sites/{SITE}/api/v5/eventgroups/42648?format=json`
    - returns `403 text/html`, `server: AkamaiGHost`
  - FlareSolverr does not help:
    - FlareSolverr is healthy and returns cookies, but the response body is still Akamai Access Denied.
    - Not a Cloudflare challenge.
  - `curl_cffi` Chrome impersonation also did not help old endpoint.
  - Browser-backed Chromium can load DK web shell:
    - `https://sportsbook.draftkings.com/leagues/basketball/nba`
    - `https://sportsbook.draftkings.com/page/nba-player-props`
  - DK web shell uses newer `sportscontent/controldata` endpoints that work:
    - General NBA page used `league/leagueSubcategory/v1/markets` with `subcategoryId=4511`.
    - NBA Player Props page used `standalone/leagueSubcategory/v1/markets`.
  - DK NBA Player Props URL:
    - `https://sportsbook.draftkings.com/page/nba-player-props`
  - DK category filters in HTML include:
    - `player-points`
    - `player-threes`
    - `player-combos`
    - `player-rebounds`
    - `player-assists`
    - `player-defense`
    - `h2h-player-props`
  - DK `Player Defense` then `Steals O/U` yields:
    - endpoint path:
      ```text
      https://sportsbook-nash.draftkings.com/sites/US-NJ-SB/api/sportscontent/controldata/standalone/leagueSubcategory/v1/markets
      ```
    - query:
      ```text
      isBatchable=false
      eventsQuery=$filter=leagueId eq '42648' AND clientMetadata/Subcategories/any(s: s/Id eq '13508')
      marketsQuery=$filter=clientMetadata/subCategoryId eq '13508' AND tags/all(t: t ne 'SportcastBetBuilder')
      include=Events
      entity=events
      ```
    - `subcategoryId=13508`
    - `marketType.id=12664`
    - `marketType.name="Steals O/U"`
  - DK Josh Hart standard O/U:
    - eventId `34041275`
    - market id `328789167`
    - market name `Josh Hart Steals O/U`
    - over selection:
      - label `Over`
      - points `0.5`
      - odds `−226`
      - participant `Josh Hart`
      - tags include `MainPointLine`
    - under selection:
      - label `Under`
      - points `0.5`
      - odds `+168`
      - participant `Josh Hart`
      - tags include `MainPointLine`
  - This clarifies the original issue:
    - Dashboard `SGO_DK 0.5 -226/+168` matched the direct DraftKings standard O/U at browser-capture time.
    - User-reported `2+` is likely a DK milestone/ladder market, not the standard O/U line.
    - FanDuel standard O/U differs at `1.5 +178/-245`.

- The Odds API:
  - Already integrated in `src/data/prop_lines.py`.
  - Production-safe, no bot wall, but current key was out of usage credits.
  - Should remain the safest source for DK/FD if quota restored.

- Environment/tooling:
  - Local system Python is externally managed; direct `pip install --user` failed.
  - Temporary venv approach worked:
    ```bash
    python3 -m venv /tmp/sportsbook-browser-venv
    /tmp/sportsbook-browser-venv/bin/python -m pip install --quiet playwright
    /tmp/sportsbook-browser-venv/bin/python -m playwright install chromium
    ```
  - Initial stealth-browser/nodriver failed earlier because no Chrome/Chromium was installed.
  - Playwright Chromium in temp venv was successful for browser-backed testing.
  - Need to remove `/tmp/sportsbook-browser-venv` at end.

- Homelab:
  - FlareSolverr service is in `homelab/compose/compose.jobs.yml`.
  - Container is internal-only, healthy, and uses port `8191`.
  - It is not a general Akamai bypass.

- Important source priority decision:
  - Use direct `FD_WEB` and discovered `DK_WEB` sportscontent endpoints as validation-first adapters.
  - The Odds API remains production-safe baseline when quota is available.
  - SGO should remain demoted/quarantined until validation filters are hardened.
</technical_details>

<important_files>
- `reports/2026-04-25-prop-line-integrity-audit.md`
  - Already committed/pushed report documenting the Josh Hart/SportsGameOdds data-integrity incident.
  - Explains raw SGO contamination and fix plan.
- `reports/2026-04-25-direct-sportsbook-props-plan.md`
  - Newly created but not yet committed.
  - Documents the direct FD/DK source plan.
  - Needs update with latest browser-backed DK sportscontent discovery and conclusion about DK `0.5` standard O/U vs `2+` milestone.
- `src/data/prop_lines.py`
  - Existing prop ingestion code.
  - Important sections:
    - The Odds API config/markets/bookmakers around lines 43-110.
    - SGO extraction around lines 371-505.
    - Fetch order around lines 801-820.
    - Filters around lines 838-865.
    - Upsert/snapshot logic around lines 870-893.
  - Future direct-source adapters should integrate with or sit beside this module.
- `src/db/models.py`
  - `PropLine` schema around lines 206-229.
  - `source` is part of PK and `String(20)`, so source names like `FD_WEB` and `DK_WEB` fit.
- `dashboard-ui/server/src/index.ts`
  - Current dashboard `/api/props` BFF uses `mv_prop_lines_primary`.
  - Important if future source-priority logic changes are needed.
- `homelab/compose/compose.jobs.yml`
  - Defines FlareSolverr.
  - Important because user mentioned FlareSolverr and it was tested.
- `homelab/.env.example`
  - Includes NBA ML API and odds provider env vars.
  - Future implementation may need direct sportsbook source flags.
- `/tmp/copilot-tool-output-1777135686268-najpa0.txt`
  - Temporary but critical until the report is updated.
  - Contains full DK browser capture and parsed market/selections.
  - Read lines 1-8 and 35, 77-78 for Josh Hart steals evidence.
</important_files>

<next_steps>
Immediate continuation:
1. Open and update `reports/2026-04-25-direct-sportsbook-props-plan.md` with:
   - Browser-backed FanDuel success.
   - DraftKings old endpoint failure remains true.
   - New DraftKings `sportscontent/controldata/standalone/leagueSubcategory/v1/markets` endpoint discovery.
   - DK `subcategoryId=13508` for `Steals O/U`.
   - DK Josh Hart standard O/U line `0.5 -226/+168`.
   - Clarification: user’s `2+` is a milestone/ladder market, while the dashboard’s `0.5` matched DK standard O/U at browser-capture time.
2. Mark SQL todos:
   - `document-direct-plan` done after report update.
   - `browser-fetch-fd` done.
   - `browser-fetch-dk` done.
   - `summarize-browser-results` done after final report update.
3. Clean up temporary venv:
   ```bash
   rm -rf /tmp/sportsbook-browser-venv
   ```
4. Run `git status`, review diff, commit, and push:
   - Suggested commit:
     ```text
     docs: document direct sportsbook source plan

     Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
     ```
5. Save final findings to MemPalace:
   - Direct FD works.
   - DK works through `sportscontent/controldata/standalone/leagueSubcategory/v1/markets`.
   - Old DK eventgroups blocked.
   - FlareSolverr not useful for DK Akamai.
   - Josh Hart DK standard O/U `0.5 -226/+168`; FD standard O/U `1.5 +178/-245`; `2+` is ladder/milestone.
6. Final user response should clearly say:
   - Plan documented and pushed if completed.
   - Browser-backed FD succeeded.
   - Browser-backed DK succeeded via a different endpoint than expected.
   - FlareSolverr did not solve DK’s old endpoint.
   - Key product implication: need to label/handle standard O/U separately from milestone `N+` markets.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
