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
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- homelab-server-deployment-nba-ml-platform
- comprehensive-grafana-monitoring-for-docker-homelab-services
- homelab-service-inventory-and-dashboard-synchronization
- split-dns-routing-cloudflare-tunnel-overrides-homelab-services
- homelab-cron-job-integration-throttled-ingestion
---

# jbl306/homelab

## What it is

This is our own homelab repository — Docker Compose infrastructure for a Beelink GTi13 Ultra running Ubuntu Server 24.04 LTS (Intel i9-13900HK, 32 GB DDR5, 1 TB NVMe). It composes ~30+ services across media (Plex, Jellyfin, Riven, Seerr), self-hosted apps (Immich, Nextcloud, Vaultwarden), the nba-ml stack (API, dashboard, MLflow, TimescaleDB), the labs-wiki ingest API, and full Prometheus + cAdvisor + Node Exporter + Grafana monitoring. Caddy reverse-proxies everything behind a Cloudflare Tunnel; AdGuard provides LAN DNS rewrites for the same `*.jbl-lab.com` hostnames.

## Why it matters

Single source of truth for what runs on the server and how it's wired. Anything we deploy goes through this repo — `homelab-deploy` skill in `.github/skills/` is the canonical workflow for adding a service. CI deploys to the server over SSH on every push to `main`, so the repo's state is the server's state.

## Key concepts

- **Stacked Compose files** — Per-domain compose files in `compose/` (`compose.media.yml`, `compose.nba-ml.yml`, `compose.proxy.yml`, `compose.monitoring.yml`, etc.) merged via `--env-file .env` from the repo root. See [[homelab-server-deployment-nba-ml-platform]].
- **Caddy + Cloudflare Tunnel** — All public hostnames terminate TLS at Cloudflare, tunnel into `cloudflared`, then HTTP `:80` to Caddy, then service. No ports forwarded. See [[split-dns-routing-cloudflare-tunnel-overrides-homelab-services]].
- **AdGuard DNS rewrites** — `*.jbl-lab.com → 192.168.1.238` for LAN; managed via `config/adguard/dns-rewrites.json` and `scripts/ops/sync-dns-rewrites.sh`. More-specific rewrites (vault, torrentio) override the wildcard.
- **Resource limits everywhere** — Every container has `deploy.resources.limits` to prevent runaway memory on the i9 / 32 GB host.
- **Riven + Real-Debrid** — Streaming-first media via Riven's FUSE VFS at `/mnt/riven/`, plugged into Plex/Jellyfin.
- **Knightcrawler** — Self-hosted Torrentio Stremio addon (PostgreSQL + Redis + LavinMQ + producer/consumer/debrid-collector).
- **Monitoring** — Prometheus scrapes cAdvisor (per-container) + Node Exporter (host); Grafana dashboards exposed at `grafana.jbl-lab.com`. See [[comprehensive-grafana-monitoring-for-docker-homelab-services]].
- **Service inventory** — `Homepage` dashboard at `home.jbl-lab.com` discovers services via a read-only Docker proxy. See [[homelab-service-inventory-and-dashboard-synchronization]].
- **Cron-driven jobs** — Galloping Bot (golf sniper, Friday noon EST), labs-wiki URL backfill (hourly), nba-ml batch jobs. See [[homelab-cron-job-integration-throttled-ingestion]].

## How it works

- All compose stacks live under `/opt/homelab` on the server (cloned from this repo).
- `./scripts/ops/deploy.sh` brings up everything; individual stacks can be deployed with `docker compose -f compose/compose.<stack>.yml --env-file .env up -d`.
- GitHub Actions (`deploy.yml`) validates the merged Compose config on every PR and pushes to `main` SSH-deploy onto the server (`HOMELAB_SSH_*` secrets).
- `release.yml` cuts tagged GitHub Releases with a packaged tarball + sha256.
- `nba-ml` stack is opt-in: requires `NBA_ML_ENGINE_PATH` in `.env` pointing at a sibling `nba-ml-engine` checkout.

## Setup

```bash
git clone <repo-url> /opt/homelab && cd /opt/homelab
cp .env.example .env && nano .env
find scripts -type f -name '*.sh' -exec chmod +x {} +
./scripts/ops/setup.sh
./scripts/ops/deploy.sh

# Inspect
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

## Integration notes

This repo *is* the deployment target for nba-ml-engine (`compose/compose.nba-ml.yml` mounts the engine via `NBA_ML_ENGINE_PATH`) and for the labs-wiki ingest API (`wiki-ingest.jbl-lab.com`). Galloping Bot and the labs-wiki URL backfill run as cron jobs from this stack. When adding a new service to the workspace, follow the `homelab-deploy` skill — it walks the path/port/Caddy/DNS conventions enforced here.

## Caveats / Gotchas

- Repo is private; deploy paths assume `/opt/homelab` and the Beelink hardware profile.
- LAN access intentionally uses HTTP (no internal wildcard TLS) — TLS terminates at Cloudflare for public flows only.
- Default `./scripts/ops/deploy.sh` excludes the `nba-ml` stack — set `NBA_ML_ENGINE_PATH` and deploy it separately.
- Knightcrawler DMM crawler is intentionally disabled — upstream hashlist ingest exceeds the host memory envelope.
- Plex tunnels directly to `host.docker.internal:32400` (host network exception, not a Caddy upstream).

## Repo metadata

| Field | Value |
|---|---|
| Stars | 0 (private/personal) |
| Primary language | Shell |
| Topics | (none) |
| License | (private) |

## Source

- Raw dump: `raw/2026-04-07-jbl306homelab.md`
- Upstream: https://github.com/jbl306/homelab
