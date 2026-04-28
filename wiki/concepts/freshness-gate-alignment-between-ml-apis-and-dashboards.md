---
title: "Freshness-Gate Alignment Between ML APIs and Dashboards"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "6caf80ac3afa85f4adf295e7c39d6eeba187acacd73f68dd65fc123c58576db1"
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-hardening-404bc17e.md
related:
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]"
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
tier: hot
tags: [freshness, dashboard, api-design, ml-ops, reliability, warnings]
quality_score: 81
---

# Freshness-Gate Alignment Between ML APIs and Dashboards

## Overview

Freshness-gate alignment is the practice of making the dashboard's warning logic reflect the same staleness policy that the backend uses to accept, block, or publish data. It matters because a dashboard becomes untrustworthy when the API says a state is acceptable but the UI still warns that it is stale, or when the UI looks clean even though the backend would reject the same freshness relationship for downstream jobs.

## How It Works

The checkpoint captures a classic policy-drift problem between backend logic and user-facing semantics. The NBA ML API already allowed a one-day lag between game logs and predictions through `PREDICTION_MAX_GAME_LOG_LAG_DAYS=1`. That meant predictions could still be considered operationally valid when game logs trailed by one day. But the dashboard layer had a stricter, hardcoded stale-log rule based on roughly 12 hours. As a result, the UI warned users about a state the backend itself considered acceptable.

This is not just a cosmetic mismatch. Freshness warnings are supposed to summarize policy. When they diverge from backend gates, operators and users learn the wrong rule. They may distrust valid data, escalate false incidents, or spend time “fixing” a lag that the system deliberately tolerates. In the checkpoint, that mismatch was especially costly because the broader dashboard-accuracy effort was about making the interface honest rather than alarmist.

The repair moved freshness reasoning into shared BFF contract logic. `dashboard-ui/server/src/dashboardContracts.ts` gained `FreshnessDates`, a date-lag helper, and `buildFreshnessWarnings()`. Instead of scattering staleness heuristics across route handlers or frontend copy, the BFF now computes warnings from a coherent freshness model before handing them to the UI. That keeps the frontend simple and makes the warning semantics reviewable alongside the rest of the contract layer.

The governing rule can be expressed simply. If $d_p$ is the prediction date, $d_g$ is the most recent game-log date, and $L$ is the permitted lag in days, then warn only when

$$
d_p - d_g > L
$$

In this checkpoint, $L = 1$. A one-day lag is therefore acceptable; a two-day lag is not. That single inequality aligns user-facing warnings with backend gating and explains several live observations in the checkpoint.

The date examples make the policy concrete. The live final state had `game_logs=2026-04-24`, `predictions=2026-04-25`, and `prop_lines=2026-04-26`. Under the aligned policy, `2026-04-25` predictions are still acceptable because the game-log lag is exactly one day. That is why the stale game-log dashboard warning could be removed. But `2026-04-26` predictions would be blocked with `2026-04-24` logs because the lag becomes two days, which exceeds the allowed threshold. The policy is tolerant, but not permissive.

This pattern also clarifies the difference between informational freshness metadata and policy-triggered warnings. A dashboard may still display raw dates for game logs, predictions, and prop lines even when no warning is active. The absence of a warning does not mean “perfectly fresh”; it means “within tolerated bounds.” That nuance matters in operational dashboards, where binary good/bad messaging often hides the fact that systems intentionally accept bounded lag.

Another important lesson is architectural. Freshness-policy alignment belongs near the contract boundary, not as scattered conditional rendering in the frontend. The BFF already knows the relevant dates and already emits `accuracy_warnings`. By deriving those warnings in one place, the system avoids duplicated logic and makes future threshold changes safer. If the backend changes `L`, the dashboard should change with it, ideally from a shared configuration source rather than a second hand-maintained constant.

The checkpoint demonstrates the user-facing payoff. After the change, the dashboard warning list no longer included a stale game-log complaint for the one-day lag case. The only remaining warning was the legitimate degraded model-health alert. That makes the UI quieter, but more importantly, it makes it more truthful. The dashboard stops shouting about a condition the platform itself defines as acceptable and starts reserving warnings for genuinely actionable risk.

## Key Properties

- **Policy/UI consistency**: Warning semantics match backend gating semantics.
- **Explicit lag budget**: A named threshold such as `PREDICTION_MAX_GAME_LOG_LAG_DAYS` defines tolerated staleness.
- **Shared contract computation**: BFF helpers like `buildFreshnessWarnings()` centralize freshness reasoning.
- **Bounded tolerance**: The pattern allows controlled lag without collapsing into “anything goes.”
- **Cleaner operator signals**: Warnings correspond to true threshold violations instead of local UI heuristics.

## Limitations

Alignment does not guarantee the chosen threshold is correct. A one-day lag may be appropriate operationally yet still be too stale for certain use cases or users. The pattern also depends on consistent date semantics: if one layer reports source timestamps in local time and another in UTC, aligned logic can still produce confusing results. Finally, dashboards that simply mirror backend policy may under-communicate nuance unless they also show the underlying dates.

## Examples

```typescript
type FreshnessDates = {
  gameLogsDate: string | null
  predictionsDate: string | null
  propLinesDate: string | null
}

function buildFreshnessWarnings(dates: FreshnessDates, maxLagDays = 1): string[] {
  const lagDays = diffDays(dates.predictionsDate, dates.gameLogsDate)
  if (lagDays > maxLagDays) {
    return [`Game logs are ${lagDays} days behind predictions.`]
  }
  return []
}
```

The important thing is not the helper signature; it is that the helper encodes the same freshness rule the backend uses to decide whether data should proceed.

## Practical Applications

This concept is useful for dashboards that summarize data pipelines, ETL jobs, forecasts, or ML predictions where freshness tolerance is intentionally bounded rather than absolute. It applies to analyst-facing dashboards, ops consoles, and any BFF-mediated interface that presents data from multiple schedules. In the labs-wiki workspace, it is directly applicable to future [[NBA ML Engine]] and homelab UIs: warnings should describe actual policy violations, not merely local front-end discomfort with lag.

## Related Concepts

- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]**: Freshness-gate alignment is one concrete case of making warning metadata truthful rather than decorative.
- **[[Shared Contract Normalization for Dashboard APIs]]**: Centralizing freshness warnings in the contract layer follows the same “one boundary, one truth” discipline.
- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]**: The BFF is the natural place to combine dates from multiple sources and emit a policy-aware warning surface for the UI.

## Sources

- [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]] — documents the one-day lag rule, the new `buildFreshnessWarnings()` helper, and the live removal of the false stale-log warning.
