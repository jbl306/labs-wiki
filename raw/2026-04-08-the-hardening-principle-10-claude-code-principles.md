---
title: "The Hardening Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:35:35.786069+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/hardening/"
content_hash: "sha256:fd4be2da162f9b5e98130628d8e173ac7de3b46fd7c1c6df70682ba673369bd7"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/hardening/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:23:02+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/hardening/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/hardening/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The War Story
The recording stopped. Ffmpeg converted. Whisper transcribed. Claude summarized. And then… nothing happened. No Obsidian note. No wikilinks. Just a silent failure in a pipeline that worked yesterday.
I had built what I thought was a clever meeting transcription workflow. A microphone on my Mac captured the audio. An LLM-orchestrated pipeline took it from there: ffmpeg converted the recording to WAV, Whisper transcribed the audio to text, Claude summarized the transcript and generated an Obsidian note complete with wikilinks to relevant projects, people, and topics. The whole thing ran end-to-end with zero human intervention after I hit the stop button.
When it worked, it was magic. I would finish a meeting, press a key, walk away, and come back to a perfectly structured note sitting in my vault. Tags applied. Links resolved. Action items extracted. The kind of workflow that makes you feel like you are living in the future.
The problem was the word “when.”
Some days the pipeline ran flawlessly. Other days, it silently ate my recording and produced nothing. No error. No partial output. Just… nothing. I would realize hours later that I had no notes from that morning’s architecture discussion. The failure modes were maddening in their variety. Sometimes the WAV conversion would succeed but the transcription step would hang. Sometimes the transcription would complete but the summarization would hallucinate structure that broke the Obsidian parser. Sometimes the wikilink generation would reference pages that did not exist or, worse, link to the wrong project entirely.
Every failure triggered the same ritual: restart the pipeline, stare at the logs (such as they were), mutter “it worked yesterday,” and manually reconstruct the notes from memory. I was spending more time debugging the automation than the automation was saving me. The pipeline had become a net negative — all the cognitive overhead of maintaining it with none of the reliability I needed from it.
That pipeline taught me the first and most important lesson of working with AI agents. And it is the foundation everything else in this series builds on.
## 2. The Principle
Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool built with Claude’s help. Claude prototypes and orchestrates; the developer hardens it into reliable code and pulls the LLM back to the role of caller only.
Most people treat LLMs as runtime engines. They build workflows where the model is responsible for executing multi-step processes — file conversions, API calls, data transformations, file I/O — and then act surprised when those workflows are unreliable. The instinct makes sense: the LLM can do all of these things, and watching it chain them together feels like the entire point of agentic AI.
But there is a fundamental mismatch between what LLMs are good at and what production workflows require. LLMs excel at fuzzy reasoning: summarization, classification, creative generation, intent extraction, synthesizing unstructured information into structured output. These are tasks where “close enough” is the right answer and where no two correct outputs need to be identical. Production workflows, on the other hand, require steps that behave identically every time. Converting audio to WAV is not a creative act. Writing a file to disk is not a judgment call. Generating wikilinks from a known set of page titles is not a task that benefits from probabilistic reasoning.
The mistake is using a probabilistic system for deterministic work. And the cost of that mistake is not just unreliability — it is the invisible tax of never fully trusting your own tools. You check the output. You re-run “just to be sure.” You build in manual verification steps that defeat the purpose of automation. The entire value proposition of the workflow erodes because you cannot trust the foundation.
The Hardening Principle says: identify those deterministic steps, build them as reliable code, and let the LLM do only what LLMs do best.
## 3. The Science
This principle is more engineering discipline than LLM research finding, but the underlying science explains why the discipline matters.
LLMs are probabilistic systems. Every output is sampled from a distribution of possible next tokens, weighted by the model’s learned parameters and the current context. Even at temperature zero, the model is selecting the single most probable token at each step — which means the output is a function of the entire context window, including every token of every previous step. Change one word in a prompt, and the downstream output can shift unpredictably. This is not a bug. It is the fundamental mechanism that makes LLMs capable of creative, flexible reasoning. But it is also the mechanism that makes them unreliable for tasks that demand identical behavior across runs.
Deterministic systems, by contrast, produce the same output for the same input every time. An ffmpeg command that converts audio to WAV will produce byte-identical output on every execution. A function that generates wikilinks from a lookup table will produce the same links for the same inputs, forever. The behavior is defined by the code, not inferred from patterns.
The reliability gap between these two paradigms is not marginal. It is categorical. A deterministic tool either works or fails loudly with a stack trace you can debug. A probabilistic system can fail in ways that look like success — generating plausible but incorrect output, silently dropping steps, producing subtly different results on each run. These are the failures that erode trust, because you cannot distinguish success from failure without inspecting every output.
This distinction matters for agentic workflows because most workflows contain both types of steps. The meeting pipeline had genuinely fuzzy steps (summarize this transcript, extract action items, determine which projects are relevant) mixed with purely mechanical steps (convert audio format, write file to disk, generate Markdown with specific syntax). The fuzzy steps benefit from LLM involvement. The mechanical steps do not — they only suffer from it.
The engineering discipline is separation of concerns applied to the probabilistic-deterministic boundary. Fuzzy reasoning gets the LLM. Mechanical execution gets deterministic code. Each component operates in its zone of reliability.
The same pattern applies to any fuzzy workflow. Wherever you find a process that mixes creative reasoning with mechanical execution, you will find an opportunity to harden the mechanical parts and improve the reliability of the whole.
## 4. Before and After
Before and After Pipeline Architecture
Comparison of a monolithic LLM pipeline where the model handles all steps unreliably versus a hardened pipeline that separates mechanical tool steps from LLM reasoning, improving reliability from roughly 70 percent to 100 percent.
BEFORE
LLM handles everything
Convert Audio
Transcribe
Generate Wikilinks
Summarize
Extract Actions
~70% reliable
Harden
mechanical steps
AFTER
Deterministic
FFmpeg
Convert
Whisper
Transcribe
Vault Linker
Wikilinks
Probabilistic
Summarize
+ Extract
100% reliable
Hardened tools
LLM only where needed
Figure 1: Separating deterministic steps from probabilistic reasoning transforms reliability from ~70% to 100%.
Before: The Flaky Pipeline
The original workflow was a single LLM-orchestrated chain. Claude received a system prompt describing the entire pipeline and executed it step by step: call ffmpeg, call Whisper, summarize the transcript, generate the Obsidian note with wikilinks, write the file. Every step depended on the LLM correctly constructing a command or generating output in a precise format. Every step was a point of failure.
The ffmpeg step failed when Claude put a flag in the wrong position or mishandled a path with special characters. The Whisper step failed when the model chose different parameters across runs. The wikilink step was the most fragile: it required exact page titles from my Obsidian vault, and the LLM would confidently generate links to pages that did not exist or link to pages with similar but wrong titles.
Debugging was miserable. Failures were silent. Even when I added error handling to the prompt, the LLM’s error reporting was inconsistent — sometimes noting the failure, sometimes hallucinating success. I was stuck in the uncanny valley of automation: too automated to do manually, too unreliable to trust.
After: The Hardened Pipeline
The hardened version separates concerns cleanly. A deterministic CLI orchestrator handles every mechanical step: audio conversion, file I/O, Obsidian note creation, wikilink resolution against the actual vault index. These steps are implemented in code — tested, logged, and completely predictable.
The LLM’s role is reduced to exactly two tasks where fuzzy reasoning is genuinely required: interpreting the user’s intent (did they want to transcribe, summarize, or both?) and transforming unstructured transcript text into a structured note (summary, action items, key decisions, relevant topics). Everything else is deterministic.
The result is a single command. I stop the recording, hit Enter, and the pipeline runs to completion. Every time. If a step fails, it fails loudly with a clear error message identifying exactly what went wrong. The logs show every step, every input, every output. The wikilinks are correct because they resolve against the actual vault index, not the LLM’s guess at what pages might exist.
I have not had a single silent failure since hardening the pipeline. Not one. The workflow went from “it worked yesterday maybe” to a tool I use without thinking about — which is what automation is supposed to be.
## 5. Tactical Implementation
Here is how to apply the Hardening Principle to your own workflows, starting tomorrow.
Step 1: Map every LLM-powered step in your workflow.
Write down every point where an LLM is doing work. Be specific. Not “Claude handles the transcription pipeline” but “Claude calls ffmpeg with these arguments,” “Claude parses Whisper output,” “Claude generates Markdown with wikilinks,” and so on. You cannot harden what you have not identified.
Step 2: Categorize each step — does it need fuzzy reasoning or reliable execution?
For each step, ask: would a correct implementation of this step produce the same output for the same input every time? If yes, it is a deterministic step and a candidate for hardening. If no — if the step genuinely benefits from creativity, judgment, or synthesis — it belongs with the LLM. Be honest about this categorization. Many steps feel fuzzy but are actually mechanical. “Generate a filename from the meeting date and title” is not a creative act. “Summarize the key decisions from a rambling two-hour discussion” is.
Step 3: Prototype the deterministic replacement with Claude’s help.
This is the beautiful irony of the Hardening Principle: you use the LLM to build the tool that replaces the LLM. Ask Claude to write the script, the CLI command, the function that handles the deterministic step. Claude is an excellent prototyping partner. It can generate the ffmpeg wrapper, the file I/O handler, the Markdown template, the wikilink resolver. Let it build the first draft. Then test it, fix the edge cases, and harden it yourself.
Step 4: Build the hardened tool.
Take the prototype and turn it into a proper tool: a CLI script, a serverless function, an MCP server, whatever fits your infrastructure. The key attributes of a hardened tool are: it accepts well-defined inputs, produces well-defined outputs, fails loudly on error, and behaves identically on every run. No LLM in the loop for execution. Code only.
Step 5: Pull the LLM back to caller role only.
Restructure your workflow so the LLM’s job is limited to deciding which tool to call and with what arguments, and to performing any genuinely fuzzy transformations on the tool’s output. The LLM is the orchestrator and the reasoning engine. The hardened tools are the execution layer. The LLM says “convert this audio file”; the tool converts it. The LLM says “write this note to Obsidian”; the tool writes it. The LLM never touches the mechanical execution.
Step 6: Test the hardened version independently.
Run the hardened tool outside of any LLM context. Feed it known inputs and verify the outputs. Run it 50 times with the same input and confirm identical output. Test the error cases: malformed input, missing files, network failures. The tool should handle every case deterministically, with clear error messages. If you cannot test it independently, it is not properly hardened.
Step 7: Log and monitor.
Every invocation of the hardened tool should produce a log entry: what was called, with what arguments, what was returned, how long it took. This is a preview of Principle 7 (Observability), but even at this stage, basic logging transforms debugging from archaeology into reading a report. When something fails — and eventually something will — the logs tell you exactly where and why.
## 6. Common Pitfalls
“Hardening Too Early”
You identified a workflow three days ago and you are already writing production-grade tooling for it. The problem: the workflow is not stable yet. You are still figuring out the steps, the inputs, the outputs, the edge cases. Hardening a workflow that is still changing means building tools you will immediately need to rebuild.
The fix: let the LLM run the fuzzy version until the workflow is stable. Use the LLM-orchestrated version as a prototype. Pay attention to which steps are consistent and which vary. Once you have run the workflow enough times to know what “correct” looks like, harden the stable parts. Premature hardening is premature optimization — it locks in assumptions that have not been tested.
“Never Hardening”
The opposite failure. The workflow has been running for months in its LLM-orchestrated form. You have worked around the failures. You have developed rituals: check the output, re-run if it looks wrong, manually fix the wikilinks. The prototype has become permanent infrastructure, and its unreliability has become your normal.
This is the more dangerous pitfall because it is invisible. You have adapted to the pain. You no longer notice the five minutes you spend checking every output, or the occasional lost meeting note, or the subtle trust deficit that makes you hesitate before relying on the pipeline for anything important. The cost is real but diffuse, spread across hundreds of small moments of friction.
The fix: set a deadline. If a workflow has been running in prototype form for more than two to four weeks and the steps are stable, it is time to harden. The investment pays for itself quickly because you stop paying the invisible tax of unreliability.
“Hardening the Wrong Step”
Not every step should be hardened. Summarization, creative generation, intent classification, novel reasoning — these are tasks where the LLM’s probabilistic nature is a feature, not a bug. If you try to replace “summarize this transcript” with a deterministic algorithm, you will build something brittle that handles only the cases you anticipated and fails on everything else.
The fix: return to Step 2 of the tactical implementation. If a step genuinely benefits from fuzzy reasoning — if two equally valid outputs could be different and that is acceptable — leave it with the LLM. Harden the mechanical steps around it so the fuzzy step can focus on what it does best, with reliable inputs and a reliable path for its outputs.
## 7. Expected Impact
The meeting transcription pipeline went from a workflow I used nervously — always checking, always doubting — to one I use without thinking. That is the metric that matters most: the transition from manual verification to genuine trust.
Quantitatively: workflow reliability went from somewhere around 70-80% (rough estimate — the failures were intermittent enough that I never tracked them precisely, which is itself a symptom of the problem) to 100%. Zero silent failures since hardening. Zero lost meeting notes. Zero incorrect wikilinks. The time I used to spend on manual verification — checking every note, fixing broken links, re-running failed pipelines — dropped to zero.
The less obvious metric is development velocity. When you trust your tools, you build on top of them without hesitation. The hardened transcription pipeline became the foundation for other workflows: automated standup summaries, project status extraction, decision tracking. None of those would have been worth building on a foundation that failed unpredictably.
## 8. Fact Sheet
Principle:
The Hardening Principle
One-sentence definition:
Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool, pulling the LLM back to the role of caller only.
The science:
LLMs are probabilistic systems that sample from token distributions — reliable for fuzzy reasoning, unreliable for mechanical execution that demands identical behavior across runs.
5 key takeaways:
- LLMs are excellent prototyping partners but poor production runtime components for deterministic steps
- Every agentic workflow contains a mix of fuzzy (LLM-appropriate) and mechanical (code-appropriate) steps
- Use the LLM to build the tool that replaces the LLM — prototype with AI, harden into code
- The LLM’s production role is orchestration and reasoning, not mechanical execution
- Silent failures are the most expensive failures — hardened tools fail loudly or succeed completely
Quick-start checklist:
- Map every LLM-powered step in your most-used workflow
- Label each step as “needs fuzzy reasoning” or “needs reliable execution”
- Pick the most failure-prone deterministic step and harden it first
- Test the hardened tool independently with known inputs
- Add basic logging to every hardened tool invocation
The metric to watch:
Workflow completion rate — the percentage of runs that complete successfully without manual intervention.
Download Fact Sheet (SVG) →
## 9. What’s Next
You now know when to pull the LLM out of the loop. You can identify the mechanical steps hiding inside your agentic workflows, build deterministic replacements, and push the LLM back to the role it was designed for: reasoning, not executing.
But what about when the LLM is in the loop — when it is doing the fuzzy reasoning that only it can do? Every token you feed it matters. More than you think. The context window is not an infinite canvas where you can dump everything and hope the model finds what it needs. It is a finite resource with measurable constraints, and the research on how models process that context will change how you structure every prompt, every session, and every workflow.
The science of context will surprise you. That is Principle 2: The Context Hygiene Principle.
<!-- fetched-content:end -->
