---
title: "Skill Design Framework for AI Agents"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "db7bbe28e5c6cd6654d03bbd74fe141b54ef9afb68018a4e7d641d5c7c9ab59e"
sources:
  - raw/2026-04-08-the-toolkit-principle-10-claude-code-principles.md
quality_score: 0
concepts:
  - skill-design-framework-for-ai-agents
related:
  - "[[The Context Hygiene Principle]]"
  - "[[The Specialized Review Principle]]"
  - "[[The Hardening Principle]]"
  - "[[The Toolkit Principle | 10 Claude Code Principles]]"
tier: hot
tags: [skill-design, ai-agents, prompt-engineering, vocabulary-routing, anti-patterns]
---

# Skill Design Framework for AI Agents

## Overview

The Skill Design Framework is a comprehensive, research-backed methodology for constructing high-quality, reusable AI agent skills. It emphasizes expert vocabulary, dual-register descriptions, anti-pattern detection, structured instructions, and progressive disclosure to ensure skills are both effective and robust against common failure modes.

## How It Works

The Skill Design Framework synthesizes findings from multiple research sources to define a set of DOs and DON'Ts for building AI agent skills. The framework is structured around the insight that the quality of an AI agent's output is determined not just by the underlying model, but by the specificity, structure, and context of the skills it is given.

**1. Expert Vocabulary as the Primary Quality Lever:**
Every skill must include a payload of 15-30 precise domain terms, chosen to pass the '15-year practitioner test.' This vocabulary acts as a routing signal, ensuring that the model activates the correct region of its knowledge space. Research shows that vague or generic terms lead to generic outputs, while precise vocabulary triggers domain-specific expertise.

**2. Dual-Register Descriptions:**
Descriptions should operate in both expert and natural language registers. The expert register ensures the model triggers deep knowledge, while the natural language register allows for accessibility and flexibility in user queries. Skills with only formal or only casual descriptions underperform, either by failing to trigger or by producing generic responses.

**3. Named Anti-Patterns with Detection and Resolution:**
Each skill includes a watchlist of 5-10 anti-patterns, each with a detection signal, resolution step, and prevention principle. Anti-patterns serve as both guardrails and routing signals, helping the model avoid known failure modes and escape the 'distribution center' of generic advice.

**4. Structured, Conditional Instructions:**
Instructions are formatted as ordered, imperative steps with explicit IF/THEN conditions. This structure reduces ambiguity and increases reliability, as models are less likely to misinterpret numbered steps than prose. Research demonstrates that atomic, conditional checks dramatically reduce false negatives compared to free-text instructions.

**5. Canonical Examples and Progressive Disclosure:**
Each skill includes 2-3 BAD vs GOOD example pairs, with the most representative example placed last to leverage recency bias. Skills are organized for progressive disclosure: metadata and vocabulary are always loaded, the main skill body is loaded on trigger, and heavy references are loaded on demand. This structure optimizes the model's attention budget, ensuring that the most important signals are front-loaded.

**6. Separation of Generation and Evaluation:**
Evaluation criteria are separated from generation instructions, weighted, and phrased as gradable questions. This allows for deterministic verification before LLM-based evaluation, ensuring that skills can be audited and improved over time.

The framework also prescribes what NOT to do: avoid generic consultant-speak, over-prompting, flattery-based personas, positive-only instructions, and ambiguous or overlapping skill sets. Each of these pitfalls is linked to specific failure modes documented in research.

The recommended file architecture for a skill is as follows:

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

This order leverages the U-shaped attention curve observed in LLMs: the beginning and end of context receive the most attention, so vocabulary and retrieval anchors are placed there, while structured instructions occupy the middle, surviving attention drop-off due to their format.

## Key Properties

- **Vocabulary Routing:** 15-30 precise domain terms per skill, ensuring activation of the correct knowledge cluster.
- **Anti-Pattern Watchlists:** 5-10 named failure modes per skill, each with detection, explanation, and resolution steps.
- **Structured, Conditional Instructions:** Ordered steps with explicit conditions, reducing ambiguity and increasing reliability.
- **Progressive Disclosure:** Layered context loading, with metadata always in context, main body on trigger, and references on demand.
- **Separation of Generation and Evaluation:** Evaluation criteria are distinct from generation instructions, enabling deterministic and LLM-based review.

## Limitations

The framework assumes that domain expertise can be adequately captured in vocabulary payloads and structured instructions, which may not hold for highly interdisciplinary or emergent fields. Overly rigid adherence to the framework can stifle creativity or adaptability, and the requirement for multiple examples and anti-patterns increases the upfront investment in skill creation. Skills that are too narrowly defined may fail to generalize, while those that are too broad risk ambiguity and mis-triggering.

## Example

A security audit skill for SaaS APIs might include the following:
- Vocabulary: 'OWASP Top 10', 'lateral movement', 'NIST 800-53', 'defense-in-depth'
- Anti-patterns: 'checkbox compliance', 'scope creep into penetration testing', 'severity inflation'
- Instructions: 1. Review network configuration. 2. Assess access controls. 3. Test for API-specific vulnerabilities IF authentication flows are present.
- Examples: BAD - 'Check security.' GOOD - 'Perform OWASP Top 10 audit with STRIDE threat modeling.'
- Evaluation: 'Does the Findings Report include severity classifications and remediation recommendations?'

## Visual

The article includes a diagram (Figure 13) showing the SKILL.md file as a stack of seven sections, with a U-shaped attention curve overlay. The top (YAML frontmatter, Expert Vocabulary) and bottom (Questions) receive high attention, while the middle (Behavioral Instructions, Output Format) receives less. This visual demonstrates why section order matters for LLM attention allocation.

## Relationship to Other Concepts

- **[[The Context Hygiene Principle]]** — Progressive disclosure and context management are direct applications of context hygiene.
- **[[The Specialized Review Principle]]** — Vocabulary routing and anti-patterns ensure skills are specialized and robust.
- **[[The Hardening Principle]]** — Structured, deterministic instructions harden skills against drift and ambiguity.

## Practical Applications

The framework is used to design reusable, high-quality skills for AI agents in domains such as software engineering, security audits, marketing, and compliance. It is especially valuable in environments where reliability, auditability, and domain specificity are critical, such as regulated industries or large-scale AI deployments.

## Sources

- [[The Toolkit Principle | 10 Claude Code Principles]] — primary source for this concept
