---
title: "The Disposable Blueprint Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:36:21.703567+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/disposable-blueprint/"
content_hash: "sha256:417c8d4343cd81d43b940e374c08fdb3669cd666a073519a9013f4a7436d12c9"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/disposable-blueprint/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:22:31+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/disposable-blueprint/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/disposable-blueprint/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The Sunk Cost
I used to fall in love with my code. I’d spend hours crafting an elegant solution, then refuse to throw it away even when the approach was clearly wrong. I’d patch, hack, and band-aid rather than admit the direction was flawed. The abstraction didn’t fit? Wrap it in another layer. The data model was wrong? Add a translation step. The architecture was fighting me at every turn? Push harder. I had hours invested. I wasn’t going to throw that away.
Sound familiar? Every developer I know has done this. The sunk-cost fallacy isn’t just an economics concept — it’s the default operating mode for anyone who writes code for a living. We get emotionally attached to our work because it feels like an extension of ourselves. Deleting code feels like deleting effort, like admitting failure.
Then I started working with AI agents, and I learned the most liberating lesson of my career: code is an acquaintance, not a spouse. Like them, enjoy them, but do not love them. Love the thing you build, not how you build it.
When you can regenerate a complete implementation in minutes from a solid plan, the calculus changes completely. The code itself becomes disposable. The plan — the blueprint that describes the intent, the structure, the constraints — that’s where your intellectual capital lives. Kill the branch, refine the blueprint, restart cleanly. It takes minutes. The hours you used to spend patching a bad direction? Gone. Not reduced. Eliminated.
But this only works if the blueprint exists. If it’s saved. If it’s versioned. If it’s structured enough to survive a context reset and still be useful. That’s the principle.
## 2. The Principle
The Disposable Blueprint Principle:
Never implement without a saved, versioned plan artifact. Brainstorm, deepen, archive the full blueprint. If execution goes off the rails, kill the branch, refine the blueprint, and restart cleanly.
Most developers jump straight to code. Even with AI agents, the pattern is: describe the feature in chat, start implementing immediately, course-correct as problems emerge. This works fine when the feature is small and the approach is obvious. It falls apart the moment complexity exceeds what you can hold in your head — and with agentic workflows, that threshold arrives faster than you expect.
The core insight is that planning and implementation are fundamentally different cognitive modes, and mixing them degrades both. When you plan during implementation, you make compromises to fit what’s already written. When you implement during planning, you lock in decisions before you’ve explored the space. Separating them — planning fully, then implementing from the plan — sounds like waterfall thinking, but it’s the opposite. Waterfall plans are heavy, sacred, change-resistant. Disposable blueprints are cheap, versioned, and meant to be thrown away the moment a better approach surfaces.
The plan is the artifact that survives everything: context resets, session boundaries, team handoffs, and your own forgetfulness after a weekend away from the code.
## 3. The Science
### Structured Artifacts Survive Handoffs
Hong et al. (2023) studied multi-agent collaboration in their MetaGPT framework and found that teams using structured artifacts — documented plans, interface definitions, and formal specifications shared between agents — produced approximately 40% fewer errors than teams relying on free-form dialogue alone. The mechanism is straightforward: dialogue is lossy. Information gets paraphrased, reinterpreted, and gradually mutated as it passes between participants. A structured artifact has one interpretation. A conversation has as many interpretations as it has participants.
This finding applies directly to the most common “handoff” in agentic development: the transition between conversation sessions. When you
`/clear`
your context or start a new session, everything in the conversation is gone. Everything in files persists. A plan saved to a markdown file survives the context reset perfectly — same words, same structure, same intent. The new session reads the plan with fresh attention, no degradation, no “Lost in the Middle” effects from a bloated conversation history. The plan IS the handoff mechanism.
He et al. (2025) measured something complementary: model performance can vary up to 40% based on prompt format alone. The same information, restructured with clear sections, headers, and explicit delineation, produces dramatically better results than the same information in prose paragraphs. Anthropic’s own documentation confirms this for Claude specifically — “Claude has been specifically tuned to pay special attention to your structure.” A plan with labeled sections (Goal, Constraints, Architecture, File Changes, Test Strategy) has exactly one interpretation. A plan described in flowing paragraphs is a Rorschach test.
### The Blueprint as Communication Medium
Plans externalized to files become something more powerful than documentation — they become the communication interface between conversation sessions. Think of each Claude session as a fresh team member joining the project. That team member has the model’s full training knowledge but zero context about your specific situation. The plan file is their onboarding document.
Each new session reads the plan fresh. No accumulated context drift. No information that was clear in message 3 but buried by message 47. No “I think you mentioned earlier that…” hedging. The plan is clean context every time, which connects directly to the Context Hygiene Principle (Principle 2): the best context is focused, positioned at the start of the conversation, and free of noise. A structured plan file delivered at the beginning of a fresh session is the optimal use of the attention budget.
This also means the plan serves as a checkpoint. If the implementation diverges from the plan, you have a reference point to identify where and why. If the plan itself was flawed, you revise the plan — not the code. The blueprint is the source of truth, and the code is the output derived from it.
## 4. Before and After
Blueprint, Branch, Build Cycle
A triangular cycle showing how a disposable blueprint drives branching and building. On success the branch merges; on failure the branch is killed and lessons update the plan to a new version.
BLUEPRINT
Goal · Constraints · Approach
File Changes · Test Strategy
v1
BRANCH
/clear → fresh session
reads plan
BUILD
Implement against plan
Merge
Kill branch.
Lessons update
plan → v2
Code is disposable.
The plan is capital.
Figure 5: The Blueprint-Branch-Build cycle. Failed code is disposable; the plan accumulates value.
### Before: The Sunk-Cost Spiral
The pattern was always the same. Start a feature, describe it to the agent in conversation, begin coding. Thirty messages in, realize the data model doesn’t support the edge case that just surfaced. But the API layer is built. The tests are written. The frontend components are wired up. So instead of stepping back, you patch: add a transformation layer, introduce a special case, bolt on a workaround. Forty messages later, the context is bloated and the agent is losing track of what was decided when. You’re spending more time re-explaining previous decisions than making progress.
The real cost wasn’t the code — it was the compound interest on a bad direction. Every patch made the next patch harder. Every workaround constrained the solution space. After two hours, I’d have a “working” implementation that was fragile, hard to test, and would require a full rewrite if anyone tried to extend it. But I’d invested two hours. So I’d ship it, tell myself it was “good enough,” and move on. The technical debt accrued silently until the next developer (or the next me) paid for it.
### After: Blueprint, Branch, Build
Now the workflow is different. Before any implementation, the plan exists as a file. Sometimes it takes five minutes to write. Sometimes it takes an hour of back-and-forth brainstorming with Claude. Either way, the artifact gets saved: a markdown file in the repo, committed alongside the code, with clear sections for the goal, the approach, the file changes, and the known constraints.
Then:
`/clear`
. Fresh session. The agent reads the plan file with a clean attention budget. Implementation begins from a structured, unambiguous specification — not from a conversation that’s been accumulating noise for an hour.
When things go wrong — and they still go wrong, because software is hard — the response is different. The plan file says the approach was X. The implementation revealed that X doesn’t work because of Y. Instead of patching, the process is:
`git stash`
or kill the branch. Open the plan file. Add what was learned. Revise the approach. Start a fresh session with the updated plan. Total time to restart: minutes. The failed attempt wasn’t wasted — it produced information that improved the plan. The code was disposable. The learning wasn’t.
## 5. Tactical Implementation
1. Never implement without a saved plan file — even for “small” changes.
Scope always grows. The feature that was “just a quick fix” becomes a three-file refactor. If you started without a plan, you’re now deep into implementation with no reference point for the original intent. Start every unit of work by writing or updating a plan file, even if it’s five lines.
2. Brainstorm freely in conversation, then distill into a structured plan artifact.
Use the conversational mode for what it’s good at: exploring possibilities, asking “what if,” challenging assumptions. Then take the output of that exploration and distill it into a structured document. Sections like Goal, Constraints, Approach, File Changes, and Test Strategy force you to make implicit decisions explicit.
3. Version the plan in git alongside the code.
The plan is a first-class artifact, not a scratchpad. Commit it. Review it in PRs. When you look back in three months and wonder why the API was designed that way, the plan file will tell you — including what alternatives were considered and rejected.
4. Use
`/clear`
between planning and implementation.
This is the critical habit. Planning and implementing are different modes that benefit from different contexts. The planning session might involve exploring three approaches, debating trade-offs, and reading reference code. The implementation session needs a clean focus on the chosen approach.
`/clear`
gives you that clean slate, and the plan file carries over everything the implementation session needs.
5. When implementation goes off the rails: kill the branch, refine the blueprint, restart.
This is the part that feels wrong until you’ve done it three times. Throwing away code feels wasteful. But the code was cheap — the agent generated most of it. What’s expensive is your time debugging a bad direction. Update the plan with what you learned, start a fresh branch, and let the agent regenerate from the improved specification. The second attempt is almost always faster and cleaner than any amount of patching would have produced.
6. Plans should define not just what to build but the expected structure.
Go beyond “add a user settings page.” Define the component hierarchy, the state management approach, the API contract. For more complex work involving multiple coordinated agents, the plan should describe which agents are responsible for what, how they’re arranged, and the interfaces between their deliverables. The more explicit the structure, the less room for misinterpretation.
7. Review plans before code — your capital as a developer belongs in planning, not typing.
When you review a PR, the implementation is already done. Mistakes are expensive to fix. When you review a plan, nothing is built yet. Changes are free. Spend your human judgment where it has the highest leverage: before the first line of code is written.
## 6. Common Pitfalls
### “Implementing Without a Plan”
The most common failure. It feels faster to skip the plan and jump straight to code, especially for experienced developers who can “see the solution” immediately. The problem isn’t the first 30 minutes — it’s the second hour, when the approach you “saw” turns out to be wrong and you’re too invested to restart. Detection signal: you find yourself re-explaining decisions to the agent mid-session, or saying “actually, forget what I said earlier.” If you’re course-correcting verbally, you needed a plan.
### “Precious Plans”
The opposite failure: treating the plan as sacred. The plan is a tool, not a commitment. If new information surfaces during implementation that invalidates the approach, the correct response is to update the plan, not to force the implementation to match a flawed plan. Detection signal: you’re writing code that feels wrong because “the plan says to do it this way.” Plans are cheap. Debugging is expensive. Kill the plan and write a better one.
### “Plans Without Version Control”
A plan in a chat session dies when the session ends. A plan in a local text file can be lost, overwritten, or diverge from what was actually built. If the plan isn’t in git, it doesn’t exist — not in any meaningful sense. Version control gives you history, review, and the ability to compare what was planned against what was built. Detection signal: you’ve ever said “I think the plan was…” instead of pulling it up.
### “Sunk-Cost Attachment”
You’ve written 400 lines. The approach is wrong. You know it’s wrong. But 400 lines. This is pure sunk-cost fallacy, and it’s the exact failure mode this principle exists to address. Those 400 lines took the agent minutes to generate. A restart from an updated plan will take minutes more. The hours you’ll spend patching a bad direction are the real cost. Detection signal: the phrase “we’re too far in to start over” has entered your vocabulary. You’re never too far in. The plan is right there.
## 7. Expected Impact
Time to restart after a failed approach: minutes (refine the blueprint, create a new branch, let the agent regenerate) instead of hours (debugging a bad direction, adding workarounds, patching structural problems). This alone pays for the time spent planning by the second or third course correction.
Plans reviewed before code catches architectural mistakes before a single line is written. In practice, plan review surfaces roughly 80% of structural issues — wrong data model, missing edge cases, incorrect API contracts — when they’re free to fix, not after they’re baked into the implementation. Review of a plan takes minutes. Reworking a completed implementation takes hours or days.
The compounding effect: teams that adopt this principle report that their second implementation attempt (after a blueprint revision) is consistently higher quality than what patching would have produced. The failed attempt isn’t waste — it’s research that improves the blueprint.
## 8. Fact Sheet
Principle:
The Disposable Blueprint Principle
One-sentence definition:
Never implement without a saved, versioned plan artifact; if execution goes off the rails, kill the branch, refine the blueprint, and restart cleanly.
The science:
Teams using structured artifacts produce ~40% fewer errors than those using free dialogue (Hong et al., 2023 — MetaGPT); prompt structure alone accounts for up to 40% performance variance (He et al., 2025).
5 key takeaways:
- Planning and implementation are different cognitive modes — separate them with `/clear`
- Code is disposable; the blueprint is where your intellectual capital lives
- Structured plan files are the optimal handoff mechanism between sessions
- Sunk-cost attachment to failing code is the most expensive habit in agentic development
- Review plans before code — human judgment has the highest leverage before implementation begins
Quick-start checklist:
- Create a plan file before your next implementation task (even a small one)
- Commit the plan to git alongside your code
- Use `/clear` between planning and implementation sessions
- The next time an approach fails, kill the branch and restart from a revised plan instead of patching
The metric to watch:
Time from “this approach is wrong” to “clean restart with a better plan.” Target: under 5 minutes.
Download Fact Sheet (SVG) →
## 9. What’s Next
You’ve got clean context (Principle 2), fresh documentation (Principle 3), and a versioned plan that survives session boundaries and bad branches alike. The planning workflow is solid. But what about the mistakes you made last month?
If your agent makes the same error your colleague fixed three weeks ago — uses the wrong date library, ignores a project convention, repeats an architectural anti-pattern that’s been solved before — your process has no memory. The plan for
this
feature is great, but the accumulated knowledge from every previous feature is trapped in closed PRs, old conversations, and someone’s head.
Principles 2, 3, and 4 handle the present. Principle 5 handles the past. It’s about building institutional memory — a living record of patterns, rules, and past mistakes that the agent consults on every task. Not documentation about
what
your system does, but codified knowledge about
how
your team works and
what never to do again.
That’s next.
<!-- fetched-content:end -->
