---
title: "MAST Failure Taxonomy"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "3b8f3f5bf18a470b6b8c086dbe24c89c1770ad4369359a4451bdfc3af49181f5"
sources:
  - raw/2026-04-08-the-observability-imperative-10-claude-code-principles.md
quality_score: 0
concepts:
  - mast-failure-taxonomy
related:
  - "[[The Observability Imperative]]"
  - "[[Structured, Automated Documentation vs. Institutional Memory in Agentic Workflows]]"
  - "[[The Observability Imperative | 10 Claude Code Principles]]"
tier: hot
tags: [failure-taxonomy, multi-agent-systems, observability, debugging, error-detection]
---

# MAST Failure Taxonomy

## Overview

The MAST Failure Taxonomy is a structured framework cataloging 14 distinct failure modes in multi-agent systems, grouped into Communication, Coordination, and Quality categories. It provides detection strategies for each failure mode, most of which are only observable with structured logging.

## How It Works

The MAST (Multi-Agent System Taxonomy) Failure Taxonomy organizes failure modes encountered in agentic workflows into three main categories:

**1. Communication Failures:**
- *Message Loss (FM-1.1):* An agent's output is not received by the next agent. Detection: Hash handoff payloads and confirm receipt.
- *Misinterpretation (FM-1.2):* Instructions are understood differently than intended. Detection: Require structured formats for communication.
- *Info Overload (FM-1.3):* Excessive context degrades agent performance. Detection: Monitor token counts.
- *Stale Context (FM-1.4):* Agents act on outdated information. Detection: Timestamp all context and compare at handoff.

**2. Coordination Failures:**
- *Deadlock (FM-2.1):* Agents wait indefinitely for each other. Detection: Timeout all operations.
- *Race Condition (FM-2.2):* Output depends on execution order. Detection: Use sequence-number handoffs.
- *Role Confusion (FM-2.3):* Overlapping or unclear responsibilities. Detection: Assign single-responsibility identities.
- *Authority Vacuum (FM-2.4):* No agent is empowered to decide. Detection: Explicitly assign decision owners.
- *Resource Contention (FM-2.5):* Multiple agents modify the same resource. Detection: Lock or queue shared resources.

**3. Quality Failures:**
- *Rubber-Stamp Approval (FM-3.1):* Reviewer approves without scrutiny. Detection: Require specific citations, log approval latency and content.
- *Error Cascading (FM-3.2):* One agent's mistake is amplified downstream. Detection: Validate at each handoff, hash artifact chains.
- *LCD Output (FM-3.3):* Lowest-common-denominator quality. Detection: Set domain-specific quality bars.
- *Groupthink (FM-3.4):* Agents converge on the same approach. Detection: Encourage diversity in specialist prompts.
- *Regression (FM-3.5):* Later agent undoes earlier agent's work. Detection: Use immutable completed sections.

Each failure mode is paired with a detection strategy, most of which require explicit, structured logging. For example, message loss is only detectable if every handoff is logged and hashes are compared. Stale context is only visible if timestamps are recorded and checked. Rubber-stamp approval is revealed by logging both the content and latency of reviews.

The taxonomy provides a practical checklist for instrumenting agentic pipelines, ensuring that silent, non-crashing failures are surfaced and can be addressed. Without observability, these failures degrade output quality in ways that are subtle, intermittent, and often indistinguishable from normal system variance.

## Key Properties

- **Comprehensive Coverage:** Covers 14 failure modes across communication, coordination, and quality, providing a holistic view of multi-agent system risks.
- **Detection Strategies:** Each failure mode is paired with a concrete detection method, most requiring structured logging and observability.
- **Invisible Failures:** Most failure modes do not crash the pipeline and are only detectable with proper instrumentation.

## Limitations

The taxonomy assumes the presence of structured logging and observability. Without these, most detection strategies are infeasible. It does not prescribe prevention, only detection. Some failure modes may overlap or interact in complex ways, requiring careful analysis.

## Example

Suppose an agentic pipeline exhibits intermittent quality issues. By applying the MAST taxonomy:
- The developer logs all handoffs with hashes and timestamps.
- They detect that the implementation agent sometimes works from a stale plan (FM-1.4) by comparing timestamps.
- Review logs show approvals in under 2 seconds for 94% of submissions (FM-3.1, rubber-stamp approval).
- By restructuring prompts and enforcing review latency, these failure modes are surfaced and mitigated.

## Visual

The article presents a three-column reference table listing all 14 failure modes, their descriptions, and detection strategies. It also includes a diagram (Figure 8) visually grouping failure modes by category and showing their detection dependencies on observability.

## Relationship to Other Concepts

- **[[The Observability Imperative]]** — Observability is required to detect most MAST failure modes.
- **[[Structured, Automated Documentation vs. Institutional Memory in Agentic Workflows]]** — Both address the need for traceability and error detection in complex workflows.

## Practical Applications

The MAST taxonomy is used to audit and instrument multi-agent systems, ensuring that silent failures are surfaced. It is applied in LLM-based pipelines, automated code review systems, and any workflow where agents interact and hand off artifacts. It provides a checklist for developers to ensure comprehensive observability.

## Sources

- [[The Observability Imperative | 10 Claude Code Principles]] — primary source for this concept
