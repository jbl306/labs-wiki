---
title: "Recursive Language Models"
type: concept
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "5f2847d1dbcf35bd34acfecc570026a5d5e0b7bde6f961fa89402aa86610f961"
sources:
  - raw/2026-04-10-251224601v2pdf.md
quality_score: 75
concepts:
  - recursive-language-models
related:
  []
  []
  []
tier: hot
tags: [language-models, long-context, recursion, scaffolding, prompt-engineering, inference]
---

# Recursive Language Models

## Overview

Recursive Language Models (RLMs) are an inference-time scaffold for large language models (LLMs) that enable them to process arbitrarily long prompts by treating the prompt as an external environment. This paradigm allows the LLM to programmatically examine, decompose, and recursively invoke itself over portions of the input, overcoming the limitations of fixed context windows and enabling dense access to prompt content.

## How It Works

The core mechanism of RLMs is to wrap a base neural language model (ℳ) with a persistent Read-Eval-Print Loop (REPL) environment. Upon receiving an arbitrary-length prompt string P, the RLM initializes the REPL with P as a variable and provides a function for invoking sub-RLMs on new prompts. The process begins by supplying the LLM with metadata about the prompt (such as its length, a short prefix, and access methods), rather than the full prompt itself. The LLM is prompted or fine-tuned to operate as an RLM, generating code that manipulates and transforms parts of P, building intermediate values, and recursively invoking sub-RLMs as needed.

Algorithmically, the RLM loop iterates as follows:
1. The LLM receives only constant-size metadata about the prompt and the current REPL state.
2. The LLM generates code to interact with the prompt variable, possibly decomposing it or launching recursive calls on slices of the prompt.
3. The REPL executes the generated code, updates its state, and collects any output.
4. Only metadata about the output (e.g., prefix and length) is appended to the LLM's history for the next iteration, avoiding context window pollution.
5. This process repeats until a designated 'Final' variable is set in the REPL, at which point its value is returned as the response.

Symbolic recursion is central: code running in the REPL can invoke the LLM on programmatically constructed transformations of P, enabling loops over slices and launching Ω(|P|) or even Ω(|P|^2) processes to understand or transform all parts of the prompt. This is in contrast to standard scaffolds, which typically copy the prompt into the context window and rely on context compaction or summarization, losing dense access and expressive power.

RLMs make three key design choices:
- The prompt is handled as a symbolic variable in the environment, not copied into the LLM's context window.
- Output is constructed programmatically, not autoregressively, allowing outputs longer than the context window.
- Recursion is symbolic and programmatic, enabling the LLM to launch arbitrarily many sub-calls and manage intermediate results.

Empirically, RLMs are shown to scale to 10M+ token inputs, outperforming base LLMs and common scaffolds (summarization, retrieval, code-generation agents) across tasks like deep research, information aggregation, code repository understanding, and synthetic pairwise reasoning. The REPL environment is necessary for handling long inputs, and recursive sub-calling provides strong benefits for information-dense tasks. RLMs' performance degrades much less with increasing input length and task complexity compared to vanilla LLMs, and their inference costs remain comparable, though with higher variance due to trajectory length differences.

Fine-tuning a model to be natively recursive (e.g., RLM-Qwen3-8B) further improves performance, with a simple training recipe yielding a 28.3% median gain across evaluation tasks. Training focuses on enhancing the model's ability to manipulate the REPL and launch recursive calls, making it more tractable at small scale.

## Key Properties

- **Scalability:** RLMs can process inputs up to two orders of magnitude beyond the base model's context window, handling 10M+ token prompts.
- **Expressive Power:** Symbolic recursion and programmatic decomposition allow RLMs to densely access and transform all parts of the prompt, outperforming compaction and retrieval-based scaffolds.
- **Cost Efficiency:** RLMs maintain comparable or even lower average token costs than base LLMs and summarization agents, though with higher variance due to recursive trajectory lengths.
- **Model-Agnostic:** RLMs are an inference-time strategy applicable to any LLM, though different models may exhibit different context management and sub-calling behaviors.

## Limitations

RLMs may perform slightly worse than base LLMs on small input contexts due to overhead from the REPL and recursive scaffolding. The inference cost has high variance, with some trajectories being significantly more expensive. Implementation details (e.g., sequential vs. asynchronous LM calls) affect runtime. RLMs require careful prompting or fine-tuning to operate effectively, and excessive recursion or sub-calling can lead to inefficiency.

## Example

Algorithm 1 (from the paper):
```python
# Pseudocode for Recursive Language Model
state = InitREPL(prompt=P)
state = AddFunction(state, sub_RLM)
hist = [Metadata(state)]
while True:
    code = LLM(hist)
    state, stdout = REPL(state, code)
    hist = hist + code + Metadata(stdout)
    if state['Final'] is set:
        return state['Final']
```
This loop allows the LLM to generate code that recursively processes slices of the prompt, storing intermediate results and launching sub-calls as needed.

## Visual

Figure 1: Line chart comparing GPT-5 and RLM(GPT-5) performance across three long-context tasks (S-NIAH, OOLONG, OOLONG-Pairs) as input length increases. GPT-5 performance degrades steeply with longer prompts and higher task complexity, while RLM maintains strong performance even beyond GPT-5's context window. Figure 2: Diagram showing an RLM treating the prompt as a variable in a REPL environment, with code written to peek into, decompose, and recursively invoke itself over prompt snippets.

## Relationship to Other Concepts

- **Context Compaction** — RLMs overcome the limitations of context compaction by enabling dense access to prompt content.
- **Retrieval-Augmented Generation** — RLMs provide a more expressive alternative to retrieval-based scaffolds for long-context tasks.
- **Code Generation Agents** — RLMs extend the programmatic capabilities of code-generation agents by enabling symbolic recursion and environment interaction.

## Practical Applications

RLMs are suited for tasks requiring processing of extremely long or information-dense inputs, such as deep research (multi-document reasoning), code repository understanding, large-scale information aggregation, and synthetic reasoning tasks where answers depend on dense access to the entire prompt. They are particularly valuable in settings where context window limitations would otherwise constrain performance, such as legal document analysis, scientific literature review, and large-scale data mining.

## Sources

- Recursive Language Models — primary source for this concept
