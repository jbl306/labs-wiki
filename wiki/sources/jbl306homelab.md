---
title: "jbl306/homelab"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "de40bc77baf9d870707b2d2f3dae074f17d8170ab8973495138735003e86f9d3"
sources:
  - raw/2026-04-07-jbl306homelab.md
quality_score: 100
concepts:
  - homelab-server-deployment-architecture
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
  - comprehensive-grafana-monitoring-for-docker-homelab-services
related:
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
  - "[[Comprehensive Grafana Monitoring for Docker Homelab Services]]"
  - "[[Homelab]]"
tier: hot
knowledge_state: validated
tags: [docker, grafana, architecture, networking, cloudflare, adguard, uptime-kuma, monitoring, homelab]
---

# jbl306/homelab

## Summary

The jbl306/homelab repository provides a comprehensive Docker Compose-based infrastructure for running a Beelink GTi13 Ultra home server on Ubuntu Server 24.04 LTS. It details hardware specs, service inventory, network architecture, resource limits, and maintenance procedures, including setup guides for Ubuntu, Docker, storage, VPN, and per-service configuration. The system emphasizes secure remote access, robust monitoring, and modular deployment for media, analytics, cloud, and infrastructure services.

## Key Points

- Docker Compose orchestration for a multi-service home server on Ubuntu 24.04 LTS
- Secure remote access via Cloudflare Tunnel and Tailscale VPN, with LAN routing managed by AdGuard DNS rewrites
- Detailed service inventory, resource limits, monitoring (Grafana, Uptime Kuma), and maintenance guides for resilient operation

## Concepts Extracted

- **Homelab Server Deployment Architecture** — Homelab Server Deployment Architecture refers to the integrated design and orchestration of multiple services on a home server, leveraging Docker Compose, secure networking, and resource management to deliver robust, modular infrastructure. This architecture is tailored for the Beelink GTi13 Ultra running Ubuntu Server 24.04 LTS, emphasizing security, scalability, and maintainability for media, analytics, cloud, and infrastructure workloads.
- **[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]** — Split-DNS Routing and Cloudflare Tunnel Overrides are network strategies used to securely and efficiently route traffic to homelab services, distinguishing between LAN and remote access. AdGuard DNS rewrites direct LAN traffic to the server's local IP, while Cloudflare Tunnel handles public access, terminating TLS and tunneling requests without exposing ports or public IPs.
- **[[Comprehensive Grafana Monitoring for Docker Homelab Services]]** — Comprehensive Grafana Monitoring for Docker Homelab Services involves provisioning dashboards and data sources to track host and container resource usage, service health, and network metrics. This approach leverages automated config-based provisioning, integrating Prometheus, cAdvisor, and Node Exporter to deliver real-time, actionable insights for homelab infrastructure.

## Entities Mentioned

- **[[Homelab]]** — Homelab is a Docker Compose-based infrastructure project designed for the Beelink GTi13 Ultra home server running Ubuntu Server 24.04 LTS. It orchestrates a wide range of services, including media streaming, analytics, cloud storage, password management, monitoring, and knowledge capture, with a strong emphasis on secure networking, resource management, and modular deployment.

## Notable Quotes

> "Remote access is provided via Cloudflare Tunnel — no ports forwarded, no public IP exposed." — README
> "All containers have CPU and memory limits configured via deploy.resources.limits to prevent runaway processes from starving the host." — README
> "Grafana dashboards and datasources are provisioned from config files — no manual import needed after deployment." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-jbl306homelab.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/jbl306/homelab |
