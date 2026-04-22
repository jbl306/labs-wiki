---
title: "Building Effective Agents (Anthropic)"
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: ffc229d83891918f82064b92e6624a3de7bce686fc211cb123e4eb4a0cd488f1
sources:
  - raw/2026-04-22-test-html-anthropic-agents.md
source_url: https://www.anthropic.com/engineering/building-effective-agents
concepts:
  - augmented-llm
  - prompt-chaining-workflow
  - orchestrator-workers-workflow
  - evaluator-optimizer-workflow
related:
  - "[[Anthropic]]"
  - "[[Anthropic’s 'Building Effective Agents' Guide]]"
  - "[[Claude]]"
  - "[[SWE-Bench-Verified]]"
tags: [anthropic, agentic-systems, llm-agents, workflows, tool-use]
tier: warm
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Building Effective Agents (Anthropic)

## Summary

Anthropic's December 2024 engineering guide argues that effective LLM agents are usually built from simple, composable patterns rather than heavyweight frameworks. It distinguishes deterministic **workflows** from more autonomous **agents**, recommends starting with the least complex design that works, and catalogs production-tested patterns such as prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer loops.

## Key Points

- **Start simple first**: Anthropic recommends exhausting simpler options such as a single LLM call with retrieval and in-context examples before introducing agentic complexity.
- **Core architectural split**: The guide distinguishes **workflows**, where code predefines the path, from **agents**, where the model dynamically decides which tools and steps to use.
- **Foundational building block**: The base unit of an agentic system is an [[Augmented LLM]] with access to retrieval, tools, and memory.
- **Framework caution**: Frameworks can accelerate setup, but they often hide prompts and responses behind abstractions that make systems harder to debug and easier to overcomplicate.
- **[[Prompt Chaining Workflow]]**: Best for tasks that can be decomposed into fixed stages, optionally with gates or validation checks between stages.
- **Routing and parallelization**: Routing specializes downstream handling by input type, while parallelization improves speed or confidence through sectioning and voting.
- **[[Orchestrator-Workers Workflow]]**: Useful when the required subtasks are not known in advance, such as multi-file coding changes or multi-source research tasks.
- **[[Evaluator-Optimizer Workflow]]**: Effective when there are clear evaluation criteria and iterative critique can materially improve the output.
- **Agent operating model**: Autonomous agents should gather ground truth from the environment, pause for human feedback at checkpoints, and run with explicit stopping conditions.
- **Design principles**: Anthropic closes with three operating principles for production agents: preserve simplicity, expose planning transparently, and invest heavily in the agent-computer interface through well-designed tools and documentation.
- **High-value domains**: The guide highlights customer support and coding agents as especially strong fits because both combine conversation with action and provide relatively clear success criteria.
- **Benchmarked coding example**: Anthropic points to coding agents solving tasks on [[SWE-Bench-Verified]] as evidence that autonomous loops become practical when outputs are verifiable through tests.

## Key Concepts

- [[Augmented LLM]]
- [[Prompt Chaining Workflow]]
- Routing workflow
- Parallelization workflow
- [[Orchestrator-Workers Workflow]]
- [[Evaluator-Optimizer Workflow]]

## Related Entities

- **[[Anthropic]]** — Publisher of the guide and the organization framing these recommendations from deployment experience.
- **[[Anthropic’s 'Building Effective Agents' Guide]]** — The guide as a durable wiki entity for the article's arguments and pattern catalog.
- **[[Claude]]** — Anthropic's model family, referenced through examples such as Claude Haiku 4.5 and Claude Sonnet 4.5 in routing guidance.
- **[[SWE-Bench-Verified]]** — Benchmark cited as a concrete setting where coding agents can operate with test-driven feedback.
