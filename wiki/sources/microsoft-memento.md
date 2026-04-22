---
title: microsoft/memento
type: source
created: '2026-04-21'
last_verified: '2026-04-21'
source_hash: d3cabcf1e262cf327625ca3be9427a8fb7c93529209aca175575f612e0fe5bb4
sources:
- raw/2026-04-21-httpsgithubcommicrosoftmemento.md
source_url: https://github.com/microsoft/memento
tags:
- github
- python
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
quality_score: 43
---

# microsoft/memento

## Summary

None

## Repository Info

- **Source URL**: https://github.com/microsoft/memento
- **Stars**: 377
- **Primary language**: Python

## README Excerpt

# Memento

[**Paper (PDF)**](docs/memento.pdf) | [**OpenMementos Dataset**](https://huggingface.co/datasets/microsoft/OpenMementos)

**Memento** extends the effective output length of large language models by splitting chain-of-thought reasoning into **blocks** and **summaries** (memento). After each reasoning block, the model generates a short summary, then the block content is evicted from the KV cache. The model continues from the summary with a shorter context, enabling more reasoning within a fixed context window.

## Activity Snapshot

### Recent Commits

- 2026-04-08 d8c10e6 Vasilis Kontonis: Add Memento blogpost and Pages deployment
- 2026-04-08 ebacb0c Vasileios Kontonis: Initial release: Memento data pipeline, vLLM block masking overlay, and paper
### Recently Merged PRs (top 10)

- #1 Adding Microsoft SECURITY.MD (merged 2026-03-25)

## Crawled Files

Source dump in `raw/2026-04-21-httpsgithubcommicrosoftmemento.md` includes:

- `data/.gitignore`
- `data/README.md`
- `data/requirements.txt`
- `LICENSE`
- `vllm/README.md`
- `SECURITY.md`
- `.github/workflows/static.yml`
- `blogpost/figures/build_animation.py`
- `blogpost/figures/build_animation_v2.py`
- `blogpost/figures/example_code.json`
- `blogpost/figures/example_response.json`
- `blogpost/figures/example_science.json`
- `blogpost/figures/extract_examples.py`
