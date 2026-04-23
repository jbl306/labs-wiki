---
title: jbl306/homelab
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 495fc3408f26cc34a71561c8d3a2ef579a525f88f0fd54807a1a9990c3b81516
sources:
- raw/2026-04-07-jbl306homelab.md
source_url: https://github.com/jbl306/homelab
tags:
- github
- shell
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 65
concepts:
- homelab-server-deployment-nba-ml-platform
- comprehensive-grafana-monitoring-for-docker-homelab-services
- homelab-service-inventory-and-dashboard-synchronization
- split-dns-routing-cloudflare-tunnel-overrides-homelab-services
- homelab-cron-job-integration-throttled-ingestion
- homelab-media-domain-routing-lan-public-https-diagnostics
---

# jbl306/homelab

## What it is

This is our own homelab repository — Docker Compose infrastructure for a Beelink GTi13 Ultra running Ubuntu Server 24.04 LTS (Intel i9-13900HK, 32 GB DDR5, 1 TB NVMe). It composes ~30+ services across media (Plex, Jellyfin, Riven, Seerr), self-hosted apps (Immich, Nextcloud, Vaultwarden), the nba-ml stack (API, dashboard, MLflow, TimescaleDB), the labs-wiki ingest API, and full Prometheus + cAdvisor + Node Exporter + Grafana monitoring. Caddy reverse-proxies everything behind a Cloudflare Tunnel; AdGuard provides LAN DNS rewrites for the same `*.jbl-lab.com` hostnames.

## Why it matters

Single source of truth for what runs on the server and how it's wired. Anything we deploy goes through this repo — `homelab-deploy` skill in `.github/skills/` is the canonical workflow for adding a service. CI deploys to the server over SSH on every push to `main`, so the repo's state is the server's state.

## Architecture / Technical model

**Stacked Docker Compose files** — Per-domain compose files in `compose/` (`compose.media.yml`, `compose.nba-ml.yml`, `compose.proxy.yml`, `compose.monitoring.yml`, `compose.jobs.yml`, `compose.riven.yml`, `compose.stremio.yml`, `compose.cloud.yml`, `compose.photos.yml`, `compose.infra.yml`, `compose.wiki.yml`, `compose.wiki-graph.yml`, `compose.web.yml`, `compose.tunnel.yml`) merged via root `docker-compose.yml` (uses `include:` directive). All stacks share a single `.env` file at repo root. Deploy all: `docker compose up -d`. Deploy one: `docker compose -f compose/compose.<stack>.yml --env-file .env up -d`.
> See [[homelab-server-deployment-nba-ml-platform]] for the nba-ml stack.

**Caddy + Cloudflare Tunnel** — Public access: Internet → Cloudflare Edge (TLS termination) → `cloudflared` tunnel connector → Caddy `:80` HTTP → service. LAN access: AdGuard DNS rewrites `*.jbl-lab.com → 192.168.1.238` → Caddy `:80` HTTP → service. No ports forwarded, no public IP exposed. Plex exception: tunnel routes directly to `host.docker.internal:32400` (host network mode, bypasses Caddy).
> See [[split-dns-routing-cloudflare-tunnel-overrides-homelab-services]].

**AdGuard DNS rewrites** — LAN clients (including Tailscale) resolve `*.jbl-lab.com` to the server's LAN IP (`192.168.1.238`). More-specific rewrites override the wildcard: `vault.jbl-lab.com` and `torrentio.jbl-lab.com` point to Cloudflare proxy IPs (forcing TLS termination at the edge even for LAN clients). Managed via `config/adguard/dns-rewrites.json` and synced to AdGuard's API with `scripts/ops/sync-dns-rewrites.sh`.
> See [[homelab-media-domain-routing-lan-public-https-diagnostics]].

**Resource limits everywhere** — Every container has `deploy.resources.limits` (memory and CPU) to prevent runaway processes from starving the host. Key allocations: Plex/Jellyfin 4G/4.0, nba-ml-api 4G/4.0, Riven 2G/2.0, MLflow 2G/1.0, Knightcrawler Producer 512M/0.5 (DMM crawler disabled to avoid memory overflow), databases 512M–2G/0.5–1.0, Redis 64M–512M/0.25–0.5, infrastructure (Caddy, AdGuard, Homepage) 64M–256M/0.25–0.5, monitoring 64M–512M/0.25–1.0.

**Riven + Real-Debrid** — Riven mounts a FUSE VFS at `/mnt/riven/` backed by Real-Debrid's CDN. Plex and Jellyfin read from this mount as if it were local storage. No torrents stored on disk; everything streams from Real-Debrid on demand. Riven manages library metadata, symlink trees, and debrid integration.

**Knightcrawler (self-hosted Torrentio)** — PostgreSQL + Redis + LavinMQ (RabbitMQ-compatible) + three workers: producer (scrapes torrent sources), consumer (processes metadata), debrid-collector (enriches with Real-Debrid availability). Exposes Stremio addon at `torrentio.jbl-lab.com:7000`. DMM crawler intentionally disabled — upstream hashlist ingestion exceeds host memory envelope.

**Monitoring (Prometheus + cAdvisor + Node Exporter + Grafana)** — Prometheus scrapes cAdvisor (per-container CPU/memory/network/disk I/O) and Node Exporter (host-level metrics). Grafana dashboards provisioned from `config/grafana/dashboards/` (no manual import). "Homelab Overview" dashboard: host gauges, CPU/memory trends, top-10 container resources, full container table, network & disk I/O.
> See [[comprehensive-grafana-monitoring-for-docker-homelab-services]].

**Service inventory (Homepage)** — Homepage dashboard at `home.jbl-lab.com` discovers services via a read-only Docker proxy (`homepage-docker-proxy` container). Organized into groups: Media (Plex, Jellyfin, Seerr, Riven, Knightcrawler), Cloud & Storage (Nextcloud, Immich, Vaultwarden), Analytics (NBA ML API/Dashboard, MLflow), Infrastructure (Homepage, AdGuard, Uptime Kuma, Grafana), Dev (OpenCode, Giniecode), Internal (Homepage DB Stats).
> See [[homelab-service-inventory-and-dashboard-synchronization]].

**Cron-driven jobs** — Host cron or container-based cron jobs: Galloping Bot (golf tee-time sniper, Friday noon EST via `compose.jobs.yml`), labs-wiki URL backfill (hourly free-tier helper via `compose.jobs.yml`), FlareSolverr (Cloudflare clearance prewarm for Galloping Bot).
> See [[homelab-cron-job-integration-throttled-ingestion]].

**NBA ML stack (opt-in)** — Requires `NBA_ML_ENGINE_PATH` in `.env` pointing at a sibling `nba-ml-engine` checkout. Compose stack (`compose.nba-ml.yml`) mounts the engine via relative path, deploys TimescaleDB (time-series NBA stats), FastAPI (prediction API), Streamlit dashboard, MLflow (experiment tracking). Not deployed by default `./scripts/ops/deploy.sh`; must be deployed separately.

**MemPalace (native, not Docker)** — Installed via `pipx` on the host (not containerized). Persistent AI memory layer with ChromaDB embeddings at `~/.mempalace/palace/`. MCP server configured in `~/.copilot/mcp-config.json` (stdio transport). Used by OpenCode/Copilot CLI for cross-session memory. Requires `GITHUB_MODELS_TOKEN` (PAT with `models:read` scope) for wiki auto-ingest GPT-4.1 calls.

**Docker networks** — `proxy` (HTTP exposure via Caddy), `media` (media servers ↔ Riven VFS), `stremio` (Knightcrawler ↔ Riven), `cloud` (Nextcloud ↔ MariaDB ↔ Redis), `photos` (Immich ↔ PostgreSQL ↔ Redis), `monitoring` (Prometheus ↔ Grafana ↔ cAdvisor ↔ Node Exporter).

**Storage layout** — `/opt/homelab/` (repo root, compose files, configs), `/mnt/riven/` (Riven VFS FUSE mount), `/mnt/nas/` (optional NAS mount for backups/media/photos).

**Push notifications (ntfy)** — Two layers: (1) Uptime Kuma → ntfy (HTTP health checks for service down/up/errors/timeouts), (2) docker-notify container → ntfy (Docker events: container crashes, OOM kills, unhealthy status, restart loops). Configured via `.env`: `NTFY_SERVER=https://ntfy.sh`, `NTFY_TOPIC=your-homelab-alerts`.

**GitHub Actions CI/CD** — `deploy.yml` (validates merged Compose config on PRs; SSH-deploys to server on `main` pushes), `release.yml` (validates, packages, creates GitHub Release with tarball + sha256 on `v*.*.*` tags). Required secrets: `HOMELAB_SSH_HOST`, `HOMELAB_SSH_USERNAME`, `HOMELAB_SSH_PRIVATE_KEY`, `HOMELAB_SSH_FINGERPRINT`. Optional vars: `HOMELAB_DEPLOY_PATH` (default `/opt/homelab`), `HOMELAB_SSH_PORT` (default 22).

## How it works

### Deployment flow
1. Developer pushes to `main` or creates a PR
2. GitHub Actions validates the merged Compose config (`docker compose config`)
3. On `main` push: SSH into the server, `git pull --ff-only`, run `scripts/ops/deploy.sh`
4. `deploy.sh` recreates missing top-level media config directories (Plex, Jellyfin, Seerr), resets ownership to `PUID:PGID`, then `docker compose up -d` for all stacks (or specified stacks if args provided)
5. Services start/restart with zero-downtime rolling updates (Compose recreates changed containers)

### Service registration (Caddy reverse proxy)
- Each service's Compose stack includes a Caddy site block in `config/caddy/sites/`
- Format: `<service>.${DOMAIN} { reverse_proxy <container-name>:<port> }`
- Example: `jellyfin.${DOMAIN} { reverse_proxy jellyfin:8096 }`
- Caddy reloads automatically when config changes (mounted as volume)
- Cloudflare Tunnel routes `*.jbl-lab.com` traffic to Caddy `:80`; Caddy proxies to the correct container based on hostname

### Secret/env management
- All secrets in `.env` at repo root (gitignored)
- Template: `.env.example` (committed, secrets replaced with placeholders)
- Services reference variables via `${VAR}` in Compose files
- Per-service DB passwords: `RIVEN_DB_PASSWORD`, `IMMICH_DB_PASSWORD`, `NBA_ML_DB_PASSWORD`, etc.
- Real-Debrid token (`RD_API_TOKEN`) shared by Knightcrawler debrid-collector; Riven requires separate UI config
- GitHub Models token (`GITHUB_MODELS_TOKEN`) for wiki auto-ingest GPT-4.1 API access

### Restart/update conventions
- Per-stack: `docker compose -f compose/compose.<stack>.yml --env-file .env restart`
- Full deploy: `./scripts/ops/deploy.sh` (default excludes nba-ml)
- NBA ML deploy: `./scripts/ops/deploy.sh nba-ml` (after setting `NBA_ML_ENGINE_PATH`)
- Update images: `docker compose pull && docker compose up -d` (pulls latest tags, recreates containers)
- Image update monitoring: Diun container (notify-only, no auto-updates)
- Backup: `scripts/ops/backup.sh` (documented in `docs/06-maintenance.md`)

## API / interface surface

**Top-level scripts** (`scripts/ops/`):
- `setup.sh` — Initial server setup (creates directories, sets permissions, installs dependencies)
- `deploy.sh [stack...]` — Deploy all stacks (or specified stacks). Default excludes `nba-ml`. Always run from repo root.
- `backup.sh` — Backup databases and service configs (see `docs/06-maintenance.md`)
- `sync-dns-rewrites.sh` — Sync `config/adguard/dns-rewrites.json` to AdGuard Home via API (requires `ADGUARD_USER` and `ADGUARD_PASS` in `.env`)
- `opencode-serve.sh` — Start OpenCode server on `OPENCODE_PORT` (default 4096)

**Monitoring scripts** (`scripts/monitoring/`):
- `update_uptime_kuma.py` — Sync service monitors to Uptime Kuma via API (uses `KUMA_URL`, `KUMA_USER`, `KUMA_PASS` from `.env`)
- `smoke_test.sh` — Health check all services (curl endpoints, check HTTP status)
- `docker-notify` container — Watch Docker events, push alerts to ntfy (crashes, OOM, unhealthy, restarts)

**Knightcrawler scripts** (`scripts/knightcrawler/`):
- `backfill.sh` — Trigger Knightcrawler backfill (SQL + API automation)
- `*.sql` — Database queries for diagnostics/maintenance
- Patches and diagnostics helpers

**Service ports** (direct access, not through Caddy):
- Plex: 32400 (host network mode)
- Jellyfin: 8096
- Riven: 8070
- Knightcrawler: 7000
- Immich: 2283
- Nextcloud: 8080
- Vaultwarden: 8081
- Homepage: 3002
- AdGuard: 3000
- Uptime Kuma: 3001
- Grafana: 3003
- Seerr: 5055
- NBA ML API: 8000
- NBA ML Dashboard: 8501
- MLflow: 5000
- Wiki Ingest API: 8000
- OpenCode: 4096
- Giniecode: 4097

**Public domains** (via `*.jbl-lab.com`):
- All services listed in "Service Inventory" section of README are accessible via their subdomains
- LAN: resolves to `192.168.1.238` via AdGuard DNS rewrites
- Public: resolves to Cloudflare proxy IPs, tunnels through `cloudflared` to Caddy

## Setup

```bash
# 1. Clone to server
git clone <repo-url> /opt/homelab && cd /opt/homelab

# 2. Create environment file from template
cp .env.example .env
nano .env  # Fill in PUID, PGID, TZ, RD_API_TOKEN, DOMAIN, SERVER_IP, TAILSCALE_IP, etc.

# 3. Make scripts executable
find scripts -type f -name '*.sh' -exec chmod +x {} +

# 4. Run initial setup (creates directories, sets permissions)
./scripts/ops/setup.sh

# 5. Deploy all stacks (excludes nba-ml by default)
./scripts/ops/deploy.sh

# 6. Check status
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker ps -q | wc -l  # Container count

# 7. Optional: Deploy NBA ML stack (after setting NBA_ML_ENGINE_PATH)
./scripts/ops/deploy.sh nba-ml

# 8. Access services
# LAN: http://<service>.jbl-lab.com (resolves to 192.168.1.238)
# Public: https://<service>.jbl-lab.com (Cloudflare Tunnel)
```

## Integration notes

This repo *is* the deployment target for nba-ml-engine (`compose/compose.nba-ml.yml` mounts the engine via `NBA_ML_ENGINE_PATH`) and for the labs-wiki ingest API (`wiki-ingest.jbl-lab.com`). Galloping Bot and the labs-wiki URL backfill run as cron jobs from this stack. When adding a new service to the workspace, follow the `homelab-deploy` skill — it walks the path/port/Caddy/DNS conventions enforced here.

## Caveats / Gotchas

- **Repo is private** — This is a personal infrastructure repo. Deploy paths, secrets, and service configs assume the Beelink hardware profile (`i9-13900HK`, 32GB RAM, 1TB NVMe, `192.168.1.238`). Port to other hardware by adjusting resource limits and IP references in `.env` and Compose files.
- **LAN access uses HTTP (no internal wildcard TLS)** — TLS terminates at Cloudflare for public flows only. LAN clients connect via `http://<service>.jbl-lab.com`. This is intentional (avoids self-signed cert warnings, simplifies config). Sensitive services (`vault.jbl-lab.com`, `torrentio.jbl-lab.com`) force TLS via AdGuard DNS override (points to Cloudflare proxy IPs even for LAN).
- **Default deploy excludes `nba-ml` stack** — `./scripts/ops/deploy.sh` skips `compose.nba-ml.yml` by default. To deploy: set `NBA_ML_ENGINE_PATH` in `.env`, ensure the sibling repo exists, then `./scripts/ops/deploy.sh nba-ml`.
- **Knightcrawler DMM crawler is intentionally disabled** — Upstream hashlist ingest from DMM exceeds the 32GB host memory envelope. The producer container crashes with OOM kills when DMM is enabled. Disable in Knightcrawler's producer config.
- **Plex tunnels directly to host network** — Plex runs in `network_mode: host` (not behind Caddy). The Cloudflare Tunnel routes `plex.jbl-lab.com` directly to `host.docker.internal:32400`. This is a Plex-specific exception due to its non-standard direct-play requirements.
- **Single-box fragility** — No HA, no failover. If the Beelink goes down, all services go down. Backups (`scripts/ops/backup.sh`) mitigate data loss but don't prevent downtime.
- **Env-var handling in passwords** — Avoid `=` characters in passwords (breaks `alembic` configparser in Riven DB migrations). Use `openssl rand -hex 24` for passwords instead of `openssl rand -base64 32`.
- **Resource limit tuning** — Limits are tuned for the Beelink hardware. Adjust per service in Compose files if deploying on different hardware. Knightcrawler Producer limited to 512M/0.5 CPU to prevent OOM; Plex/Jellyfin get 4G/4.0 for transcoding headroom.
- **Cloudflare Tunnel token exposure** — `CLOUDFLARE_TUNNEL_TOKEN` in `.env` grants tunnel access. Rotate if leaked. Token is in plaintext in `.env` (gitignored but visible to anyone with server access).
- **Homepage discovery requires Docker socket** — `homepage-docker-proxy` container binds read-only to `/var/run/docker.sock`. This is a security surface (Docker socket access). The proxy container is isolated to a read-only bind and runs as a non-root user, but it's still a Docker API exposure.
- **Grafana dashboards are provisioned** — Dashboards in `config/grafana/dashboards/` are loaded on Grafana startup. Manual edits in the Grafana UI are not persisted (overwritten on restart). Edit the JSON files and redeploy to persist changes.
- **Labs-Wiki URL backfill runs hourly** — The `compose.jobs.yml` stack includes a container that runs `scripts/backfill_urls_free_tier.py` hourly via cron. This hits the ntfy endpoint when complete. Intentional low-volume helper for free-tier operation.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 0 (private/personal) |
| Primary language | Shell |
| Topics | (none) |
| License | (private) |

## Related concepts

- [[homelab-server-deployment-nba-ml-platform]]
- [[comprehensive-grafana-monitoring-for-docker-homelab-services]]
- [[homelab-service-inventory-and-dashboard-synchronization]]
- [[split-dns-routing-cloudflare-tunnel-overrides-homelab-services]]
- [[homelab-cron-job-integration-throttled-ingestion]]
- [[homelab-media-domain-routing-lan-public-https-diagnostics]]
- [[homelab-infrastructure-patterns-for-ai-memory-migration]]

## Source

- Raw dump: `raw/2026-04-07-jbl306homelab.md`
- Upstream: https://github.com/jbl306/homelab
