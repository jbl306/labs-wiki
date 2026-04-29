---
title: "Multi-Agent Debate"
type: concept
created: 2026-04-29
last_verified: 2026-04-29
source_hash: "a9a46db366eb237bc5197e4bbfcfeb10afd90cf81333ac5446f3e83995f057a1"
sources:
  - raw/2026-04-29-260424881v1pdf.md
quality_score: 82
related:
  - "[[Internalized Multi-Agent Debate]]"
  - "[[Agent-Specific Activation Subspaces]]"
  - "[[Theory Of Mind In Large Language Models]]"
tier: hot
tags: [llm, multi-agent-systems, debate, reasoning, inference-time-scaling]
---

# Multi-Agent Debate

## Overview

Multi-agent debate is an inference-time reasoning pattern where several language-model agents answer the same problem, critique one another over multiple rounds, and then converge on a final answer. The core intuition is that disagreement is useful: when multiple agents expose intermediate reasoning and challenge each other's errors, the system can often reduce hallucinations and correct mistakes that would survive a single forward pass.

In the Latent Agents paper, multi-agent debate is the teacher protocol rather than the final deployment target. The authors use it to generate structured supervision that can later be internalized by a single model, which makes the paper especially useful as a clean explanation of what debate actually contributes before any distillation happens.

## How It Works

At a high level, multi-agent debate starts with a shared prompt $q$ and a set of agents $a_1, a_2, \ldots, a_n$. In round 1, each agent produces its own answer independently, giving a first-pass set of candidate solutions $r_i^{(1)}$. This independence is important: the first round captures diversity in reasoning paths, not just repeated agreement. If one agent spots a shortcut, another notices an arithmetic slip, and a third frames the task differently, the system now has a pool of alternative trajectories to work with.

In later rounds, each agent conditions on both its own earlier answer and the previous answers from the other agents. Formally, an agent at round $t$ can be viewed as generating

$$
r_i^{(t)} = f(q, r_i^{(1:t-1)}, r_{-i}^{(1:t-1)}),
$$

where $r_{-i}$ denotes the responses of the other agents. This turns the process into iterative critique-and-revision rather than simple ensembling. Each round gives the system a chance to surface contradictions, repair brittle logic, and move toward consensus. In the Latent Agents source, the standard setup uses **3 agents** over **2 rounds**, which the paper reports as a good balance between performance and efficiency.

The final answer is usually selected through a simple aggregation rule such as majority vote over the last-round responses. If the final-round outputs are $r_1^{(m)}, \ldots, r_n^{(m)}$, a canonical decision rule is

$$
\hat{y} = \operatorname{mode}(r_1^{(m)}, \ldots, r_n^{(m)}).
$$

This mechanism is intentionally simple. The value of debate does not come from a sophisticated controller so much as from forcing multiple reasoning chains into contact with one another before the decision is made. The majority vote then acts as a lightweight way to turn that structured interaction into a single answer.

The Latent Agents paper makes an important practical observation: debate's gains depend heavily on transcript structure. During dataset construction, the authors insert tags such as `<|Agent 1|>`, `<|Round 1|>`, `<|Consensus|>`, and `<|endofdebate|>`. These markers make the latent roles explicit, reduce ambiguity about which agent is speaking, and create a clean scaffold for later training. Without this structure, agent identity becomes blurrier, and the paper reports weaker separation in downstream subspace analysis.

The paper's training corpus for debate traces is deliberately simple. The authors use GPT-3.5 turbo agents to solve arithmetic expressions made from six randomly generated two-digit numbers. They filter out debates that do not end with a majority consensus, then keep **944** traces of the form `{Question, Trace, Answer}`. This design choice matters: by holding the domain simple and the answers short, the dataset emphasizes the *interaction pattern* of debate rather than long-form domain knowledge. In other words, the authors want to teach the structure of collaborative reasoning, not just a benchmark-specific answer style.

Why does this help? Debate creates explicit opportunities for self-correction that a single pass often lacks. A wrong answer is not merely wrong; it becomes an object other agents can inspect. One agent can point out a violated constraint, another can re-evaluate a calculation, and a third can test whether the current consensus is justified. That makes debate especially attractive for tasks where local reasoning errors are common and where exposing the reasoning trace is acceptable.

The downside is cost. If one model call becomes $n \times m$ calls plus transcript growth across rounds, token usage rises quickly. The Latent Agents paper is motivated by exactly this issue: debate works, but it is expensive enough that deployment pressure pushes researchers to ask whether the useful part can be retained without carrying the full visible conversation. That question leads directly to [[Internalized Multi-Agent Debate]].

## Key Properties

- **Role diversity**: Debate works by preserving multiple candidate viewpoints before forcing a consensus.
- **Iterative correction**: Later rounds condition on prior answers, turning debate into a critique-and-revision loop instead of a one-shot vote.
- **Simple aggregation**: Majority vote over the final round is often enough to convert discussion into a final answer.
- **Transcript dependence**: Clear role and round markers materially improve the learnability and analyzability of debate traces.
- **High inference cost**: Compute and token usage scale with the number of agents, rounds, and transcript length.

## Limitations

Multi-agent debate is expensive at inference time, especially when each agent produces long rationales. It can also suffer from coordination failures: agents may anchor on the same early mistake, over-correct each other, or converge on superficial agreement rather than truth. The Latent Agents paper further notes that increasing agents or rounds beyond the paper's standard setting offers only marginal benefits under its task distribution, which suggests a diminishing-returns regime rather than unlimited scaling.

## Examples

```python
def multi_agent_debate(question, agents, rounds=2):
    transcript = []
    last_round = []
    for round_id in range(rounds):
        current_round = []
        for i, agent in enumerate(agents):
            context = {
                "question": question,
                "transcript": transcript,
                "agent_id": i + 1,
            }
            response = agent.generate(context)
            current_round.append(response)
            transcript.append((round_id + 1, i + 1, response))
        last_round = current_round
    return majority_vote(last_round), transcript
```

In the Latent Agents paper, this explicit protocol is not the endpoint. The resulting transcript becomes supervision for a single model that will later learn to perform the same style of reasoning internally.

## Practical Applications

Multi-agent debate is useful when reasoning reliability matters more than raw inference cost, or when developers want an explicit transcript for auditing and error analysis. It is especially attractive as a data-generation protocol for post-training: the transcript exposes intermediate reasoning moves that can be distilled, compressed, or analyzed later. In that sense, debate is both a reasoning method and a supervision factory for stronger single-model systems.

## Related Concepts

- **[[Internalized Multi-Agent Debate]]** — Distills the explicit debate procedure into one model while trying to preserve its reasoning benefits.
- **[[Agent-Specific Activation Subspaces]]** — A mechanistic consequence of internalizing debate: different debate roles can survive as distinct directions in activation space.
- **[[Theory Of Mind In Large Language Models]]** — Related because debate and perspective-taking both depend on maintaining separable internal viewpoints rather than a single undifferentiated response style.

## Sources

- [[Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate]] — Uses standard multi-agent debate as the teacher protocol that IMAD later internalizes.
