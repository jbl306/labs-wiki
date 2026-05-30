---
title: "Provenance-Stamped Managed Blocks for Upgrade-Safe Agent Installs"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "1e5d1918b741d826e423e9404d456c2e9d9b94ea731fae6a5591d18f7669ee34"
sources:
  - raw/2026-05-30-copilot-session-extending-jbl-dev-kit-workflow-toolkit-c56bdb5a.md
related:
  - "[[Managed-Block Layering for Cross-Repo Agent Installs]]"
  - "[[Cross-Platform Agent Plugin Conversion]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
tier: hot
tags: [managed-blocks, provenance, agent-installation, auditability, rollback, jbl-dev-kit]
---

# Provenance-Stamped Managed Blocks for Upgrade-Safe Agent Installs

## Overview

Provenance-stamped managed blocks are an extension of ordinary managed-block installs in which the block boundary comment carries machine-readable version and timestamp metadata. In the jbl-dev-kit checkpoint, the idea matters because the toolkit already knows how to layer generated instructions safely into downstream repositories, but the next operational problem is showing *which kit version wrote the block* without breaking idempotent comparisons or sync behavior.

## How It Works

The underlying install model is already based on bounded ownership. A toolkit such as jbl-dev-kit writes only the content inside explicit markers like `<!-- jbl-dev-kit:start -->` and `<!-- jbl-dev-kit:end -->`, leaving the rest of the target file under human control. That solves safe insertion, sync, and rollback at the file-content level, but it does not answer a common operational question: if a generated block is sitting inside a repo six weeks later, how can an operator tell *which build of the toolkit* wrote it and when?

Provenance stamps answer that by enriching the marker rather than the payload. Instead of embedding version text inside the managed content itself, the opening marker is allowed to carry an optional suffix such as `<!-- jbl-dev-kit:start v0.1.0 2026-05-30 -->`. The key design constraint from the checkpoint is that the compared content must stay unaffected. In other words, the installer's internal `extractManagedBlock()` and in-sync checks should still compare only the payload between the markers. The stamp is operational metadata, not part of the semantic content being rendered for the runtime.

That design leads directly to the regex requirement called out in the source. The marker parser must accept both the original plain form and the stamped form, using a non-greedy allowance before the comment close. Conceptually, the parser shifts from matching exactly `<!-- jbl-dev-kit:start -->` to matching something closer to `<!-- jbl-dev-kit:start.*?-->`. This preserves backward compatibility with older installs and keeps the update path one-way safe: old files without stamps still parse, while new files can expose provenance immediately after the toolkit version is threaded through the installer.

The checkpoint also spells out the thread that carries the stamp. The version originates in `package.json`, while the install date is supplied by the installer at write time. That metadata then moves through `compile/lib/managed-block.mjs` and `compile/lib/install.mjs` until the final `upsertManagedBlock(existing, content, stamp)` call renders the block. The important subtlety is that the default must remain the unstamped marker. Existing unit tests call the helper with only `(existing, content)` and assert the exact legacy marker string, so the stamp has to be optional. In effect, provenance becomes an additive capability layered on top of the stable managed-block contract.

Why does this work better than putting version text inside the generated block body? Because block bodies are what downstream runtimes consume and what sync logic compares. If version text lived inside the payload, a no-op reinstall from the same semantic source could still look like content churn if the timestamp changed. By isolating provenance in the comment boundary, the system gains traceability without making the downstream instruction surface noisier or more brittle. Humans inspecting the file can see the writer and date immediately, while the machine still treats the rendered payload as the source of truth for convergence.

The pattern also improves rollback hygiene. Suppose an operator finds a generated block in a repository and wants to know whether it came from the current installed kit or an older build that should be replaced. With plain managed blocks, the operator often has to infer that from git blame or external notes. With stamped blocks, the block carries its own origin signal. That makes support, audits, and fleet-wide upgrade validation easier across many sibling repositories. It is especially useful in multi-repo agent environments where the same toolkit may be writing `AGENTS.md`, `CLAUDE.md`, or Copilot instruction surfaces into several projects at different times.

At a systems level, provenance-stamped blocks are a trust mechanism. They preserve the low-risk merge semantics of [[Managed-Block Layering for Cross-Repo Agent Installs]] while making generated overlays more inspectable. They also align with compile-once knowledge habits: once a block is written, the file itself retains enough metadata to explain where it came from, instead of requiring operators to reconstruct that history from transient session state.

## Key Properties

- **Backward-compatible parsing**: both plain and stamped markers are accepted by the same block extractor.
- **Comparison-safe metadata**: version/date data lives in the marker comment instead of the managed payload, so semantic diffing stays stable.
- **Optional stamping**: legacy behavior remains the default, which protects existing tests and previously written files.
- **Human-visible provenance**: operators can inspect a target file and immediately identify which toolkit version last wrote the managed region.
- **Upgrade-friendly rollback**: stamps make it easier to distinguish stale generated overlays from current ones during audits or support work.

## Limitations

Provenance stamps improve observability, not correctness. A stamped block can still contain bad content if the compiler emitted the wrong instructions. The pattern also depends on consistent marker parsing across every runtime-specific writer; if one adapter writes stamped markers and another still assumes the plain form only, sync behavior can drift. Finally, stamps provide write-time metadata, not full change history: they tell you the last known writer, but not the entire sequence of prior updates.

## Examples

One safe implementation shape looks like this:

```javascript
const START_RE = /<!--\s*jbl-dev-kit:start.*?-->/;
const END_RE = /<!--\s*jbl-dev-kit:end\s*-->/;

function startMarker(stamp = "") {
  return stamp
    ? `<!-- jbl-dev-kit:start ${stamp} -->`
    : "<!-- jbl-dev-kit:start -->";
}
```

Rendered output might become:

```markdown
<!-- jbl-dev-kit:start v0.4.2 2026-05-30 -->
## Generated workflow overlay
- managed by jbl-dev-kit
<!-- jbl-dev-kit:end -->
```

The installer still compares only `## Generated workflow overlay ...` when deciding whether the block is already in sync.

## Practical Applications

This pattern is useful anywhere a shared automation toolkit installs generated instructions into many downstream repositories and later needs to support audit, rollback, or fleet-wide upgrade verification. It is especially strong for agent-tooling stacks, because those stacks often update prompts and policies centrally while needing repo-local trust that generated overlays are fresh, explainable, and reversible.

## Related Concepts

- **[[Managed-Block Layering for Cross-Repo Agent Installs]]**: provenance stamps build on managed blocks by making machine-owned regions attributable, not just safe to update.
- **[[Cross-Platform Agent Plugin Conversion]]**: compilation decides what should be emitted; provenance-stamped blocks make the install path auditable after emission.
- **[[Durable Copilot Session Checkpoint Promotion]]**: both patterns turn transient execution history into durable, inspectable artifacts.

## Sources

- [[Copilot Session Checkpoint: Extending jbl-dev-kit workflow toolkit]] — source of the optional stamp design, regex constraint, and `package.json` version-threading plan.

