---
title: "Kelly Bankroll Simulator with Quarter-Kelly Sizing and Daily Exposure Cap"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d12567d0a0a05fa3d657bf2e2ec6bb6e9fa482a9676eee6bf73ec13f8bbf53c0"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md
quality_score: 100
concepts:
  - kelly-bankroll-simulator-quarter-kelly-sizing-daily-exposure-cap
related:
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]]"
tier: hot
tags: [kelly-criterion, bankroll-management, sports-betting, simulation]
---

# Kelly Bankroll Simulator with Quarter-Kelly Sizing and Daily Exposure Cap

## Overview

The Kelly criterion is a formula used to size bets optimally to maximize logarithmic growth of bankroll. However, applying full Kelly sizing across many daily bets can lead to unrealistic bankroll growth estimates. This concept describes a practical adjustment using quarter-Kelly sizing and a daily exposure cap to produce realistic bankroll simulations.

## How It Works

The Kelly criterion calculates the optimal fraction of the bankroll to wager on a bet based on the edge and odds. The formula for the Kelly fraction `f` is:

\[
f = \frac{bp - q}{b}
\]

where:
- `b` = net odds received on the wager (e.g., 1 for even money)
- `p` = probability of winning
- `q` = probability of losing (1 - p)

Applying full Kelly sizing (f=1) across 30+ daily bets compounds exponentially, resulting in absurd bankroll growth (e.g., $1000 → $53 quintillion in 5 days), which is unrealistic due to risk and variance.

To mitigate this, the simulator was adjusted to use quarter-Kelly sizing (0.25× Kelly fraction) and a daily exposure cap of 25% of the starting bankroll. This means:

- Each wager is sized as `f * 0.25` of the bankroll.
- The total wager amount across all bets in a day cannot exceed 25% of the bankroll at the start of that day.
- If the sum of raw wagers exceeds the daily cap, all wagers are scaled down proportionally.
- Wager sizing uses the start-of-day balance, not the running balance during the day, to avoid compounding within the day.

This approach balances growth potential with risk management, producing realistic simulations. After the fix, a $1000 bankroll grew to $1531 over 5 days (53.1% ROI), which is plausible.

The simulator is implemented in the dashboard server code and integrates with the confidence tiers and player P&L leaderboard.

Trade-offs include conservative growth estimates and ignoring intraday bankroll fluctuations, but these are acceptable for dashboard reporting and risk management.

## Key Properties

- **Kelly Fraction:** Quarter-Kelly (0.25×) multiplier applied to full Kelly fraction.
- **Daily Exposure Cap:** Maximum 25% of start-of-day bankroll wagered per day.
- **Wager Sizing:** Wagers sized from start-of-day balance; scaled proportionally if total exceeds cap.
- **Result:** Realistic bankroll growth: $1000 → $1531 over 5 days (53.1% ROI).

## Limitations

Does not model intraday bankroll changes or variance fully; assumes independent bets; quarter-Kelly is a heuristic, not optimal for all risk profiles.

## Example

```python
def size_wagers(kelly_fractions, bankroll):
    raw_wagers = [f * 0.25 * bankroll for f in kelly_fractions]
    total_wager = sum(raw_wagers)
    cap = 0.25 * bankroll
    if total_wager > cap:
        scale = cap / total_wager
        wagers = [w * scale for w in raw_wagers]
    else:
        wagers = raw_wagers
    return wagers
```

## Relationship to Other Concepts

- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — Uses corrected confidence scores from primary prop lines for wager sizing.

## Practical Applications

Used in sports betting bankroll simulators to provide realistic growth projections and risk management by tempering full Kelly bets with fractional sizing and exposure caps.

## Sources

- [[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]] — primary source for this concept
