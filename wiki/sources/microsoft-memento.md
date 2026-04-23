---
title: microsoft/memento
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: 83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
source_url: https://github.com/microsoft/memento
tags: [github, llm, long-context, kv-cache, block-masking, vllm, chain-of-thought, microsoft]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 59
concepts:
  - memento-blockwise-summarization-for-llms
  - block-masking-for-llm-kv-cache-compaction
  - reasoning-trace-segmentation-and-iterative-summarization
related:
  - "[[Memento]]"
  - "[[OpenMementos Dataset]]"
  - "[[vLLM Block Masking Overlay]]"
  - "[[Microsoft]]"
---

# microsoft/memento

## What it is

`microsoft/memento` is an open-source research repo for extending the effective output length of large language models without increasing the base context window. It does that with a paired design: a training-data pipeline that converts chain-of-thought traces into alternating reasoning blocks and summaries, and a customized vLLM overlay that evicts completed blocks from the KV cache during inference. The README positions it as both a method and an executable stack for teaching models to summarize their own reasoning and then operationalizing that format at serving time.

## Why it matters

For `labs-wiki`, this repo is a strong reference point because it cleanly connects dataset construction, prompt/token protocol, and runtime systems work in one artifact instead of treating "longer reasoning" as a model-only problem. For our workspace more broadly, it is more valuable as a design pattern than a drop-in dependency: booking bots or homelab assistants would only benefit if we were willing to train or fine-tune a Memento-style checkpoint and serve it through a patched vLLM runtime.

## Architecture / Technical model

**Memento format** — The core output shape is a repeated block-summary structure: `<|block_start|> reasoning <|block_end|> <|summary_start|> summary <|summary_end|>`. The model keeps generating full reasoning, but only the summaries are meant to persist in active context across long runs.

> See [[Memento Blockwise Summarization for LLMs]].

**Special token protocol** — The repo uses `<think>...</think>` as the high-level reasoning wrapper, block delimiters for full reasoning spans, and summary delimiters for compressed carry-forward state. These token boundaries are what both the data pipeline and the runtime compaction logic key off.

> See [[Memento Blockwise Summarization for LLMs]].

**Data pipeline (`data/`)** — `data/pipeline/run_full_pipeline.py` chains five stages that turn raw chain-of-thought traces into supervised fine-tuning examples. It is the offline half of the project: the model has to learn to emit well-formed blocks and faithful summaries before the runtime overlay is useful.

> See [[Reasoning Trace Segmentation and Iterative Summarization]].

**Boundary scoring (`data/pipeline/score.py`)** — Sentence boundaries are scored on a `0-3` scale, where `0` is a poor mid-thought break and `3` is a strong topic shift. The pipeline supports two-pass scoring with coprime windows `(16, 11)` to stabilize boundary quality estimates before segmentation.

> See [[Reasoning Trace Segmentation and Iterative Summarization]].

**Dynamic-programming segmentation (`data/pipeline/segment.py`)** — Blocks are chosen by optimizing `avg_boundary_score - variance_penalty x CV(block_token_sizes)` while enforcing a minimum token budget (`--min-block-tokens`, default `200`). That gives balanced blocks instead of arbitrary fixed-size chunks.

> See [[Reasoning Trace Segmentation and Iterative Summarization]].

**Iterative summary refinement (`data/pipeline/summarize_iterative.py`)** — Each block gets an initial summary, then an LLM judge scores it on a `0-10` rubric. Summaries below the threshold are refined up to `--max-iterations` (default `3`), targeting roughly `10-20%` compression while preserving reasoning-critical details.

> See [[Reasoning Trace Segmentation and Iterative Summarization]].

**vLLM block masking overlay (`vllm/`)** — The repo ships only the modified files relative to stock vLLM 0.13.x. The overlay patches scheduler, engine, KV cache manager, worker, request state, and sampling logic so completed reasoning blocks can be compacted when `<|summary_end|>` is observed at generation time.

> See [[Block Masking for LLM KV Cache Compaction]].

**`BlockMaskingConfig`** — The runtime interface exposes knobs such as `keep_last_n_blocks`, `mask_delimiters`, `compact_on_summary_end`, `require_assistant_section`, `restart_mode`, `keep_last_block_for_answer`, `max_block_tokens`, and `debug`. These switches control what gets evicted, when compaction triggers, and how conservative the runtime is about preserving recent context.

> See [[Block Masking for LLM KV Cache Compaction]].

**Pipeline output contract** — The training pipeline writes `pipeline_results.jsonl`, where each line stores `task_id`, `sentences`, `boundary_scores`, `blocks`, `block_summaries`, `avg_final_score`, `num_blocks`, and `num_sentences`. That output is the handoff point between raw traces and Memento-style SFT data generation.

> See [[Reasoning Trace Segmentation and Iterative Summarization]].

## How it works

1. **Collect raw traces** — The pipeline starts from chain-of-thought traces such as OpenThoughts samples and filters out examples that are unusable for Memento training, including traces with CJK characters, traces missing complete `<think>...</think>` tags, and traces that are too short.

2. **Split into sentence-like units** — `sentence_split.py` breaks each trace into semantically coherent units while explicitly preserving code blocks, LaTeX math spans, multiline derivations, and list structure. The goal is to make later boundaries align with reasoning units instead of raw punctuation.

3. **Score candidate boundaries** — `score.py` asks an LLM to rate each boundary from `0` to `3`, where higher values indicate a cleaner conceptual transition. The optional two-pass mode uses coprime window sizes `16` and `11` to reduce sensitivity to any single local framing of the trace.

4. **Choose blocks with dynamic programming** — `segment.py` turns those local boundary scores into a global block plan. Instead of blindly packing every `N` sentences, it optimizes for high-quality breakpoints while also penalizing unstable block-size variance through the coefficient of variation term. The default `--variance-penalty` is `0.5`, and `--min-block-tokens` defaults to `200`.

5. **Summarize each block iteratively** — `summarize_iterative.py` first generates a compressed summary for every block, then runs an LLM judge over those summaries. If a summary scores below the default threshold `8.0`, it is refined with judge feedback, up to `3` iterations by default.

6. **Emit training-ready artifacts** — The resulting JSONL records preserve both the low-level segmentation output and the high-level block summaries. A typical line includes the sentence list, boundary scores, block spans, summary text, block count, sentence count, and average final summary score.

7. **Fine-tune a Memento-style checkpoint** — The repo itself does not prescribe one exact training script in the README, but the purpose of the data pipeline is clear: produce traces that teach a model to emit block-delimited reasoning and summary-delimited carry-forward state. Without that behavioral adaptation, runtime block masking would just delete information the model still expects to see verbatim.

8. **Patch stock vLLM for serving** — On the inference side, the repo assumes stock `vllm==0.13.0`, then applies the overlay from `vllm/` with `bash install_overlay.sh`. The installer overlays pure-Python changes, restores critical `.so`-interface files from the stock wheel, and verifies imports such as `BlockMaskingConfig`, `BlockMaskingProcessor`, `BlockMaskingState`, `LLM`, and `_custom_ops`.

9. **Serve with compaction enabled** — The OpenAI-compatible server entrypoint is standard `python -m vllm.entrypoints.openai.api_server`, but it receives a Memento-specific `--block-masking-config`. The example server uses `--max-model-len 32768`, `--gpu-memory-utilization 0.9`, and `keep_last_n_blocks: 0`, which means every completed block is eligible for compaction once its summary ends.

10. **Compact the KV cache at runtime** — During token-by-token generation, the patched scheduler watches for `<|summary_end|>`. When that marker arrives, it evicts the corresponding reasoning block from the KV cache while retaining the summary; with `mask_delimiters=false`, the block delimiters stay in cache, while `mask_delimiters=true` evicts them too.

11. **Continue reasoning from compressed state** — The active context now contains the prompt, the remaining recent material, and the accumulated summaries instead of the full token history of all prior reasoning blocks. That lets the model produce substantially more reasoning tokens within the same nominal context window, as long as the summaries remain faithful enough to support downstream reasoning.

## API / interface surface

| Surface | Location | What it exposes |
|---|---|---|
| End-to-end pipeline runner | `data/pipeline/run_full_pipeline.py` | Main CLI for converting raw traces into Memento-style outputs |
| Stage 1: seed selection | `data/pipeline/seed_select.py` | Filters and selects traces from OpenThoughts-style inputs |
| Stage 2: sentence splitting | `data/pipeline/sentence_split.py` | Structure-aware splitting that preserves code, math, and lists |
| Stage 3: boundary scoring | `data/pipeline/score.py` | LLM-based `0-3` boundary scoring, including two-pass mode |
| Stage 4: segmentation | `data/pipeline/segment.py` | Dynamic-programming block construction with size-variance penalty |
| Stage 5: summary refinement | `data/pipeline/summarize_iterative.py` | Iterative compression with judge feedback and score thresholding |
| OpenAI-compatible server | `python -m vllm.entrypoints.openai.api_server` | Serves a Memento checkpoint with `--block-masking-config` |
| Python inference API | `from vllm import LLM, SamplingParams` | Creates an `LLM(...)` object with `block_masking_config={...}` |
| Runtime config | `vllm/config/block_masking.py` | `BlockMaskingConfig` fields for compaction behavior |
| Chat template | `chat_templates/memento_nosys.jinja` | Template for Qwen3 models trained without a system prompt |

## Setup

```bash
# Data pipeline
pip install -r data/requirements.txt
export OPENAI_API_KEY=sk-...

cd data/pipeline
python run_full_pipeline.py \
    --input ../examples/example_trace.jsonl \
    --output-dir output/ \
    --model gpt-4o \
    --limit 1

# vLLM overlay + serving
cd ../../vllm
pip install vllm==0.13.0
bash install_overlay.sh

python -m vllm.entrypoints.openai.api_server \
    --model /path/to/memento-checkpoint \
    --served-model-name memento \
    --port 8010 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.9 \
    --trust-remote-code \
    --chat-template chat_templates/memento_nosys.jinja \
    --block-masking-config '{
        "enable": true,
        "keep_last_n_blocks": 0,
        "mask_delimiters": false,
        "compact_on_summary_end": true,
        "require_assistant_section": true
    }'
```

## Integration notes

This is best treated as a research reference for `labs-wiki` and for any future long-context agent experiments, not as a standard package dependency. If we ever wanted to apply it to the booking bots or other assistants, the real integration boundary would be "train or acquire a Memento-formatted checkpoint, then serve it through the patched vLLM path" rather than "pip install a library and call one helper."

## Caveats / Gotchas

- The repo is two systems, not one: the model must be trained to emit Memento-format traces, and the runtime must understand how to compact them.
- The data pipeline depends on an OpenAI-compatible API for scoring and summarization stages; the cheap path still needs external or local model access.
- The overlay is tied to **vLLM 0.13.x** and assumes a stock wheel patched in place rather than a clean plugin mechanism.
- Prefix caching must be disabled when using block masking (`enable_prefix_caching=False`); the overlay does not auto-correct this.
- If you want to inspect block markers in responses, requests need `skip_special_tokens=false`.
- Licensing is slightly split-brain: the repo root is MIT, while the vLLM overlay modifications are released under Apache 2.0 to match upstream vLLM.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 377 |
| Primary language | Python 91.2%, HTML 7.8%, CSS 0.5%, Shell 0.5%, Jinja 0.0% |
| Topics | Not listed in the raw dump |
| License | MIT (repo root); Apache 2.0 for vLLM overlay modifications |

## Related concepts

- [[Memento Blockwise Summarization for LLMs]]
- [[Block Masking for LLM KV Cache Compaction]]
- [[Reasoning Trace Segmentation and Iterative Summarization]]

## Source

- Raw dump: `raw/2026-04-21-httpsgithubcommicrosoftmemento.md`
- Upstream: https://github.com/microsoft/memento
