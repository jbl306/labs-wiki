# Tool Setup

Global `/home/jbl/.codex/AGENTS.md` owns workflow and testing policy. The repository's
`AGENTS.md` owns wiki schema, provenance, transaction, and release constraints.
Load personal `wiki-*` skills from `/home/jbl/.agents/skills` for the requested
workflow. Domain personas live in `agents/`. Client-specific instruction copies
and automatic instruction mirroring are retired.

## Labs-Wiki MCP Server

`scripts/wiki_mcp_server.py` provides the local read/graph tools and the
authenticated `wiki_capture` tool. Set these variables in the MCP server
process to enable capture:

| Variable | Required | Description |
|----------|----------|-------------|
| `WIKI_INGEST_API_BASE_URL` | Yes | HTTPS base URL for the wiki ingest API; HTTP is accepted only for `localhost` or an IP loopback address |
| `WIKI_INGEST_API_TOKEN` | Yes | Raw bearer token sent to `POST /api/ingest` |

`wiki_capture` accepts only `url`, `text`, or `note` captures and validates
request sizes before making a network call. Adding or enabling this server in
a Codex or Hermes MCP client is a separately authorized live configuration
step; this repository change does not modify client configuration or call the
live API.

The base URL and URL-capture tool are operator-trusted capabilities. The base
URL determines where the MCP process sends its bearer token, and an accepted
URL capture can cause the downstream ingest pipeline to fetch that URL. Point
the tool only at an ingest service you control, and do not expose URL capture
to untrusted callers.

Capture is explicitly non-idempotent: every accepted request creates a new raw
source, adding a numeric filename suffix when needed. The MCP client makes one
request and does not automatically retry network failures because a timeout
can occur after the server has written the source. An operator retry may
therefore create a duplicate.

The ingest API itself must set `WIKI_API_TOKEN`; capture endpoints return
`503 Service Unavailable` without it. `WIKI_INGEST_API_TOKEN` must contain the
same raw token in the MCP server process.

## Codex CLI

### Prerequisites

- [Codex CLI](https://github.com/openai/codex) (`codex`)
- Authenticated Codex environment for unattended `codex exec` runs

### How It Works

Codex CLI is the primary unattended compile backend for `wiki-auto-ingest` (`WIKI_INGEST_BACKEND=codex-cli`). The orchestrator prepares a disposable workspace containing the selected source, domain context, `AGENTS.md`, and `scripts/prompts/wiki_ingest_prompt.md`. Codex proposes compiled output there; the orchestrator validates and publishes accepted results back into the repository.

### Usage

```bash
# Navigate to the repo
cd ~/projects/labs-wiki

# Default manual processing path: Codex CLI backend, no GitHub Models token required
python3 scripts/auto_ingest.py raw/<source>.md --project-root .

# Optional model/effort overrides
WIKI_INGEST_MODEL=gpt-5.5 WIKI_INGEST_EFFORT=high \
  python3 scripts/auto_ingest.py raw/<source>.md --project-root . --force

# Copilot CLI remains available only as a compatibility backend
WIKI_INGEST_BACKEND=copilot-cli python3 scripts/auto_ingest.py raw/<source>.md --project-root .
```
