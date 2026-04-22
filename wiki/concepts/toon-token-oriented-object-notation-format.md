---
title: "TOON (Token-Oriented Object Notation) Format"
type: concept
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "7ef9072ee6e8f54af2f4e053827cb93014f7a120cab02927398106bd2360e937"
sources:
  - raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
quality_score: 76
concepts:
  - toon-token-oriented-object-notation-format
related:
  - "[[AXI Design Principles for Agent-Ergonomic CLI Tools]]"
  - "[[kunchenguid/axi]]"
tier: hot
tags: [TOON format, token efficiency, agent automation, cli output]
---

# TOON (Token-Oriented Object Notation) Format

## Overview

TOON is a compact, tabular output format designed for agent consumption, offering significant token savings over JSON while maintaining readability and structure. It is central to AXI's token-efficient output principle, enabling agents to parse and act on CLI responses with minimal inference cost.

## How It Works

TOON (Token-Oriented Object Notation) is a specialized output format for CLI tools intended for AI agent interaction. Unlike JSON, which is verbose and includes redundant structural tokens, TOON presents data in a tabular, columnar format that is both human-readable and agent-parseable.

The format consists of a header specifying the collection, row count, and fields, followed by rows of comma-separated values. For example:

```text
tasks[2]{id,title,status,assignee}:
  "1",Fix auth bug,open,alice
  "2",Add pagination,closed,bob
```

This structure eliminates the need for repeated field names and curly braces, reducing the token count by approximately 40% compared to equivalent JSON. TOON is used exclusively at the output boundary; internal logic may operate on JSON or other structures.

TOON supports both lists and detail views, with truncated previews for large fields and explicit size hints. When content is truncated, TOON output includes the total size and a suggestion for retrieving the full content (e.g., `--full` flag). This ensures agents have enough information to decide whether to request additional data.

The format is robust against ambiguity: empty states are explicitly stated (e.g., 'tasks: 0 closed tasks found'), and errors are structured in the same format as normal output. Agents can reliably parse TOON responses, extract actionable data, and avoid misinterpretation caused by mixed progress messages or prompts.

TOON is extensible: additional fields can be requested via CLI flags, and aggregate counts or derived statuses can be included as needed. The format's simplicity and efficiency make it ideal for high-volume, agent-driven automation scenarios.

## Key Properties

- **Token Savings:** TOON reduces token usage by ~40% compared to JSON, directly impacting agent inference cost and context window utilization.
- **Tabular Structure:** Data is presented in columnar format, with headers specifying fields and rows containing comma-separated values.
- **Explicit Empty States:** TOON outputs unambiguous empty results, preventing agent confusion and unnecessary retries.
- **Truncation and Size Hints:** Large fields are truncated with explicit size hints and retrieval suggestions.

## Limitations

TOON requires agents to support parsing of tabular formats; human users may need additional documentation. The format is less flexible for deeply nested or hierarchical data. Truncation must be managed carefully to avoid omitting critical information. Not all CLI tools can easily convert internal data structures to TOON without additional logic.

## Example

Example TOON output for a task list:

```text
tasks[2]{id,title,status,assignee}:
  "1",Fix auth bug,open,alice
  "2",Add pagination,closed,bob
```

Example with truncated content:

```text
task:
  number: 42
  title: Fix auth bug
  state: open
  body: First 500 chars of the issue body...
    ... (truncated, 8432 chars total)
help[1]: Run `tasks view 42 --full` to see complete body
```

## Relationship to Other Concepts

- **[[AXI Design Principles for Agent-Ergonomic CLI Tools]]** — TOON is the mandated output format for token-efficient AXI tools.

## Practical Applications

TOON is used in AXI-compliant CLI tools for browser and GitHub automation, enabling agents to perform tasks with reduced inference cost. Developers can adopt TOON for any agent-facing CLI to optimize token usage and improve agent reliability.

## Sources

- [[kunchenguid/axi]] — primary source for this concept
