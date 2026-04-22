---
title: "OpenMementos Dataset"
type: entity
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "7b344980e889d401d340d2539bd18583a585c26640fe19f36c596d887e647ba2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
quality_score: 65
concepts:
  - openmementos-dataset
related:
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[microsoft/memento]]"
  - "[[Memento]]"
  - "[[Microsoft]]"
tier: hot
tags: [dataset, llm, summarization, chain-of-thought]
---

# OpenMementos Dataset

## Overview

The OpenMementos Dataset is a collection of chain-of-thought traces formatted in the Memento block+summary style, designed for supervised fine-tuning of LLMs to learn the Memento protocol. It is hosted on HuggingFace and referenced in the Memento repository.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Dataset |
| Created | Unknown |
| Creator | Microsoft |
| URL | https://huggingface.co/datasets/microsoft/OpenMementos |
| Status | Active |

## Relevance

This dataset provides the necessary training data for models to learn how to segment reasoning into blocks and generate effective summaries, which is essential for the success of the Memento approach.

## Associated Concepts

- **[[Memento Blockwise Summarization for LLMs]]** — Provides training traces in the required format.

## Related Entities

- **[[Memento]]** — Parent project
- **[[Microsoft]]** — Creator
- **vLLM Overlay for Memento** — co-mentioned in source (Tool)

## Sources

- [[microsoft/memento]] — where this entity was mentioned
