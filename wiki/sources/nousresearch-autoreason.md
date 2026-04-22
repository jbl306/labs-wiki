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
ingest_method: manual-deepen-github-2026-04-22
quality_score: 90
concepts:
- autoreason-iterative-self-refinement-framework
- iterative-self-critique-loop
---

# NousResearch/autoreason

## What it is

Autoreason (Nous Research; SHL0MS / Hermes Agent) is a research framework — and accompanying paper — for iterative self-refinement that knows when to stop. Each pass produces three competing versions: the unchanged incumbent A, an adversarial revision B, and a synthesis AB. A panel of fresh judging agents (Borda count, no shared context) picks the winner; "do nothing" is always a first-class option. The repo contains the LaTeX paper, blinded human-evaluation materials, the experiment runners, and the result corpora across writing tasks and CodeContests problems.

## Why it matters

Direct counter to the naive "critique + revise" loop most of us reach for first. Three findings are practically useful for any verification or self-review skill we build (including `superpowers:code-reviewer`, the `code-reviewer` agent skill, or the Ralph-loop pattern): critique-and-revise *destroys* weak models (Haiku 3.5 outputs shrunk 59–70% over 15 passes), 7 judges converge ~3× faster than 3, and the gains vanish once a model crosses ~60% private accuracy on the underlying task — meaning self-refinement has a model-quality floor and ceiling.

## Architecture / Technical model

- **A / B / AB tournament** — Each iteration produces three competing versions: (A) the unchanged incumbent, (B) an adversarial revision, (AB) a synthesis combining A and B. A panel of fresh judging agents (with no shared context) scores all three via blind Borda count. "Do nothing" (picking A) is always a first-class option.
> See [[autoreason-iterative-self-refinement-framework]] and [[iterative-self-critique-loop]] for the tournament structure.

- **Fresh-agent isolation** — Critic, Author B, Synthesizer, and all judges run with no shared context. Each agent sees only its immediate input (incumbent or critique) and generates output independently. Prevents critique-loop contamination where agents anchor on prior iterations' mistakes.

- **Blind Borda count** — Judges score with randomized order and neutral labels (Proposal 1/2/3, not A/B/AB) to defeat positional and label bias. Each judge ranks proposals 1st, 2nd, 3rd; Borda points are summed; highest score wins. Ties broken randomly.

- **Convergence rule** — Iteration stops when the incumbent A wins k=2 consecutive tournaments, or after a max iteration limit (15 passes in writing experiments, 24 in code experiments). "Do nothing" is validated rather than assumed.

- **Generation-evaluation gap** — Self-refinement only helps when the model can evaluate better than it can generate. Below ~60% private accuracy on CodeContests (Haiku 4.5 / Sonnet 4 threshold), the gap is large and autoreason improves; above this threshold, the gap closes and gains vanish.

- **Length-controlled evaluation** — Ablation compares outputs at matched word count (via truncation or padding) to rule out "longer = better" confound. Autoreason beats 3 of 4 baselines (21/28 wins) even at matched length, confirming quality improvements are not purely from verbosity.

- **Component necessity** — Removing either B (adversarial revision) or AB (synthesis) collapses the tournament: convergence happens in 2–3 passes vs 24 in the full system. Both are required to maintain productive tension.

- **Judge panel size ablation** — 7 judges converge ~3× faster than 3 judges (measured in passes to convergence). 1 judge is noisy and slow. 3 is the practical minimum; 7 is preferred when compute permits.

- **Robustness** — Monte Carlo (5 runs), multi-seed replication (15 runs across 5 tasks), and failure taxonomy analysis confirm consistency. Writing tasks show 42/42 perfect Borda sweep (Haiku 3.5 + autoreason); all baselines degraded below single-pass.

## How it works

1. **Initialization**: Task prompt → generate incumbent A (single-pass output).
2. **Critic step**: Fresh agent reads A, generates a critique (identifies flaws, suggests improvements).
3. **Author B step**: Fresh agent reads the critique (not A), generates adversarial revision B.
4. **Synthesizer step**: Fresh agent reads A and the critique, generates synthesis AB.
5. **Judge panel**: 3 fresh agents (or 7 in high-compute settings) score A, B, AB with randomized order and neutral labels. Each judge ranks proposals 1st/2nd/3rd.
6. **Borda aggregation**: Sum Borda points (1st = 2 points, 2nd = 1 point, 3rd = 0 points). Highest score wins.
7. **Incumbent update**: Winner becomes new A. If A won, increment convergence counter; if A wins k=2 times, stop.
8. **Iteration**: Repeat steps 2–7 until convergence or max passes.
9. **Experiments**:
   - **Writing tasks** (5 open-ended + 3 constrained): 15-pass iterations, 4 baselines (single-pass, critique-and-revise, best-of-N, self-consistency).
   - **CodeContests** (150 problems): 3 strategies (autoreason, single-pass, best-of-N) × 4 model tiers (Sonnet 4, Sonnet 4.6, Haiku 3.5, Haiku 4.5).
   - **Ablations**: Judge count (1/3/7), Borda vs majority vote, component necessity (remove B or AB), length-controlled evaluation.
   - **Robustness**: Monte Carlo (5 runs per task), multi-seed replication (15 runs across 5 tasks).
10. **Key finding (code scaling)**: Haiku 3.5 (40% private) → Haiku 4.5 (60% private) → Sonnet 4 (64% private) → Sonnet 4.6 (77% private). Gains persist at Sonnet 4.6 level; vanish at Haiku 4.5.
11. **Key finding (writing)**: Haiku 3.5 + autoreason scored perfect Borda (42/42 wins) across 3 tasks; all baselines (critique-and-revise, best-of-6, self-consistency) degraded below single-pass.
12. **Key finding (refinement destroys weak models)**: Critique-and-revise reduced Haiku 3.5 outputs by 59–70% in word count over 15 passes. Models below the generation-evaluation threshold hallucinate flaws and progressively delete valid content.

## API / interface surface

### Experiment Runners

| Script | Purpose |
|--------|---------|
| `experiments/v2/run_overnight.py` | Writing experiments (5 open-ended + 3 constrained tasks) |
| `experiments/v2/run_code_overnight.py` | CodeContests experiments (Sonnet 4.6, 150 problems) |
| `experiments/v2/run_code_haiku45.py` | CodeContests experiments (Haiku 4.5, 150 problems) |
| `experiments/v2/run_code_haiku.py` | CodeContests experiments (Haiku 3.5, 150 problems) |
| `experiments/v2/run_multi_seed.py` | Multi-seed replication (15 runs across 5 tasks) |
| `experiments/v2/run_ablations.py` | Ablations (judge count, Borda vs majority, component, length) |
| `experiments/v2/compute_stats.py` | Compute bootstrap CIs and McNemar tests |

### Result Directories

| Directory | Contents |
|-----------|----------|
| `experiments/v2/results_code_s46/` | Sonnet 4.6 code results (150 problems) |
| `experiments/v2/results_code_haiku/` | Haiku 3.5 code results (150 problems) |
| `experiments/v2/results_code_haiku45/` | Haiku 4.5 code results (150 problems) |
| `experiments/v2/results_code_best_of_n/` | Best-of-N baseline (compute-matched) |
| `experiments/v2/results_multi_seed/` | 15 independent writing runs |
| `experiments/v2/results_ablations/` | Judge count, aggregation, component, length ablations |
| `experiments/v2/results_baselines/` | Baseline comparison outputs |
| `experiments/v2/results_monte_carlo/` | Monte Carlo replication (5 runs) |

### Human Evaluation Materials

`human_eval/` contains blinded materials for human raters:
- 5 tasks × 3 methods (autoreason, critique-and-revise, single-pass) = 15 documents
- Documents identified by random 4-character codes
- Rubric: Clarity, Usefulness, Correctness, Concision, Overall (1–5 scale)
- See `human_eval/README.md` for instructions

### Paper

`paper/autoreason.pdf` — LaTeX source + compiled PDF (80.8% TeX, 19.2% Python)

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

- **Strong-model-only effect** — Gains vanish at Haiku 4.5 / Sonnet 4 quality on CodeContests (~60% private accuracy). Self-refinement requires a generation-evaluation gap; once the model crosses the threshold, the gap closes and iterative refinement provides no benefit.
- **Weak models are destroyed by refinement** — Critique-and-revise reduced Haiku 3.5 outputs by 59–70% in word count over 15 passes. Models below the threshold hallucinate flaws and progressively delete valid content.
- **Single-judge runs are noisy and slow** — 1 judge is insufficient for reliable rankings. 3 is the practical minimum; 7 converges ~3× faster than 3.
- **Compute cost scales with judge panel** — 7 judges × 3 candidates × N iterations = 21N LLM calls per pass. Budget accordingly.
- **Code-heavy repo** — 80.8% TeX (the paper) + 19.2% Python (experiment runners). This is a research artifact, not a library; expect to adapt the scripts to your use case.
- **Corrected citations** — The bibliography had 4 fabricated/wrong citations fixed in 2026-04-12 commits. Pull a recent PDF if citing the paper.
- **No production API** — The repo provides experiment runners and result corpora, not a packaged library. To use the pattern, extract the tournament logic from `run_overnight.py` / `run_code_overnight.py`.
- **Human evaluation is blinded** — The `human_eval/` materials use random 4-character codes to prevent rater bias. The answer key (`human_eval_answer_key.json`) maps codes to methods; do not share it with raters.
- **Borda vs majority vote** — Borda count is more robust than majority vote (ablation confirms). Majority vote ignores preference intensity; Borda captures ordinal ranking.
- **Length-controlled findings** — Autoreason beats 3 of 4 baselines (21/28 wins) even at matched word count. The 4th baseline (self-consistency) ties at matched length but loses on raw output.
- **No license specified** — The repository does not include a LICENSE file; usage rights are unclear. Verify with Nous Research before production use.

## Related concepts

- [[autoreason-iterative-self-refinement-framework]]
- [[iterative-self-critique-loop]]

## Source

- Raw dump: `raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md`
- Upstream: https://github.com/NousResearch/autoreason
