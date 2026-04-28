---
title: "Reference-Safe Artifact Pruning in Shared Model Registries"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "6caf80ac3afa85f4adf295e7c39d6eeba187acacd73f68dd65fc123c58576db1"
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-hardening-404bc17e.md
related:
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[Registry Health Validation via Scheduled Cron]]"
  - "[[Atomic Save Pattern for Model Artifacts]]"
tier: hot
tags: [artifact-registry, ml-ops, pruning, model-registry, reliability, production]
quality_score: 65
---

# Reference-Safe Artifact Pruning in Shared Model Registries

## Overview

Reference-safe artifact pruning is a model-lifecycle discipline in which cleanup code deletes an artifact file only if no kept registry entry still references that same path. It matters because registries often behave like logical version stores while the filesystem underneath behaves like a mutable shared namespace; if pruning assumes one row equals one unique file, normal cleanup can silently break production.

## How It Works

The checkpoint reveals a particularly dangerous form of registry drift. The `model_registry` table tracked multiple historical rows for a model family, but those rows did not always point to unique versioned artifacts. Instead, some used shared, unversioned paths such as `/app/models/reb/ensemblemodel.pkl`. That means an older non-production row and a newer kept or production row could reference the exact same file on disk. Logically, the rows were different versions. Physically, they shared one artifact.

That breaks a naive pruning algorithm. A simple implementation of `prune_old_models()` often looks like this: determine which registry rows are old, delete those rows' artifact files, then remove the rows from the database. This works only under a hidden assumption that each pruned row uniquely owns its artifact path. Once that assumption fails, filesystem cleanup becomes destructive. Deleting the file for a pruned row can also delete the file for a retained row, because the file is the same file.

The checkpoint surfaced this bug through operational evidence rather than code inspection alone. `registry-health` reported missing artifacts for `MinutesModel_minutes`, `EnsembleModel_reb`, `RidgeModel_ast`, `EnsembleModel_tov`, and `RidgeModel_fg3m`. At first glance that can look like a training or deployment failure. The deeper diagnosis was that pruning old rows could unlink artifact files still needed by kept rows. This is a classic reference-integrity bug crossing the database/filesystem boundary.

The hardening fix introduced `_delete_artifact_if_unreferenced()`. Conceptually, the helper asks a single question before unlinking: “After pruning this row, does any kept row still reference the same artifact path?” If the answer is yes, the cleanup step skips deletion. If the answer is no, the file can be safely removed. The invariant is simple:

$$
\text{delete}(p) \iff \mathrm{refcount}_{\text{kept}}(p) = 0
$$

where $p$ is an artifact path and $\mathrm{refcount}_{\text{kept}}(p)$ counts kept rows pointing to that path after the prune decision.

This idea turns artifact pruning into a reference-management problem rather than a row-deletion problem. The registry decides which entries remain authoritative, and the filesystem layer deletes only files that are no longer reachable from any authoritative entry. In database terms, the artifact path behaves like a shared resource with weak reference counting. In storage terms, pruning becomes safe garbage collection rather than eager unlinking.

The checkpoint also shows why validation and repair workflows remain necessary even after the pruning fix. Once shared files had already been deleted, the system could not restore them by marking rows differently. The missing artifacts had to be rebuilt through existing training commands: minutes via `train_minutes_model(session)`, other stats via `python main.py train --stat ... --model ...`. This is important operationally: validation detects the failure, pruning safety prevents recurrence, and retraining remediates already-lost artifacts.

Another useful lesson is that row uniqueness and artifact uniqueness should be treated as separate design choices. Ideally, each registry entry would point to a versioned immutable artifact, making pruning trivial. But many real systems use stable “current model” paths for convenience, especially when swapping files in place. In those systems, cleanup code must explicitly defend against shared-path aliasing. Otherwise, retention policies turn into production breakage policies.

The final state in the checkpoint demonstrates the payoff. After the pruning fix and artifact rebuilds, `registry-health` returned `ok` with `missing_count=0`. That does not mean the design is perfect; it means the cleanup invariant now matches the actual storage model. The registry can retain history without treating shared artifacts as disposable.

## Key Properties

- **Reference-aware deletion**: Files are removed only when no kept row still points at the same artifact path.
- **Cross-layer integrity**: The database cleanup policy respects filesystem aliasing rather than assuming one-to-one row/file ownership.
- **Operational detectability**: Scheduled registry-health checks reveal when reference safety was previously violated.
- **Safe compatibility with shared paths**: The pattern works even when artifact paths are stable and unversioned.
- **Remediation separation**: Prevention lives in pruning logic; repair lives in retraining or artifact regeneration workflows.

## Limitations

Reference-safe pruning prevents one class of deletion bug but does not fix all artifact problems. A referenced file can still be corrupt, stale, manually removed, or semantically wrong for the row that points to it. The pattern also depends on complete visibility into kept rows; if another external system references the same path without registry visibility, deletion can still be unsafe. Finally, shared mutable paths remain more fragile than immutable versioned artifacts, so this fix is safer than the previous design but still not the strongest possible design.

## Examples

```python
def delete_artifact_if_unreferenced(artifact_path, kept_entries):
    still_referenced = any(
        entry.artifact_path == artifact_path for entry in kept_entries
    )
    if not still_referenced:
        Path(artifact_path).unlink(missing_ok=True)

def prune_old_models(pruned_entries, kept_entries):
    for entry in pruned_entries:
        delete_artifact_if_unreferenced(entry.artifact_path, kept_entries)
        delete_registry_row(entry)
```

The key idea is that cleanup runs against the post-prune reference set, not against the row being deleted in isolation.

## Practical Applications

This concept is useful in any ML platform, feature store, or deployment registry that keeps historical metadata while reusing stable artifact paths. It applies to model registries, rules-engine bundles, serialized embeddings, and even container-image metadata if logical versions can alias physical storage. In the labs-wiki workspace, it is especially relevant to [[NBA-ML Model Registry]] operations: artifact-validation jobs and model-promotion logic are much safer when pruning treats artifacts as shared references rather than disposable per-row payloads.

## Related Concepts

- **[[Artifact Registry Validation In ML Pipelines]]**: Validation detects missing production artifacts; reference-safe pruning prevents one important way they go missing.
- **[[Registry Health Validation via Scheduled Cron]]**: Scheduled health checks are the operational mechanism that surfaced the shared-path bug.
- **[[Atomic Save Pattern for Model Artifacts]]**: Atomic save protects write integrity, while reference-safe pruning protects delete integrity.

## Sources

- [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]] — documents the shared-path prune bug, the `_delete_artifact_if_unreferenced()` fix, and the follow-up artifact rebuild workflow.
