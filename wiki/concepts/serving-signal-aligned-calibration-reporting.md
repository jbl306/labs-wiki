---
title: "Serving-Signal-Aligned Calibration Reporting"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "6caf80ac3afa85f4adf295e7c39d6eeba187acacd73f68dd65fc123c58576db1"
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-hardening-404bc17e.md
related:
  - "[[Calibration Analysis for Regression Models]]"
  - "[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
tier: hot
tags: [model-calibration, ml-ops, dashboard, ece, reliability, serving]
---

# Serving-Signal-Aligned Calibration Reporting

## Overview

Serving-signal-aligned calibration reporting is the practice of evaluating and publishing calibration metrics for the exact score that the production system uses to rank or filter decisions, rather than for a proxy feature that happens to be easier to compute. It matters because calibration numbers are supposed to tell operators how trustworthy a visible model signal is; if the endpoint measures one score while the product serves another, the metric becomes observationally neat but operationally false.

## How It Works

The checkpoint documents a subtle but damaging mismatch in the NBA dashboard stack. Public calibration endpoints reported Expected Calibration Error (ECE) for a raw edge ratio computed from the gap between prediction and betting line. But the prop-selection logic did not actually serve that raw edge ratio directly. Instead, the production path turned prediction-interval width into a confidence-oriented score, passed that score through a CI Platt calibrator when available, and then optionally through a global post-hoc calibrator. In other words, the dashboard was showing and filtering on one signal while the public reliability endpoint graded another.

That mismatch explains why the system could look paradoxical. The public endpoint showed calibration around `ECE ~0.365`, which implied a badly miscalibrated confidence signal. Yet the serving pipeline was already applying additional transforms intended to make the ranking signal more reliable. The fix was not to hide the bad raw-edge metric; it was to separate concerns. The checkpoint introduced `compute_ci_z_scores()` and `compute_serving_confidence_scores()` so that evaluation code could reconstruct the same score path used during serving, then report that score's calibration directly.

Conceptually, the pattern is: start from a model prediction and a betting line, infer a standardized confidence measure from the prediction interval, then calibrate the resulting score along the same path used in production. If $\hat{y}$ is the predicted value, $l$ is the line, and $\hat{\sigma}$ is an uncertainty term derived from the interval width, the uncalibrated ranking signal looks like

$$
z = \frac{|\hat{y} - l|}{\hat{\sigma}}
$$

or an equivalent standardized margin. That score is then transformed by calibration layers rather than consumed raw. The crucial insight is that the calibration endpoint must evaluate the post-transform score if the product surfaces the post-transform score.

The checkpoint also fixed a second, lower-level calibration bug in `compute_calibration()`. The earlier implementation relied on `sklearn.calibration_curve()`, which returns only populated bins. That behavior is easy to misuse. If code assumes the returned arrays correspond to the first `N` bins instead of the actually populated bins, sparse middle-only probability mass can be paired with the wrong counts and produce falsely tiny or even zero ECE. The repair iterated the real bin edges, kept only populated bins, and associated each populated bin with the correct count before aggregating error.

That aggregation matters because ECE is effectively a weighted discrepancy between predicted confidence and empirical success rate:

$$
\mathrm{ECE} = \sum_{b \in B} \frac{n_b}{N} \left| \mathrm{acc}(b) - \mathrm{conf}(b) \right|
$$

If the counts $n_b$ are attached to the wrong bins, the metric stops describing reality. In the checkpoint, that bug could make sparse middle-bin probabilities look harmless. Once fixed, ECE once again reflected the actual occupied regions of the score distribution.

The hardening pass then propagated the same score-source alignment into model-health alerting. `src/notifications/dispatcher.py` stopped evaluating alert thresholds against the raw proxy signal and instead checked the served signal, storing fields such as `ece_score_source` and `oos_ece_score_source`. That is an important operational design choice: dashboards, alerting, and route-level evaluation should all agree about what signal is being measured. Otherwise, teams spend their time arguing with inconsistent instrumentation instead of repairing the actual model.

Another strong design choice was to preserve the raw metric rather than delete it. The public endpoint now exposes served-score ECE and raw-edge ECE separately. This avoids a common anti-pattern where calibration improvements are reported by quietly swapping metrics. Here, the operator can still see that the old raw-edge view is poor (`0.3653`) while the actual served score is much better calibrated (`0.0215`). The split makes the system more honest, not less.

The practical intuition is simple: a calibration number is only meaningful if it answers the user's real question. In this dashboard, the real question is not “how well calibrated is some nearby raw feature?” It is “how well calibrated is the signal that decides what the user sees and what the system labels as most trustworthy?” Serving-signal alignment makes the answer match the product.

## Key Properties

- **Evaluation parity with serving**: Endpoints and alerts score the same transformed signal that drives prop filtering and ranking.
- **Score-source transparency**: Response metadata such as `score_source` and alert metadata such as `ece_score_source` make the evaluated signal explicit.
- **Sparse-bin correctness**: ECE uses actual populated bins and correct counts instead of positional assumptions about `calibration_curve()` output.
- **Dual reporting**: The system can expose served-score ECE and raw-edge ECE simultaneously, preserving historical comparability without conflating them.
- **Operational trust**: Reliability dashboards describe the decision surface the user actually experiences.

## Limitations

This pattern does not guarantee that the served signal is well calibrated; it only ensures the measurement targets the correct signal. If the upstream uncertainty estimate is unstable, if CI Platt calibration drifts, or if the post-hoc calibrator is trained on stale data, a perfectly aligned endpoint can still report poor reliability. The approach also raises a communication burden: teams must document what each `score_source` means, or operators may compare incompatible ECE values without realizing it.

## Examples

```python
def evaluate_served_signal(predictions, calibrators):
    z_scores = compute_ci_z_scores(predictions)
    served_scores, score_source = compute_serving_confidence_scores(
        z_scores=z_scores,
        ci_platt=calibrators.ci_platt,
        posthoc=calibrators.posthoc,
    )
    served_ece = compute_calibration(served_scores, predictions.outcomes)
    raw_edge_ece = compute_calibration(predictions.raw_edge_ratio, predictions.outcomes)
    return {
        "score_source": score_source,
        "expected_calibration_error": served_ece,
        "raw_edge_expected_calibration_error": raw_edge_ece,
    }
```

The important behavior is that the metric follows the same scoring path as production instead of evaluating a neighboring heuristic out of convenience.

## Practical Applications

This concept applies anywhere a production system transforms raw model outputs before users or downstream policies consume them. Recommendation systems, ranking services, fraud scores, medical triage tools, and betting dashboards all benefit from evaluating the exact post-transform signal in production. In the labs-wiki workspace, it is directly relevant to future [[NBA ML Engine]] work: if the UI or policy engine depends on a calibrated, clipped, or thresholded serving score, every reliability endpoint should measure that same object.

## Related Concepts

- **[[Calibration Analysis for Regression Models]]**: General calibration analysis explains the evaluation objective; this concept adds the requirement that the measured score match the production serving signal.
- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]**: Both concepts are about user trust, but this one targets the correctness of the metric itself rather than how degraded states are communicated.
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]**: Both help explain “contradictory” dashboard numbers, though here the contradiction comes from score-source mismatch rather than population mismatch.

## Sources

- [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]] — documents the shift from raw-edge calibration to served-score calibration, the sparse-bin ECE fix, and the exposure of separate score-source metrics.
