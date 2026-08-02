---
title: "Sealed Review Publication"
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: "0662c95f97a999e095421b9c41509fa89d7d7d27f75ce095bf118482790ed0bd"
sources:
  - raw/2026-07-09-github-ingestion-phase-3-delivery.md
related:
  - "[[Non-Authorizing Lifecycle Records]]"
  - "[[Artifact Registry Validation in ML Pipelines]]"
  - "[[Clean Worktree-Based Development for Wiki Curation Pipelines]]"
tier: hot
tags: [github, code-review, artifact-integrity, branch-safety, security]
---

# Sealed Review Publication

## Overview

Sealed review publication is a delivery pattern for publishing a generated repository review only when the review's identity, evaluation record, and branch contents are all bound to the same exact artifact. It treats a review pull request as a constrained transport envelope rather than as proof that a change is approved or safe to apply. The Phase 3 GitHub-ingestion delivery uses this pattern to make automated review publishing idempotent and resistant to accidental branch pollution.

## How It Works

The first problem is incomplete identity. A Phase 2 artifact manifest contains enough information to describe the review package but excludes `evaluation.json`. Publication and adoption cannot rely on the manifest alone because the evaluation is part of the security and correctness boundary. The publisher therefore recomputes the identity fields and verifies a separate hash seal over the complete evaluation record. This makes the evaluation an independently checked input instead of an implicitly trusted sidecar.

Next, the publisher starts from a pristine base clone. This is important because latest-star discovery can update local state after the review command has started. If the same checkout were reused for publication, unrelated local changes could be mistaken for review output. A clean clone establishes a stable comparison point and narrows the set of files that can legitimately appear in the delivery branch.

The branch check compares the complete report-branch delta with the base branch, not merely the contents of a presumed report directory. The allowed delta is exact: `review.md`, `evaluation.json`, and `publication.json`, all belonging to the evaluated artifact. Any extra file, unexpected path, or mismatched evaluation causes publication to fail. This is stronger than checking that required files exist because it also detects pollution by generated state, operator edits, or unrelated changes.

The delivery path is idempotent. Repeating a publication request for the same evaluation should update or reuse the existing report pull request rather than create ambiguous duplicates. Idempotency depends on binding the request to the exact evaluation identity and on deterministic branch and publication behavior. The implementation adds branch-collision checks, remote and repository binding, non-force pushes, and mocked create, update, close, and merge behavior to exercise those cases.

Credentials are part of the seal boundary. The narrow GitHub credential must cover both REST calls and Git transport, but the transport uses clean HTTPS remotes and environment-only extra-header configuration. It does not fall back to the operator's broader SSH authority or place tokens in command arguments. This reduces accidental privilege expansion and keeps secrets out of process-visible CLI parameters.

The result is a publication mechanism with two separate claims: first, that the delivered report exactly matches a sealed evaluation; second, that the report was transported through an allowed GitHub workflow. Neither claim authorizes applying a change. That separation lets the system publish useful review evidence while reserving any future adoption mechanism for a distinct, explicitly bound workflow.

## Key Properties

- **Exact artifact binding:** Identity fields and the complete `evaluation.json` record are recomputed and hash-verified.
- **Branch purity:** The full branch delta is checked against an allowlist of three report files.
- **Pristine comparison base:** Publication is isolated from local state changes caused by review-time discovery.
- **Idempotent delivery:** Repeated requests for one evaluation can update or reuse the corresponding report pull request.
- **Credential minimization:** REST and Git use narrow, environment-configured HTTPS credentials rather than broader SSH authority.

## Limitations

The pattern proves integrity and delivery constraints, not the truth of the review's conclusions. A sealed evaluation may still contain a mistaken judgment. The exact allowlist also assumes the report format remains limited to `review.md`, `evaluation.json`, and `publication.json`; legitimate format expansion requires a deliberate schema and publisher change. The Phase 3 result does not yet provide the scheduled worker or target-specific multi-file adoption planned for later phases.

## Examples

An abstract publication check can be expressed as:

```python
identity = recompute_identity(review_artifact)
assert verify_hash(evaluation_json, identity.evaluation_hash)
assert branch_delta(base, report_branch) == {
    "review.md", "evaluation.json", "publication.json"
}
assert remote_matches_expected_repository(report_branch)
publish_or_update_report_pull_request(identity)
```

The important property is that every assertion is evaluated against the same exact evaluation, rather than against whichever report files happen to be present locally.

## Practical Applications

Use sealed publication when an automated system must expose review output through pull requests without allowing the publication path to become an implicit deployment or approval path. It is applicable to repository audits, dependency reviews, generated compliance reports, and other workflows where artifact identity and branch cleanliness matter more than merge convenience.

## Related Concepts

- **[[Non-Authorizing Lifecycle Records]]**: Keeps publication and adoption history auditable without turning records into apply authority.
- **[[Artifact Registry Validation in ML Pipelines]]**: Shares the principle that artifact identity and integrity must be checked at delivery boundaries.
- **[[Clean Worktree-Based Development for Wiki Curation Pipelines]]**: Provides the broader isolation principle behind pristine publication checkouts.

## Sources

- [[GitHub Ingestion Phase 3 Review Delivery]]
