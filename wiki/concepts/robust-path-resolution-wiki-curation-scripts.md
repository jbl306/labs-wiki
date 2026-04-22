---
title: "Robust Path Resolution in Wiki Curation Scripts"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "4f6f78933f56d8ae7e529c0883a3bea68f61cc64465402d8aa421afc538919d5"
sources:
  - raw/2026-04-20-copilot-session-second-curation-reports-23bcd48f.md
quality_score: 46
concepts:
  - robust-path-resolution-wiki-curation-scripts
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Copilot Session Checkpoint: Second Curation Reports]]"
tier: hot
tags: [path-resolution, wiki-curation, scripting, automation, robustness]
---

# Robust Path Resolution in Wiki Curation Scripts

## Overview

Robust path resolution is a critical implementation detail in scripts that operate across multiple wiki roots or external directories. By dynamically deriving the project root from the provided wiki directory, scripts avoid hardcoded assumptions and ensure correct file discovery, result path generation, and write operations regardless of the execution context.

## How It Works

Many curation scripts are initially written with the assumption that all operations occur relative to a fixed project root (e.g., `ROOT`). This works in simple setups but fails when the script is used with external or live wiki trees, such as during targeted curation passes or when integrating with host-side auto-ingest pipelines.

The robust approach is to accept a `--wiki` argument specifying the target wiki directory, then resolve the actual project root as the parent of this directory. All subsequent operations—such as raw checkpoint lookup, path normalization, and file writes—are performed relative to this dynamically determined root, not a hardcoded path.

This change prevents errors like `ValueError: path.relative_to(ROOT)` when the script encounters files outside the expected directory structure. It also ensures that results are written to the correct location, whether operating in a clean worktree, a live host checkout, or an external repository.

The implementation involves updating all path resolution logic in the script: for example, replacing `ROOT / r["path"]` with `project_root / r["path"]`, and ensuring that all functions receive and use the correct `project_root` parameter. This makes the script portable, robust, and suitable for use in a variety of development and production environments.

Testing and validation are performed by running the script against known checkpoint pages in both clean and dirty environments, confirming that files are discovered, processed, and written as expected. Once validated, the fix is merged back to main and documented in the curation report.

## Key Properties

- **Dynamic Project Root Resolution:** Derives the root directory from the provided wiki path, ensuring correct operation in any environment.
- **Consistent File Discovery and Writes:** All lookup, normalization, and write operations use the resolved project root, preventing path errors.
- **Portability:** Script can be used in clean worktrees, live host checkouts, or external repositories without modification.

## Limitations

Requires careful code review to ensure all path operations are updated; missing a single hardcoded reference can result in subtle bugs. May introduce complexity if the script must support legacy usage patterns or multiple directory layouts.

## Example

The script `backfill_checkpoint_curation.py` originally failed when run with `--wiki /home/jbl/projects/labs-wiki/wiki`, as it attempted to resolve paths relative to `ROOT`. After the fix, it derives `project_root = wiki_dir.parent` and uses this for all subsequent operations, successfully processing and writing curated checkpoints in the live wiki tree.

## Visual

No images, but the technical details section provides a step-by-step breakdown of the path resolution bug and its fix.

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Both require robust, portable path handling for reliable operation.

## Practical Applications

Enables reliable curation, backfill, and editorial workflows in large wiki systems with multiple roots or deployment environments. Critical for teams that need to process live, external, or host-mounted wiki directories without manual path adjustments.

## Sources

- [[Copilot Session Checkpoint: Second Curation Reports]] — primary source for this concept
