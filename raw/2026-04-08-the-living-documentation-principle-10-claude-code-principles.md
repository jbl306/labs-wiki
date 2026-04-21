---
title: "The Living Documentation Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:35:53.591647+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/living-documentation/"
content_hash: "sha256:137dab8122511c4851da23574533ffc6024bb706eb264f2c0203f82db684eacd"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/living-documentation/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:24:01+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/living-documentation/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/living-documentation/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The Bug That Wasn’t a Bug
It took us three days to find the bug. Three days of debugging ESLint violations that appeared out of nowhere.
The agent kept using
`Array<T>`
instead of
`T[]`
. Every file it touched, same violation. We checked our ESLint config —
`T[]`
was enforced. We checked our project rules —
`T[]`
was specified. We checked our prompts, our CLAUDE.md, our system instructions. Everything said
`T[]`
. The agent kept writing
`Array<T>`
.
We started suspecting the model itself. Maybe a regression in the latest version. Maybe something about our codebase was triggering a preference. We ran test prompts in isolation — the model used
`T[]`
just fine. Back in the project,
`Array<T>`
every time. Three developers, three days, burning hours on something that should not have been possible.
Finally, one of us ran a search across every markdown file in the repository. Buried in an old conventions document that hadn’t been touched in months — a file nobody remembered editing, loaded automatically by our tooling — was a single line: “Prefer
`Array<T>`
for readability.”
One line. Written during a different era of the project, before we standardized on
`T[]`
, before we configured the linter to enforce it. The document had never been updated. The agent read it, pattern-matched against it, and faithfully followed the stale instruction — exactly as it was designed to do.
The model wasn’t broken. Our documentation was.
## 2. The Principle
Claude must document everything exhaustively and in a structured, machine-readable way. Documentation becomes the single source of truth for both humans and agents alike. Automate freshness checks so stale docs can never silently poison your workflow.
Most teams treat documentation as a one-time artifact. They write it when they set up the project, update it when someone complains, and forget about it until the next onboarding session. That approach was already fragile. With AI agents reading your documentation as operational instructions — not just as reference material — it becomes actively dangerous.
Here is the shift most people miss: documentation is no longer just for humans who can exercise judgment when something looks outdated. Your agent reads your docs the way a new hire reads the employee handbook on their first day — literally, completely, without the institutional context to know which parts are stale. When a human reads “prefer
`Array<T>`
for readability” in a dusty markdown file, they might check whether that still matches the linter. The agent will not. It will follow the instruction.
Documentation entropy — the natural tendency of docs to drift out of sync with reality — is not a minor inconvenience in agentic workflows. It is a vector for systematic, repeatable errors that look like model failures but are entirely self-inflicted.
The Living Documentation Principle treats this as an engineering problem, not a discipline problem. You do not solve it by telling people to update their docs. You solve it with structure, automation, and CI.
## 3. The Science
### Documentation IS Few-Shot Context
There is a persistent misconception that you tell an LLM what to do by writing rules, and it follows them. The reality is more nuanced and has direct implications for how you write documentation.
LLMs are fundamentally pattern-matching engines. They were trained on sequence prediction — given this input, predict the most likely next token. When they encounter examples in their context, they pattern-match against the demonstrated structure far more reliably than they follow abstract verbal rules. This is not a quirk; it is how the architecture works.
LangChain’s few-shot research (2024) quantified this precisely: three well-chosen examples match nine in effectiveness, with diminishing returns beyond that. Wei et al. (2022) demonstrated the same principle in chain-of-thought prompting — showing the model
how
to reason, step by step, outperforms telling it
to
reason carefully.
The implication for documentation is direct. Your convention docs, your CLAUDE.md, your ADRs — these are not passive reference material. They are the few-shot context the agent uses to calibrate its output. Every code example in your documentation is a demonstration the model will pattern-match against. Every convention you describe with an example is a few-shot prompt. Every stale example is a poisoned example.
There is also a positional effect. LLMs exhibit recency bias — they weight the last example in a sequence more heavily than earlier ones (Liu et al., 2024). This means the ordering of your documentation sections is not arbitrary. The convention you place last in a section will have disproportionate influence. Structure your docs so the most critical convention appears at the end of each section, not buried in the middle.
### Structure Reduces Ambiguity
If few-shot context explains
what
the agent learns from your docs, structure explains
how reliably
it learns.
Anthropic’s own documentation states it plainly: “Claude has been specifically tuned to pay special attention to your structure.” XML tags, Markdown headers, YAML frontmatter — these are not cosmetic formatting choices. They are parsing boundaries that tell the model exactly where one instruction ends and another begins.
He et al. (2025) measured this in a comparative study: model performance varies up to
40%
based on prompt format alone, with the same semantic content. The difference between a well-structured prompt and a prose wall is not readability for humans — it is parseability for the model.
Machine-readable documentation — YAML headers, clearly delimited Markdown sections, consistent heading hierarchies — serves both audiences simultaneously. A human can scan the headers. The agent can parse the structure. Prose paragraphs are ambiguous by nature; they rely on the reader to infer boundaries, prioritize information, and resolve contradictions. Structured formats have exactly one interpretation.
This is why “make docs machine-readable” is not a nice-to-have. It is the difference between documentation that occasionally misleads and documentation that reliably instructs.
## 4. Before and After
### Before: The Slow Rot
The project starts with decent documentation. Someone writes a
`CONVENTIONS.md`
file during setup. It has some TypeScript preferences, import ordering rules, naming conventions. Good intentions.
Six months later, the linter config has changed twice. Two team members have joined and brought different preferences that got adopted informally. The original author of
`CONVENTIONS.md`
left the company three months ago. The file still says “prefer default exports” even though the team switched to named exports in month two. It still says “use Moment.js for date formatting” even though the project migrated to
`date-fns`
in a PR that nobody thought to pair with a docs update.
The agent reads all of it. Every outdated preference, every stale recommendation. It uses Moment.js in new code because the documentation said to. A developer catches it in review, fixes the code, and moves on. Nobody updates the doc. The next agent session does the same thing. The cycle repeats until someone either finds the stale doc or gives up and adds a correction to the system prompt — which itself becomes stale documentation in a different location.
The failure mode is not dramatic. It is a slow bleed: ten minutes here, twenty minutes there, a three-day debugging session once in a while. Death by a thousand paper cuts, all traceable to documentation that nobody owns.
### After: Living Documentation
The same project, restructured.
`CLAUDE.md`
contains active conventions in clearly delimited sections with YAML-style metadata. Each convention includes a
`last-verified`
date. Each section has 2-3 canonical code examples that demonstrate the convention in practice.
Significant decisions are recorded in Architecture Decision Records (ADRs) — not just
what
was decided, but
why
, and what was explicitly rejected. When the team switched from default exports to named exports, the ADR captured the rationale. When an agent encounters both patterns in old code, the ADR tells it which is current and why.
A weekly CI job scans every documentation file. Anything not updated in 30 days gets flagged. The job generates a PR that assigns the relevant team member to verify or update each flagged doc. Stale documentation does not survive in silence — it gets surfaced automatically.
The agent now reads documentation that matches reality. First-attempt convention compliance went from sporadic to consistent. The debugging sessions caused by stale docs stopped entirely — not because the team became more disciplined about updating docs, but because the system made staleness visible before it could cause damage.
## 5. Tactical Implementation
### 1. Document every significant decision in an ADR
Architecture Decision Records capture the
why
behind decisions, not just the
what
. When you switch from
`Array<T>`
to
`T[]`
, the ADR records the date, the rationale, what you considered and rejected, and who approved it. Six months from now, when an agent or a new hire encounters the old pattern in legacy code, the ADR provides the authoritative answer. Keep ADRs in a
`/docs/decisions/`
directory, numbered sequentially.
### 2. Use structured formats, not prose paragraphs
YAML frontmatter for metadata. Clear Markdown sections with consistent heading hierarchies. Bulleted lists for conventions. Code blocks for examples. If you catch yourself writing a paragraph that explains a convention, stop and restructure it as a heading, a one-line rule, and an example. The agent will parse the structured version reliably; the paragraph version is a coin flip.
### 3. Make every doc machine-readable
Read each documentation file and ask: can an agent extract every convention from this without ambiguity? If a section requires inferring the boundary between one instruction and the next, rewrite it. If a convention is stated in prose but not demonstrated in code, add a code example. Machine-readable does not mean inhuman — it means unambiguous.
### 4. Automate freshness checks
Create a CI job that runs weekly. It checks the
`last-modified`
date (or a
`last-verified`
frontmatter field) on every doc in your conventions directory. Anything older than 30 days generates a PR assigned to the file’s owner (or the team lead if no owner is specified). The PR asks one question: “Is this still accurate?” The answer is either a verification commit that updates the date or an update commit that fixes the content.
Documentation Freshness CI Pipeline
A weekly cron job scans docs for last-verified dates. If updated within 30 days the check passes. Otherwise a PR is created for the file owner to confirm accuracy and update the last-verified timestamp, looping back to the scan step.
DOCUMENTATION FRESHNESS PIPELINE
Weekly
Cron
Scan docs for
last-verified
Updated
< 30 days?
YES
✓ Pass
NO
Create PR
→ file owner
Owner: still
accurate?
Update
last-verified
next cycle
Figure 4: A weekly CI job enforces documentation freshness by creating PRs for stale docs.
### 5. Put conventions in CLAUDE.md
Claude Code reads
`CLAUDE.md`
automatically at the start of every session. This is not optional documentation — it is the agent’s operating instructions. Put your most critical conventions here: coding standards, naming conventions, import patterns, testing requirements. Keep it focused. Every token in
`CLAUDE.md`
competes for attention with every other token. Structured, machine-readable formats are the foundation for defining agent behaviors — the more precisely you structure these instructions, the more reliably the agent follows them.
### 6. Version documentation alongside code
Documentation changes belong in the same PR as the code changes they describe. If a PR changes the import convention, the PR also updates
`CONVENTIONS.md`
and
`CLAUDE.md`
. Make this a review requirement. Documentation that lives in a wiki, a Notion page, or a Google Doc is documentation that will drift from reality within weeks. Docs in the repo, reviewed in the same PR, stay synchronized by process rather than by discipline.
### 7. Include 2-3 canonical examples in your conventions
The agent learns from examples more reliably than from rules. For every convention, include a “do this” code block and optionally a “not this” code block. Three examples is the sweet spot — enough to demonstrate the pattern, not so many that they consume attention budget. Place the most representative example last in each section to take advantage of recency bias.
## 6. Common Pitfalls
### “Write once, never update”
Documentation entropy is the default state. Every project starts with accurate docs and drifts toward inaccuracy at a rate proportional to the pace of development. The failure is not that someone forgot to update the docs — it is that the system has no mechanism to detect or surface staleness. Detection: you find yourself correcting the agent for following a convention that used to be correct. Fix: automated freshness checks that make staleness visible before it causes damage.
### “Prose-only docs”
A three-paragraph explanation of your naming convention feels thorough to the human who wrote it. To the agent, it is an ambiguous blob that requires inference to parse. The model must guess where one instruction ends and another begins, which phrases are conventions and which are commentary, which examples are current and which are historical. Detection: the agent follows the spirit of the doc but gets specifics wrong. Fix: restructure as heading + one-line rule + code example. Let structure carry the meaning that prose obscures.
### “Documentation that contradicts code”
The doc says “use Moment.js.” The
`package.json`
has
`date-fns`
. The linter enforces one convention; the documentation recommends another. The agent must resolve the contradiction, and it may resolve it differently each time depending on what else is in context. Detection: inconsistent agent behavior on the same convention across sessions. Fix: treat documentation-code contradictions as bugs with the same severity as functional bugs. Add a CI check that cross-references documented dependencies with actual dependencies.
### “Documenting the obvious”
Over-documentation wastes attention budget. If your linter enforces semicolons, you do not need a convention doc that says “use semicolons.” The agent will hit the linter error and self-correct. Document the things that are not mechanically enforced — architectural patterns, naming conventions that ESLint cannot check, reasons behind non-obvious decisions. Detection: your CLAUDE.md is longer than 200 lines and half of it restates what the linter already enforces. Fix: remove anything the toolchain already handles. Reserve documentation for human and agent judgment calls.
## 7. Expected Impact
After implementing automated freshness checks, stale-doc incidents dropped to zero. Not reduced — eliminated. The CI job surfaces every aging document before it can silently mislead an agent session.
Agent-generated code started matching conventions on first attempt rather than requiring correction cycles. The compounding effect is significant: each correction cycle costs context tokens (the review comment, the agent’s acknowledgment, the regenerated code) and human attention. When the agent gets it right the first time because the documentation is accurate and unambiguous, both costs disappear.
Teams that adopted structured documentation with canonical examples reported measurably fewer “why did the agent do that?” debugging sessions. The answer to that question, almost always, is “because the documentation told it to.” When the documentation is current, structured, and verified, the agent’s behavior becomes predictable — which is the entire point.
## 8. Fact Sheet
Principle:
The Living Documentation Principle
One-sentence definition:
Documentation must be structured, machine-readable, and automatically checked for freshness — because agents follow stale docs as faithfully as current ones.
The science:
LLMs pattern-match against examples more reliably than they follow rules; 3 well-chosen examples match 9 in effectiveness (LangChain, 2024), and prompt structure alone accounts for up to 40% performance variation (He et al., 2025).
5 key takeaways:
- Documentation is operational context for agents, not passive reference for humans
- Stale docs are not just unhelpful — they are actively poisonous to agent output
- Structured formats (YAML, delimited Markdown) outperform prose for both human and agent consumption
- Few-shot examples in docs teach conventions more effectively than written rules
- Freshness is an engineering problem solved by CI, not a discipline problem solved by reminders
Quick-start checklist:
- Add `last-verified` frontmatter to every convention doc
- Create a weekly CI job that flags docs older than 30 days
- Add 2-3 code examples to each convention in CLAUDE.md
- Move one prose-heavy doc to structured format (heading + rule + example)
The metric to watch:
Number of agent-generated code corrections caused by stale or ambiguous documentation. Target: zero.
Download Fact Sheet (SVG) →
## 9. What’s Next
Fresh documentation gives your agent accurate instructions. But instructions alone do not produce good outcomes — you also need a plan. And that plan needs to be something you can throw away without flinching.
Most developers have an emotional relationship with their code. They spend hours on an elegant solution and then refuse to kill it even when the direction is clearly wrong. They patch, they hack, they band-aid — anything to avoid admitting the approach was flawed. In agentic workflows, this attachment is not just inefficient. It is structurally incompatible with how the work should flow.
The moment you fall in love with your code, you lose the ability to kill it cleanly. And clean kills — scrapping a bad branch, refining the blueprint, restarting from a fresh context — are how you stay fast. Your capital as a developer does not belong in the code you wrote. It belongs in the plan you made. Code is an acquaintance, not a spouse.
That is Principle 4: The Disposable Blueprint Principle.
<!-- fetched-content:end -->
