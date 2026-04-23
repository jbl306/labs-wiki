---
title: "Agent Context Compression Layers in Tool-Using Systems"
type: synthesis
created: 2026-04-23
last_verified: 2026-04-23
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-23-260419572v1pdf.md
  - raw/2026-04-18-260414228v1pdf.md
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
concepts:
  - terminal-observation-compression
  - self-evolving-rule-pools-agent-compression
  - context-management-compaction-pipeline-claude-code
  - reasoning-trace-segmentation-and-iterative-summarization
related:
  - "[[Terminal Observation Compression]]"
  - "[[Self-Evolving Rule Pools for Agent Compression]]"
  - "[[Context Management and Compaction Pipeline in Claude Code]]"
  - "[[Reasoning Trace Segmentation and Iterative Summarization]]"
tier: hot
tags: [context-compression, terminal-agents, llm-agents, long-horizon-reasoning, synthesis]
quality_score: 75
---

# Agent Context Compression Layers in Tool-Using Systems

## Question

Where should compression logic live in a long-running tool-using agent: in the live observation stream, in a persistent rule-learning layer, in a generic runtime compaction pipeline, or in offline training-time preparation?

## Summary

The sources suggest that these are complementary layers rather than interchangeable choices. [[Terminal Observation Compression]] handles noisy tool feedback at the moment it enters the agent loop, [[Self-Evolving Rule Pools for Agent Compression]] make that filtering improve over time, [[Context Management and Compaction Pipeline in Claude Code]] manages whole-session overflow at runtime, and [[Reasoning Trace Segmentation and Iterative Summarization]] prepares models offline to compress their own internal state.

## Comparison

| Dimension | [[Terminal Observation Compression]] | [[Self-Evolving Rule Pools for Agent Compression]] | [[Context Management and Compaction Pipeline in Claude Code]] | [[Reasoning Trace Segmentation and Iterative Summarization]] |
|-----------|--------------------------------------|----------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------|
| Primary target | Raw command output from the environment | Reusable compression knowledge across tasks | Conversation history and context-window pressure | Training traces of internal reasoning |
| Runs when | Immediately after each command | Across and within task trajectories over repeated runs | Before model calls during live runtime | Before model deployment, during data generation |
| Main unit of work | One observation `O_t` | One structured rule plus its confidence/usage stats | One assembled context window | One reasoning trace split into blocks |
| Adaptation source | Command type and matched output patterns | Successful reuse plus implicit complaint signals | Hand-designed layered policies | LLM boundary scoring and iterative summary refinement |
| Safety mechanism | Preserve critical errors unchanged | Suppress or replace complained-about rules | Progressive cheap-to-expensive compaction layers | Judge-refined summaries and balanced segmentation |
| Best use case | Log-heavy CLI agents | Fleets of agents seeing recurring tool patterns | General-purpose coding agents with long sessions | Long-context models that learn to self-summarize reasoning |

## Analysis

The cleanest lesson across these pages is that "context compression" is too broad a phrase unless we specify **what is being compressed**. TACO's new contribution is to focus on the observation boundary: terminal output is compressed before it pollutes future reasoning steps. That is a different problem from the one Claude Code addresses, where the challenge is managing the entire active prompt and cache footprint of an extended interactive session. It is also different from Memento's training pipeline, where the compressed object is not tool output at all but internal reasoning traces turned into summary supervision.

This separation matters because each layer sees different information and therefore supports different guarantees. Terminal observation compression can preserve exact error lines while removing repetitive package-manager churn because it still has access to raw command semantics and raw output. A generic compaction pipeline usually acts later, when tool outputs, user instructions, and prior model responses have already been blended into one long context. By then, compression is broader but less specialized. The TACO paper shows that specialization pays off in tool-heavy environments.

The self-evolving rule-pool layer is what turns that specialization into a durable capability rather than a brittle ruleset. Without it, terminal compression would remain a fixed catalog of handcrafted filters. With it, the agent stack accumulates environment-specific operational memory while staying training-free. That gives it an interesting position between prompt engineering and memory systems: the learned artifacts are not model weights, but they are more structured and reusable than one-off prompts.

Memento's training-time segmentation highlights a fourth layer: some compression problems are better solved before runtime ever starts. If a model is expected to replace old reasoning blocks with summaries during inference, it must be taught how to do that faithfully. That makes Memento a useful contrast case. TACO compresses external observations online; Memento teaches models to compress internal reasoning offline. Together they suggest that strong long-horizon agents may need multiple compression strata, not one universal trick.

For practical system design, the choice should follow the dominant source of bloat. If the main problem is shell noise, put compression at the tool boundary. If the main problem is long conversational drift, use a runtime compaction stack. If the goal is extending model reasoning depth through summary state replacement, invest in training-time segmentation and runtime support for that protocol. In many mature agents, these layers could coexist: observation filters first, global session compaction second, and model-native reasoning compression as a longer-term research path.

## Key Insights

1. **Compression should be placed where the noise originates** — TACO works because it attacks terminal noise before it contaminates the next reasoning step, while Claude Code's pipeline solves a different, broader runtime problem.
2. **Learning reusable compression rules is a distinct capability layer** — [[Self-Evolving Rule Pools for Agent Compression]] adds durable adaptation on top of [[Terminal Observation Compression]] instead of replacing it.
3. **Runtime and training-time compression are complementary** — [[Reasoning Trace Segmentation and Iterative Summarization]] solves a model-preparation problem that neither TACO nor generic session compaction can fully cover by themselves.

## Open Questions

- Can a single agent stack safely combine command-aware observation filters, session-level compaction, and model-native reasoning summaries without compounding information loss?
- How should implicit over-compression complaints be validated so that rule-pool updates do not react to unrelated agent failures?
- What evaluation setup best separates "token savings" from "better reasoning" when multiple compression layers are enabled at once?

## Sources

- [[A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression]]
- [[Dive into Claude Code: The Design Space of Today’s and Future AI Agent Systems]]
- [[microsoft/memento]]
