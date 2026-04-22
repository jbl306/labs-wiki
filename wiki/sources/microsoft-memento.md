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
ingest_method: manual-deepen-github-2026-04-22
quality_score: 90
concepts:
- memento-blockwise-summarization-for-llms
- memory-aware-test-time-scaling
- kv-cache-and-paged-attention-in-large-language-models
---

# microsoft/memento

## What it is

Memento is a Microsoft Research technique that extends the effective output length of an LLM by interleaving **reasoning blocks** and short **summary blocks** in chain-of-thought generation. After each reasoning block ends, the model emits a summary, then the block content is evicted from the KV cache; the model continues from the much shorter summary. The repo ships the data pipeline that converts ordinary CoT traces into the Memento block-structured format for SFT, plus a vLLM overlay that adds KV-cache block masking for efficient inference.

## Why it matters

Closest in spirit to a "scrollable" context window for long-horizon reasoning — directly relevant to anything we build that has to reason through long traces (debugging agents, the planning loop in nba-sprint, or any future research-style agent). Even if we don't train Memento models ourselves, the pipeline is a clean reference for how to *generate* training data that teaches a model to summarize-and-evict.

## Architecture / Technical model

**Block-structured CoT** — Each reasoning trace is split into `<|block_start|> reasoning <|block_end|> <|summary_start|> summary <|summary_end|>` pairs. Blocks contain verbose reasoning; summaries compress them to ~10–20% of original tokens while preserving logical dependencies. Wrapper tokens `<think>` / `</think>` enclose the entire chain.
> See [[memento-blockwise-summarization-for-llms]] for the full treatment.

**KV-cache compaction** — After the model generates a `<|summary_end|>` token, the vLLM scheduler evicts the upstream block's KV cache entries. Attention from that point forward can only see the summary, not the original reasoning. Peak cache size remains bounded even as total output tokens grow.
> See [[kv-cache-and-paged-attention-in-large-language-models]] for KV cache mechanics.

**5-stage data pipeline** — Converts raw CoT traces (e.g., OpenThoughts dataset) into Memento training data: (1) **seed_select** filters/samples traces; (2) **sentence_split** preserves code/math/LaTeX blocks while splitting into sentences; (3) **score** uses an LLM to rate boundary quality (0–3 scale) for each sentence pair, optionally with coprime two-pass windows (16, 11); (4) **segment** applies dynamic programming to maximize `avg_boundary_score - variance_penalty × CV(block_sizes)`; (5) **summarize_iterative** generates block summaries, scores them with an LLM judge (0–10 rubric), and refines up to `--max-iterations` if below `--score-threshold`. Stages 3 and 5 require LLM API access; the rest are deterministic. Checkpointing every N batches allows restarts.

**DP segmentation objective** — Stage 4 minimizes variance in block token counts while maximizing boundary scores. The coefficient of variation (CV) penalty ensures blocks stay balanced, avoiding a single massive block. Minimum block size (`--min-block-tokens`, default 200) prevents trivial one-sentence segmentations.

**vLLM overlay (block masking)** — Patches vLLM `0.13.0` with `BlockMaskingConfig`, `BlockMaskingState`, and scheduler hooks. The overlay is Python-only (no CUDA recompilation). `install_overlay.sh` rsync's modified `.py` files over a stock vLLM wheel, then restores pre-compiled interface files (`flash_attn_interface.py`, `_custom_ops.py`) to preserve extension compatibility. Server arg `--block-masking-config` JSON controls behavior: `enable`, `keep_last_n_blocks` (0 = compact all), `mask_delimiters` (false for Qwen3, true for Phi3/Phi4), `compact_on_summary_end`, `require_assistant_section`, `restart_mode` (evict + recompute summary KV), `max_block_tokens` (cap block length), `debug` (stdout trace). **Prefix caching must be disabled** (`enable_prefix_caching=False`).

**OpenAI-compatible API support** — Pipeline stages 3 and 5 work with any provider: OpenAI (default), Together AI, Fireworks, Groq, OpenRouter, local vLLM, Ollama. Set `--base-url` and `--api-key` (or `OPENAI_BASE_URL` / `OPENAI_API_KEY` env vars).

**Iterative summarization with judge feedback** — Stage 5 generates an initial summary for each block, scores it with an LLM judge, and refines if the score is below threshold. The judge rubric penalizes lost logical dependencies or over-compression. Up to `--max-iterations` refinement rounds; early-stop if a high score is reached. Target compression: 10–20% of block tokens.

**Memory-aware test-time scaling** — The core value proposition: a model trained on Memento format can produce more reasoning tokens within a fixed context window by evicting verbose blocks and retaining only their compressed summaries. Effective output length scales beyond the model's native context limit.
> See [[memory-aware-test-time-scaling]] for the theory.

## How it works

1. **Training data generation (data pipeline)**:
   - Filter seed traces (no CJK, must have complete `<think>...</think>`, minimum length)
   - Split into sentences, preserving code fences (triple-backtick, indented), LaTeX (`$$`, `$`, `\[...\]`), and list structures
   - Score each sentence boundary (0–3) with an LLM: 0 = mid-thought, 1 = weak break, 2 = good transition, 3 = major topic shift. Optional two-pass scoring with coprime window sizes (16, 11) averages results for robustness.
   - Run DP segmentation to find block boundaries that maximize score quality and minimize size variance (enforcing `--min-block-tokens`)
   - Generate iterative summaries: (a) summarize all blocks, (b) judge each summary (0–10), (c) refine those below threshold with judge feedback, (d) repeat up to `--max-iterations` or until threshold met
   - Output: `pipeline_results.jsonl` with `sentences`, `boundary_scores`, `blocks` (index ranges), `block_summaries`, `avg_final_score`, `num_blocks`, `num_sentences`

2. **SFT training**: Fine-tune a base model on the Memento-structured traces. The model learns to emit `<|summary_start|>...<|summary_end|>` after each reasoning block. Companion paper + OpenMementos dataset on HuggingFace.

3. **Inference (vLLM with block masking)**:
   - Serve the Memento checkpoint via `vllm.entrypoints.openai.api_server` with `--block-masking-config` JSON
   - Model generates block → summary → block → summary in sequence
   - Each time `<|summary_end|>` is emitted, the scheduler compacts the KV cache: evicts the upstream block tokens (and optionally delimiters if `mask_delimiters=true`), preserves the summary tokens
   - If `keep_last_n_blocks > 0`, the most recent N blocks are retained in full; otherwise all blocks are compacted (`keep_last_n_blocks=0`)
   - Use `skip_special_tokens=false` in the sampling request to see the block/summary markers in the output
   - Debug mode (`"debug": true`) logs every block event (started, ended, summary started/ended, compaction triggered) with token positions to stdout

4. **OpenAI-compatible client**: Query the vLLM server like any OpenAI chat endpoint. Chat template (`--chat-template chat_templates/memento_nosys.jinja`) formats user/assistant messages; system prompts are ignored if using the `nosys` template.

## API / interface surface

**Data pipeline CLI** (`run_full_pipeline.py`):
- `--input` — JSONL file or HuggingFace dataset directory
- `--output-dir` — Results directory (creates `pipeline_results.jsonl`)
- `--model` — Model for stages 3 and 5 (default: `gpt-4o`)
- `--api-key`, `--base-url` — API credentials (or env vars)
- `--workers` — Parallel workers (default: 1)
- `--batch-size`, `--checkpoint-every` — Batch processing and checkpoint intervals
- `--limit` — Max tasks to process (for smoke tests)
- `--two-pass-scoring` — Enable coprime window averaging
- `--variance-penalty` — Block size CV penalty (default: 0.5)
- `--max-block-size`, `--min-block-tokens` — Block size constraints
- `--max-iterations`, `--score-threshold` — Summarization refinement params (default: 3 iterations, 8.0 threshold)
- `--include-problem`, `--include-original-cot` — Output verbosity flags
- `--no-early-stop`, `--max-consecutive-failures` — Failure handling

**vLLM inference CLI** (`python -m vllm.entrypoints.openai.api_server`):
- `--model` — Path to Memento checkpoint
- `--served-model-name`, `--port` — API server config
- `--max-model-len`, `--gpu-memory-utilization` — Memory tuning
- `--trust-remote-code`, `--chat-template` — Model-specific flags
- `--block-masking-config` — JSON config for block masking (see Architecture section)
- `--enable-prefix-caching=false` — **Must be disabled** when using block masking

**Python API** (programmatic inference):
```python
from vllm import LLM, SamplingParams
llm = LLM(model="path/to/checkpoint", block_masking_config={...}, max_model_len=32768, enable_prefix_caching=False)
params = SamplingParams(temperature=0.6, top_p=0.95, top_k=20, max_tokens=16384)
outputs = llm.generate([prompt], params)
```

**Output format** (`pipeline_results.jsonl`):
- `task_id` — Trace identifier (e.g., `ot3-train-00001`)
- `sentences` — List of sentence strings
- `boundary_scores` — Per-boundary scores from stage 3
- `blocks` — List of `[start_idx, end_idx]` sentence ranges
- `block_summaries` — One summary per block
- `avg_final_score` — Mean judge score across summaries
- `num_blocks`, `num_sentences` — Counts

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

- **vLLM version lock**: Overlay is pinned to `vllm==0.13.0` and extracted from `0.13.1.dev0`. Won't apply cleanly to `0.14+` because scheduler internals changed. The installer restores `flash_attn_interface.py` and `_custom_ops.py` from the stock wheel to prevent function signature mismatches with pre-compiled extensions.
- **Prefix caching conflict**: Block masking is incompatible with vLLM's prefix caching (`enable_prefix_caching=False` is required, but not automatically set). Enabling both causes undefined KV cache states.
- **LLM costs**: Pipeline stages 3 (scoring) and 5 (iterative summarization) send every trace through an LLM multiple times. For a 10k-trace corpus with two-pass scoring and 3 refinement iterations, expect significant API spend (OpenThoughts-114k scale). Use a local vLLM server or cheaper model for cost control.
- **API stability**: Released April 2026 with a single PR (Microsoft SECURITY.MD). No semver tags yet. APIs (pipeline stage flags, block-masking-config schema) are fresh and subject to change.
- **Special token handling**: Must set `skip_special_tokens=false` in sampling requests to preserve `<|block_start|>`, `<|summary_end|>`, etc. in output text. Without this, delimiters are stripped and the structure is lost.
- **Companion resources**: Paper in `docs/memento.pdf` (not indexed in arXiv as of April 2026). OpenMementos dataset on HuggingFace (formatted training data, not raw traces).
- **Block size trade-offs**: Larger `--min-block-tokens` reduces block count (less overhead, fewer summaries) but increases peak KV cache per block. Smaller values increase segmentation opportunities but add summarization cost. Default 200 tokens is a middle ground.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 377 |
| Primary language | Python |
| Topics | (none) |
| License | MIT |

## Related concepts

- [[memento-blockwise-summarization-for-llms]]
- [[memory-aware-test-time-scaling]]
- [[kv-cache-and-paged-attention-in-large-language-models]]
- [[attention-mechanism-in-large-language-models]]
- [[flash-attention-in-large-language-models]]

## Source

- Raw dump: `raw/2026-04-21-httpsgithubcommicrosoftmemento.md`
- Upstream: https://github.com/microsoft/memento
