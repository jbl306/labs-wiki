---
title: "Copilot Session Checkpoint: Hermes Dashboard Migration"
type: text
captured: 2026-05-11T15:04:46.343049Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace, agents, dashboard]
checkpoint_class: durable-architecture
checkpoint_class_rule: "title:migration"
retention_mode: retain
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Hermes Dashboard Migration
**Session ID:** `eff82e9b-6a87-4640-a477-2a81cd426ccb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/eff82e9b-6a87-4640-a477-2a81cd426ccb/checkpoints/001-hermes-dashboard-migration.md`
**Checkpoint timestamp:** 2026-05-11T14:51:39.574081Z
**Exported:** 2026-05-11T15:04:46.343049Z
**Checkpoint class:** `durable-architecture` (rule: `title:migration`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user wanted the homelab Hermes deployment migrated from the old community `hermes-webui` container to the official host-managed Hermes dashboard, TUI, gateway, and Kanban flow, then wanted documentation for public access through Cloudflare Access. The work followed the existing migration plan in `homelab/tasks/todo.md`, used the homelab deployment workflow, and prioritized safe exposure because Hermes Dashboard has no native auth.
</overview>

<history>
1. The user asked to execute the Hermes native dashboard/TUI/Kanban migration plan and update the homelab Homepage.
   - Loaded `task-observer`, `homelab-deploy`, `executing-plans`, and related context from MemPalace.
   - Reviewed `homelab/tasks/todo.md` and `docs/plans/2026-05-11-hermes-native-dashboard-tui-kanban.md`.
   - Created an isolated worktree/branch, implemented the migration, reviewed via subagents, then fast-forwarded the live checkout.
   - Removed the old `hermes-webui` compose service and live container.
   - Added host systemd user services for `hermes-dashboard.service` and `hermes-gateway.service`.
   - Updated Caddy, AdGuard rewrites, Homepage, Uptime Kuma, docs, and task tracker.
   - Fixed several issues discovered during deployment:
     - `hermes gateway start` was wrong for systemd; changed launcher to `hermes gateway run --replace`.
     - Gateway needed the existing Node path for the WhatsApp bridge.
     - Caddy on the `proxy` Docker network needed a UFW allow rule for `172.20.1.0/24` before the raw-port deny.
     - Public route initially exposed the dashboard; added Caddy gate requiring `Cf-Access-Jwt-Assertion`.
     - DNS sync script needed executable bit and `.env` loading.
     - GitHub Actions deploy failed because SSH secrets are absent; workflow now skips deploy cleanly when secrets are missing.
   - Pushed all migration commits; final GitHub Actions run `25671435296` succeeded.

2. The user asked how to configure/access `hermes.jbl-lab.com` publicly away from home and to document it.
   - Added public access runbook sections to:
     - `docs/05-service-guide.md` under Hermes Dashboard → “Public access away from home”.
     - `docs/08-cloudflare-tunnel.md` under “Hermes Dashboard Access setup”.
   - Documented Cloudflare Zero Trust Access application setup:
     - App name `Hermes Dashboard`.
     - Domain `hermes.jbl-lab.com`.
     - Allow only approved users/groups.
     - Confirm tunnel public hostname routes to `http://caddy:80`.
   - Documented validation commands for:
     - Unauthenticated public 403.
     - LAN DNS resolving Hermes to Cloudflare IPs.
     - Local synthetic `Cf-Access-Jwt-Assertion` header reaching `/api/status`.
   - Pushed docs commit `445210d docs: document Hermes public Access setup`.

3. The user then reported that after Cloudflare setup, `hermes.jbl-lab.com` still shows the old WebUI and seems cached.
   - Loaded `task-observer`, `homelab-deploy`, and `systematic-debugging`.
   - Retrieved MemPalace context showing prior Cloudflare cache gotcha: CF “Cache Everything” page rules can cache assets/html and ignore origin `Cache-Control`; busting may require querystrings or explicit Cloudflare purge/rule changes.
   - Began root-cause investigation plan: check old containers/processes, local Caddy responses with/without Access header, public Cloudflare headers/title, and whether public content is cached or hitting another origin.
   - Several `bash` tool attempts failed due malformed tool payloads (`description` missing error), so the actual diagnostics for the old WebUI issue had not yet completed when compaction was requested.
</history>

<work_done>
Files modified and pushed in `homelab`:
- `.env.example`
  - Removed obsolete `HERMES_WEBUI_PASSWORD`.
- `AGENTS.md`
  - Clarified live repo checkout path is `~/projects/homelab`; runtime data remains `/opt/homelab`.
- `README.md`
  - Replaced Hermes WebUI inventory with Hermes Dashboard.
  - Updated deploy path docs to `~/projects/homelab`.
- `compose/compose.proxy.yml`
  - Added Caddy route for `http://hermes.${DOMAIN}`.
  - Route requires `Cf-Access-Jwt-Assertion`; otherwise returns `403 Cloudflare Access required`.
  - Proxies authorized requests to `host.docker.internal:9119`.
- `compose/compose.web.yml`
  - Removed `hermes-webui` service.
- `config/adguard/dns-rewrites.json`
  - Added exact-host rewrite for `hermes.jbl-lab.com` to Cloudflare IP target.
- `config/homepage/services.yaml`
  - Replaced Hermes WebUI card with Hermes Dashboard pointing to `https://hermes.${DOMAIN}` and monitoring `http://host.docker.internal:9119/api/status`.
- `config/systemd/user/hermes-dashboard.service`
  - New systemd user unit for `hermes dashboard --host 0.0.0.0 --port 9119 --no-open --insecure --tui`.
- `config/systemd/user/hermes-gateway.service`
  - New systemd user unit running foreground `hermes gateway run --replace`.
  - Includes Node path for WhatsApp bridge.
- `scripts/ops/hermes-dashboard.sh`
  - New executable launcher.
- `scripts/ops/hermes-gateway.sh`
  - New executable launcher.
- `scripts/ops/setup.sh`
  - Removed `webui-mvp` directory setup and old WebUI warning.
- `scripts/ops/sync-dns-rewrites.sh`
  - Made executable.
  - Loads `.env` automatically for `ADGUARD_USER`/`ADGUARD_PASS`.
- `scripts/monitoring/update_uptime_kuma.py`
  - Added `Hermes Dashboard` monitor.
  - Removes stale `Hermes WebUI`.
- `docs/05-service-guide.md`
  - Replaced Hermes WebUI section with Hermes Dashboard operations.
  - Added public-access-away-from-home Cloudflare Access setup.
- `docs/08-cloudflare-tunnel.md`
  - Added Hermes public hostname and required Access setup.
- `docs/14-hermes-dashboard-evaluation.md`
  - Marked old evaluation superseded.
- `docs/plans/2026-05-11-hermes-native-dashboard-tui-kanban.md`
  - Updated implementation notes for live v0.12 CLI, foreground gateway command, Caddy Access gate, and no `kanban boards` subcommand.
- `tasks/todo.md`
  - Added implementation/review notes.
- `.github/workflows/deploy.yml`
  - Removed obsolete CI `HERMES_WEBUI_PASSWORD`.
  - Default `HOMELAB_DEPLOY_PATH` set to `/home/jbl/projects/homelab`.
  - Deploy job skips cleanly if SSH secrets are missing.

Live system state after migration:
- `hermes-dashboard.service`: active.
- `hermes-gateway.service`: active.
- Dashboard API reports Hermes `0.12.0`, gateway `running`, `gateway_running=True`.
- `hermes-webui` container absent.
- Homepage reachable and healthy.
- Uptime Kuma has Hermes Dashboard monitor.
- AdGuard rewrite for `hermes.jbl-lab.com` applied.
- UFW rules include:
  - Allow `9119/tcp` on `docker0`.
  - Allow `9119/tcp` from `172.20.1.0/24` proxy network.
  - Deny `9119/tcp` from anywhere else.
- Caddy public route:
  - No Access header → `403 Cloudflare Access required`.
  - Synthetic `Cf-Access-Jwt-Assertion` header locally → official Hermes dashboard/API.

Commits pushed during this session:
- `98b352e feat: migrate Hermes to native dashboard`
- `216c869 fix: align Hermes gateway service with host runtime`
- `409186b fix: make DNS rewrite sync executable`
- `9478523 fix: load env for DNS rewrite sync`
- `ec4e42a fix: gate Hermes route on Cloudflare Access header`
- `f964f55 fix: order Hermes Caddy Access gate`
- `9e1742f ci: skip homelab deploy when SSH secrets are absent`
- `445210d docs: document Hermes public Access setup`

Non-repo workspace change:
- `skill-observations/log.md`
  - Observation `obs-2026-05-11-001` marked `APPLIED`.
</work_done>

<technical_details>
- Hermes Dashboard has no native auth when bound beyond localhost. Public access must go through Cloudflare Access.
- Caddy gate pattern used:
  - `caddy.@cf_access.header: Cf-Access-Jwt-Assertion *`
  - `caddy.route.0_reverse_proxy: "@cf_access host.docker.internal:9119"`
  - `caddy.route.1_respond: '"Cloudflare Access required" 403'`
  - Order matters. Earlier use of `caddy.reverse_proxy` plus `caddy.respond` caused Caddy to respond `403` before the matcher route.
- Caddy container image lacks `sh` and `wget`; validate through published `:80` with Host header instead:
  - `curl -fsS -H 'Host: hermes.jbl-lab.com' -H 'Cf-Access-Jwt-Assertion: smoke' http://127.0.0.1/api/status`
- Caddy is on custom Docker network `proxy` with subnet `172.20.1.0/24`, not just `docker0`; UFW needed an allow for that subnet before deny-all port 9119.
- `hermes gateway start` is a service-management command, not the right systemd foreground command. Use `hermes gateway run --replace`.
- Gateway needs Node in PATH for WhatsApp bridge:
  - `/home/jbl/.nvm/versions/node/v20.20.1/bin`
- Hermes live version is `0.12.0 (2026.4.30)`.
- Hermes v0.12 Kanban CLI does not expose `kanban boards`; use `hermes kanban init`, `create`, `list`, `show`, `stats`, etc.
- Hermes virtualenv lacks `pip`; initial attempt to install extras fell back to system `pip` and hit Ubuntu PEP 668 externally-managed environment. Since Hermes CLI already had dashboard/TUI/Kanban/gateway commands, no package install was needed.
- `sync-dns-rewrites.sh` required `.env` loading for `ADGUARD_USER`/`ADGUARD_PASS`.
- GitHub Actions deploy job has no SSH secrets configured; compose validation passes, deploy now skips instead of failing.
- Cloudflare cache gotcha found in session memory: CF “Cache Everything” page rules can cache `.js`/`.css`/HTML at edge and ignore origin `Cache-Control`. Cache-busting may require querystring, Cloudflare purge, disabling Cache Everything for `hermes.jbl-lab.com`, or explicit cache-control/CDN-cache headers.
- Active debugging hypothesis for current user report:
  - Local Caddy likely serves official Hermes (previously verified).
  - If user sees old WebUI publicly, likely Cloudflare edge cache/page rule, a Cloudflare Tunnel public-hostname route not pointing to `caddy:80`, browser cache/service worker from old WebUI, or some remaining old process/origin route.
- Need to avoid further “fixes” until evidence is collected per systematic debugging.
</technical_details>

<important_files>
- `homelab/compose/compose.proxy.yml`
  - Central for Hermes public route.
  - Current Hermes route should require `Cf-Access-Jwt-Assertion` and proxy to `host.docker.internal:9119`.
  - Check lines around labels under `services.caddy`.
- `homelab/compose/compose.web.yml`
  - Should no longer contain `hermes-webui`.
- `homelab/config/adguard/dns-rewrites.json`
  - Contains `hermes.jbl-lab.com` exact-host Cloudflare rewrite around the Plex/OpenCode entries.
- `homelab/config/systemd/user/hermes-dashboard.service`
  - Tracked unit for dashboard.
- `homelab/config/systemd/user/hermes-gateway.service`
  - Tracked unit for gateway; must run foreground `hermes gateway run --replace` and include Node path.
- `homelab/scripts/ops/hermes-dashboard.sh`
  - Dashboard launcher.
- `homelab/scripts/ops/hermes-gateway.sh`
  - Gateway launcher.
- `homelab/scripts/ops/sync-dns-rewrites.sh`
  - Now executable and loads `.env`.
- `homelab/config/homepage/services.yaml`
  - Homepage Hermes Dashboard card.
- `homelab/scripts/monitoring/update_uptime_kuma.py`
  - Uptime Kuma monitor desired state.
- `homelab/docs/05-service-guide.md`
  - Hermes operations and public access docs.
  - Sections: `## Hermes Dashboard`, `### Public access away from home`.
- `homelab/docs/08-cloudflare-tunnel.md`
  - Cloudflare public hostname and Access setup.
  - Section: `### Hermes Dashboard Access setup`.
- `homelab/.github/workflows/deploy.yml`
  - CI deploy skip logic and checkout path.
- `homelab/tasks/todo.md`
  - Migration plan implementation/review summary.
- `skill-observations/log.md`
  - Contains applied observation about host-service Caddy routes, UFW custom network, and Access gates.
</important_files>

<next_steps>
Immediate task: debug why the user still sees old WebUI at `hermes.jbl-lab.com`.

Planned systematic debugging steps:
1. Verify current local origin state:
   - `docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.Image}}' | grep -i hermes`
   - `ps -eo user,pid,ppid,cmd | grep -i '[h]ermeswebui\|[h]ermes-webui'`
   - `systemctl --user list-unit-files 'hermes*' --no-pager`
2. Verify Caddy locally:
   - No header: `curl -sS -D /tmp/hermes-local-nohdr.headers -o /tmp/hermes-local-nohdr.body -H 'Host: hermes.jbl-lab.com' http://127.0.0.1/ -w '%{http_code}\n'`
   - With synthetic Access header root/title: `curl -fsS -H 'Host: hermes.jbl-lab.com' -H 'Cf-Access-Jwt-Assertion: smoke' http://127.0.0.1/`
   - With synthetic Access header API: `curl -fsS -H 'Host: hermes.jbl-lab.com' -H 'Cf-Access-Jwt-Assertion: smoke' http://127.0.0.1/api/status`
3. Verify public Cloudflare response:
   - Use `curl -sS -L --max-time 30 -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' -D /tmp/hermes-public.headers -o /tmp/hermes-public.html https://hermes.jbl-lab.com/ -w '%{http_code}\n'`
   - Inspect `cf-cache-status`, `age`, `server`, `location`, title/body.
   - Compare cache-busting URL: `https://hermes.jbl-lab.com/?bust=$(date +%s)`.
4. If Cloudflare serves old content:
   - Check Cloudflare dashboard for Page Rules / Cache Rules affecting `*.jbl-lab.com` or `hermes.jbl-lab.com`, especially “Cache Everything”.
   - Purge cache for `https://hermes.jbl-lab.com/*`.
   - Add a cache bypass rule for `hermes.jbl-lab.com/*` if needed.
   - Consider adding Caddy response headers for Hermes:
     - `Cache-Control: no-store`
     - `CDN-Cache-Control: no-store`
     - But first confirm root cause from headers.
5. If Cloudflare is not hitting Caddy:
   - Check Cloudflare Tunnel public hostname for `hermes.jbl-lab.com` is `http://caddy:80`, not a stale old service URL.
   - Check DNS record/public hostname order and wildcard precedence in tunnel config.
6. If browser-only issue:
   - Have user hard-refresh, clear site data for `hermes.jbl-lab.com`, or test private browsing / another device.
   - Old WebUI may have cached service worker/assets in browser.
7. After root cause is found:
   - Apply minimal fix.
   - Document cache/tunnel gotcha in `docs/08-cloudflare-tunnel.md` and/or Hermes section.
   - Commit/push if repo changes are needed.
   - Store finding in MemPalace and possibly update `skill-observations/log.md`.

Note: Last tool attempts failed because `functions.bash` calls were malformed with missing `description`; next assistant should use a valid `bash` payload with both `description` and `command`.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
