---
title: "Kelly Bet Sizing Bug Fix in Sequential Betting Simulations"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1544a9390c8a215aeb38b788d3103fd5a18163dc8ce9182c4c6fc36fbb638e43"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-critical-ml-fixes-sprint-28-9cff218d.md
quality_score: 100
concepts:
  - kelly-bet-sizing-bug-fix-in-sequential-betting-simulations
related:
  - "[[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]]"
tier: hot
tags: [betting, kelly criterion, simulation, financial modeling]
---

# Kelly Bet Sizing Bug Fix in Sequential Betting Simulations

## Overview

The Kelly criterion is a formula used to determine the optimal size of a series of bets to maximize logarithmic growth of bankroll. Correct implementation in sequential simulations is critical to accurately model bankroll evolution and bet sizing.

## How It Works

In sequential betting simulations, the Kelly bet size for each bet depends on the current bankroll before placing that bet. The bug fixed involved recalculating the Kelly bet sizes after the entire bankroll loop using the final bankroll value, which is incorrect because each bet size should be based on the bankroll at that point in time.

The fix captures the `kelly_bet` amount inside the sequential loop during the bankroll update iteration, storing each bet size in a list (`kelly_bet_list`). This ensures that each bet size reflects the bankroll state at the time of the bet, preserving the correct sequential dependency.

The Kelly formula typically is:

$$ f^* = \frac{bp - q}{b} $$

where:
- $f^*$ is the fraction of the current bankroll to bet,
- $b$ is the net odds received on the wager,
- $p$ is the probability of winning,
- $q = 1 - p$ is the probability of losing.

Correct sequential application requires updating bankroll after each bet and recalculating bet size accordingly.

Trade-offs include the complexity of bookkeeping bet sizes and bankroll states, but this is necessary for accurate simulation.

Edge cases include zero or negative bankrolls, which must be handled to avoid invalid bet sizes.

## Key Properties

- **Sequential Bet Sizing:** Kelly bet sizes are computed inside the bankroll loop, reflecting the bankroll state at each bet.
- **Bug Description:** Previous code recalculated bet sizes after loop using final bankroll, causing incorrect bet sizing.
- **Data Structure:** `kelly_bet_list` stores bet sizes sequentially as bets are processed.

## Limitations

Assumes bankroll updates and bet outcomes are processed sequentially and deterministically. Does not handle stochastic or parallel bet outcomes. Requires careful handling of bankroll edge cases (e.g., bankruptcies).

## Example

```python
kelly_bet_list = []
current_bankroll = initial_bankroll
for bet in bets:
    bet_amount = compute_kelly_bet(current_bankroll, bet.odds, bet.probability)
    kelly_bet_list.append(bet_amount)
    current_bankroll += update_bankroll(bet_amount, bet.outcome)
```

## Relationship to Other Concepts

- **Kelly Criterion** — The fix ensures correct application of the Kelly criterion in sequential betting simulations.

## Practical Applications

Used in sports betting simulations, portfolio management, and gambling strategy modeling to optimize bet sizing and bankroll growth over time.

## Sources

- [[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]] — primary source for this concept
