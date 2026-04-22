---
title: HKUDS/AutoAgent
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 75c037c2356703a56f0c437652b8e9247474c4d6b491ee0379f7fa0e5ec6e8d8
sources:
- raw/2026-04-12-httpsgithubcomhkudsautoagent.md
source_url: https://github.com/HKUDS/AutoAgent
tags:
- agent
- github
- llms
- python
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 90
concepts:
- autoagent-framework-research
- natural-language-driven-agent-creation
- natural-language-driven-agent-building
- agent-tool-memory-loop
---

# HKUDS/AutoAgent

## What it is

AutoAgent (formerly MetaChain, HKU Data Science Lab) is a fully-automated, zero-code LLM agent framework. Instead of writing Python or wiring tool definitions, the user describes the agent or workflow in natural language and AutoAgent constructs, runs, and iteratively refines a multi-agent system to handle the task. It includes a CLI with three modes — `user mode` (a Deep Research–style assistant), `agent editor` (build single agents), and `workflow editor` (build multi-agent workflows).

## Why it matters

This is a research framework worth studying for ideas — particularly its natural-language-to-agent compilation and self-improvement loop — rather than a tool to deploy in our pipelines. For the `agent-organizer` and `agent-installer` workflows in our skill stack, AutoAgent's three-mode separation (use vs. build-agent vs. build-workflow) is a useful design pattern even if we never adopt the framework directly.

## Architecture / Technical model

- **Three operational modes** — `user mode` (Deep Research assistant), `agent editor` (single-agent creation), `workflow editor` (multi-agent workflow creation). Each mode is a distinct CLI entry point with separate interaction patterns.
> See [[autoagent-framework-research]] for the GAIA benchmark evaluation.

- **Natural-language agent building** — User describes the desired agent in dialogue; the system profiles the request, generates agent stubs (role, tools, instructions), and tests them in a sandboxed Docker environment. No Python code required from the user.
> See [[natural-language-driven-agent-building]] for the agent-editor workflow.

- **Self-play customization** — Iterative self-improvement loop: controller LLM generates tool/agent code → executes in Docker → observes failures → regenerates. Repeats until the agent satisfies the original request or a max-iteration limit is reached.
> See [[agent-tool-memory-loop]] for the agent loop pattern.

- **Zero-code framework** — All tool creation, agent scaffolding, and workflow orchestration happens through LLM code generation. The user never writes or edits code directly; they only provide natural-language descriptions and feedback.
> See [[natural-language-driven-agent-creation]] for the zero-code design philosophy.

- **Docker-sandboxed execution** — Agent code runs in a containerized environment (`deepresearch` container by default, port 12346). The image is auto-pulled based on the host architecture. Sandboxing prevents rogue generated code from affecting the host system.

- **LLM-agnostic** — Supports Anthropic (Claude), OpenAI (GPT), Deepseek, Gemini, Huggingface, Groq, XAI (Grok), and any OpenAI-compatible endpoint. Model selection via `COMPLETION_MODEL` env var (Litellm naming convention).

- **Git-clone mode** — For `agent editor` and `workflow editor`, the system clones a mirror of the AutoAgent repo into the Docker container (`autoagent_mirror` branch by default). This allows the controller LLM to self-modify the framework (create new tools, agents, workflows) within the sandboxed environment.

- **GAIA benchmark performance** — Claims Deep Research–parity using Claude 3.5 Sonnet (not o3). Also evaluated on Agentic-RAG (MultiHopRAG dataset). See `evaluation/gaia/` and `evaluation/multihoprag/` for reproduction scripts.

- **Third-party tool platform integration** — Supports RapidAPI and other tool platforms. Users subscribe to tools externally, then run `process_tool_docs.py` to register their API keys with AutoAgent.

## How it works

1. **Installation**: `git clone` → `pip install -e .` → Install Docker → Copy `.env.template` to `.env` and fill in API keys (at least `GITHUB_AI_TOKEN` + one LLM provider).
2. **CLI mode selection**: Run `auto main` (full framework), `auto deep-research` (user mode only), or specify agent-editor/workflow-editor via CLI prompts.
3. **User mode (Deep Research)**: System launches a pre-built multi-agent research assistant. User submits a research query; agents collaborate to retrieve, analyze, and synthesize results into a comprehensive report.
4. **Agent editor**: User describes the desired agent → system profiles the agent (role, tools, capabilities) → optionally generates new tools via code generation → scaffolds the agent → tests it (optionally against a user-provided task) → iterates until satisfied.
5. **Workflow editor**: User describes the desired multi-agent workflow → system profiles the workflow (agent roles, collaboration patterns) → scaffolds a DAG or sequential workflow → tests it → iterates.
6. **Docker container lifecycle**: Container is started on first run, reused for subsequent calls, and persists unless manually stopped. Agent code executes inside the container with access to cloned repos, tool libraries, and the file system mount.
7. **Self-play loop**: Controller LLM generates agent/tool code → `docker exec` runs it → captures logs/errors → feeds back to controller → regenerates if needed. Continues until success or max iterations.
8. **Tool platforms**: If using RapidAPI or similar, user runs `python process_tool_docs.py` to register API keys. AutoAgent then includes these tools in the agent scaffold.
9. **File uploads**: User mode supports file uploads for data interaction (e.g., upload a CSV, ask the agent to analyze it).
10. **Browser cookies**: Optional — user can import browser cookies into the Docker environment to let agents access authenticated websites. See `AutoAgent/environment/cookie_json/README.md`.

## API / interface surface

### CLI Commands

| Command | Description |
|---------|-------------|
| `auto main` | Start full AutoAgent (user mode + agent editor + workflow editor) |
| `auto deep-research` | Start lightweight user mode only (Deep Research assistant) |

### CLI Flags (for `auto` commands)

| Flag | Default | Description |
|------|---------|-------------|
| `--container_name` | `deepresearch` | Docker container name |
| `--port` | `12346` | Container port |
| `COMPLETION_MODEL` | `claude-3-5-sonnet-20241022` | LLM model (Litellm naming) |
| `DEBUG` | `False` | Enable debug logging |
| `API_BASE_URL` | `None` | Base URL for LLM provider (for OpenAI-compatible endpoints) |
| `FN_CALL` | `None` | Force function-calling mode (usually auto-detected) |
| `git_clone` | `True` | Clone AutoAgent repo mirror into Docker (agent-editor/workflow-editor only) |
| `test_pull_name` | `autoagent_mirror` | Branch name for cloned repo mirror |

### Environment Variables (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_AI_TOKEN` | **Yes** | GitHub personal access token |
| `OPENAI_API_KEY` | No | OpenAI API key (if using GPT models) |
| `DEEPSEEK_API_KEY` | No | Deepseek API key |
| `ANTHROPIC_API_KEY` | No | Anthropic API key (Claude) |
| `GEMINI_API_KEY` | No | Google AI Studio API key |
| `HUGGINGFACE_API_KEY` | No | Huggingface API key |
| `GROQ_API_KEY` | No | Groq API key |
| `XAI_API_KEY` | No | XAI (Grok) API key |
| `MISTRAL_API_KEY` | No | Mistral API key |
| `OPENROUTER_API_KEY` | No | OpenRouter API key |

### Evaluation Scripts

| Script | Purpose |
|--------|---------|
| `evaluation/gaia/scripts/run_infer.sh` | Run GAIA benchmark inference |
| `evaluation/gaia/get_score.py` | Compute GAIA scores |
| `evaluation/multihoprag/scripts/run_rag.sh` | Run Agentic-RAG inference (MultiHopRAG) |

### Tool Registration

```bash
python process_tool_docs.py
```
Prompts user to enter API keys for third-party tool platforms (RapidAPI, etc.)

## Setup

```bash
git clone https://github.com/HKUDS/AutoAgent.git
cd AutoAgent
pip install -e .

# Docker required — image auto-pulled on first run
cp .env.template .env
# Fill in: GITHUB_AI_TOKEN (required) + at least one of OPENAI_API_KEY / DEEPSEEK_API_KEY /
# ANTHROPIC_API_KEY / GEMINI_API_KEY / HUGGINGFACE_API_KEY / GROQ_API_KEY / XAI_API_KEY
auto deep-research      # or: auto agent / auto workflow
```

## Integration notes

Worth a deeper read for the `subagent-driven-development` and `agent-organizer` skills — particularly the agent-editor → workflow-editor separation. Not a fit for direct adoption inside the workspace; we already have a working Copilot CLI + OpenCode + MCP stack and don't need a competing agent runtime. The Docker-sandboxed code-generation pattern is, however, a good reference for any future code-execution sandbox in nba-ml-engine.

## Caveats / Gotchas

- **Requires Docker** — Agent execution happens in a containerized environment. Docker must be installed and running; the image is auto-pulled on first run.
- **Project renamed from MetaChain** — v0.2.0 (Feb 2025) renamed the project from MetaChain to AutoAgent. Older docs, blog posts, and GitHub issues may reference the old name.
- **Active research project** — APIs are not stabilized. Expect breaking changes between minor versions.
- **GitHub token required** — `GITHUB_AI_TOKEN` is mandatory even if you're not using GitHub-specific features. The token is used for internal repo cloning and version-controlled agent scaffolds.
- **Git-clone mode writes to Docker** — When `git_clone=True` (default for agent-editor/workflow-editor), the system clones a mirror of the AutoAgent repo into the Docker container and allows the controller LLM to self-modify it. This is powerful but opaque; tracking what changed requires inspecting the container's file system.
- **LLM function-calling detection** — The `FN_CALL` flag auto-detects whether the model supports function calling based on the Litellm model name. If detection fails, you must manually set `FN_CALL=True` or `FN_CALL=False`.
- **Tool platform API keys** — Third-party tools (RapidAPI, etc.) require external subscriptions and manual API key registration via `process_tool_docs.py`. The system does not handle subscription management.
- **GAIA benchmark claims** — The "Deep Research parity with Claude 3.5 Sonnet (not o3)" claim is based on the project's internal evaluation; independent replication results are not publicly available.
- **Container persistence** — The Docker container persists across sessions. If you want to reset the agent environment, you must manually stop and remove the container (`docker stop <name> && docker rm <name>`).
- **No license specified** — The repository does not include a LICENSE file; usage rights are unclear. Verify with the maintainers before production use.

## Related concepts

- [[autoagent-framework-research]]
- [[natural-language-driven-agent-building]]
- [[natural-language-driven-agent-creation]]
- [[agent-tool-memory-loop]]

## Source

- Raw dump: `raw/2026-04-12-httpsgithubcomhkudsautoagent.md`
- Upstream: https://github.com/HKUDS/AutoAgent
