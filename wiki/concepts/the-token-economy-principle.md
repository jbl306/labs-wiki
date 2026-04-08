---
title: "The Token Economy Principle"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "a5ed6720a8e499fec504f09a5c3ce60d6067385dc5b5038864e2b0f8372284f3"
sources:
  - raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
  - raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
quality_score: 0
concepts:
  - the-token-economy-principle
related:
  - "[[Agent Handoffs in VS Code]]"
  - "[[10 Claude Code Principles | What the Research Actually Says]]"
tier: hot
tags: [llm, cost, scaling, efficiency]
---

# The Token Economy Principle

## Overview

The Token Economy Principle treats tokens as a finite, costly resource and advocates for efficient agent team design. Empirical research shows that adding more agents quickly leads to diminishing returns and runaway costs.

## How It Works

DeepMind’s 2025 multi-agent scaling research quantifies the relationship between agent team size, token consumption, and output. A 5-agent team consumes 7x the tokens of a single agent but produces only 3.1x the output, yielding an efficiency ratio of 0.44. When team size exceeds 7 agents, output can actually decrease compared to a 4-agent team, while costs continue to rise.

The principle prescribes:
- Always starting with a single, well-prompted agent and measuring its performance.
- Escalating to multi-agent setups only when data justifies the additional cost.
- Recognizing the '45% threshold': if a single agent achieves more than 45% of optimal performance, adding more agents yields diminishing returns.

This approach prevents wasteful spending on tokens and infrastructure, and encourages thoughtful, data-driven scaling. It also highlights the importance of prompt quality over agent quantity.

Trade-offs include the potential for slower parallelization in some tasks, but the efficiency and cost savings are significant for most real-world applications.

## Key Properties

- **Cost Efficiency:** Minimizes token usage and associated costs by avoiding unnecessary agent proliferation.
- **Diminishing Returns:** Output gains from additional agents plateau quickly; more agents can even reduce total output.
- **Performance Measurement:** Scaling decisions are based on empirical measurement, not intuition.

## Limitations

May not capture rare cases where large agent teams are justified (e.g., highly parallelizable tasks). Requires robust measurement infrastructure to assess performance accurately.

## Example

A developer starts with a single agent for code review. Only if the agent’s performance is below 45% of the desired outcome does the team add a second agent, avoiding the default use of large, inefficient agent teams.

## Relationship to Other Concepts

- **[[Agent Handoffs in VS Code]]** — Both relate to the orchestration and efficiency of agent teams in coding workflows.

## Practical Applications

Critical for organizations using LLMs at scale, where token costs can be substantial. Guides the design of efficient, cost-effective agentic systems.

## Sources

- [[10 Claude Code Principles | What the Research Actually Says]] — primary source for this concept
- [[The Token Economy Principle | 10 Claude Code Principles]] — additional source
