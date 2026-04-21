---
title: "The Observability Imperative | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:36:59.320052+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/observability/"
content_hash: "sha256:840ac6c20a0a2cc87d4d81f8dfbe51a2b9c057f97fa6e407123755f32a61d968"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/observability/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T00:07:45+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/observability/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/observability/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The Invisible Catastrophe
There are 14 documented failure modes in multi-agent systems. Communication failures like message loss and misinterpretation. Coordination failures like deadlock and role confusion. Quality failures like rubber-stamp approval and error cascading. Want to know the terrifying part? Most of them are completely invisible without logging.
Your pipeline could be failing in six different ways right now, and you would have no idea until the final output is obviously, catastrophically wrong.
You built a multi-step agentic workflow. An agent plans, another implements, a third reviews. The output looks reasonable most of the time. So you trust it. But behind the scenes, the review agent is approving everything in under two seconds. The planning agent’s output occasionally never reaches the implementation agent — silently dropped, silently regenerated with different assumptions. The implementation agent is sometimes working from a stale version of the plan.
None of these failures produce error messages. None of them crash the pipeline. They degrade output quality in ways that are intermittent, subtle, and indistinguishable from normal LLM variance. You shrug at the occasional mediocre result and chalk it up to “LLMs being LLMs.”
It is not the LLM. It is your pipeline. And without observability, you will never know the difference.
MAST Failure Taxonomy Quick Reference
Three-column reference of 14 multi-agent failure modes across Communication, Coordination, and Quality categories, each with detection strategies.
MAST Failure Taxonomy
Communication
FM-1.1
Message Loss
Agent output not received by next agent
Detect:
Hash handoff payloads
FM-1.2
Misinterpretation
Instruction understood differently than intended
Detect:
Require structured formats
FM-1.3
Info Overload
Too much context degrades performance
Detect:
Monitor token counts
FM-1.4
Stale Context
Outdated information in active context
Detect:
Timestamp all context
Coordination
FM-2.1
Deadlock
Agents waiting on each other
Detect:
Timeout all operations
FM-2.2
Race Condition
Output depends on execution order
Detect:
Sequence-number handoffs
FM-2.3
Role Confusion
Overlapping or unclear responsibilities
Detect:
Single-responsibility identities
FM-2.4
Authority Vacuum
No agent empowered to decide
Detect:
Explicit decision owners
FM-2.5
Resource Contention
Multiple agents modifying same resource
Detect:
Lock or queue shared resources
Quality
FM-3.1
Rubber-Stamp Approval
Reviewer approves without scrutiny
Detect:
Require specific citations
FM-3.2
Error Cascading
One agent's mistake amplified downstream
Detect:
Validate at each handoff
FM-3.3
LCD Output
Lowest-common-denominator quality
Detect:
Domain-specific quality bars
FM-3.4
Groupthink
Agents converge on same approach
Detect:
Diversity in specialist prompts
FM-3.5
Regression
Later agent undoes earlier agent's work
Detect:
Immutable completed sections
Figure 8: The MAST taxonomy — 14 failure modes that are invisible without structured logging.
## 2. The Principle
Log every tool call, LLM interaction, plan artifact, and workflow outcome with full inputs, outputs, model versions, and hashes. The entire system must be reproducible, debuggable, and auditable — no black boxes.
Most developers build agentic workflows the way they build weekend projects: get it working, ship it, move on. Logging is an afterthought. The pipeline is a black box with an input and an output, and as long as the output looks right, nobody looks inside.
This works when your system is a single deterministic function. It does not work when your system involves multiple probabilistic agents making decisions, passing artifacts, and reviewing each other’s work. In that world, the space between “input” and “output” is where every interesting failure lives. Without structured observability, you are operating on faith.
The cost of that faith is not just the occasional bad output. It is the inability to improve. You cannot optimize a system you cannot measure. You cannot debug a handoff you did not log. You cannot detect rubber-stamp approvals if you never recorded the approval latency. Observability is the infrastructure that makes every other principle in this series measurable.
## 3. The Science
Two bodies of research converge here: the structured artifact approach that creates audit trails by design, and the failure taxonomy that catalogs what goes wrong when you cannot see inside your pipeline.
### Structured Artifacts as Audit Trail
Hong et al. (2023) published MetaGPT, a framework where multi-agent teams exchange structured artifacts — requirements documents, design specs, code modules with defined interfaces — rather than free-form dialogue. Teams using structured artifact exchanges had approximately 40% fewer errors than those relying on unstructured conversation.
But the error reduction is only half the story. The more consequential finding is what structured artifacts create as a side effect: a complete, inspectable record of every decision the system made.
In a structured pipeline, the sequence of artifacts tells the full story. Agent A produced Artifact 1 with these contents at this timestamp. Agent B received Artifact 1 and produced Artifact 2. Agent C reviewed Artifact 2 and produced a review report with these findings. Every step is a discrete, inspectable object. When the final output is wrong, you trace the artifact chain backward until you find where the error entered. The debugging process is linear, mechanical, and fast.
In a free-dialogue system, you have none of this. To reconstruct what happened, you must read the entire conversation — every message, every tangent, every implicit assumption. You are doing archaeology, not debugging. And archaeology is slow, expensive, and unreliable.
Anthropic’s “Building Effective Agents” guide (December 2024) reinforces this by recommending structured handoffs — typed inputs, typed outputs, explicit interfaces — as the default pattern. Not because structure is inherently virtuous, but because structure is inherently observable. When every handoff has a defined shape, the observability is built into the architecture.
The mechanism is straightforward: artifact chains are debuggable; conversation logs are archaeology.
### MAST Failure Modes Detectable Only Through Observability
The MAST framework (2024-2025) documents 14 distinct failure modes in multi-agent systems, organized into three categories: communication failures, coordination failures, and quality failures. Most of these failure modes are invisible without explicit logging. They do not crash the pipeline. They silently degrade output quality in ways that are impossible to diagnose without the right instrumentation.
Four failure modes illustrate the pattern:
FM-1.1 — Message Loss.
An agent’s output never reaches the next agent. The downstream agent proceeds without it, either regenerating from scratch or working with a default. The pipeline looks like it succeeded. Only by logging every handoff and confirming receipt can you detect that an artifact was lost in transit.
FM-1.4 — Stale Context.
An agent acted on outdated information. The plan was updated, but the implementation agent was already working from the previous version. The result is code that implements the old plan correctly — a subtle failure that passes cursory review. Detectable only by logging timestamps at each handoff and comparing them.
FM-3.1 — Rubber-Stamp Approval.
The review agent approved a submission too quickly, with no substantive feedback. It said “LGTM” in 1.8 seconds to a 200-line implementation. If your average review takes 2 seconds and approves 94% of submissions, you do not have a review process. You have a rubber stamp. You will never know that without logging both the time and the content of every approval.
FM-3.2 — Error Cascading.
One agent’s mistake propagated through the entire pipeline. The planning agent made an incorrect assumption. The implementation agent implemented it faithfully. The review agent approved because it matched the plan. Every agent did its job correctly relative to its input. Traceable only with hashed artifact chains that let you reconstruct the exact state each agent received and produced.
The common thread: none of these failures announce themselves. They all require you to have logged the right data before the failure occurred. Observability is not something you add after a problem surfaces. It is something you build before problems become invisible.
## 4. Before and After
Black Box vs Observable Pipeline
Comparison of two agent pipelines. The top black-box pipeline hides failures between handoffs, making debugging archaeological. The bottom observable pipeline logs every handoff with hashes, timestamps, and metrics, making debugging a simple lookup.
Black Box
Planner
FM-1.1?
Implementer
FM-2.3?
Reviewer
Output
?
Failures invisible. Debugging is archaeology.
Observable
Planner
abc123 → abc123
12:04:31
Implementer
d4e5f6 → d4e5f6
12:04:58
Reviewer
Approval: 94% in 2.1s
Output
Every handoff logged. Debugging is lookup.
Figure 9: Observability transforms debugging from archaeology to lookup.
### Before: The Black Box Pipeline
The pipeline runs. Three agents — planner, implementer, reviewer — work in sequence. The developer kicks it off with a task description and receives a final output: reviewed, approved code. When the output is good, it is very good. When it is bad, it is baffling.
Every few runs, the output misses requirements from the plan. The developer tweaks the system prompt, reruns, gets a good result. Problem solved — until the same failure appears two days later. Other times, the review agent’s feedback is suspiciously thin. “Looks good, all requirements met.” Weeks later, a pattern emerges: the review agent has not rejected a single submission in 47 runs. Not one. Is the implementation always perfect, or is the review always shallow? Without data, there is no way to tell.
The most insidious failures are the ones that look like successes. The output exists. It compiles. It mostly works. No log of what each agent received, what it produced, how long it took, or what version of the model it was running. Debugging means re-running with print statements and staring at raw conversation logs. The developer’s mental model of the pipeline is based on assumption. The pipeline’s actual behavior is unknowable.
### After: The Observable Pipeline
Same three agents. Same workflow. Different infrastructure. Every tool call logged with full inputs and outputs. Every LLM interaction logged with the model version, temperature, and system prompt hash. Every artifact handoff logged with a content hash, a timestamp, and the producing and consuming agents.
When the output misses a plan requirement, the developer queries the handoff log. Agent A produced plan artifact
`abc123`
at 14:32:07. Agent B received
`abc123`
at 14:32:08. Receipt confirmed — the plan was not lost. Diff the plan against the implementation. Missed requirement found in 90 seconds. System prompt was missing a key instruction. Fix deployed in five minutes.
When the review seems thin, the developer queries the approval metrics. Average review latency: 2.1 seconds. Approval rate: 94%. Rubber-stamp pattern obvious from the data. The developer restructures the review prompt to require at least one specific finding with evidence. Approval rate drops to 71%. The reviews that pass are meaningfully reviewed.
When an error cascades, the developer traces the hashed artifact chain backward. Implementation faithfully implements the plan. The plan contains the error. The planning agent’s input is logged — the original task description was ambiguous. Developer refines the task template. The entire category of error is eliminated.
Every improvement is data-driven. Every diagnosis is fast. The developer’s mental model matches reality because reality is logged.
## 5. Tactical Implementation
Here is how to add observability to your agentic workflows, ordered from highest impact to most sophisticated.
1. Log every tool call with full inputs and outputs.
This is the single highest-leverage observability investment. Every time an agent calls a tool — file read, file write, API call, code execution — log the tool name, full input arguments, full output, and wall-clock duration. Use structured JSON, not printf. When you need to find every file write that took longer than 5 seconds, a JSON log is a database query. A text log is a grep expedition.
```
{
"event"
:
"tool_call"
,
"agent"
:
"implementer"
,
"tool"
:
"file_write"
,
"input"
:
{
"path"
:
"src/auth.ts"
,
"content_hash"
:
"a1b2c3"
},
"output"
:
{
"success"
:
true
,
"bytes_written"
:
1847
},
"duration_ms"
:
34
,
"timestamp"
:
"2026-03-28T14:32:08.441Z"
}
```
2. Log model version, parameters, and system prompt hash for every LLM interaction.
When output quality changes, you need to know whether the model changed, the temperature changed, or the system prompt changed. Log the model identifier, temperature, max tokens, and a system prompt hash for every LLM call. This makes “it worked yesterday” solvable: diff yesterday’s logs against today’s and find the variable that changed.
3. Hash artifacts at each handoff point.
When Agent A produces output and Agent B consumes it, hash the content at both ends. Matching hashes mean a clean handoff. Mismatched hashes mean message loss. Hashing also enables diff-based debugging: when two pipeline runs produce different outputs, compare artifact hashes at each stage to find the exact point of divergence.
4. Use structured logging — JSON, not printf.
Unstructured text logs are a shoebox full of receipts. They contain the information, but finding it requires reading everything sequentially. Structured JSON logs are a database — queryable with
`jq`
, aggregatable by agent or tool or time range, piped into dashboards. The marginal cost over printf is near zero. The debugging speed improvement is orders of magnitude.
5. Record approval latency and content for review steps.
For every review action, log the time between receipt and response, plus the full content of the review. This catches rubber-stamp approval. An approval that took 1.8 seconds and contains only “LGTM” is a data point. Fifty of them in a row is a pattern. You cannot detect the pattern without the data.
6. Build a pipeline viewer.
Even a simple CLI tool that reads your structured logs and prints the artifact chain — Agent A produced X, Agent B received X, Agent B produced Y, Agent C reviewed Y — transforms debugging from log-spelunking to reading a report. As your pipelines mature, this can evolve into a web UI with diff views and timeline visualization. But start with a script that prints the chain. That alone is a step change.
7. Version your observation config alongside code.
Your logging configuration should live in version control next to the code it instruments. When someone changes the pipeline, the logging changes with it. Forge’s structured artifact definitions make every handoff inherently auditable by design. jig configs are versioned system state — your observation setup should receive the same treatment.
## 6. Common Pitfalls
### “Black Box Pipelines”
What happens:
No logging at all. The pipeline has an input and an output, and everything between is invisible. The developer trusts the output because it usually looks reasonable.
Why it fails:
“Usually looks reasonable” is not a quality metric. Without logging, you cannot distinguish between a pipeline that works correctly 95% of the time and one that works correctly 60% of the time with plausible-looking failures in the other 40%. You are trusting the system on faith, and faith is not an engineering discipline.
What to do instead:
Start with tool call logging (Tactical Step 1). It takes 30 minutes to implement and immediately makes every pipeline run inspectable.
### “Printf Debugging”
What happens:
The developer adds logging, but it is unstructured text —
`print(f"Agent {name} called {tool} at {time}")`
. The logs exist but are walls of text that require manual reading.
Why it fails:
Unstructured logs scale linearly with effort. Ten runs produce logs you can scan manually. A thousand runs produce logs nobody will ever read. You cannot aggregate, query, or filter printf output without writing a parser for your own ad-hoc format — which is building a structured logging system with extra steps.
What to do instead:
Use JSON from the start. The marginal cost is negligible. The downstream value is transformative.
### “Logging Too Much”
What happens:
The developer logs everything — every token, every intermediate thought, every internal model state. Log files are gigabytes per run. Nobody reads them because the signal is buried in noise.
Why it fails:
Observability is not about volume. It is about signal. Comprehensive logging can be less useful than targeted logging because the cost of extraction exceeds the value of the information.
What to do instead:
Log at the boundaries — tool calls, LLM interactions, artifact handoffs, review actions. These are the points where agents interact with each other and with the outside world. Log the what, the when, and the who. Skip the internal monologue.
### “Logging Output but Not Inputs”
What happens:
The developer logs what each agent produced but not what it received. When the output is wrong, they can see the bad result but cannot determine why it was produced.
Why it fails:
Outputs without inputs make diagnosis impossible. You can see that Agent B produced incorrect code, but you cannot tell whether it received an incorrect plan (Error Cascading), a stale plan (Stale Context), or no plan at all (Message Loss). Every diagnosis becomes speculation.
What to do instead:
Always log both sides of every interaction. Input hash, output hash, timestamps on both. The cost of logging inputs is marginal. The cost of not logging them is hours of guesswork.
## 7. Expected Impact
Mean time to debug agent failures dropped from hours to minutes. When you can query structured logs instead of reading conversation transcripts, debugging becomes lookup instead of investigation.
The more revealing metric surfaced within the first day of logging: the review agent was approving 94% of submissions with an average review time of 2 seconds. The rubber-stamp pattern was immediately obvious from the data — and completely invisible without it. That single finding led to restructuring the review prompt, dropping the approval rate to 71% and meaningfully improving output quality. One day of observability data drove a structural improvement that months of “it seems fine” had missed.
Beyond individual debugging, observability enables trend analysis. Track approval rates over time. Identify which task types produce the most handoff failures. Measure whether a system prompt change actually improved quality or just shifted which failures occurred. The pipeline stops being something you hope works and becomes something you know works — because you have the data.
## 8. Fact Sheet
Principle:
The Observability Imperative
One-sentence definition:
Log every tool call, LLM interaction, and artifact handoff with full inputs, outputs, model versions, and hashes — no black boxes.
The science:
MetaGPT’s structured artifacts reduce errors ~40% (Hong et al., 2023) AND create inherent audit trails; the MAST taxonomy’s 14 failure modes are mostly invisible without logging.
5 key takeaways:
- Structured artifact chains are debuggable; conversation logs are archaeology
- Most multi-agent failure modes (message loss, stale context, rubber-stamping, error cascading) are invisible without explicit logging
- Use structured logging (JSON) from the start — the cost is negligible, the debugging speed improvement is orders of magnitude
- Log at the boundaries: tool calls, LLM interactions, artifact handoffs, review actions
- Always log both inputs and outputs — outputs without inputs make diagnosis impossible
Quick-start checklist:
- Add structured JSON logging to every tool call in your pipeline (inputs, outputs, duration)
- Log model version and system prompt hash for every LLM interaction
- Hash artifacts at handoff points and verify receipt
- Record approval latency and content for every review step
- Build a minimal pipeline viewer that prints the artifact chain from logs
The metric to watch:
Review approval rate and latency — if your review agent approves more than 85% of submissions in under 5 seconds, you have a rubber stamp, not a reviewer.
Download Fact Sheet (SVG) →
## 9. What’s Next
You can see everything now. Every tool call, every handoff, every approval. You can trace an error back to its origin in minutes. You can detect rubber-stamp approvals from the data. You can identify stale context from timestamp comparisons.
But observability without the authority to stop bad output is just watching the train wreck in slow motion.
Your logs tell you the review agent approved a security vulnerability in 1.3 seconds. Your artifact chain shows the error cascading through three agents. And all of it happens after the fact, because no human was in the loop to catch it before it shipped.
At some point, a human needs to step in. The question is not whether — it is where. Too many checkpoints and you become the bottleneck. Too few and mistakes propagate unchecked through a pipeline that faithfully logs every step of its own failure.
That is Principle 8: The Strategic Human Gate Principle.
<!-- fetched-content:end -->
