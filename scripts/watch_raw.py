#!/usr/bin/env python3
"""Watch, reconcile and report pending Labs Wiki captures."""

from __future__ import annotations

import argparse
import fcntl
import json
import logging
import os
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ingest_transaction import commit_receipt_path
from auto_ingest import (
    _backend_requires_token,
    _selected_backend,
    classify_ingest_route,
    ingest_raw_source,
    notify_ingest_failure,
    parse_frontmatter,
)

log = logging.getLogger("watch-raw")
DEBOUNCE_SECONDS = float(os.environ.get("DEBOUNCE_SECONDS", "5"))
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", "1"))
RECONCILE_SECONDS = 60
MAX_ATTEMPTS = 5


def write_ingest_state(path: Path, state: dict) -> None:
    """Atomically replace one operator-readable runtime receipt."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as out:
        tmp_path = Path(out.name)
        try:
            json.dump(state, out)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise
    try:
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _retry_path(root: Path, raw: Path) -> Path:
    return root / ".cache/wiki-watcher/retries" / f"{raw.name}.json"


def _retry_record(root: Path, raw: Path) -> dict:
    try:
        return json.loads(_retry_path(root, raw).read_text())
    except FileNotFoundError:
        return {"attempts": 0, "next_attempt": 0}


def _due(root: Path, raw: Path, record: dict) -> bool:
    return (
        not _held(root, raw) and not (root / commit_receipt_path(raw)).exists()
        and record["attempts"] < MAX_ATTEMPTS
        and record["next_attempt"] <= time.time()
    )


def _record_attempt(root: Path, raw: Path, attempts: int, outcome: str) -> None:
    delay = min(3600, 60 * 3 ** (attempts - 1))
    write_ingest_state(_retry_path(root, raw), {
        "attempts": attempts, "next_attempt": time.time() + delay, "outcome": outcome,
    })


def _held(root: Path, raw: Path) -> bool:
    return (root / ".cache/wiki-watcher/holds" / raw.name).exists()


def backlog(root: Path) -> tuple[dict, list[Path]]:
    """Inspect durable source and retry state without changing it."""
    raw_dir = root / "raw"
    if not raw_dir.is_dir():
        raise FileNotFoundError(raw_dir)
    summary = {
        "pending": 0, "failed": 0, "held": 0, "exhausted": 0, "retrying": 0,
        "unreadable": [], "oldest_pending": None, "oldest_failed": None,
        "oldest_unsuccessful_pending": None,
        "unconfirmed_git_commits": sorted(
            path.stem for path in (root / ".cache/wiki-watcher/uncommitted").glob("*.json")
        ),
    }
    due = []
    now = time.time()
    for raw in sorted(raw_dir.glob("*.md")):
        try:
            fm, _ = parse_frontmatter(raw, header_only=True)
            status = fm.get("status")
            if not status:
                summary["unreadable"].append(raw.name)
                continue
            if status not in {"pending", "failed"}:
                continue
            summary[status] += 1
            try:
                captured = datetime.fromisoformat(str(fm.get("captured", "")).replace("Z", "+00:00"))
                captured_at = captured.replace(tzinfo=captured.tzinfo or timezone.utc).timestamp()
            except (ValueError, OverflowError):
                captured_at = raw.stat().st_mtime
            item = {"file": raw.name, "age_seconds": max(0, int(now - captured_at))}
            key = "oldest_" + status
            if summary[key] is None or item["age_seconds"] > summary[key]["age_seconds"]:
                summary[key] = item
            if status == "pending":
                retry = _retry_record(root, raw)
                if retry.get("outcome") == "pending_after_attempt":
                    oldest = summary["oldest_unsuccessful_pending"]
                    if oldest is None or item["age_seconds"] > oldest["age_seconds"]:
                        summary["oldest_unsuccessful_pending"] = {**item, "attempts": retry["attempts"]}
                if _held(root, raw):
                    summary["held"] += 1
                elif (root / commit_receipt_path(raw)).exists():
                    continue
                elif retry["attempts"] >= MAX_ATTEMPTS:
                    summary["exhausted"] += 1
                elif retry["next_attempt"] > now:
                    summary["retrying"] += 1
                else:
                    due.append(raw)
        except FileNotFoundError:
            continue  # A concurrent removal is reflected in the next scan.
        except (OSError, ValueError, KeyError, TypeError):
            summary["unreadable"].append(raw.name)
    return summary, due


class RawFileHandler(FileSystemEventHandler):
    """The observer only records events. The main loop is the sole consumer."""

    def __init__(self, project_root: Path, token: str, model_override: str | None) -> None:
        self.project_root = project_root
        self.token = token
        self.model_override = model_override
        self._pending: dict[str, float] = {}
        self._lock = threading.Lock()

    def on_created(self, event) -> None:
        if not event.is_directory:
            self._schedule(event.src_path)

    on_modified = on_created

    def on_moved(self, event) -> None:
        if not event.is_directory:
            self._schedule(event.dest_path)

    def _schedule(self, path: str) -> None:
        raw = Path(path)
        if raw.parent == self.project_root / "raw" and raw.suffix == ".md":
            with self._lock:
                self._pending[str(raw)] = time.monotonic() + DEBOUNCE_SECONDS

    def reconcile(self) -> None:
        summary, due = backlog(self.project_root)
        log.info("watcher_backlog %s", json.dumps(summary))
        with self._lock:
            for raw in due:
                self._pending.setdefault(str(raw), time.monotonic() + DEBOUNCE_SECONDS)

    def _process_pending(self) -> None:
        with self._lock:
            due = [Path(name) for name, at in self._pending.items() if at <= time.monotonic()]
            for raw in due:
                del self._pending[str(raw)]

        prioritized = []
        for raw in due:
            try:
                fm, _ = parse_frontmatter(raw, header_only=True)
                if fm.get("status") != "pending":
                    continue
                retry = _retry_record(self.project_root, raw)
                if not _due(self.project_root, raw, retry):
                    continue
                try:
                    route = classify_ingest_route(fm, model_override=self.model_override)
                except Exception:
                    _record_attempt(self.project_root, raw, retry["attempts"] + 1, "pending_after_attempt")
                    raise
                prioritized.append((route.priority, raw))
            except FileNotFoundError:
                continue
            except Exception as exc:
                log.exception("Failed to inspect %s", raw.name)
                notify_ingest_failure(raw, backend=_selected_backend(), detail=f"{type(exc).__name__}: {exc}")

        for _, raw in sorted(prioritized):
            try:
                retry = _retry_record(self.project_root, raw)
                if not _due(self.project_root, raw, retry):
                    continue
                attempts = retry["attempts"] + 1
                # Reserve only the source about to run. Queued work does not
                # consume an attempt if the worker restarts.
                _record_attempt(self.project_root, raw, attempts, "started")
                try:
                    ingest_raw_source(raw, self.project_root, self.token, self.model_override)
                finally:
                    fm, _ = parse_frontmatter(raw, header_only=True)
                    if fm.get("status") == "pending":
                        _record_attempt(self.project_root, raw, attempts, "pending_after_attempt")
                    else:
                        _retry_path(self.project_root, raw).unlink(missing_ok=True)
            except Exception as exc:
                log.exception("Failed to process %s", raw.name)
                notify_ingest_failure(raw, backend=_selected_backend(), detail=f"{type(exc).__name__}: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true", help="Print backlog and unconfirmed Git commits as JSON")
    parser.add_argument("--project-root", type=Path, default=os.environ.get("PROJECT_ROOT", "."))
    args = parser.parse_args()
    root = args.project_root.resolve()
    if args.status:
        print(json.dumps(backlog(root)[0], indent=2))
        return

    logging.basicConfig(
        level=logging.DEBUG if os.environ.get("LOG_LEVEL", "").upper() == "DEBUG" else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    backend = _selected_backend()
    token = os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    model = (
        os.environ.get("WIKI_INGEST_MODEL_OVERRIDE", "").strip()
        or os.environ.get("GITHUB_MODELS_MODEL_OVERRIDE", "").strip()
        or os.environ.get("CODEX_MODEL_OVERRIDE", "").strip()
        or None
    )
    if _backend_requires_token(backend) and not token:
        parser.error(f"GITHUB_MODELS_TOKEN/GITHUB_TOKEN is required for {backend}")
    if not (root / "raw").is_dir():
        parser.error(f"Missing raw directory under {root}")
    runtime = root / ".cache/wiki-watcher"
    runtime.mkdir(parents=True, exist_ok=True)
    with (runtime / "watcher.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another watcher owns this project root")

        handler = RawFileHandler(root, token, model)
        observer = Observer()
        observer.schedule(handler, str(root / "raw"), recursive=False)
        observer.start()
        next_scan = 0.0
        try:
            while observer.is_alive():
                if time.monotonic() >= next_scan:
                    handler.reconcile()
                    next_scan = time.monotonic() + RECONCILE_SECONDS
                handler._process_pending()
                observer.join(timeout=POLL_INTERVAL)
            raise RuntimeError("Raw file observer stopped unexpectedly")
        except KeyboardInterrupt:
            log.info("Shutting down watcher")
        finally:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    main()
