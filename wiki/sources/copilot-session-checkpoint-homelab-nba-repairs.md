---
title: "Copilot Session Checkpoint: Homelab NBA repairs"
type: source
created: '2026-05-18'
last_verified: '2026-05-18'
source_hash: "f1615c76dd0a7e0be29992b380c486942c47624fcf57a9e648a03b30912314f7"
sources:
  - raw/2026-05-18-copilot-session-homelab-nba-repairs-e405020e.md
concepts:
  - trusted-domain-scope-reverse-proxied-nextcloud-checks
  - task-specific-feature-profiles-memory-bounded-ml-training
  - oom-failure-diagnosis-remediation-ml-containers
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
  - "[[Nextcloud]]"
  - "[[NBA ML Engine]]"
  - "[[Spatial Design Studio]]"
  - "[[Task Observer]]"
  - "[[Configuration Scope vs Workload Shaping in Homelab Repairs]]"
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
tags: [copilot-session, checkpoint, durable-debugging, homelab, nextcloud, nba-ml-engine, ml-ops, spatial-design-studio]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: Homelab NBA repairs

## Summary

This checkpoint captures a three-part repair session across the [[Homelab]]: decommissioning [[Spatial Design Studio]], fixing a broken [[Nextcloud]] deployment, and recovering a failing [[NBA ML Engine]] weekly training path. The durable lesson is that each incident was resolved by tightening scope at the right layer: remove stale service surfaces, narrow trusted domains to the canonical hostname, and constrain the minutes model to a task-specific feature profile instead of letting it inherit the full training workload.

## Key Points

- The session explicitly followed [[Task Observer]] plus the workspace debugging and deployment workflows before making runtime or code changes, treating the checkpoint as a durable operational artifact rather than an ad hoc shell transcript.
- [[Spatial Design Studio]] was removed end-to-end from the homelab surface area: `compose/compose.web.yml`, `.env.example`, Homepage services, AdGuard DNS rewrites, README/service docs, setup/deploy scripts, and the live `spatial-design-studio-*` containers.
- The initial [[Nextcloud]] failure signature was misleading: `config.php` was unreadable inside `nextcloud:29-apache`, which produced `Permission denied`, "Configuration was not read or initialized correctly", and SQLite-looking fallback errors even though the real problem was mount ownership.
- The root cause of the Nextcloud incident was a UID/GID mismatch between host-owned mounts (`1000:1000`) and the container's `www-data` user (`33:33`) combined with `config.php` mode `640`; fixing ownership and preserving it in setup scripts restored normal config reads and writes.
- Nextcloud hardening went beyond file permissions: the session added `TRUSTED_PROXIES=172.20.1.0/24`, `OVERWRITEHOST=cloud.${DOMAIN}`, an HSTS Caddy label, moved the data mount to `/var/www/data`, and applied persistent `occ` settings for proxy headers, CLI URL, cron jobs, and maintenance windows.
- The lingering Nextcloud "Data directory protected" warning turned out to be a trusted-domain scope bug: because `trusted_domains` included `192.168.1.238`, setup checks probed the LAN IP, hit Caddy's wildcard route, and received `HTTP 200` for `/var/www/data/.ocdata`; narrowing the trusted domain set to `cloud.jbl-lab.com` removed the false positive.
- The [[NBA ML Engine]] failure was traced to a real cgroup OOM on the minutes stage: `train-minutes` exited `-9`, Docker reported `OOMKilled=true`, and `memory.events` recorded `oom_kill 4`, while the live scheduler image was also stale and still running the older weekly command.
- The code fix introduced `feature_profile="minutes"` in `src/features/builder.py` and updated `train_minutes_model()` to request that profile together with `predicted_minutes_mode="disabled"`, skipping expensive high-memory feature sources that are irrelevant to minutes prediction.
- The regression work was done with tests first, then validated with a focused suite of **53 passing tests** after repairing stale monkeypatches and import patterns in the guardrail tests.
- The live result after redeploy was concrete: `docker exec nba-ml-api python main.py train-minutes` completed in about **48s**, built a **158353 x 262** matrix, used **34 / 231** minutes features, and reported **`val_r2=0.55946`** without another OOM.

## Key Concepts

- [[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]]
- [[Task-Specific Feature Profiles for Memory-Bounded ML Training]]
- [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]
- [[Configuration Scope vs Workload Shaping in Homelab Repairs]]

## Related Entities

- **[[Homelab]]** — The shared Docker Compose environment where service removal, Nextcloud repair, and NBA redeploy all had to remain operationally consistent.
- **[[Nextcloud]]** — The self-hosted cloud service whose config mounts, trusted domains, and reverse-proxy behavior were corrected.
- **[[NBA ML Engine]]** — The ML system whose minutes-model workload was reshaped to avoid repeat OOM failures.
- **[[Spatial Design Studio]]** — The service that was intentionally removed from compose, DNS, docs, and runtime.
- **[[Task Observer]]** — The meta-skill that framed the session as a workflow-driven debugging and deployment exercise.

