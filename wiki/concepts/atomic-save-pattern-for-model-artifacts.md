---
title: "Atomic Save Pattern For Model Artifacts"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "924e132f95d9fa94650d78f540b91683d2ddb7c4f20d9fb9d776cf74f1885c5a"
sources:
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
quality_score: 100
concepts:
  - atomic-save-pattern-for-model-artifacts
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]]"
tier: hot
tags: [atomic save, artifact integrity, ML deployment, filesystem, robustness]
---

# Atomic Save Pattern For Model Artifacts

## Overview

The atomic save pattern is a robust method for writing model artifacts to disk, ensuring data integrity by preventing partial writes and handling failures gracefully. Originally implemented for EnsembleModel, it is now extended to all base models in the NBA ML Engine to guarantee reliable artifact persistence.

## How It Works

The atomic save pattern addresses the risk of corrupted or incomplete model artifacts caused by interruptions or errors during the write process. The approach leverages temporary files and filesystem synchronization to ensure that only fully written artifacts are visible to downstream consumers.

**Step-by-Step Process:**
1. **Create Temporary File**: Use `tempfile.mkstemp` to create a uniquely named temporary file in the target directory. This file is not visible to other processes as the final artifact.
2. **Write Payload With Flush and Sync**: Open the temporary file descriptor, write the pickled model payload, flush the buffer, and call `os.fsync` to ensure the data is physically written to disk.
3. **Atomic Replace**: Use `os.replace(tmp_path, path)` to atomically move the temporary file to the intended artifact path. This operation is guaranteed to be atomic by the underlying filesystem, so consumers never see a partially written file.
4. **Cleanup On Failure**: If any exception occurs during writing or replacing, the temporary file is deleted to avoid clutter and confusion.

**Integration With Model Classes:**
- Each model class (CatBoost, XGBoost, LightGBM, RandomForest, Ridge) implements a `save()` method that pickles a dict containing model parameters, feature names, and residuals. The atomic save pattern is applied to these methods, replacing direct writes with the robust sequence outlined above.

**Benefits:**
- Prevents artifact corruption due to process crashes, disk errors, or interrupted writes.
- Ensures that retrain and deployment workflows always operate on valid, complete artifacts.
- Simplifies error recovery and debugging by guaranteeing artifact consistency.

**Testing:**
- Tests patch `pickle.dump` to simulate write failures, verifying that pre-existing artifacts remain unchanged and no temporary files are left behind.
- Byte-level comparisons confirm artifact integrity after successful saves.

## Key Properties

- **Atomicity:** Ensures that artifact writes are all-or-nothing, preventing partial or corrupted files.
- **Filesystem Synchronization:** Uses `os.fsync` to guarantee that written data is physically persisted before replacement.
- **Failure Cleanup:** Deletes temporary files on failure, avoiding orphaned artifacts.
- **Integration With Custom Serialization:** Works seamlessly with model classes that serialize artifacts as pickled dictionaries.

## Limitations

Relies on underlying filesystem support for atomic `os.replace`. May not be portable to networked or exotic filesystems. Does not address artifact integrity if the serialization logic itself is faulty.

## Example

```python
fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
tmp_path = Path(tmp_name)
try:
    with os.fdopen(fd, "wb") as f:
        pickle.dump(payload, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
except Exception:
    try: tmp_path.unlink()
    except FileNotFoundError: pass
    raise
```

## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Both ensure artifact integrity and robust persistence for model files.

## Practical Applications

Used in production ML pipelines to guarantee artifact reliability during retrain, deployment, and automated workflows. Critical for systems where model artifacts are consumed by multiple processes or scheduled jobs, such as NBA ML Engine's daily prediction refresh.

## Sources

- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — primary source for this concept
