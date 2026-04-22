---
title: Thought-Action-Result (TAR) Trajectories
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "5173b70a6725e131573c351830b6c4874521518221c53b9cb004f836568ed255"
sources:
  - raw/2026-04-22-260401437v1pdf.md
related:
  - "[[Agentic AI Evaluation for Software Engineering]]"
  - "[[The Observability Imperative]]"
  - "[[Agent Memory Frameworks]]"
tier: hot
tags: [agentic-ai, evaluation, trajectories, observability, software-engineering, reproducibility]
---

# Thought-Action-Result (TAR) Trajectories

## Overview

Thought-Action-Result (TAR) trajectories are structured traces of how an autonomous agent reasoned, what it did, and what happened after each step. In the arXiv position paper *Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering*, TAR trajectories are presented as a critical evaluation artifact because they expose process-level evidence that final metrics alone cannot capture.

They matter because software-engineering agents do not succeed or fail in a single atomic move. They plan, inspect code, invoke tools, interpret outputs, revise hypotheses, and sometimes spiral into dead ends. A TAR trajectory preserves those intermediate states, making an evaluation explainable enough for other researchers to analyze and reproducible enough for them to compare approaches meaningfully.

## How It Works

At a high level, a TAR trajectory records an execution as a sequence of triples:

$$
\tau = \left[(t_1, a_1, r_1), (t_2, a_2, r_2), \ldots, (t_n, a_n, r_n)\right]
$$

where each `t` is a thought or intermediate rationale, each `a` is an action taken in the environment, and each `r` is the resulting observation, state change, or tool output. The paper does not prescribe this exact notation, but its recommendation implies this basic structure: capture not only what the agent did, but also the reasoning context and the observed consequence. That makes the trace substantially richer than a simple event log.

The first component, **thought**, is what turns a TAR record from a shell transcript into an evaluation artifact. In agentic software-engineering tasks, a raw action like "open file", "run tests", or "edit function" is often ambiguous without the intermediate hypothesis that motivated it. A useful trajectory therefore records the local decision logic: what bug the agent thinks it is chasing, which file it believes is relevant, or why it chose a specific remediation path. Even if those thoughts are summarized rather than released verbatim, the key function is preserved: a reviewer can understand the intended strategy behind each move.

The second component, **action**, captures the concrete intervention. In the software-engineering setting described by the paper, actions may include reading repository files, issuing tool calls, modifying code, running tests, querying documentation, or navigating issue context. Actions anchor the trajectory in externally inspectable behavior. This is why the paper recommends publishing LLM interaction data alongside or in summarized form with TAR trajectories: actions become more interpretable when paired with the prompts, tool inputs, and environment state that produced them.

The third component, **result**, closes the loop. A result may be a command output, a test failure, a compiler error, a changed program state, or an unexpected observation from the environment. Without the result field, an evaluator only sees intent and intervention, not whether the step actually moved the agent closer to success. Results are especially valuable for failure analysis because they reveal whether an error came from a bad plan, a bad tool call, a misread observation, or a brittle benchmark setup. This is one reason the paper argues that final success metrics are insufficient on their own.

Once a trajectory is captured, it can support several kinds of analysis. Researchers can compare two approaches that reached the same final outcome but followed very different paths. They can inspect where one agent repeatedly loops, where another agent overfits to a benchmark hint, or where a third agent succeeds only because an environmental detail was favorable. The paper's proof-of-concept case study exists precisely to show that these kinds of cross-approach analyses become feasible when TAR traces are available. In other words, the trajectory is not just a debugging log; it is a comparative research instrument.

The paper also makes an important practical concession: full raw traces are not always easy to release. They can be large, noisy, or sensitive. That is why the recommendation explicitly includes "summarized versions" of TAR trajectories and interaction data. The crucial principle is not maximal rawness; it is preservation of enough causal structure to let later readers understand what the agent attempted and why. A high-quality summary should therefore preserve sequence, decision points, failures, and notable observations rather than collapsing the run into a single paragraph.

This makes TAR trajectories tightly aligned with **[[The Observability Imperative]]**. Observability says that complex AI workflows must retain enough runtime evidence to be debuggable and auditable. TAR trajectories operationalize that idea for evaluation: they expose the internal decision path of an agent in a form that can be inspected by humans, compared across papers, and potentially reused as substrate for memory or analysis systems. They are also adjacent to **[[Agent Memory Frameworks]]**, because the same traces that support evaluation can later be distilled into reusable lessons or reasoning memories.

In practice, TAR trajectories work best when they are treated as first-class outputs of an evaluation pipeline rather than as incidental byproducts. If a benchmark only stores final scores, later explanation is mostly impossible. If it stores trajectories, prompts, and selected environment state, later work can ask stronger questions: Which failures were avoidable? Which tools were misused? Which benchmark wins were robust versus accidental? That shift from outcome-only evidence to process-aware evidence is the concept's main contribution.

## Key Properties

- **Process visibility**: Exposes the sequence of reasoning, action, and feedback rather than only the terminal result.
- **Comparability**: Makes it possible to compare different agent approaches step by step, not just score by score.
- **Failure localization**: Helps identify whether failure came from planning, tool use, interpretation, or environment mismatch.
- **Summarizability**: Can be released in full or as structured summaries while still preserving causal structure.
- **Auditability**: Supports inspection, replication, and critique by third parties after a paper is published.

## Limitations

- **Storage and publication cost**: Full traces can be long, expensive to store, and awkward to package in a paper artifact.
- **Privacy and leakage concerns**: Prompts, repository content, or proprietary tool outputs may limit what can be released publicly.
- **Summary loss**: Over-compressed summaries can remove the exact step where an approach succeeded or failed, defeating the purpose.
- **Observer-effect risk**: Instrumentation and logging policies can subtly change an agent's runtime behavior or latency budget.
- **No guarantee of validity**: A detailed trajectory can still document a flawed benchmark, weak baseline, or biased task set.

## Examples

A minimal TAR schema for a coding-agent evaluation might look like this:

```python
trajectory = [
    {
        "thought": "The failing tests mention parsing, so inspect tokenizer changes first.",
        "action": "open src/tokenizer.py",
        "result": "Found a branch that strips newline tokens unconditionally."
    },
    {
        "thought": "The parser probably needs conditional stripping for markdown tables.",
        "action": "edit src/tokenizer.py and rerun targeted tests",
        "result": "Tokenizer tests pass; integration test still fails on escaped pipes."
    }
]
```

Even this simplified form is much more informative than a statement such as "the agent eventually fixed the bug." It reveals search strategy, intervention sequence, and partial progress.

## Practical Applications

TAR trajectories are useful for benchmark papers, artifact appendices, internal evaluation dashboards, and post-hoc debugging of software-engineering agents. They are especially valuable when teams need to compare competing agents on the same repository task, explain surprising benchmark outcomes, or analyze why a system failed in a production-like environment. In each case, the trajectory becomes the evidence layer between raw execution and scientific or engineering judgment.

## Related Concepts

- **[[Agentic AI Evaluation for Software Engineering]]**: The broader methodology in which TAR trajectories serve as a core evidence artifact.
- **[[The Observability Imperative]]**: A general principle that complex AI workflows must retain enough detail to be inspectable and auditable.
- **[[Agent Memory Frameworks]]**: Trajectory records can later be distilled into reusable memories, though evaluation and memory serve different immediate goals.
