---
title: "Block Masking for LLM KV Cache Compaction"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
related:
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[KV Cache and Paged Attention in Large Language Models]]"
  - "[[vLLM Block Masking Overlay]]"
  - "[[Reasoning Trace Segmentation and Iterative Summarization]]"
tier: hot
tags: [llm, kv-cache, block-masking, vllm, inference, long-context]
quality_score: 82
---

# Block Masking for LLM KV Cache Compaction

## Overview

Block masking is an inference-time method for extending effective reasoning length by selectively evicting old reasoning spans from a transformer's KV cache once they have been summarized. In the Memento stack, the model emits explicit block and summary delimiters, and the serving runtime uses those delimiters to decide which cached tokens are safe to compact.

What makes the idea important is that it reframes long-context scaling as a state-management problem instead of purely a model-size or context-window problem. Rather than preserving every token forever, the runtime keeps only the compressed state that later reasoning still needs.

## How It Works

Autoregressive transformers accumulate a KV cache as they generate tokens. Every new token needs to attend over the keys and values of all previous tokens that remain in context, so the cache grows with sequence length and eventually becomes the system bottleneck. Standard inference optimizations such as KV caching and paged attention make this process faster or more memory-efficient, but they still assume that previously generated content remains semantically necessary in near-original form.

Block masking changes that assumption. It starts from a model that has been trained to write reasoning in structured chunks. A typical Memento-formatted trace looks like:

```text
<think>
<|block_start|> ... detailed reasoning ... <|block_end|>
<|summary_start|> ... compressed summary ... <|summary_end|>
</think>
```

The runtime treats the detailed reasoning and the summary differently. The block is high-resolution working state, while the summary is the durable representation meant to survive into future steps. Once the summary closes, the runtime no longer needs the full token-by-token internals of the earlier reasoning block if the model has learned to rely on the summary as its carry-forward memory.

Operationally, the serving system keeps a per-request state machine that tracks whether generation is inside a block, inside a summary, or outside the Memento reasoning channel entirely. When it sees `<|block_start|>`, it records the beginning of a potentially disposable region. When it sees `<|block_end|>`, it knows that the verbose reasoning span has completed. When it later sees `<|summary_end|>`, it has both the verbose block and the compressed summary, so it can trigger compaction.

The compaction rule can be expressed schematically as:

$$
K_{active}, V_{active} = f(K_{prompt}, V_{prompt}, K_{summaries}, V_{summaries}, K_{recent}, V_{recent})
$$

instead of the usual:

$$
K_{active}, V_{active} = f(K_{prompt}, V_{prompt}, K_{all\ previous\ tokens}, V_{all\ previous\ tokens})
$$

In other words, the active attention state is no longer "all old tokens." It is "prompt plus summaries plus whatever recent blocks we choose to preserve."

That choice is governed by runtime configuration. `keep_last_n_blocks` determines whether some number of recent reasoning blocks should remain uncompressed. `mask_delimiters` controls whether delimiter tokens themselves are evicted along with the reasoning content. `compact_on_summary_end` determines when the system pulls the trigger. `keep_last_block_for_answer` is a more conservative option that delays compaction of the final block so the model has high-resolution context right before emitting the answer. `restart_mode` offers an alternate strategy that evicts and recomputes summary KV state instead of operating in the ordinary compact mode.

The result is a different growth curve for active context. If a sequence contains $n$ completed reasoning blocks with lengths $b_1, b_2, ..., b_n$ and summary lengths $s_1, s_2, ..., s_n$, standard decoding keeps approximately:

$$
L_{standard} \approx L_{prompt} + \sum_{i=1}^{n} b_i + \sum_{i=1}^{n} s_i
$$

whereas block masking aims for something closer to:

$$
L_{masked} \approx L_{prompt} + \sum_{i=1}^{n} s_i + \sum_{j \in recent} b_j
$$

If summaries are much shorter than blocks, the gap becomes large. That is the core efficiency gain: preserve semantic continuity with summaries while dropping the expensive full-resolution history.

The catch is that block masking only works if the summaries are faithful. If the model omits a latent assumption, loses a variable binding, or compresses too aggressively, the later reasoning path will attend over an incomplete memory. In that case the runtime has saved memory at the cost of correctness. This is why Memento pairs block masking with a training pipeline that explicitly teaches summary generation and judges summary quality.

Another subtle requirement is that the rest of the inference stack must not silently violate the compaction assumption. The Memento overlay specifically notes that prefix caching should be disabled, because prefix reuse can preserve stale state in ways that do not line up with block-eviction semantics. Likewise, inspecting output often requires `skip_special_tokens=false`, since the special markers are part of the observable protocol rather than noise to strip out.

The best intuition is to treat block masking like garbage collection for reasoning. A long derivation is produced in full, distilled into a durable note, then the bulky working memory behind that note is reclaimed. The technique is not just about making KV cache smaller; it is about defining which parts of prior reasoning are worth keeping at full fidelity and which can safely collapse into structured summaries.

## Key Properties

- **Explicit boundary dependence:** The method requires reliable delimiter tokens so the runtime knows exactly where disposable spans begin and end.
- **Runtime-controlled memory policy:** Compaction behavior is configurable through `keep_last_n_blocks`, `mask_delimiters`, `compact_on_summary_end`, and related switches.
- **Semantic compression instead of raw retention:** The system preserves summaries, not the full internal reasoning trace.
- **Model-and-runtime co-design:** It only works well when the model has been trained to write useful summaries and the runtime has been patched to act on them.
- **Context-budget extension:** Effective reasoning length grows because active cache length scales with summaries and only a small set of recent blocks.

## Limitations

Block masking is brittle when summary quality is weak. A model can follow the delimiter format correctly while still dropping crucial state from the summary, causing downstream errors that are hard to diagnose because the original block has already been evicted.

It also depends on a custom runtime path. A vanilla model server will happily emit Memento-style tokens but will not compact the cache, so the main systems benefit disappears. Finally, the technique does not eliminate context limits; it reallocates the budget more intelligently, which still leaves trade-offs around summary fidelity, recent-block retention, and final-answer context.

## Examples

```python
from vllm import LLM

llm = LLM(
    model="path/to/memento-checkpoint",
    block_masking_config={
        "enable": True,
        "keep_last_n_blocks": 0,
        "mask_delimiters": False,
        "compact_on_summary_end": True,
        "keep_last_block_for_answer": False,
    },
    max_model_len=32768,
    enable_prefix_caching=False,
)
```

In this configuration, every completed reasoning block becomes eligible for eviction once its summary finishes, so the active cache tracks summaries plus the latest unresolved reasoning rather than the entire chain of thought.

## Practical Applications

Block masking is most useful for long-form reasoning workloads where the model must keep working through many intermediate steps: mathematical derivations, code synthesis with multi-stage planning, long scientific explanations, and tool-using agents that benefit from internal reflection but still need bounded inference memory.

It is especially relevant when we can control both the model behavior and the serving stack. That makes it attractive for research systems, benchmark experiments, and dedicated long-context deployments, but less attractive for generic third-party API use where neither the model internals nor the KV-cache policy are accessible.

## Related Concepts

- **[[Memento Blockwise Summarization for LLMs]]**: Block masking is the runtime half of the larger Memento protocol.
- **[[KV Cache and Paged Attention in Large Language Models]]**: Provides the baseline memory-management context that block masking extends.
- **[[Reasoning Trace Segmentation and Iterative Summarization]]**: Produces the training data that teaches models to emit summaries suitable for compaction.

## Sources

- [[microsoft/memento]] — primary source for this concept
