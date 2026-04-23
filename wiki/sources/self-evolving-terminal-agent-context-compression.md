---
title: "A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression"
type: source
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: "1ca1c01606b2b234d278cd0aefc974bff993603f4c4596baf0be8b058331d26e"
sources:
  - raw/2026-04-23-260419572v1pdf.md
source_url: https://arxiv.org/pdf/2604.19572
tags: [terminal-agents, context-compression, long-horizon-reasoning, benchmarks, arxiv]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 65
concepts:
  - terminal-observation-compression
  - self-evolving-rule-pools-agent-compression
related:
  - "[[TACO]]"
  - "[[TerminalBench]]"
  - "[[Qwen3-Coder-480B-A35B]]"
---

# A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression

## Summary

This paper introduces [[TACO]], a training-free framework for compressing terminal-agent observations without breaking long-horizon reasoning. Instead of relying on fixed heuristics, it evolves reusable compression rules from real trajectories, preserves critical error signals, and shows that better context hygiene improves both task success and token efficiency across terminal benchmarks.

## Key Points

- **Core problem**: Terminal agents often replay raw logs, build traces, and command output back into future prompts, causing context cost to grow roughly quadratically over long runs and burying the information that actually matters for the next step.
- **Framework introduced**: TACO is a plug-and-play terminal observation compression adapter that sits between command execution and the next model call, returning either the raw output for critical failures or a compressed version for non-critical noise.
- **Three-part architecture**: The method combines terminal output compression, intra-task rule-set evolution, and global rule-pool evolution so it can adapt within a task and also carry useful rules across tasks.
- **Rule format**: Compression rules are structured artifacts with trigger regexes, keep patterns, strip patterns, conservative first/last-line retention, priorities, confidence scores, and usage statistics instead of being opaque free-form summaries.
- **Safety mechanism**: TACO treats explicit error signals and exception traces as `Critical` and leaves them uncompressed; if later behavior suggests over-compression, the triggered rule is suppressed and replaced with a more conservative variant.
- **Seed initialization**: The global rule pool starts from 6 reusable rules covering common CLI noise such as `git` transfer progress, heredoc echo, `pip install`, `apt-get`, compiler command spam, and OpenSSL key-generation progress.
- **Benchmarks**: Main evaluation is on [[TerminalBench]] 1.0 and 2.0, with additional transfer tests on SWE-Bench Lite, CompileBench, DevEval, and CRUST-Bench.
- **Performance gains**: On TerminalBench, the paper reports consistent absolute accuracy gains of roughly 1% to 4% across strong agentic models, with larger aggregate gains ranging from 0.36 to 6.02 points depending on model and benchmark configuration.
- **Efficiency gains**: For high-capacity models such as MiniMax-2.5, DeepSeek-V3.2, and [[Qwen3-Coder-480B-A35B]], TACO cuts per-step prompt-token overhead by about 10% while also improving fixed-budget accuracy.
- **Convergence signal**: The paper defines a Top-30 rule-retention metric to detect when self-evolution has stabilized, and chooses `k=30` retrieved rules with batch size `N=4` as the best trade-off between accuracy, token cost, and runtime.

## Key Concepts

- [[Terminal Observation Compression]]
- [[Self-Evolving Rule Pools for Agent Compression]]
- [[The Context Hygiene Principle]]
- [[Context Management and Compaction Pipeline in Claude Code]]

## Related Entities

- **[[TACO]]** — The paper's self-evolving compression framework for terminal agents.
- **[[TerminalBench]]** — The primary benchmark family used to measure accuracy and token-efficiency gains.
- **[[Qwen3-Coder-480B-A35B]]** — A strong backbone model used in the paper's TerminalBench experiments.
