---
title: "The Specialized Review Principle | 10 Claude Code Principles"
type: url
captured: 2026-04-08T01:36:48.953631+00:00
source: android-share
url: "https://jdforsythe.github.io/10-principles/principles/specialized-review/"
content_hash: "sha256:46aeec2f0f0d1a0546b7f9ef7c85ab29ab8351f08074f2fd8e35432f542c18e6"
tags: []
status: ingested
---

https://jdforsythe.github.io/10-principles/principles/specialized-review/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:36:36+00:00
- source_url: https://jdforsythe.github.io/10-principles/principles/specialized-review/
- resolved_url: https://jdforsythe.github.io/10-principles/principles/specialized-review/
- content_type: text/html; charset=utf-8
- image_urls: []

## Fetched Content
## 1. The War Story
The security violation was obvious. Blindingly, screamingly obvious. An API key hardcoded in a React component, committed to a public repo. Our “senior code review” agent — the one we trusted to catch exactly this kind of thing — gave it a clean bill of health. “Code looks good, well-structured, follows React best practices.” It wasn’t lying. The code DID follow React best practices. The agent just couldn’t see beyond React.
The component was clean. Props typed correctly. Hooks used properly. State management was sound. From a React perspective, the code was genuinely well-written. The review agent saw a well-structured component and said so. It never thought to look at the string literal on line 14 and ask: “Wait — is that an API key?”
This was not a hallucination. The model knew what API keys were. It knew they should not be hardcoded. If I had asked directly — “Is there a security issue in this file?” — it would have found the key in seconds. But nobody asked. The agent’s prompt said “review this code,” and the agent interpreted “review” through the lens of the vocabulary it had been given: React patterns, component architecture, TypeScript conventions. Security was not in its vocabulary, so security was not in its attention.
The failure was mine, not the model’s. I had built a generalist reviewer and expected specialist depth across every domain simultaneously. That expectation was not just unrealistic — it was scientifically wrong.
## 2. The Principle
Code review is too important for a single generalist. Orchestrate a panel of specialist agents that each apply your exact rules and deliver prioritized, multi-angle feedback.
Most teams that use AI for code review take the path of least resistance: one agent, one prompt, one pass. “Review this PR for issues.” The agent obliges. It scans the code, identifies some things it recognizes, says something encouraging, and moves on. The output feels useful. It is occasionally useful. But it trends relentlessly toward the median — the most generic, average-quality review the model’s training data can produce.
This is not a quality problem you can solve by making the prompt longer. You cannot write a single system prompt that makes one agent simultaneously expert in OWASP security vulnerabilities, Big-O complexity analysis, WCAG accessibility compliance, and your domain’s business logic. Stacking roles fragments the model’s attention across competing knowledge domains, activating a shallow intersection rather than any deep expertise.
The alternative is specialization: a panel of focused reviewers, each defined with the precise vocabulary of their domain, each looking at the same code through a different expert lens. One agent does not need to know everything. It needs to know its domain deeply, using the exact terms that activate expert-level knowledge in the model’s training data.
## 3. The Science
This principle sits at the intersection of three research findings that together explain why generalist review fails and how specialist review works.
### Vocabulary Routing in Embedding Space
LLMs organize knowledge in clusters within their learned embedding space, and specific vocabulary acts as the routing signal that determines which clusters get activated. Ranjan et al. (2024) demonstrated in “One Word Is Not Enough” that prompt word choice significantly affects which knowledge regions the model draws from. This is not metaphorical — it is a direct consequence of how embeddings and attention operate.
Consider the difference:
| Non-expert prompt | Expert prompt | What gets activated |
| --- | --- | --- |
| “nice colors” | “OKLCH tinted neutrals with warm base hue” | Color science cluster |
| “plan the project” | “vertically-sliced work packages with INVEST criteria” | Work breakdown expertise |
| “review the security” | “OWASP Top 10 audit, STRIDE threat model (Shostack)” | Security engineering cluster |
The left column routes to blog posts, introductory tutorials, and casual explanations. The right column routes to technical papers, engineering documentation, and expert-level discourse. Same model, same capabilities, radically different output — determined entirely by the vocabulary in the prompt.
The practical test is what I call the 15-year practitioner test: would a senior expert with 15+ years of domain experience use this exact term when talking with a peer? If a principal security engineer would say “STRIDE threat model” but would never say “review the security,” then “STRIDE threat model” is the vocabulary that activates the knowledge you want.
### PRISM Persona Science
The PRISM persona research framework revealed a clear pattern: accuracy damage from personas scales with length. Shorter identities cause less degradation. Longer personas, at 100 or more tokens, measurably degrade accuracy on knowledge tasks. The mechanism is straightforward: attention spent processing an elaborate persona description is attention not spent on the actual task. The synthesis is to keep identities the minimum length required — no shorter, no longer — with under 50 tokens as the practical sweet spot.
Ranjan et al.’s vocabulary routing research explains why flattery specifically makes things worse. “You are the world’s best security expert” does not activate security expertise. It activates motivational content and marketing copy — the regions of training data where superlatives like “world’s best” appear most frequently. Real job titles activate real training data clusters. “Senior site reliability engineer” routes to incident postmortems, runbooks, and infrastructure documentation. “Expert in keeping systems running” routes to blog posts about productivity. The vocabulary in the identity is a routing signal, and flattery points it in the wrong direction.
PRISM also documented an alignment-accuracy tradeoff: stronger persona definitions improve instruction-following but can reduce factual accuracy. The model tries harder to stay in character, even when staying in character means being wrong. The optimal configuration is a minimum viable role definition under 50 tokens combined with domain-specific vocabulary. The vocabulary does the heavy lifting. The role definition sets the frame.
### Self-Evaluation Fails
When asked to evaluate its own work, a model confidently praises mediocre output. This is well-documented: the generator has the same biases and blind spots as the evaluator. If the model did not notice a security vulnerability while generating code, it will not notice the same vulnerability when reviewing that code. The biases are not random — they are systematic, arising from the same training distribution.
Anthropic’s harness design research (March 2026) found that separating generation from evaluation dramatically improves quality. The agent that wrote the code should not be the agent that reviews it. And before any LLM-based review happens at all, deterministic verification — build, lint, test — should be the first quality gate. LLMs evaluate subjective qualities. Compilers evaluate objective ones. Run the compiler first.
## 4. Before and After
Generalist vs Specialist Panel Comparison
Side-by-side comparison showing how a single generalist reviewer provides shallow coverage across security, performance, accessibility, and domain logic, while a panel of focused specialists each under 50 tokens delivers deep, expert-level coverage in every domain.
Generalist
GEN
Generalist Reviewer
>200 tokens
Security
40%
Performance
20%
Accessibility
10%
Domain Logic
5%
Surface issues only. Shallow, uniform coverage.
VS
Specialist Panel
SEC
Security
PERF
Performance
A11Y
Accessibility
DOM
Domain
<50 tokens each
Security
95%
Performance
85%
Accessibility
80%
Domain Logic
75%
Deep, focused expertise per domain.
Brief identities (<50 tokens) outperform elaborate personas. — PRISM, 2024
Figure 7: A panel of brief specialists (<50 tokens each) outperforms a single elaborate generalist (>200 tokens).
Before: The Generalist Reviewer
We had a single code review agent with an ambitious system prompt. It was supposed to check for security issues, performance problems, accessibility violations, code style, and domain conventions. The prompt was long — several paragraphs covering each area. We thought thoroughness in the prompt would produce thoroughness in the output.
What we got was the median. The agent identified surface-level issues — an unused import here, a missing return type there — and pronounced the code clean. Its security “review” amounted to checking whether error messages leaked stack traces. Its performance analysis was limited to spotting obvious N+1 patterns. Accessibility was mentioned in passing, if at all. Domain logic review was nonexistent because the agent had no vocabulary to reason about our business rules.
The review felt useful because it found some things. But it was missing the things that mattered. The API key. The SQL query that would lock the users table under load. The form unusable with a screen reader. The business rule that violated a regulatory constraint.
We were getting the lowest common denominator across five domains — the shallow intersection of what one generalist prompt could activate simultaneously.
After: The Specialist Panel
The replacement was a panel of four specialist reviewers, each with a tightly scoped identity and domain-specific vocabulary.
The security reviewer was defined as “senior application security engineer” in 30 tokens. Its vocabulary payload included OWASP Top 10, STRIDE threat modeling (Shostack), CWE classifications, secrets detection, input validation boundaries, authentication flow analysis, and authorization bypass patterns. Its anti-pattern list named specific vulnerabilities: hardcoded credentials, SQL injection via string concatenation, insecure direct object references, missing CSRF tokens.
The performance reviewer was defined as “senior performance engineer.” Its vocabulary included Big-O complexity analysis, query execution plans, connection pool saturation, memory leak patterns, bundle size regression, critical rendering path, and time-to-interactive budgets.
The accessibility reviewer was “senior accessibility engineer” with WCAG 2.2 AA criteria, ARIA landmark patterns, keyboard navigation flows, screen reader announcement order, color contrast ratios, and focus management vocabulary.
The domain logic reviewer used our specific business terminology — the named entities, workflow states, regulatory constraints, and validation rules unique to our product.
Each specialist had fewer than 50 tokens of identity, 15-30 domain terms, and 5-10 named anti-patterns with detection signals. The same code went to all four reviewers. Each found different issues. The security reviewer caught the API key on the first run. The performance reviewer identified a query that would degrade under load. The accessibility reviewer flagged a form with no label associations. The domain reviewer caught a state transition that violated a business rule.
Four focused lenses on the same code. Each seeing what the generalist could not.
## 5. Tactical Implementation
Here is how to build a specialist review panel, starting tomorrow.
Step 1: Identify the domains your code review needs to cover.
Most codebases need security, performance, and code quality at minimum. Many also need accessibility, domain logic, and infrastructure review. Do not try to cover everything on day one. Pick the two or three domains where your generalist reviewer has missed the most issues. Those are your highest-value specialists.
Step 2: Build one specialist agent per domain with a real job title.
Keep the identity under 50 tokens. Use a title that exists in the real world — one that appears in job postings, conference talks, and technical publications. “Senior application security engineer” activates security engineering training data. “Code safety checker” activates nothing useful. The title is a routing signal, not a decoration.
Step 3: Give each specialist 15-30 domain-specific vocabulary terms.
Apply the 15-year practitioner test to every term. A principal security engineer says “STRIDE threat model,” not “think about threats.” A senior performance engineer says “query execution plan,” not “check if the database is slow.” Include named frameworks with their originators where applicable: “circuit breaker pattern (Nygard)” is more precise than “error handling pattern.” The vocabulary primes the model’s embedding space before it reads a single line of your code.
Step 4: Include 5-10 named anti-patterns with detection signals per specialist.
Each anti-pattern should have a name, a detection signal (what in the code indicates this pattern is present), and a resolution step. “Hardcoded secrets — detection: string literals matching API key, token, or password patterns in source files — resolution: move to environment variables with .env.example documenting required keys.” Named anti-patterns are routing signals themselves, activating the same expert clusters as positive vocabulary.
Step 5: Never use flattery — define competence through knowledge, not adjectives.
“You are the world’s best security expert” burns tokens and activates the wrong training data. Define competence through what the specialist knows (vocabulary), what it watches for (anti-patterns), and how it behaves (instructions). Knowledge demonstrates expertise. Superlatives do not.
Step 6: Separate generation from evaluation.
The agent that wrote the code should never be the agent that reviews it. The generator’s blind spots are the evaluator’s blind spots when they share the same context. A fresh agent with a specialist prompt and no knowledge of how the code was written will see things the original author cannot.
Step 7: Require reviewers to identify at least one issue OR explicitly justify clearance with evidence.
A review that says “LGTM” with no analysis is worse than no review — it creates false confidence. Require each specialist to either identify at least one issue or provide evidence-backed justification for clearance. “No security issues found” is not enough. “No hardcoded secrets, all user input sanitized via validation middleware on lines 12-15, auth checked via route guard” is evidence.
Step 8: Automate the assembly.
Building specialist agents by hand works, but it is the kind of fuzzy, repeated workflow that Principle 1 (Hardening) says should become a tool.
Forge
(github.com/jdforsythe/forge) is an open-source system that automates this: it uses vocabulary routing, PRISM persona science, DeepMind scaling laws, and the MAST failure taxonomy to assemble specialist agent teams from a goal description. It includes a library of 11 domain agents and 3 team templates. We will do a full walkthrough in Principle 10.
One practical note on context management: you do not need every specialist loaded into every session. Load only the reviewers relevant to the current PR. A frontend-only change does not need the infrastructure reviewer. A database migration does not need the accessibility specialist. Selective loading keeps your context budget focused on the reviews that matter.
## 6. Common Pitfalls
“The Generalist Trap”
One agent reviewing everything trends toward the median. When a single prompt tries to activate security AND performance AND accessibility AND domain logic simultaneously, the model activates the shallow intersection of all four rather than the depth of any one. The intersection is where blog posts live. The depth is where engineering papers live.
“Flattery Personas”
“You are the world’s best security expert, a legendary hacker who has found more zero-days than anyone in history.” Vocabulary routing research (Ranjan et al., 2024) explains what happens: superlatives activate motivational content, marketing copy, and fictional narratives about hackers — not security engineering expertise. The more elaborate the flattery, the further from expert knowledge the model drifts. Replace flattery with vocabulary. Twenty precise security terms do more work than two hundred tokens of praise.
“Rubber-Stamp Reviews” (MAST FM-3.1)
The single most common quality failure in multi-agent systems, documented as failure mode FM-3.1 in the MAST taxonomy. LLMs are sycophantic by default. A review agent with a weak prompt will say “LGTM” to a hardcoded API key and a SQL injection — not because it cannot see the problem, but because approving is the path of least resistance in its training distribution. The fix is structural: require evidence-backed justification for every clean review.
“Role Stacking”
Making one agent simultaneously a security expert, performance engineer, and accessibility specialist fragments knowledge activation. The model cannot deeply activate three competing domain clusters at once. Each role dilutes the others. One agent, one domain, one vocabulary set. If you need three domains reviewed, use three agents.
“Skipping Deterministic Checks”
Always run the build, linter, and test suite BEFORE sending code to LLM reviewers. Deterministic tools catch objective failures — syntax errors, type violations, lint rule breaches — with 100% reliability and zero tokens. LLM reviewers should evaluate subjective qualities: architectural fitness, security implications, performance characteristics, accessibility compliance. Sending code that does not compile to a security reviewer wastes attention on problems a compiler would catch for free.
## 7. Expected Impact
Security violations caught in review went from approximately 40% to 95% after specializing agents. The generalist was catching roughly four in ten security issues — mostly the obvious ones any developer might notice. The specialist security reviewer, armed with OWASP vocabulary and a named anti-pattern list, catches nearly all of them.
False positive rates dropped because each specialist understands its domain well enough to distinguish real issues from style preferences. The generalist flagged code style choices as “potential issues” because it lacked domain confidence. The specialist knows the difference between a genuine vulnerability and a conscious tradeoff.
Four specialist passes take roughly the same wall-clock time as one generalist pass when run in parallel. But the value per review increased dramatically — every finding is domain-relevant, actionable, and backed by specialist vocabulary.
## 8. Fact Sheet
Principle:
The Specialized Review Principle
One-sentence definition:
Code review is too important for a single generalist — orchestrate a panel of specialist agents that each apply domain-specific vocabulary and deliver prioritized, multi-angle feedback.
The science:
LLM vocabulary acts as a routing signal in embedding space — including why flattery routes to motivational content instead of expertise (Ranjan et al., 2024); accuracy damage from personas scales with length, with under 50 tokens as the practical sweet spot (PRISM); self-evaluation fails because the generator shares the evaluator’s biases (Anthropic Harness Design, Mar 2026).
5 key takeaways:
- Expert vocabulary is the primary lever for output quality — the words in your prompt determine which knowledge the model accesses
- Keep identities the minimum length required, under 50 tokens in practice — accuracy damage scales with persona length
- Flattery routes to motivational content instead of domain expertise — define competence through vocabulary, not adjectives
- The agent that wrote the code must not be the agent that reviews it
- Deterministic checks (build, lint, test) first; LLM specialist review second
Quick-start checklist:
- Identify the top 2-3 review domains where your generalist misses the most issues
- Build one specialist per domain: real job title (<50 tokens) + 15-30 expert vocabulary terms + 5-10 named anti-patterns
- Require every review to cite specific evidence — no bare “LGTM” approvals
- Run deterministic checks before any LLM review pass
- Separate code generation agents from code review agents
The metric to watch:
Domain-specific issue detection rate — the percentage of real issues in each domain (security, performance, accessibility) caught before code reaches production.
Download Fact Sheet (SVG) →
## 9. What’s Next
You have specialist reviewers finding real issues. But can you see what they are finding? Can you trace back why two specialists disagree about the same line of code? Can you debug a review that was wrong? If your review pipeline is a black box, you are trusting it on faith. You know it is finding issues because you see the output. But you do not know what it is missing, how it is deciding, or whether the specialists are actually reading the code or just pattern-matching against their anti-pattern lists.
When you have four agents reviewing the same code, you need to see every input, every finding, every justification. Without that visibility, you cannot improve the system — you can only hope it keeps working.
That is Principle 7: The Observability Imperative.
<!-- fetched-content:end -->
