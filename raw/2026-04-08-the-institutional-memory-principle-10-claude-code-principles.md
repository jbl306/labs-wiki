---
title: "The Institutional Memory Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:36:33.226750+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/institutional-memory/"
content_hash: "sha256:35683715fda0f10d03ca19da3200270b4855a70d0e266d432160ea385d76a84f"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/institutional-memory/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:23:35+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/institutional-memory/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/institutional-memory/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The War Story
The agent did it again. The exact same mistake. Different session, different developer, same result.
We had fixed this before. I remembered the pull request. Three weeks earlier, a teammate had spent an afternoon debugging the same cascade of test failures — the agent importing a deprecated internal module instead of the replacement we had migrated to months prior. The PR comment even included a clear explanation: “The agent keeps reaching for the old module because it is the more common pattern in the training data. We need to tell it explicitly.” The review was approved, the code was merged, and the knowledge evaporated.
It evaporated because the fix lived in a closed pull request comment. Not in our CLAUDE.md. Not in our project rules. Not anywhere that any agent, in any session, on any developer’s machine, would ever see again. The knowledge existed. The system just could not find it.
This is the default state of most teams working with AI agents. Every session starts from zero. Every correction is local to the conversation where it happened. Every developer accumulates tribal knowledge about what the agent gets wrong, and that knowledge lives in their head until they leave the company or forget. The same mistakes cycle through the same code on the same schedule.
The fix is not better prompting. It is an engineering handbook that the entire system — every agent, every session, every developer — consults and updates as a matter of workflow discipline.
## 2. The Principle
Maintain a living engineering handbook of project-specific patterns, rules, and past mistakes. Claude must consult and update it on every relevant task so the system learns permanently and stops repeating errors.
Most teams correct their agents in the moment. The agent uses the wrong import, and the developer says “No, use the new module.” The agent generates callbacks, and the developer says “We use async/await here.” Each correction is perfectly effective for the current session. And each correction is perfectly useless for the next session.
This is not a limitation of the model. It is a limitation of the workflow. LLMs have no memory between sessions — each conversation starts from a blank slate, with only the context you provide. If you provide nothing about your project’s conventions and past mistakes, the agent will fall back to the most statistically common patterns from its training data. And the most common patterns are, by definition, the most generic — the average of everything the model has seen, not the specific practices your team has chosen.
The research reveals that the solution is not just a guardrail but a steering mechanism. When you codify a constraint with its reasoning, you are not merely preventing one mistake. You are pushing the model’s entire output distribution away from the generic center and toward your project’s specific territory. That shift compounds across every task, every session, and every developer on the team.
## 3. The Science
### Negative Constraints as Steering Mechanisms
LLMs are trained on next-token prediction over massive corpora. The most probable next token at any position is the most statistically average one — the center of the training distribution. Without specific constraints, the model’s output gravitates toward this center: the most generic, common version of whatever you asked for. If your project uses
`T[]`
for TypeScript arrays but the broader ecosystem is split between
`T[]`
and
`Array<T>`
, the model has no reason to prefer your convention. It will reach for whichever pattern is more activated by its training data. Your convention is invisible to it.
A negative constraint changes this. “Never use
`Array<T>`
” creates explicit pressure away from one region of the output distribution. This is not just a guardrail that blocks a single wrong answer. It is a steering mechanism that shifts the entire output toward more specific, project-appropriate territory. The model must select from the remaining distribution, which is, by construction, closer to your intended convention.
The CHI 2023 paper “Why Johnny Can’t Prompt” (Zamfirescu-Pereira et al.) investigated how non-experts write prompts and found a critical pattern: non-experts overwhelmingly rely on “Do not X” phrasing alone, which is less effective than providing a positive alternative. However, when combined — positive instruction plus negative constraint — the effect is strongest. “Always use
`T[]`
BECAUSE our ESLint config enforces it and
`Array<T>`
will trigger CI failures” gives the model three interlocking signals: what to do, what not to do, and why. That combination outperforms either signal alone.
### Why “Why” Matters More Than “What”
A rule without an explanation is brittle. “Never use
`Array<T>`
” covers exactly one case — the literal use of
`Array<T>`
. A principle with an explanation generalizes. “Always use
`T[]`
BECAUSE our ESLint config enforces the
`array`
style for consistency with our codebase” tells the model something broader: this team has strong linting conventions, and the agent should defer to the linter’s preferences for any style question, not just this one.
Anthropic’s own skill-creator documentation makes this explicit: “Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs.” The model has been trained on vast amounts of human reasoning text. When given a principle plus its rationale, it draws on related knowledge to handle novel situations that the bare rule never anticipated. When given only the rule, it can only pattern-match against the literal text.
This is the difference between dead rules and living principles. A dead rule — “Never use
`Array<T>`
” — decays the moment a situation arises that does not match its exact wording. A living principle — “Defer to our ESLint config for all style decisions BECAUSE the linter is the source of truth” — gives the model a heuristic it can apply to dozens of analogous situations: semicolons, quote styles, trailing commas, import ordering. One well-reasoned principle does the work of twenty dead rules.
Rule Anatomy: Dead Rule vs Living Principle
Annotated anatomy of a living rule showing its four components (unambiguous directive, specific action, BECAUSE signal, and reason), compared side by side with a dead rule that lacks reasoning.
RULE ANATOMY
Always
use
T[]
BECAUSE
our ESLint config enforces it
Unambiguous directive
Specific action
Signal — not optional
Reason enables generalization
Dead Rule
Never use Array<T>
Covers one case. No reasoning.
Cannot generalize. Will fossilize.
Living Principle
Always use T[]
BECAUSE
...
Covers case explicitly. Model generalizes
to adjacent style decisions.
Reason enables pruning.
Figure 6: A rule with a BECAUSE clause generalizes to adjacent decisions. Without it, rules fossilize.
## 4. Before and After
Before: Corrections That Evaporate
The workflow was reactive and session-scoped. A developer would start a new Claude session, encounter familiar mistakes, and correct them one by one. The agent would reach for the deprecated module. Correction. Callbacks instead of async/await. Correction.
`Array<T>`
instead of
`T[]`
. Correction. Each fix worked within that session. And each fix vanished when the session ended.
The developer who had been on the project for six months had accumulated a mental list of “things Claude gets wrong on this project,” but that list existed only in their head. When they were out sick, their teammates rediscovered the same issues from scratch. The cost was not just wasted time — it was the erosion of trust. Developers stopped believing the agent could produce correct code on the first attempt for anything project-specific. Some gave up on using the agent for anything beyond boilerplate.
After: Mistakes Codified Once, Prevented Forever
The transformation was adding a structured “always/never” section to the project’s CLAUDE.md file. Every time an agent made a project-specific mistake, the developer who caught it did two things: fixed the immediate issue and added a rule to the handbook with its reasoning.
The section grew organically. The first week produced about a dozen rules:
```
## Always/Never
- Always use `T[]` for array types, BECAUSE our ESLint config enforces the `array` style and `Array<T>` triggers CI failures
- Never import from `@internal/legacy-auth`, BECAUSE it was deprecated in v3.2 — use `@internal/auth` instead
- Always use `async/await` over `.then()` chains, BECAUSE our codebase convention is async-first and mixed styles make PRs harder to review
- Never use `index` as a React list key, BECAUSE our performance reviews flagged re-render bugs from non-stable keys
- Always include a `data-testid` attribute on interactive elements, BECAUSE our E2E tests rely on them and missing IDs cause test failures
```
Each rule followed the same format: always or never, the specific action, and the reason. The reason was not optional. A rule without a reason was not allowed into the handbook.
Within two weeks, repeat errors on codified patterns dropped to near zero. New developers joining the project got convention-compliant code from their very first agent session, because the agent read the handbook before generating a single line. The knowledge that used to live in one developer’s head now lived in the system, accessible to every agent, every session, every team member.
## 5. Tactical Implementation
Here is how to build institutional memory into your workflow, starting tomorrow.
Step 1: Create an “always/never” section in your CLAUDE.md.
Open your project’s CLAUDE.md file — or create one if it does not exist. Add a clearly labeled section for project-specific rules. This is the engineering handbook that every agent session will read automatically. Keep it at the top level of the project so it is loaded into context at the start of every session.
Step 2: When an agent makes a mistake, fix it AND codify the rule with the reason.
This is the critical discipline. Correcting the agent in the session is necessary but not sufficient. The second step — adding the rule to the handbook — is what turns a one-time fix into permanent institutional knowledge. Do both every time. If you only fix and do not codify, you are choosing to debug this again.
Step 3: Format every rule as “Always/Never [action] BECAUSE [reason].”
The format is the mechanism. “Always” and “never” are unambiguous directives that leave no room for hedging. The “BECAUSE” clause is what makes the rule generalizable — a rule without a reason covers one case, while a rule with a reason becomes a living principle the model extends to novel situations. If you cannot articulate the reason, the rule may not be worth codifying.
Step 4: Use named anti-patterns from your domain.
“Bikeshedding (Parkinson’s Law of Triviality)” is a more powerful directive than “don’t spend too much time on small things.” Named anti-patterns activate specific knowledge clusters in the model’s training data. When the model sees “Bikeshedding,” it draws on everything it knows about that concept. When it sees “don’t spend too much time on small things,” it has no cluster to activate. The name is the routing signal.
The same applies to your project-specific patterns. If your team has a name for a recurring problem — “the timezone bug,” “the eager-loading trap,” “the N+1 migration” — use that name in the handbook.
Step 5: Review and prune quarterly.
Rules accumulate. Some become obsolete as the codebase evolves — the deprecated module gets removed entirely, the ESLint config changes, the convention gets superseded. Rules without reasons are the first to become dead weight because no one remembers why they were added. The BECAUSE clause gives future reviewers the context to decide whether a rule still applies.
Set a quarterly reminder to review the handbook. Delete rules that no longer apply. Update rules whose reasoning has changed. A lean, current handbook outperforms a bloated one — this connects directly to Principle 2 (Context Hygiene), because every obsolete rule consumes attention budget for zero value.
Step 6: Share the handbook across the team.
The handbook should live in the repository, version-controlled alongside the code. One developer’s mistake, codified in the handbook, prevents every other developer’s agent from making the same mistake. The cost of adding a rule is borne once; the benefit is distributed across every session on the team.
Step 7: Give your failures a shared vocabulary.
The MAST taxonomy identifies 14 distinct failure modes in multi-agent systems, organized into three categories: communication failures, coordination failures, and quality failures. You do not need to memorize all 14. But giving your team a shared vocabulary for what goes wrong — “that was a role confusion failure,” “this is a rubber-stamp review problem” — transforms debugging from vague frustration into precise diagnosis. Named failures are diagnosable failures. Unnamed failures repeat.
## 6. Common Pitfalls
“Rules Without Reasons”
A handbook full of bare directives — “Never do X,” “Always do Y” — without any explanation. The model follows the literal rule when it recognizes the exact situation, but cannot generalize to adjacent cases. Worse, when the rule’s context changes and no one knows why it was added, no one removes it. The rule fossilizes.
The fix: every rule gets a BECAUSE clause. No exceptions. If you cannot explain why, investigate until you can.
“Never Pruning”
The handbook grows monotonically. Six months in, it contains 80 rules — some contradictory, some obsolete, some applying to code deleted three sprints ago. The model reads all 80 at the start of every session, consuming context that could be allocated to the actual task. This is a direct violation of Principle 2 (Context Hygiene).
The fix: quarterly reviews. Check whether each BECAUSE clause still applies. Delete ruthlessly. A 20-rule current handbook outperforms an 80-rule stale one.
“Rules That Contradict”
The handbook says “Always use
`lodash`
for utility functions BECAUSE it is our standard library.” Three months later, someone adds “Never import
`lodash`
for single-use utilities BECAUSE it increases bundle size.” Both rules have valid reasoning, but they conflict. The model has no way to resolve the contradiction and will oscillate between them depending on which one gets more attention weight in the current context. This connects to Principle 3 (Living Documentation): contradictory rules are a form of documentation rot.
The fix: when adding a rule that modifies an existing one, update the original rule rather than adding a new one. The handbook should have one authoritative statement per topic, not a chronological log of evolving opinions.
“Session-Only Corrections”
The most common and most insidious failure. The developer corrects the agent, the session proceeds smoothly, and the correction is never codified. Three sessions later, the same mistake recurs. Each individual instance feels too small to bother codifying, but the cumulative cost is enormous.
The fix: make codification reflexive. The moment you correct the agent, ask: will this come up again? For project-specific conventions, the answer is almost always yes. The thirty seconds it takes to write the rule saves the team hours over the life of the project.
## 7. Expected Impact
The most immediate metric is repeat error rate. Once a rule is codified in the handbook, the specific mistake it addresses should drop to near-zero across all sessions and all developers. On our team, repeat errors on codified patterns effectively disappeared within two weeks. The errors did not gradually decline — they stopped.
The second metric is onboarding velocity. When a new developer joins the team, their agent produces convention-compliant code from the first session. The handbook is the ramp-up. New team members who used to spend their first week fighting convention violations now spend it shipping features.
The third metric is trust. When developers trust that the agent will follow project conventions without being reminded, they stop pre-loading corrections at the start of every session. They stop double-checking every output for known pitfalls. The cognitive overhead drops, and the agent becomes the accelerator it was supposed to be.
## 8. Fact Sheet
Principle:
The Institutional Memory Principle
One-sentence definition:
Maintain a living engineering handbook of project-specific patterns, rules, and past mistakes so the system learns permanently and stops repeating errors across every session and every developer.
The science:
Negative constraints steer the model away from the generic distribution center toward project-specific output (CHI 2023, “Why Johnny Can’t Prompt”); rules with explanations generalize to novel situations while bare rules cover only listed cases (Anthropic skill-creator docs).
5 key takeaways:
- Every session-only correction is a future repeat error waiting to happen
- “Always/Never X BECAUSE Y” is the format — the BECAUSE clause is what makes rules generalizable
- Named anti-patterns activate expert knowledge clusters; unnamed problems get generic responses
- Rules without reasons become dead weight; prune the handbook quarterly
- Share the handbook across the team — one developer’s codified mistake prevents everyone’s repeat
Quick-start checklist:
- Add an “always/never” section to your project’s CLAUDE.md
- Codify the next three agent mistakes you correct, with BECAUSE clauses
- Review the handbook for contradictions or stale rules
- Share the handbook with your team via version control
- Set a quarterly calendar reminder to prune and update
The metric to watch:
Repeat error rate on codified patterns — should drop to near-zero within the first two weeks.
Download Fact Sheet (SVG) →
## 9. What’s Next
Your handbook prevents repeat errors. The agent reads the rules, follows the conventions, and the same mistakes stop cycling through your codebase. The institutional memory is working.
But who catches errors the first time? The handbook codifies past mistakes. It does nothing about novel ones — the subtle security vulnerability, the performance cliff hiding behind an innocent-looking query, the accessibility gap no one on the team has encountered before.
If your answer is “one generalist review agent,” I have bad news. That agent is confidently missing bugs that would make a specialist cringe. A generalist reviewer trends toward the median of its training data, and the median developer is not a security expert, not a performance engineer, and not an accessibility specialist. The generalist catches the obvious issues and waves through the rest with the confidence of someone who does not know what they do not know.
That is Principle 6 — The Specialized Review Principle. The science behind it will change how you think about AI expertise, and it starts with a research finding that demolishes one of the most common prompting practices: flattery does not work. It makes output worse. What works instead is vocabulary, and the mechanism explains why a 30-token job title outperforms a three-paragraph backstory.
<!-- fetched-content:end -->
