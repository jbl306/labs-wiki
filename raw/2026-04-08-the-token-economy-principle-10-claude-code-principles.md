---
title: "The Token Economy Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:37:48.427520+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/token-economy/"
content_hash: "sha256:ecc0fd0b3affa22fabead207c580116b4b4886db0c39c4fc54e5ffc85a62b44b"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/token-economy/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:37:47+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/token-economy/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/token-economy/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The Numbers Nobody Mentions
Here are the numbers nobody in your YouTube tutorial mentions:
| Team Size | Token Cost | Effective Output | Efficiency |
| --- | --- | --- | --- |
| 1 agent | 1.0x | 1.0x | 1.00 |
| 3 agents | 3.5x | 2.3x | 0.66 |
| 5 agents | 7.0x | 3.1x | 0.44 |
| 7+ agents | 12.0x+ | 3.0x or less | <0.25 |
Cost vs Output Scaling
Dual-line chart showing how cost scales superlinearly while output peaks around 4 team members then declines, based on DeepMind 2025 data.
0x
2x
4x
6x
8x
10x
12x
Multiplier
1
2
3
4
5
6
7+
Team Size
DEGRADATION
45% Threshold
Cost
Output
Source: DeepMind, 2025
Figure 11: Cost scales superlinearly while output plateaus. Beyond 4 agents, you get less output for exponentially more spend.
A 5-agent team costs you 7x the tokens but produces only 3.1x the output. Your efficiency ratio is 0.44. At 7+ agents, the numbers invert entirely: you are likely getting
less
output than a 4-agent team while paying 12x as much. The marginal agent is not just expensive. It is actively destructive.
This is not a hypothetical. This is DeepMind’s 2025 multi-agent scaling research. Tokens are money. Every API call has a price tag. Every context window consumed is compute burned. And most people are burning it because they never measured.
The instinct to throw more agents at a problem feels right — more workers, more output. But tokens are not labor. They are attention. And attention does not scale linearly. Every agent you add introduces coordination overhead that grows superlinearly with team size. Past a threshold, the team spends more tokens coordinating than producing.
If you have never tracked your token spend per workflow step, you have no idea where your money goes.
## 2. The Principle
Treat tokens, latency, and dollars as first-class engineering constraints. Every workflow includes cost tracking, optimization suggestions, and hard caps. Claude must proactively propose moving fuzzy steps to deterministic tools when they become too expensive.
Most developers treat tokens as an afterthought. They build multi-agent pipelines because it seems sophisticated, add tools and plugins because they might be useful, and let context windows fill up because the limit is high enough that it feels infinite. The bill arrives at the end of the month, and they shrug.
This is the equivalent of a team that never profiles its code. You would not ship a web application without knowing which endpoints are slow. But developers routinely run agentic workflows — workflows that cost real money per execution — without knowing which step consumes the most tokens, which agent contributes the least value, or whether the entire multi-agent setup outperforms a single agent at a fraction of the cost.
The Token Economy Principle says: measure first, optimize second, scale last. The research shows, with uncomfortable clarity, that the default instinct — more agents, more tools, more context — is almost always wrong.
## 3. The Science
This is the economics article. The numbers are precise and the implications are stark.
### DeepMind’s Three Principles of Multi-Agent Scaling (2025)
DeepMind’s 2025 multi-agent scaling research produced three principles that should govern every decision about when and how to scale past a single agent.
Principle 1: Effectiveness depends on task decomposability.
Multi-agent teams only outperform single agents when the task decomposes into independent subtasks with typed interfaces between them. “Independent” is the operative word. If subtasks require frequent back-and-forth — shared state, iterative refinement, sequential reasoning — coordination overhead eats the benefit. On tasks requiring sequential reasoning chains, multi-agent setups degraded performance by 39-70% compared to a single agent. Not “slightly worse.” Catastrophically worse.
Principle 2: Coordination overhead can exceed benefits.
Every agent adds communication cost: messages sent, received, interpreted, acted upon. Shared context synchronized. Conflicts resolved. This overhead grows superlinearly with team size because every new agent must coordinate with every existing agent. Past a threshold, the team spends more tokens coordinating than producing.
Principle 3: Team size saturates at 4.
Diminishing returns start at 3 agents. At 5, the marginal benefit is near zero. At 7+, total effective output degrades — coordination overhead actively harms the team’s output.
### The 45% Threshold
Buried in the data is a finding that deserves its own rule:
if a single well-prompted agent achieves greater than 45% of optimal performance on a task, adding more agents yields diminishing returns.
Run the task with one agent. Measure the output quality. If it clears 45%, the economically correct decision is to optimize the single agent — better prompts, better tools, better context — not to add a second one.
Most tasks clear this threshold easily. The tasks that genuinely benefit from multi-agent coordination are the exception, not the rule.
### The Cascade Pattern
The research points to a clear escalation model:
- Level 0: Single well-prompted agent. Always try this first.
- Level 1: Single agent with tools. Add deterministic tools (Principle 1) before adding agents.
- Level 2: Two agents — a worker and a reviewer. This is the Specialized Review Principle (Principle 6) applied minimally.
- Level 3: Small team, 3-5 agents with defined roles and typed interfaces.
- Level 4: Multi-team with a coordinator agent.
The rule:
never escalate until the current level demonstrably fails.
“Demonstrably” means measured, not felt. If you cannot point to specific output quality metrics showing that Level N is insufficient, you do not move to Level N+1.
Cascade Escalation Levels
Four progressively smaller blocks showing escalation from a single agent to multi-team orchestration, with arrows indicating each step should only occur when measured data justifies it.
Level 0
1 Agent + Tools
Always start here.
Handles 70% of tasks.
Level 1
Worker + Reviewer
Handles 20% more.
Level 2
3-5 Agent Team
Handles 9% more.
Level 3
Multi-Team
Last resort.
<1% of tasks.
Escalate only when measured data justifies it. Do not skip levels.
Figure 12: Start at Level 0. Each escalation requires measured evidence that the current level is insufficient.
### Captain Agent: Adaptive Teams Beat Static Teams (2024)
The Captain Agent research (2024) found that adaptive team composition — dynamically selecting which agents participate based on the task — outperforms static teams by 15-25%. A fixed 5-agent team wastes tokens on agents that contribute nothing to the current task. An adaptive system that selects 2-3 relevant specialists produces better output at lower cost. The task determines the team, not the other way around.
### Attention Budget Economics
The Context Hygiene Principle (Principle 2) established that context is a finite resource. The Token Economy Principle extends this to a dollar amount.
The optimal operating range for context utilization is 15-40% of the available window. Below 15%, the agent lacks sufficient context. Above 40%, attention degradation accelerates and token costs balloon without proportional quality improvement. Every plugin, MCP server, and skill loaded into context consumes tokens simply by existing. If you have 20 tools loaded but use 3 on any given task, you are paying for 17 tools’ worth of dead-weight context that actively degrades attention on the 3 tools that matter.
## 4. Before and After
### Before: The Five-Agent Default
The setup looked impressive on paper. Five agents for every significant task: a planner, a coder, a reviewer, a tester, and an integrator. The YouTube tutorial that inspired it showed all five collaborating to build a feature in minutes. Compelling viewing. Terrible economics.
In practice, the planner generated plans the coder ignored because the task was straightforward. The reviewer’s feedback was marginally useful but cost as much in tokens as the original code generation. The tester wrote inconsistent tests because it lacked the coder’s implementation context. The integrator merged outputs — a task that could have been a deterministic script.
Token costs tripled over three months. Output quality barely improved. The team was spending 7x the tokens for maybe 2x the useful output. And nobody measured. The bill went up, but nobody connected it to specific agents or steps. It was just “AI costs” — a line item that grew every month with no accountability.
### After: Cascade with Measured Escalation
The revised workflow starts at Level 0. Every task begins with a single well-prompted agent with tools (Level 1) — linters, test runners, file operations — but no other agents. For 70% of tasks, this is sufficient. Token cost: 1x.
The remaining 30% escalate to Level 2: a worker agent and a specialized review agent (Principle 6) scoped to the specific concern the task demands. This handles another 20%.
Only the final 10% — genuinely complex tasks with independent, decomposable subtasks — escalate to Level 3 with 3 adaptive agents.
Token spend dropped 60%. Output quality held steady or improved, because single agents at Level 0 operate with clean context windows. The tasks that genuinely needed multi-agent coordination still get it — they just no longer subsidize the 70% that never did.
## 5. Tactical Implementation
Here is how to apply the Token Economy Principle to your workflows, starting with the cheapest intervention and escalating only when the data justifies it.
1. Track token spend per workflow step.
You cannot optimize what you do not measure. Instrument your workflows to log token consumption at each step: planning, code generation, review, testing, integration. Most API providers expose token counts in their responses. The first time you see the numbers, you will find at least one step that consumes a disproportionate share relative to its contribution.
2. Always start with a single well-prompted agent.
Level 0 is the baseline. Before you design any multi-agent workflow, run the task with one agent. Good context, appropriate tools, clear prompt. Measure the output quality. The tasks it cannot handle are your candidates for escalation — everything else stays at Level 0.
3. Apply the 45% threshold.
If the Level 0 output achieves more than 45% of what you need — structurally sound code needing minor refinement, a plan covering most requirements but missing edge cases — the correct move is to improve the single agent, not add a second one. Better prompts, better tools, better context. Escalation is for tasks where the single agent fundamentally cannot produce an adequate result.
4. If you must scale, cap at 3-5 agents with adaptive selection.
Keep the team small. Saturation at 3, degradation past 5. Use adaptive composition: select agents based on the task, not from a fixed roster. A security task gets a coder and a security reviewer. A data pipeline task gets a coder and a testing specialist. The planner agent joins only when decomposition is genuinely needed.
5. Choose topology deliberately.
Sequential subtasks get a pipeline topology. Independent subtasks get parallel topology. Never use a mesh topology (every agent talks to every agent) unless you have measured evidence that it outperforms simpler options. Mesh coordination overhead is quadratic in team size.
6. Set hard caps on team size and token budget.
“No task uses more than 4 agents” is a rule, not a guideline. “Each workflow step has a token budget of X” is an engineering constraint, not a suggestion. Hard caps force optimization — without them, token spend drifts upward because the default instinct is always “add more.”
7. Manage context loading costs.
Every plugin, MCP server, and skill consumes tokens in your context window. If you have 20 tools loaded but use 3 on any given task, you are burning massive context on dead weight — and that dead weight is not free. It competes for attention with the tokens that matter, degrading the quality of the 3 tools you actually use.
jig
(
github.com/jdforsythe/jig
) solves this with project-level configuration files that declare exactly which tools activate per session. Your team checks in the jig config alongside the code, ensuring reproducible, minimal context loading. A frontend task loads frontend tools. A database migration task loads database tools. Nothing else. The context window stays lean, the attention budget stays focused, and you stop paying for tools that contribute nothing to the current task.
8. Encode the economics into your tooling.
These constraints should not live in your head — they should live in your tools. Forge encodes these economics directly: mission-planner will not recommend a 5-agent team unless task decomposition analysis justifies the 7x token multiplier. The 45% threshold is a hard constraint in Forge’s planning logic, not a suggestion. When you ask Forge to assemble a team, it starts at Level 0 and escalates only when the task characteristics — decomposability, interdependency, complexity — warrant the cost. The cascade pattern is built into the tool so you do not have to remember to apply it manually.
## 6. Common Pitfalls
### “More Agents = Better”
The YouTube influencer trap. The demo shows five agents in a flashy terminal display, and the viewer assumes five is always better than one. The data says the opposite past 4. The person who showed you the demo did not show you the token bill, and they did not compare against a single well-prompted agent. If you cannot prove the multi-agent setup outperforms the baseline in output quality — not visual impressiveness — you are paying for theater.
### “Ignoring the Single-Agent Baseline”
The most common failure in multi-agent design is never testing whether a single agent could handle the task. Teams build elaborate coordination systems for tasks that one agent with good tools would solve in a single pass. Before designing any multi-agent workflow, run the task with one agent and measure. This takes minutes. Skipping it can cost months of inflated token bills.
### “Static Teams”
The same 5-agent team for every task. The Captain Agent research showed that adaptive composition outperforms static teams by 15-25%. A static team means every task pays for agents that contribute nothing. A simple refactoring task does not need a security reviewer. A documentation task does not need an integrator. If your team composition does not change based on the task, you are wasting tokens on the agents that sit idle.
### “Ignoring Context Loading Costs”
Invisible, which makes it dangerous. You install 15 MCP servers and 20 skills because they might be useful someday. Each one adds its schema and instructions to your context window. You pay in two ways: direct token cost and indirect quality cost (idle tools compete for attention with the tokens that matter). Audit your loaded tools. Disable everything not needed for the current task.
### “Skipping Cascade Levels”
Jumping from Level 0 straight to Level 3 or 4 because the task “seems complex.” Complexity is not a feeling — it is measurable. Can the task be decomposed into independent subtasks? Do those subtasks have typed interfaces? Does sequential reasoning fail at Level 0? If you cannot answer these questions with data, you are guessing. And guessing almost always overshoots, because the human intuition is to over-estimate complexity and over-provision resources.
## 7. Expected Impact
Token spend reduced 60% with the cascade pattern. Same or better output quality. That is cutting your bill by more than half while maintaining the work product.
The single-agent baseline solved 70% of tasks we had been routing to 3-agent teams. Those tasks never needed multi-agent coordination. They needed a well-prompted agent with appropriate tools. The 3-agent setup was producing equivalent output at 3.5x the cost.
The remaining 30% saw improved quality at Level 2 and Level 3 because agents operated with cleaner context windows. Smaller, focused teams outperform bloated teams not just in economics but in output quality.
The metric that matters: cost per unit of useful output. Not total tokens consumed, not number of agents deployed — how much you pay for each unit of work that ships. Track it weekly.
## 8. Fact Sheet
Principle:
The Token Economy Principle
One-sentence definition:
Treat tokens, latency, and dollars as first-class engineering constraints — measure before scaling, optimize before adding agents, and set hard caps that force efficiency.
The science:
DeepMind’s 2025 multi-agent scaling research shows team effectiveness saturates at 3-4 agents, with 7+ agents producing less output than smaller teams at 12x the cost. Sequential reasoning tasks degrade 39-70% in multi-agent setups.
5 key takeaways:
- A single well-prompted agent handles 70% of tasks that teams over-provision with 3-5 agents
- The 45% threshold: if one agent achieves >45% of optimal, improve the agent before adding more
- Coordination overhead grows superlinearly — every additional agent costs more than the last
- Adaptive team composition outperforms static teams by 15-25% (Captain Agent, 2024)
- Context loading costs are invisible but real — every idle tool degrades attention on active tools
Quick-start checklist:
- Instrument your most expensive workflow to log token consumption per step
- Run your next multi-agent task with a single agent first and measure output quality
- Audit your loaded plugins, MCP servers, and skills — disable everything not needed for the current task
- Set a hard cap: no workflow uses more than 4 agents without measured justification
- Track cost per unit of useful output weekly
The metric to watch:
Cost per unit of useful output — the total token spend divided by the number of tasks completed to an acceptable quality threshold. This number should decrease over time, not increase.
Download Fact Sheet (SVG) →
## 9. What’s Next
You understand the science, the economics, and the discipline. You have learned 9 principles, each backed by research, each battle-tested in real workflows. You know when to pull the LLM out of the loop (Principle 1), how to manage its attention (Principle 2), how to keep its context clean (Principle 3), how to plan and restart without sunk-cost attachment (Principle 4), how to codify institutional memory (Principle 5), how to build specialist reviewers (Principle 6), how to observe your pipelines (Principle 7), where to place human gates (Principle 8), and now how to treat every token as money.
Now it is time to see what happens when you apply all 9 principles to the tools themselves.
Principle 10 is the capstone — and the two open-source tools that make all of this practical. One assembles agent teams using the science from every article in this series. The other ensures your context window loads only what the current task demands. Every design decision in both tools traces directly to the research you have been reading for the past 9 weeks.
The science becomes software. That is next.
<!-- fetched-content:end -->
