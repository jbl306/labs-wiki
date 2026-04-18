---
title: "Custom Copilot CLI Agents"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "3a38e39284cc0602ec33af8d22ef0dfb3c2a3a21b23b03f06716e3221ca8b49e"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-building-4-copilot-cli-custom-agents-4d3f83bc.md
quality_score: 100
concepts:
  - custom-copilot-cli-agents
related:
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents]]"
tier: hot
tags: [copilot-cli, custom-agents, automation, feedback-loop]
---

# Custom Copilot CLI Agents

## Overview

Custom Copilot CLI agents are specialized command-line interface agents built to automate, orchestrate, and optimize workflows across different projects and repositories. They enable tailored operations such as infrastructure management, deployment, machine learning pipeline control, and knowledge curation, enhancing productivity and integration.

## How It Works

Custom Copilot CLI agents are constructed by defining agent archetypes that encapsulate specific domain knowledge and operational tasks. In this session, four distinct agents were built in parallel, each targeting a different repository and functional area:

1. **Homelab Ops Agent**: Manages 13 Docker Compose stacks, includes diagnostic playbooks and safety rules for infrastructure operations.
2. **DevOps Deploy Agent**: Automates deployment scripts and workflows, referencing server details and orchestrating multi-step deployment processes.
3. **NBA-ML Pipeline Agent**: Controls the machine learning pipeline with CLI commands for initialization, ingestion, training, prediction, backtesting, evaluation, and serving.
4. **Knowledge Curator Agent**: Maintains wiki knowledge quality, runs maintenance workflows, applies quality rubrics, and bridges to MemPalace memory architecture.

Each agent is defined in markdown documentation files with detailed commands, operating rules, diagnostic playbooks, and integration points. They are integrated into the repositories' agent persona systems and documented in AGENTS.md files. Feedback loops are implemented via lesson templates to capture agent performance and improvement opportunities.

The agents are validated by a dedicated validation agent that checks file references and command correctness across all agents, ensuring consistency and operational readiness. This validation step is critical before committing and pushing changes to the repositories.

The design balances modularity and integration, allowing agents to operate independently yet share feedback and status information. The agents are intended to be invoked via the Copilot CLI, leveraging the existing infrastructure and workflows of each repository.

## Key Properties

- **Agent Archetypes:** Four archetypes covering infrastructure ops, deployment, ML pipeline, and knowledge curation.
- **Feedback Loop:** Structured feedback via lessons.md templates to iteratively improve agent performance.
- **Validation:** Automated validation checking 44 file references and 29 commands with 4/4 pass rate.
- **Integration:** Agents integrated into AGENTS.md persona tables and repository-specific instruction files.

## Limitations

Agents require manual commit and push steps before becoming active. They depend on accurate documentation and consistent repository structure. Feedback loops depend on user discipline to record lessons. Agents may not cover all edge cases without further refinement and testing in live sessions.

## Example

Example agent persona entry in AGENTS.md:

```markdown
| Agent Name          | Description                          | Commands Count | Operating Rules | Diagnostic Playbooks |
|---------------------|------------------------------------|----------------|-----------------|---------------------|
| homelab-ops         | Manages homelab Docker stacks      | 13             | 10              | 3                   |
| devops-deploy       | Automates deployment workflows     | 8              | 10              | 0                   |
| nba-ml-pipeline     | Controls NBA ML pipeline CLI       | 10             | 10              | 3                   |
| knowledge-curator   | Maintains wiki knowledge quality   | 4              | 10              | 0                   |
```

Validation pseudocode snippet:

```python
def validate_agents(agent_files):
    for file in agent_files:
        check_file_references(file)
        check_cli_commands(file)
    return all_checks_passed

result = validate_agents(['homelab-ops.md', 'devops-deploy.md', 'nba-ml-pipeline.md', 'knowledge-curator.md'])
assert result == True
```

## Visual

No diagrams or images provided in the source document illustrating agent architecture or workflows.

## Relationship to Other Concepts

- **[[Agent-Ergonomic Tool Design Principles]]** — Custom agents follow ergonomic principles to enhance CLI usability.
- **Feedback Loop Mechanisms in Agent Workflows** — Agents incorporate feedback loops for continuous improvement.

## Practical Applications

These custom agents automate complex multi-repo workflows such as infrastructure management, deployment orchestration, ML pipeline control, and knowledge curation. They reduce manual overhead, improve consistency, and enable scalable operations in development and production environments.

## Sources

- [[Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents]] — primary source for this concept
