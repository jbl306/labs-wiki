# AutoAgent Integration Plan

> Deep research and integration plan for [HKUDS/AutoAgent](https://github.com/HKUDS/AutoAgent) in the homelab environment.
> Created: 2025-07-17

---

## What Is AutoAgent?

AutoAgent (formerly MetaChain) is a **fully-automated, zero-code framework for creating and deploying LLM agents through natural language**. Developed by the HKUDS lab at the University of Hong Kong, it allows users to build tools, agents, and multi-agent workflows without writing code.

### Core Architecture

```
┌─────────────────────────────────────────────────┐
│                  AutoAgent CLI                    │
│    auto main  |  auto deep-research  |  auto agent│
├─────────┬──────────┬────────────────────────────┤
│User Mode│Agent     │Workflow Editor              │
│(research)│Editor   │(multi-agent pipelines)      │
├─────────┴──────────┴────────────────────────────┤
│              MetaChain Engine                     │
│   ┌──────────┐ ┌──────────┐ ┌───────────────┐   │
│   │ Registry │ │ LiteLLM  │ │ Event Flow    │   │
│   │ (agents, │ │ (20+ LLM │ │ (async DAG    │   │
│   │  tools)  │ │ providers)│ │  execution)   │   │
│   └──────────┘ └──────────┘ └───────────────┘   │
├──────────────────────────────────────────────────┤
│              Execution Environments               │
│   Docker Sandbox  |  Local Env  |  Browser Env   │
├──────────────────────────────────────────────────┤
│              Memory Systems                       │
│   ChromaDB RAG | Tool Memory | Code Memory       │
└──────────────────────────────────────────────────┘
```

### Three Operating Modes

| Mode | Purpose | Description |
|------|---------|-------------|
| **User Mode** | Task execution | Multi-agent research assistant with routing triage agent. Routes to File Surfer, Web Surfer, or Coder agents. |
| **Agent Editor** | Create agents via NL | Dynamically generates tool code, agent definitions, and registers them at runtime. Self-modifying: clones itself into sandbox. |
| **Workflow Editor** | Create pipelines via NL | Builds multi-agent workflows with DAG execution, parallel agent runs, and vote aggregation. |

### Built-in Agent Teams

| Agent | Role | Tools |
|-------|------|-------|
| System Triage Agent | Routes tasks to specialists | Agent transfer |
| File Surfer Agent | Browse and analyze local files | read_file, list_files, search |
| Web Surfer Agent | Web browsing and scraping | Playwright, html2text |
| Coding Agent | Write and execute code | run_python, execute_command |
| Math Solver Agent | Mathematical problem solving | Code execution |
| Agent Creator Agent | Meta-agent: creates other agents | create_tool, create_agent |

### Key Technical Details

- **LLM Backend**: LiteLLM v1.55.0 — supports OpenAI, Anthropic, DeepSeek, Gemini, Groq, Mistral, HuggingFace, OpenRouter, and any OpenAI-compatible endpoint
- **Default Model**: `claude-3-5-sonnet-20241022`
- **Docker**: Pre-built images (`tjbtech1/metachain:amd64_latest` / `arm64`), auto-pulled
- **Memory**: ChromaDB for RAG, tool indexing, code tree storage
- **CLI**: `auto` command via Click, Rich terminal UI, prompt_toolkit completion
- **REST API**: FastAPI server with `/agents/{name}/run`, `/tools/{name}`, `/agents` endpoints
- **Python**: ≥3.10, ~60 dependencies including playwright, docling, sentence-transformers

---

## Why Consider AutoAgent?

### Strengths

1. **Zero-code agent creation** — Create tools and agents via natural language descriptions, no Python needed
2. **Self-modifying framework** — Can generate its own tools and agents at runtime, then persist them
3. **Multi-provider LLM support** — 20+ providers through LiteLLM, easy model switching
4. **Sandboxed execution** — Docker containers isolate agent code execution
5. **Deep research mode** — Lightweight `auto deep-research` matches OpenAI Deep Research quality
6. **REST API** — FastAPI endpoints for programmatic agent execution
7. **Extensible registry** — Decorator-based plugin system (`@register_plugin_tool`, `@register_agent`)
8. **Event-driven workflows** — Async DAG execution with parallel agent coordination

### Weaknesses

1. **No MCP support** — Zero Model Context Protocol integration (no server, no client, not mentioned anywhere)
2. **No web UI** — Interactive terminal only; web GUI listed as "under development"
3. **Heavy dependencies** — ~60 packages including playwright, docling, faster-whisper, moviepy, sentence-transformers
4. **Pinned LiteLLM** — Locked to v1.55.0 (current is v1.60+), may cause compatibility issues
5. **Docker image opacity** — Uses pre-built images from `tjbtech1/`, no Dockerfile to customize
6. **No Docker Compose** — Manual container management, no compose file provided
7. **Early stage** — v0.1.0, API likely unstable, sparse documentation
8. **Interactive-first** — Designed for interactive CLI sessions, not headless/service mode
9. **Large footprint** — Expects full browser environment (Playwright), audio processing stack, etc.
10. **No GitHub Models API support** — `GITHUB_AI_TOKEN` is for git operations only, not model inference

---

## Comparison: AutoAgent vs Current Stack

### Feature Matrix

| Capability | Copilot CLI | OpenCode | AutoAgent | MemPalace | labs-wiki |
|-----------|-------------|----------|-----------|-----------|-----------|
| **Agent execution** | ✅ Native | ✅ Native | ✅ Core feature | ❌ Memory only | ❌ Knowledge only |
| **MCP support** | ✅ Full | ✅ Full | ❌ None | ❌ N/A | ✅ Via skills |
| **Custom agents** | ✅ AGENTS.md | ✅ agents.json | ✅ NL creation | ❌ N/A | ✅ Skill files |
| **Memory/context** | ✅ Session | ✅ Session | ✅ ChromaDB RAG | ✅ Core feature | ✅ Wiki pages |
| **Web research** | ✅ web_search | ✅ Via tools | ✅ Built-in | ❌ N/A | ❌ N/A |
| **Code execution** | ✅ Bash/inline | ✅ Bash/inline | ✅ Docker sandbox | ❌ N/A | ❌ N/A |
| **Multi-agent** | ✅ Sub-agents | ✅ Via config | ✅ Workflow DAGs | ❌ N/A | ❌ N/A |
| **LLM flexibility** | ❌ GitHub only | ✅ Multi-provider | ✅ 20+ providers | ❌ N/A | ✅ GitHub Models |
| **Headless/service** | ❌ Interactive | ✅ Can be | ⚠️ CLI-focused | ✅ CLI tool | ✅ Auto-ingest |
| **Self-modifying** | ❌ No | ❌ No | ✅ Core feature | ❌ No | ❌ No |

### Overlap Analysis

**AutoAgent overlaps with Copilot CLI/OpenCode in:**
- Agent task routing and execution
- Web research capabilities
- Code generation and execution
- File system operations

**AutoAgent offers unique value in:**
- Zero-code agent/tool creation via natural language
- Self-modifying agent framework
- Workflow DAG orchestration with parallel execution
- REST API for programmatic access

**AutoAgent lacks compared to current stack:**
- MCP integration (critical for MemPalace/labs-wiki bridge)
- GitHub Models API support (free inference for homelab)
- Lightweight deployment (heavy dependency chain)
- Mature documentation and stable API

---

## Integration Options

### Option A: Full Deployment (Not Recommended)

Deploy AutoAgent as a standalone service alongside Copilot CLI/OpenCode.

**Pros**: Full feature access, independent operation
**Cons**: Massive overlap with existing tools, heavy resource footprint, no MCP bridge, maintenance burden

**Verdict**: ❌ Too much overlap with Copilot CLI + OpenCode. Both already handle agent execution, web research, and code generation with MCP support that AutoAgent lacks.

### Option B: Deep Research Service Only (Recommended)

Deploy AutoAgent's `auto deep-research` mode as a dedicated research service, callable from Copilot CLI/OpenCode.

```
Copilot CLI / OpenCode
    │
    ▼ (shell command or REST API)
AutoAgent deep-research
    │
    ├── Web Surfer Agent (Playwright browsing)
    ├── File Surfer Agent (document analysis)
    └── Coding Agent (data processing)
    │
    ▼ (results)
labs-wiki raw/ → auto-ingest pipeline
```

**Pros**:
- Leverages AutoAgent's strongest feature (deep research)
- Complements Copilot CLI/OpenCode rather than competing
- REST API allows programmatic invocation
- Results feed directly into labs-wiki knowledge pipeline

**Cons**:
- Still heavy dependencies for one feature
- Docker container overhead
- No MCP bridge (must use REST API or shell)

### Option C: Cherry-Pick Ideas (Recommended Companion)

Extract architectural patterns from AutoAgent to enhance labs-wiki and Copilot workflows, without deploying AutoAgent itself.

**Ideas worth borrowing:**

1. **Registry-based tool/agent system** — Apply to labs-wiki skills for auto-discovery
2. **Event-driven workflow DAGs** — Add to `wiki-orchestrate` for parallel processing
3. **REST API for agent execution** — Extend `wiki-ingest-api` to support query/lint/update endpoints
4. **NL tool creation pattern** — Copilot CLI custom agents already achieve this via AGENTS.md
5. **Vote aggregation** — Multi-model consensus for wiki quality scoring

---

## Recommended Plan: Option B + C Hybrid

### Phase 1: Deploy Deep Research Service

Deploy AutoAgent as a Docker service limited to `auto deep-research` mode.

**Container Configuration:**

```yaml
# compose.wiki.yml addition
  autoagent:
    image: tjbtech1/metachain:amd64_latest
    container_name: autoagent
    restart: unless-stopped
    ports:
      - "12346:12346"
    volumes:
      - ${AUTOAGENT_PATH}:/autoagent
      - ${AUTOAGENT_WORKSPACE}:/workspace
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}      # Or use OpenAI-compatible
      - COMPLETION_MODEL=${AUTOAGENT_MODEL:-gpt-4o}
      - GITHUB_AI_TOKEN=${GITHUB_TOKEN}
    working_dir: /autoagent
    command: >
      /bin/bash -c "
        pip install -e . &&
        uvicorn autoagent.server:app --host 0.0.0.0 --port 8000
      "
    networks:
      - wiki-net
```

**Alternatively (lighter):** Install via pipx alongside MemPalace:
```bash
cd ~/projects
git clone https://github.com/HKUDS/AutoAgent.git
cd AutoAgent
pipx install -e . --python python3.12
```

**⚠️ Warning**: The ~60 dependencies are heavy. Docker isolation recommended.

### Phase 2: Bridge to labs-wiki

Create a capture script that runs AutoAgent deep research and feeds results into `raw/`:

```bash
#!/bin/bash
# scripts/autoagent-research.sh
# Usage: ./scripts/autoagent-research.sh "research topic"

TOPIC="$1"
SLUG=$(echo "$TOPIC" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 50)
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="raw/${DATE}-autoagent-${SLUG}.md"

# Run AutoAgent deep research via REST API
RESULT=$(curl -s -X POST http://localhost:8000/agents/deep_research/run \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$TOPIC\", \"model\": \"gpt-4o\"}")

# Write as raw source
cat > "$OUTPUT_FILE" << EOF
---
title: "AutoAgent Research: ${TOPIC}"
type: text
captured: $(date -Iseconds)
source: autoagent
tags: [research, autoagent]
status: pending
---

${RESULT}
EOF

echo "Research saved to ${OUTPUT_FILE}"
echo "Auto-ingest will process it automatically."
```

### Phase 3: Cherry-Pick Enhancements

Incorporate AutoAgent patterns into existing infrastructure:

| Enhancement | Target | Effort | Value |
|------------|--------|--------|-------|
| REST API for wiki skills | wiki-ingest-api | Medium | High — programmatic query/lint/update |
| Registry auto-discovery | labs-wiki skills | Low | Medium — auto-find skill files |
| Parallel workflow DAG | wiki-orchestrate | Medium | Medium — parallel lint + ingest |
| Multi-model consensus | auto-ingest | Low | Medium — quality scoring validation |

---

## Resource Requirements

### Minimum (Deep Research Only)

| Resource | Requirement |
|----------|-------------|
| RAM | 2-4 GB (Python + ChromaDB + Playwright) |
| Disk | ~2 GB (dependencies + browser + workspace) |
| CPU | 1-2 cores |
| GPU | Not required (LLM inference is remote) |
| Network | Outbound HTTPS for LLM APIs |
| Docker | Required for sandbox execution |

### Full Deployment

| Resource | Requirement |
|----------|-------------|
| RAM | 4-8 GB (all agents + browser + memory) |
| Disk | ~5 GB (dependencies + images + workspace) |
| CPU | 2-4 cores |
| Docker | 2 containers (host + sandbox) |

### Cost

- **LLM API costs**: Depends on provider. Using GitHub Models API (free tier: 149 req/min) would require an OpenAI-compatible proxy since AutoAgent doesn't natively support it.
- **Infrastructure**: Docker container overhead on existing homelab server.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Dependency conflicts with MemPalace/labs-wiki | Medium | Isolate via Docker or separate pipx venv |
| API instability (v0.1.0) | High | Pin to specific commit, don't auto-update |
| No MCP bridge | Medium | Use REST API + shell scripts as bridge |
| Heavy resource usage | Medium | Limit to deep-research mode only |
| Maintenance burden | Medium | Evaluate quarterly; remove if unused |
| LiteLLM version lock (v1.55.0) | Low | Only matters inside AutoAgent container |

---

## Decision Matrix

| Factor | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| Unique value over current stack | 30% | 3 | 0.90 |
| Integration ease | 20% | 2 | 0.40 |
| Resource efficiency | 15% | 2 | 0.30 |
| Maintenance burden (inverse) | 15% | 2 | 0.30 |
| Community/stability | 10% | 2 | 0.20 |
| Future potential | 10% | 4 | 0.40 |
| **Total** | **100%** | | **2.50/5** |

**Score: 2.5/5** — Marginal value. The deep research capability is interesting but the lack of MCP, heavy dependencies, and massive overlap with Copilot CLI/OpenCode make full adoption hard to justify.

---

## Recommendation

**Deploy cautiously as a deep research sidecar (Option B), and cherry-pick architectural ideas (Option C).**

### Immediate Actions (Low effort, high learning)
1. Clone repo locally, experiment with `auto deep-research` using existing API keys
2. Test REST API endpoints for programmatic research triggering
3. Evaluate research quality vs Copilot CLI's `web_search` tool

### Defer Until
- AutoAgent adds MCP support (would enable direct bridge to MemPalace/labs-wiki)
- AutoAgent adds web UI (would enable non-terminal access)
- AutoAgent reaches v1.0 (API stability)
- A specific use case emerges that Copilot CLI/OpenCode cannot handle

### Skip Entirely
- Agent Editor mode (Copilot CLI custom agents + AGENTS.md already covers this)
- Workflow Editor mode (Copilot CLI sub-agents + skills already handle orchestration)
- Full deployment (too much overlap, too heavy)

---

## Next Steps (If Proceeding)

- [ ] Clone AutoAgent repo to homelab projects
- [ ] Create isolated pipx/Docker environment
- [ ] Test `auto deep-research` with a real research query
- [ ] Benchmark research quality vs Copilot CLI web_search
- [ ] If quality justifies: create Docker Compose service entry
- [ ] If quality justifies: create `scripts/autoagent-research.sh` bridge
- [ ] Cherry-pick: add REST API endpoints to wiki-ingest-api for query/lint
- [ ] Cherry-pick: add parallel execution to wiki-orchestrate skill
