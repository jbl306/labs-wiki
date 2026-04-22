---
title: NousResearch/autoreason
type: source
created: '2026-04-21'
last_verified: '2026-04-21'
source_hash: fa541749897b9f7b80e6458c2d972050d87a3e54aff9fbcd82146ac2fd666cf6
sources:
- raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
source_url: https://github.com/NousResearch/autoreason
tags:
- github
- tex
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
quality_score: 50
---

# NousResearch/autoreason

## Summary

Autoresearch for subjective domains.

## Repository Info

- **Source URL**: https://github.com/NousResearch/autoreason
- **Stars**: 495
- **Primary language**: TeX

## README Excerpt

# Autoreason: Self-Refinement That Knows When to Stop

**SHL0MS | HERMES AGENT**

[Paper (PDF)](paper/autoreason.pdf) · [Human Eval Materials](human_eval/)

---

Iterative self-refinement fails for three structural reasons: *prompt bias* (models hallucinate flaws when asked to critique), *scope creep* (outputs expand unchecked each pass), and *lack of restraint* (models never say "no changes needed"). Autoreason fixes all three.

Each iteration produces three competing versions — the **unchanged incumbent (A)**, an **adversarial revision (B)**, and a **synthesis (AB)** — judged by fresh agents with no shared context via blind Borda count. "Do nothing" is always a first-class option.

## Activity Snapshot

### Recent Commits

- 2026-04-12 538f881 SHL0MS: chore: recompile PDF with corrected citations
- 2026-04-12 4bb1f02 SHL0MS: fix: correct 4 fabricated/wrong citations in bibliography
- 2026-04-03 bbe6dc1 shl0ms: Integrate Haiku 4.5 results, update framing to five-tier scaling curve
- 2026-04-02 61a5157 shl0ms: Rewrite README, add ablation/haiku45 results, remove outdated OVERVIEW.md and RESULTS.md
- 2026-04-02 f2260a6 shl0ms: Add component ablation, aggregation comparison, update intro/abstract/conclusion/discussion with ablation findings
- 2026-04-02 6746dff shl0ms: Add judge panel size ablation (1v3v7) and length-controlled evaluation results
- 2026-04-02 9c464e9 shl0ms: Layout refinements: shorter abstract, wider tables, better spacing, increased line spread
- 2026-04-02 c53c050 shl0ms: Author: SHL0MS | HERMES AGENT
- 2026-04-02 db2b36e shl0ms: Fix overfull hboxes, format model list in reproducibility appendix
- 2026-04-02 0f6a9e4 shl0ms: Fig 1: nudge winner->new A lower and left
- 2026-04-02 bef2222 shl0ms: Fig 1: center fresh x3 badge with judge panel box
- 2026-04-02 b135231 shl0ms: Fig 1: horizontal 'winner -> new A' label above gray arrow
- 2026-04-02 356c64c shl0ms: Fix fig 1 label overlap: bump unchanged/synthesis/revision labels lower
- 2026-04-02 12a2576 shl0ms: Title: Autoreason: Self-Refinement That Knows When to Stop
- 2026-04-02 8da20c8 shl0ms: lowercase the
- 2026-04-02 ccceee3 shl0ms: Title: Autoreason: Resolving The Self-Refinement Paradox
- 2026-04-02 f5a864f shl0ms: Fix figure 1 overflow (resizebox), widen table 17, add section breaks before references/appendix/repro
- 2026-04-02 62193a1 shl0ms: Strengthen claims where data supports: remove over-hedging in abstract, intro conditions, conclusion, scope discussion
- 2026-04-02 d74d8ad shl0ms: Single-column layout, larger figures, 1in margins
- 2026-04-02 2b6c44f shl0ms: Recompile PDF with Latin Modern (was missing lmodern.sty)

## Crawled Files

Source dump in `raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md` includes:

- `.gitignore`
- `experiments/prior/runs/run_01_fixed_order/README.md`
- `human_eval/README.md`
- `human_eval_answer_key.json`
- `experiments/prior/config_matrix.yaml`
- `experiments/prior/evaluation/blind_pairs/task_01_pair_01.md`
- `experiments/prior/evaluation/blind_pairs/task_01_pair_02.md`
- `experiments/prior/evaluation/blind_pairs/task_01_pair_03.md`
- `experiments/prior/evaluation/blind_pairs/task_01_pair_04.md`
- `experiments/prior/evaluation/blind_pairs/task_02_pair_01.md`
