---
title: "Agent-Specific Activation Subspaces"
type: concept
created: 2026-04-29
last_verified: 2026-04-29
source_hash: "a9a46db366eb237bc5197e4bbfcfeb10afd90cf81333ac5446f3e83995f057a1"
sources:
  - raw/2026-04-29-260424881v1pdf.md
quality_score: 84
related:
  - "[[Internalized Multi-Agent Debate]]"
  - "[[Theory Of Mind In Large Language Models]]"
  - "[[Circuit Tracing in Language Models]]"
tier: hot
tags: [llm, activation-steering, interpretability, controllability, multi-agent-debate]
---

# Agent-Specific Activation Subspaces

## Overview

Agent-specific activation subspaces are interpretable directions in a model's hidden-state space that correspond to distinct internalized agent perspectives. In the Latent Agents paper, they provide the mechanistic evidence that internalized multi-agent debate is not just a shorter output style: different debate personas remain recoverable as separate latent directions that can be amplified or suppressed at inference time.

This matters because it turns a behavioral claim into a representational one. If a model really internalizes debate, then the different roles from the original transcript should survive as structured internal states rather than collapsing into a single generic reasoning policy. The paper uses steering experiments to test exactly that hypothesis.

## How It Works

The paper studies activation subspaces after training models with [[Internalized Multi-Agent Debate]]. To make the roles measurable, the authors create a debate dataset in which each of the three agents follows a distinct reasoning persona: **Chain-of-Thought**, **Self-Critique**, and **Program-of-Thought**. They generate **500 training** and **100 test** debate traces using the same three-agent, two-round protocol as the main experiments, then train models with the same SFT-plus-RL pipeline. This setup gives the researchers concrete, behaviorally distinct agent identities to look for in the model's activations.

To extract a subspace for agent $i$, the authors use **Contrastive Activation Addition (CAA)** together with a difference-in-means construction. The procedure keeps the prompt context fixed up to the target agent's turn and then compares two continuations: one in which the target agent's original response is appended, and one in which a different agent's response is appended instead. If $\mathbf{h}_{\ell}(p, c_i)$ is the layer-$\ell$ activation for prompt $p$ with the target continuation $c_i$, and $\mathbf{h}_{\ell}(p, c_{\neg i})$ is the activation with a non-target continuation, the steering vector is

$$
\mathbf{v}_i = \frac{1}{|\mathcal{D}|}\sum_{p, c \in \mathcal{D}} \left(\mathbf{h}_{\ell}(p, c_i) - \mathbf{h}_{\ell}(p, c_{\neg i})\right).
$$

This vector is a compact estimate of "what changes in activation space when the model behaves like agent $i$ instead of some other agent." The important detail is that the method is contrastive. It does not just ask what the target agent looks like; it asks what distinguishes that agent from its peers under matched context.

Once a vector is extracted, steering is performed by modifying the hidden state during inference:

$$
\mathbf{h}_{\ell} \leftarrow \mathbf{h}_{\ell} + \alpha \mathbf{v}_i,
$$

where $\alpha$ is the steering coefficient. Positive $\alpha$ amplifies the target persona; negative $\alpha$ suppresses it. If the internalized debate really created role-specific subspaces, then increasing $\alpha$ should move generations toward the target persona more effectively in the IMAD model than in an untrained base model.

The evaluation protocol is designed to measure that effect cleanly. The authors compare steered outputs against ground-truth agent responses using **ROUGE-1**, **ROUGE-2**, and **ROUGE-L**, then summarize performance as area under the curve (AUC) across steering coefficients from **0.0 to 5.0**. Using **LLaMA-3.1 8B** as the base architecture, they find that the internalized model outperforms the base model across all three personas, with improvements ranging from **6.10% to 24.97%** and an average gain of **15.41%**. The strongest effect appears for the Program-of-Thought persona, which gains roughly **21-25%**, suggesting that code-like reasoning style produces especially distinct internal structure.

Qualitatively, the steered outputs also separate in intuitive ways. Chain-of-Thought steering increases step-by-step exposition, Self-Critique steering produces more corrective language, and Program-of-Thought steering induces more equation-heavy or computational responses. The paper reports that these differences become visible at coefficients as low as **0.5**, while the base model under the same steering regime tends to produce muddier, mixed-style outputs. That contrast is the central evidence that the subspaces are a consequence of internalization, not merely artifacts of generic steering.

The paper then extends the same framework from interpretability to control. The authors train variants where one internalized agent is malicious, defining two trait families: **evil** behavior and **hallucination**. Steering vectors for those traits are extracted the same way and evaluated over coefficients from **-5.0 to +5.0** using an LLM-based trait-expression score, perplexity, and GSM8K accuracy. The resulting picture is nuanced. The evil trait becomes highly localizable: in the IMAD model it is driven to zero at coefficients from **-3.0 to -5.0**, while the base model still shows residual expression at **-5.0**. Hallucination is harder: both models start with elevated trait scores and neither achieves complete suppression, implying that hallucination is more distributed in representation space.

This distinction is one of the most useful conceptual takeaways. Some behaviors appear as relatively discrete persona-like directions that can be isolated by structured training. Others are spread more broadly through the model and therefore resist clean deletion. Agent-specific activation subspaces are valuable precisely because they reveal that difference rather than hiding it. They show where internalized structure becomes linearly accessible, and where linear control runs into representational entanglement.

## Key Properties

- **Contrastive definition**: Each subspace is defined relative to alternative agents under matched context, not in isolation.
- **Linearly steerable**: Behavior changes are induced by adding or subtracting a vector at a chosen layer.
- **Mechanistic evidence of internalization**: Stronger steering in IMAD than in the base model suggests that debate roles survive in latent form.
- **Persona sensitivity**: Distinct reasoning styles produce measurably different subspace strength and separability.
- **Control relevance**: The same extracted directions can be used to suppress unwanted internalized traits.

## Limitations

Activation subspace methods depend on having cleanly labeled contrast sets and may be sensitive to the chosen layer, dataset, and steering coefficient range. They also do not imply that a behavior is fully contained in one direction. The paper's hallucination experiments show that some traits remain distributed enough that negative steering only partially suppresses them. More broadly, linear steering is a useful probe, but it is not a full mechanistic account of how the model computes.

## Examples

```python
def extract_agent_vector(dataset, layer, target_agent):
    diffs = []
    for prompt, target_completion, other_completions in dataset:
        pos = hidden_state(prompt, target_completion, layer=layer)
        neg = average([
            hidden_state(prompt, completion, layer=layer)
            for completion in other_completions
        ])
        diffs.append(pos - neg)
    return sum(diffs) / len(diffs)


def steer(hidden_state_tensor, vector, alpha):
    return hidden_state_tensor + alpha * vector
```

The Latent Agents experiments then score the steered outputs against reference personas or malicious-trait judges to determine whether the subspace truly controls the intended behavior.

## Practical Applications

Agent-specific activation subspaces are useful for mechanistic auditing, persona recovery, and behavior control. In research settings, they provide a way to test whether a post-training method genuinely creates structured internal viewpoints. In safety settings, they offer a route to targeted suppression of internalized harmful behavior with less collateral damage than blunt decoding or policy filters. They also connect naturally to broader interpretability work such as [[Circuit Tracing in Language Models]] and to perspective-taking questions raised by [[Theory Of Mind In Large Language Models]].

## Related Concepts

- **[[Internalized Multi-Agent Debate]]** — Creates the structured latent roles that the steering analysis later recovers.
- **[[Theory Of Mind In Large Language Models]]** — Both topics concern whether distinct viewpoints can exist and be manipulated inside a single model.
- **[[Circuit Tracing in Language Models]]** — Another interpretability lens for identifying how internal computations map to model behavior.

## Sources

- [[Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate]] — Introduces the subspace extraction, steering evaluation, and malicious-trait suppression experiments.
