"""Shared checkpoint state heuristics for ingest and backfill flows."""

from __future__ import annotations

from checkpoint_classifier import CLASS_DURABLE_ARCHITECTURE, CLASS_PROJECT_PROGRESS, COMPRESS

KNOWLEDGE_STATE_PLANNED = "planned"
KNOWLEDGE_STATE_EXECUTED = "executed"
KNOWLEDGE_STATE_VALIDATED = "validated"

_PLANNING_TITLE_HINTS = ("planning", "audit", "exploration")
_PLANNING_BODY_HINTS = (
    "<next_steps>",
    "open questions",
    "conversation compacted before",
    "plan + tracker",
    "sql todos seeded",
    "branch + tracker",
)
_NO_EXECUTION_HINTS = (
    "no code changes made this session",
    "files modified this session: **none**",
    "files modified: **none**",
    "(no edits yet this session)",
)
_EXECUTION_HINTS = (
    "- [x] implementation",
    "- [x] tests",
    "- [x] deploy",
    "merged feature branches",
    "deployed and verified",
    "committed, pushed",
    "implemented ",
    "fixed ",
    "updated ",
    "deployed ",
)
_VALIDATION_HINTS = (
    "validated",
    "verified",
    "confirmed",
    "tests passed",
    "all tests passed",
    "dry-run",
    "smoke test",
    "healthy",
    "regression coverage",
    "retrieved live",
    "checked live",
)
_ARCHITECTURE_PLANNING_HINTS = (
    "design doc",
    "design spec",
    "architecture review",
    "proposed approach",
    "recommended next steps",
    "implementation plan",
)


def is_planning_only_checkpoint(
    title: str,
    body: str,
    checkpoint_class: str,
    retention_mode: str,
) -> bool:
    """Return True for project-progress checkpoints that contain plans, not outcomes."""
    if checkpoint_class != CLASS_PROJECT_PROGRESS or retention_mode != COMPRESS:
        return False

    lower_title = (title or "").lower()
    lower_body = (body or "").lower()

    if any(hint in lower_body for hint in _NO_EXECUTION_HINTS):
        return True

    title_planning = any(hint in lower_title for hint in _PLANNING_TITLE_HINTS)
    planning_hits = sum(1 for hint in _PLANNING_BODY_HINTS if hint in lower_body)
    has_execution = any(hint in lower_body for hint in _EXECUTION_HINTS)

    return title_planning and planning_hits >= 2 and not has_execution


def derive_knowledge_state(
    title: str,
    body: str,
    checkpoint_class: str,
    retention_mode: str,
) -> str:
    """Classify the checkpoint's claimed execution posture."""
    lower_title = (title or "").lower()
    lower_body = (body or "").lower()
    haystack = f"{lower_title}\n{lower_body}"

    if is_planning_only_checkpoint(title, body, checkpoint_class, retention_mode):
        return KNOWLEDGE_STATE_PLANNED

    has_validation = any(hint in haystack for hint in _VALIDATION_HINTS)
    has_execution = any(hint in haystack for hint in _EXECUTION_HINTS)
    architecture_planning = (
        checkpoint_class == CLASS_DURABLE_ARCHITECTURE
        and any(hint in haystack for hint in _ARCHITECTURE_PLANNING_HINTS)
        and not has_execution
        and not has_validation
    )

    if architecture_planning:
        return KNOWLEDGE_STATE_PLANNED
    if has_validation:
        return KNOWLEDGE_STATE_VALIDATED
    if has_execution:
        return KNOWLEDGE_STATE_EXECUTED
    if checkpoint_class == CLASS_DURABLE_ARCHITECTURE:
        return KNOWLEDGE_STATE_PLANNED
    return KNOWLEDGE_STATE_EXECUTED


__all__ = [
    "KNOWLEDGE_STATE_EXECUTED",
    "KNOWLEDGE_STATE_PLANNED",
    "KNOWLEDGE_STATE_VALIDATED",
    "derive_knowledge_state",
    "is_planning_only_checkpoint",
]
