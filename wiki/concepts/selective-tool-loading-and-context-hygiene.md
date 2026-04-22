---
title: "Selective Tool Loading and Context Hygiene"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "db7bbe28e5c6cd6654d03bbd74fe141b54ef9afb68018a4e7d641d5c7c9ab59e"
sources:
  - raw/2026-04-08-the-toolkit-principle-10-claude-code-principles.md
quality_score: 75
concepts:
  - selective-tool-loading-and-context-hygiene
related:
  - "[[The Context Hygiene Principle]]"
  - "[[The Token Economy Principle]]"
  - "[[The Toolkit Principle | 10 Claude Code Principles]]"
tier: hot
tags: [context-hygiene, tool-loading, ai-workflows, token-economy]
---

# Selective Tool Loading and Context Hygiene

## Overview

Selective tool loading is an operationalization of the Context Hygiene Principle, ensuring that only the tools, agents, and skills relevant to a specific task or project are loaded into an AI system's context. This minimizes context drift, reduces token consumption, and maximizes model performance by focusing attention on what matters.

## How It Works

In large, extensible AI environments, it is common for users to install numerous plugins, agents, and skills—many of which are only relevant to specific projects or workflows. Without selective loading, every session incurs a 'context tax,' as irrelevant tool definitions consume valuable tokens and dilute the model's attention, actively degrading performance on the tokens that matter.

Selective tool loading addresses this by decoupling installation from activation. Tools are installed broadly, but only activated per project or session according to a versioned profile. For example, the open-source CLI tool 'jig' enables users to define profiles in a '.jig/profiles/' directory, specifying which tools, MCP servers, skills, and settings are active for each project. When a session is launched with a given profile, only the declared tools are loaded, while others remain dormant.

This approach is deeply integrated with version control (e.g., git), so that tool profiles are checked in alongside code, ensuring that every developer on a team has the same context for a given project. This eliminates 'it works on my machine' discrepancies and makes tool configuration reproducible, reviewable, and diffable.

Selective loading is also session-type aware. For example, a code review session might load only the reviewer agent, security specialist, and lint server, while a planning session loads the mission planner and researcher. Each configuration is a deliberate decision about what context the model needs, rather than a default kitchen-sink approach.

By making context hygiene a structural property of the workflow, rather than a manual discipline, selective tool loading ensures that attention budgets are maximized for the actual task at hand. It also provides observability, as changes to profiles are visible in pull requests and can be audited for appropriateness.

## Key Properties

- **Context Minimization:** Only relevant tools are loaded per session, reducing token consumption and improving model focus.
- **Reproducibility:** Profiles are versioned and checked into git, ensuring consistent tool context across teams and environments.
- **Observability:** Profile changes are reviewable and auditable, making tool loading decisions transparent.
- **Session-Type Awareness:** Different profiles can be defined for code review, planning, writing, etc., each with a tailored tool set.

## Limitations

Selective tool loading requires upfront investment in profile configuration and ongoing maintenance as projects evolve. If profiles are not kept up to date, relevant tools may be omitted or irrelevant ones included, undermining the benefits. The approach also assumes that all tools can be cleanly decoupled and that dependencies are well understood. In highly dynamic or exploratory environments, rigid profiles may constrain flexibility.

## Example

A backend API project defines a profile that loads database tools, testing frameworks, and an API design skill. When a developer runs 'jig run backend-api', only these tools are active, and all others are dormant. The profile is checked into git, so every developer has the same setup.

## Relationship to Other Concepts

- **[[The Context Hygiene Principle]]** — Selective tool loading is a direct implementation of context hygiene, minimizing unnecessary context.
- **[[The Token Economy Principle]]** — By reducing unused tools in context, selective loading optimizes token usage and cost.

## Practical Applications

Selective tool loading is essential in organizations with large libraries of AI tools, ensuring that each project or workflow only incurs the context cost of what it actually needs. It is particularly valuable in multi-agent environments, regulated industries, and teams with diverse, project-specific requirements.

## Sources

- [[The Toolkit Principle | 10 Claude Code Principles]] — primary source for this concept
