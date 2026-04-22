---
title: "Dedupe Candidates Audit"
type: report
generated: 2026-04-21
scope: "wiki/concepts/ + wiki/entities/ semantic clustering"
threshold: 0.85
method: rapidfuzz token_set_ratio (fallback)
---

# Dedupe Candidates Audit

Scanned **507** pages (concepts + entities). Embedding method: **rapidfuzz token_set_ratio (fallback)**. Cosine threshold: **0.85** (rapidfuzz uses scaled token_set_ratio when sentence-transformers is unavailable).

Found **49** merge cluster(s) covering **164** pages.

> This is a **read-only audit**. No pages were modified.

## Cluster 1 (28 pages)

**Pages:**

-    `wiki/concepts/comparison-mempalace-labs-wiki-openmemory.md` — *Comparison of MemPalace, Labs-Wiki, and OpenMemory* (last_verified: 2026-04-18)
-    `wiki/concepts/comprehensive-grafana-monitoring-for-docker-homelab-services.md` — *Comprehensive Grafana Monitoring for Docker Homelab Services* (last_verified: 2026-04-18)
-    `wiki/concepts/copilot-cli-opencode-integration-with-mempalace.md` — *Copilot CLI and OpenCode Integration with MemPalace* (last_verified: 2026-04-18)
-    `wiki/concepts/custom-copilot-cli-agents.md` — *Custom Copilot CLI Agents* (last_verified: 2026-04-18)
-    `wiki/concepts/docker-container-resource-auditing-and-optimization.md` — *Docker Container Resource Auditing and Optimization* (last_verified: 2026-04-18)
-    `wiki/concepts/homelab-cron-job-integration-throttled-ingestion.md` — *Homelab Cron-Job Integration for Throttled Ingestion* (last_verified: 2026-04-21)
-    `wiki/concepts/homelab-infrastructure-patterns-for-ai-memory-migration.md` — *Homelab Infrastructure Patterns for AI Memory Migration* (last_verified: 2026-04-18)
-    `wiki/concepts/homelab-media-domain-routing-lan-public-https-diagnostics.md` — *Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics* (last_verified: 2026-04-18)
-    `wiki/concepts/homelab-server-deployment-nba-ml-platform.md` — *Homelab Server Deployment Architecture for NBA ML Platform* (last_verified: 2026-04-18)
-    `wiki/concepts/homelab-service-inventory-and-dashboard-synchronization.md` — *Homelab Service Inventory And Dashboard Synchronization* (last_verified: 2026-04-18)
-    `wiki/concepts/mempalace-architecture-and-migration.md` — *MemPalace Architecture and Migration* (last_verified: 2026-04-18)
-    `wiki/concepts/mempalace-control-protocol-mcp-integration.md` — *MemPalace Control Protocol (MCP) Integration* (last_verified: 2026-04-18)
-    `wiki/concepts/mempalace-memory-system.md` — *MemPalace Memory System* (last_verified: 2026-04-18)
-    `wiki/concepts/mempalace-phase-3-4-features-and-implementation.md` — *MemPalace Phase 3-4 Features and Implementation* (last_verified: 2026-04-18)
-    `wiki/concepts/mempalace-timeout-database-lock-remediation.md` — *MemPalace Timeout and Database Lock Remediation* (last_verified: 2026-04-18)
-    `wiki/concepts/migration-from-openmemory-to-mempalace.md` — *Migration from OpenMemory to MemPalace* (last_verified: 2026-04-18)
-    `wiki/concepts/opencode-bash-shell-configuration-posix-spawn-enoent-fix.md` — *OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix* (last_verified: 2026-04-18)
-    `wiki/concepts/opencode-docker-container-bash-shell-configuration.md` — *Opencode Docker Container Bash Shell Configuration* (last_verified: 2026-04-18)
-    `wiki/concepts/openmemory-mcp-integration-with-copilot-cli.md` — *OpenMemory MCP Integration with Copilot CLI* (last_verified: 2026-04-18)
-    `wiki/concepts/orphan-pruning-mempalace-sync-scripts.md` — *Orphan Pruning in MemPalace Sync Scripts* (last_verified: 2026-04-20)
-    `wiki/concepts/split-dns-routing-cloudflare-tunnel-overrides-homelab-services.md` — *Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services* (last_verified: 2026-04-20)
-    `wiki/entities/cloudflare.md` — *Cloudflare* (last_verified: 2026-04-18)
-    `wiki/entities/copilot-cli.md` — *Copilot CLI* (last_verified: 2026-04-18)
-    `wiki/entities/docker.md` — *Docker* (last_verified: 2026-04-18)
-    `wiki/entities/homelab.md` — *Homelab* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/mempalace.md` — *MemPalace* (last_verified: 2026-04-11)
-    `wiki/entities/opencode.md` — *OpenCode* (last_verified: 2026-04-18)
-    `wiki/entities/openmemory.md` — *OpenMemory* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `comparison-mempalace-labs-wiki-openmemory` | `openmemory` | 1.000 |
| `comprehensive-grafana-monitoring-for-docker-homelab-services` | `docker` | 1.000 |
| `comprehensive-grafana-monitoring-for-docker-homelab-services` | `homelab` | 1.000 |
| `copilot-cli-opencode-integration-with-mempalace` | `copilot-cli` | 1.000 |
| `copilot-cli-opencode-integration-with-mempalace` | `mempalace` | 1.000 |
| `copilot-cli-opencode-integration-with-mempalace` | `opencode` | 1.000 |
| `custom-copilot-cli-agents` | `copilot-cli` | 1.000 |
| `docker-container-resource-auditing-and-optimization` | `docker` | 1.000 |
| `homelab-cron-job-integration-throttled-ingestion` | `homelab` | 1.000 |
| `homelab-infrastructure-patterns-for-ai-memory-migration` | `homelab` | 1.000 |
| `homelab-media-domain-routing-lan-public-https-diagnostics` | `homelab` | 1.000 |
| `homelab-server-deployment-nba-ml-platform` | `homelab` | 1.000 |
| `homelab-service-inventory-and-dashboard-synchronization` | `homelab` | 1.000 |
| `mempalace-architecture-and-migration` | `mempalace` | 1.000 |
| `mempalace-control-protocol-mcp-integration` | `mempalace` | 1.000 |
| `mempalace-memory-system` | `mempalace` | 1.000 |
| `mempalace-phase-3-4-features-and-implementation` | `mempalace` | 1.000 |
| `mempalace-timeout-database-lock-remediation` | `mempalace` | 1.000 |
| `migration-from-openmemory-to-mempalace` | `mempalace` | 1.000 |
| `migration-from-openmemory-to-mempalace` | `openmemory` | 1.000 |
| `opencode-bash-shell-configuration-posix-spawn-enoent-fix` | `opencode` | 1.000 |
| `opencode-docker-container-bash-shell-configuration` | `docker` | 1.000 |
| `opencode-docker-container-bash-shell-configuration` | `opencode` | 1.000 |
| `openmemory-mcp-integration-with-copilot-cli` | `copilot-cli` | 1.000 |
| `openmemory-mcp-integration-with-copilot-cli` | `openmemory` | 1.000 |
| `orphan-pruning-mempalace-sync-scripts` | `mempalace` | 1.000 |
| `split-dns-routing-cloudflare-tunnel-overrides-homelab-services` | `cloudflare` | 1.000 |
| `split-dns-routing-cloudflare-tunnel-overrides-homelab-services` | `homelab` | 1.000 |

**Recommended winner:** `wiki/entities/mempalace.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Comparison of MemPalace, Labs-Wiki, and OpenMemory", "Comprehensive Grafana Monitoring for Docker Homelab Services", "Copilot CLI and OpenCode Integration with MemPalace", "Custom Copilot CLI Agents", "Docker Container Resource Auditing and Optimization", "Homelab Cron-Job Integration for Throttled Ingestion", "Homelab Infrastructure Patterns for AI Memory Migration", "Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics", "Homelab Server Deployment Architecture for NBA ML Platform", "Homelab Service Inventory And Dashboard Synchronization", "MemPalace Architecture and Migration", "MemPalace Control Protocol (MCP) Integration", "MemPalace Memory System", "MemPalace Phase 3-4 Features and Implementation", "MemPalace Timeout and Database Lock Remediation", "Migration from OpenMemory to MemPalace", "OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix", "Opencode Docker Container Bash Shell Configuration", "OpenMemory MCP Integration with Copilot CLI", "Orphan Pruning in MemPalace Sync Scripts", "Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services", "Cloudflare", "Copilot CLI", "Docker", "Homelab", "OpenCode", "OpenMemory" into `wiki/entities/mempalace.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 2 (8 pages)

**Pages:**

-    `wiki/concepts/batch-prediction-optimization-nba-ml-engine.md` — *Batch Prediction Optimization in NBA ML Engine* (last_verified: 2026-04-18)
-    `wiki/concepts/feature-engineering-nba-ml-engine-sprint-10.md` — *Feature Engineering for NBA ML Engine Sprint 10* (last_verified: 2026-04-18)
-    `wiki/concepts/lstm-gating-mechanism-nba-ml-engine.md` — *LSTM Gating Mechanism in NBA ML Engine* (last_verified: 2026-04-18)
-    `wiki/concepts/per-stat-model-selection-and-ensemble-learning-nba-ml-engine.md` — *Per-Stat Model Selection and Ensemble Learning in NBA ML Engine* (last_verified: 2026-04-18)
-    `wiki/concepts/shap-analysis-bug-resolution-in-nba-ml-engine.md` — *SHAP Analysis Bug Resolution In NBA ML Engine* (last_verified: 2026-04-18)
-    `wiki/concepts/sprint-12-nba-ml-engine-code-cleanup-feature-tuning.md` — *Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning* (last_verified: 2026-04-18)
-    `wiki/concepts/walk-forward-stability-analysis-backtesting-nba-ml-engine.md` — *Walk-Forward Stability Analysis and Backtesting in NBA ML Engine* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/nba-ml-engine.md` — *NBA ML Engine* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `batch-prediction-optimization-nba-ml-engine` | `nba-ml-engine` | 1.000 |
| `feature-engineering-nba-ml-engine-sprint-10` | `nba-ml-engine` | 1.000 |
| `lstm-gating-mechanism-nba-ml-engine` | `nba-ml-engine` | 1.000 |
| `per-stat-model-selection-and-ensemble-learning-nba-ml-engine` | `nba-ml-engine` | 1.000 |
| `shap-analysis-bug-resolution-in-nba-ml-engine` | `nba-ml-engine` | 1.000 |
| `sprint-12-nba-ml-engine-code-cleanup-feature-tuning` | `nba-ml-engine` | 1.000 |
| `walk-forward-stability-analysis-backtesting-nba-ml-engine` | `nba-ml-engine` | 1.000 |

**Recommended winner:** `wiki/entities/nba-ml-engine.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Batch Prediction Optimization in NBA ML Engine", "Feature Engineering for NBA ML Engine Sprint 10", "LSTM Gating Mechanism in NBA ML Engine", "Per-Stat Model Selection and Ensemble Learning in NBA ML Engine", "SHAP Analysis Bug Resolution In NBA ML Engine", "Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning", "Walk-Forward Stability Analysis and Backtesting in NBA ML Engine" into `wiki/entities/nba-ml-engine.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 3 (7 pages)

**Pages:**

-    `wiki/concepts/claude-code-skill-summarization.md` — *Claude Code Skill Summarization* (last_verified: 2026-04-10)
-    `wiki/concepts/comparative-agent-system-architecture-claude-code-vs-openclaw.md` — *Comparative Agent System Architecture: Claude Code vs. OpenClaw* (last_verified: 2026-04-18)
-    `wiki/concepts/context-management-compaction-pipeline-claude-code.md` — *Context Management and Compaction Pipeline in Claude Code* (last_verified: 2026-04-18)
-    `wiki/concepts/layered-agentic-architecture-claude-code.md` — *Layered Agentic Architecture in Claude Code* (last_verified: 2026-04-18)
-    `wiki/entities/claude-code.md` — *Claude Code* (last_verified: 2026-04-10)
- 🏆 `wiki/entities/claude.md` — *Claude* (last_verified: 2026-04-08)
-    `wiki/entities/openclaw.md` — *OpenClaw* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `claude-code-skill-summarization` | `claude-code` | 1.000 |
| `claude-code-skill-summarization` | `claude` | 1.000 |
| `comparative-agent-system-architecture-claude-code-vs-openclaw` | `claude-code` | 1.000 |
| `comparative-agent-system-architecture-claude-code-vs-openclaw` | `claude` | 1.000 |
| `comparative-agent-system-architecture-claude-code-vs-openclaw` | `openclaw` | 1.000 |
| `context-management-compaction-pipeline-claude-code` | `claude-code` | 1.000 |
| `context-management-compaction-pipeline-claude-code` | `claude` | 1.000 |
| `layered-agentic-architecture-claude-code` | `claude-code` | 1.000 |
| `layered-agentic-architecture-claude-code` | `claude` | 1.000 |
| `claude-code` | `claude` | 1.000 |

**Recommended winner:** `wiki/entities/claude.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Claude Code Skill Summarization", "Comparative Agent System Architecture: Claude Code vs. OpenClaw", "Context Management and Compaction Pipeline in Claude Code", "Layered Agentic Architecture in Claude Code", "Claude Code", "OpenClaw" into `wiki/entities/claude.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 4 (7 pages)

**Pages:**

-    `wiki/concepts/histogram-based-learning-in-lightgbm.md` — *Histogram-Based Learning in LightGBM* (last_verified: 2026-04-08)
-    `wiki/concepts/lightgbm-feature-importance-and-shap-values.md` — *LightGBM Feature Importance and SHAP Values* (last_verified: 2026-04-08)
-    `wiki/concepts/lightgbm-hyperparameter-tuning.md` — *LightGBM Hyperparameter Tuning* (last_verified: 2026-04-20)
-    `wiki/concepts/lightgbm-leaf-wise-tree-growth.md` — *LightGBM Leaf-Wise Tree Growth* (last_verified: 2026-04-08)
-    `wiki/concepts/quantile-crossing-fix-xgboost-lightgbm.md` — *Quantile Crossing Fix in XGBoost and LightGBM Models* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/lightgbm.md` — *LightGBM* (last_verified: 2026-04-08)
-    `wiki/entities/xgboost.md` — *XGBoost* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `histogram-based-learning-in-lightgbm` | `lightgbm` | 1.000 |
| `lightgbm-feature-importance-and-shap-values` | `lightgbm` | 1.000 |
| `lightgbm-hyperparameter-tuning` | `lightgbm` | 1.000 |
| `lightgbm-leaf-wise-tree-growth` | `lightgbm` | 1.000 |
| `quantile-crossing-fix-xgboost-lightgbm` | `lightgbm` | 1.000 |
| `quantile-crossing-fix-xgboost-lightgbm` | `xgboost` | 1.000 |

**Recommended winner:** `wiki/entities/lightgbm.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Histogram-Based Learning in LightGBM", "LightGBM Feature Importance and SHAP Values", "LightGBM Hyperparameter Tuning", "LightGBM Leaf-Wise Tree Growth", "Quantile Crossing Fix in XGBoost and LightGBM Models", "XGBoost" into `wiki/entities/lightgbm.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 5 (6 pages)

**Pages:**

-    `wiki/concepts/concurrent-refresh-postgresql-materialized-views.md` — *Concurrent Refresh of PostgreSQL Materialized Views* (last_verified: 2026-04-18)
-    `wiki/concepts/handling-postgresql-numeric-type-in-nodejs-pg-library.md` — *Handling PostgreSQL NUMERIC Type in Node.js with pg Library* (last_verified: 2026-04-18)
-    `wiki/concepts/postgresql-materialized-views-for-dashboard-optimization.md` — *PostgreSQL Materialized Views for Dashboard Optimization* (last_verified: 2026-04-18)
-    `wiki/concepts/replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data.md` — *Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/fastapi.md` — *FastAPI* (last_verified: 2026-04-18)
-    `wiki/entities/postgresql.md` — *PostgreSQL* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `concurrent-refresh-postgresql-materialized-views` | `postgresql` | 1.000 |
| `handling-postgresql-numeric-type-in-nodejs-pg-library` | `postgresql` | 1.000 |
| `postgresql-materialized-views-for-dashboard-optimization` | `postgresql` | 1.000 |
| `replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data` | `fastapi` | 1.000 |
| `replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data` | `postgresql` | 1.000 |

**Recommended winner:** `wiki/entities/fastapi.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Concurrent Refresh of PostgreSQL Materialized Views", "Handling PostgreSQL NUMERIC Type in Node.js with pg Library", "PostgreSQL Materialized Views for Dashboard Optimization", "Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data", "PostgreSQL" into `wiki/entities/fastapi.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 6 (6 pages)

**Pages:**

-    `wiki/concepts/knightcrawler-cron-automation-monitoring-status-tracking.md` — *Knightcrawler Cron Automation Monitoring and Status Tracking* (last_verified: 2026-04-18)
-    `wiki/concepts/knightcrawler-gating-fix-for-stremio-streams.md` — *KnightCrawler Gating Fix for Stremio Streams* (last_verified: 2026-04-18)
-    `wiki/concepts/knightcrawler-metadata-service-imdb-data-refresh.md` — *Knightcrawler Metadata Service and IMDB Data Refresh* (last_verified: 2026-04-18)
-    `wiki/concepts/knightcrawler-permission-issue-and-cron-job-management.md` — *KnightCrawler Permission Issue and Cron Job Management* (last_verified: 2026-04-18)
-    `wiki/concepts/knightcrawler-populate-files-cron-job.md` — *Knightcrawler Populate Files Cron Job* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/knightcrawler.md` — *KnightCrawler* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `knightcrawler-cron-automation-monitoring-status-tracking` | `knightcrawler` | 1.000 |
| `knightcrawler-gating-fix-for-stremio-streams` | `knightcrawler` | 1.000 |
| `knightcrawler-metadata-service-imdb-data-refresh` | `knightcrawler` | 1.000 |
| `knightcrawler-permission-issue-and-cron-job-management` | `knightcrawler` | 1.000 |
| `knightcrawler-populate-files-cron-job` | `knightcrawler` | 1.000 |

**Recommended winner:** `wiki/entities/knightcrawler.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Knightcrawler Cron Automation Monitoring and Status Tracking", "KnightCrawler Gating Fix for Stremio Streams", "Knightcrawler Metadata Service and IMDB Data Refresh", "KnightCrawler Permission Issue and Cron Job Management", "Knightcrawler Populate Files Cron Job" into `wiki/entities/knightcrawler.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 7 (5 pages)

**Pages:**

-    `wiki/concepts/labs-wiki-architecture-and-implementation.md` — *Labs-Wiki Architecture and Implementation* (last_verified: 2026-04-18)
-    `wiki/concepts/labs-wiki-architecture.md` — *Labs-Wiki Architecture* (last_verified: 2026-04-18)
-    `wiki/concepts/multi-device-ingestion-api-for-labs-wiki.md` — *Multi-Device Ingestion API for Labs-Wiki* (last_verified: 2026-04-18)
-    `wiki/entities/labs-wiki-ingest-api.md` — *Labs-Wiki Ingest API* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/labs-wiki.md` — *Labs-Wiki* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `labs-wiki-architecture-and-implementation` | `labs-wiki-architecture` | 1.000 |
| `labs-wiki-architecture-and-implementation` | `labs-wiki` | 1.000 |
| `labs-wiki-architecture` | `labs-wiki` | 1.000 |
| `multi-device-ingestion-api-for-labs-wiki` | `labs-wiki` | 1.000 |
| `labs-wiki-ingest-api` | `labs-wiki` | 1.000 |

**Recommended winner:** `wiki/entities/labs-wiki.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Labs-Wiki Architecture and Implementation", "Labs-Wiki Architecture", "Multi-Device Ingestion API for Labs-Wiki", "Labs-Wiki Ingest API" into `wiki/entities/labs-wiki.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 8 (4 pages)

**Pages:**

-    `wiki/concepts/agent-memory-ingestion-pipeline.md` — *Agent Memory Ingestion Pipeline* (last_verified: 2026-04-20)
-    `wiki/concepts/agent-memory-retrieval-pipeline.md` — *Agent Memory Retrieval Pipeline* (last_verified: 2026-04-20)
- 🏆 `wiki/concepts/hybrid-retrieval-agent-memory-systems.md` — *Hybrid Retrieval in Agent Memory Systems* (last_verified: 2026-04-18)
-    `wiki/entities/agent-memory.md` — *Agent Memory* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `agent-memory-ingestion-pipeline` | `agent-memory` | 1.000 |
| `agent-memory-retrieval-pipeline` | `agent-memory` | 1.000 |
| `hybrid-retrieval-agent-memory-systems` | `agent-memory` | 1.000 |

**Recommended winner:** `wiki/concepts/hybrid-retrieval-agent-memory-systems.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Agent Memory Ingestion Pipeline", "Agent Memory Retrieval Pipeline", "Agent Memory" into `wiki/concepts/hybrid-retrieval-agent-memory-systems.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 9 (4 pages)

**Pages:**

-    `wiki/concepts/backfill-script-copilot-session-checkpoint-curation.md` — *Backfill Script for Copilot Session Checkpoint Curation* (last_verified: 2026-04-20)
-    `wiki/concepts/durable-copilot-session-checkpoint-promotion.md` — *Durable Copilot Session Checkpoint Promotion* (last_verified: 2026-04-18)
-    `wiki/entities/backfill-checkpoint-curation-script.md` — *Backfill Checkpoint Curation Script* (last_verified: 2026-04-20)
- 🏆 `wiki/entities/durable-copilot-session-checkpoint.md` — *Durable Copilot Session Checkpoint* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `backfill-script-copilot-session-checkpoint-curation` | `backfill-checkpoint-curation-script` | 1.000 |
| `backfill-script-copilot-session-checkpoint-curation` | `durable-copilot-session-checkpoint` | 0.867 |
| `durable-copilot-session-checkpoint-promotion` | `durable-copilot-session-checkpoint` | 1.000 |

**Recommended winner:** `wiki/entities/durable-copilot-session-checkpoint.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Backfill Script for Copilot Session Checkpoint Curation", "Durable Copilot Session Checkpoint Promotion", "Backfill Checkpoint Curation Script" into `wiki/entities/durable-copilot-session-checkpoint.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 10 (4 pages)

**Pages:**

-    `wiki/concepts/chrome-devtools-mcp-cli-interface.md` — *Chrome DevTools MCP CLI Interface* (last_verified: 2026-04-13)
-    `wiki/concepts/model-context-protocol-mcp-server-for-chrome-devtools.md` — *Model-Context-Protocol (MCP) Server for Chrome DevTools* (last_verified: 2026-04-13)
-    `wiki/entities/chrome-devtools-mcp.md` — *Chrome DevTools MCP* (last_verified: 2026-04-13)
- 🏆 `wiki/entities/chrome-devtools.md` — *Chrome DevTools* (last_verified: 2026-04-13)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `chrome-devtools-mcp-cli-interface` | `chrome-devtools-mcp` | 1.000 |
| `chrome-devtools-mcp-cli-interface` | `chrome-devtools` | 1.000 |
| `model-context-protocol-mcp-server-for-chrome-devtools` | `chrome-devtools-mcp` | 0.882 |
| `model-context-protocol-mcp-server-for-chrome-devtools` | `chrome-devtools` | 1.000 |
| `chrome-devtools-mcp` | `chrome-devtools` | 1.000 |

**Recommended winner:** `wiki/entities/chrome-devtools.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Chrome DevTools MCP CLI Interface", "Model-Context-Protocol (MCP) Server for Chrome DevTools", "Chrome DevTools MCP" into `wiki/entities/chrome-devtools.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 11 (3 pages)

**Pages:**

-    `wiki/concepts/adaboost-adaptive-boosting.md` — *AdaBoost (Adaptive Boosting)* (last_verified: 2026-04-08)
- 🏆 `wiki/concepts/adaboost-algorithm.md` — *AdaBoost Algorithm* (last_verified: 2026-04-08)
-    `wiki/entities/adaboost.md` — *AdaBoost* (last_verified: 2026-04-21)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `adaboost-adaptive-boosting` | `adaboost` | 1.000 |
| `adaboost-algorithm` | `adaboost` | 1.000 |

**Recommended winner:** `wiki/concepts/adaboost-algorithm.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "AdaBoost (Adaptive Boosting)", "AdaBoost" into `wiki/concepts/adaboost-algorithm.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 12 (3 pages)

**Pages:**

-    `wiki/concepts/attention-mechanism-in-large-language-models.md` — *Attention Mechanism in Large Language Models* (last_verified: 2026-04-13)
- 🏆 `wiki/concepts/flash-attention-in-large-language-models.md` — *Flash Attention in Large Language Models* (last_verified: 2026-04-13)
-    `wiki/concepts/kv-cache-and-paged-attention-in-large-language-models.md` — *KV Cache and Paged Attention in Large Language Models* (last_verified: 2026-04-13)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `attention-mechanism-in-large-language-models` | `flash-attention-in-large-language-models` | 0.919 |
| `attention-mechanism-in-large-language-models` | `kv-cache-and-paged-attention-in-large-language-models` | 0.872 |
| `flash-attention-in-large-language-models` | `kv-cache-and-paged-attention-in-large-language-models` | 0.919 |

**Recommended winner:** `wiki/concepts/flash-attention-in-large-language-models.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Attention Mechanism in Large Language Models", "KV Cache and Paged Attention in Large Language Models" into `wiki/concepts/flash-attention-in-large-language-models.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 13 (3 pages)

**Pages:**

-    `wiki/concepts/autoagent-framework-research-integration-planning.md` — *AutoAgent Framework Research and Integration Planning* (last_verified: 2026-04-18)
-    `wiki/concepts/autoagent-framework-research.md` — *AutoAgent Framework Research* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/autoagent.md` — *AutoAgent* (last_verified: 2026-04-12)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `autoagent-framework-research-integration-planning` | `autoagent-framework-research` | 1.000 |
| `autoagent-framework-research-integration-planning` | `autoagent` | 1.000 |
| `autoagent-framework-research` | `autoagent` | 1.000 |

**Recommended winner:** `wiki/entities/autoagent.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "AutoAgent Framework Research and Integration Planning", "AutoAgent Framework Research" into `wiki/entities/autoagent.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 14 (3 pages)

**Pages:**

-    `wiki/concepts/caddy-handle-path-directive-and-its-impact-on-upstream-url-construction.md` — *Caddy handle_path Directive and Its Impact on Upstream URL Construction* (last_verified: 2026-04-18)
-    `wiki/concepts/caddy-handle-path-directive-and-url-token-injection.md` — *Caddy handle_path Directive and URL Token Injection* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/caddy.md` — *Caddy* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `caddy-handle-path-directive-and-its-impact-on-upstream-url-construction` | `caddy` | 1.000 |
| `caddy-handle-path-directive-and-url-token-injection` | `caddy` | 1.000 |

**Recommended winner:** `wiki/entities/caddy.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Caddy handle_path Directive and Its Impact on Upstream URL Construction", "Caddy handle_path Directive and URL Token Injection" into `wiki/entities/caddy.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 15 (3 pages)

**Pages:**

- 🏆 `wiki/concepts/gradient-descent-in-linear-regression.md` — *Gradient Descent in Linear Regression* (last_verified: 2026-04-08)
-    `wiki/concepts/linear-regression.md` — *Linear Regression* (last_verified: 2026-04-17)
-    `wiki/concepts/regularization-techniques-in-linear-regression.md` — *Regularization Techniques in Linear Regression* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `gradient-descent-in-linear-regression` | `linear-regression` | 1.000 |
| `linear-regression` | `regularization-techniques-in-linear-regression` | 1.000 |

**Recommended winner:** `wiki/concepts/gradient-descent-in-linear-regression.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Linear Regression", "Regularization Techniques in Linear Regression" into `wiki/concepts/gradient-descent-in-linear-regression.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 16 (3 pages)

**Pages:**

-    `wiki/concepts/html-over-the-wire-with-htmx.md` — *HTML Over The Wire With htmx* (last_verified: 2026-04-08)
-    `wiki/concepts/htmx-attribute-api.md` — *htmx Attribute API* (last_verified: 2026-04-08)
- 🏆 `wiki/entities/htmx.md` — *htmx* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `html-over-the-wire-with-htmx` | `htmx` | 1.000 |
| `htmx-attribute-api` | `htmx` | 1.000 |

**Recommended winner:** `wiki/entities/htmx.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "HTML Over The Wire With htmx", "htmx Attribute API" into `wiki/entities/htmx.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 17 (3 pages)

**Pages:**

-    `wiki/concepts/latent-planning-leworldmodel.md` — *Latent Planning with LeWorldModel* (last_verified: 2026-04-20)
-    `wiki/concepts/leworldmodel-architecture.md` — *LeWorldModel Architecture* (last_verified: 2026-04-20)
- 🏆 `wiki/entities/leworldmodel.md` — *LeWorldModel* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `latent-planning-leworldmodel` | `leworldmodel` | 1.000 |
| `leworldmodel-architecture` | `leworldmodel` | 1.000 |

**Recommended winner:** `wiki/entities/leworldmodel.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Latent Planning with LeWorldModel", "LeWorldModel Architecture" into `wiki/entities/leworldmodel.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 18 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/aaak-compression-dialect.md` — *AAAK Compression Dialect* (last_verified: 2026-04-11)
-    `wiki/entities/aaak-compression-dialect.md` — *AAAK Compression Dialect* (last_verified: 2026-04-11)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `aaak-compression-dialect` | `aaak-compression-dialect` | 1.000 |

**Recommended winner:** `wiki/concepts/aaak-compression-dialect.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "AAAK Compression Dialect" into `wiki/concepts/aaak-compression-dialect.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 19 (2 pages)

**Pages:**

-    `wiki/concepts/adguard-memory-oom-diagnosis-and-fix.md` — *AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/adguard.md` — *AdGuard* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `adguard-memory-oom-diagnosis-and-fix` | `adguard` | 1.000 |

**Recommended winner:** `wiki/entities/adguard.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix" into `wiki/entities/adguard.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 20 (2 pages)

**Pages:**

-    `wiki/concepts/agent-ergonomic-tool-design-principles.md` — *Agent-Ergonomic Tool Design Principles* (last_verified: 2026-04-13)
- 🏆 `wiki/concepts/axi-design-principles-for-agent-ergonomic-cli-tools.md` — *AXI Design Principles for Agent-Ergonomic CLI Tools* (last_verified: 2026-04-10)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `agent-ergonomic-tool-design-principles` | `axi-design-principles-for-agent-ergonomic-cli-tools` | 0.930 |

**Recommended winner:** `wiki/concepts/axi-design-principles-for-agent-ergonomic-cli-tools.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Agent-Ergonomic Tool Design Principles" into `wiki/concepts/axi-design-principles-for-agent-ergonomic-cli-tools.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 21 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/agentic-context-engineering-ace.md` — *Agentic Context Engineering (ACE)* (last_verified: 2026-04-16)
-    `wiki/entities/agentic-context-engineering-ace.md` — *Agentic Context Engineering (ACE)* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `agentic-context-engineering-ace` | `agentic-context-engineering-ace` | 1.000 |

**Recommended winner:** `wiki/concepts/agentic-context-engineering-ace.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Agentic Context Engineering (ACE)" into `wiki/concepts/agentic-context-engineering-ace.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 22 (2 pages)

**Pages:**

-    `wiki/concepts/autoreason-iterative-self-refinement-framework.md` — *Autoreason Iterative Self-Refinement Framework* (last_verified: 2026-04-13)
- 🏆 `wiki/entities/autoreason.md` — *Autoreason* (last_verified: 2026-04-13)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `autoreason-iterative-self-refinement-framework` | `autoreason` | 1.000 |

**Recommended winner:** `wiki/entities/autoreason.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Autoreason Iterative Self-Refinement Framework" into `wiki/entities/autoreason.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 23 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/code-mode-mcp-server.md` — *Code Mode MCP Server* (last_verified: 2026-04-20)
-    `wiki/entities/code-mode-mcp-server.md` — *Code Mode MCP Server* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `code-mode-mcp-server` | `code-mode-mcp-server` | 1.000 |

**Recommended winner:** `wiki/concepts/code-mode-mcp-server.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Code Mode MCP Server" into `wiki/concepts/code-mode-mcp-server.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 24 (2 pages)

**Pages:**

-    `wiki/concepts/edge-threshold-optimizer-kelly-criterion.md` — *Edge Threshold Optimizer Using Kelly Criterion* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/edge-optimizer.md` — *Edge Optimizer* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `edge-threshold-optimizer-kelly-criterion` | `edge-optimizer` | 1.000 |

**Recommended winner:** `wiki/entities/edge-optimizer.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Edge Threshold Optimizer Using Kelly Criterion" into `wiki/entities/edge-optimizer.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 25 (2 pages)

**Pages:**

-    `wiki/concepts/ensemblemodel-stacking-meta-learner.md` — *EnsembleModel Stacking Meta-Learner* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/ensemblemodel.md` — *EnsembleModel* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `ensemblemodel-stacking-meta-learner` | `ensemblemodel` | 1.000 |

**Recommended winner:** `wiki/entities/ensemblemodel.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "EnsembleModel Stacking Meta-Learner" into `wiki/entities/ensemblemodel.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 26 (2 pages)

**Pages:**

-    `wiki/concepts/hope-architecture.md` — *Hope Architecture* (last_verified: 2026-04-08)
- 🏆 `wiki/entities/hope.md` — *Hope* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `hope-architecture` | `hope` | 1.000 |

**Recommended winner:** `wiki/entities/hope.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Hope Architecture" into `wiki/entities/hope.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 27 (2 pages)

**Pages:**

-    `wiki/concepts/http-shortcuts-android-app-scripting-api-quirks.md` — *HTTP Shortcuts Android App Scripting API Quirks* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/http-shortcuts.md` — *HTTP Shortcuts* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `http-shortcuts-android-app-scripting-api-quirks` | `http-shortcuts` | 1.000 |

**Recommended winner:** `wiki/entities/http-shortcuts.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "HTTP Shortcuts Android App Scripting API Quirks" into `wiki/entities/http-shortcuts.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 28 (2 pages)

**Pages:**

-    `wiki/concepts/intelligent-resource-orchestration-for-llm-agents.md` — *Intelligent Resource Orchestration for LLM Agents* (last_verified: 2026-04-12)
- 🏆 `wiki/concepts/intelligent-resource-orchestration.md` — *Intelligent Resource Orchestration* (last_verified: 2026-04-12)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `intelligent-resource-orchestration-for-llm-agents` | `intelligent-resource-orchestration` | 1.000 |

**Recommended winner:** `wiki/concepts/intelligent-resource-orchestration.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Intelligent Resource Orchestration for LLM Agents" into `wiki/concepts/intelligent-resource-orchestration.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 29 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/llm-operating-system-architecture.md` — *LLM Operating System Architecture* (last_verified: 2026-04-08)
-    `wiki/concepts/llm-wiki-architecture.md` — *LLM Wiki Architecture* (last_verified: 2026-04-17)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `llm-operating-system-architecture` | `llm-wiki-architecture` | 0.865 |

**Recommended winner:** `wiki/concepts/llm-operating-system-architecture.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "LLM Wiki Architecture" into `wiki/concepts/llm-operating-system-architecture.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 30 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/logistic-regression.md` — *Logistic Regression* (last_verified: 2026-04-08)
-    `wiki/concepts/maximum-likelihood-estimation-in-logistic-regression.md` — *Maximum Likelihood Estimation in Logistic Regression* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `logistic-regression` | `maximum-likelihood-estimation-in-logistic-regression` | 1.000 |

**Recommended winner:** `wiki/concepts/logistic-regression.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Maximum Likelihood Estimation in Logistic Regression" into `wiki/concepts/logistic-regression.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 31 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/mast-failure-taxonomy.md` — *MAST Failure Taxonomy* (last_verified: 2026-04-08)
-    `wiki/entities/mast-failure-taxonomy.md` — *MAST Failure Taxonomy* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `mast-failure-taxonomy` | `mast-failure-taxonomy` | 1.000 |

**Recommended winner:** `wiki/concepts/mast-failure-taxonomy.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "MAST Failure Taxonomy" into `wiki/concepts/mast-failure-taxonomy.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 32 (2 pages)

**Pages:**

-    `wiki/concepts/memento-blockwise-summarization-for-llms.md` — *Memento Blockwise Summarization for LLMs* (last_verified: 2026-04-21)
- 🏆 `wiki/entities/memento.md` — *Memento* (last_verified: 2026-04-21)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `memento-blockwise-summarization-for-llms` | `memento` | 1.000 |

**Recommended winner:** `wiki/entities/memento.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Memento Blockwise Summarization for LLMs" into `wiki/entities/memento.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 33 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/natural-language-driven-agent-building.md` — *Natural Language-Driven Agent Building* (last_verified: 2026-04-12)
-    `wiki/concepts/natural-language-driven-agent-creation.md` — *Natural Language-Driven Agent Creation* (last_verified: 2026-04-12)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `natural-language-driven-agent-building` | `natural-language-driven-agent-creation` | 0.866 |

**Recommended winner:** `wiki/concepts/natural-language-driven-agent-building.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Natural Language-Driven Agent Creation" into `wiki/concepts/natural-language-driven-agent-building.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 34 (2 pages)

**Pages:**

-    `wiki/concepts/nodejs-installation-nvm-global-taste-skill-installation.md` — *Node.js Installation via nvm and Global Taste-Skill Package Installation* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/taste-skill-package.md` — *Taste-Skill Package* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `nodejs-installation-nvm-global-taste-skill-installation` | `taste-skill-package` | 1.000 |

**Recommended winner:** `wiki/entities/taste-skill-package.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Node.js Installation via nvm and Global Taste-Skill Package Installation" into `wiki/entities/taste-skill-package.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 35 (2 pages)

**Pages:**

-    `wiki/concepts/ntfy-push-notifications-for-service-monitoring.md` — *Ntfy Push Notifications for Service Monitoring* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/ntfy.md` — *Ntfy* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `ntfy-push-notifications-for-service-monitoring` | `ntfy` | 1.000 |

**Recommended winner:** `wiki/entities/ntfy.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Ntfy Push Notifications for Service Monitoring" into `wiki/entities/ntfy.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 36 (2 pages)

**Pages:**

-    `wiki/concepts/odds-api-quota-optimization.md` — *Odds API Quota Optimization* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/odds-api.md` — *Odds API* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `odds-api-quota-optimization` | `odds-api` | 1.000 |

**Recommended winner:** `wiki/entities/odds-api.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Odds API Quota Optimization" into `wiki/entities/odds-api.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 37 (2 pages)

**Pages:**

-    `wiki/concepts/proxy-pointer-rag-architecture.md` — *Proxy-Pointer RAG Architecture* (last_verified: 2026-04-20)
- 🏆 `wiki/entities/proxy-pointer.md` — *Proxy-Pointer* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `proxy-pointer-rag-architecture` | `proxy-pointer` | 1.000 |

**Recommended winner:** `wiki/entities/proxy-pointer.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Proxy-Pointer RAG Architecture" into `wiki/entities/proxy-pointer.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 38 (2 pages)

**Pages:**

-    `wiki/concepts/react-dashboard-redesign-typescript-tailwindcss.md` — *React Dashboard Redesign with TypeScript and Tailwind CSS* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/tailwind-css-4.md` — *Tailwind CSS 4* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `react-dashboard-redesign-typescript-tailwindcss` | `tailwind-css-4` | 0.923 |

**Recommended winner:** `wiki/entities/tailwind-css-4.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "React Dashboard Redesign with TypeScript and Tailwind CSS" into `wiki/entities/tailwind-css-4.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 39 (2 pages)

**Pages:**

-    `wiki/concepts/refrag-decoding-framework.md` — *REFRAG Decoding Framework* (last_verified: 2026-04-22)
- 🏆 `wiki/entities/refrag.md` — *REFRAG* (last_verified: 2026-04-22)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `refrag-decoding-framework` | `refrag` | 1.000 |

**Recommended winner:** `wiki/entities/refrag.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "REFRAG Decoding Framework" into `wiki/entities/refrag.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 40 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/sketched-isotropic-gaussian-regularizer-sigreg.md` — *Sketched-Isotropic-Gaussian Regularizer (SIGReg)* (last_verified: 2026-04-20)
-    `wiki/entities/sketched-isotropic-gaussian-regularizer-sigreg.md` — *Sketched-Isotropic-Gaussian Regularizer (SIGReg)* (last_verified: 2026-04-20)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `sketched-isotropic-gaussian-regularizer-sigreg` | `sketched-isotropic-gaussian-regularizer-sigreg` | 1.000 |

**Recommended winner:** `wiki/concepts/sketched-isotropic-gaussian-regularizer-sigreg.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Sketched-Isotropic-Gaussian Regularizer (SIGReg)" into `wiki/concepts/sketched-isotropic-gaussian-regularizer-sigreg.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 41 (2 pages)

**Pages:**

-    `wiki/concepts/sportsgameodds-sgo-api-data-extraction-challenges.md` — *SportsGameOdds (SGO) API Data Extraction Challenges* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/sportsgameodds-sgo-api.md` — *SportsGameOdds (SGO) API* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `sportsgameodds-sgo-api-data-extraction-challenges` | `sportsgameodds-sgo-api` | 1.000 |

**Recommended winner:** `wiki/entities/sportsgameodds-sgo-api.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "SportsGameOdds (SGO) API Data Extraction Challenges" into `wiki/entities/sportsgameodds-sgo-api.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 42 (2 pages)

**Pages:**

- 🏆 `wiki/concepts/textual-frequency-paired-dataset.md` — *Textual Frequency Paired Dataset* (last_verified: 2026-04-21)
-    `wiki/entities/textual-frequency-paired-dataset-tfpd.md` — *Textual Frequency Paired Dataset (TFPD)* (last_verified: 2026-04-21)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `textual-frequency-paired-dataset` | `textual-frequency-paired-dataset-tfpd` | 1.000 |

**Recommended winner:** `wiki/concepts/textual-frequency-paired-dataset.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Textual Frequency Paired Dataset (TFPD)" into `wiki/concepts/textual-frequency-paired-dataset.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 43 (2 pages)

**Pages:**

-    `wiki/concepts/timesfm-model-architecture.md` — *TimesFM Model Architecture* (last_verified: 2026-04-21)
- 🏆 `wiki/entities/timesfm.md` — *TimesFM* (last_verified: 2026-04-13)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `timesfm-model-architecture` | `timesfm` | 1.000 |

**Recommended winner:** `wiki/entities/timesfm.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "TimesFM Model Architecture" into `wiki/entities/timesfm.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 44 (2 pages)

**Pages:**

-    `wiki/concepts/toon-token-oriented-object-notation-format.md` — *TOON (Token-Oriented Object Notation) Format* (last_verified: 2026-04-10)
- 🏆 `wiki/entities/toon-token-oriented-object-notation.md` — *TOON (Token-Oriented Object Notation)* (last_verified: 2026-04-10)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `toon-token-oriented-object-notation-format` | `toon-token-oriented-object-notation` | 1.000 |

**Recommended winner:** `wiki/entities/toon-token-oriented-object-notation.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "TOON (Token-Oriented Object Notation) Format" into `wiki/entities/toon-token-oriented-object-notation.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 45 (2 pages)

**Pages:**

-    `wiki/concepts/universal-agent-schema-agents-md-for-ai-tool-integration.md` — *Universal Agent Schema (AGENTS.md) for AI Tool Integration* (last_verified: 2026-04-18)
- 🏆 `wiki/concepts/universal-agent-schema-tool-integration.md` — *Universal Agent Schema and Tool Integration* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `universal-agent-schema-agents-md-for-ai-tool-integration` | `universal-agent-schema-tool-integration` | 0.951 |

**Recommended winner:** `wiki/concepts/universal-agent-schema-tool-integration.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Universal Agent Schema (AGENTS.md) for AI Tool Integration" into `wiki/concepts/universal-agent-schema-tool-integration.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 46 (2 pages)

**Pages:**

-    `wiki/concepts/uptime-kuma-monitor-authentication-and-notification-integration.md` — *Uptime Kuma Monitor Authentication and Notification Integration* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/uptime-kuma.md` — *Uptime Kuma* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `uptime-kuma-monitor-authentication-and-notification-integration` | `uptime-kuma` | 1.000 |

**Recommended winner:** `wiki/entities/uptime-kuma.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Uptime Kuma Monitor Authentication and Notification Integration" into `wiki/entities/uptime-kuma.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 47 (2 pages)

**Pages:**

-    `wiki/concepts/vision-support-in-llm-knowledge-ingestion-using-gpt-4-1.md` — *Vision Support in LLM Knowledge Ingestion Using GPT-4.1* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/gpt-4-1.md` — *GPT-4.1* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `vision-support-in-llm-knowledge-ingestion-using-gpt-4-1` | `gpt-4-1` | 1.000 |

**Recommended winner:** `wiki/entities/gpt-4-1.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Vision Support in LLM Knowledge Ingestion Using GPT-4.1" into `wiki/entities/gpt-4-1.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 48 (2 pages)

**Pages:**

-    `wiki/concepts/warmstarting-hyperparameter-tuning-optuna.md` — *Warmstarting Hyperparameter Tuning with Optuna* (last_verified: 2026-04-18)
- 🏆 `wiki/entities/optuna.md` — *Optuna* (last_verified: 2026-04-18)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `warmstarting-hyperparameter-tuning-optuna` | `optuna` | 1.000 |

**Recommended winner:** `wiki/entities/optuna.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Warmstarting Hyperparameter Tuning with Optuna" into `wiki/entities/optuna.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

## Cluster 49 (2 pages)

**Pages:**

-    `wiki/entities/obsidian-web-clipper.md` — *Obsidian Web Clipper* (last_verified: 2026-04-08)
- 🏆 `wiki/entities/obsidian.md` — *Obsidian* (last_verified: 2026-04-08)

**Pairwise similarity:**

| A | B | score |
|---|---|-------|
| `obsidian-web-clipper` | `obsidian` | 1.000 |

**Recommended winner:** `wiki/entities/obsidian.md` (oldest last_verified, then shortest slug).

**Suggested action:** merge content of "Obsidian Web Clipper" into `wiki/entities/obsidian.md` (preserve sources + wikilinks), then redirect or delete the loser slugs after the merge is verified.

