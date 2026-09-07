# Codex durable session memory

On 2026-09-07, selective automatic MemPalace checkpoints were authorized for
Labs Wiki work. Codex stages decisions, verified results, and unresolved
blockers with explicit execution state and project-file evidence. Ordinary
conversation and unchanged facts need no checkpoint.

The versioned implementation is
[`integrations/codex/mempalace_durable.py`](../integrations/codex/mempalace_durable.py).
The installed copy lives at `/home/jbl/.codex/hooks/mempalace_durable.py`.
The policy is in
`/home/jbl/.codex/AGENTS.md`, and the hooks are in
`/home/jbl/.codex/hooks.json`.

SessionStart supplies the policy. Stop and PreCompact save staged records to
MemPalace's `labs_wiki/session-checkpoints` room through the already-connected
MCP server. The launcher extends the installed native server, preserving its
writer-lock and read-only checks. A standalone hook process cannot write while
the MCP server holds the palace lock, so saves run inside that server.

Checkpoints use private local staging, bounded validation, common credential
pattern rejection, exact duplicate protection, and acknowledged-save receipts.
Failed saves retain their pending data. The agent must still select facts
carefully: validation does not prove their truth or detect every possible
secret. No transcript is read or mined by the selective path. Existing
transcript watchers and other clients are separate, unchanged integrations.

The 2026-09-07 verification used six focused unit tests and the native MCP
JSON-RPC transport against a temporary palace, including duplicate delivery
and the read-only gate. The review findings were also saved and read back from
the live MemPalace connection, retaining their local-tested/undeployed status.
All three memory hooks were verified enabled and trusted, and the connected
server exposed `mempalace_durable_hook`.

This authorization covers session checkpoints. It does not automatically
publish compiled wiki pages or sources, refresh verification dates, or extend
capture to other projects.

## Runtime and maintenance

This adapter targets the installed MemPalace Python interface and the local
`/home/jbl/projects/labs-wiki` checkout. The MemPalace MCP launcher runs the
installed adapter with `--mcp`; SessionStart runs it as a command hook, while
Stop and PreCompact invoke its MCP tool. Keep the installed copy synchronized
with the versioned source when applying future changes. Do not copy personal
configuration, hook trust state, or checkpoint data into the repository.

`--stage` reads a JSON object from stdin and uses `CODEX_THREAD_ID` for the
session. If that variable is unavailable, set it to the session ID supplied by
SessionStart. For example, from the Labs Wiki checkout:

```bash
/home/jbl/.local/share/pipx/venvs/mempalace/bin/python \
  /home/jbl/.codex/hooks/mempalace_durable.py --stage <<'JSON'
{"project":"labs-wiki","items":[{"kind":"decision","state":"implemented","summary":"Selected Labs Wiki checkpoints use the connected native MCP writer to preserve its palace lock.","evidence":["docs/codex-durable-memory.md"]}]}
JSON
```

Each checkpoint accepts 1–8 items. Kind is `decision`, `result`, or `blocker`;
state is `planned`, `implemented`, `tested`, `deployed`, or `unresolved`.
Each item needs a single-line summary of 15–800 characters and 1–4 existing,
relative, non-sensitive project file references. The complete input is bounded
to 16,384 characters.

Stage success means queued. Stop/PreCompact save pending data automatically.
For an immediate receipt, call `mempalace_durable_hook` with an `event` object
containing `hook_event_name: Stop`, the current `session_id`, and the project
`cwd`. Pending records and acknowledged receipts stay in the private local
`~/.mempalace/codex_checkpoints/` directory. Do not run the diagnostic `--flush`
as a separate writer while MCP owns the palace lock.

The native auto-save opt-out and writer gates remain effective. This adapter
supports direct native routing; daemon-required routing retains checkpoints
for retry and reports failure. Other sessions delegate to the installed native
hook behavior. Once a session stages Labs Wiki data, its session directory
keeps it on the selective path even if the working directory changes.

## Checks

Run from the repository root with the installed MemPalace interpreter:

```bash
/home/jbl/.local/share/pipx/venvs/mempalace/bin/python -m unittest discover \
  -s integrations/codex -p test_mempalace_durable.py -v
/home/jbl/.local/share/pipx/venvs/mempalace/bin/python \
  integrations/codex/check_mempalace_durable_integration.py
```

The integration check uses a temporary palace and the actual native JSON-RPC
transport. It verifies tool registration, save acknowledgment, duplicate
delivery, receipt creation, and the read-only tool gate without writing to
production memory. Rerun both checks after MemPalace upgrades. A new Codex
session loads launcher changes; changed hook definitions also require review
and trust through Codex's hook configuration.
