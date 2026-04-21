---
title: "The Toolkit Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:38:18.226087+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/toolkit/"
content_hash: "sha256:150b1388be4f1388aa85f2ef62c08645ead1416adef2db057b5309a28cce933a"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/toolkit/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T03:05:03+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/toolkit/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/toolkit/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## The Accidental Forge
I set out to build a meta-skill — a single Claude Code skill that creates other skills. Simple enough, right?
I started with a system prompt. The generated skills were functional but generic — they read like someone had skimmed a blog post about the domain rather than lived in it for a decade. So I added vocabulary routing based on Ranjan et al.’s embedding space research: 15-30 precise domain terms per skill, the kind a 15-year practitioner would use with a peer. Output quality jumped immediately.
Then I realized the persona definitions were too long — 150-token identity blocks full of flattery and backstory. PRISM’s research showed accuracy damage scales with persona length — shorter causes less degradation, under 50 tokens is the practical sweet spot. Ranjan et al.’s vocabulary routing research explained why flattery backfires: superlatives route to motivational content, not expertise. Real job titles. No “world-renowned expert” nonsense.
Then I realized the skill had no way to decide when a task needed one agent versus a team. So I integrated DeepMind’s 2025 scaling laws — the 45% threshold, the saturation point at 4 agents, the cascade pattern that says never escalate until the current level demonstrably fails.
Then I realized review agents were rubber-stamping everything. So I added the MAST failure taxonomy — 14 documented failure modes, with FM-3.1 (rubber-stamp approval) as the primary quality gate to detect and prevent.
By the time I was done, the “meta-skill” had become an entire system — four meta-skills, three infrastructure agents, a library of domain specialists, and 90KB of research documentation. I had accidentally built a forge.
This article is about what happens when you apply Principle 1 to your own workflow. When you take the same hardening discipline you use on flaky pipelines and point it inward — at the process of building AI tools itself. The result is not an article. It is a toolkit. And a toolkit is what turns knowledge into lasting capability.
## Part A: The Toolkit Philosophy
You have learned nine principles across this series. Each is backed by published research. Each is tested in production. And each will fade from your practice within two weeks if you try to follow them manually.
This is not a motivation problem. It is a systems problem. Knowledge stored in your head competes with every other demand on your attention. You will remember to use vocabulary routing on Monday. By Thursday, under deadline pressure, you will write “review the security” instead of “OWASP Top 10 audit with STRIDE threat modeling.” By the following Monday, the habit is gone. The research you read is still valid. Your implementation of it has decayed.
The Toolkit Principle: encode your principles into tools that enforce them automatically. Knowledge without automation decays. Automation without knowledge is dangerous. The toolkit is where knowledge becomes durable.
This IS Principle 1 — the Hardening Principle — applied recursively. Principle 1 says every fuzzy LLM step that must behave identically every time should become a deterministic tool. The Toolkit Principle says that applies to the process of building and managing AI tools themselves. If you are manually remembering to add vocabulary payloads to your skills, you have a fuzzy workflow. If a tool adds them for you because it encodes the research that says vocabulary is the primary quality lever, you have a hardened workflow.
What goes in a toolkit? Skills — reusable prompt packages that encode expert knowledge for specific domains. Custom agents — specialist definitions with vocabulary routing, anti-patterns, and structured deliverables. MCP servers — deterministic tools that handle mechanical execution. Prompt templates — proven structures that position information for optimal attention. Automation scripts — CI/CD enforcement that catches drift before it ships.
The meta-narrative of this series is straightforward: these articles teach you to harden fuzzy workflows. Forge is what happened when I applied that lesson to my own workflow for building AI tools. My first version was just a long system prompt — a single monolithic skill definition that tried to be everything. PRISM research showed me why that was routing to the distribution center. DeepMind’s scaling data showed me when to use one agent versus a team. The MAST taxonomy showed me why my review agents were useless. Each research finding demanded a structural change, and each structural change pushed the system further from “system prompt” toward “toolkit.”
The rest of this article walks through that toolkit: what it contains, why each piece exists, and how to build your own.
## Part B: Forge — Science-Backed Agent Assembly
Forge (
github.com/jdforsythe/forge
) is an open-source system for assembling AI agent teams grounded in published research. We open-sourced it alongside this series because we think you should see how the research translates into implementation. The bibliography is the product. The code is the implementation.
Install:
```
claude plugin marketplace add jdforsythe/forge
claude plugin
install
forge
```
### The Architecture
Four meta-skills
handle the core workflow:
Mission Planner
analyzes your goal and determines the right level of complexity. It enforces the cascade pattern from Principle 9: always start at Level 0 (single well-prompted agent) and escalate only when the current level demonstrably fails. The 45% threshold from DeepMind’s scaling research is a hard constraint — if a single agent can achieve more than 45% of optimal performance on the task, the Mission Planner will not recommend a team. It decomposes goals into subtasks, identifies dependencies between them, and recommends composition only when the task genuinely demands it.
Agent Creator
generates agent definitions that encode the science from Principles 5 and 6. Every agent gets vocabulary routing — 15-30 precise domain terms selected to pass the 15-year practitioner test. Identities stay under 50 tokens, using real job titles instead of flattery. Each agent receives an anti-pattern watchlist drawn from the MAST failure taxonomy — 5-10 named failure modes with detection signals and resolution steps. Deliverables are typed and structured, making every handoff verifiable.
Skill Creator
builds reusable skill packages following the evidence-based framework synthesized from the research (detailed in Part E). It enforces progressive disclosure, dual-register descriptions, evaluation criteria separated from generation, and the attention-optimized section ordering that puts vocabulary first and retrieval anchors last.
Librarian
manages the health of the agent and template library. It detects stale items — agents whose vocabulary has drifted from current domain usage, templates that reference deprecated patterns, definitions that overlap in ways that create ambiguous triggering. It recommends consolidation when two agents cover the same territory and flags items that have not been used or updated in configurable time windows.
Three infrastructure agents
support the meta-skills:
Verifier
validates agent definitions against schemas — deterministic checks that Principle 1 says should never be left to an LLM. Does the definition include a vocabulary payload? Is the identity under 50 tokens? Binary checks. Code handles them.
Researcher
gathers context before agent creation begins. It reads your CLAUDE.md, scans codebase structure, and identifies domain context the agents will need. Principle 2 in action — loading relevant context rather than forcing the Agent Creator to guess.
Reviewer
applies the Specialized Review Principle to Forge’s own output. The agent that creates other agents cannot reliably evaluate its own work (Anthropic harness design research, March 2026). The Reviewer has its own evaluation criteria, weighted toward vocabulary specificity, anti-pattern coverage, and identity conciseness.
The library
includes 11 domain agents across three verticals:
- Software: Product Manager, Architect, Lead Engineer, QA Engineer
- Marketing: Campaign Strategist, Content Creator, Designer, Analytics Lead
- Security: Lead Auditor, Penetration Tester, Compliance Analyst
And 3 team templates: SaaS product team, marketing campaign, and security audit. Each template defines not just which agents to include but the topology (pipeline, parallel, or hub-and-spoke), the handoff interfaces between agents, and the cascade level that justifies the team size.
### Methodology Mapping
Every methodology principle in Forge maps directly to a principle in this series:
| Forge Methodology | Series Principle | What It Enforces |
| --- | --- | --- |
| Vocabulary Routing | P6 (Specialized Review) | 15-30 expert terms per agent, 15-year practitioner test |
| Real-World Roles | P6 (Specialized Review) | <50 token identities, real job titles, no flattery |
| Scaling Laws | P9 (Token Economy) | 45% threshold, saturation at 4, cascade pattern |
| Anti-Pattern Principle | P5 (Institutional Memory) | 5-10 named failure modes with detection signals per agent |
| Progressive Disclosure | P2 (Context Hygiene) | Layered context loading, attention budget management |
| Structured Artifacts | P7 (Observability) | Typed deliverables, verifiable handoffs, audit trails |
### Live Walkthrough: “Plan a security audit for a SaaS API”
Here is what happens when you give Forge a real goal.
Step 1 — Mission Planner decomposes the goal.
The planner identifies three distinct workstreams: infrastructure review (network configuration, access controls, secrets management), application security testing (OWASP Top 10, API-specific vulnerabilities, authentication flows), and compliance assessment (regulatory requirements, data handling, audit trail verification). It notes that these workstreams have low interdependency — the infrastructure review does not block the application testing — which means parallel execution is appropriate. The cascade analysis recommends Level 3: a small team of 3-4 agents, justified by the distinct expertise domains.
Step 2 — Agent Creator builds the specialists.
For the Lead Auditor, the vocabulary payload includes terms like “attack surface enumeration,” “lateral movement paths,” “defense-in-depth layering,” “NIST 800-53 control families,” and “compensating controls.” The identity is 38 tokens: “Senior security auditor with 15 years of experience in cloud infrastructure security assessments for SaaS platforms.” No flattery. No “world-class expert.” The anti-pattern watchlist includes “checkbox compliance” (auditing to a checklist without understanding the threat model), “scope creep into penetration testing” (the auditor’s job is to assess, not to exploit), and “severity inflation” (marking everything as critical dilutes actual critical findings).
Step 3 — Structured artifacts define the handoffs.
Each deliverable is typed: a Findings Report with severity classifications and remediation recommendations, a Vulnerability Assessment with reproduction steps and CVSS scores, a Gap Analysis mapping current state against regulatory requirements. Typed deliverables make every handoff verifiable — the Reviewer can check that a Findings Report contains severity classifications, not just prose.
Step 4 — The Reviewer evaluates the team design.
Before the team executes, the Reviewer checks: Is the vocabulary specific enough to route past the distribution center? Are the anti-patterns drawn from the security domain, not generic project management? Do the deliverable types create a complete picture when combined? Feedback loops back to the Agent Creator for refinement.
The entire process takes one conversation. The output is a set of agent definitions and a team template that can be reused, versioned, and refined. The science is invisible to the user. It is embedded in the tools.
## Part C: jig — Intelligent Context Utilization
You now have Forge, plus specialist review agents, plus MCP servers for linting and testing, plus custom skills for your domain. That is a lot of tools. And every one of them consumes tokens just by existing in your context.
### The Problem
Without management, every Claude session loads ALL your installed plugins, MCP servers, skills, and hooks. Twenty tools installed, three needed — seventeen injecting definitions into your system prompt for zero value. The research from Principle 2 is unambiguous: every irrelevant token actively degrades performance on the tokens that matter. You have spent nine articles learning to keep context focused, and then your tool loading strategy undermines it before you type your first prompt.
This is kitchen-sink context loading applied to the tool layer — the exact kind of fuzzy workflow that Principle 1 says should be hardened.
jig (
github.com/jdforsythe/jig
) is an open-source CLI for selective tool loading. We open-sourced it alongside this series because the problem is universal: anyone with more than a handful of Claude Code extensions is paying a context tax on every session.
### How It Works
The workflow is straightforward:
- Install tools broadly. Add every plugin, MCP server, skill, and hook that you might need across all your projects. Forge’s agents. Your company’s custom skills. Third-party MCP servers for databases, APIs, documentation. Do not hold back — install them all.
- Create profile files in `.jig/profiles/` per project. Each profile declares which tools, MCP servers, skills, and settings activate for that project. A backend API project loads database tools, testing frameworks, and your API design skill. A frontend project loads component libraries, accessibility checkers, and your design system skill. A documentation project loads your writing skill and grammar checker. Different projects, different tools, different context profiles.
- jig activates only what the profile specifies. Run `jig run your-profile` and jig launches Claude Code with only the declared tools, MCP servers, and skills active. Everything else stays dormant — installed but not consuming tokens.
- Profiles are checked into git. This is critical. The `.jig/profiles/` directory is versioned alongside your code, which means every developer on the team gets the same tool context for the same project. No more “it works on my machine because I have different plugins loaded.” The tool configuration is reproducible, reviewable, and diffable.
### Session-Type Examples
The same developer, on the same machine, with the same installations — but radically different context profiles:
Code review session:
Load Forge’s reviewer agent, the security specialist, the performance specialist, and your lint MCP server. Total context cost: the definitions for 4 focused tools. Everything else — the planning skills, the documentation tools, the deployment scripts — stays dormant.
Planning session:
Load Forge’s mission-planner, the researcher agent, and your documentation MCP server. The review agents are not needed. The deployment tools are not needed. Context stays lean.
Writing session:
Load your content skill and grammar checker. That is it. Two tools. Maximum attention budget available for the actual writing task.
Each configuration represents a deliberate decision about what context the model needs for a specific type of work. Deliberate context beats default context every time.
### How jig Connects to the Principles
Principle 2 (Context Hygiene):
jig operationalizes the most actionable recommendation from Principle 2 — audit your loaded tools and disable what you are not using. Instead of auditing manually every session, jig makes the audit a one-time configuration decision per project.
Principle 7 (Observability):
jig profiles are versioned system state. When you diff a profile change in a PR, you can see exactly what tools were added or removed and review whether the change is appropriate. Your tool loading decisions become auditable artifacts.
Principle 9 (Token Economy):
Every unused tool in context is a silent cost. jig eliminates that cost structurally — not by asking developers to remember to disable tools, but by making the default state “only what is declared.” The optimization is automatic.
## Part D: How Forge and jig Work Together
Forge creates tools. jig manages their context footprint. Together, they form a closed loop that operationalizes all nine principles.
Design with Forge.
Need a database migration reviewer or an accessibility auditor? Forge creates it with vocabulary routing, PRISM-compliant identities, MAST-informed anti-patterns, and structured deliverables. Grounded in research from the moment of creation. No manual research required.
Manage with jig.
The new agent gets added to jig profiles for relevant projects only. A database migration reviewer loads in backend projects, not frontend. An accessibility auditor loads in frontend, not infrastructure. Each project maintains a minimal, focused tool set.
Review with specialists.
Domain experts, not generalists. The security reviewer uses OWASP vocabulary. The performance reviewer uses Big-O and query plan vocabulary. Each covers a distinct angle with visible scope boundaries.
Observe with structured artifacts.
Every handoff between agents is a typed deliverable, not a conversation. The Architect hands the Lead Engineer a structured design document with defined fields. That artifact is the audit trail.
Gate with human approval.
The cascade pattern requires validation before escalating. The human reviews whether the single-agent approach was genuinely insufficient before the Mission Planner recommends a team. Strategic gates at high-stakes decisions — not checkpoints at every step.
The full mapping across all nine principles:
- P1 (Hardening): Forge is the hardened version of “manually design agents from research papers”
- P2 (Context Hygiene): jig enforces minimal tool loading per session
- P3 (Living Documentation): Forge’s research docs and methodology are versioned, structured, and machine-readable
- P4 (Disposable Blueprint): Mission Planner outputs are versioned team blueprints — disposable by design
- P5 (Institutional Memory): Anti-pattern watchlists encode past failures into every agent definition
- P6 (Specialized Review): Vocabulary routing and PRISM identities produce genuine specialists
- P7 (Observability): Typed deliverables create inherent audit trails
- P8 (Strategic Human Gate): Cascade validation requires human sign-off before escalation
- P9 (Token Economy): The 45% threshold and team-size cap prevent runaway costs
Nine principles. Two tools. One workflow.
## Part E: The Skill Design Framework
For readers who want to build their own skills — not just use Forge’s library — here is the evidence-based framework distilled from the research cited across this entire series.
### The DOs
1. Expert vocabulary as the primary quality lever.
15-30 precise domain terms per skill. “OKLCH tinted neutrals” routes to color science; “nice colors” routes to blog posts. Vocabulary determines which region of the model’s knowledge activates (Ranjan et al., 2024). This is the single highest-leverage intervention.
2. Dual-register descriptions.
Every description works in two registers: expert terminology that activates deep knowledge, and natural language that triggers on plain queries. Formal-only descriptions undertrigger. Casual-only descriptions produce generic output.
3. Named anti-patterns with detection and resolution.
5-10 per skill, each with a detection signal, resolution step, and prevention principle. Anti-patterns are routing signals, distribution-center escapes, and proactive guardrails simultaneously. “Bikeshedding (Parkinson’s Law of Triviality)” is a stronger signal than “spending too much time on small things.”
4. Imperative, structured, conditional instructions.
Ordered steps with explicit IF/THEN conditions. Vaarta Analytics (2026) found that structured atomic checks dramatically reduced false negatives versus free-text instructions. “Classify the decision tier based on reversibility and blast radius” has one interpretation. “Try to figure out the tier” has many.
5. 2-3 diverse canonical examples.
LLMs pattern-match against examples more reliably than they follow verbal rules. LangChain (2024) found 3 examples often match 9 in effectiveness. Use BAD versus GOOD pairs. Place the most representative example last for recency bias.
6. Progressive disclosure.
Three layers: metadata always in context (~100 tokens), SKILL.md body loaded when triggered (<500 lines), and
`references/`
loaded on demand. Heavy content belongs in references, not in the main skill file.
7. Pushy descriptions.
Current models undertrigger. Include both domain terms and user scenarios. Include synonyms, variations, and explicit exclusions for when the skill should NOT fire.
8. Filesystem context reading.
Skills should read CLAUDE.md, config files, and existing conventions rather than defaulting to generic patterns. Project-specific signals eliminate guessing.
9. Separated generation and evaluation.
Evaluation criteria in a separate section, weighted, phrased as gradable questions. “Can the user identify the most important metric in under 3 seconds?” is testable. “Is the design good?” is not. Deterministic verification first, LLM evaluation second.
10. Right-altitude prompting.
Balance between brittle over-specification and vague under-specification. “Use
`var(--spacing-md)`
for standard element gaps” names the token without dictating application. At n=19 requirements, accuracy drops below n=5. More specificity is not always better.
### The DON’Ts
1. No generic consultant-speak.
“Best practices,” “leverage,” “synergy” route to the most generic advice in the distribution. Use precise terms.
2. No over-prompting.
Restating instructions “for emphasis” wastes attention budget. At n=19 requirements, accuracy drops below n=5 due to competing constraints (underspecification research, 2025). State each instruction once.
3. No flattery-based personas.
“World-renowned expert” activates motivational text, not expertise. Define competence through domain knowledge, not adjectives.
4. No positive-only instructions.
Without negative constraints, the model gravitates to the distribution center. Without anti-pattern detection, the skill cannot notice when the user is heading toward a known failure mode.
5. No flagging without fixing.
“Warning: this may be bikeshedding” is noise. Use the full Detect, Name, Explain, Resolve, Prevent pattern.
6. No single-register descriptions.
Formal-only undertriggers. Casual-only produces generic output. Both fail.
7. No cross-conversation assumptions.
Each conversation is isolated. “Never repeat yourself across sessions” is a dead instruction.
8. No edge-case stuffing.
Anthropic warns against this directly. Laundry lists of rules consume context and conflict. Use 2-3 canonical examples instead.
9. No paragraph-form complex instructions.
Prose is ambiguous. Numbered steps with conditions have exactly one interpretation.
10. No overlapping skill sets.
“If a human engineer can’t definitively say which tool should be used in a given situation, an AI agent can’t be expected to do better” (Anthropic). Ambiguous boundaries cause mis-triggers.
### Skill Architecture
```
skill-name/
├── SKILL.md (<500 lines)
│   ├── YAML frontmatter (name + dual-register description, ~100 words)
│   ├── Expert Vocabulary Payload (FIRST in body)
│   ├── Anti-Pattern Watchlist (BEFORE behavioral instructions)
│   ├── Behavioral Instructions (ordered imperative steps)
│   ├── Output Format
│   ├── Examples (2-3 BAD vs GOOD pairs)
│   └── Questions This Skill Answers (at END, 8-15 queries)
└── references/
├── anti-patterns-full.md
├── frameworks.md
├── evaluation-criteria.md
└── checklists.md
```
Why this order matters:
The U-shaped attention curve (Liu et al., 2024; Wu et al., 2025) means the beginning and end of context receive disproportionate attention weight, while the middle receives measurably less. The Expert Vocabulary Payload sits at the top because it is the routing signal that determines which knowledge cluster the model draws from — it must be established before any behavioral instructions execute. The Questions This Skill Answers section sits at the bottom because retrieval anchors benefit from end-of-context attention and the recency effect. Behavioral instructions occupy the middle, but they are structured as numbered steps with explicit conditions — a format that survives middle-position attention degradation because the structure itself provides the signal that prose would lose.
Keep SKILL.md under 500 lines. If you need more, the content belongs in
`references/`
. The skill file is the router. The references are the depth.
Skill File Architecture and Attention Curve
Left column shows the seven sections of a SKILL.md file rendered as stacked rows with a tree connector. Right column shows a rotated U-shaped attention curve mapping each section to its attention weight, demonstrating that the top and bottom of the file receive the highest model attention.
SKILL.md (<500 lines)
YAML frontmatter
← HIGH ATTENTION
Expert Vocabulary
← HIGH ATTENTION
Anti-Pattern Watchlist
← MEDIUM
Behavioral Instructions
← LOW
Output Format
← LOW
Examples (2-3 BAD/GOOD)
← RISING
Questions (retrieval)
← HIGH ATTENTION
Attention Weight
Top
End
Front-load vocabulary + constraints, close with retrieval anchors (P2 attention curve)
Figure 13: Skill section order follows the attention curve — high-attention slots for vocabulary and retrieval anchors, structured formats for the middle.
## Part F: Source Index
All 20 research sources cited across this series are consolidated in the
Research Citation Index
, with links to the original papers and cross-references to the principles that cite them.
View the complete source index →
## The Capstone
This series started with a flaky meeting transcription pipeline and ended with a toolkit. The arc was deliberate.
Principles 1 through 3 taught you the foundations: when to pull the LLM out of the loop, how to manage context as a finite resource, and why documentation is live infrastructure. Principles 4 through 6 taught you execution discipline: plan before you build, codify your mistakes, and never trust a generalist reviewer. Principles 7 through 9 taught you governance: observe everything, gate what matters, and measure what you spend.
Principle 10 says: none of that matters if it lives in your head. Encode it. Automate it. Share it.
Forge encodes the science of agent design so you do not have to re-derive it from papers every time you build a specialist. jig encodes the discipline of context hygiene so you do not have to manually audit your tool loading every session. Together, they turn nine principles from knowledge you read into practice you follow — automatically, consistently, and without the decay that erodes manual discipline.
The tools are open-source. The research is open-access. The methodology is documented. Take what is useful. Ignore what is not. Build your own toolkit if ours does not fit. The point was never adoption. The point was showing that science-backed practice, encoded in tools, produces better results than vibes-based practice stored in memory. The research is clear. The implementation is up to you.
Install Forge:
```
claude plugin marketplace add jdforsythe/forge
claude plugin
install
forge
```
Try jig:
github.com/jdforsythe/jig
Star both repos if they helped. Fork and contribute domain agents — the library has 11 specialists, but your domain probably needs one we have not built yet.
This is the final article in the “10 Claude Code Principles” series. The full series, all research citations, and both open-source tools are linked from the overview article. Thank you for reading.
<!-- fetched-content:end -->
