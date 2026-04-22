---
title: https://github.com/microsoft/memento
type: url
captured: 2026-04-21 01:25:10.960840+00:00
source: android-share
url: https://github.com/microsoft/memento
content_hash: sha256:83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2
tags: []
status: pending
last_refreshed: '2026-04-22T02:45:18+00:00'
---

https://github.com/microsoft/memento

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:45:18+00:00
- source_url: https://github.com/microsoft/memento
- resolved_url: https://github.com/microsoft/memento
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: microsoft/memento
Description: None
Stars: 377
Language: Python

## README

# Memento

[**Paper (PDF)**](docs/memento.pdf) | [**OpenMementos Dataset**](https://huggingface.co/datasets/microsoft/OpenMementos)

**Memento** extends the effective output length of large language models by splitting chain-of-thought reasoning into **blocks** and **summaries** (memento). After each reasoning block, the model generates a short summary, then the block content is evicted from the KV cache. The model continues from the summary with a shorter context, enabling more reasoning within a fixed context window.

## Special tokens

| Token | Purpose |
|-------|---------|
| `<think>` / `</think>` | Reasoning wrapper |
| `<\|block_start\|>` / `<\|block_end\|>` | Reasoning block boundaries |
| `<\|summary_start\|>` / `<\|summary_end\|>` | Summary (memento block) boundaries |

**Block structure:** `<|block_start|> reasoning <|block_end|> <|summary_start|> summary <|summary_end|>`

## Repository layout

| Directory | Description |
|-----------|-------------|
| [`data/`](data/) | Data pipeline — converts raw CoT traces into the Memento format (block boundaries + summaries) for SFT training |
| [`vllm/`](vllm/) | vLLM overlay — adds KV cache block masking to stock vLLM for efficient Memento inference |

## Quick start

### Data pipeline

Convert chain-of-thought traces into Memento training data:

```bash
pip install -r data/requirements.txt
export OPENAI_API_KEY=sk-...   # or any OpenAI-compatible provider

cd data/pipeline
python run_full_pipeline.py \
    --input ../examples/example_trace.jsonl \
    --output-dir output/ \
    --model gpt-4o \
    --limit 1
```

See [data/README.md](data/README.md) for full documentation.

### vLLM inference with block masking

* Step 1: Set Up the Environment
    Build a customized vllm with block masking support:
    ```bash
    pip install vllm==0.13.0
    cd vllm
    bash install_overlay.sh
    ```

* Step 2: Serve a Memento Model with KV Cache Compaction
    To expose the model through an API-compatible server, run:
    ```bash
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
            "require_assistant_section": true,
            "debug": true
        }'
    ```

    See [vllm/README.md](vllm/README.md) for full documentation, including API usage and alternative setup options.

## License

This project is licensed under the [MIT License](LICENSE).

Languages: Python 91.2%, HTML 7.8%, CSS 0.5%, Shell 0.5%, Jinja 0.0%

## Recent Commits

- 2026-04-08 d8c10e6 Vasilis Kontonis: Add Memento blogpost and Pages deployment
- 2026-04-08 ebacb0c Vasileios Kontonis: Initial release: Memento data pipeline, vLLM block masking overlay, and paper

## Recently Merged PRs (top 10)

- #1 Adding Microsoft SECURITY.MD (merged 2026-03-25)


## File: data/.gitignore

```
# Pipeline output directories
**/output/
**/runs/
**/checkpoint.json
**/*.jsonl.tmp

# Python cache
__pycache__/
*.py[cod]
*$py.class

# Logs
*.log

# Environment
.env

```


## File: data/README.md

```
# Memento Data Pipeline

This pipeline converts raw chain-of-thought (CoT) reasoning traces into the **Memento format** — with block boundaries and compressed summaries — used for SFT training.

## Pipeline Overview

The pipeline processes each CoT trace through 5 stages:

| Stage | Script | Description | Requires LLM? |
|-------|--------|-------------|----------------|
| 1 | `seed_select.py` | Select traces from OpenThoughts dataset | No |
| 2 | `sentence_split.py` | Split CoT into sentences (preserves code/math blocks) | No |
| 3 | `score.py` | Score boundary quality between sentences (0-3) | **Yes** |
| 4 | `segment.py` | Optimal segmentation into blocks via DP | No |
| 5 | `summarize_iterative.py` | Generate & refine block summaries with judge feedback | **Yes** |

The unified runner `run_full_pipeline.py` chains all stages together.

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up API access

The pipeline works with any **OpenAI-compatible API**:

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Or any compatible provider (Together AI, Fireworks, Groq, etc.)
export OPENAI_API_KEY=your-key
export OPENAI_BASE_URL=https://api.together.xyz/v1

# Or local vLLM server (no key needed)
export OPENAI_BASE_URL=http://localhost:8000/v1
```

### 3. Run the pipeline

```bash
cd data/pipeline

# Process a single trace (smoke test)
python run_full_pipeline.py \
    --input ../examples/example_trace.jsonl \
    --output-dir output/ \
    --model gpt-4o \
    --limit 1 \
    --include-problem

# Process a full dataset with parallelism
python run_full_pipeline.py \
    --input /path/to/openthoughts_subset.jsonl \
    --output-dir runs/my_run \
    --model gpt-4o \
    --workers 8 \
    --batch-size 10 \
    --checkpoint-every 100

# Using a local vLLM server
python run_full_pipeline.py \
    --input traces.jsonl \
    --output-dir runs/local_run \
    --model Qwen/Qwen3-32B \
    --base-url http://localhost:8000/v1 \
    --api-key no-key \
    --workers 4
```

### Supported Providers

| Provider | `--base-url` | Example `--model` |
|----------|-------------|-------------------|
| OpenAI (default) | *(not needed)* | `gpt-4o`, `gpt-4o-mini` |
| Together AI | `https://api.together.xyz/v1` | `Qwen/Qwen3-32B` |
| Fireworks | `https://api.fireworks.ai/inference/v1` | `accounts/fireworks/models/qwen3-32b` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` |
| OpenRouter | `https://openrouter.ai/api/v1` | `openai/gpt-4o` |
| Local vLLM | `http://localhost:8000/v1` | *(your served model)* |
| Ollama | `http://localhost:11434/v1` | `llama3.1` |

## Pipeline Stages in Detail

### Stage 1: Seed Selection (`seed_select.py`)

Selects and filters traces from the [OpenThoughts](https://huggingface.co/datasets/open-thoughts/OpenThoughts-114k) dataset. Filters out:
- Traces with Chinese/CJK characters
- Traces without complete `<think>...</think>` tags
- Traces that are too short

### Stage 2: Sentence Splitting (`sentence_split.py`)

Splits CoT text into semantically coherent sentences while preserving:
- Code blocks (fenced and indented)
- Math expressions (LaTeX `$$...$$`, `$...$`, `\[...\]`)
- Multi-line derivations
- List structures

### Stage 3: Boundary Scoring (`score.py`)

Uses an LLM to score each boundary between sentences (0-3):
- **0**: Poor break (mid-thought, mid-calculation)
- **1**: Weak break (minor transition)
- **2**: Good break (clear transition)
- **3**: Strong break (major topic shift)

Supports two-pass scoring with coprime window sizes (16, 11) for more robust results.

### Stage 4: Segmentation (`segment.py`)

Optimal block segmentation using dynamic programming:
- Maximizes: `avg_boundary_score - variance_weight × CV(block_token_sizes)`
- Enforces minimum block size in tokens
- Produces balanced blocks that align with natural reasoning boundaries

### Stage 5: Iterative Summarization (`summarize_iterative.py`)

For each block, generates a compressed summary with iterative refinement:
1. Initial summarization of all blocks
2. LLM judge scores each summary (0-10 rubric)
3. If score < threshold, refine with judge feedback
4. Repeat up to `--max-iterations` times

Target compression: ~10-20% of block tokens while preserving all logically relevant information.

## CLI Reference

```
python run_full_pipeline.py [OPTIONS]

Required:
  --input PATH              Input JSONL file or HuggingFace dataset directory
  --output-dir PATH         Output directory for results

API Configuration:
  --model MODEL             Model name (default: gpt-4o)
  --api-key KEY             API key (default: OPENAI_API_KEY env var)
  --base-url URL            Base URL (default: OPENAI_BASE_URL env var or OpenAI)

Processing:
  --workers N               Parallel workers (default: 1)
  --batch-size N            Tasks per checkpoint batch (default: 10)
  --checkpoint-every N      Checkpoint interval (default: 10)
  --limit N                 Max tasks to process

Scoring (Stage 3):
  --two-pass-scoring        Use two-pass coprime window scoring
  --include-problem         Include problem text in output

Segmentation (Stage 4):
  --variance-penalty F      Block size variance penalty (default: 0.5)
  --max-block-size N        Max sentences per block
  --min-block-tokens N      Min tokens per block (default: 200)

Summarization (Stage 5):
  --max-iterations N        Max refinement iterations (default: 3)
  --score-threshold F       Early stop score threshold (default: 8.0)

Output:
  --include-original-cot    Include original CoT in output
  --no-early-stop           Disable failure-based early stopping
  --max-consecutive-failures N  Failure threshold (default: 20)
```

## Output Format

The pipeline produces `pipeline_results.jsonl` where each line is a JSON object:

```json
{
  "task_id": "ot3-train-00001",
  "sentences": ["First sentence...", "Second sentence..."],
  "boundary_scores": [0.0, 2.5, 1.0, 3.0],
  "blocks": [[0, 5], [6, 12], [13, 20]],
  "block_summaries": ["Summary of block 1...", "Summary of block 2...", "Summary of block 3..."],
  "avg_final_score": 8.5,
  "num_blocks": 3,
  "num_sentences": 21
}
```


```


## File: data/requirements.txt

```
openai>=1.0.0
tiktoken>=0.5.0
datasets>=2.0.0
transformers>=4.30.0
tqdm>=4.0.0
numpy

```


## File: LICENSE

```
MIT License

Copyright (c) 2026 Microsoft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


## File: vllm/README.md

```
# vLLM Block Masking Overlay

Custom modifications to [vLLM](https://github.com/vllm-project/vllm) that add **block masking** support for Memento-style inference. During generation, completed reasoning blocks are compacted (evicted) from the KV cache, keeping only their summaries. This allows the model to produce more reasoning tokens within a fixed context window.

## How it works

A Memento model generates structured chain-of-thought with special tokens:

```
<think>
<|block_start|> ... reasoning ... <|block_end|>
<|summary_start|> ... compressed summary ... <|summary_end|>

<|block_start|> ... more reasoning ... <|block_end|>
<|summary_start|> ... summary ... <|summary_end|>
...
</think>
Final answer
```

When block masking is enabled, the vLLM scheduler watches for `<|summary_end|>` during token-by-token generation. Each time a block's summary completes, the block's reasoning content is evicted from the KV cache. The model continues from the summary with a shorter effective context.

With `mask_delimiters=False` (Qwen3 style), delimiter tokens (`<|block_start|>`, `<|block_end|>`) are **preserved** in the cache; only the content between them is evicted. With `mask_delimiters=True` (Phi3/Phi4 style), the delimiters are evicted too.

## What's here

This directory contains **only the files modified or added** relative to stock vLLM. It is not a full vLLM installation — it's an overlay that patches an existing vLLM install.

**New files:**
- `vllm/config/block_masking.py` — `BlockMaskingConfig` dataclass
- `vllm/v1/core/block_masking/` — Per-request state tracker and token processor
- `vllm/v1/sample/logits_processor/block_length_cap.py` — Optional block length cap
- `chat_templates/` — Chat templates for Memento models
- `install_overlay.sh` — Automated installer

**Modified vLLM files** — scheduler, engine, KV cache manager, worker, config, and request types (see `vllm/` tree).

## Base version

Compatible with **vLLM 0.13.x**. Overlay files were extracted from stock vLLM `0.13.1.dev0` with block masking patches applied.

## Installation

### Quick install (overlay on existing vLLM)

```bash
# 1. Install stock vLLM 0.13.x
pip install vllm==0.13.0

# 2. Apply the Memento overlay
cd vllm/
bash install_overlay.sh
```

### How the overlay installer works

The block masking changes are pure Python — no C++/CUDA recompilation needed. The installer patches `.py` files on top of a stock vLLM wheel while preserving the pre-compiled extensions:

1. **Find the installed vLLM** — locates the `vllm/` package in your Python environment's site-packages (carefully skipping the local `vllm/` directory in the repo).

2. **Download the stock wheel** — fetches the matching release wheel from PyPI (e.g. `vllm==0.13.0`) and extracts its `.py` files to `/tmp/vllm_stock/` for reference.

3. **rsync all `.py` files** — copies every Python file from `vllm/vllm/` in this repo on top of the installed package. This applies all block masking modifications (config, scheduler, engine, worker, KV cache manager, etc.) in one shot.

4. **Restore `.so`-interface files** — the overlay's upstream base may have newer function signatures than the compiled `.so` extensions expect. The installer restores two critical files from the stock wheel:
   - `vllm_flash_attn/flash_attn_interface.py` — FlashAttention wrapper (arg count must match the compiled `_C` extension)
   - `_custom_ops.py` — custom op bindings

5. **Verify** — imports `BlockMaskingConfig`, `BlockMaskingProcessor`, `BlockMaskingState`, `LLM`, and `_custom_ops` to confirm everything loads.

### From source

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm && git checkout 85f55c943

# Copy overlay files on top
cp -r /path/to/memento/vllm/vllm/* vllm/

# Build
pip install -e .
```

## Usage

### OpenAI-compatible server

```bash
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
        "require_assistant_section": true,
        "debug": true
    }'
```

Then query it with any OpenAI-compatible client:

```bash
curl http://localhost:8010/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "memento",
        "messages": [{"role": "user", "content": "What is 2+3? Put your answer in \\boxed{}."}],
        "max_tokens": 16384,
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "skip_special_tokens": false
    }'
```

> Set `skip_special_tokens: false` to see the `<|block_start|>` / `<|summary_end|>` markers in the response text.

### Python API

```python
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

model_path = "path/to/memento-checkpoint"
tokenizer = AutoTokenizer.from_pretrained(model_path)
prompt = tokenizer.apply_chat_template(
    [{"role": "user", "content": "What is 2+3? Put your answer in \\boxed{}."}],
    tokenize=False,
    add_generation_prompt=True,
)

llm = LLM(
    model=model_path,
    block_masking_config={
        "enable": True,
        "keep_last_n_blocks": 0,
        "mask_delimiters": False,
        "compact_on_summary_end": True,
    },
    max_model_len=32768,
    enable_prefix_caching=False,
)

params = SamplingParams(temperature=0.6, top_p=0.95, top_k=20, max_tokens=16384)
outputs = llm.generate([prompt], params)
print(outputs[0].outputs[0].text)
```

## Block masking parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable` | bool | `false` | Enable block masking |
| `keep_last_n_blocks` | int | `0` | Blocks to keep in KV cache. `0` = compact all, `-1` = disabled (no compaction) |
| `mask_delimiters` | bool | `false` | Include delimiter tokens in compaction range. `false` for Qwen3/OLMo3, `true` for Phi3/Phi4 |
| `compact_on_summary_end` | bool | `true` | Trigger compaction when `<|summary_end|>` is generated |
| `require_assistant_section` | bool | `true` | Only activate block masking inside assistant turns |
| `restart_mode` | bool | `false` | Evict block + recompute summary KV (alternative to compact mode) |
| `keep_last_block_for_answer` | bool | `false` | Defer last block compaction to preserve context for the final answer |
| `max_block_tokens` | int | `0` | Cap block length (0 = unlimited) |
| `debug` | bool | `false` | Print `[BlockMasking]` events to stdout |

## Chat templates

- `chat_templates/memento_nosys.jinja` — For Qwen3 models trained **without** a system prompt. System messages are silently ignored.

Use with `--chat-template` when launching the server.

## Important notes

- **Prefix caching must be disabled** when using block masking (`enable_prefix_caching=False`). The overlay does not set this automatically.
- **`skip_special_tokens=False`** is needed in the sampling request to preserve block/summary markers in the output text.
- Debug mode (`"debug": true`) logs every block lifecycle event (`started`, `ended`, `summary started/ended`, `compaction triggered`) with token positions to stdout.

## License

vLLM is licensed under [Apache License 2.0](https://github.com/vllm-project/vllm/blob/main/LICENSE). Our modifications are released under the same license.

```


## File: SECURITY.md

```
<!-- BEGIN MICROSOFT SECURITY.MD V1.0.0 BLOCK -->

## Security

Microsoft takes the security of our software products and services seriously, which
includes all source code repositories in our GitHub organizations.

**Please do not report security vulnerabilities through public GitHub issues.**

For security reporting information, locations, contact information, and policies,
please review the latest guidance for Microsoft repositories at
[https://aka.ms/SECURITY.md](https://aka.ms/SECURITY.md).

<!-- END MICROSOFT SECURITY.MD BLOCK -->
```


## File: .github/workflows/static.yml

```
name: Deploy Blogpost Pages

on:
  push:
    branches:
      - main
    paths:
      - blogpost/**
      - .github/workflows/static.yml
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Configure GitHub Pages
        uses: actions/configure-pages@v5

      - name: Build Pages artifact
        run: |
          set -eu

          mkdir -p _site/blogpost
          cp blogpost/index.html _site/blogpost/
          cp -R blogpost/css _site/blogpost/
          cp -R blogpost/figures _site/blogpost/
          printf '' > _site/.nojekyll

          cat > _site/index.html <<'EOF'
          <!DOCTYPE html>
          <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="0; url=./blogpost/">
            <title>Memento Blogpost Redirect</title>
            <link rel="canonical" href="./blogpost/">
          </head>
          <body>
            <p>Redirecting to <a href="./blogpost/">the Memento blogpost</a>.</p>
          </body>
          </html>
          EOF

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: _site

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5

```


## File: blogpost/figures/build_animation.py

```
#!/usr/bin/env python3
"""Generate animation.html from example_response.json and the HTML template."""
import json
import re

with open("example_response.json") as f:
    data = json.load(f)

# Build JS SEGMENTS array using backtick template literals
seg_lines = []
for seg in data["segments"]:
    t = seg["type"]
    idx = seg["block_idx"]
    tokens = seg["approx_tokens"]
    text = seg["text"]
    # Escape for JS backtick template literal: only backticks and ${
    text = text.replace("\\", "\\\\")   # \ -> \\
    text = text.replace("`", "\\`")     # ` -> \`
    text = text.replace("${", "\\${")   # ${ -> \${
    seg_lines.append(f'  {{type:"{t}", idx:{idx}, text:`{text}`, tokens:{tokens}}},')

segments_js = "const SEGMENTS = [\n" + "\n".join(seg_lines) + "\n];"

problem_text = data["problem"]

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
/* ===== Animation Figure Styles ===== */
.memento-demo {
  font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
  max-width: 1060px;
  margin: 32px auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.demo-header {
  background: #f7f9fb;
  padding: 14px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.demo-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1a1a2e;
}

.demo-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.demo-controls button {
  background: #268bd2;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.demo-controls button:hover { background: #1a6fb5; }
.demo-controls button:disabled { background: #ccc; cursor: not-allowed; }

.demo-controls button.secondary {
  background: #fff;
  color: #268bd2;
  border: 1px solid #268bd2;
}
.demo-controls button.secondary:hover { background: #d6eaf8; }

.speed-control {
  font-size: 0.8rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.speed-control input[type="range"] {
  width: 80px;
}

.demo-body {
  display: grid;
  grid-template-columns: 1fr 340px;
  min-height: 500px;
}

/* ---- Left: generation view ---- */
.gen-panel {
  padding: 16px 20px;
  overflow-y: auto;
  max-height: 600px;
  border-right: 1px solid #e0e0e0;
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 0.88rem;
  line-height: 1.6;
  color: #303030;
}

.problem-text {
  background: #f7f9fb;
  border-left: 3px solid #268bd2;
  padding: 10px 14px;
  margin-bottom: 16px;
  font-size: 0.85rem;
  border-radius: 3px;
}

.problem-text strong {
  font-family: 'Source Sans 3', sans-serif;
  color: #1a1a2e;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.gen-segment {
  margin: 0;
  padding: 10px 14px;
  border-radius: 4px;
  position: relative;
  transition: opacity 0.4s, max-height 0.5s ease;
  overflow: hidden;
}

.gen-segment.block {
  background: rgba(38, 139, 210, 0.06);
  border-left: 3px solid #268bd2;
  margin-bottom: 2px;
}

.gen-segment.summary {
  background: rgba(211, 54, 130, 0.06);
  border-left: 3px solid #d33682;
  margin-bottom: 12px;
  font-style: italic;
}

.gen-segment.answer {
  background: rgba(133, 153, 0, 0.08);
  border-left: 3px solid #859900;
  margin-bottom: 4px;
}

.gen-segment .seg-label {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
  display: block;
}

.gen-segment.block .seg-label { color: #268bd2; }
.gen-segment.summary .seg-label { color: #d33682; }
.gen-segment.answer .seg-label { color: #859900; }

.gen-segment.masked {
  opacity: 0.2;
  max-height: 42px;
  position: relative;
}

.gen-segment.masked::after {
  content: '— masked from attention —';
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Source Sans 3', sans-serif;
  font-size: 0.75rem;
  color: #999;
  font-style: italic;
  font-weight: 600;
}

.gen-segment.active {
  box-shadow: 0 0 0 2px #268bd2;
}

.gen-segment.summary.active {
  box-shadow: 0 0 0 2px #d33682;
}

/* Typewriter cursor */
.cursor {
  display: inline-block;
  width: 2px;
  height: 1.1em;
  background: #268bd2;
  animation: blink 0.7s step-end infinite;
  vertical-align: text-bottom;
  margin-left: 1px;
}

@keyframes blink {
  50% { opacity: 0; }
}

/* ---- Right: KV cache chart ---- */
.kv-panel {
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kv-panel h4 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1a1a2e;
}

.kv-chart-container {
  flex: 1;
  position: relative;
  min-height: 280px;
}

.kv-chart-container canvas {
  width: 100%;
  height: 100%;
}

.kv-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.kv-stat {
  background: #f7f9fb;
  border-radius: 4px;
  padding: 8px 10px;
  text-align: center;
}

.kv-stat .stat-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #888;
  margin-bottom: 2px;
}

.kv-stat .stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a2e;
  font-variant-numeric: tabular-nums;
}

.kv-stat .stat-value.memento { color: #d33682; }
.kv-stat .stat-value.vanilla { color: #268bd2; }

.kv-legend {
  display: flex;
  gap: 16px;
  font-size: 0.75rem;
  color: #666;
  justify-content: center;
}

.kv-legend span::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 3px;
  margin-right: 4px;
  vertical-align: middle;
  border-radius: 1px;
}

.kv-legend .leg-memento::before { background: #d33682; }
.kv-legend .leg-vanilla::before { background: #268bd2; opacity: 0.5; }

/* Progress bar */
.progress-bar {
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar .fill {
  height: 100%;
  background: #268bd2;
  transition: width 0.1s;
  border-radius: 2px;
}

/* ---- Responsive ---- */
@media (max-width: 800px) {
  .demo-body {
    grid-template-columns: 1fr;
  }
  .gen-panel {
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
    max-height: 400px;
  }
  .kv-panel {
    min-height: 300px;
  }
}
</style>
</head>
<body>

<div class="memento-demo" id="mementoDemo">
  <div class="demo-header">
    <h3>Memento Generation &mdash; Qwen3-32B on PROBLEM_SOURCE_PLACEHOLDER</h3>
    <div class="demo-controls">
      <button id="btnPlay" onclick="togglePlay()">&#9654; Play</button>
      <button id="btnStep" class="secondary" onclick="stepForward()">Step &rarr;</button>
      <button id="btnReset" class="secondary" onclick="resetDemo()">Reset</button>
      <div class="speed-control">
        <label>Speed</label>
        <input type="range" id="speedSlider" min="1" max="50" value="15">
      </div>
    </div>
  </div>
  <div class="progress-bar"><div class="fill" id="progressFill"></div></div>
  <div class="demo-body">
    <div class="gen-panel" id="genPanel">
      <div class="problem-text">
        <strong>Problem (PROBLEM_SOURCE_PLACEHOLDER)</strong><br>
        PROBLEM_TEXT_PLACEHOLDER
      </div>
    </div>
    <div class="kv-panel">
      <h4>KV Cache During Generation</h4>
      <div class="kv-chart-container">
        <canvas id="kvCanvas"></canvas>
      </div>
      <div class="kv-legend">
        <span class="leg-memento">Memento</span>
        <span class="leg-vanilla">Vanilla (no masking)</span>
      </div>
      <div class="kv-stats">
        <div class="kv-stat">
          <div class="stat-label">Current KV</div>
          <div class="stat-value memento" id="statCurrentKV">0</div>
        </div>
        <div class="kv-stat">
          <div class="stat-label">Peak KV</div>
          <div class="stat-value memento" id="statPeakKV">0</div>
        </div>
        <div class="kv-stat">
          <div class="stat-label">Vanilla KV</div>
          <div class="stat-value vanilla" id="statVanillaKV">0</div>
        </div>
        <div class="kv-stat">
          <div class="stat-label">Reduction</div>
          <div class="stat-value" id="statReduction">&mdash;</div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ================================================================
// DATA — parsed from Qwen3-32B PROBLEM_SOURCE_PLACEHOLDER
// Correct answer: ANSWER_PLACEHOLDER
// ================================================================
SEGMENTS_PLACEHOLDER

// Prompt tokens (approximate)
const PROMPT_TOKENS = 80;

// ================================================================
// ANIMATION STATE
// ================================================================
let state = {
  segIdx: 0,
  charIdx: 0,
  playing: false,
  timer: null,
  kvHistory: [],
  totalTokens: 0,
  currentKV: PROMPT_TOKENS,
  peakKV: PROMPT_TOKENS,
  maskedBlocks: new Set(),
  maskedTokens: 0,
  elements: [],
};

// ================================================================
// INIT
// ================================================================
function init() {
  const panel = document.getElementById('genPanel');
  state.elements = [];

  SEGMENTS.forEach((seg, i) => {
    const div = document.createElement('div');
    div.className = `gen-segment ${seg.type}`;
    div.style.display = 'none';

    const label = document.createElement('span');
    label.className = 'seg-label';
    if (seg.type === 'block') label.textContent = `Thinking Block ${seg.idx}`;
    else if (seg.type === 'summary') label.textContent = `Memento ${seg.idx}`;
    else label.textContent = 'Final Answer';
    div.appendChild(label);

    const content = document.createElement('span');
    content.className = 'seg-content';
    div.appendChild(content);

    panel.appendChild(div);
    state.elements.push({ div, content, seg });
  });

  state.kvHistory = [{tokensSoFar: 0, kvTokens: PROMPT_TOKENS, vanillaTokens: PROMPT_TOKENS}];
  drawChart();
  updateStats();
}

// ================================================================
// ANIMATION TICK
// ================================================================
function tick() {
  if (state.segIdx >= SEGMENTS.length) {
    stopPlay();
    return;
  }

  const speed = parseInt(document.getElementById('speedSlider').value);
  const charsPerTick = speed * 3;

  const seg = SEGMENTS[state.segIdx];
  const el = state.elements[state.segIdx];

  if (state.charIdx === 0) {
    el.div.style.display = 'block';
    el.div.classList.add('active');
    el.div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  state.charIdx = Math.min(state.charIdx + charsPerTick, seg.text.length);
  const revealed = seg.text.substring(0, state.charIdx);
  el.content.textContent = revealed;

  if (state.charIdx < seg.text.length) {
    const cursor = document.createElement('span');
    cursor.className = 'cursor';
    el.content.appendChild(cursor);
  }

  const tokensRevealed = Math.round((state.charIdx / seg.text.length) * seg.tokens);
  const totalTokensSoFar = PROMPT_TOKENS + SEGMENTS.slice(0, state.segIdx).reduce((s, x) => s + x.tokens, 0) + tokensRevealed;

  let mementoKV = PROMPT_TOKENS + tokensRevealed;
  for (let i = 0; i < state.segIdx; i++) {
    if (SEGMENTS[i].type === 'summary') {
      mementoKV += SEGMENTS[i].tokens;
    } else if (SEGMENTS[i].type === 'block' && !state.maskedBlocks.has(SEGMENTS[i].idx)) {
      mementoKV += SEGMENTS[i].tokens;
    } else if (SEGMENTS[i].type === 'answer') {
      mementoKV += SEGMENTS[i].tokens;
    }
  }

  state.currentKV = mementoKV;
  state.peakKV = Math.max(state.peakKV, mementoKV);
  state.totalTokens = totalTokensSoFar;

  const vanillaKV = totalTokensSoFar;

  state.kvHistory.push({
    tokensSoFar: totalTokensSoFar,
    kvTokens: mementoKV,
    vanillaTokens: vanillaKV
  });

  drawChart();
  updateStats();
  updateProgress();

  if (state.charIdx >= seg.text.length) {
    el.div.classList.remove('active');

    if (seg.type === 'summary') {
      state.maskedBlocks.add(seg.idx);
      for (let i = 0; i < state.segIdx; i++) {
        if (SEGMENTS[i].type === 'block' && SEGMENTS[i].idx === seg.idx) {
          state.elements[i].div.classList.add('masked');
          const blockTokens = SEGMENTS[i].tokens;
          state.currentKV -= blockTokens;
          state.kvHistory.push({
            tokensSoFar: totalTokensSoFar + 1,
            kvTokens: state.currentKV,
            vanillaTokens: vanillaKV
          });
          drawChart();
          updateStats();
          break;
        }
      }
    }

    state.segIdx++;
    state.charIdx = 0;
  }
}

// ================================================================
// PLAY/PAUSE/STEP/RESET
// ================================================================
function togglePlay() {
  if (state.playing) {
    stopPlay();
  } else {
    state.playing = true;
    document.getElementById('btnPlay').textContent = '\u23F8 Pause';
    state.timer = setInterval(tick, 40);
  }
}

function stopPlay() {
  state.playing = false;
  document.getElementById('btnPlay').textContent = '\u25B6 Play';
  if (state.timer) { clearInterval(state.timer); state.timer = null; }
}

function stepForward() {
  stopPlay();
  if (state.segIdx >= SEGMENTS.length) return;
  const seg = SEGMENTS[state.segIdx];
  state.charIdx = seg.text.length;
  tick();
}

function resetDemo() {
  stopPlay();
  state.segIdx = 0;
  state.charIdx = 0;
  state.kvHistory = [{tokensSoFar: 0, kvTokens: PROMPT_TOKENS, vanillaTokens: PROMPT_TOKENS}];
  state.currentKV = PROMPT_TOKENS;
  state.peakKV = PROMPT_TOKENS;
  state.maskedBlocks = new Set();
  state.maskedTokens = 0;
  state.totalTokens = 0;

  state.elements.forEach(el => el.div.remove());
  state.elements = [];
  init();
}

// ================================================================
// KV CHART (Canvas)
// ================================================================
function drawChart() {
  const canvas = document.getElementById('kvCanvas');
  const ctx = canvas.getContext('2d');
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  const W = rect.width;
  const H = rect.height;
  const pad = {top: 10, right: 15, bottom: 36, left: 48};
  const cw = W - pad.left - pad.right;
  const ch = H - pad.top - pad.bottom;

  ctx.clearRect(0, 0, W, H);

  const totalMax = PROMPT_TOKENS + SEGMENTS.reduce((s, x) => s + x.tokens, 0);
  const kvMax = totalMax * 1.05;

  // Axes
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, pad.top + ch);
  ctx.lineTo(pad.left + cw, pad.top + ch);
  ctx.stroke();

  // Grid
  ctx.strokeStyle = '#f0f0f0';
  for (let i = 1; i <= 4; i++) {
    const y = pad.top + ch - (ch * i / 4);
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + cw, y);
    ctx.stroke();
  }

  // Y labels
  ctx.fillStyle = '#999';
  ctx.font = '10px Source Sans 3, sans-serif';
  ctx.textAlign = 'right';
  for (let i = 0; i <= 4; i++) {
    const val = Math.round(kvMax * i / 4);
    const y = pad.top + ch - (ch * i / 4);
    ctx.fillText(val.toLocaleString(), pad.left - 6, y + 3);
  }

  // X label
  ctx.fillStyle = '#999';
  ctx.font = '10px Source Sans 3, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Tokens generated', pad.left + cw / 2, H - 4);

  // Y label
  ctx.save();
  ctx.translate(12, pad.top + ch / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('KV cache (tokens)', 0, 0);
  ctx.restore();

  if (state.kvHistory.length < 2) return;

  function toX(tok) { return pad.left + (tok / totalMax) * cw; }
  function toY(kv) { return pad.top + ch - (kv / kvMax) * ch; }

  // Vanilla line (das
```


## File: blogpost/figures/build_animation_v2.py

```
#!/usr/bin/env python3
"""Generate animation.html with multi-example support (Math/Code/Science)."""
import json

def escape_js_backtick(text):
    """Escape text for JS template literal (backtick)."""
    text = text.replace("\\", "\\\\")   # \ -> \\
    text = text.replace("`", "\\`")     # ` -> \`
    # Escape ${ to prevent template literal interpolation
    text = text.replace("${", "\\${")
    return text

def build_example_js(data):
    """Build JS object literal for one example."""
    problem = escape_js_backtick(data["problem"])
    source = data.get("problem_source", "")
    answer = escape_js_backtick(str(data.get("answer", "")))
    
    seg_lines = []
    for seg in data["segments"]:
        t = seg["type"]
        idx = seg["block_idx"]
        tokens = seg["approx_tokens"]
        text = escape_js_backtick(seg["text"])
        seg_lines.append(f'      {{type:"{t}", idx:{idx}, text:`{text}`, tokens:{tokens}}}')
    
    segs_str = ",\n".join(seg_lines)
    
    return f"""{{
    source: `{source}`,
    problem: `{problem}`,
    answer: `{answer}`,
    segments: [\n{segs_str}\n    ]
  }}"""

# Load all 3 examples
examples = {}
for fname, key in [("example_response.json", "math"), 
                    ("example_code.json", "code"), 
                    ("example_science.json", "science")]:
    with open(fname) as f:
        examples[key] = json.load(f)

# Build the EXAMPLES JS object
example_entries = []
for key, data in examples.items():
    example_entries.append(f"  {key}: {build_example_js(data)}")
examples_js = "const EXAMPLES = {\n" + ",\n".join(example_entries) + "\n};"

# Read existing animation.html
with open("animation.html") as f:
    html = f.read()

# 1. Replace the SEGMENTS declaration with EXAMPLES + active tracking
old_seg_start = html.find("const SEGMENTS = [")
old_seg_end = html.find("];\n", old_seg_start)
# Find the end of the SEGMENTS array (the ];)
# We need to find the closing ]; that ends the array
import re
# Find from old_seg_start to the next line that is just "];""
pos = old_seg_start
depth = 0
i = pos
while i < len(html):
    if html[i] == '[':
        depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0:
            old_seg_end = i + 2  # include ];\n
            break
    i += 1

# Also remove the comment lines before SEGMENTS
comment_start = html.rfind("// ===", 0, old_seg_start)
if comment_start > 0:
    # Go back to find all comment lines
    line_start = html.rfind("\n", 0, comment_start) + 1
    old_seg_start = line_start

old_segment_block = html[old_seg_start:old_seg_end]

new_segment_block = f"""{examples_js}

let currentExample = 'math';
let SEGMENTS = EXAMPLES.math.segments;"""

html = html[:old_seg_start] + new_segment_block + html[old_seg_end:]

# 2. Add tab buttons in the header (after the h3)
old_header_h3 = '<h3>Memento Generation &mdash; Qwen3-32B on AIME 2025 Problem 5</h3>'
new_header = """<h3 id="demoTitle">Memento Generation &mdash; Qwen3-32B</h3>
    <div class="example-tabs">
      <button class="tab active" data-key="math" onclick="switchExample('math')">Math</button>
      <button class="tab" data-key="code" onclick="switchExample('code')">Code</button>
      <button class="tab" data-key="science" onclick="switchExample('science')">Science</button>
    </div>"""
html = html.replace(old_header_h3, new_header)

# 3. Update problem text to use an ID
old_problem = """<div class="problem-text">
        <strong>Problem (AIME 2025 Problem 5)</strong><br>
        An isosceles trapezoid has an inscribed circle tangent to each of its four sides. The radius of the circle is 3, and the area of the trapezoid is 72. Let the parallel sides of the trapezoid have lengths r and s, with r \u2260 s. Find r\u00b2 + s\u00b2.
      </div>"""
new_problem = """<div class="problem-text" id="problemText">
        <strong id="problemSource">Problem (AIME 2025 Problem 5)</strong><br>
        <span id="problemBody">An isosceles trapezoid has an inscribed circle tangent to each of its four sides. The radius of the circle is 3, and the area of the trapezoid is 72. Let the parallel sides of the trapezoid have lengths r and s, with r \u2260 s. Find r\u00b2 + s\u00b2.</span>
      </div>"""
html = html.replace(old_problem, new_problem)

# 4. Add tab CSS before the closing </style>
tab_css = """
/* ---- Example tabs ---- */
.example-tabs {
  display: flex;
  gap: 4px;
}

.example-tabs .tab {
  background: #fff;
  color: #268bd2;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 4px 12px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.example-tabs .tab:hover {
  background: #d6eaf8;
}

.example-tabs .tab.active {
  background: #268bd2;
  color: #fff;
  border-color: #268bd2;
}
"""
html = html.replace("</style>", tab_css + "</style>")

# 5. Add switchExample function before the BOOT section
switch_fn = """
// ================================================================
// EXAMPLE SWITCHING
// ================================================================
function switchExample(key) {
  if (key === currentExample && !state.finished && state.segIdx === 0) return;
  
  // Update active tab
  document.querySelectorAll('.example-tabs .tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.key === key);
  });
  
  currentExample = key;
  SEGMENTS = EXAMPLES[key].segments;
  
  // Update problem text
  document.getElementById('problemSource').textContent = 'Problem (' + EXAMPLES[key].source + ')';
  document.getElementById('problemBody').textContent = EXAMPLES[key].problem;
  
  // Reset animation
  resetDemo();
}
"""

boot_marker = "// ================================================================\n// BOOT"
html = html.replace(boot_marker, switch_fn + boot_marker)

with open("animation.html", "w") as f:
    f.write(html)

print(f"Wrote animation.html ({len(html)} chars)")
print(f"  Math segments: {len(examples['math']['segments'])}")
print(f"  Code segments: {len(examples['code']['segments'])}")
print(f"  Science segments: {len(examples['science']['segments'])}")

```


## File: blogpost/figures/example_code.json

```
{
  "problem": "You have an empty sequence A. There are Q queries given, and you need to process them in the order they are given.\nThe queries are of the following two types:\n\n- 1 x: Append x to the end of A.\n- 2 k: Find the k-th value from the end of A. It is guaranteed that the length of A is at least k when this query is given.\n\nInput\n\nThe input is given from Standard Input in the following format:\nQ\n\\mathrm{query}_1\n\\mathrm{query}_2\n\\vdots\n\\mathrm{query}_Q\n\nEach query is in one of the following two formats:\n1 x\n\n2 k\n\nOutput\n\nPrint q lines, where q is the number of queries of the second type.\nThe i-th line should contain the answer to the i-th such query.\n\nConstraints\n\n\n- 1 \\leq Q \\leq 100\n- In the first type of query, x is an integer satisfying 1 \\leq x \\leq 10^9.\n- In the second type of query, k is a positive integer not greater than the current length of sequence A.\n\nSample Input 1\n\n5\n1 20\n1 30\n2 1\n1 40\n2 3\n\nSample Output 1\n\n30\n20\n\n\n- Initially, A is empty.\n- The first query appends 20 to the end of A, making A=(20).\n- The second query appends 30 to the end of A, making A=(20,30).\n- The answer to the third query is 30, which is the 1-st value from the end of A=(20,30).\n- The fourth query appends 40 to the end of A, making A=(20,30,40).\n- The answer to the fifth query is 20, which is the 3-rd value from the end of A=(20,30,40).",
  "problem_source": "LiveCodeBench v6",
  "label": "Code",
  "answer": "Q = int(input())\nA = []\nfor _ in range(Q):\n    parts = input().split()\n    if parts[0] == '1':\n        x = int(parts[1])\n        A.append(x)\n    else:\n        k = int(parts[1])\n        print(A[-k])",
  "segments": [
    {
      "type": "block",
      "block_idx": 1,
      "text": "Okay, let's see. I need to solve this problem where there's a sequence A and I have to process some queries. The queries can be either appending a number to the end or finding the k-th element from the end. Hmm. So first, I should think about how to handle these operations efficiently. Wait, the problem says for the second type query, the answer is the k-th from the end. Oh right, like if the array is [20, 30, 40], then the 3rd from the end is 20. Because the end is the last element, so first is 40, second is 30, third is 20. Oh right, so for the query 2 3 in the sample, that's why the answer is 20. So the straightforward approach would be, whenever we have a query of type 2, we can just access the array from the end. But in Python, lists are easy to handle. Let's think about using a list. For each type 1, append x to the list. For type 2, the k-th from the end is the element at position len(A)-k. Wait yes. Because the list's end is the last element, so the first from end is index -1, second -2, etc. So the k-th from the end would be at index -k. But in Python, negative indices are allowed, right? Like if the list has 3 elements, then A[-1] is last, -2 second, etc. So for k=3, A[-3] would be the third from end. But I have to make sure that the length is sufficient, but the problem says that the queries are valid, so no need to check. Wait the problem states that in the second type query, k is not greater than the current length, so we don't have to worry about invalid k. So the steps are:\nInitialize a list A. Then process each query:\nFor a type 1, append x to A. For a type 2, get the k-th from end, which is A[-k], and output that. Wait that's simple. Let me test with the sample input. Sample Input 1: 5 The first two queries make A as [20, 30].\nThird query is 2 1 \u2192 A[-1] is 30 \u2192 correct.\nFourth appends 40 \u2192 A is [20,30,40].\nFifth is 2 3 \u2192 A[-3] is 20 \u2192 correct. Yes, so that works. So the code can be straightforward.",
      "char_len": 1948,
      "approx_tokens": 487
    },
    {
      "type": "summary",
      "block_idx": 1,
      "text": "Chooses Python list A; invariant: A stores elements in arrival order; for type2 query with 1<=k<=len(A), k-th from end = A[-k] (negative indices). Operations: type1 -> A.append(x); type2 -> output A[-k]. Validity: queries ensure k within bounds so no checks. Sample validation: after appends [20,30]; query(2,1)->A[-1]=30; after append40 => [20,30,40]; query(2,3)->A[-3]=20.",
      "char_len": 374,
      "approx_tokens": 93
    },
    {
      "type": "block",
      "block_idx": 2,
      "text": "Now, how to code this. First, read Q. Then process each query line by line. Wait, in Python, the first line is Q, then Q lines follow. Each line is either starting with 1 or 2. So, for each line after the first, split the line into parts. For example, for a line like \"1 20\", split into list gives ['1', '20'], so the first element is the type, second is x. For type 2, it's like \"2 1\", so split into ['2','1'], and k is the second element. So, code steps: Initialize A as empty list. Read Q. Then loop Q times:\nRead each query line. Split into parts. Depending on the first part being '1' or '2'. For type 1: append int(x) to A.\nFor type 2: take the second part, convert to int k, then output A[-k] Wait, yes. Wait the output for type2 queries must be printed as separate lines for each such query. So collect all outputs and print each in order. So, perhaps, in code:\nWe can just process each query as we read them, and whenever it's a type2, immediately print the result, since the order is sequential. Wait yes, because the queries are to be processed in order, and each type2's answer must be printed in the order they appear. So code outline: import sys A = [] Q = int(input())\nfor _ in range(Q):\n```python\nquery = input().split()\n\nif query[0] == '1':\n\n    x = int(query[1])\n\n    A.append(x)\n``` else:\nk = int(query[1])\nprint(A[-k]) Wait, that's all?",
      "char_len": 1356,
      "approx_tokens": 339
    },
    {
      "type": "summary",
      "block_idx": 2,
      "text": "Implements Python algorithm: read Q, init A=[], iterate Q times reading each query via input().split(). For type '1', parse x=int(query[1]) and append to A; for type '2', parse k=int(query[1]) and print A[-k]. Confirms printing each result immediately in encounter order satisfies requirements.",
      "char_len": 294,
      "approx_tokens": 73
    },
    {
      "type": "block",
      "block_idx": 3,
      "text": "Yes, that seems to handle it. Let me test the sample input. Sample Input 1: 5 The first query is \"1 20\" \u2192 append 20 \u2192 A is [20]\nSecond query \"1 30\" \u2192 append \u2192 [20,30]\nThird query \"2 1\" \u2192 print A[-1] \u2192 30. Correct.\nFourth query \"1 40\" \u2192 append \u2192 [20, 30,40]\nFifth query \"2 3\" \u2192 A[-3] is 20, correct. So yes, the code would output 30 and 20 as required. Wait, but what if the list is empty? But the problem states that for type 2 queries, the k is valid. So no problem. Hmm, what about when the list has exactly k elements? Like, if k is 1, then A[-1] is the last element, which is correct. Yes. So this code should work. Let me think about possible edge cases. Another test case: Suppose Q=1 and the query is type 2 with k=1, but the list must have at least 1 element. So the input would be:\n1 2 1 But the first line is Q=1, but then there's only one query which is type 2. Wait, but that's impossible, because the first query can't be type 2 if the list is empty. So the problem's input ensures that all queries are valid. So the code can proceed without error handling. Another test case: Suppose multiple appends and queries. Let's see. Suppose input: 3 1 5 2 1 2 2 Then output would be 5 and then 5? Wait after first append, the list has [5].\nThe second query is type 2, k=1 \u2192 5. The third query is type 2, k=2? Wait no, because the length is 1. So that's an invalid input, but problem says it is valid. So in this case, the third query can't be 2 2. Thus, the code can proceed as the problem ensures validity. So the code is correct.",
      "char_len": 1537,
      "approx_tokens": 384
    },
    {
      "type": "summary",
      "block_idx": 3,
      "text": "Manual simulation on sample and selected edge cases confirms Python logic: maintain list A; for type 1 x do A.append(x); for type 2 k do print(A[-k]). Sample trace: start A=[]; q1 \"1 20\" -> A=[20]; q2 \"1 30\" -> A=[20,30]; q3 \"2 1\" -> print A[-1]=30; q4 \"1 40\" -> A=[20,30,40]; q5 \"2 3\" -> print A[-3]=20; matches sample output \"30\" and \"20\". Relies on problem guarantee that for type-2 queries 1 <= k <= len(A), so no need for empty-list or out-of-range checks. Edge-case reasoning: considers Q=1 with only type 2 (impossible due to validity guarantee); considers multiple appends/queries, e.g., input \"3; 1 5; 2 1; 2 2\", notes that query \"2 2\" would be invalid if len(A)=1, but such inputs are excluded by the guarantee, so no additional error handling is required.",
      "char_len": 766,
      "approx_tokens": 191
    },
    {
      "type": "block",
      "block_idx": 4,
      "text": "Therefore the code is as written above. Wait, but in Python, when you split the input, the elements are split by any whitespace, so even if the numbers have leading zeros or whatever, but the problem states that x is an integer, so the code is okay. Therefore, the code is straightforward. Let me write it properly. Wait, the code should read Q first. So, first read Q with input(). Then loop Q times, each time read the next line, split into parts, etc. Yes. So the code would be:\n```python\nQ = int(input())\nA = []\nfor _ in range(Q):\n    parts = input().split()\n    if parts[0] == '1':\n        x = int(parts[1])\n        A.append(x)\n    else:\n        k = int(parts[1])\n        print(A[-k])\n``` That's all. That should work. Let me check the sample input again. Sample Input 1 gives 5 queries. The fifth query is 2 3 \u2192 the array is [20,30,40], so A[-3] is 20. Yes. Correct.\nAnother test case: Let me imagine a case where after several appends, the query is 2 with k= len(A). For example, after appending 3 elements, querying 3 would give the first element (since it's third from end). Yes, that's correct. So this code should handle all cases correctly. I think that's the solution.",
      "char_len": 1181,
      "approx_tokens": 295
    },
    {
      "type": "summary",
      "block_idx": 4,
      "text": "Finalizes code structure explicitly: Q=int(input()); A=[]; loop Q times reading parts=input().split(); if parts[0]=='1' then x=int(parts[1]); A.append(x); else k=int(parts[1]); print(A[-k]); asserts readiness for all valid inputs.",
      "char_len": 230,
      "approx_tokens": 57
    },
    {
      "type": "answer",
      "block_idx": 0,
      "text": "```python\nQ = int(input())\nA = []\nfor _ in range(Q):\n    parts = input().split()\n    if parts[0] == '1':\n        x = int(parts[1])\n        A.append(x)\n    else:\n        k = int(parts[1])\n        print(A[-k])\n```",
      "char_len": 211,
      "approx_tokens": 52
    }
  ]
}
```


## File: blogpost/figures/example_response.json

```
{
  "problem": "An isosceles trapezoid has an inscribed circle tangent to each of its four sides. The radius of the circle is 3, and the area of the trapezoid is 72. Let the parallel sides of the trapezoid have lengths r and s, with r \u2260 s. Find r\u00b2 + s\u00b2.",
  "problem_source": "AIME 2025 Problem 5",
  "answer": "504",
  "segments": [
    {
      "type": "block",
      "block_idx": 1,
      "text": "Okay, so I need to find \\( r^2 + s^2 \\) for an isosceles trapezoid that has an inscribed circle. The radius of the circle is 3, and the area of the trapezoid is 72. The trapezoid has parallel sides of lengths \\( r \\) and \\( s \\), which are not equal. First, I remember that not all trapezoids can have an inscribed circle (a circle tangent to all four sides). For a trapezoid to have an inscribed circle, it must be tangential, meaning it has an incircle. I think the condition for a trapezoid to be tangential is that the sum of the lengths of the two bases must equal the sum of the lengths of the two legs. Since it's an isosceles trapezoid, the legs are equal in length. Let me write down what I know:\n- The radius of the inscribed circle is 3. Therefore, the diameter is 6, which might relate to the height? Wait, yes, in a trapezoid with an incircle, the height is equal to twice the radius? Wait, actually, the radius is the distance from the center of the circle to the sides, so the height of the trapezoid should be twice the radius. Let me confirm that. The height (altitude) of the trapezoid is the distance between the two bases, which should be equal to twice the radius because the diameter would span the circle perpendicular to the bases. So, if the radius is 3, the height is \\( 2 \\times 3 = 6 \\). That seems right. The area of the trapezoid is given by the formula: $$\n$$\n\\text{Area} = \\frac{(r + s)}{2} \\times h $$\n$$\nPlugging in the known values: $$\n$$\n72 = \\frac{(r + s)}{2} \\times 6 $$\n$$\nLet me solve for \\( r + s \\):\nMultiply both sides by 2: $$\n$$\n144 = (r + s) \\times 6 $$\n$$\nDivide both sides by 6: $$\n$$\nr + s = 24 $$\n$$\nOkay, so the sum of the two bases is 24. Now, since the trapezoid is isosceles and tangential, the sum of the bases equals the sum of the legs. Let me denote each of the non-parallel sides (the legs) as \\( l \\).\nSince it's isosceles, both legs are equal, so the sum of the legs is \\( 2l \\).\nTherefore, the condition for a tangential trapezoid is: $$\n$$\nr + s = 2l $$\n$$\nSo, from this, \\( 2l = 24 \\implies l = 12 \\). Each leg is 12 units long.",
      "char_len": 2092,
      "approx_tokens": 523
    },
    {
      "type": "summary",
      "block_idx": 1,
      "text": "Let r,s be unequal parallel sides; trapezoid is isosceles and tangential (incircle) so r+s = sum of legs. Radius=3 => height h=2*3=6. Area formula: 72=((r+s)/2)*6 => r+s=24. Legs both l satisfy r+s=2l=24 => l=12.",
      "char_len": 212,
      "approx_tokens": 53
    },
    {
      "type": "block",
      "block_idx": 2,
      "text": "Now, how can I find \\( r \\) and \\( s \\) individually? The problem asks for \\( r^2 + s^2 \\). I know that if I can find \\( r \\) and \\( s \\), then I can compute this. Since I have \\( r + s = 24 \\), maybe I can find another equation involving \\( r \\) and \\( s \\). Let me think. In an isosceles trapezoid, the legs are equal, and the non-parallel sides are congruent. Also, the height is perpendicular to the bases. Let me try to draw the trapezoid and see if I can find a relationship using the height and the legs. If I consider the trapezoid with bases of lengths \\( r \\) and \\( s \\), the difference in their lengths is \\( |r - s| \\). When you have an isosceles trapezoid, the legs form the sides, and the projection of each leg onto the base is \\( \\frac{|r - s|}{2} \\). So, each leg forms the hypotenuse of a right triangle with height \\( h = 6 \\) and base \\( \\frac{|r - s|}{2} \\).\nSince the legs are 12, by the Pythagorean theorem:\n$$\n\\left( \\frac{|r - s|}{2} \\right)^2 + 6^2 = 12^2 \\\\\n\\left( \\frac{|r - s|}{2} \\right)^2 + 36 = 144 \\\\\n\\left( \\frac{|r - s|}{2} \\right)^2 = 144 - 36 = 108 \\\\\n$$\nTherefore, \\( \\frac{|r - s|}{2} = \\sqrt{108} = \\sqrt{36 \\times 3} = 6 \\sqrt{3} \\)\nHence, \\( |r - s| = 12 \\sqrt{3} \\)\nSo, the difference between the two bases is \\( 12 \\sqrt{3} \\).",
      "char_len": 1272,
      "approx_tokens": 318
    },
    {
      "type": "summary",
      "block_idx": 2,
      "text": "Use isosceles trapezoid geometry: each leg (length 12) is hypotenuse of right triangle with height 6 and horizontal leg (r-s)/2 (assume r>s). Equation: ((r-s)/2)^2+6^2=12^2 => ((r-s)/2)^2=108 => |r-s|=12*sqrt(3).",
      "char_len": 212,
      "approx_tokens": 53
    },
    {
      "type": "block",
      "block_idx": 3,
      "text": "But we also know that \\( r + s = 24 \\). So, we have two equations:\n1. \\( r + s = 24 \\) 2. \\( |r - s| = 12\\sqrt{3} \\)\nAssuming, without loss of generality, that \\( r > s \\), so \\( r - s = 12\\sqrt{3} \\). Now, let me solve these two equations:\nLet me write them again:\n\\( r + s = 24 \\)\n\\( r - s = 12\\sqrt{3} \\) Adding both equations:\n\\( 2r = 24 + 12\\sqrt{3} \\) \u21d2 \\( r = 12 + 6\\sqrt{3} \\) Subtracting the second equation from the first:\n\\( 2s = 24 - 12\\sqrt{3} \\) \u21d2 \\( s = 12 - 6\\sqrt{3} \\)\nTherefore, the two bases are \\( 12 + 6\\sqrt{3} \\) and \\( 12 - 6\\sqrt{3} \\).\nNow, the problem asks for \\( r^2 + s^2 \\). Let me compute that. First, compute \\( r^2 + s^2 \\):\n\\( r^2 + s^2 = (12 + 6\\sqrt{3})^2 + (12 - 6\\sqrt{3})^2 \\)\nLet me compute each term separately. First term: \\( (12 + 6\\sqrt{3})^2 \\)\n= \\( 12^2 + 2*12*6\\sqrt{3} + (6\\sqrt{3})^2 \\)\n= \\( 144 + 144\\sqrt{3} + 36*3 \\)\n= \\( 144 + 144\\sqrt{3} + 108 \\)\n= \\( 252 + 144\\sqrt{3} \\)\nSecond term: \\( (12 - 6\\sqrt{3})^2 \\)\n= \\( 12^2 - 2*12*6\\sqrt{3} + (6\\sqrt{3})^2 \\)\n= \\( 144 - 144\\sqrt{3} + 108 \\)\n= \\( 252 - 144\\sqrt{3} \\)\nAdding both terms together:\n\\( (252 + 144\\sqrt{3}) + (252 - 144\\sqrt{3}) = 252 + 252 = 504 \\)\nTherefore, \\( r^2 + s^2 = 504 \\).",
      "char_len": 1197,
      "approx_tokens": 299
    },
    {
      "type": "summary",
      "block_idx": 3,
      "text": "With r+s=24 and r-s=12*sqrt(3) (assume r>s): r=12+6*sqrt(3), s=12-6*sqrt(3). Compute r^2=252+144*sqrt(3), s^2=252-144*sqrt(3) => r^2+s^2=504.",
      "char_len": 141,
      "approx_tokens": 35
    },
    {
      "type": "block",
      "block_idx": 4,
      "text": "Hmm, so the answer is 504? Let me just check my steps again to make sure I didn't make a mistake. First, area calculation: area = (r + s)/2 * h = 72. Since h = 6, then (r + s) must be 24. That seems okay.\nThen, since the trapezoid is tangential, the sum of the bases equals the sum of the legs. Since it's isosceles, both legs are equal, so each is 12. Therefore, 2 legs sum to 24, so that works with r + s =24. Then, using the legs as hypotenuse of a right triangle with height 6 and base difference/2. The difference of the bases is 12\u221a3, so (12\u221a3)/2 = 6\u221a3. Then, the Pythagorean theorem:\n(6\u221a3)^2 + 6^2 = (leg)^2 ?\nWait, 6\u221a3 squared is 36*3 = 108, plus 36 is 144, which is 12^2. That checks out. So that's correct.\nTherefore, r and s are 12 \u00b1 6\u221a3, and their squares add to 504. Hmm, that seems straightforward. Let me just confirm the calculation of r\u00b2 + s\u00b2 again. Alternatively, maybe there's a smarter way to compute r\u00b2 + s\u00b2 without having to find r and s individually? We know that:\n(r + s)^2 = r\u00b2 + 2rs + s\u00b2\n(r - s)^2 = r\u00b2 - 2rs + s\u00b2\nTherefore, (r + s)^2 + (r - s)^2 = 2(r\u00b2 + s\u00b2) Therefore,\nr\u00b2 + s\u00b2 = [(r + s)^2 + (r - s)^2]/2 We already know r + s =24 and r - s =12\u221a3, so:\n[(24)^2 + (12\u221a3)^2]/2 = [576 + 144*3]/2 = [576 + 432]/2 = 1008/2 = 504 Same result. So that's correct. Therefore, the answer should be 504. Let me see if there's any possible mistake here. Wait, maybe the height is not 6? Let me think again. The radius is 3. Is the diameter equal to the height? In a tangential quadrilateral, the inradius is equal to the area divided by the semiperimeter. Wait, maybe I oversimplified. Hold on, maybe I made an error in assuming the height is twice the radius. Let me recall the correct relation. In any tangential quadrilateral, the area is equal to the inradius multiplied by the semiperimeter. Wait, let me check that formula again. Wait, actually, for a tangential quadrilateral, the area (K) is equal to the inradius (r) multiplied by the semiperimeter (s). Wait, no, is that right? Wait, let me confirm:\nYes, for a tangential quadrilateral, the area is \\( K = r \\times s \\), where \\( s \\) is the semiperimeter. Wait, semiperimeter? Wait, that might have been my mistake. Let me check again. Wait, actually, in a tangential polygon, the area is equal to the inradius multiplied by the semiperimeter. Wait, for a circle tangent to all sides, the formula for the area is indeed \\( K = r \\times \\frac{a + b + c + d}{2} \\), where a,b,c,d are the sides. Wait, so that's semiperimeter times radius. Wait, that seems conflicting with my previous thought. Let me check with a square: if a square with side length \\( a \\), inradius is \\( a/2 \\), semiperimeter is \\( 2a \\), so area would be \\( (a/2)*(2a) = a\u00b2 \\), which is correct. So that formula holds.\nTherefore, in this problem, the area is 72, the inradius is 3, so the semiperimeter is \\( 72 / 3 = 24 \\). Therefore, the semiperimeter is 24. The semiperimeter is half the sum of all sides. Therefore, the sum of all sides is 48. Wait, but earlier, I thought that the sum of the bases is 24, but that might be incorrect. Wait, let me redo this part. Let me start over with the correct formulas. Given an isosceles trapezoid with inradius 3, so the area is \\( K = r \\times N \\), where N is the semiperimeter. Wait, actually, hold on, the formula is \\( K = r \\times \\sigma \\), where \\( \\sigma \\) is the semiperimeter. Wait, so:\n\\( K = r \\times \\frac{a + b + c + d}{2} \\). Wait, actually, no, semiperimeter is half the perimeter, so:\n\\( K = r \\times \\text{semiperimeter} \\). Therefore,\n\\( 72 = 3 \\times \\frac{ (r + s + 2l) }{2} \\)\nMultiply both sides by 2:\n\\( 144 = 3 \\times (r + s + 2l) \\) Divide both sides by 3:\n\\( 48 = r + s + 2l \\)\nTherefore, the sum of the two bases (r + s) plus twice the leg length equals 48.\nBut we also know that in a tangential trapezoid, the sum of the bases equals the sum of the legs. Since it's isosceles, the legs are equal, so:\n\\( r + s = 2l \\) Therefore, substituting into the previous equation, \\( (2l) + 2l = 48 \\) So,\n\\( 4l = 48 \\implies l = 12 \\)\nTherefore, legs are 12 each, so sum of the bases \\( r + s = 24 \\), which matches the previous result. So that is okay. Therefore, the height can be found via area:\nArea = (r + s)/2 * h = 24/2 * h = 12 h = 72 \u21d2 h = 6. So that's correct. So height is indeed 6. So my initial thought was okay. The inradius is 3, but the height is twice that? Wait, but in a tangential quadrilateral, is there a direct relation between inradius and height? In a trapezoid, the inradius (if exists) must satisfy certain conditions. Since the circle is tangent to both bases, the distance between the bases is the height, which is equal to 2r? Wait, here the inradius is 3, so height would be 6, so that is correct. So in a trapezoid with an incircle, the height is twice the inradius? Let me see. Wait, actually, in a trapezoid with an incircle, the inradius is equal to the area divided by the semiperimeter. But in the case of a trapezoid, the area is also (a + b)/2 * h. So if we have the inradius, then r = (Area)/semiperimeter. But in this case, we were given the inradius and the area, so that led us to the semiperimeter being 24. But the height is indeed 6 here, so that's twice the radius. Hmm, so in this case, the height is twice the radius. So maybe in a trapezoid with an incircle, the height is twice the radius? Is that a general formula? Wait, let me check with another example. Suppose a square with side length 2, inradius 1, then the height (which is the same as the side) is 2, which is twice the radius (1). Wait, but the inradius of a square is equal to half the side length, so if the inradius is r, the side is 2r, so the height (side) is 2r. So that's consistent. Another example, take a rectangle which is a tangential quadrilateral. The inradius would be half the height, so again, height is twice the radius. Wait, but a rectangle is a trapezoid as well (with both pairs of sides parallel). So in a rectangle, yes, the inradius is half the height. But in a non-rectangle trapezoid, like our case, the inradius is half the height. Wait, so in general for any tangential trapezoid, the inradius is equal to half the height? Therefore, height = 2r. So that's why here, with radius 3, the height is 6. So that formula is valid. Therefore, my initial thought was correct. So all steps are okay. So, in conclusion, the answer is 504. But let me check once more. Alternatively, perhaps there is a different approach. Let me think.",
      "char_len": 6477,
      "approx_tokens": 1619
    },
    {
      "type": "summary",
      "block_idx": 4,
      "text": "Checks consistency: area gives r+s=24; tangential isosceles => legs equal and r+s=2l => l=12. Uses (r+s)^2+(r-s)^2=2(r^2+s^2) with r-s=12*sqrt(3) to recompute r^2+s^2=504. Re-derives semiperimeter formula K=r*(perimeter/2) => r+s+2l=48 plus r+s=2l => l=12, h=6; confirms height=2*radius in this setting; concludes answer 504.",
      "char_len": 325,
      "approx_tokens": 81
    },
    {
      "type": "block",
      "block_idx": 5,
      "text": "In an isosceles trapezoid with an incircle, we know that the sum of the lengths of the two bases equals the sum of the lengths of the two legs. Since it's isosceles, legs are equal, so each leg is (r + s)/2. Wait, but legs can't be (r + s)/2 because legs are the non-parallel sides. Wait, actually, the condition is that the sum of the bases equals the sum of the legs. Since there are two legs, each of length l, so sum of legs is 2l, so indeed r + s = 2l. So legs are each length l = (r + s)/2. Wait, but in our case, since r + s =24, legs are 12 each, which is okay. Alternatively, since in an isosceles trapezoid with bases r and s, the legs can be calculated via the Pythagorean theorem as I did before. The difference of the bases is (r - s), so when you project the legs onto the base, the horizontal component is (r - s)/2. So the legs are hypotenuse of a right triangle with sides (r - s)/2 and h (height). Therefore, leg length squared is h\u00b2 + [(r - s)/2]^2. So:\n\\( l^2 = h^2 + \\left( \\frac{r - s}{2} \\right)^2 \\)\nWe have l = 12, h =6, so:\n12^2 = 6^2 + [(r - s)/2]^2\n144 = 36 + [(r - s)/2]^2\n[(r - s)/2]^2 = 108\nWhich again gives (r - s)^2 = 432.\nWe also know that (r + s)^2 = 24^2 = 576.\nThen, since (r + s)^2 + (r - s)^2 = 2(r\u00b2 + s\u00b2), so:\n576 + 432 = 2(r\u00b2 + s\u00b2)\n1008 = 2(r\u00b2 + s\u00b2) => r\u00b2 + s\u00b2 = 504. Yep, same result. Therefore, this confirms that the answer is indeed 504. I think that's solid. **Final Answer** \\boxed{504}",
      "char_len": 1434,
      "approx_tokens": 358
    },
    {
      "type": "summary",
      "block_idx": 5,
      "text": "Restates tangential condition r+s=2l with l=12. Uses leg formula l^2=h^2+((r-s)/2)^2: 144=36+((r-s)/2)^2 => (r-s)^2=432. With (r+s)^2=576, apply (r+s)^2+(r-s)^2=2(r^2+s^2) => r^2+s^2=504; final boxed answer 504.",
      "char_len": 211,
      "approx_tokens": 52
    },
    {
      "type": "answer",
      "block_idx": 0,
      "text": "Given an isosceles trapezoid with an inscribed circle (radius 3) and area 72, we need to find \\( r^2 + s^2 \\) where \\( r \\) and \\( s \\) are the lengths of the parallel sides.\n\n1. **Height Calculation**:\n   - The radius \\( r \\) is 3, so the height \\(
```


## File: blogpost/figures/example_science.json

```
{
  "problem": "Your overhear two chemists talking to each other as they leave a synthetic organic chemistry lab. One asks the other \"So, how did it go?\" The second chemist replies, \"Not well - my compounds are on top of each other.\"\n\nWhat is the second chemist most likely referring to?",
  "problem_source": "GPQA Diamond",
  "label": "Science",
  "answer": "C",
  "segments": [
    {
      "type": "block",
      "block_idx": 1,
      "text": "Okay, let's see. The problem is about two chemists talking, and one says their compounds are \"on top of each other. \" I need to figure out what that means from the given options. First, I'll consider each option one by one. Option A: Similar optical rotations. Optical rotation has to do with how a compound rotates plane-polarized light. If compounds have similar optical rotations, maybe they are enantiomers or similar stereoisomers. But how does that relate to being \"on top of each other\"? Maybe if they are superimposable, like mirror images, but enantiomers aren't superimposable. Hmm, not sure yet. Option B: Similar boiling points. Boiling point is related to intermolecular forces. If they have similar boiling points, maybe they have similar intermolecular forces. But how would that cause compounds to be on top of each other? Maybe in distillation, if boiling points are close, they would co-distill or not separate well. But the phrasing is \"on top of each other,\" maybe like overlapping in a distillation? Not sure. Option C: Similar polarities. Similar polarities would mean they have similar solubility, might not separate well in some techniques like chromatography. If they have similar polarity, maybe they co-elute, so their spots or peaks are on top of each other in TLC or GC? That seems possible. Like if you run a chromatogram and the compounds have similar Rf values or retention times, they'd overlap, making it hard to see them separately. That could be what \"on top of each other\" refers to. Option D: Bonding through non-covalent interactions. Van der Waals, hydrogen bonding, etc. If they are bonding that way, maybe they form aggregates or precipitates? Not sure how that would make compounds \"on top of each other. \" Maybe forming a complex that's hard to separate? Alternatively, if they stick too much, maybe clogging equipment?",
      "char_len": 1863,
      "approx_tokens": 465
    },
    {
      "type": "summary",
      "block_idx": 1,
      "text": "Begins interpreting phrase \"compounds are on top of each other\"; evaluates options: A) similar optical rotation (stereoisomer issue, uncertain link), B) similar bp (co-distillation overlap), C) similar polarity (co\u2011elution in chromatography), D) non\u2011covalent bonding (aggregation). Notes C most plausible for overlap in separation techniques.",
      "char_len": 342,
      "approx_tokens": 85
    },
    {
      "type": "block",
      "block_idx": 2,
      "text": "Now, considering common lab techniques. If you're doing chromatography, like TLC or column, compounds with similar polarity will have similar Rf values or retention times, so their spots/bands would overlap, making it hard to see them or analyze them separately. Similarly, in GC-MS, if two compounds have similar volatility, they co-elute. So if the compounds are \"on top of each other,\" that would be overlapping in a chromatogram, which would happen if they have similar polarity (so similar partitioning in chromatography) or similar boiling points (so similar volatility). The question is between B and C. Let me think again. Boiling points being similar would affect distillation. If you're trying to separate them by distillation, similar boiling points mean they won't separate well, so they might both distill over together. But the problem is, in distillation, you would say they \"co-distill\" but maybe not \"on top of each other. \" Whereas in chromatography, overlapping peaks are literally on top of each other in the chromatogram. Since the question is about a general lab setting, maybe chromatography is more common in organic synthesis. So similar polarities leading to overlapping spots or peaks would make sense. Alternatively, similar boiling points might lead to co-distillation but not necessarily being \"on top. \"",
      "char_len": 1334,
      "approx_tokens": 333
    },
    {
      "type": "summary",
      "block_idx": 2,
      "text": "Uses chromatography context: similar polarity \u2192 similar Rf/retention \u2192 overlapping bands; similar bp \u2192 co\u2011distillation; prefers C (chromatogram overlap) as more typical \"on top\" description.",
      "char_len": 190,
      "approx_tokens": 47
    },
    {
      "type": "block",
      "block_idx": 3,
      "text": "Also, non-covalent interactions (option D) might cause aggregation, but that might not make them \"on top of each other\" in a separation sense. Maybe they clump, but that's different from overlapping in a chromatogram. So between B and C. Let me think of the phrasing again: \"my compounds are on top of each other. \" In chromatography terms, if two compounds co-elute, their peaks overlap, so they are on top of each other in the chromatogram. That would happen if they have similar retention properties, which depend on polarity (among other factors). So if their polarities are similar, they might not separate properly. Alternatively, similar boiling points would lead to co-distillation, but in distillation, they might come off together, but you might say they \"come over together\" rather than \"on top of each other. \" Hmm. \"On top of each other\" might be a metaphor from chromatography where peaks overlap. So maybe the answer is C. Alternatively, in NMR spectroscopy, if compounds have similar chemical shifts, their signals could overlap. But that's more about molecular structure affecting shifts rather than bulk properties like polarity or boiling point. So maybe not. Wait, another angle: \"compounds are on top of each other\" could mean that they are superimposed in a spectrum, which would be due to similar properties that make them indistinguishable in the technique being used. Since the chemists are working in a synthetic lab, they might be using TLC, HPLC, GC, etc. In any case, similar polarity leading to similar Rf or retention times would cause overlapping spots or peaks. So C. Alternatively, if they have similar boiling points, during a distillation, the compounds would have overlapping distillation fractions. But the phrase \"on top of each other\" might not be the typical way to describe that. Maybe \"they come over together\" or \"they co-distill. \" Whereas in chromatography, \"on top of each other\" makes sense as peaks overlapping.",
      "char_len": 1960,
      "approx_tokens": 490
    },
    {
      "type": "summary",
      "block_idx": 3,
      "text": "Uses phrase interpretation + comparative analysis of options. Evaluates \"on top of each other\" as possible chromatographic peak overlap vs physical aggregation. Considers D (non-covalent interactions) but dismisses as clumping not separation overlap. Focuses on B (similar bp causing co-distillation) vs C (similar polarity causing co-elution). Notes chromatography terminology: overlapping peaks, co-elution, similar retention properties, Rf/retention time. Argues similar polarity leads to overlapping spots/peaks and fits the wording; similar bp gives co-distillation but not the same phraseology. Mentions NMR overlap as unlikely (structural shifts). Concludes C as most consistent.",
      "char_len": 686,
      "approx_tokens": 171
    },
    {
      "type": "block",
      "block_idx": 4,
      "text": "So I think the answer is B or C. Let me think again. The key is the phrasing \"on top of each other\". If they are on top in a chromatogram, then C. If in distillation, maybe B. But which is more likely? Alternatively, maybe the problem is referring to something else. Wait, another angle: \"compounds are on top of each other\" could mean they are layered? Like in a liquid-liquid extraction, if two compounds have different densities, they might form layers. But if they are on top, maybe they are immiscible? But the problem says \"on top of each other\" not separating, so maybe they can't be separated because they are mixed? Not sure. Alternatively, if they have similar polarities, they might not separate in a chromatogram. So in that case, the compounds are \"on top\" (overlapping) each other in the chromatogram. So C. Alternatively, if they have similar boiling points, distillation can't separate them, so they end up together in the same fraction, but \"on top of each other\" might not be the term. Alternatively, if they are forming a solid, maybe they can't be seen. But D is about bonding, so maybe forming aggregates, but again not sure. Another thought: \"on top of each other\" might mean they are superimposed, like in NMR spectra overlapping peaks. So that would be due to similar chemical environments, which could be due to similar structure, but the options given are about physical properties. So similar polarities (C) would affect HPLC, GC, etc. So I think the best answer is C. Wait, but let me check another angle. The problem says \"my compounds are on top of each other\". The compounds themselves, so maybe the product and starting material are still together because they didn't react. But that's not about physical properties. Alternatively, maybe they are in a reaction mixture that's a thick paste, but that's vague. Alternatively, if they have similar boiling points, and when distilled, they both evaporate at the same time, so the distillation didn't work, so the compounds are still mixed, \"on top of each other\". Hmm. Alternatively, the compounds are in a solution and can't be separated because they have similar solubility? But that's not one of the options. Wait, another thought: \"on top of each other\" could be a misinterpretation. Maybe the compounds are forming a superposition in NMR or something, but more likely the chromatogram. Alternatively, if the compounds are chiral and have similar optical rotations (A), but if they are enantiomers, their rotations are opposite. If they have similar magnitudes but opposite, maybe they net to zero? But how would that make them \"on top of each other\"? Not sure. Alternatively, if they are the same compound? But the question says compounds (plural). So probably different compounds. Hmm, I think the best options are B and C. Let me think of common lab scenarios. If you're doing chromatography, like TLC or HPLC, and two compounds have similar polarity, they would have similar Rf values or retention times, so their spots or peaks would be on top of each other, making it hard to see them as separate. That seems likely. So C is the answer. Alternatively, if they have similar boiling points, when you do distillation, you can't separate them, so they stay mixed. But the phrasing \"on top of each other\" makes me think visually in a chromatogram. So I think C is correct.",
      "char_len": 3355,
      "approx_tokens": 838
    },
    {
      "type": "summary",
      "block_idx": 4,
      "text": "Reconsiders B vs C; explores other contexts (extraction, NMR) but returns to chromatography overlap due to similar polarity as most consistent. Concludes likely answer = C.",
      "char_len": 172,
      "approx_tokens": 43
    },
    {
      "type": "answer",
      "block_idx": 0,
      "text": "The second chemist is most likely referring to **C) The compounds they are working with have similar polarities.**\n\n### Reasoning:\nThe phrase \"compounds are on top of each other\" suggests overlapping or co-elution in a separation technique like chromatography. In chromatography, compounds with **similar polarities** will have similar affinities for the stationary and mobile phases, leading to overlapping retention times or spots/bands on a chromatogram or TLC plate. This would make it difficult to distinguish or separate the compounds, hence them being \"on top of each other.\"\n\n- **Option A (Optical rotations):** Similar optical rotations might indicate enantiomers or similar stereoisomers, but this doesn\u2019t directly cause overlapping in analytical techniques like chromatography. \n- **Option B (Boiling points):** Similar boiling points would cause co-distillation, but the phrase \"on top of each other\" is more closely associated with separation issues in chromatography rather than distillation. \n- **Option D (Non-covalent interactions):** While such interactions might cause aggregation, this doesn\u2019t directly explain overlapping in analytical methods. \n\nThus, **Option C** best fits the context of separation challenges in common lab techniques like chromatography. \n\n**Answer: C) The compounds they are working with have similar polarities.**",
      "char_len": 1357,
      "approx_tokens": 339
    }
  ]
}
```


## File: blogpost/figures/extract_examples.py

```
#!/usr/bin/env python3
"""Extract specific examples from eval results and save as JSON for animation."""
import json
import re
import sys

def parse_response(full_response):
    """Parse a Memento response into segments."""
    text = full_response
    # Remove <think> wrapper
    text = re.sub(r'^<think>\s*', '', text)
    text = re.sub(r'</think>\s*', '', text)
    
    segments = []
    remaining = text
    block_idx = 0
    
    while remaining:
        bs = remaining.find("<|block_start|>")
        if bs == -1:
            answer_text = remaining.strip()
            if answer_text:
                segments.append({
                    "type": "answer",
                    "block_idx": 0,
                    "text": answer_text,
                    "char_len": len(answer_text),
                    "approx_tokens": len(answer_text) // 4
                })
            break
        
        if bs > 0:
            pre = remaining[:bs].strip()
            if pre:
                segments.append({
                    "type": "pre",
                    "block_idx": 0,
                    "text": pre,
                    "char_len": len(pre),
                    "approx_tokens": len(pre) // 4
                })
        
        remaining = remaining[bs + len("<|block_start|>"):]
        block_idx += 1
        
        be = remaining.find("<|block_end|>")
        if be == -1:
            break
        
        block_text = remaining[:be].strip()
        segments.append({
            "type": "block",
            "block_idx": block_idx,
            "text": block_text,
            "char_len": len(block_text),
            "approx_tokens": len(block_text) // 4
        })
        remaining = remaining[be + len("<|block_end|>"):]
        
        ss = remaining.find("<|summary_start|>")
        if ss == -1:
            break
        remaining = remaining[ss + len("<|summary_start|>"):]
        
        se = remaining.find("<|summary_end|>")
        if se == -1:
            break
        
        summary_text = remaining[:se].strip()
        segments.append({
            "type": "summary",
            "block_idx": block_idx,
            "text": summary_text,
            "char_len": len(summary_text),
            "approx_tokens": len(summary_text) // 4
        })
        remaining = remaining[se + len("<|summary_end|>"):]
    
    return segments

# Config: which examples to extract
targets = [
    {"source": "gpqa_diamond", "problem_idx": 39, "rep_idx": 0, 
     "label": "Science", "source_name": "GPQA Diamond"},
    {"source": "lcb_v6", "problem_idx": 380, "rep_idx": 0,
     "label": "Code", "source_name": "LiveCodeBench v6"},
]

source = sys.argv[1]  # gpqa_diamond or lcb_v6
target = [t for t in targets if t["source"] == source][0]

for line in sys.stdin:
    d = json.loads(line.strip())
    if d["problem_idx"] == target["problem_idx"] and d["rep_idx"] == target["rep_idx"]:
        segments = parse_response(d["full_response"])
        
        result = {
            "problem": d.get("problem", ""),
            "problem_source": target["source_name"],
            "label": target["label"],
            "answer": d.get("prediction", d.get("ground_truth", "")),
            "segments": segments
        }
        
        outfile = f"example_{target['label'].lower()}.json"
        with open(outfile, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"Wrote {outfile}")
        print(f"  Segments: {len(segments)}")
        for i, seg in enumerate(segments):
            print(f"  {i}: {seg['type']} idx={seg['block_idx']} chars={seg['char_len']} tokens≈{seg['approx_tokens']}")
        break

```


(… 42 more files omitted due to size limit)
<!-- fetched-content:end -->
