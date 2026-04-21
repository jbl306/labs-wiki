---
title: "10 Claude Code Principles | What the Research Actually Says — 10 evidence-based principles for production-grade agentic workflows"
type: url
captured: 2026-04-08T01:35:22.351076+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/overview/"
content_hash: "sha256:3f11a7d0a6d862d26233994fb222afef9aadd8f2a63a5f2c7ac7d39e8dcc20b6"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/overview/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-20T23:20:14+00:00
- source_url: https://jdforsythe.github.io/10-principles/overview/
- resolved_url: https://jdforsythe.github.io/10-principles/overview/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
Most AI coding advice is wrong. Not “slightly suboptimal” wrong — measurably, scientifically, provably wrong.
You’ve been told to write detailed system prompts with exhaustive instructions. Research shows that at 19 requirements, accuracy is
lower
than at 5. You’ve been told to use flattery — “You are the world’s best programmer” — to get better output. The PRISM persona research framework shows that flattery degrades output quality. You’ve been told that more agents means better results. DeepMind’s 2025 multi-agent scaling data shows that 7+ agents makes your team
worse
than a team of 4.
Every week, a new tutorial drops claiming to unlock “10x productivity” with some elaborate agent setup. Every week, a developer follows it, burns through tokens, gets mediocre output, and concludes that AI coding tools are overhyped. The tools aren’t the problem. The advice is.
This series is about what the research actually says — and how to build workflows that hold up in production, not just in demos.
## The Meta-Argument: Vibes vs. Science
There are two ways to develop AI-assisted coding workflows. The first is vibes: try things, see what feels right, copy what worked for someone on YouTube. The second is science: read the papers, understand the mechanisms, build on evidence.
Most of the community runs on vibes. That’s not an insult — it’s the natural state of a field moving this fast. When the tools change every month, who has time to read papers? You ship what works today and hope it keeps working tomorrow.
The problem is that vibes-based workflows are fragile. They work until they don’t, and when they break, you have no mental model for
why
they broke. You can’t debug a process you don’t understand. You can’t optimize a system you built on intuition alone.
I’ve been doing this wrong for months. I built agent pipelines that were impressive in demos but flaky in production. I wrote system prompts that were novels when they should have been postcards. I spun up multi-agent teams for tasks a single well-prompted agent could handle. And I didn’t know why any of it was failing until I started reading the research.
What I found was a body of peer-reviewed work — from Anthropic, DeepMind, MIT, and independent researchers — that explains the mechanisms behind what works and what doesn’t. Not opinions. Not “best practices” from someone with a Twitter following. Actual measured results with confidence intervals.
This series distills that research into 10 actionable principles. Each principle is grounded in published science, tested in real production workflows, and written for developers who build things — not developers who watch tutorials about building things.
## The 10 Principles
### Principle 1: The Hardening Principle
Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool.
Claude is an extraordinary prototyping partner. It can take a vague idea and turn it into a working pipeline in minutes. But “working” and “reliable” are different things. LLMs are probabilistic — same input, different output. For steps that need identical behavior every time, that’s a liability. The Hardening Principle says: use the LLM to prototype, then harden the deterministic parts into real tools. Hardened workflows go from “it worked yesterday” to 100% reliability. The LLM stays in the loop for what it’s good at — intent interpretation and fuzzy reasoning — and gets pulled out of everything else.
### Principle 2: The Context Hygiene Principle
Context is your scarcest resource. Treat it like memory in an embedded system, not disk space on a server.
Liu et al. (2024) measured something that should change how every developer structures their prompts: when critical information is placed in the middle of a long context rather than at the beginning or end, accuracy drops by more than 30%. This is the “Lost in the Middle” effect, and MIT researchers (Wu et al., 2025) traced it to architectural causes in the transformer itself. Context hygiene isn’t about minimalism for its own sake. It’s about understanding that every token competes for the model’s finite attention budget — and unfocused context actively degrades output quality.
### Principle 3: The Living Documentation Principle
Documentation is context. Stale documentation is poisoned context.
One stale line in a markdown file — an outdated instruction about preferring
`Array<T>`
over
`T[]`
— triggered cascading ESLint violations that took days to trace. The agent wasn’t hallucinating. It was faithfully following instructions that were wrong. Your documentation IS the few-shot context the model uses to generate code. When docs rot, the model’s output rots with them. Living documentation means structured, machine-readable formats with automated freshness checks — because documentation entropy is the default state.
### Principle 4: The Disposable Blueprint Principle
Never implement without a saved, versioned plan artifact. And never fall in love with one.
MetaGPT research (Hong et al., 2023) found that teams using structured artifacts had approximately 40% fewer errors than those using free dialogue. Plans externalized to files survive
`/clear`
commands perfectly — no context degradation, no information loss. The Disposable Blueprint Principle says: brainstorm, deepen, archive the blueprint, then implement against it. If execution goes off the rails, kill the branch, refine the blueprint, and restart cleanly. Your capital as a developer belongs in planning, not in code you’re afraid to delete.
### Principle 5: The Institutional Memory Principle
When an agent makes a mistake, don’t just correct it — codify it forever.
LLMs gravitate toward the center of their training distribution — the most generic, average version of any output. Negative constraints (“never use
`Array<T>`
BECAUSE our ESLint config enforces
`T[]`
”) literally steer the model away from that generic center into more specific, project-appropriate territory. This isn’t just a guardrail — it’s a steering mechanism. An “always/never” list with reasons becomes institutional memory that prevents the same mistake across every session, every developer, and every agent on the team. The CHI 2023 paper “Why Johnny Can’t Prompt” confirmed: combined positive instruction with negative constraint is the strongest approach.
### Principle 6: The Specialized Review Principle
A generalist reviewer trends toward the median. Specialists find what generalists can’t.
PRISM persona research revealed something counterintuitive: brief identities under 50 tokens produce higher-quality outputs than elaborate 200+ token persona descriptions. Flattery — “You are the world’s best programmer” — actively degrades quality by activating motivational and marketing text in the training data instead of technical expertise. Real job titles activate real knowledge clusters. A reviewer defined as “senior site reliability engineer” in 30 tokens outperforms one defined with three paragraphs of flattering backstory. The implication: build a panel of tightly-scoped specialists, not one omniscient generalist.
### Principle 7: The Observability Imperative
If you can’t see inside your pipeline, you’re trusting it on faith.
The MAST failure taxonomy documents 14 distinct failure modes in multi-agent systems, organized into three categories: communication failures, coordination failures, and quality failures. Message loss. Misinterpretation. Deadlock. Role confusion. Error cascading. Most of them are completely invisible without structured logging. MetaGPT’s structured artifact approach doesn’t just reduce errors — it creates an inherent audit trail where the sequence of artifacts tells the full story. Without observability, your pipeline could be failing in six different ways right now, and you wouldn’t know until the final output is obviously, catastrophically wrong.
### Principle 8: The Strategic Human Gate Principle
Rubber-stamp approval is the single most common quality failure in multi-agent systems.
That’s not an opinion — it’s MAST failure mode FM-3.1, the most frequently observed quality failure in the taxonomy. LLMs are sycophantic by default. They trend toward agreement. A review agent with a weak prompt will say “LGTM” to a hardcoded API key, a SQL injection, a race condition — not because it can’t see the problem, but because approving is the path of least resistance in its training distribution. Strategic human gates at 2-3 high-stakes decision points (plan finalization, tool hardening, major refactors) catch what automated review misses. The key word is
strategic
— too many gates and you become the bottleneck; too few and mistakes propagate unchecked.
### Principle 9: The Token Economy Principle
Tokens are money. Most people are burning it.
DeepMind’s 2025 multi-agent scaling research produced a table that should be pinned above every developer’s monitor: a 5-agent team costs 7x the tokens of a single agent but produces only 3.1x the output. That’s an efficiency ratio of 0.44. At 7+ agents, you’re likely getting
less
output than a 4-agent team while paying 12x as much. The data also shows a “45% threshold” — if a single well-prompted agent achieves more than 45% of optimal performance on a task, adding more agents yields diminishing returns. Always start with one agent. Measure. Escalate only when the data justifies the cost.
### Principle 10: The Toolkit Principle
Knowledge without automation decays. Encode your principles into tools that enforce them automatically.
Everything above — all 9 principles, all the research, all the battle scars — means nothing if it lives in your head and fades after two weeks. The Toolkit Principle is Principle 1 (Hardening) applied recursively: if you follow a workflow manually, eventually you forget a step. If the workflow is encoded in a tool, it runs the same way every time. This article series ships alongside two open-source tools built on the same science:
Forge
(
github.com/jdforsythe/forge
), a Claude Code plugin for assembling science-backed specialist agent teams, and
jig
(
github.com/jdforsythe/jig
), a session profile manager that loads only the tools each project needs. Every design decision in both tools traces to the published research covered in this series. Full walkthrough in Principle 10.
## The Narrative Arc
This series isn’t a random collection of tips. It’s a progressive argument built in four acts.
Act I — Foundations (Principles 1-3):
How to think about LLM reliability, context, and documentation. These are the mental models that everything else builds on. If you understand why context is finite, why position matters, and why stale docs are actively harmful, every subsequent principle will feel obvious rather than arbitrary.
Act II — Execution Discipline (Principles 4-6):
How to plan, remember, and review. With the foundations in place, these principles govern the daily workflow: externalize your plans, codify your mistakes, and build specialist reviewers instead of trusting generalists.
Act III — Governance and Safety (Principles 7-9):
How to observe, gate, and economize. These principles protect you from the failure modes that emerge at scale: invisible pipeline failures, rubber-stamp approvals, and runaway token costs.
Act IV — Capstone (Principle 10):
How to encode it all into a reusable toolkit. The final article connects every principle to open-source tools you can install and use. The science becomes software.
Each article links to the next. Each principle builds on the ones before it. You can read them out of order — each stands alone — but the full series tells a single story about moving from fragile, vibes-based AI workflows to production-grade systems backed by evidence.
## The Series
Each article covers the science behind the principle, a real-world before/after, tactical implementation steps you can use immediately, common pitfalls, and measurable outcomes.
If you’ve ever had a session degrade after 30 messages, been frustrated by an agent repeating a mistake you fixed last week, or watched a review agent approve obviously broken code — this series explains why, with citations, and gives you a concrete path forward.
Principle 1 is the place to start: knowing when to pull the LLM out of the loop entirely. A meeting transcription pipeline that went from “it worked yesterday, maybe” to 100% reliability — and the general pattern that applies to any fuzzy workflow you’re fighting with today.
<!-- fetched-content:end -->
