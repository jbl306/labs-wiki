---
title: "https://github.com/microsoft/memento"
type: url
captured: 2026-04-21T01:25:10.960840+00:00
source: android-share
url: "https://github.com/microsoft/memento"
content_hash: "sha256:40da9cbc38f18c26cb2fdc472d895ca9bf6fd5f4c41644ccf3b423579e7390b8"
tags: []
status: ingested
---

https://github.com/microsoft/memento

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:49:28+00:00
- source_url: https://github.com/microsoft/memento
- resolved_url: https://github.com/microsoft/memento
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: microsoft/memento
Description: None
Stars: 369
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
      "type": "summar
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
      "text": "Hmm, so the answer is 504? Let me just check my steps again to make sure I didn't make a mistake. First, area calculation: area = (r + s)/2 * h = 72. Since h = 6, then (r + s) must be 24. That seems okay.\nThen, since the trapezoid is tangential, the sum of the bases equals the sum of the legs. Since it's isosceles, both legs are equal, so each is 12. Therefore, 2 legs sum to 24, so that works with r + s =24. Then, using the legs as hypotenuse of a right triangle with height 6 and base difference/2. The difference of the bases is 12\u221a3, so (12\u221a3)/2 = 6\u221a3. Then, the Pythagorean theorem:\n(6\u221a3)^2 + 6^2 = (leg)^2 ?\nWait, 6\u221a3 squared is 36*3 = 108, plus 36 is 144, which is 12^2. That checks out. So that's correct.\nTherefore, r and s are 12 \u00b1 6\u221a3, and their squares add to 504. Hmm, that seems straightforward. Let me just confirm the calculation of r\u00b2 + s\u00b2 again. Alternatively, maybe there's a smarter way to compute r\u00b2 + s\u00b2 without having to find r and s individually? We know that:\n(r + s)^2 = r\u00b2 + 2rs + s\u00b2\n(r - s)^2 = r\u00b2 - 2rs + s\u00b2\nTherefore, (r + s)^2 + (r - s)^2 = 2(r\u00b2 + s\u00b2) Therefore,\nr\u00b2 + s\u00b2 = [(r + s)^2 + (r - s)^2]/2 We already know r + s =24 and r - s =12\u221a3, so:\n[(24)^2 + (12\u221a3)^2]/2 = [576 + 144*3]/2 = [576 + 432]/2 = 1008/2 = 504 Same result. So that's correct. Therefore, the answer should be 504. Let me see if there's any possible mis
```


(… 48 more files omitted due to size limit)
<!-- fetched-content:end -->
