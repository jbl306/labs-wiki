---
title: "Contradiction Detection Utility"
type: concept
created: 2026-04-11
last_verified: 2026-04-11
source_hash: "101bef9011616b455e60e17998c3f1b308c5cab895c27a19c5a6f4d028ffcfb8"
sources:
  - raw/2026-04-07-llm-wiki.md
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 100
concepts:
  - contradiction-detection-utility
related:
  - "[[Palace Memory Architecture]]"
  - "[[MemPalace GitHub Repository]]"
tier: hot
tags: [fact-checking, validation, knowledge-graph, ai]
---

# Contradiction Detection Utility

## Overview

Contradiction Detection Utility is a separate tool in MemPalace that checks assertions against stored entity facts, identifying conflicts, stale data, and attribution errors in conversational memory. It enhances reliability by dynamically validating knowledge graph claims.

## How It Works

The Contradiction Detection Utility, implemented as `fact_checker.py`, operates by parsing input assertions and cross-referencing them with the temporal entity-relationship knowledge graph stored in SQLite. When a user or AI agent makes a claim (e.g., 'Soren finished the auth migration'), the utility checks the relevant entity, predicate, and date range to determine if the assertion is consistent with recorded facts.

The system flags conflicts (attribution errors), stale data (outdated information), and wrong tenures (incorrect durations) by dynamically calculating ages, dates, and relationships. For example, if the knowledge graph shows Maya was assigned to 'auth-migration', but the input claims Soren finished it, the utility outputs an attribution conflict. Similarly, if a sprint end date is outdated, it flags stale_date.

Currently, the utility is not wired into the main knowledge graph operations but is slated for integration in upcoming releases. When enabled, it will automatically validate conversational claims during mining and search, improving the accuracy and reliability of AI memory retrieval.

The utility is extensible, allowing for custom predicates and validation rules. It supports dynamic calculation, so facts are not hardcoded but derived from entity histories. This is especially valuable in collaborative environments where decisions and assignments change frequently.

## Key Properties

- **Dynamic Fact Checking:** Validates assertions against entity histories, calculating ages, tenures, and dates in real time.
- **Conflict Detection:** Flags attribution conflicts, stale data, and wrong tenures based on knowledge graph records.
- **Extensible Validation:** Supports custom predicates and validation rules for diverse conversational contexts.

## Limitations

Not yet integrated into main knowledge graph operations; must be manually invoked. Effectiveness depends on the completeness and accuracy of mined entity data. May require tuning for edge cases and ambiguous assertions.

## Example

Input: 'Kai has been here 2 years' — Output: 'KAI: wrong_tenure — records show 3 years (started 2023-04)'. Input: 'The sprint ends Friday' — Output: 'SPRINT: stale_date — current sprint ends Thursday (updated 2 days ago)'.

## Visual

No diagram, but README provides textual examples of input/output for contradiction detection.

## Relationship to Other Concepts

- **[[Palace Memory Architecture]]** — Contradiction detection validates facts within the palace's knowledge graph.

## Practical Applications

Used by team leads and AI agents to verify decisions, assignments, and timelines in collaborative projects. Prevents misinformation and ensures reliable recall in long-term conversational memory.

## Sources

- [[MemPalace GitHub Repository]] — primary source for this concept
- [[LLM Wiki]] — additional source
