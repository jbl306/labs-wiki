---
title: "AXI Design Principles for Agent-Ergonomic CLI Tools"
type: concept
created: 2026-04-10
last_verified: 2026-04-22
source_hash: "7ef9072ee6e8f54af2f4e053827cb93014f7a120cab02927398106bd2360e937"
sources:
  - raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
quality_score: 79
concepts:
  - axi-design-principles-for-agent-ergonomic-cli-tools
related:
  - "[[Agent Handoffs in VS Code]]"
  - "[[The Context Hygiene Principle]]"
  - "[[kunchenguid/axi]]"
tier: hot
tags: [agent ergonomics, cli design, token efficiency, automation, TOON format, session hooks, structured errors]
---

# AXI Design Principles for Agent-Ergonomic CLI Tools

## Overview

The AXI (Agent eXperience Interface) framework establishes 10 ergonomic principles for building CLI tools optimized for AI agent interaction. These principles address token efficiency, schema minimalism, error handling, and context management, enabling agents to operate with higher accuracy and lower token cost compared to traditional CLI and MCP protocols.

## How It Works

AXI's design principles are a systematic response to the inefficiencies and friction inherent in traditional CLI and MCP (Machine Control Protocol) interfaces when used by AI agents. The framework treats the token budget as a primary constraint, recognizing that every token output by a CLI multiplies agent inference cost and can degrade performance. The principles are as follows:

1. **Token-Efficient Output**: AXI mandates the use of TOON (Token-Oriented Object Notation) for CLI output, which achieves approximately 40% token savings over JSON. TOON is a compact, agent-readable tabular format. Internally, tools may use JSON, but conversion to TOON occurs at the output boundary. This reduces both inference cost and context window pressure for agents, enabling more tasks per dollar and faster response times.

2. **Minimal Default Schemas**: AXI tools default to the smallest schema necessary for agent decision-making, typically 3–4 fields per list item. This prevents unnecessary token expenditure (e.g., including verbose metadata or long-form content in lists). Agents can request additional fields explicitly via a `--fields` flag. Default limits are set high enough to cover common cases, minimizing repeated calls for pagination.

3. **Content Truncation**: Large text fields (e.g., issue bodies, descriptions) are truncated by default, with clear size hints and an escape hatch (`--full` flag) for agents to retrieve the complete content. Truncated previews always include the total size, so agents can assess whether further retrieval is warranted. This balances information sufficiency with token economy, avoiding both omission and waste.

4. **Pre-Computed Aggregates**: AXI tools proactively include aggregate counts and derived status fields in output, eliminating the need for agents to make follow-up calls for summary information. For example, list outputs include the total count, not just the page size, and task views summarize related statuses (e.g., "3/3 checks passed"). Only aggregates that can be computed efficiently are included, ensuring responsiveness.

5. **Definitive Empty States**: When a query returns no results, AXI tools explicitly state "0 results" with contextual information, preventing ambiguity and unnecessary agent retries. This principle ensures that agents can reliably interpret the absence of data as a valid outcome.

6. **Structured Errors and Exit Codes**: Errors are output in structured format on stdout, with actionable suggestions, never leaking raw dependency errors or stack traces. Mutations are idempotent: if the desired state already exists (e.g., closing an already closed task), the tool acknowledges and exits with code 0. Non-zero exit codes are reserved for genuine failures. All operations must be flag-completable; interactive prompts are forbidden.

7. **Ambient Context via Session Hooks**: AXI tools self-install into agent session hooks, providing compact dashboards at session start. This ensures agents have relevant state before taking action, improving orientation and reducing redundant queries. Hooks are idempotent, directory-scoped, and token-budget-aware, capturing session lifecycle data for richer future context.

8. **Content First**: Running an AXI tool with no arguments displays live data, not help text, prioritizing actionable information for agents.

9. **Contextual Disclosure**: Each output includes next-step suggestions, guiding agents toward productive follow-up actions.

10. **Consistent Way to Get Help**: Help is concise and available per subcommand, ensuring agents can always retrieve reference information efficiently.

Collectively, these principles create a CLI environment where agents operate with minimal friction, maximal clarity, and optimal token usage. The design is validated by benchmark studies showing AXI tools outperforming both traditional CLI and MCP interfaces in accuracy, cost, and interaction efficiency.

## Key Properties

- **Token Efficiency:** TOON output format reduces token usage by ~40% compared to JSON, directly lowering agent inference costs.
- **Minimal Schemas:** Default list outputs contain only essential fields (typically 3–4), with additional fields available via explicit flags.
- **Structured Error Handling:** Errors are output in structured, agent-readable format with actionable suggestions; idempotent mutations avoid unnecessary failures.
- **Session Hook Integration:** Tools self-install into agent session lifecycle, providing ambient context and capturing session data for richer future state.

## Limitations

AXI principles require backend support for aggregate computation and session hook integration, which may not be feasible in all environments. Truncation limits must be tuned to avoid omitting critical information. Strict adherence to token efficiency may conflict with user expectations for verbose output in some cases. The framework assumes agents can interpret TOON format and structured errors; human users may require additional documentation.

## Example

Example of TOON output for a task list:

```text
tasks[2]{id,title,status,assignee}:
  "1",Fix auth bug,open,alice
  "2",Add pagination,closed,bob
```

Example of structured error handling:

```text
error: --title is required
help: tasks create --title "..." [--body "..."]
```

## Visual

The splash image in the README shows a stylized banner with the phrase 'AXI — Let's build apps agents love.' No technical diagram is present. Benchmark tables in the README visually compare AXI, CLI, and MCP conditions across metrics such as success rate, average cost, duration, and turns.

## Relationship to Other Concepts

- **TOON Format** — AXI mandates TOON as the output format for token efficiency.
- **[[Agent Handoffs in VS Code]]** — Both involve session lifecycle management and agent context.
- **[[The Context Hygiene Principle]]** — AXI's token-budget awareness aligns with context hygiene strategies.

## Practical Applications

AXI principles are applied in agent-facing CLI tools for browser automation (chrome-devtools-axi) and GitHub operations (gh-axi), enabling AI agents to perform tasks with higher accuracy and lower cost. Developers building tools for autonomous agents can use AXI guidelines to ensure ergonomic, efficient, and reliable agent interaction. Benchmark harnesses demonstrate AXI's effectiveness in real-world scenarios, such as CI audits, issue management, and browser task automation.

## Sources

- [[kunchenguid/axi]] — primary source for this concept, deepened 2026-04-22 with benchmark results (490 browser runs, 425 GitHub runs), reference CLI surfaces, TOON spec link
