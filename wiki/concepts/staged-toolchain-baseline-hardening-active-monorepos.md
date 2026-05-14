---
title: "Staged Toolchain Baseline Hardening for Active Monorepos"
type: concept
created: 2026-05-14
last_verified: 2026-05-14
source_hash: "0d94d553ecb570bca3b0848b2cbd97ce0d128da1be62cba460dd45e8f868efe2"
sources:
  - raw/2026-05-14-copilot-session-implementing-s6-sprint-foundation-sds-100-102-10-4831f34a.md
related:
  - "[[Phased Progress Tracking With Validation Gates]]"
  - "[[Agent Skill Routing Architecture]]"
tier: hot
tags: [tooling, monorepo, linting, type-checking, staged-hardening, eslint, ruff, mypy]
---

# Staged Toolchain Baseline Hardening for Active Monorepos

## Overview

Staged toolchain baseline hardening is the practice of introducing linting, formatting, type checking, and pre-commit discipline in a codebase that is still undergoing major structural refactors, without letting the hardening work overwhelm or block the roadmap. The central idea is to make the repository measurably stricter than before, but only by enforcing checks the current architecture can realistically satisfy and by explicitly documenting the debt that remains.

## How It Works

The workflow starts from an uncomfortable but common state: a monorepo already has real product momentum, but its quality surface is still inconsistent. Some directories may have no toolchain config at all, a "lint" command may secretly just be a type-check alias, and the most strategically important files may already be large enough that a repo-wide formatter would explode the diff. In that situation, the right first move is not to demand perfection. It is to define a baseline that is **strict enough to be real** and **narrow enough to be survivable**.

In the checkpoint that motivated this concept, the API side was hardened first because it could absorb structure more safely. The repo added `apps/api/pyproject.toml` with Ruff, mypy, and pytest settings, plus a dedicated `requirements-dev.txt` that pinned `ruff==0.7.4`, `mypy==1.13.0`, and `pre-commit==4.0.1`. That is an important design choice: the baseline is not just "install some tools"; it is a versioned contract for the branch. The Ruff configuration selected `E`, `F`, `I`, `B`, and `UP` families but still ignored `E501`, `B008`, and `B904`, which means the baseline focused on correctness, import ordering, and obvious bug patterns before it tried to police line length or opinionated exception style everywhere.

The next move is to keep formatting pressure proportional to the codebase's refactor horizon. A full `ruff format .` would have produced roughly 1200 lines of churn across 18 files, including modules scheduled for near-term decomposition. Instead of forcing that diff through review, the session used `ruff check --fix .`, which delivered import sorting and low-risk cleanups across 13 files. This is the essence of the staged model: prefer changes that improve signal for future reviews without burying the next roadmap tasks under unrelated formatting noise. Hardening succeeds only if people will keep it turned on after the first pass.

Type checking follows the same philosophy. Mypy initially reported seven errors across four modules: `spatial_api.main`, `spatial_api.schemas`, `spatial_api.storage`, and `spatial_api.reference.proposals`. The checkpoint did **not** respond by disabling mypy globally or pretending the errors did not matter. Instead, it used targeted `ignore_errors = true` overrides for those modules. That preserves a useful invariant: the project now knows exactly where its type debt lives, and all other modules still benefit from type checking. Staged hardening therefore treats "green" as **bounded honesty**, not as fake cleanliness.

On the frontend side, baseline hardening often requires replacing placeholder checks with domain-aware real ones. Here, the old `lint` command was only `tsc --noEmit`, which duplicated `typecheck` and left the JavaScript/React surface largely ungoverned. The session changed `lint` to `typecheck && lint:js`, added ESLint 9, Prettier, and associated plugins, and then discovered that `eslint-config-next` plus `FlatCompat` triggered a "circular structure to JSON" failure. Rather than freezing work on tool incompatibility, the branch switched to a direct flat config using `@next/eslint-plugin-next`, `typescript-eslint`, `eslint-plugin-react`, and `eslint-plugin-react-hooks`. In other words, the baseline is allowed to change shape as long as the enforcement surface becomes more real, not less.

A staged baseline also has to respect domain-specific syntax. The checkpoint's remaining ESLint errors were dominated by `react/no-unknown-property` on React Three Fiber scene props like `position`, `args`, `roughness`, `castShadow`, `receiveShadow`, `rotation`, and `transparent`. Those are valid in a 3D JSX scene graph even though the generic React rule does not recognize them. The correct response is not to edit the scene into a worse API shape just to satisfy a browser-DOM-oriented rule. It is to scope or disable the rule in that domain. That decision preserves the semantic correctness of the application while still keeping the rest of ESLint active.

The final stage is to convert ad hoc local success into repository habit. In this checkpoint, the next steps were a root `.pre-commit-config.yaml`, a root `.editorconfig`, and later CI gates through `scripts/ci/run-gates.sh` plus GitHub Actions. This ordering matters. Pre-commit and editor config stabilize developer behavior locally; CI only becomes valuable once local rules are trustworthy enough that contributors can pass them without ritual frustration. A staged baseline therefore expands in concentric circles: repo-local config, low-churn autofixes, bounded type debt, domain-aware lint exceptions, commit hooks, and only then automated gates that run everywhere.

The trade-off is deliberate incompleteness. Some warnings remain acceptable, some modules are explicitly ignored, and some formatters are deferred until larger refactors land. But this incompleteness is governed rather than accidental. The concept works because it transforms "we should clean this up later" into a sequence of concrete, reviewable milestones that improve everyday engineering immediately.

## Key Properties

- **Version-pinned tooling introduction:** Baselines are anchored in explicit config files and dependency pins rather than ambient local installs.
- **Low-churn first pass:** Safe autofixes such as import sorting land before repo-wide formatting that would obscure semantic review.
- **Bounded debt accounting:** Type or lint exceptions are scoped to named modules or known domains instead of disabled wholesale.
- **Domain-aware rule calibration:** Framework-specific syntax such as React Three Fiber JSX is treated as first-class input, not as an anomaly to silence by hand.
- **Progressive enforcement surface:** Local config and scripts become pre-commit hooks and then CI gates only after the checks are stable enough to be trusted.

## Limitations

Staged baselines can normalize temporary exceptions if the follow-up work never lands. Module-level mypy ignores and disabled lint rules are safe only when they are documented as debt with a credible owner. The approach also depends on engineers resisting the urge to sneak in broad formatter churn during unrelated branches. If the repo lacks discipline around roadmap sequencing, a staged baseline can devolve into a pile of permanent carve-outs.

## Examples

The pattern often looks like this in practice:

```toml
[tool.ruff]
target-version = "py312"
lint.select = ["E", "F", "I", "B", "UP"]
lint.ignore = ["E501", "B008", "B904"]

[[tool.mypy.overrides]]
module = ["spatial_api.main", "spatial_api.schemas"]
ignore_errors = true
```

```js
export default [
  {
    rules: {
      "react/no-unknown-property": "off",
    },
  },
];
```

Those snippets are not about lowering standards. They are about choosing standards that match the repository's actual state while keeping a path open to stronger enforcement later.

## Practical Applications

This concept is useful when a team inherits an active monorepo, when a side project starts maturing into a production service, or when a repository is about to enter CI hardening but still contains large files scheduled for decomposition. It is especially effective in mixed Python/TypeScript stacks where different subtrees can tolerate different levels of strictness at the same time. In those settings, staged baseline hardening gives the team a way to improve reviewability, catch real bugs earlier, and prepare for CI without turning tool adoption into its own destabilizing migration.

## Related Concepts

- **[[Phased Progress Tracking With Validation Gates]]**: Both approaches break work into explicit checkpoints, but staged baseline hardening focuses on quality-tool rollout inside a live codebase rather than generic phase management.
- **[[Agent Skill Routing Architecture]]**: Repository-local workflows and skill surfaces make it easier to apply the baseline consistently across branches and contributors.
- **[[Universal Agent Schema (AGENTS.md) for AI Tool Integration]]**: A stable agent contract helps future automated sessions respect the same toolchain boundaries and validation expectations.

## Sources

- [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]] — documents the exact Ruff, mypy, ESLint, and Prettier choices, along with the reasons some checks were intentionally deferred.
