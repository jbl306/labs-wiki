---
title: TACO
type: entity
created: 2026-04-23
last_verified: 2026-04-23
source_hash: "1ca1c01606b2b234d278cd0aefc974bff993603f4c4596baf0be8b058331d26e"
sources:
  - raw/2026-04-23-260419572v1pdf.md
concepts:
  - terminal-observation-compression
  - self-evolving-rule-pools-agent-compression
related:
  - "[[TerminalBench]]"
  - "[[Qwen3-Coder-480B-A35B]]"
tier: hot
tags: [terminal-agents, context-compression, rule-evolution, llm-agents, arxiv]
quality_score: 85
---

# TACO

## Overview

TACO is a plug-and-play framework for compressing terminal-agent observations during long-horizon CLI tasks. It was introduced in the 2026 paper *A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression* and is designed to reduce the token burden of verbose command-line feedback without hiding the signals an agent needs for subsequent decisions.

What makes TACO notable is that it does not treat compression as a fixed post-processing rule set. Instead, it evolves structured rules from actual trajectories, reuses high-value rules across tasks, and revises rules that prove too aggressive. That makes it a closer fit to tool-using agents than generic context summarization pipelines such as [[Context Management and Compaction Pipeline in Claude Code]], because it is specialized for command-conditioned terminal output.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Framework |
| Created | 2026-04-21 |
| Creator | Jincheng Ren, Siwei Wu, Yizhi Li, Kang Zhu, Shu Xu, Boyu Feng, Ruibin Yuan, Wei Zhang, Riza Batista-Navarro, Jian Yang, Chenghua Lin |
| URL | https://github.com/multimodal-art-projection/TACO |
| Status | Active |

## Core Concept

TACO inserts a compression layer into the standard terminal-agent loop. After a host agent issues a command and receives raw terminal output, TACO decides whether that observation should be passed through unchanged or compressed before the next model call. Outputs containing explicit failure cues such as syntax errors, exception traces, linker errors, or other critical diagnostics are preserved exactly; non-critical logs are filtered through task-specific rules.

The framework's core operator is summarized in the paper as:

$$
\tilde{O}_t =
\begin{cases}
O_t & \text{if } O_t \text{ is Critical} \\
F_{R_t}(O_t \mid C_t) & \text{otherwise}
\end{cases}
$$

where $R_t$ is the active task-level rule set and $F_{R_t}$ is a conservative rule-based compressor conditioned on the current command. In practice, this lets TACO keep stack traces, warning lines, and completion signals while stripping repetitive transfer progress, long compiler invocations, repeated package-install lines, or low-value disassembly noise.

## Rule Architecture

TACO organizes its knowledge into two layers. The first is a task-specific rule set that evolves during a single run. The second is a global rule pool that stores reusable rules discovered across many tasks. Rules are structured objects, not vague summaries: they contain a trigger regex, patterns to keep, patterns to strip, retention bounds such as `keep_first_n` and `keep_last_n`, and statistics such as confidence and successful application counts.

The global pool starts with 6 seed rules for common command categories including `git`, heredoc echo, `pip install`, `apt-get`, compiler output, and OpenSSL key generation. During a task, uncovered high-volume outputs trigger new-rule generation, while implicit complaints such as re-running a command to recover missing information cause TACO to suppress the responsible rule and generate a more conservative replacement. Effective rules are written back only if they were used successfully and retain enough confidence at task end.

## Performance & Evaluation

The paper evaluates TACO primarily on [[TerminalBench]] 1.0 and 2.0 and additionally on SWE-Bench Lite, CompileBench, DevEval, and CRUST-Bench. Across strong agent backbones, the paper reports consistent absolute gains on TerminalBench, with model-level improvements ranging from roughly 1% to 4% in many settings and overall benchmark gains spanning 0.36 to 6.02 points.

The efficiency story is equally important. For large models such as MiniMax-2.5, DeepSeek-V3.2, and [[Qwen3-Coder-480B-A35B]], TACO lowers per-step prompt-token cost by about 10% while preserving or improving trajectory quality. Under equal token budgets, it still outperforms the baseline, which suggests the gains are not just an artifact of spending more compute on longer trajectories.

## Convergence and Operating Regime

Because TACO is self-evolving, the paper also introduces a convergence diagnostic. It tracks retention of the Top-30 global rules between consecutive dataset runs and treats high retention as evidence that the reusable rule frontier has stabilized. In the reported ablations, the authors choose `k=30` retrieved rules and batch size `N=4`, noting that smaller batches propagate newly learned rules faster while larger batches improve throughput; one full round of self-evolution at the chosen setting takes about 4 days.

## Impact

TACO makes a strong case that [[The Context Hygiene Principle]] should not be applied only at the conversation level. In terminal-heavy agents, the largest source of waste is often the observation stream itself. By learning command-aware compression rules instead of relying only on fixed heuristics or generic summarizers, TACO turns context cleaning into a reusable capability that improves both efficiency and task success.

## Sources

- [[A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression]] — primary paper introducing the framework
