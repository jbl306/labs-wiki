---
title: "The Context Hygiene Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:35:43.464086+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/context-hygiene/"
content_hash: "sha256:ed233491fba9c2f6c06db33dd4d499512504fd8098b929ba75a718db37bf6a2b"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/context-hygiene/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:21:24+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/context-hygiene/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/context-hygiene/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. Context Rot
You’ve felt it. That creeping anxiety as your Claude session grows. The responses get slower. The quality drifts. You’re 47 messages deep and the model just suggested something you explicitly told it not to do 30 messages ago.
You check the conversation history. The instruction is right there — message 14 — clear as day. “Do not add default exports.” And yet, there it is in the latest response:
`export default`
. Not because the model is broken. Not because your instruction was ambiguous. Because your instruction is buried under 33 messages of code, corrections, tangents, and follow-ups, and the model’s attention mechanism physically cannot weight it as strongly as the 2,000 tokens of code you just pasted in message 46.
Welcome to context rot.
Most developers treat context like disk space — keep adding until it’s full, then wonder why performance degrades. But context is not disk space. It is not a filing cabinet. It is closer to working memory during a complex surgery: every instrument on the tray competes for your attention with every other instrument, and at some point, the one you actually need disappears into the noise.
The science behind this is more alarming than you think. And once you understand it, you’ll never approach a Claude session the same way again.
## 2. The Principle
The Context Hygiene Principle:
Context is your scarcest resource. Clear conversations aggressively, externalize every plan and artifact to focused files, and use minimal knowledge structures so the agent stays sharp and token-efficient.
Most developers do the opposite. They treat Claude sessions like ongoing conversations with a colleague — accumulating context over dozens of messages, trusting that the model “remembers” what was said earlier, loading every reference document and plugin “just in case.” The mental model is: more information equals better results.
The research says the exact opposite.
Every token you add to context actively competes with every other token for the model’s attention. This is not a metaphor. It is a mathematical consequence of the transformer architecture. When you have 5,000 tokens of focused context, the model’s attention is concentrated. When you have 150,000 tokens of accumulated conversation, that same critical instruction from message 14 is competing with 149,500 other tokens for attention weight. The instruction didn’t change. The competition did.
Context hygiene is the discipline of keeping that competition manageable — not by using less context, but by using the
right
context at the
right
time in the
right
position.
## 3. The Science
This is the first principle where the underlying science is not just supportive — it is the entire argument. Every recommendation in the tactical section traces directly to one of these findings.
### The Attention Budget
Anthropic’s context engineering guide (September 2025) introduced a concept that should reshape how every developer thinks about prompts: the
attention budget
. Context is a finite resource, and every token you add depletes it.
The mechanism is straightforward. LLMs are built on the transformer architecture (Vaswani et al., 2017), and the core operation is self-attention: every token attends to every other token, creating n-squared pairwise relationships. Double your context length and you quadruple the relationships competing for attention weight. At 10,000 tokens, the model manages 100 million pairwise relationships. At 100,000 tokens, that number is 10 billion.
The practical implication is blunt: every token you add that is not directly relevant to the current task is actively degrading performance on the tokens that are.
### The U-Shaped Attention Curve
Knowing that attention is finite is useful. Knowing
where
it concentrates is actionable.
Liu et al. (2024) published “Lost in the Middle,” one of the most practically important papers for anyone working with LLMs. They placed the answer to a question at different positions within a long context and measured accuracy. The result:
accuracy dropped by more than 30%
when the answer was in the middle compared to the beginning or end. The attention curve is U-shaped — strong at the start, strong at the finish, weak in the middle.
Wu et al. (2025) at MIT traced this to architectural causes. The U-shaped curve is not a quirk or a bug to be patched. It is a structural consequence of
causal masking
(early tokens cannot attend to later tokens) and
Rotary Position Embedding (RoPE)
, which creates inherent decay toward middle positions. This means the curve is baked into the architecture itself. You cannot prompt your way around it. You can only design for it.
The practical implication:
front-load critical information
(identity, vocabulary, hard constraints) so it sits at the high-attention beginning.
Back-load instructions and retrieval anchors
so they sit at the high-attention end. Never bury your most important content in the middle of a long prompt or a long conversation.
### The Optimal Zone
If context is finite and position matters, the natural question is: how much context should you actually use?
The research points to an optimal utilization zone of roughly
15-40% of the context window
. Below approximately 10%, the model starts hallucinating to fill information gaps — it does not have enough signal to constrain its output. Above approximately 60%, relevant information gets buried in noise and the quadratic attention dilution overwhelms the signal.
This is counterintuitive. Developers with 200K token windows assume they should use them. But a model at 20% utilization (40K tokens of focused context) will consistently outperform the same model at 80% (160K tokens of accumulated conversation). More is not better. Focused is better.
U-Shaped Attention Curve
Chart showing how LLM attention weight follows a U-shaped curve across context position, with high accuracy at start and end but a significant drop in the middle. Includes a context window utilization bar showing optimal fill ranges.
Start
Middle
End
Position in Context
Attention Weight / Accuracy
Low
High
HIGH
Front-load: identity, constraints
DANGER ZONE
30%+ accuracy drop (Liu et al., 2024)
HIGH
Back-load: instructions, retrieval anchors
Context Window Utilization
0%
10%
15%
40%
60%
100%
Hallucination risk
Optimal zone
Attention dilution
Figure 2: The U-shaped attention curve (Liu et al., 2024) and optimal context utilization zones.
### Progressive Disclosure
If you cannot load everything at once, you need a strategy for loading the right context at the right time. A four-layer model works well:
- Layer 1 (always loaded, ~200-500 tokens): Role identity and domain vocabulary. This is the minimum viable context that routes the model to the correct region of its knowledge.
- Layer 2 (task-triggered, ~500-2,000 tokens): Standard operating procedures and checklists relevant to the current task. Loaded when the task type is identified.
- Layer 3 (on-demand, 2,000+ tokens): Full documentation, detailed examples, reference material. Loaded only when specifically needed.
- Layer 4 (compressed): Summaries of large inputs. When you must reference a 50-page document, a structured summary preserves the key facts without the quadratic attention cost of the full text.
The key insight: you do not need the model to hold everything in context simultaneously. You need it to hold the right things at the right time.
Progressive Disclosure: 4-Layer Context Loading Stack
A funnel diagram showing four layers of context loading, from narrow permanent context at the top (L1) to wide ephemeral compressed context at the bottom (L4), illustrating how token cost increases with each layer.
Permanent → Ephemeral
L1
Always loaded
Identity + domain vocabulary
~200-500 tok
L2
Task-triggered
SOPs + checklists
~500-2K tok
L3
On-demand
Full docs + examples
2K+ tok
L4
Compressed
Summaries of large inputs
Variable
Narrow scope, always present
→
Broad scope, loaded as needed
Figure 3: Progressive disclosure loads the right context at the right time, from permanent identity to ephemeral summaries.
### Cross-Conversation Isolation
Each Claude conversation is completely isolated. The model has zero memory of previous sessions.
Justin Wetch documented this in January 2026: instructions like “never repeat yourself across sessions” or “remember what we discussed yesterday” are
dead instructions
. They require knowledge the model cannot have. Every instruction must be achievable within a single conversation’s context. If you need continuity, externalize it to files the next session can read.
This is liberating. Every
`/clear`
gives you a genuinely fresh start with full attention capacity. The model is not “forgetting” — it is resetting to peak performance.
### Context Poisoning
The final piece of the science is the most underappreciated. Stale context is not merely wasted tokens. It is
actively harmful
.
An outdated instruction in your CLAUDE.md actively misleads the model. A resolved issue still in conversation history causes the model to re-address a problem that no longer exists. Verbose examples that are no longer representative route the model toward outdated patterns.
Context poisoning is worse than context bloat. Bloat dilutes attention passively. Poisoned context misdirects it actively.
## 4. Before and After
### Before: The 47-Message Death Spiral
The session starts clean. You describe the feature. Claude nails the implementation in message 3. Then you ask for a modification. Then a test. Then a refactor of something tangentially related. Then you paste in an error log.
By message 20, you notice the first drift. Claude suggests a pattern you already rejected in message 8. By message 30, the responses are slower and more generic — the model is hedging because it is drowning in competing signals. By message 40, you are fighting the tool more than collaborating with it.
You have 47 messages of history. Your CLAUDE.md loads 3,000 tokens. You have 12 MCP servers and 8 plugins loaded, most unused for this task. The tokens that actually matter for your current task represent maybe 5% of the total context. You are operating a precision instrument with the signal-to-noise ratio of a crowded bar.
### After: Focused Sessions with Externalized State
Same developer. Same project. Different discipline.
You describe the feature. Claude nails the implementation. You save the plan and current state to a markdown file. You run
`/clear`
.
New session. You reference the plan file. Claude reads it fresh — full attention, no dilution from 20 messages of prior tangents. You ask for the tests. Claude writes them cleanly because 100% of its attention budget is allocated to the test-writing task, not to the ghost of a refactoring discussion from 30 minutes ago.
Each unit of work gets a fresh session. The plan file bridges sessions. Context stays focused. Quality stays high. Token spend drops because you stop paying for 47 messages of accumulated history on every subsequent response.
The feeling of “context anxiety” disappears entirely. Not because the model changed. Because the signal-to-noise ratio stayed high.
## 5. Tactical Implementation
These steps are ordered by impact. Start with the first three and add the rest as your discipline matures.
1. Clear conversations aggressively.
Run
`/clear`
between units of work. A “unit of work” is one coherent task: implement a feature, write tests for it, review a PR, debug a specific issue. When the task shifts, clear the context and start fresh. The cost of re-establishing context from an externalized plan file is trivially small compared to the cost of operating in a polluted 47-message session.
2. Externalize every plan, artifact, and reference to focused files.
Before you
`/clear`
, save the current state. Plans go in plan files. Decisions go in ADRs. Artifacts go in their target files. The next session reads what it needs from disk — fresh, focused, and positioned at the high-attention beginning of the new context. Files on disk are permanent. Conversation context is ephemeral. Treat them accordingly.
3. Use minimal knowledge structures.
Your CLAUDE.md should be lean — core identity, project vocabulary, hard constraints, and pointers to deeper docs. Not a 5,000-token encyclopedia of every convention you have ever established. Project rules (
`.claude/rules/`
) should be focused and categorical, not monolithic. If your CLAUDE.md is longer than 500 lines, it is consuming attention budget on every single interaction whether the content is relevant or not.
4. Front-load critical information in any prompt.
When you write a prompt or structure a CLAUDE.md, put the most important content first: identity, vocabulary, non-negotiable constraints. The U-shaped attention curve means the beginning of your context gets disproportionate attention weight. Use that real estate for what matters most.
5. Back-load retrieval anchors and instructions.
Place “Questions This Skill Answers” sections, checklist items, and step-by-step instructions at the end of documents. The end of context also receives strong attention weight. The middle is the dead zone — use it for reference material that supports but does not drive behavior.
6. Audit your loaded plugins and MCP servers.
Every plugin and MCP server you have connected injects tool definitions into the system prompt. If you have 15 loaded but only need 3 for the current task, those 12 unnecessary plugins are consuming attention budget for zero value. They are not free. They are actively diluting attention from the tools you actually need. Disable what you are not using.
7. Manage your tool loading per session.
We built
jig
(
github.com/jdforsythe/jig
) to handle this. It selectively enables and disables plugins, MCP servers, skills, and hooks per Claude session using project-checked-in config files. Install dozens of focused tools across your system. Load only the handful needed for the current task. The rest stay dormant, consuming zero attention budget. Full deep-dive in Principle 10.
## 6. Common Pitfalls
### “Kitchen Sink Context”
What happens:
You load every reference document, every plugin, every MCP server “just in case.” Your CLAUDE.md is 4,000 tokens. You have 15 tools connected. You paste entire error logs instead of the relevant 10 lines.
Why it fails:
Every unnecessary token competes with every necessary token. The quadratic scaling of self-attention means this is structural degradation, not minor inefficiency. “Just in case” context pays a guaranteed cost for a speculative benefit.
What to do instead:
Load the minimum viable context for the current task. Add more on demand. Progressive disclosure is not laziness — it is architecture.
### “Never Clearing”
What happens:
You treat Claude sessions as persistent workspaces. One session for the whole morning. Sessions that stretch to 50, 80, 100+ messages.
Why it fails:
Every prior message competes with the current task for attention. The model cannot selectively ignore old messages — it attends to everything. By message 50, your current instruction is one voice in a crowd of 49.
What to do instead:
Clear between units of work. Externalize state to files first. A fresh session with a focused plan file outperforms a 50-message session every time.
### “Context Poisoning”
What happens:
Your CLAUDE.md still contains instructions from three months ago that no longer apply. Old conventions superseded by new ones. Workarounds for bugs that were fixed.
Why it fails:
The model has no way to know an instruction is outdated. It treats everything in context as current and authoritative. One stale line can override ten correct ones if attention happens to weight it strongly.
What to do instead:
Audit your CLAUDE.md and project rules monthly. Remove anything that no longer applies. Treat context files like code — they need maintenance, review, and pruning.
### “Ignoring Position”
What happens:
You write a 2,000-token prompt with the critical constraint buried in paragraph 4 of 6. You structure your CLAUDE.md with the most important rules in the middle.
Why it fails:
The U-shaped attention curve is not optional. Middle content receives measurably less attention — 30%+ less, per Liu et al. Critical instructions in the middle may as well be whispered in a noisy room.
What to do instead:
Put your hardest constraints in the first few lines. Put your step-by-step instructions at the end. Use the middle for supporting context that is helpful but not critical.
## 7. Expected Impact
Cut token spend 40-90% while improving output quality. That is not a typo — those numbers move in the same direction.
Sessions that used to degrade after 30 messages now stay sharp because you clear and restart with focused context. The model at message 3 of a fresh session with a plan file performs identically to the model at message 3 of the original session. You have eliminated degradation by eliminating accumulation.
In concrete terms: developers who adopt aggressive clearing and externalized state report fewer correction cycles per task, less time fighting the model on previously-stated constraints, and a dramatic reduction in the “context anxiety” that makes long sessions feel like they are working against you. The signal-to-noise ratio stays high because you keep the noise low.
## 8. Fact Sheet
Principle:
The Context Hygiene Principle
One-sentence definition:
Context is your scarcest resource — clear conversations aggressively, externalize state to files, and load only what the current task demands.
The science:
Self-attention creates n-squared pairwise relationships between tokens, and accuracy drops 30%+ when critical information lands in the middle of context (Liu et al., 2024).
5 key takeaways:
- Every token competes with every other token for attention weight — irrelevant tokens actively degrade performance
- The U-shaped attention curve means position matters: front-load constraints, back-load instructions
- The optimal context utilization zone is 15-40% of the window — more is not better
- Each conversation is completely isolated; design for single-session completeness
- Stale context is worse than no context — it actively misdirects the model
Quick-start checklist:
- Run `/clear` between every distinct unit of work
- Save plans and state to files before clearing so the next session can pick up cleanly
- Audit your CLAUDE.md — if it exceeds 500 lines, trim it
- Disable plugins and MCP servers you are not actively using for the current task
- Put your hardest constraints in the first few lines of any prompt or config file
The metric to watch:
Messages per session before quality degrades. If the answer was “30 and then it drifts,” it should now be “never, because I clear at 10.”
Download Fact Sheet (SVG) →
## 9. What’s Next
Clean context is powerful. You clear aggressively, externalize state to files, and load only what the current task demands. Your sessions stay sharp. Your token spend drops. The model operates in its optimal zone.
But there is a catch. All that externalized state — the plan files, the conventions, the CLAUDE.md rules — has to be
accurate
. And documentation has a natural enemy: time.
The moment you externalize your project conventions to a file and walk away, entropy starts. Conventions evolve. Dependencies update. Patterns that made sense six months ago become anti-patterns today. And if the documentation your agent reads on every session is stale, you have not solved the context problem — you have just moved it to a slower-burning fuse.
Like the time one outdated line about
`Array<T>`
sat in a markdown file nobody remembered editing. It took three days of cascading ESLint violations before anyone traced it back. One stale instruction. Three days.
That is Principle 3: The Living Documentation Principle. Documentation is not a write-once artifact. It is a living system that requires automated freshness checks, structured formats, and the same maintenance discipline you give your code. Because if your agent’s context is clean but its source-of-truth is rotten, you have just traded fast failure for slow failure.
<!-- fetched-content:end -->
