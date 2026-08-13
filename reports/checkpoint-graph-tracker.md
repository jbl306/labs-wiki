# Checkpoint Graph Tracker

> **Report-only.** This file is auto-generated on every graph build.
> It does not rewrite retention settings, tier values, or checkpoint
> frontmatter. Its purpose is to surface disagreements between the
> heuristic classifier and the graph recommendation layer so they can
> be evaluated before any policy change is made.

**Generated:** 2026-08-13T00:00:00Z
**Total checkpoints:** 150

## Graph recommendation counts

| Recommendation | Count |
| --- | --- |
| `keep` | 107 |
| `compress` | 33 |
| `merge` | 10 |
| `archive` | 0 |

## Disagreement summary

> **Note:** Graph `merge` is a structural signal (checkpoint community ≥ 3 members,
> concept-connected, no synthesis neighbor). The heuristic baseline never emits `merge`,
> so graph-`merge` checkpoints are shown separately below and are **not** counted here.

**Disagreements (excluding merge):** 46 of 150

| Transition (heuristic→graph) | Count |
| --- | --- |
| `compress→keep` | 41 |
| `keep→compress` | 5 |

## Disagreement detail

| Title | Path | Class | Retention | Heuristic rec | Graph rec | Degree | Concept nb | Synth nb | Tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Copilot Session Checkpoint: Backtest Completion Props Investigation | `sources/copilot-session-checkpoint-backtest-completion-props-investigation.md` | project-progress | compress | `compress` | `keep` | 13 | 4 | 3 | hot |
| Copilot Session Checkpoint: BeddyByes RTÉ ingest — DRM wall | `sources/copilot-session-checkpoint-beddybyes-rte-ingest-drm-wall.md` | project-progress | compress | `compress` | `keep` | 10 | 3 | 2 | hot |
| Copilot Session Checkpoint: Building jbl-dev-kit multiagent workflow | `sources/copilot-session-building-jbl-dev-kit-multiagent-workflow.md` |  |  | `compress` | `keep` | 12 | 5 | 2 | hot |
| Copilot Session Checkpoint: Canonical Props Implementation | `sources/copilot-session-checkpoint-canonical-props-implementation.md` | project-progress | compress | `compress` | `keep` | 10 | 4 | 1 | hot |
| Copilot Session Checkpoint: Copilot CLI container deployment fixes | `sources/copilot-session-checkpoint-copilot-cli-container-fixes.md` | project-progress | compress | `compress` | `keep` | 10 | 3 | 2 | hot |
| Copilot Session Checkpoint: Dashboard Accuracy Finalization | `sources/copilot-session-checkpoint-dashboard-accuracy-finalization.md` | project-progress | compress | `compress` | `keep` | 17 | 6 | 1 | hot |
| Copilot Session Checkpoint: Dashboard Accuracy Hardening | `sources/copilot-session-checkpoint-dashboard-accuracy-hardening.md` | project-progress | compress | `compress` | `keep` | 17 | 6 | 2 | hot |
| Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress | `sources/copilot-session-checkpoint-dashboard-matviews-implementation-in-progress.md` | project-progress | compress | `compress` | `keep` | 9 | 3 | 1 | archive |
| Copilot Session Checkpoint: Direct Sportsbook Sources | `sources/copilot-session-checkpoint-direct-sportsbook-sources.md` |  |  | `compress` | `keep` | 14 | 5 | 3 | hot |
| Copilot Session Checkpoint: Extending jbl-dev-kit workflow toolkit | `sources/copilot-session-extending-jbl-dev-kit-workflow-toolkit.md` |  |  | `compress` | `keep` | 11 | 6 | 1 | hot |
| Copilot Session Checkpoint: Fixing Android Share Ingest API | `sources/copilot-session-checkpoint-fixing-android-share-ingest-api.md` | durable-debugging | retain | `keep` | `compress` | 7 | 3 | 0 | hot |
| Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete | `sources/copilot-session-checkpoint-full-labs-wiki-implementation-complete.md` | durable-workflow | retain | `keep` | `compress` | 7 | 3 | 0 | hot |
| Copilot Session Checkpoint: Implementing CSR benefits UI/UX uplift | `sources/copilot-session-implementing-csr-benefits-ui-ux-uplift.md` | project-progress | compress | `compress` | `keep` | 10 | 4 | 2 | hot |
| Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements | `sources/copilot-session-checkpoint-implementing-sprint-29-ml-improvements.md` | project-progress | compress | `compress` | `keep` | 10 | 4 | 2 | archive |
| Copilot Session Checkpoint: Knightcrawler TorBox Backend | `sources/copilot-session-checkpoint-knightcrawler-torbox-backend.md` |  |  | `compress` | `keep` | 5 | 2 | 1 | hot |
| Copilot Session Checkpoint: MemPalace Phase 3-4 and AutoAgent Research | `sources/copilot-session-checkpoint-mempalace-phase-3-4-and-autoagent-research.md` | project-progress | compress | `compress` | `keep` | 10 | 2 | 1 | archive |
| Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation | `sources/copilot-session-checkpoint-odds-api-quota-optimization-sgo-investigation.md` | project-progress | compress | `compress` | `keep` | 10 | 3 | 1 | archive |
| Copilot Session Checkpoint: Phase 5 Merged; Graph UI Next | `sources/copilot-session-checkpoint-phase-5-merged-graph-ui-next.md` | project-progress | compress | `compress` | `keep` | 5 | 3 | 1 | archive |
| Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed | `sources/copilot-session-checkpoint-pipeline-enhancements-and-vision-support-deployed.md` | project-progress | compress | `compress` | `keep` | 12 | 3 | 3 | archive |
| Copilot Session Checkpoint: Planning and Progress Tracking Complete | `sources/copilot-session-checkpoint-planning-and-progress-tracking-complete.md` | project-progress | compress | `compress` | `keep` | 9 | 3 | 2 | archive |
| Copilot Session Checkpoint: Rankings Page and Performance Optimization | `sources/copilot-session-checkpoint-rankings-page-and-performance-optimization.md` | project-progress | compress | `compress` | `keep` | 9 | 3 | 1 | archive |
| Copilot Session Checkpoint: Retrained Models, Deploying Improvements | `sources/copilot-session-checkpoint-retrained-models-deploying-improvements.md` | project-progress | compress | `compress` | `keep` | 10 | 4 | 1 | archive |
| Copilot Session Checkpoint: Second Curation Reports | `sources/copilot-session-checkpoint-second-curation-reports.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |
| Copilot Session Checkpoint: Spatial Production Deployment | `sources/copilot-session-checkpoint-spatial-production-deployment.md` | project-progress | compress | `compress` | `keep` | 11 | 2 | 1 | hot |
| Copilot Session Checkpoint: Spatial Studio Production Roadmap | `sources/copilot-session-checkpoint-spatial-studio-production-roadmap.md` | project-progress | compress | `compress` | `keep` | 10 | 2 | 3 | hot |
| Copilot Session Checkpoint: Sprint 10 Complete and Deployed | `sources/copilot-session-checkpoint-sprint-10-complete-and-deployed.md` | project-progress | compress | `compress` | `keep` | 12 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 10 Implementation and Deployment | `sources/copilot-session-checkpoint-sprint-10-implementation-and-deployment.md` | project-progress | compress | `compress` | `keep` | 11 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 10 Retrain In Progress | `sources/copilot-session-checkpoint-sprint-10-retrain-in-progress.md` | project-progress | compress | `compress` | `keep` | 14 | 6 | 1 | archive |
| Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed | `sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed.md` | project-progress | compress | `compress` | `keep` | 13 | 7 | 1 | archive |
| Copilot Session Checkpoint: Sprint 13 Model Improvements Code | `sources/copilot-session-checkpoint-sprint-13-model-improvements-code.md` | project-progress | compress | `compress` | `keep` | 12 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 18 GE integration and credential purge | `sources/copilot-session-checkpoint-sprint-18-ge-integration-and-credential-purge.md` | durable-architecture | retain | `keep` | `compress` | 3 | 0 | 1 | hot |
| Copilot Session Checkpoint: Sprint 50 complete, skill optimized | `sources/copilot-session-checkpoint-sprint-50-complete-skill-optimized.md` | project-progress | compress | `compress` | `keep` | 4 | 0 | 1 | archive |
| Copilot Session Checkpoint: Sprint 52 implementation, deploying matviews | `sources/copilot-session-checkpoint-sprint-52-implementation-deploying-matviews.md` | project-progress | compress | `compress` | `keep` | 4 | 0 | 1 | archive |
| Copilot Session Checkpoint: Sprint 52 planning started | `sources/copilot-session-checkpoint-sprint-52-planning-started.md` | project-progress | compress | `compress` | `keep` | 4 | 0 | 1 | archive |
| Copilot Session Checkpoint: Sprint 55 Implementation and Deployment | `sources/copilot-session-checkpoint-sprint-55-implementation-and-deployment.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 55 Planning and Exploration | `sources/copilot-session-checkpoint-sprint-55-planning-and-exploration.md` | project-progress | compress | `compress` | `keep` | 8 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning | `sources/copilot-session-checkpoint-sprint-56-no-retrain-fixes-planning.md` | project-progress | compress | `compress` | `keep` | 6 | 2 | 1 | archive |
| Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis | `sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis.md` | project-progress | compress | `compress` | `keep` | 10 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning | `sources/copilot-session-checkpoint-sprint-58-shap-bug-planning.md` | project-progress | compress | `compress` | `keep` | 12 | 4 | 3 | archive |
| Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation | `sources/copilot-session-checkpoint-sprint-59-shap-coverage-implementation.md` | project-progress | compress | `compress` | `keep` | 8 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 60 PTS Feature Planning | `sources/copilot-session-checkpoint-sprint-60-pts-feature-planning.md` | project-progress | compress | `compress` | `keep` | 6 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 61 Planning + Audit | `sources/copilot-session-checkpoint-sprint-61-planning-audit.md` | project-progress | compress | `compress` | `keep` | 5 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint Accuracy Planning | `sources/copilot-session-checkpoint-sprint-accuracy-planning.md` | project-progress | compress | `compress` | `keep` | 10 | 3 | 1 | hot |
| Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox | `sources/copilot-session-checkpoint-swapping-real-debrid-comet-torbox.md` |  |  | `compress` | `keep` | 7 | 2 | 1 | hot |
| Copilot Session Checkpoint: Training guardrails and resume command | `sources/copilot-session-checkpoint-training-guardrails-and-resume-command.md` | durable-architecture | retain | `keep` | `compress` | 3 | 0 | 1 | hot |
| Copilot Session Checkpoint: VS Code agents, instructions, and Android capture setup | `sources/copilot-session-checkpoint-vs-code-agents-instructions-and-android-capture-setup.md` | durable-architecture | retain | `keep` | `compress` | 2 | 0 | 1 | hot |

## Merge-signal checkpoints

> Structural candidates for a synthesis page: concept-connected (concept_nb ≥ 2),
> no synthesis neighbor, and in a checkpoint community of ≥ 3 members.
> These are not counted in the disagreement metric above.

| Title | Path | Class | Community | Degree | Concept nb | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot Session Checkpoint: Auto-ingest fix + arxiv loop | `sources/copilot-session-checkpoint-auto-ingest-fix-arxiv-loop.md` | durable-debugging | 0 | 8 | 3 | hot |
| Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos | `sources/copilot-session-checkpoint-creating-claude-and-labs-wiki-repos.md` | project-progress | 6 | 8 | 3 | archive |
| Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes | `sources/copilot-session-checkpoint-dashboard-alt-line-accuracy-fixes.md` | durable-debugging | 12 | 7 | 3 | hot |
| Copilot Session Checkpoint: Fixing Live Graph Taps | `sources/copilot-session-checkpoint-fixing-live-graph-taps.md` | durable-debugging | 10 | 7 | 3 | hot |
| Copilot Session Checkpoint: Free Tier Backfill Runner | `sources/copilot-session-checkpoint-free-tier-backfill-runner.md` | durable-workflow | 11 | 3 | 2 | hot |
| Copilot Session Checkpoint: Graph Tracker and Depth Review | `sources/copilot-session-checkpoint-graph-tracker-and-depth-review.md` | durable-architecture | 11 | 5 | 2 | hot |
| Copilot Session Checkpoint: Optimizing Dev Kit Instructions | `sources/copilot-session-checkpoint-optimizing-dev-kit-instructions.md` |  | 0 | 8 | 4 | hot |
| Copilot Session Checkpoint: Phase 5 Backfill Script Written | `sources/copilot-session-checkpoint-phase-5-backfill-script-written.md` | project-progress | 11 | 4 | 2 | archive |
| Copilot Session Checkpoint: Sprint 11 Evaluation and Report | `sources/copilot-session-checkpoint-sprint-11-evaluation-and-report.md` | project-progress | 1 | 9 | 4 | archive |
| Copilot Session Checkpoint: Task-Observer Repo Rollout | `sources/copilot-session-checkpoint-task-observer-repo-rollout.md` | durable-architecture | 0 | 9 | 4 | hot |

## Merge-cluster candidates

Communities with ≥ 3 checkpoints are candidates for a synthesis page.

| Community | Checkpoint node IDs |
| --- | --- |
| 1 | `sources/copilot-session-checkpoint-audit-recommendations-implementation`, `sources/copilot-session-checkpoint-audit-recommendations-sprint`, `sources/copilot-session-checkpoint-backtest-accuracy-contracts`, `sources/copilot-session-checkpoint-backtest-completion-props-investigation`, `sources/copilot-session-checkpoint-canonical-props-implementation`, `sources/copilot-session-checkpoint-dashboard-accuracy-finalization`, `sources/copilot-session-checkpoint-dashboard-accuracy-fixes`, `sources/copilot-session-checkpoint-dashboard-accuracy-hardening`, `sources/copilot-session-checkpoint-data-source-expansion-exploration`, `sources/copilot-session-checkpoint-homelab-nba-repairs`, `sources/copilot-session-checkpoint-implementing-sprint-29-ml-improvements`, `sources/copilot-session-checkpoint-nba-ml-pipeline-oom-fixes`, `sources/copilot-session-checkpoint-oom-mitigation-follow-up`, `sources/copilot-session-checkpoint-phases-1-4-implementation-and-deployment`, `sources/copilot-session-checkpoint-pipeline-resilience-fixes-dashboard-metrics-investiga`, `sources/copilot-session-checkpoint-retrained-models-deploying-improvements`, `sources/copilot-session-checkpoint-scheduler-dns-agents-cleanup`, `sources/copilot-session-checkpoint-sprint-11-evaluation-and-report`, `sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed`, `sources/copilot-session-checkpoint-sprint-13-model-improvements-code`, `sources/copilot-session-checkpoint-sprint-14-retrain-and-composite-edge`, `sources/copilot-session-checkpoint-sprint-17-tests-and-skill-conversion`, `sources/copilot-session-checkpoint-sprint-18-ge-integration-and-credential-purge`, `sources/copilot-session-checkpoint-sprint-22-post-retrain-optimization`, `sources/copilot-session-checkpoint-sprint-23-props-dashboard-fixes`, `sources/copilot-session-checkpoint-sprint-24-prop-consolidation-implementation`, `sources/copilot-session-checkpoint-sprint-25-dashboard-fixes-implementation`, `sources/copilot-session-checkpoint-sprint-32-feature-implementation`, `sources/copilot-session-checkpoint-sprint-33-drift-aware-training-deployment`, `sources/copilot-session-checkpoint-sprint-35-36-and-game-lines-diagnosis`, `sources/copilot-session-checkpoint-sprint-35-props-page-audit`, `sources/copilot-session-checkpoint-sprint-37-backfill-and-dashboard-enhancements`, `sources/copilot-session-checkpoint-sprint-38-and-documentation-audit`, `sources/copilot-session-checkpoint-sprint-39-41-implementation-and-deployment`, `sources/copilot-session-checkpoint-sprint-39-drift-health-improvements`, `sources/copilot-session-checkpoint-sprint-41-42-completion-and-roadmap`, `sources/copilot-session-checkpoint-sprint-47-prediction-accuracy-fixes`, `sources/copilot-session-checkpoint-sprint-48-complete-sprint-49-audit-done`, `sources/copilot-session-checkpoint-sprint-50-audit-complete-ready-to-implement`, `sources/copilot-session-checkpoint-sprint-50-complete-skill-optimized`, `sources/copilot-session-checkpoint-sprint-52-implementation-deploying-matviews`, `sources/copilot-session-checkpoint-sprint-52-planning-started`, `sources/copilot-session-checkpoint-sprint-53-implementation-started`, `sources/copilot-session-checkpoint-sprint-53-merged-dashboard-metrics-investigation-star`, `sources/copilot-session-checkpoint-sprint-55-implementation-and-deployment`, `sources/copilot-session-checkpoint-sprint-55-planning-and-exploration`, `sources/copilot-session-checkpoint-sprint-56-no-retrain-fixes-planning`, `sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis`, `sources/copilot-session-checkpoint-sprint-58-shap-bug-planning`, `sources/copilot-session-checkpoint-sprint-59-shap-coverage-implementation`, `sources/copilot-session-checkpoint-sprint-60-pts-feature-planning`, `sources/copilot-session-checkpoint-sprint-61-planning-audit`, `sources/copilot-session-checkpoint-sprint-7-browser-based-nba-backfill`, `sources/copilot-session-checkpoint-sprint-8-full-retrain-monitoring`, `sources/copilot-session-checkpoint-sprint-8-model-quality-implementation`, `sources/copilot-session-checkpoint-sprint-8-retrain-results-collection`, `sources/copilot-session-checkpoint-sprint-8-retrain-with-optuna-fix`, `sources/copilot-session-checkpoint-sprint-9-implementation-in-progress`, `sources/copilot-session-checkpoint-sprint-accuracy-planning`, `sources/copilot-session-checkpoint-training-guardrails-and-resume-command`, `sources/copilot-session-checkpoint-training-status-tracker-and-oom-fix`, `sources/copilot-session-checkpoint-weekly-retrain-oom-debugging` |
| 0 | `sources/copilot-session-checkpoint-auto-ingest-fix-arxiv-loop`, `sources/copilot-session-checkpoint-auto-ingest-pipeline-built-and-docs-updated`, `sources/copilot-session-checkpoint-building-4-copilot-cli-custom-agents`, `sources/copilot-session-checkpoint-copilot-cli-container-fixes`, `sources/copilot-session-checkpoint-dashboard-matviews-implementation-in-progress`, `sources/copilot-session-checkpoint-fixing-mempalace-timeouts`, `sources/copilot-session-checkpoint-galloping-bot-cf-clearance-recovery`, `sources/copilot-session-checkpoint-github-crawling-and-richer-extraction`, `sources/copilot-session-checkpoint-graphify-comparison-and-quality-evaluation`, `sources/copilot-session-checkpoint-hermes-dashboard-migration`, `sources/copilot-session-checkpoint-homelab-migration-tunnel-fix`, `sources/copilot-session-checkpoint-homelab-monitoring-and-knightcrawler-fixes`, `sources/copilot-session-checkpoint-homepage-overhaul-and-resource-tuning`, `sources/copilot-session-checkpoint-implementing-checkpoint-curation-phases`, `sources/copilot-session-checkpoint-implementing-post-ingest-quality-fixes`, `sources/copilot-session-checkpoint-installing-mempalace-beginning-migration`, `sources/copilot-session-checkpoint-knightcrawler-done-routing-traced`, `sources/copilot-session-checkpoint-knightcrawler-gating-fix-opencode-bash-config`, `sources/copilot-session-checkpoint-labs-wiki-full-review-report`, `sources/copilot-session-checkpoint-mempalace-phase-3-4-and-autoagent-research`, `sources/copilot-session-checkpoint-mobile-graph-ui-wiki-dedup`, `sources/copilot-session-checkpoint-nba-ml-agents-and-homelab-fixes`, `sources/copilot-session-checkpoint-nba-ml-oom-fix-and-docs-cleanup`, `sources/copilot-session-checkpoint-ntfy-notifications-galloping-bot-alerts-monitor-fixes`, `sources/copilot-session-checkpoint-optimizing-dev-kit-instructions`, `sources/copilot-session-checkpoint-optimizing-snipe-book-then-retry-flow`, `sources/copilot-session-checkpoint-phase-5-merged-graph-ui-next`, `sources/copilot-session-checkpoint-pipeline-enhancements-and-vision-support-deployed`, `sources/copilot-session-checkpoint-researching-mempalace-for-comparison-doc`, `sources/copilot-session-checkpoint-resource-optimization-opencode-bash-fix`, `sources/copilot-session-checkpoint-reworking-docs-for-copilotopencode`, `sources/copilot-session-checkpoint-session-wiki-promotion`, `sources/copilot-session-checkpoint-spatial-production-deployment`, `sources/copilot-session-checkpoint-task-observer-repo-rollout`, `sources/copilot-session-checkpoint-vs-code-agents-instructions-and-android-capture-setup`, `sources/copilot-session-checkpoint-wiki-audit-followups`, `sources/copilot-session-checkpoint-wiki-ingest-4-fix-implementation`, `sources/copilot-session-galloping-bot-payment-resilience-fix` |
| 14 | `sources/copilot-session-checkpoint-beddybyes-rte-ingest-drm-wall`, `sources/copilot-session-checkpoint-fixing-knightcrawler-populate-cron-and-rd-playback`, `sources/copilot-session-checkpoint-homelab-memory-beddybyes-ingest`, `sources/copilot-session-checkpoint-knightcrawler-torbox-backend`, `sources/copilot-session-checkpoint-swapping-real-debrid-comet-torbox` |
| 4 | `sources/copilot-session-checkpoint-clarifying-vision-options`, `sources/copilot-session-checkpoint-edit-hotel-auto-population`, `sources/copilot-session-checkpoint-implementing-full-review-r1-r19-recommendations`, `sources/copilot-session-checkpoint-implementing-s8-quality`, `sources/copilot-session-checkpoint-implementing-s9-features`, `sources/copilot-session-checkpoint-light-ui-redesign-csr-benefits`, `sources/copilot-session-checkpoint-no-llm-reference-workflow`, `sources/copilot-session-checkpoint-react-dashboard-scaffold-and-pages-built`, `sources/copilot-session-checkpoint-spatial-s6-foundation`, `sources/copilot-session-checkpoint-spatial-studio-production-roadmap`, `sources/copilot-session-completing-s6-roadmap`, `sources/copilot-session-implementing-automated-catalog-refresh-pipeline`, `sources/copilot-session-implementing-csr-benefits-ui-ux-uplift`, `sources/copilot-session-implementing-hotel-auto-population-pipeline` |
| 6 | `sources/copilot-session-checkpoint-creating-claude-and-labs-wiki-repos`, `sources/copilot-session-checkpoint-integrating-agent-skill-routing`, `sources/copilot-session-checkpoint-pilot-worktree-baseline`, `sources/copilot-session-checkpoint-url-followup-pass` |
| 12 | `sources/copilot-session-checkpoint-dashboard-alt-line-accuracy-fixes`, `sources/copilot-session-checkpoint-dashboard-prop-line-debug`, `sources/copilot-session-checkpoint-direct-sportsbook-ingestion`, `sources/copilot-session-checkpoint-direct-sportsbook-sources`, `sources/copilot-session-checkpoint-odds-api-quota-optimization-sgo-investigation`, `sources/copilot-session-checkpoint-sgo-data-extraction-fix-and-quality-audit` |
| 10 | `sources/copilot-session-checkpoint-fixing-live-graph-taps`, `sources/copilot-session-checkpoint-github-ingest-depth-fetcher-trim`, `sources/copilot-session-checkpoint-graph-incident-and-cleanup`, `sources/copilot-session-checkpoint-mobile-node-viewer-and-richer-github-ingestion`, `sources/copilot-session-checkpoint-self-synthesizing-r4-checkpoint-clusters` |
| 11 | `sources/copilot-session-checkpoint-free-tier-backfill-runner`, `sources/copilot-session-checkpoint-graph-tracker-and-depth-review`, `sources/copilot-session-checkpoint-phase-5-backfill-script-written`, `sources/copilot-session-checkpoint-planning-and-progress-tracking-complete`, `sources/copilot-session-checkpoint-second-curation-reports` |
| 15 | `sources/copilot-session-checkpoint-sprint-10-complete-and-deployed`, `sources/copilot-session-checkpoint-sprint-10-implementation-and-deployment`, `sources/copilot-session-checkpoint-sprint-10-retrain-in-progress` |

