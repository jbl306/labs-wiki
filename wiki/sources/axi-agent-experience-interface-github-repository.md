---
title: "AXI: Agent eXperience Interface (GitHub Repository)"
type: source
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "7ef9072ee6e8f54af2f4e053827cb93014f7a120cab02927398106bd2360e937"
sources:
  - raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
quality_score: 85
concepts:
  - axi-design-principles-for-agent-ergonomic-cli-tools
  - toon-token-oriented-object-notation-format
related:
  - "[[AXI Design Principles for Agent-Ergonomic CLI Tools]]"
  - "[[TOON (Token-Oriented Object Notation) Format]]"
  - "[[AXI (Agent eXperience Interface)]]"
  - "[[TOON (Token-Oriented Object Notation)]]"
  - "[[gh-axi]]"
  - "[[chrome-devtools-axi]]"
tier: hot
tags: [benchmark, TOON format, session hooks, token efficiency, agent ergonomics, automation, cli design]
---

# AXI: Agent eXperience Interface (GitHub Repository)

## Summary

AXI introduces a new paradigm for agent-native CLI tools, grounded in 10 ergonomic design principles that optimize token efficiency, usability, and agent interaction. The repository includes benchmark harnesses for browser and GitHub automation, demonstrating AXI's superior performance over traditional CLIs and MCP protocols. Detailed guidance and reference implementations are provided for developers building agent-facing tools.

## Key Points

- AXI defines 10 principles for agent-ergonomic CLI design, prioritizing token efficiency and agent usability.
- Benchmarks show AXI tools outperform both traditional CLI and MCP protocols in accuracy, token cost, and interaction efficiency.
- Reference implementations and a skill definition are available to guide developers in building AXI-compliant tools.

## Concepts Extracted

- **[[AXI Design Principles for Agent-Ergonomic CLI Tools]]** — The AXI (Agent eXperience Interface) framework establishes 10 ergonomic principles for building CLI tools optimized for AI agent interaction. These principles address token efficiency, schema minimalism, error handling, and context management, enabling agents to operate with higher accuracy and lower token cost compared to traditional CLI and MCP protocols.
- **[[TOON (Token-Oriented Object Notation) Format]]** — TOON is a compact, tabular output format designed for agent consumption, offering significant token savings over JSON while maintaining readability and structure. It is central to AXI's token-efficient output principle, enabling agents to parse and act on CLI responses with minimal inference cost.

## Entities Mentioned

- **[[AXI (Agent eXperience Interface)]]** — AXI is a framework and set of ergonomic standards for building CLI tools optimized for AI agent interaction. It defines 10 principles that prioritize token efficiency, usability, and structured output, validated by benchmark studies and reference implementations.
- **[[TOON (Token-Oriented Object Notation)]]** — TOON is a compact, tabular output format designed for agent consumption, offering significant token savings over JSON. It is central to AXI's token-efficient output principle.
- **[[gh-axi]]** — gh-axi is a reference AXI implementation for GitHub operations, providing agent-native CLI functionality with token-efficient output and ergonomic design.
- **[[chrome-devtools-axi]]** — chrome-devtools-axi is a reference AXI implementation for browser automation, providing agent-native CLI functionality with token-efficient output and ergonomic design.

## Notable Quotes

> "AXI is a new paradigm — agent-native CLI tools built from 10 design principles that treat token budget as a first-class constraint." — README
> "Use TOON format for ~40% token savings over JSON." — README
> "Every operation must be completable with flags alone. If a required value is missing, fail immediately with a clear error — don't prompt for it." — AXI Skill Definition

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-httpsgithubcomkunchenguidaxi.md` |
| Type | repo |
| Author | Kun Chen |
| Date | Unknown |
| URL | https://github.com/kunchenguid/axi |
