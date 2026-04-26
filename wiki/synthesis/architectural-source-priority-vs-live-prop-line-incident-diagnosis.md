---
title: "Architectural Source Priority vs Live Prop-Line Incident Diagnosis"
type: synthesis
created: '2026-04-26'
last_verified: '2026-04-26'
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-26-copilot-session-dashboard-prop-line-debug-ccc0f19c.md
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
  - raw/2026-04-25-copilot-session-direct-sportsbook-sources-855a32a8.md
concepts:
  - source-priority-canonical-prop-ingestion
  - browser-backed-sportsbook-truth-validation
  - standard-over-under-vs-milestone-prop-market-identity
related:
  - "[[Source-Priority Canonical Prop Ingestion]]"
  - "[[Browser-Backed Sportsbook Truth Validation]]"
  - "[[Standard Over/Under vs Milestone Prop Market Identity]]"
  - "[[NBA ML Engine]]"
tier: hot
tags: [sports-betting, synthesis, prop-lines, incident-response, nba-ml-engine]
---

# Architectural Source Priority vs Live Prop-Line Incident Diagnosis

## Question

Why can a dashboard still show low-priority sportsbook rows even after a system has implemented explicit direct-source priority, and how should engineers debug that gap without blaming the ranking rule too early?

## Summary

[[Source-Priority Canonical Prop Ingestion]] answers what should win **if** the right direct-book rows exist and are correctly classified in storage. [[Browser-Backed Sportsbook Truth Validation]] answers a different question: whether those rows were ever fetched, whether the disputed line belongs to the same market family, and whether the live system is actually serving from the inputs the architecture assumes.

The Josh Hart checkpoint makes the dependency explicit. Source-priority design is a policy layer, not proof that `DK_WEB` or `FD_WEB` rows are present, fresh, or semantically equivalent to the user-observed market.

## Comparison

| Dimension | [[Source-Priority Canonical Prop Ingestion]] | [[Browser-Backed Sportsbook Truth Validation]] |
|-----------|----------------------------------------------|-----------------------------------------------|
| Core question | Which row should win inside a bookmaker family? | What is the sportsbook actually showing right now? |
| Main inputs | `prop_lines`, bookmaker mapping, `market_scope`, `market_class`, source ranks | Sportsbook UI, captured network calls, provider payloads, DB rows, dashboard/API responses |
| Preconditions | Direct and fallback rows already exist in canonical storage | A trust-critical mismatch or ambiguous market claim exists |
| Typical failure mode | Correct ranking policy but missing or misclassified high-priority rows | Correct sportsbook evidence but no durable serving rule encoded afterward |
| Best output | Stable canonical selection for production serving | Root-cause proof about ingestion freshness, taxonomy, or endpoint drift |
| Escalation trigger | Normal ingestion/serving path | Incident response when user trust is at risk |

## Analysis

The earlier direct-ingestion work taught the system how to prefer truth. By mapping `DK_WEB` and `FD_WEB` above `DK`, `FD`, `SGO_DK`, and `SGO_FD`, the pipeline stopped treating all providers as epistemically equal. That is a major architectural improvement, but it only governs the candidate set the live system actually has.

The dashboard-debug checkpoint is valuable because it preserves the next operational lesson: a well-designed priority ladder can still produce a fallback answer when direct rows are absent. That absence can happen for several distinct reasons. The direct fetch may not have run after deployment. The adapter may have failed silently at runtime because of endpoint, anti-bot, or config issues. The row may have been fetched but classified into a non-canonical market bucket. Or the row may exist in storage while the serving layer still reads older materialized-view state.

This is why incident diagnosis must step outside ranking logic and follow the evidence chain end to end. A user sees a suspicious line on the dashboard, but the fix does not start in SQL ordering. It starts by confirming the sportsbook's real market, then comparing provider payloads, then checking `prop_lines`, `prop_line_snapshots`, and `mv_prop_lines_primary`, and only then asking whether source-priority selection behaved incorrectly. The architecture tells you how the system should choose; the incident workflow tells you whether the system had the right things to choose from.

The checkpoint also sharpens the role of [[Standard Over/Under vs Milestone Prop Market Identity]]. The user-visible DraftKings **2+** observation and the dashboard's `0.5` row may look contradictory while actually referring to different products. If the market family is wrong, source priority is not yet the relevant bug. In that case the live system may be serving a valid standard O/U fallback while the human is thinking about a milestone ladder. The taxonomy layer has to resolve that semantic mismatch before source ranking can be judged fairly.

For the [[NBA ML Engine]], the practical takeaway is that architecture and incident response should be treated as two linked but separate layers. Source priority should remain the durable serving rule. But when live rows still come from `SGO_*`, the next move is not "rewrite the ranking logic" by reflex. The next move is to determine whether direct truth is missing, stale, filtered out, or simply talking about a different market family. Only after that distinction is made can the system decide between an ingestion fix, a query fix, or a product-labeling fix.

## Key Insights

1. **Source priority is a selection policy, not a freshness guarantee** — supported by [[Source-Priority Canonical Prop Ingestion]] and [[Copilot Session Checkpoint: Dashboard Prop Line Debug]].
2. **Live sportsbook incidents are often candidate-set failures, not ranking failures** — supported by [[Browser-Backed Sportsbook Truth Validation]] and [[Copilot Session Checkpoint: Dashboard Prop Line Debug]].
3. **Market-family identity must be settled before a disputed line can be called wrong** — supported by [[Standard Over/Under vs Milestone Prop Market Identity]] and [[Copilot Session Checkpoint: Direct Sportsbook Sources]].

## Open Questions

- When direct-book rows are temporarily missing, should the dashboard continue serving `SGO_*` fallbacks, suppress those books entirely, or surface an explicit "direct truth unavailable" warning?
- Should `mv_prop_lines_primary` or upstream ingestion track freshness/provenance metadata strongly enough to distinguish "fallback by design" from "fallback because direct rows never landed"?

## Sources

- [[Copilot Session Checkpoint: Dashboard Prop Line Debug]]
- [[Copilot Session Checkpoint: Direct Sportsbook Ingestion]]
- [[Copilot Session Checkpoint: Direct Sportsbook Sources]]

