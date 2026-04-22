---
title: microsoft/memento
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: d3cabcf1e262cf327625ca3be9427a8fb7c93529209aca175575f612e0fe5bb4
sources:
- raw/2026-04-21-httpsgithubcommicrosoftmemento.md
source_url: https://github.com/microsoft/memento
tags:
- github
- python
tier: warm
knowledge_state: ingested
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- memento-blockwise-summarization-for-llms
- memory-aware-test-time-scaling
---

# microsoft/memento

## What it is

Memento is a Microsoft Research technique that extends the effective output length of an LLM by interleaving **reasoning blocks** and short **summary blocks** in chain-of-thought generation. After each reasoning block ends, the model emits a summary, then the block content is evicted from the KV cache; the model continues from the much shorter summary. The repo ships the data pipeline that converts ordinary CoT traces into the Memento block-structured format for SFT, plus a vLLM overlay that adds KV-cache block masking for efficient inference.

## Why it matters

Closest in spirit to a "scrollable" context window for long-horizon reasoning — directly relevant to anything we build that has to reason through long traces (debugging agents, the planning loop in nba-sprint, or any future research-style agent). Even if we don't train Memento models ourselves, the pipeline is a clean reference for how to *generate* training data that teaches a model to summarize-and-evict.

## Key concepts

- **Block / summary structure** — `<|block_start|> reasoning <|block_end|> <|summary_start|> summary <|summary_end|>`. See [[memento-blockwise-summarization-for-llms]].
- **KV-cache compaction** — After each summary, the upstream block tokens are evicted from the KV cache so attention only sees summaries from then on.
- **Special tokens** — `<think>` / `</think>` reasoning wrapper plus the four block/summary delimiter tokens.
- **5-stage data pipeline** — `seed_select → sentence_split → score → segment → summarize_iterative`. Stages 3 and 5 require an OpenAI-compatible LLM; the rest are deterministic.
- **DP segmentation** — Stage 4 uses dynamic programming over per-sentence boundary scores to choose optimal block boundaries.
- **vLLM overlay** — `vllm/install_overlay.sh` patches stock vLLM 0.13.0 to apply block masking at serve time.
- **Memory-aware test-time scaling** — More reasoning fits in a fixed context window. See [[memory-aware-test-time-scaling]].

## How it works

- Take raw CoT traces (e.g. from OpenThoughts) → split into sentences (preserving code/math) → score boundary candidates with an LLM → pick optimal block boundaries via DP → generate iterative block summaries with judge feedback.
- The result is SFT training data in Memento format that teaches the model to emit `<|summary_start|>...<|summary_end|>` after each reasoning block.
- At inference, the vLLM overlay (`block-masking-config`) detects summary-end tokens and compacts the KV cache, optionally keeping the last N blocks (`keep_last_n_blocks`).
- Works with any OpenAI-compatible API for the LLM-requiring pipeline stages (OpenAI, Together, Fireworks, Groq, or a local vLLM server).

## Setup

```bash
# Data pipeline — convert CoT traces to Memento format
pip install -r data/requirements.txt
export OPENAI_API_KEY=sk-...
cd data/pipeline
python run_full_pipeline.py \
    --input ../examples/example_trace.jsonl \
    --output-dir output/ \
    --model gpt-4o --limit 1

# vLLM inference with block masking
pip install vllm==0.13.0
cd vllm && bash install_overlay.sh
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/memento-checkpoint \
    --served-model-name memento --port 8010 \
    --max-model-len 32768 --gpu-memory-utilization 0.9 \
    --trust-remote-code \
    --chat-template chat_templates/memento_nosys.jinja \
    --block-masking-config '{"enable":true,"keep_last_n_blocks":0,"compact_on_summary_end":true,"require_assistant_section":true}'
```

## Integration notes

Research-grade — we don't currently serve our own models, so the inference overlay isn't immediately deployable. The data pipeline is the reusable artifact: it's a good reference for any synthesis pipeline we build (e.g. for distilling our own session diaries into a smaller model). Pairs conceptually with MemPalace's verbatim-then-retrieve story by tackling the *intra-session* compression problem MemPalace doesn't address.

## Caveats / Gotchas

- vLLM overlay is pinned to `vllm==0.13.0` — won't apply cleanly to newer vLLM.
- Pipeline stages 3 and 5 require an LLM; budget can be significant for large trace corpora.
- Released April 2026 with a single PR (Microsoft SECURITY.MD); APIs are fresh and unstable.
- Companion paper is in `docs/memento.pdf`; OpenMementos dataset on HuggingFace.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 377 |
| Primary language | Python |
| Topics | (none) |
| License | MIT |

## Source

- Raw dump: `raw/2026-04-21-httpsgithubcommicrosoftmemento.md`
- Upstream: https://github.com/microsoft/memento
