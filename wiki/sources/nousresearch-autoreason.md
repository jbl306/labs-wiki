---
title: NousResearch/autoreason
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: fa541749897b9f7b80e6458c2d972050d87a3e54aff9fbcd82146ac2fd666cf6
sources:
- raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
source_url: https://github.com/NousResearch/autoreason
tags:
- github
- tex
tier: warm
knowledge_state: ingested
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- autoreason-iterative-self-refinement-framework
---

# NousResearch/autoreason

## What it is

Autoreason (Nous Research; SHL0MS / Hermes Agent) is a research framework — and accompanying paper — for iterative self-refinement that knows when to stop. Each pass produces three competing versions: the unchanged incumbent A, an adversarial revision B, and a synthesis AB. A panel of fresh judging agents (Borda count, no shared context) picks the winner; "do nothing" is always a first-class option. The repo contains the LaTeX paper, blinded human-evaluation materials, the experiment runners, and the result corpora across writing tasks and CodeContests problems.

## Why it matters

Direct counter to the naive "critique + revise" loop most of us reach for first. Three findings are practically useful for any verification or self-review skill we build (including `superpowers:code-reviewer`, the `code-reviewer` agent skill, or the Ralph-loop pattern): critique-and-revise *destroys* weak models (Haiku 3.5 outputs shrunk 59–70% over 15 passes), 7 judges converge ~3× faster than 3, and the gains vanish once a model crosses ~60% private accuracy on the underlying task — meaning self-refinement has a model-quality floor and ceiling.

## Key concepts

- **A / B / AB tournament** — Incumbent, adversarial revision, synthesis. Each pass three candidates compete. See [[autoreason-iterative-self-refinement-framework]].
- **Blind Borda count** — Judges score with randomized order and neutral labels (Proposal 1/2/3) to defeat positional and label bias.
- **"Do nothing" as a first-class option** — A wins by default if no revision is strictly better; convergence after k=2 incumbent wins.
- **Fresh-agent isolation** — Critic, Author B, Synthesizer, and judges all run with no shared context, preventing critique-loop contamination.
- **Generation-evaluation gap** — Self-refinement only helps when the model can evaluate better than it can generate (transition point ~60% private accuracy on CodeContests).
- **Length-controlled evaluation** — Beats 3 of 4 baselines (21/28 wins) even at matched word count, ruling out "longer = better" confound.

## How it works

```
Task Prompt → Incumbent A
                 ↓
       ┌── Critic (fresh) ──→ Critique
       ├── Author B (fresh) ─→ Revision (B)
       └── Synthesizer ──────→ Synthesis (AB)
                 ↓
         Judge Panel (3 fresh, Borda)
                 ↓
             Winner → new A   (or converge if A wins k=2)
```

- Writing experiments: 5 open-ended + 3 constrained tasks, 4 baselines, 15-pass iterations.
- Code experiments: 150 CodeContests problems × 3 strategies × 4 model tiers (Sonnet 4 / 4.6, Haiku 3.5 / 4.5).
- Ablations cover judge count (1/3/7), Borda vs majority, component necessity (removing B or AB collapses convergence), and length control.
- Robustness: Monte Carlo (5 runs), multi-seed replication (15 runs across 5 tasks).

## Setup

The repo is a research artifact, not a library. Experiment runners live in `experiments/v2/`:

```bash
git clone https://github.com/NousResearch/autoreason.git
cd autoreason/experiments/v2
# requires API access for the relevant model tiers
python run_overnight.py        # writing tasks
python run_code_overnight.py   # CodeContests (Sonnet 4.6)
python run_code_haiku45.py     # Haiku 4.5 code experiment
python run_multi_seed.py       # multi-seed replication
python run_ablations.py        # judge count, aggregation, component, length
python compute_stats.py        # bootstrap CIs and McNemar tests
```

## Integration notes

Take the *pattern*, not the code: the A/B/AB + blind-Borda structure is directly portable into any verification step we add to `superpowers:code-reviewer` or the Ralph loop. For nba-ml-engine, the "evaluator must outperform generator for self-refinement to help" finding is a useful stop-rule for any LLM-graded model selection logic. Worth pairing with the `verification-before-completion` skill.

## Caveats / Gotchas

- Strong-model-only effect — the gains evaporate at Haiku 4.5 / Sonnet 4 quality on CodeContests; don't assume self-refinement is universally beneficial.
- Single-judge runs are noisy and slow; 3 is the practical minimum; 7 converges ~3× faster.
- Code-heavy: 80.8% TeX (the paper) + 19.2% Python (the runners).
- Cited bibliography was corrected post-publication (4 fabricated/wrong citations fixed in 2026-04-12 commits) — pull a recent PDF.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 495 |
| Primary language | TeX |
| Topics | (none) |
| License | (see upstream) |

## Source

- Raw dump: `raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md`
- Upstream: https://github.com/NousResearch/autoreason
