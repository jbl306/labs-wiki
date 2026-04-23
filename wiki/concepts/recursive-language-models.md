---
title: "Recursive Language Models"
type: concept
created: 2026-04-10
last_verified: 2026-04-23
source_hash: "7368a08484d58101c8102490723a5cbfabe63a85dde56bb84b8cde3ecabf99e8"
sources:
  - raw/2026-04-10-251224601v2pdf.md
  - raw/2026-04-23-251224601v2pdf.md
related:
  - "[[Block Masking for LLM KV Cache Compaction]]"
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[Augmented LLM]]"
tier: hot
tags: [language-models, long-context, recursion, inference-time-scaling, agentic-systems]
quality_score: 90
---

# Recursive Language Models

## Overview

Recursive Language Models (RLMs) are an inference-time scaffold for large language models that treat the prompt itself as part of an external environment rather than as a blob that must fit inside one forward pass. The key move is to let the model inspect, decompose, transform, and recursively re-query prompt fragments through executable code, which turns long-context reasoning into an active control problem instead of a passive attention-allocation problem. This matters because many tasks fail not when the model "forgets" the prompt in a vague sense, but when the model cannot afford dense access to all the parts that matter at once.

## How It Works

An RLM starts with a base neural model $\mathcal{M}$ that has a fixed context limit $K$, but it refuses to treat that limit as the boundary of the overall task. Given an arbitrary prompt string $P \in \Sigma^\*$, the scaffold creates a persistent environment $\mathcal{E}$, typically a REPL, and stores $P$ there as data. The model is then shown only compact metadata about that environment: facts like prompt length, a short prefix, available helper functions, and later the length or prefix of any stdout emitted by executed code. In other words, the model never has to ingest the full prompt just to start reasoning about it.

The control loop is simple but powerful. The root model emits code, the REPL executes it, the environment state updates, and the next model call sees metadata about what changed. One of the functions exposed inside the environment is a recursive sub-call operator, often written as `sub_RLM`, which lets the model invoke another RLM call on a programmatically constructed prompt fragment. A schematic form is:

$$
\text{state} \leftarrow \text{InitREPL}(P), \qquad
\text{hist}_0 = [\text{Metadata(state)}]
$$

and then, iteratively,

$$
\text{code}_t \leftarrow \mathcal{M}(\text{hist}_{t-1}), \qquad
(\text{state}_t, \text{stdout}_t) \leftarrow \text{REPL}(\text{state}_{t-1}, \text{code}_t).
$$

The final answer is not forced to appear as an autoregressive tail of the root model's context. Instead, the loop stops once the environment contains a designated value such as `Final`, and the system returns that variable. That detail matters: it means the scaffold is not only trying to beat the input-window limit, but also the output-window limit.

The paper argues that three design choices separate true RLMs from lookalike agent loops. First, the prompt must be stored symbolically in the environment rather than copied into model history. If the prompt starts inside the model window, the system inherits the original context bottleneck and eventually falls back to compaction or truncation. Second, recursive calls must be programmatic rather than verbalized. A model that can merely "ask for a sub-call" in natural language still has to spend output budget describing each delegation. Third, intermediate results must live symbolically in environment variables, so the scaffold can compose many partial computations without constantly reserializing them into the root history.

This changes the effective growth law of reasoning. In a standard long prompt setup, the model history is roughly dominated by $|P|$ plus whatever additional turns accumulate:

$$
|\text{hist}_{\text{standard}}| \approx |P| + O(Tc),
$$

where $T$ is the number of steps and $c$ is the average control-trace size per step. In an RLM, the root history is closer to:

$$
|\text{hist}_{\text{RLM}}| \approx O(Tc),
$$

because the prompt stays external and only metadata enters the model window. That does not make the task free; it shifts cost from "attend to every token every turn" to "actively query the right pieces at the right time." The payoff is that the system can do semantic work that scales like $\Omega(|P|)$ for line-by-line processing or even $\Omega(|P|^2)$ for pairwise aggregation, without pretending those operations fit neatly inside one monolithic context.

Why does this help in practice? The experiments show that models can use executable code plus priors to filter huge inputs before paying sub-call costs. In successful trajectories, the model searches with regexes, chunks large prompts by line or section boundaries, invokes recursive sub-calls on smaller slices, and stitches outputs together in variables. This is especially important on tasks like OOLONG-Pairs, where the answer depends on comparisons across many pairs of prompt segments. A plain long-context model may technically fit some of the data, but it still struggles to organize the computation. The RLM scaffold gives it a procedural workspace for doing that organization.

The empirical results make the mechanism concrete. Across S-NIAH, BrowseComp-Plus, OOLONG, OOLONG-Pairs, and LongBench-v2 CodeQA, RLMs outperform base models and several task-agnostic baselines such as summary agents, retrieval-enabled CodeAct agents, and REPL agents without sub-calls. The gains are modest or sometimes negative on very small contexts, where the scaffold overhead is not worth it, but they become dramatic as prompt length and problem complexity grow. The strongest illustration is that base models remain near zero on OOLONG-Pairs while RLM(GPT-5) reaches 58.0% F1. A post-trained version, [[RLM-Qwen3-8B]], further improves average performance by 28.3% over base Qwen3-8B as an RLM, suggesting the behavior is trainable rather than merely prompt-induced.

RLMs are therefore best understood as a computational interface, not just a prompt trick. They turn the model into a controller over an external symbolic workspace, where recursion, decomposition, and answer construction can happen with much finer control over what enters active neural context. That is why they compare naturally with memory hierarchies, tool-using agents, and compaction systems, yet remain distinct from all of them.

## Key Properties

- **Externalized prompt state**: The full prompt remains in the environment, so the model window carries metadata and control traces instead of raw long-form input.
- **Symbolic recursion**: The environment can launch `sub_RLM` calls inside loops and over generated prompt slices, enabling dense processing patterns that ordinary one-shot prompting cannot express.
- **Unbounded output construction**: Final answers can be assembled in variables and returned from the environment, rather than being limited to one continuous autoregressive stream.
- **Task-dependent scaling**: The scaffold shines most on information-dense or combinatorial tasks such as OOLONG and OOLONG-Pairs, where naive long-context access is not enough.
- **Model-agnostic but behavior-sensitive**: The idea works with multiple base models, yet each model makes different choices about chunking, search, and recursion depth.

## Limitations

RLMs are not a free substitute for longer native contexts. The scaffold adds overhead, so on short inputs the base model can still be better. Cost variance is another real limitation: median runs can be competitive or even cheaper than baselines, while outlier recursive trajectories become much more expensive because they make too many exploratory calls.

The design also depends on competent control behavior. If the model chooses poor chunk boundaries, launches wasteful recursion, or relies on brittle keyword heuristics, the extra expressive power translates into extra waste instead of extra accuracy. Finally, the paper's implementation uses blocking sequential LM calls, so runtime depends heavily on engineering details such as latency, asynchronous execution, and the efficiency of the REPL environment.

## Examples

```python
def run_rlm(prompt: str):
    state = InitREPL(prompt=prompt)
    state = AddFunction(state, "sub_RLM", sub_rlm)
    hist = [Metadata(state)]

    while True:
        code = LM(hist)
        state, stdout = REPL(state, code)
        hist = hist + [code, Metadata(stdout)]
        if state.get("Final") is not None:
            return state["Final"]
```

In practice, the interesting part is what `code` does. On a repository-understanding task it might split a file listing, identify candidate directories, recursively query the most relevant files, and combine the findings into one answer string. On a pairwise aggregation task it might chunk the prompt into records, loop over pairs, store intermediate judgments in variables, then synthesize a final result from those variables.

## Practical Applications

RLMs are useful when the main bottleneck is not just storing long text, but performing structured work over that text: multi-document research, codebase understanding, scientific literature review, legal analysis, and any task where the answer depends on inspecting many localized regions of a very large prompt. They are especially attractive when the deployment environment can expose a controlled execution surface and when we care about dense access to source material rather than just summary preservation.

They are less attractive as a default scaffold for every chat interaction. If the task is short-horizon or if the serving environment cannot safely support code execution and recursive sub-calls, simpler approaches remain easier to operate. The concept is best reserved for cases where fixed-window attention is the actual bottleneck.

## Related Concepts

- **[[Block Masking for LLM KV Cache Compaction]]**: Block masking keeps the token-stream paradigm and compresses past state, whereas RLMs move prompt access into an external symbolic environment.
- **[[Memento Blockwise Summarization for LLMs]]**: Both extend effective reasoning horizon, but Memento relies on learned summaries and cache eviction while RLMs rely on active inspection and recursive decomposition.
- **[[Augmented LLM]]**: RLMs are a specialized augmented-LLM pattern in which the most important tool is symbolic access to the prompt itself.

## Sources

- [[Recursive Language Models]] — primary paper describing the scaffold, baselines, and training results
