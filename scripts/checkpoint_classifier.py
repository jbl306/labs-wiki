"""Checkpoint classification + retention policy for Copilot session checkpoints.

Used by:
- ``homelab/scripts/mempalace-session-curator.py`` — pre-classifies checkpoints
  before exporting them into ``labs-wiki/raw/`` so the class is durable in
  frontmatter.
- ``labs-wiki/scripts/auto_ingest.py`` — reads the class out of raw frontmatter
  (or re-classifies as a fallback) and decides retention.

Design constraints:
- Pure Python, stdlib only — must work in both repos without extra deps.
- Heuristic-only (regex on title + first ~3 KB of body). No LLM calls.
- Deterministic + cheap so it can run on every export.

Classes (see ``plans/copilot-session-checkpoint-curation.md``):
    durable-architecture   — system design, refactors, integration plans
    durable-debugging      — root-cause sessions, postmortems, failure narratives
    durable-workflow       — pipeline / workflow / process changes
    project-progress       — sprint progress, status tracking, deployments
    low-signal             — short or repetitive checkpoints with little reuse value
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Class taxonomy
# ---------------------------------------------------------------------------

CLASS_DURABLE_ARCHITECTURE = "durable-architecture"
CLASS_DURABLE_DEBUGGING = "durable-debugging"
CLASS_DURABLE_WORKFLOW = "durable-workflow"
CLASS_PROJECT_PROGRESS = "project-progress"
CLASS_LOW_SIGNAL = "low-signal"

ALL_CLASSES: tuple[str, ...] = (
    CLASS_DURABLE_ARCHITECTURE,
    CLASS_DURABLE_DEBUGGING,
    CLASS_DURABLE_WORKFLOW,
    CLASS_PROJECT_PROGRESS,
    CLASS_LOW_SIGNAL,
)

# ---------------------------------------------------------------------------
# Retention modes
# ---------------------------------------------------------------------------

RETAIN = "retain"      # default behaviour — first-class wiki source page
COMPRESS = "compress"  # extract concepts/entities, archive the source page
SKIP = "skip"          # ingest only into MemPalace; no wiki compile

DEFAULT_RETENTION: dict[str, str] = {
    CLASS_DURABLE_ARCHITECTURE: RETAIN,
    CLASS_DURABLE_DEBUGGING: RETAIN,
    CLASS_DURABLE_WORKFLOW: RETAIN,
    CLASS_PROJECT_PROGRESS: COMPRESS,
    CLASS_LOW_SIGNAL: SKIP,
}

# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

# Order matters: most specific durable signals first; project-progress catches
# anything sprint/status-shaped before falling through to low-signal.
_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        CLASS_DURABLE_DEBUGGING,
        re.compile(
            r"\b(root[\s-]?cause|postmortem|post[\s-]?mortem|outage|"
            r"oom|memory leak|stack ?trace|regression|flake|hotfix|"
            r"timeout fix|crash|kernel panic|segfault|deadlock|"
            r"race condition|silent (failure|bug)|reproduc(e|ed|tion))\b",
            re.IGNORECASE,
        ),
    ),
    (
        CLASS_DURABLE_ARCHITECTURE,
        re.compile(
            r"\b(architecture|architectur(e|al) (decision|change|review)|"
            r"refactor(?!ed code style)|redesign|rewrite|migration|"
            r"integration|api design|schema (change|design|migration)|"
            r"data ?model|new service|service split|deduplicat|graph(\s|-)?(api|design)|"
            r"(adopt|introduce|switch to|move to)|"
            r"design (doc|spec|rationale)|wiki (architecture|design)|"
            r"(initial|new) implementation)\b",
            re.IGNORECASE,
        ),
    ),
    (
        CLASS_DURABLE_WORKFLOW,
        re.compile(
            r"\b(pipeline (change|fix|design|update)|workflow|"
            r"runbook|playbook|orchestrat|deployment (process|model|workflow)|"
            r"ci(?:/cd)?|cron(?: job)?|automation|"
            r"ingestion (loop|pipeline)|extraction (prompt|pipeline)|"
            r"hook( |s|-)integration|notification (system|setup)|"
            r"monitoring (setup|integration)|dashboard (setup|integration))\b",
            re.IGNORECASE,
        ),
    ),
    (
        CLASS_PROJECT_PROGRESS,
        re.compile(
            r"\b(sprint[\s-]?\d+|sprint planning|sprint (implementation|deployment|"
            r"complete|in[\s-]?progress|exploration|review|retro)|"
            r"in[\s-]?progress|wip|status|"
            r"deployed|deploying|retrain(ed|ing)?|"
            r"models? deploy|implementation update|progress (update|tracking)|"
            r"phase[\s-]?\d+|incremental (fix|update))\b",
            re.IGNORECASE,
        ),
    ),
)

_LOW_SIGNAL_MIN_CHARS = 600  # below this and no durable signal → low-signal


@dataclass(frozen=True)
class CheckpointClassification:
    cls: str
    matched_rule: str  # human-readable label of which heuristic fired
    body_chars: int


def classify_checkpoint(title: str, content: str) -> CheckpointClassification:
    """Classify a Copilot session checkpoint into one of ``ALL_CLASSES``.

    The title is weighted more heavily than the body because checkpoint titles
    in the index tend to be summaries chosen at the end of the session.
    """
    title = (title or "").strip()
    content = (content or "").strip()

    # Confine body inspection to the first 3000 chars. Checkpoints are usually
    # already short summaries; we don't need to scan tail boilerplate.
    body_window = content[:3000]
    haystack_title_only = title
    haystack_full = f"{title}\n\n{body_window}"

    for cls, pattern in _PATTERNS:
        m = pattern.search(haystack_title_only)
        if m:
            return CheckpointClassification(
                cls=cls,
                matched_rule=f"title:{m.group(0).lower()}",
                body_chars=len(content),
            )

    for cls, pattern in _PATTERNS:
        m = pattern.search(haystack_full)
        if m:
            return CheckpointClassification(
                cls=cls,
                matched_rule=f"body:{m.group(0).lower()}",
                body_chars=len(content),
            )

    if len(content) < _LOW_SIGNAL_MIN_CHARS:
        return CheckpointClassification(
            cls=CLASS_LOW_SIGNAL,
            matched_rule=f"length<{_LOW_SIGNAL_MIN_CHARS}",
            body_chars=len(content),
        )

    # Fallback: anything else is project-progress (status-shaped) rather than
    # durable, because durable rules are explicit. This errs on the side of
    # compression rather than first-class retention.
    return CheckpointClassification(
        cls=CLASS_PROJECT_PROGRESS,
        matched_rule="fallback",
        body_chars=len(content),
    )


# ---------------------------------------------------------------------------
# Retention policy
# ---------------------------------------------------------------------------


def _parse_overrides(raw: str) -> dict[str, str]:
    """Parse ``CLASS=mode,CLASS=mode`` env-var format into a dict."""
    out: dict[str, str] = {}
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk:
            continue
        key, _, value = chunk.partition("=")
        key = key.strip()
        value = value.strip().lower()
        if key in ALL_CLASSES and value in {RETAIN, COMPRESS, SKIP}:
            out[key] = value
    return out


def resolve_retention(cls: str, env: dict[str, str] | None = None) -> str:
    """Return ``retain | compress | skip`` for a checkpoint class.

    The mapping in ``DEFAULT_RETENTION`` can be overridden via the env var
    ``LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES`` with comma-separated
    ``class=mode`` entries.
    """
    if cls not in DEFAULT_RETENTION:
        return RETAIN  # unknown classes default to safe behaviour
    env = os.environ if env is None else env
    overrides = _parse_overrides(env.get("LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES", ""))
    return overrides.get(cls, DEFAULT_RETENTION[cls])


__all__ = [
    "ALL_CLASSES",
    "CLASS_DURABLE_ARCHITECTURE",
    "CLASS_DURABLE_DEBUGGING",
    "CLASS_DURABLE_WORKFLOW",
    "CLASS_PROJECT_PROGRESS",
    "CLASS_LOW_SIGNAL",
    "RETAIN",
    "COMPRESS",
    "SKIP",
    "DEFAULT_RETENTION",
    "CheckpointClassification",
    "classify_checkpoint",
    "resolve_retention",
]
