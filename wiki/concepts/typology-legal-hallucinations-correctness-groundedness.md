---
title: "Typology of Legal Hallucinations: Correctness and Groundedness"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "35e9fc85797a2b2f1a36afddb2e31c48be2da7111d6965af4170541cbeaf7331"
sources:
  - raw/2026-04-14-legal_rag_hallucinationspdf.md
quality_score: 56
concepts:
  - typology-legal-hallucinations-correctness-groundedness
related:
  - "[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]"
  - "[[Legal RAG Hallucinations]]"
tier: hot
tags: [hallucination, typology, correctness, groundedness, legal-ai, evaluation]
---

# Typology of Legal Hallucinations: Correctness and Groundedness

## Overview

The article introduces a refined typology for legal hallucinations, decomposing them into two primary dimensions: correctness (factual accuracy and relevance) and groundedness (validity of cited sources). This framework enables more rigorous evaluation of legal AI outputs and clarifies the risks posed by hallucinations.

## How It Works

Correctness refers to whether the AI's response is factually accurate and relevant to the user's query. A response is labeled correct if it contains accurate information and addresses the query, incorrect if it contains factual errors, and refusal if the model declines to answer or provides irrelevant information.

Groundedness applies to correct responses and assesses whether key factual propositions are validly supported by relevant legal documents. A response is grounded if it cites authoritative sources that genuinely support its claims. Misgrounded responses cite sources that do not actually support the proposition, while ungrounded responses make factual claims without any citation.

This typology is illustrated in Table 1 of the article, using the example query: 'Does the Constitution protect a right to same sex marriage?' Correct and grounded: cites Obergefell v. Hodges, which supports the claim. Correct but misgrounded: cites Miranda v. Arizona, which is irrelevant. Correct but ungrounded: makes the claim without citation.

By decomposing hallucinations in this way, the framework provides nuanced guidance for legal professionals. It highlights that even factually correct answers can be misleading if not properly grounded, and that citation errors can be as dangerous as factual inaccuracies. The typology is used in the empirical evaluation to manually code responses from legal AI tools, enabling systematic comparison and vulnerability analysis.

The framework also informs the responsibilities of legal professionals, emphasizing the need for supervision and verification of AI outputs. It clarifies that 'hallucination-free' claims must be assessed not only for factual accuracy but also for proper grounding in legal authority.

## Key Properties

- **Correctness:** Factually accurate and relevant response; incorrect responses contain factual errors; refusals decline to answer or are irrelevant.
- **Groundedness:** Valid references to relevant legal documents; misgrounded responses cite irrelevant sources; ungrounded responses lack citation.
- **Manual Coding Criteria:** Responses are manually reviewed and coded for correctness and groundedness, enabling systematic evaluation.

## Limitations

Groundedness assessment is only applicable to correct responses; ambiguous legal queries and complex context can make coding difficult. Proprietary systems may obscure citation mechanisms, complicating evaluation.

## Example

Table 1 (from the article):
- Correct and grounded: 'The right to same sex marriage is protected under the U.S. Constitution. Obergefell v. Hodges, 576 U.S. 644 (2015).'
- Correct but misgrounded: 'The right to same sex marriage is protected under the U.S. Constitution. Miranda v. Arizona, 384 U.S. 436 (1966).'
- Correct but ungrounded: 'The right to same sex marriage is protected under the U.S. Constitution.'

## Visual

Table 1: Matrix summarizing coding criteria for correctness (correct, incorrect, refusal) and groundedness (grounded, misgrounded, ungrounded), with example responses for each category.

## Relationship to Other Concepts

- **[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]** — Typology provides the framework for evaluating hallucinations in legal RAG outputs.

## Practical Applications

Used to assess and improve legal AI tools, inform guidelines for ethical integration, and train legal professionals to spot errors and citation issues. Enables systematic vulnerability analysis and benchmarking of legal AI systems.

## Sources

- [[Legal RAG Hallucinations]] — primary source for this concept
