---
title: "Iterative Self-Critique Loop"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
quality_score: 85
concepts:
  - iterative-self-critique-loop
related:
  - "[[NousResearch/autoreason]]"
  - "[[Autoreason Iterative Self-Refinement Framework]]"
  - "[[Faithful vs. Motivated Reasoning in Language Models]]"
tier: warm
tags: [self-refinement, critique-and-revise, iterative-improvement, llm-reasoning, agent-workflows]
---

# Iterative Self-Critique Loop

## Overview

The iterative self-critique loop is a reasoning pattern where a model generates an output, critiques it, revises based on the critique, and repeats. This pattern (often called "critique-and-revise") is intuitive and widely used, but it suffers from three structural flaws: prompt bias (models hallucinate flaws when asked to critique), scope creep (outputs expand unchecked each pass), and lack of restraint (models never say "no changes needed"). Autoreason (Nous Research) is a framework that addresses these flaws by introducing competitive revision, blind evaluation, and an explicit "do nothing" option.

## How It Works

The basic critique-and-revise loop proceeds as follows:

1. **Generate** — Produce an initial output (e.g., a draft essay, a code solution).
2. **Critique** — Ask the model (or a fresh agent) to identify flaws in the output.
3. **Revise** — Generate a new version of the output that addresses the critique.
4. **Repeat** — Iterate until a stopping condition is met (e.g., max iterations, no further critique).

**Naive implementation:**

```
output = generate(task_prompt)
for i in range(max_iterations):
    critique = critique(output)
    output = revise(output, critique)
```

**Problems with naive critique-and-revise:**

1. **Prompt bias** — When asked to critique, models tend to hallucinate flaws even when the output is already good. This leads to unnecessary revisions that degrade quality.

2. **Scope creep** — Each revision tends to expand the output (adding details, qualifications, hedges) without improving quality. Over 15 passes, Haiku 3.5 outputs in the Autoreason paper shrank by 59–70% because the model progressively deleted valid content after hallucinating flaws.

3. **Lack of restraint** — The model never says "this is already good, no changes needed." It always generates a critique and a revision, even when the output is optimal.

4. **Context contamination** — If the same model instance critiques and revises, it carries forward biases from prior iterations (e.g., over-emphasizing a flawed critique in subsequent revisions).

**Solutions (Autoreason's approach):**

- **Fresh-agent isolation** — Each critique and revision is performed by a fresh agent with no shared context, preventing contamination.
- **Competitive revision** — Generate multiple competing versions (unchanged incumbent A, adversarial revision B, synthesis AB) rather than a single revision. This introduces explicit competition and prevents unchecked scope creep.
- **Blind evaluation** — A panel of fresh judges evaluates all candidates (including the unchanged incumbent) via blind Borda count, ensuring that "do nothing" is a first-class option.
- **Convergence rule** — Stop when the incumbent wins k times (e.g., k=2), signaling that no further improvement is needed.

> See [[Autoreason Iterative Self-Refinement Framework]] for the full tournament structure.

**When critique-and-revise works:**

- The model's evaluation ability is significantly stronger than its generation ability (generation-evaluation gap).
- The task is subjective and benefits from nuanced judgment (e.g., writing, design).
- The stopping condition is well-defined (e.g., "converge when no critique is generated").

**When critique-and-revise fails:**

- The model is weak (below ~60% accuracy on the task) — it hallucinates flaws and degrades quality.
- The task is objective (e.g., competitive programming) — the model can evaluate by running tests, but this doesn't require iteration.
- The stopping condition is poorly defined — the model iterates indefinitely, expanding the output without improving it.

## Key Properties

- **Generate → Critique → Revise → Repeat** — The basic loop structure.
- **Prompt bias** — Models tend to over-critique when explicitly asked to find flaws.
- **Scope creep** — Outputs expand over iterations without quality improvement.
- **Lack of restraint** — The model never stops on its own; it always generates a critique.
- **Context contamination** — Shared context across iterations biases future critiques and revisions.

## Trade-offs

**Benefits:**
- Simple to implement (single prompt template)
- Intuitive for humans (mirrors editorial workflows)
- Can improve outputs when the evaluation-generation gap is large

**Drawbacks:**
- Degrades quality for weak models (Haiku 3.5 outputs shrank 59–70% over 15 passes)
- Requires careful stopping criteria to avoid infinite loops
- Prone to scope creep and over-revision
- Computationally expensive (multiple passes, each with full model inference)

## Example

**Naive critique-and-revise:**

```
Task: "Write a go-to-market strategy for a developer tools startup."

# Iteration 1
output_1 = generate(task)  # 500 words
critique_1 = critique(output_1)  # "Lacks specificity on pricing"
output_2 = revise(output_1, critique_1)  # 600 words, adds pricing section

# Iteration 2
critique_2 = critique(output_2)  # "Could include more competitive analysis"
output_3 = revise(output_2, critique_2)  # 700 words, adds competitor section

# Iteration 3
critique_3 = critique(output_3)  # "Needs more detail on distribution channels"
output_4 = revise(output_3, critique_3)  # 850 words, expands distribution section

# ... continues indefinitely
```

**Autoreason-style improvement:**

```
Task: "Write a go-to-market strategy for a developer tools startup."

# Iteration 1
output_A = generate(task)  # 500 words
critique = critique(output_A)  # "Lacks specificity on pricing"
output_B = revise(critique)  # 550 words, different approach to pricing
output_AB = synthesize(output_A, critique)  # 520 words, combines A's structure + B's pricing

# Judge panel evaluates A, B, AB
winner = judge([output_A, output_B, output_AB])  # Blind Borda count
# If winner == output_A (unchanged), increment convergence counter

# Iteration 2
output_A = winner
# ... repeat until convergence (incumbent wins k=2 times)
```

## Relationship to Other Concepts

- **[[Autoreason Iterative Self-Refinement Framework]]** — A structured solution to the critique-and-revise flaws.
- **[[NousResearch/autoreason]]** — The upstream project that introduces Autoreason.
- **[[Faithful vs. Motivated Reasoning in Language Models]]** — Prompt bias in critique-and-revise is a form of motivated reasoning (the model is biased to find flaws when asked).

## Practical Applications

Iterative self-critique is useful for:
- **Writing tasks** — Essays, reports, technical documentation (when used with Autoreason's improvements).
- **Code review** — Identifying bugs and suggesting fixes (but beware hallucinated flaws).
- **Design refinement** — Iteratively improving UI mockups, API designs, architecture diagrams.
- **Policy documents** — Refining corporate policies, legal contracts, compliance documents.

However, **naive critique-and-revise is often harmful**:
- Weak models (Haiku 3.5) are destroyed by iteration (59–70% word count reduction).
- Even strong models can over-revise, adding unnecessary detail and hedging.
- Without explicit restraint ("do nothing" option), the loop never stops.

**Best practices:**
- Use fresh agents for critique and revision (no shared context).
- Include the unchanged incumbent as a candidate in every iteration.
- Use blind evaluation to judge candidates (Borda count or similar).
- Set a convergence rule (e.g., incumbent wins k times).
- Monitor output length and quality metrics to detect scope creep.

## Sources

- [[NousResearch/autoreason]] — introduces Autoreason, a structured fix for critique-and-revise flaws
