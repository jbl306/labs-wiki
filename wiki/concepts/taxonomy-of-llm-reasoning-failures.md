---
title: "Taxonomy Of LLM Reasoning Failures"
type: concept
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "0d1874945b0424f95de28979ad06c589dab76f705f4a985fdbd1b79f293f0226"
sources:
  - raw/2026-04-10-260206176v1pdf.md
quality_score: 100
concepts:
  - taxonomy-of-llm-reasoning-failures
related:
  - "[[Large Language Model Reasoning Failures]]"
tier: hot
tags: [llm, reasoning, taxonomy, failure-analysis, cognitive-science]
---

# Taxonomy Of LLM Reasoning Failures

## Overview

A structured framework for categorizing reasoning failures in Large Language Models (LLMs), distinguishing between embodied and non-embodied reasoning, and classifying failures as fundamental, application-specific, or robustness-related. This taxonomy enables systematic analysis and comparison of reasoning weaknesses, guiding research and mitigation strategies.

## How It Works

The taxonomy proposed in the paper organizes reasoning failures in LLMs along two primary axes: reasoning type and failure type. The reasoning type axis distinguishes between embodied and non-embodied reasoning. Embodied reasoning refers to cognitive processes that require physical interaction with the environment, such as spatial intelligence, real-time feedback, and goal-directed behaviors constrained by physical laws. Non-embodied reasoning, on the other hand, encompasses cognitive processes that do not require such interaction. Non-embodied reasoning is further subdivided into informal (intuitive) and formal (logical) reasoning. Informal reasoning includes intuitive judgments, cognitive biases, and heuristics common in everyday decision-making and social activities. Formal reasoning involves explicit, rule-based manipulation of symbols, grounded in logic, mathematics, and code.

The failure type axis classifies failures into three categories: fundamental failures, application-specific limitations, and robustness issues. Fundamental failures are intrinsic to LLM architectures and manifest broadly across diverse tasks. Application-specific limitations are tied to particular domains, where models underperform despite human expectations of competence. Robustness issues are characterized by inconsistent performance across minor variations, often revealing hidden vulnerabilities.

By combining these axes, the taxonomy creates a matrix where each cell represents a specific intersection of reasoning type and failure type. For example, fundamental failures in informal reasoning may include deficits in working memory or cognitive flexibility, while robustness issues in formal reasoning may involve inconsistent performance on logic or math word problems under slight prompt variations.

This framework enables researchers to systematically identify, analyze, and compare reasoning failures. It also facilitates the development of targeted mitigation strategies by clarifying the underlying causes and contexts in which failures occur. The taxonomy is visualized in the paper as a table with rows representing reasoning categories and columns representing failure categories, providing a clear organizational structure for the survey.

The taxonomy is grounded in cognitive science and philosophy, drawing parallels between human reasoning failures and those observed in LLMs. It acknowledges that LLMs, inspired by human cognition, inherit both strengths and weaknesses from their training data, architectures, and alignment processes. By explicitly defining and categorizing reasoning failures, the taxonomy unifies fragmented research findings, highlights shared patterns, and directs focused efforts toward understanding and mitigating critical reasoning weaknesses.

Edge cases arise when failures do not fit neatly into a single category, such as robustness issues that span both informal and formal reasoning, or application-specific limitations that manifest as fundamental failures in certain domains. The taxonomy is flexible enough to accommodate such cases, allowing for nuanced analysis and comparison.

## Key Properties

- **Two-Axis Structure:** Organizes failures by reasoning type (embodied vs. non-embodied, informal vs. formal) and failure type (fundamental, application-specific, robustness).
- **Mutually Consistent Framework:** Each cell in the taxonomy matrix represents a specific intersection of reasoning and failure types, enabling systematic analysis.
- **Grounded In Cognitive Science:** Draws parallels between human reasoning failures and those observed in LLMs, facilitating interdisciplinary research.

## Limitations

The taxonomy may not capture all nuances of reasoning failures, especially as new types of failures emerge with advances in LLM architectures and applications. Some failures may span multiple categories or evolve over time, requiring updates to the framework. The taxonomy relies on behavioral assessments of LLM outputs, which may not fully reveal internal reasoning processes.

## Example

Consider a fundamental failure in informal reasoning: an LLM consistently exhibits confirmation bias, favoring information that aligns with prior context. This is categorized as a non-embodied, informal reasoning failure of the fundamental type. Alternatively, robustness issues in formal reasoning might be observed when an LLM performs inconsistently on math word problems depending on prompt phrasing.

## Visual

Figure 1 in the paper presents a taxonomy table with rows for reasoning categories (embodied, non-embodied informal, non-embodied formal) and columns for failure types (fundamental, application-specific, robustness). Each cell is populated with representative examples and explanations.

## Relationship to Other Concepts

- **Cognitive Biases In LLMs** — A specific category of fundamental failures in informal reasoning.
- **Theory Of Mind In LLMs** — Application-specific limitations in implicit social reasoning.

## Practical Applications

The taxonomy guides researchers in identifying and categorizing reasoning failures, informing the development of targeted mitigation strategies. It is useful for benchmarking LLMs, designing evaluation protocols, and improving robustness in real-world applications such as decision-making, social reasoning, and multi-agent systems.

## Sources

- [[Large Language Model Reasoning Failures]] — primary source for this concept
