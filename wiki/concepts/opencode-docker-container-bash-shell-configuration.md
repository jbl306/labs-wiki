---
title: "Opencode Docker Container Bash Shell Configuration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "62a3c4ffbf12d604468b3d8046bc22088aed94feabac8006f2b13c5583c1d345"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-knightcrawler-gating-fix-opencode-bash-config-b0a35301.md
quality_score: 69
concepts:
  - opencode-docker-container-bash-shell-configuration
related:
  - "[[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]]"
tier: hot
tags: [opencode, docker, bash, container-configuration, network-binding]
---

# Opencode Docker Container Bash Shell Configuration

## Overview

This concept describes the configuration of opencode and giniecode Docker containers to use the explicit bash shell path `/usr/bin/bash` by setting environment variables and updating Dockerfiles. It also covers the discovery that opencode's serve command ignores config file server settings for hostname and port, requiring CLI flags for proper network binding.

## How It Works

Opencode containers by default resolve the shell path by first checking the `SHELL` environment variable. If `SHELL` is unset, the code falls back to running `which bash` on Linux to find the shell executable. In the original container images, `SHELL` was not set, causing potential ambiguity or reliance on default shell paths.

To enforce consistent usage of `/usr/bin/bash` (preferred over `/bin/bash` despite both being symlinks on Ubuntu 24.04), the following steps were taken:

1. Added `ENV SHELL=/usr/bin/bash` to both the `opencode/Dockerfile` and `giniecode/Dockerfile`.
2. Updated the `useradd` command in the giniecode Dockerfile to set the user's login shell to `/usr/bin/bash`.
3. Created git-tracked configuration files (`opencode.json`) with recommended defaults including permissions, autoupdate settings, and user-specific configurations.
4. Updated the Docker Compose file to pass the `SHELL` environment variable and mount the configuration files inside the containers.

During testing, it was discovered that the `opencode serve` command does not honor the `server.hostname` and `server.port` settings from the config file or environment variable `OPENCODE_CONFIG`. Instead, it requires explicit CLI flags `--hostname` and `--port` to bind to the desired network interface and port. Without these flags, the server binds to `127.0.0.1` by default, making it unreachable via the Caddy proxy.

Therefore, the CLI flags were restored in the compose command line to ensure the containers are accessible externally.

This configuration ensures consistent shell usage inside containers, reliable application of recommended defaults, and proper network accessibility for the opencode services.

## Key Properties

- **Shell Resolution Order:** Opencode checks `process.env.SHELL` first, then falls back to `which bash`.
- **Config File Precedence:** Config precedence is Remote → Global → Custom (OPENCODE_CONFIG env) → Project → .opencode dirs → Inline, but `serve` ignores server hostname/port in config.
- **CLI Flags Required for Serve:** `opencode serve` requires `--hostname` and `--port` CLI flags to override default binding.

## Limitations

The need to specify CLI flags for hostname and port when running `opencode serve` indicates a limitation or bug in the config file handling. This complicates deployment automation and requires careful compose file management. Also, setting the shell path explicitly assumes the target system uses the same path conventions, which may reduce portability.

## Example

Dockerfile snippet:
```Dockerfile
ENV SHELL=/usr/bin/bash
RUN useradd -m -s /usr/bin/bash ginie
```

Docker Compose snippet:
```yaml
services:
  opencode:
    environment:
      - SHELL=/usr/bin/bash
      - OPENCODE_CONFIG=/etc/opencode/opencode.json
    command: opencode serve --hostname 0.0.0.0 --port 4096
    volumes:
      - ./config/opencode/opencode.json:/etc/opencode/opencode.json:ro
```


## Relationship to Other Concepts

- **Docker Compose Environment Variable Management** — Demonstrates environment variable injection into containers.
- **Container Network Binding and Port Exposure** — Explains how CLI flags affect container network accessibility.

## Practical Applications

This configuration approach is critical when deploying opencode or similar containerized services that rely on shell environment consistency and require explicit network binding for external access. It ensures reliable operation in homelab or production environments behind reverse proxies.

## Sources

- [[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]] — primary source for this concept
