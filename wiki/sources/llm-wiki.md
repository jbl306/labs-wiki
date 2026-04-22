---
title: LLM Wiki
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: 2e702592daf7ccd63d3f0229d4e688c3f21b4758ddb58ad0fb402ccb2fa337b6
sources:
- raw/2026-04-07-llm-wiki.md
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags:
- gist
- github
- karpathy
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
---

# LLM Wiki

## Summary

A pattern for building personal knowledge bases using LLMs.

## Repository Info

- **Source URL**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Author**: karpathy
- **Gist ID**: `442a6bf555914893e9891c11519de94f`
- **Content size**: 11,922 chars

## Content Excerpt

# LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and eve…

## Crawled Files

Source dump in `raw/2026-04-07-llm-wiki.md` includes:

- gist `karpathy/442a6bf555914893e9891c11519de94f` (single-file gist, raw text)
