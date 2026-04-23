---
title: "Self-Evolving Rule Pools for Agent Compression"
type: concept
created: 2026-04-23
last_verified: 2026-04-23
source_hash: "1ca1c01606b2b234d278cd0aefc974bff993603f4c4596baf0be8b058331d26e"
sources:
  - raw/2026-04-23-260419572v1pdf.md
related:
  - "[[TACO]]"
  - "[[Terminal Observation Compression]]"
  - "[[Context Management and Compaction Pipeline in Claude Code]]"
  - "[[Reasoning Trace Segmentation and Iterative Summarization]]"
  - "[[The Context Hygiene Principle]]"
tier: hot
tags: [rule-evolution, context-compression, terminal-agents, llm-agents, adaptation]
quality_score: 65
---

# Self-Evolving Rule Pools for Agent Compression

## Overview

Self-evolving rule pools are a mechanism for turning observation compression from a static heuristic list into a learning system. In the TACO paper, the idea is to maintain a persistent global pool of structured compression rules, retrieve the most promising ones for a new task, refine them for local context, generate new rules when the current task exposes uncovered patterns, and write successful rules back so later tasks start smarter than earlier ones.

This matters because terminal environments are too heterogeneous for one frozen set of handcrafted rules to stay effective. Compression patterns that work for package installation, disassembly, compiler output, and repository tooling differ sharply, so the system needs a way to accumulate reusable knowledge without resorting to weight updates or fine-tuning.

## How It Works

The basic tension behind self-evolving rule pools is simple: static rules are cheap and interpretable, but real terminal environments are messy enough that a fixed hand-written list will always miss important cases. TACO resolves that tension by splitting compression knowledge into two interacting layers. The **Global Rule Pool** stores reusable rules discovered across many tasks, while the **task-specific rule set** holds the subset of rules currently active for one trajectory. This lets the system reuse history without assuming that every old rule is equally relevant to every new task.

The global pool is initialized with 6 seed rules covering common high-noise command families: `git` transfer progress, heredoc echo, `pip install`, `apt-get`, compiler output, and OpenSSL or SSH key-generation noise. These seeds are intentionally conservative. They remove repetitive status chatter while preserving errors, warnings, and a small amount of leading and trailing context. The goal is not maximal compression on day one; it is to start inside a safe rule space that can be refined instead of improvising from scratch on every task.

When a new task begins, the system does not simply dump the entire global pool into context. It ranks rules and retrieves the top-$k$ candidates, then asks an LLM to select and refine the rules that actually fit the current task description. In the paper's main setup, $k = 30$. This retrieval step is important because it imposes a budget on adaptation. Too few retrieved rules starves the task of historical knowledge; too many inflate prompt cost and can destabilize smaller models. The paper's ablation shows that accuracy improves as $k$ grows at first, then saturates or degrades beyond about 30 while self-evolution token cost keeps climbing.

Once a task is underway, the active rule set evolves through two complementary triggers. The first is **uncovered output**. If a command produces a long observation that no active rule matches, the system treats that as a missing capability and asks the model to generate a new structured rule. The paper's case studies make this concrete. In a long `apt-get install` run, a newly evolved rule compressed hundreds of repetitive `Unpacking` and `Setting up` lines down to a brief progress indicator. In a reverse-engineering task, an `objdump_disassembly_rule` was created after the first uncovered disassembly block, then reused on many later `objdump` invocations.

The second trigger is **implicit feedback** from the agent itself. TACO does not need an external human reviewer to tell it a rule was too aggressive. Instead, it watches for behaviors such as re-running a command to recover detail, requesting fuller output, or otherwise acting as if critical information was removed. Those are treated as over-compression complaints. The system identifies which rules actually modified the problematic output, suppresses them for subsequent use, and asks the model to generate more conservative replacements. This makes the rule pool a feedback-controlled system rather than a one-way accumulator.

To support reuse, each rule carries statistics. The paper defines a global ranking score:

$$
R_{gs}(r) = c_r^g \cdot (n_r + 1)
$$

where $c_r^g$ is the rule's global confidence and $n_r$ is its cumulative number of successful applications across tasks. This formula is simple but clever. A rule that fires often but earns complaints should not dominate retrieval, and a rule with high confidence but no demonstrated reuse should not be ranked as if it were universally valuable. The multiplicative form balances historical reliability with transfer frequency.

Write-back to the global pool is also gated. A task-level rule is only promoted if it was successfully applied at least once and ends the task with confidence above a small threshold $\tau$. Complained-about rules are effectively zeroed out for that trajectory and can be deleted instead of reinforced. That prevents the pool from drifting toward aggressively compressive but brittle behavior. In other words, the system is not just learning rules; it is learning which rules survive repeated contact with real agent behavior.

Because the rule pool evolves over multiple passes across a dataset, the paper also needs a way to tell when evolution has stabilized. It introduces a retention metric over the Top-$K$ rules:

$$
\mathrm{Retention}^{(i)}_K =
\frac{\left|\mathrm{TopK}(R_g^{(i-1)}) \cap \mathrm{TopK}(R_g^{(i)})\right|}{K} \times 100\%
$$

with $K = 30$ in the reported experiments. The intuition is that if the same frontier rules keep surviving round after round, the system's reusable compression knowledge is no longer changing rapidly. The paper validates this metric by showing that once retention rises, rolling standard deviation in task accuracy drops as well.

There is also a systems-level trade-off involving batch size $N$. Smaller batches let newly learned rules be written back sooner, so later tasks can immediately benefit from them. Larger batches improve throughput but delay knowledge propagation. In the paper's ablation, the chosen compromise is $N = 4$, and one full round of self-evolution at that setting takes roughly 4 days. That detail matters because it frames rule evolution as an operational loop, not just a conceptual algorithm.

The deeper idea is that self-evolving rule pools are a form of non-parametric learning for tool-using agents. Instead of changing model weights, they externalize environment-specific knowledge into structured, inspectable artifacts. That makes them closer to reusable operational memory than to ordinary prompting. Compared with generic runtime compaction, they are more specialized and adaptive. Compared with training-time methods such as [[Reasoning Trace Segmentation and Iterative Summarization]], they are more online and environment-responsive. Their distinctive strength is that they learn from actual failures and successes in the live observation stream.

## Key Properties

- **Cross-task reuse**: Compression knowledge learned in one trajectory can initialize later tasks through the global rule pool.
- **Structured adaptation**: New rules stay within an explicit schema of regex triggers, keep/strip patterns, retention bounds, and confidence scores.
- **Implicit feedback loop**: Over-compression is detected through agent behavior, not only through external annotation.
- **Confidence-weighted ranking**: Retrieval balances frequency of successful reuse with rule reliability instead of using raw counts alone.
- **Convergence visibility**: Top-$K$ retention offers an operational signal for when self-evolution has stabilized.

## Limitations

- **LLM dependence**: Rule generation and refinement quality depend on the model used for proposal and repair.
- **Evolution cost**: Retrieval, rule generation, and update prompts add token and wall-clock overhead, especially across many tasks.
- **Schema ceiling**: A structured rule format is safer than free-form summarization, but it may still be too rigid for some complex outputs.
- **Feedback ambiguity**: Behaviors interpreted as over-compression complaints can have multiple causes, so repair signals are not perfectly clean.

## Examples

```json
{
  "rule_id": "seed_pip_install",
  "trigger_regex": "\\bpip3?\\s+install\\b",
  "keep_patterns": ["ERROR:", "Successfully installed", "Traceback"],
  "strip_patterns": ["^\\s*Collecting \\S+", "^\\s*Downloading \\S+"],
  "confidence": 0.8,
  "times_applied": 10
}
```

```python
def update_global_pool(rule, task_confidence, successful_apps):
    if successful_apps < 1 or task_confidence <= tau:
        return "do-not-promote"
    rule.global_confidence = mix(rule.global_confidence, task_confidence)
    rule.times_applied += successful_apps
    rule.rank = rule.global_confidence * (rule.times_applied + 1)
    return "promoted"
```

In the paper's case studies, this pattern yields rules such as `apt_install_unpacked_packages` and `objdump_disassembly_rule`, both of which emerged from uncovered outputs and then became repeatedly useful within long trajectories.

## Practical Applications

This concept is useful anywhere agents face recurring but variable tool noise: coding agents, CI triage bots, terminal-based security workflows, and autonomous operations assistants. It is particularly attractive when organizations want a form of accumulating operational knowledge that remains auditable and editable by humans instead of disappearing into model weights.

It also offers a design pattern beyond terminal logs. Any agent that repeatedly consumes semi-structured tool output could use a global-plus-local rule memory to learn what should be compressed, preserved, or escalated.

## Related Concepts

- **[[Terminal Observation Compression]]**: The direct consumer of the evolving rules; it defines where the rules are applied in the agent loop.
- **[[Context Management and Compaction Pipeline in Claude Code]]**: A broader but less environment-specific runtime strategy for controlling context growth.
- **[[Reasoning Trace Segmentation and Iterative Summarization]]**: An offline, training-data-oriented alternative for teaching models compression behavior.
- **[[The Context Hygiene Principle]]**: The higher-level argument for why prompt noise reduction improves downstream reasoning quality.

## Sources

- [[A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression]] — primary source for the global-pool/task-pool design, ranking score, and convergence metric
