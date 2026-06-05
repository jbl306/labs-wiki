# 2026-06-05 Codex ingest migration

## Goal

Replace the default Copilot CLI-based labs-wiki ingest/processing path with Codex CLI, then audit the repository for follow-up improvements.

## Acceptance Criteria

- Default unattended ingest backend is `codex-cli` rather than `copilot-cli`.
- Codex invocation is non-interactive, writes within the repo, preserves the existing final JSON status contract, and still supports legacy backends where useful.
- Auto-ingest/watch startup no longer requires a GitHub Models token when running through Codex.
- Docker auto-ingest image installs Codex CLI rather than GitHub Copilot CLI.
- Prompt/docs examples use `codex-cli-{MODEL_ID}` ingest metadata.
- Verification includes syntax/tests where available and at least one non-mutating Codex CLI smoke check.
- Repo improvement audit is recorded in this plan.

## Plan

1. Inspect current Copilot CLI backend, Dockerfile, prompt, and watcher token requirements.
2. Add Codex CLI backend and switch default routing to it.
3. Update prompt/Docker/docs references needed for the default path.
4. Run verification: Python compile, targeted tests/lint, CLI smoke checks.
5. Record improvement findings and remaining risks.

## Results

Completed 2026-06-05T20:31:16Z.

### Implemented

- Switched the default unattended backend to `codex-cli` via `_selected_backend()` and Docker `ENV WIKI_INGEST_BACKEND=codex-cli`.
- Added a non-interactive Codex CLI backend that runs `codex -a never exec ...` from the repo root, grants only workspace-write sandboxing, writes the last assistant message to a temporary status file, and parses the final embedded JSON status object.
- Kept `copilot-cli` as an explicit compatibility backend and left the legacy GitHub Models path available behind token-requiring backend selection.
- Removed the startup token requirement for Codex in both `scripts/auto_ingest.py` and `scripts/watch_raw.py` while preserving token checks for compatibility backends.
- Updated `Dockerfile.auto-ingest` to install `@openai/codex`, git, and ripgrep; copy the helper modules imported by `auto_ingest.py`; and provide a writable non-`/tmp` Codex home at `/home/codex`.
- Updated prompt and docs so new ingest metadata uses `codex-cli-{MODEL_ID}` and current examples default to `gpt-5.5`.
- Added regression coverage for default backend selection, token requirements, PDF effort routing, and Codex CLI argument ordering.
- Fixed two adjacent ingest issues found during audit: uploaded PDF file raws now route to high effort based on body / persisted metadata, and legacy file extraction honors `--refresh-fetch` like the agent CLI path.

### Verification

- `python3 -m py_compile ...` with the system interpreter: passed for touched Python files.
- First raw `python3 -m unittest discover -s tests -v`: failed because the host Python lacked project dependencies (`bs4`, `networkx`), not because of code failures.
- Built `/tmp/labs-wiki-verify-venv` with `uv` and installed `scripts/requirements-auto-ingest.txt` plus `wiki-graph-api/requirements.txt`.
- `/tmp/labs-wiki-verify-venv/bin/python -m py_compile ...`: passed.
- `/tmp/labs-wiki-verify-venv/bin/python -m unittest discover -s tests -v`: 6 tests passed.
- Codex non-mutating smoke: `codex -a never exec ... -s read-only ...` returned `{\"status\":\"ok\",\"backend\":\"codex-cli\"}`.
- Docker build: `docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest:codex-verify .` passed.
- Docker runtime smoke: `codex --version` and Python import/default-backend checks passed inside `labs-wiki-auto-ingest:codex-verify`.
- `git diff --check`: passed.

### Repo improvement audit

1. **Document parser seam:** current MarkItDown-only extraction is too hard-wired for PDF/layout-sensitive sources. The detailed implementation plan is recorded in `tasks/liteparse-integration-plan.md`.
2. **Dependency/test ergonomics:** this repo has tests but no single dev requirements file or pyproject tying together auto-ingest and graph test dependencies. Add a `requirements-dev.txt` or `pyproject.toml` test extra so `python -m unittest discover -s tests -v` works without reconstructing dependencies manually.
3. **Container smoke in CI:** Docker build/runtime smoke caught a real Codex-home warning. Add CI or a local script that builds `Dockerfile.auto-ingest` and runs `codex --version` plus import checks.
4. **Codex auth deployment:** the image has a writable `CODEX_HOME`, but deployment still needs an explicit auth/config mounting story for unattended homelab use.
5. **Docs split:** historical wiki pages still mention Copilot/GitHub Models, which is correct provenance; operational docs were updated, but future docs should clearly separate historical sources from current runtime setup.
