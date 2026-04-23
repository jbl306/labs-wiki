---
title: "Recursive Language Models"
type: source
created: '2026-04-21'
last_verified: '2026-04-23'
source_hash: 7368a08484d58101c8102490723a5cbfabe63a85dde56bb84b8cde3ecabf99e8
sources:
  - raw/2026-04-10-251224601v2pdf.md
  - raw/2026-04-23-251224601v2pdf.md
source_url: https://arxiv.org/abs/2512.24601
tags: [language-models, long-context, recursion, inference-time-scaling, arxiv]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 84
related:
  - "[[RLM-Qwen3-8B]]"
  - "[[GPT-5]]"
  - "[[Qwen3-Coder-480B-A35B]]"
---

# Recursive Language Models

## Summary

This paper reframes long-context inference as an environment-interaction problem instead of a bigger-context-window problem. Recursive Language Models (RLMs) place the prompt in a persistent REPL environment, let the model inspect it symbolically, and allow recursive self-calls over prompt slices; that setup reaches 10M+ token inputs, beats common long-context baselines, and supports the first post-trained native recursive model, [[RLM-Qwen3-8B]].

## Key Points

- **Core reframing**: The user prompt is stored as a variable in a persistent REPL environment instead of being copied wholesale into the root model context window.
- **Root-loop design**: The root model only sees constant-size metadata about prompt state and stdout, so the working history grows with control traces rather than with the full prompt length.
- **Three defining properties**: RLMs require a symbolic handle to the prompt, programmatic construction of the final answer via environment variables, and symbolic recursion through sub-RLM calls executed inside code.
- **Formal scaling claim**: The paper argues RLMs can support effectively unbounded input tokens, unbounded output tokens, and semantic work on the order of $\Omega(|P|)$ or even $\Omega(|P|^2)$ over a prompt $P$.
- **Benchmarks**: Evaluation covers S-NIAH, BrowseComp-Plus (1K docs), OOLONG, OOLONG-Pairs, and LongBench-v2 CodeQA to span constant-, linear-, and quadratic-complexity long-context tasks.
- **Base models**: The main experiments use [[GPT-5]] and [[Qwen3-Coder-480B-A35B]] as both direct baselines and recursive sub-call models.
- **Length regime**: Controlled tasks scale prompt lengths from $2^{13}$ to $2^{18}$ tokens, and the paper reports RLM behavior in the 10M+ token regime and up to two orders of magnitude beyond model context windows.
- **Performance gains**: On OOLONG, RLMs improve over the base model by 28.4% with GPT-5 and 33.3% with Qwen3-Coder; on OOLONG-Pairs, base models stay below 0.1% F1 while RLM(GPT-5) reaches 58.0% and RLM(Qwen3-Coder) reaches 23.1%.
- **Cost profile**: On BrowseComp-Plus (1K), the paper estimates naive GPT-5-mini ingestion of 6-11M tokens would cost roughly $1.50-$2.75, while RLM(GPT-5) averages $0.99 and beats summarization and retrieval baselines by more than 29%.
- **Ablation result**: A REPL-only ablation can already exceed base context limits, but recursive sub-calls deliver an extra 10%-59% gain on the most information-dense tasks.
- **Native recursion training**: [[RLM-Qwen3-8B]] is fine-tuned from Qwen3-8B on 1,000 filtered LongBenchPro trajectories and improves average downstream RLM performance by 28.3%.
- **Observed behaviors**: The authors report regex-based filtering, simple chunking strategies, and variable-based output stitching as common emergent patterns in successful RLM trajectories.

## Key Concepts

- Recursive language models
- Inference-time scaling
- Symbolic recursion
- Long-context processing
- Context-compaction baselines

## Related Entities

- **[[RLM-Qwen3-8B]]** — The paper's proof-of-concept native recursive model, fine-tuned to make better REPL and sub-call decisions.
- **[[GPT-5]]** — Frontier closed model used as a direct baseline and as the root/sub-call model in the strongest RLM runs.
- **[[Qwen3-Coder-480B-A35B]]** — Frontier open model used for baseline comparisons and for generating trajectories used in RLM-Qwen3-8B training.
