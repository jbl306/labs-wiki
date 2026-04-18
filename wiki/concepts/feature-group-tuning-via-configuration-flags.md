---
title: "Feature Group Tuning via Configuration Flags"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 100
concepts:
  - feature-group-tuning-via-configuration-flags
related:
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [feature-engineering, configuration, machine-learning]
---

# Feature Group Tuning via Configuration Flags

## Overview

Feature group tuning allows selective enabling or disabling of specific feature sets in a machine learning pipeline through configuration flags. This approach improves model flexibility and performance by allowing the exclusion of non-informative or noisy features.

## How It Works

In the NBA ML Engine Sprint 12, six feature groups were gated behind individual boolean configuration flags in the central config.py file. These flags include USE_B2B_FATIGUE, USE_INJURY_RETURN, USE_MINUTES_TREND, USE_SEASON_PHASE, USE_MATCHUP, and USE_TARGET_ENCODING. Each flag controls whether the corresponding feature group is included during feature matrix assembly in builder.py.

The feature matrix builder conditionally calls internal methods to add features from each group only if the respective flag is set to true. For example, if USE_B2B_FATIGUE is false, the three features related to back-to-back fatigue are excluded from the feature matrix.

By default, some feature groups with no signal (b2b_fatigue, injury_return, target_encoding) were disabled (false), while others with marginal signal (minutes_trend, season_phase, matchup) were enabled (true). This tuning was informed by prior evaluation results indicating which features contributed positively or negatively to model performance.

This approach allows rapid experimentation and deployment of feature subsets without code changes, facilitating iterative model improvement. It also helps reduce overfitting and computational overhead by excluding irrelevant features.

The flags are centrally managed and documented in config.py, making it easy for data scientists and engineers to understand and adjust feature usage. This modular design supports future feature group additions or removals with minimal disruption.

## Key Properties

- **Configurability:** Six independent boolean flags control inclusion of feature groups, enabling fine-grained tuning.
- **Default Settings:** Groups with no signal default to false; marginal signal groups default to true.
- **Impact on Feature Matrix:** Feature matrix size reduced by excluding disabled groups; e.g., 11 features removed in total.

## Limitations

This approach assumes that feature groups are well-defined and separable. Overlapping or highly correlated features across groups may reduce the effectiveness of gating. Also, disabling feature groups reduces model input diversity, which might hurt performance if useful signals are excluded. Requires careful evaluation to avoid removing valuable features.

## Example

In builder.py, the feature matrix assembly function includes conditional calls like:

```python
if config.USE_B2B_FATIGUE:
    self._add_b2b_fatigue_features()
```

Setting `USE_B2B_FATIGUE = False` in config.py excludes these features from training and inference.

## Relationship to Other Concepts

- **Feature Selection** — Feature group tuning is a form of feature selection at the group level.

## Practical Applications

Used in machine learning pipelines where feature sets can be logically grouped and toggled to optimize model performance and interpretability. Particularly useful in iterative development and production environments requiring rapid deployment of feature changes.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
