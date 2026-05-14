---
title: "Foundation Hardening vs Completion Closeout in Spatial Design Studio S6"
type: synthesis
created: '2026-05-14'
last_verified: '2026-05-14'
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-14-copilot-session-implementing-s6-sprint-foundation-sds-100-102-10-4831f34a.md
  - raw/2026-05-14-copilot-session-completing-s6-roadmap-212ec880.md
concepts:
  - staged-toolchain-baseline-hardening-active-monorepos
  - behavior-preserving-monolith-decomposition-live-services
related:
  - "[[Spatial Design Studio]]"
  - "[[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]"
  - "[[Copilot Session Checkpoint: Completing S6 Roadmap]]"
tier: hot
tags: [spatial-design-studio, roadmap, refactoring, tooling, deployment, synthesis]
---

# Foundation Hardening vs Completion Closeout in Spatial Design Studio S6

## Question

How should a live product sequence sprint work so that toolchain hardening makes later architectural decomposition safer instead of competing with it?

## Summary

The two S6 checkpoints describe a deliberate handoff between phases rather than two unrelated batches of work. The foundation checkpoint establishes branch discipline, shared gates, and a survivable lint/type baseline; the completion checkpoint spends that new discipline on the risky part of the roadmap by decomposing the largest API and web surfaces, then closing the sprint with merges, deploy, and cleanup.

## Comparison

| Dimension | [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]] | [[Copilot Session Checkpoint: Completing S6 Roadmap]] |
|-----------|---------------|---------------|
| Main risk being managed | Tooling chaos and unreviewable baseline churn | Behavioral drift during large API and UI refactors |
| Primary move | Introduce staged Ruff/mypy/ESLint/CI discipline | Extract routers, services, repositories, panels, and helpers while preserving contracts |
| Intentional deferral | Strict formatting and high-risk large-file decomposition | Deep hook extraction and final production verification from the current environment |
| Proof of success | Local gates, pinned configs, issue/branch/PR workflow | Same gates on refactored code, merge to `main`, homelab redeploy, explicit cleanup steps |
| Architectural result | Repo becomes safe enough for larger changes | Monolithic hot spots become thinner shells with reusable internal seams |
| Durable lesson | Strictness should follow repo reality | Refactors should preserve runtime behavior before chasing architectural purity |

## Analysis

The foundation checkpoint is valuable because it refuses a common failure mode: trying to clean up everything at once. Its staged baseline hardening says the repo first needs trustworthy issue/branch/PR mechanics, version-pinned tools, and a lint/type surface that creates signal instead of diff noise. That is not "preparatory fluff." It is what makes the later decomposition reviewable.

The completion checkpoint then uses that groundwork exactly as intended. Instead of treating SDS-103 and SDS-104 as cosmetic cleanup, it decomposes the places where the system was most fragile: the FastAPI app shell and the studio web shell. The interesting part is not only that files were split. It is that the split was constrained by unchanged endpoint paths, auth dependencies, response models, status codes, database commits, and audit event names on the backend, while the frontend kept the highest-risk orchestration logic in place rather than over-extracting for aesthetics.

Together, the checkpoints show that sequencing matters. If strict formatting, mypy cleanups, and ESLint rollout had been forced during the same branch as the 1,145-line API split and 1,314-line web-shell split, review signal would likely have collapsed. By first building a staged baseline and only then spending it on architecture, the team got both kinds of progress: safer delivery mechanics and real structural improvement.

The closeout details are what turn the second checkpoint from "refactor diary" into durable operational knowledge. The sprint is not considered done at merge time alone; it also updates roadmap registries, advances the active sprint pointer, redeploys through homelab, records stale remote-ref cleanup, and leaves exact production-verification commands. That makes S6 completion a full delivery pattern, not just a code movement pattern.

## Key Insights

1. **Baseline hardening is most valuable when it creates room for later high-risk refactors.** — supported by [[Staged Toolchain Baseline Hardening for Active Monorepos]], [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]
2. **Large-file decomposition should preserve contracts first and improve purity second.** — supported by [[Behavior-Preserving Monolith Decomposition for Live Services]], [[Copilot Session Checkpoint: Completing S6 Roadmap]]
3. **A sprint is only truly closed when code, roadmap state, deployment state, and branch state all agree.** — supported by [[Copilot Session Checkpoint: Completing S6 Roadmap]]

## Open Questions

- When should the remaining `StudioShell` orchestration be extracted into hooks or stores, and what new tests would be required first?
- Which of the temporary web lint warnings are safe to keep as baseline noise, and which should become the first S7 cleanup targets?
- Should the repo add an explicit "post-merge production verification" checklist so future roadmap closeouts do not depend on one checkpoint handoff?

## Sources

- [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]
- [[Copilot Session Checkpoint: Completing S6 Roadmap]]
