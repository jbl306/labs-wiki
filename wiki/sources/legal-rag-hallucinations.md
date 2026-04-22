---
title: "Legal RAG Hallucinations"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "35e9fc85797a2b2f1a36afddb2e31c48be2da7111d6965af4170541cbeaf7331"
sources:
  - raw/2026-04-14-legal_rag_hallucinationspdf.md
quality_score: 86
concepts:
  - hallucinations-in-legal-retrieval-augmented-generation-rag-systems
  - retrieval-augmented-generation-rag-legal-ai
  - typology-legal-hallucinations-correctness-groundedness
related:
  - "[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]"
  - "[[Typology of Legal Hallucinations: Correctness and Groundedness]]"
  - "[[LexisNexis (Lexis+ AI)]]"
  - "[[Thomson Reuters (Westlaw AI-Assisted Research)]]"
  - "[[Thomson Reuters (Ask Practical Law AI)]]"
tier: hot
knowledge_state: executed
tags: [evaluation, rag, hallucination, legal-research, llm, legal-ai]
---

# Legal RAG Hallucinations

## Summary

This article presents the first preregistered empirical evaluation of leading AI legal research tools, focusing on their reliability and the prevalence of hallucinations. It systematically assesses RAG-based proprietary legal AI tools, introduces a comprehensive dataset for vulnerability analysis, and proposes a nuanced typology for legal hallucinations. The study finds that while RAG reduces hallucinations compared to general-purpose LLMs, significant rates of hallucination persist, raising critical questions about the responsible integration of AI in legal practice.

## Key Points

- RAG-based legal AI tools (Lexis+ AI, Westlaw AI-Assisted Research, Ask Practical Law AI) hallucinate between 17% and 33% of the time.
- The article introduces a preregistered dataset of over 200 legal queries for systematic evaluation.
- A new typology decomposes legal hallucinations into correctness and groundedness, enabling more rigorous assessment.
- Empirical evidence shows that claims of 'hallucination-free' legal AI are overstated.
- Legal professionals must supervise and verify AI outputs, as hallucinations remain a central risk.

## Concepts Extracted

- **[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]** — Hallucinations in legal RAG systems refer to the generation of incorrect or misleading information by AI tools used for legal research, even when these tools employ retrieval-augmented generation mechanisms. Despite claims of 'hallucination-free' performance, empirical evidence shows that hallucinations persist at significant rates, posing risks for legal professionals relying on these systems.
- **Retrieval-Augmented Generation (RAG) in Legal AI** — Retrieval-Augmented Generation (RAG) is a technique that combines document retrieval with large language model generation to answer queries using domain-specific data. In legal AI, RAG is promoted as a solution to reduce hallucinations by grounding responses in authoritative legal content.
- **[[Typology of Legal Hallucinations: Correctness and Groundedness]]** — The article introduces a refined typology for legal hallucinations, decomposing them into two primary dimensions: correctness (factual accuracy and relevance) and groundedness (validity of cited sources). This framework enables more rigorous evaluation of legal AI outputs and clarifies the risks posed by hallucinations.

## Entities Mentioned

- **[[LexisNexis (Lexis+ AI)]]** — LexisNexis is a leading legal technology provider offering Lexis+ AI, an AI-driven legal research tool that employs retrieval-augmented generation (RAG) to answer legal queries. The tool is marketed as 'hallucination-free,' claiming to deliver accurate and authoritative answers grounded in a closed universe of legal content.
- **[[Thomson Reuters (Westlaw AI-Assisted Research)]]** — Thomson Reuters is a major legal technology provider whose Westlaw AI-Assisted Research tool uses retrieval-augmented generation (RAG) to answer legal queries. The tool is promoted as dramatically reducing hallucinations, with claims of near-zero hallucination rates.
- **[[Thomson Reuters (Ask Practical Law AI)]]** — Ask Practical Law AI is a legal research tool offered by Thomson Reuters, employing retrieval-augmented generation (RAG) to answer legal queries. The tool is evaluated for responsiveness and accuracy in the article, showing the highest rate of incomplete answers among tested systems.
- **GPT-4** — GPT-4 is a general-purpose large language model used as a baseline comparison in the article's empirical evaluation. It is not specialized for legal research and does not employ domain-specific retrieval mechanisms.

## Notable Quotes

> "While hallucinations are reduced relative to general-purpose chatbots (GPT-4), we find that the AI research tools made by LexisNexis (Lexis+ AI) and Thomson Reuters (Westlaw AI-Assisted Research and Ask Practical Law AI) each hallucinate between 17% and 33% of the time." — Legal RAG Hallucinations, Abstract
> "The binary notion of hallucination developed in Dahl et al. (2024) does not fully capture the behavior of RAG systems, which are intended to generate information that is both accurate and grounded in retrieved documents." — Legal RAG Hallucinations, Section 4

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-14-legal_rag_hallucinationspdf.md` |
| Type | paper |
| Author | Varun Magesh, Faiz Surani, Matthew Dahl, Mirac Suzgun, Christopher D. Manning, Daniel E. Ho |
| Date | 2025-03-14 |
| URL | https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf |
