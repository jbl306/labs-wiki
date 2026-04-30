---
title: "Prior-Season Feature Mapping for Temporal Leakage Prevention"
type: concept
created: 2026-04-30
last_verified: 2026-04-30
source_hash: "02ef1738c2df2fa90f694299ca6aad3b0a2119bff4c33aee54a4c6b0da5a52b5"
sources:
  - raw/2026-04-25-copilot-session-audit-recommendations-implementation-4d25144f.md
quality_score: 87
concepts:
  - prior-season-feature-mapping-temporal-leakage-prevention
related:
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[Calibration Leakage Mitigation in ML Model Training]]"
  - "[[Training-Mode-Aware Rolling Window Metadata]]"
  - "[[Minutes Prediction Sub-Model]]"
tier: hot
tags: [feature-engineering, temporal-leakage, prior-season, nba-ml-engine, ml-reliability, data-integrity]
---

# Prior-Season Feature Mapping for Temporal Leakage Prevention

## Overview

Prior-season feature mapping is a temporal feature-engineering rule that attaches season-level statistics from season $S$ only to game rows in season $S+1$, rather than reusing same-season aggregates that may already contain future information. In the audit-remediation checkpoint, this rule was applied across advanced stats, team stats, hustle stats, and Basketball Reference season-level features to stop historical training rows from “seeing” values that were only knowable later in the same season.

## How It Works

Temporal leakage often hides inside feature tables that look perfectly legitimate. Season-level datasets are especially risky: if a game row from November 2024 joins against a “2024-25 season average” table computed after March 2025 games have already occurred, the model is implicitly reading the future. The checkpoint identifies exactly this class of leakage and fixes it by changing the join policy, not merely by adding another warning or note to downstream evaluation.

The key mapping rule is simple:

$$
\text{features for season } S+1 \leftarrow \text{season summary from } S
$$

So if a row belongs to the `2024-25` game season, the safe attached season-level summary is the `2023-24` season table. This transforms season-level features from “current-season aggregate” signals into lagged priors. Lagged priors are imperfect, but they are honest: they reflect what could reasonably be known before the new season's games unfold.

In the checkpoint, that logic is implemented as a reusable prior-season mapping helper and then applied across several feature families. Advanced stats no longer use the old same-season fallback. Team-level, hustle, and Basketball Reference season features are also routed through the prior-season mapping path. This matters because leakage is rarely confined to one join. If only advanced stats were fixed while hustle or team metrics still used same-season summaries, the model would remain contaminated through a different door.

The session also tightens upstream data preparation to support these joins. `_load_game_logs()` now includes a `Player.team` join because downstream feature merges require a team identifier. That is a practical reminder that temporal integrity is not only about dates; it is also about carrying the right join keys through the pipeline so safe mappings can be expressed at all. Without the team join, certain team-scoped lagged features would be unavailable or incorrectly merged.

Missing-data behavior is part of the design too. Once same-season fallback is removed, some rows will no longer find a prior-season record. The checkpoint chooses a conservative response: values may remain `NaN` or be filled only from safe prior-derived population means. This is the right tradeoff for leakage prevention. A slightly sparser but honest feature matrix is preferable to a dense matrix contaminated by future information. In other words, the system prioritizes causal validity over superficial completeness.

The checkpoint explicitly records one remaining limitation: `Player.team` is still current-team data, not historical team-at-game data. That means the pipeline is safer than before but not yet a perfect as-of feature store. If a player changed teams, some joins may still reflect present-day roster state rather than exact historical affiliation. The session does the correct thing operationally by documenting this boundary instead of over-claiming that the leakage problem is “fully solved.”

The deeper lesson is that temporal leakage prevention must live inside feature construction rules. Evaluation-only fixes cannot recover from a feature table that already contains future-derived signals. Prior-season mapping works because it changes the semantics of the feature itself: the model now receives a true lagged prior instead of a disguised hindsight statistic.

## Key Properties

- **Lagged season semantics:** Season summaries are treated as priors for the next season, not as same-season contemporaneous facts.
- **Multi-table application:** The rule was applied across advanced, team, hustle, and BBRef feature families, not just one join.
- **Safe missingness policy:** Missing prior-season rows remain missing or use prior-derived population means rather than unsafe same-season fallback.
- **Join-key support:** Adding `Player.team` enables safer downstream merges for team-scoped features.
- **Explicit residual limitation:** Current-team versus historical-team mismatch remains documented as unresolved.

## Limitations

Prior-season mapping is conservative, but it can understate meaningful within-season change. Breakout players, role changes, and team-system changes may make last season's summary a poor proxy for current performance. It also does not provide truly as-of season-expanding statistics; that would require a time-aware feature store keyed by exact game date and historical roster state. Finally, if upstream season labels are wrong, the lagged mapping can silently attach the wrong prior season.

## Examples

```python
def prior_season(season: str) -> str:
    start, end = season.split("-")
    return f"{int(start) - 1}-{str(int(start))[-2:]}"

game_row.season = "2024-25"
safe_feature_season = prior_season(game_row.season)  # "2023-24"

advanced_stats = advanced_stats_by_season.get(safe_feature_season)
```

Concrete checkpoint example: `2023-24` season-level stats are attached to `2024-25` game rows, while the old same-season advanced-stat fallback is removed.

## Practical Applications

This pattern is useful in sports analytics, financial forecasting, churn modeling, and any domain that joins slowly changing aggregate tables onto event-level rows. Whenever a feature could have been computed using future events relative to the prediction timestamp, lagged mapping is a strong baseline defense against inflated backtests and false model confidence.

## Related Concepts

- **[[Feature Engineering Pipeline for NBA ML Platform]]** — Provides the broader pipeline context in which these lagged joins operate.
- **[[Calibration Leakage Mitigation in ML Model Training]]** — Both concepts prevent optimistic evaluation caused by future information sneaking into the training/evaluation loop.
- **[[Training-Mode-Aware Rolling Window Metadata]]** — Split-level and feature-level temporal safeguards complement each other.
- **[[Minutes Prediction Sub-Model]]** — Serves as a nearby example of a sub-model feature that also needs careful temporal semantics to avoid leakage.

## Sources

- [[Copilot Session Checkpoint: Audit Recommendations Implementation]] — primary source for the prior-season helper, removed same-season fallback, multi-table application, and documented historical-team limitation.
