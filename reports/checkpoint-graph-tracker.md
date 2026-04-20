# Checkpoint Graph Tracker

> **Report-only.** This file is auto-generated on every graph build.
> It does not rewrite retention settings, tier values, or checkpoint
> frontmatter. Its purpose is to surface disagreements between the
> heuristic classifier and the graph recommendation layer so they can
> be evaluated before any policy change is made.

**Generated:** 2026-04-20T12:13:40Z  
**Total checkpoints:** 61  

## Graph recommendation counts

| Recommendation | Count |
| --- | --- |
| `keep` | 43 |
| `compress` | 8 |
| `merge` | 10 |
| `archive` | 0 |

## Disagreement summary

> **Note:** Graph `merge` is a structural signal (checkpoint community ≥ 3 members,
> concept-connected, no synthesis neighbor). The heuristic baseline never emits `merge`,
> so graph-`merge` checkpoints are shown separately below and are **not** counted here.

**Disagreements (excluding merge):** 22 of 61

| Transition (heuristic→graph) | Count |
| --- | --- |
| `compress→keep` | 18 |
| `keep→compress` | 4 |

## Disagreement detail

| Title | Path | Class | Retention | Heuristic rec | Graph rec | Degree | Concept nb | Synth nb | Tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos | `sources/copilot-session-checkpoint-creating-claude-and-labs-wiki-repos.md` | durable-architecture | retain | `keep` | `compress` | 7 | 3 | 0 | hot |
| Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress | `sources/copilot-session-checkpoint-dashboard-matviews-implementation-in-progress.md` | project-progress | compress | `compress` | `keep` | 5 | 3 | 1 | archive |
| Copilot Session Checkpoint: Fixing Android Share Ingest API | `sources/copilot-session-checkpoint-fixing-android-share-ingest-api.md` | durable-debugging | retain | `keep` | `compress` | 5 | 3 | 0 | hot |
| Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete | `sources/copilot-session-checkpoint-full-labs-wiki-implementation-complete.md` | durable-architecture | retain | `keep` | `compress` | 5 | 3 | 0 | hot |
| Copilot Session Checkpoint: Implementing Post-Ingest Quality Fixes | `sources/copilot-session-checkpoint-implementing-post-ingest-quality-fixes.md` | durable-architecture | retain | `keep` | `compress` | 3 | 1 | 1 | archive |
| Copilot Session Checkpoint: MemPalace Phase 3-4 and AutoAgent Research | `sources/copilot-session-checkpoint-mempalace-phase-3-4-and-autoagent-research.md` | project-progress | compress | `compress` | `keep` | 8 | 2 | 1 | archive |
| Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation | `sources/copilot-session-checkpoint-odds-api-quota-optimization-sgo-investigation.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |
| Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed | `sources/copilot-session-checkpoint-pipeline-enhancements-and-vision-support-deployed.md` | project-progress | compress | `compress` | `keep` | 8 | 3 | 1 | archive |
| Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix | `sources/copilot-session-checkpoint-resource-optimization-opencode-bash-fix.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |
| Copilot Session Checkpoint: Retrained Models, Deploying Improvements | `sources/copilot-session-checkpoint-retrained-models-deploying-improvements.md` | project-progress | compress | `compress` | `keep` | 7 | 4 | 1 | archive |
| Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit | `sources/copilot-session-checkpoint-sgo-data-extraction-fix-and-quality-audit.md` | project-progress | compress | `compress` | `keep` | 4 | 1 | 1 | archive |
| Copilot Session Checkpoint: Sprint 10 Complete and Deployed | `sources/copilot-session-checkpoint-sprint-10-complete-and-deployed.md` | project-progress | compress | `compress` | `keep` | 11 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 10 Implementation and Deployment | `sources/copilot-session-checkpoint-sprint-10-implementation-and-deployment.md` | project-progress | compress | `compress` | `keep` | 9 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 10 Retrain In Progress | `sources/copilot-session-checkpoint-sprint-10-retrain-in-progress.md` | project-progress | compress | `compress` | `keep` | 13 | 6 | 1 | archive |
| Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed | `sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed.md` | project-progress | compress | `compress` | `keep` | 11 | 7 | 1 | archive |
| Copilot Session Checkpoint: Sprint 13 Model Improvements Code | `sources/copilot-session-checkpoint-sprint-13-model-improvements-code.md` | project-progress | compress | `compress` | `keep` | 9 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 55 Implementation and Deployment | `sources/copilot-session-checkpoint-sprint-55-implementation-and-deployment.md` | project-progress | compress | `compress` | `keep` | 6 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 55 Planning and Exploration | `sources/copilot-session-checkpoint-sprint-55-planning-and-exploration.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |
| Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning | `sources/copilot-session-checkpoint-sprint-56-no-retrain-fixes-planning.md` | project-progress | compress | `compress` | `keep` | 5 | 2 | 1 | archive |
| Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis | `sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis.md` | project-progress | compress | `compress` | `keep` | 9 | 4 | 1 | archive |
| Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning | `sources/copilot-session-checkpoint-sprint-58-shap-bug-planning.md` | project-progress | compress | `compress` | `keep` | 11 | 4 | 3 | archive |
| Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation | `sources/copilot-session-checkpoint-sprint-59-shap-coverage-implementation.md` | project-progress | compress | `compress` | `keep` | 7 | 3 | 1 | archive |

## Merge-signal checkpoints

> Structural candidates for a synthesis page: concept-connected (concept_nb ≥ 2),
> no synthesis neighbor, and in a checkpoint community of ≥ 3 members.
> These are not counted in the disagreement metric above.

| Title | Path | Class | Community | Degree | Concept nb | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot Session Checkpoint: Implementing Checkpoint Curation Phases | `sources/copilot-session-checkpoint-implementing-checkpoint-curation-phases.md` | durable-architecture | 1 | 3 | 2 | hot |
| Copilot Session Checkpoint: Knightcrawler done, routing traced | `sources/copilot-session-checkpoint-knightcrawler-done-routing-traced.md` |  | 3 | 7 | 3 | hot |
| Copilot Session Checkpoint: Phase 5 Backfill Script Written | `sources/copilot-session-checkpoint-phase-5-backfill-script-written.md` | project-progress | 9 | 4 | 2 | archive |
| Copilot Session Checkpoint: Phase 5 Merged; Graph UI Next | `sources/copilot-session-checkpoint-phase-5-merged-graph-ui-next.md` |  | 1 | 4 | 3 | hot |
| Copilot Session Checkpoint: Planning and Progress Tracking Complete | `sources/copilot-session-checkpoint-planning-and-progress-tracking-complete.md` | project-progress | 9 | 6 | 3 | archive |
| Copilot Session Checkpoint: Scheduler DNS Agents Cleanup | `sources/copilot-session-checkpoint-scheduler-dns-agents-cleanup.md` | durable-debugging | 3 | 7 | 3 | hot |
| Copilot Session Checkpoint: Second Curation Reports | `sources/copilot-session-checkpoint-second-curation-reports.md` | project-progress | 9 | 6 | 3 | archive |
| Copilot Session Checkpoint: Sprint 60 PTS Feature Planning | `sources/copilot-session-checkpoint-sprint-60-pts-feature-planning.md` | project-progress | 0 | 5 | 3 | archive |
| Copilot Session Checkpoint: Sprint 61 Planning + Audit | `sources/copilot-session-checkpoint-sprint-61-planning-audit.md` | project-progress | 0 | 4 | 3 | archive |
| Copilot Session Checkpoint: Wiki Audit Followups | `sources/copilot-session-checkpoint-wiki-audit-followups.md` | durable-architecture | 1 | 3 | 3 | hot |

## Merge-cluster candidates

Communities with ≥ 3 checkpoints are candidates for a synthesis page.

| Community | Checkpoint node IDs |
| --- | --- |
| 1 | `sources/copilot-session-checkpoint-auto-ingest-pipeline-built-and-docs-updated`, `sources/copilot-session-checkpoint-building-4-copilot-cli-custom-agents`, `sources/copilot-session-checkpoint-fixing-mempalace-timeouts`, `sources/copilot-session-checkpoint-github-crawling-and-richer-extraction`, `sources/copilot-session-checkpoint-graphify-comparison-and-quality-evaluation`, `sources/copilot-session-checkpoint-implementing-checkpoint-curation-phases`, `sources/copilot-session-checkpoint-implementing-post-ingest-quality-fixes`, `sources/copilot-session-checkpoint-installing-mempalace-beginning-migration`, `sources/copilot-session-checkpoint-mempalace-phase-3-4-and-autoagent-research`, `sources/copilot-session-checkpoint-mobile-graph-ui-wiki-dedup`, `sources/copilot-session-checkpoint-nba-ml-oom-fix-and-docs-cleanup`, `sources/copilot-session-checkpoint-phase-5-merged-graph-ui-next`, `sources/copilot-session-checkpoint-pipeline-enhancements-and-vision-support-deployed`, `sources/copilot-session-checkpoint-researching-mempalace-for-comparison-doc`, `sources/copilot-session-checkpoint-reworking-docs-for-copilotopencode`, `sources/copilot-session-checkpoint-session-wiki-promotion`, `sources/copilot-session-checkpoint-wiki-audit-followups` |
| 3 | `sources/copilot-session-checkpoint-dashboard-matviews-implementation-in-progress`, `sources/copilot-session-checkpoint-fixing-knightcrawler-populate-cron-and-rd-playback`, `sources/copilot-session-checkpoint-homelab-monitoring-and-knightcrawler-fixes`, `sources/copilot-session-checkpoint-homepage-overhaul-and-resource-tuning`, `sources/copilot-session-checkpoint-knightcrawler-done-routing-traced`, `sources/copilot-session-checkpoint-knightcrawler-gating-fix-opencode-bash-config`, `sources/copilot-session-checkpoint-nba-ml-agents-and-homelab-fixes`, `sources/copilot-session-checkpoint-ntfy-notifications-galloping-bot-alerts-monitor-fixes`, `sources/copilot-session-checkpoint-optimizing-snipe-book-then-retry-flow`, `sources/copilot-session-checkpoint-resource-optimization-opencode-bash-fix`, `sources/copilot-session-checkpoint-scheduler-dns-agents-cleanup` |
| 0 | `sources/copilot-session-checkpoint-data-source-expansion-exploration`, `sources/copilot-session-checkpoint-phases-1-4-implementation-and-deployment`, `sources/copilot-session-checkpoint-retrained-models-deploying-improvements`, `sources/copilot-session-checkpoint-sprint-10-complete-and-deployed`, `sources/copilot-session-checkpoint-sprint-10-implementation-and-deployment`, `sources/copilot-session-checkpoint-sprint-10-retrain-in-progress`, `sources/copilot-session-checkpoint-sprint-12-complete-and-skills-installed`, `sources/copilot-session-checkpoint-sprint-13-model-improvements-code`, `sources/copilot-session-checkpoint-sprint-55-implementation-and-deployment`, `sources/copilot-session-checkpoint-sprint-55-planning-and-exploration`, `sources/copilot-session-checkpoint-sprint-56-no-retrain-fixes-planning`, `sources/copilot-session-checkpoint-sprint-57-ensemble-save-diagnosis`, `sources/copilot-session-checkpoint-sprint-58-shap-bug-planning`, `sources/copilot-session-checkpoint-sprint-59-shap-coverage-implementation`, `sources/copilot-session-checkpoint-sprint-60-pts-feature-planning`, `sources/copilot-session-checkpoint-sprint-61-planning-audit`, `sources/copilot-session-checkpoint-training-status-tracker-and-oom-fix` |
| 11 | `sources/copilot-session-checkpoint-odds-api-quota-optimization-sgo-investigation`, `sources/copilot-session-checkpoint-pipeline-resilience-fixes-dashboard-metrics-investiga`, `sources/copilot-session-checkpoint-sgo-data-extraction-fix-and-quality-audit` |
| 9 | `sources/copilot-session-checkpoint-phase-5-backfill-script-written`, `sources/copilot-session-checkpoint-planning-and-progress-tracking-complete`, `sources/copilot-session-checkpoint-second-curation-reports` |
| 8 | `sources/copilot-session-checkpoint-props-db-query-and-chart-refinement`, `sources/copilot-session-checkpoint-rankings-page-and-performance-optimization`, `sources/copilot-session-checkpoint-react-dashboard-scaffold-and-pages-built` |

