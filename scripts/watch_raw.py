#!/usr/bin/env python3
"""
File watcher for labs-wiki raw/ directory.

Uses watchdog to detect new .md files, debounces writes, and triggers
auto_ingest.py for each new pending source.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from pathlib import Path

from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from auto_ingest import ingest_raw_source, parse_frontmatter, process_all_pending

log = logging.getLogger("watch-raw")

DEBOUNCE_SECONDS = float(os.environ.get("DEBOUNCE_SECONDS", "5"))
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", "1"))


class RawFileHandler(FileSystemEventHandler):
    """Handle new .md files in the raw/ directory."""

    def __init__(self, project_root: Path, token: str, model: str) -> None:
        super().__init__()
        self.project_root = project_root
        self.token = token
        self.model = model
        self._pending: dict[str, float] = {}
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        self._schedule(event.src_path)

    def on_modified(self, event: FileModifiedEvent) -> None:
        if event.is_directory:
            return
        self._schedule(event.src_path)

    def _schedule(self, path: str) -> None:
        """Debounce: wait for file writes to settle before processing."""
        if not path.endswith(".md"):
            return
        # Ignore files in subdirectories (e.g., raw/assets/)
        raw_dir = str(self.project_root / "raw")
        if os.path.dirname(path) != raw_dir:
            return

        with self._lock:
            self._pending[path] = time.time()
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(DEBOUNCE_SECONDS, self._process_pending)
            self._timer.start()

    def _process_pending(self) -> None:
        """Process all debounced files."""
        with self._lock:
            to_process = dict(self._pending)
            self._pending.clear()

        for path_str in sorted(to_process):
            raw_path = Path(path_str)
            if not raw_path.exists():
                continue

            try:
                fm, _ = parse_frontmatter(raw_path)
                if fm.get("status") != "pending":
                    log.debug("Skipping %s (status: %s)", raw_path.name, fm.get("status"))
                    continue

                log.info("New pending source detected: %s", raw_path.name)
                ingest_raw_source(raw_path, self.project_root, self.token, self.model)
            except Exception:
                log.exception("Failed to process %s", raw_path.name)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG if os.environ.get("LOG_LEVEL", "").upper() == "DEBUG" else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    project_root = Path(os.environ.get("PROJECT_ROOT", ".")).resolve()
    token = os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    model = os.environ.get("GITHUB_MODELS_MODEL", "gpt-4o")

    if not token:
        log.error("No API token. Set GITHUB_MODELS_TOKEN env var.")
        sys.exit(1)

    raw_dir = project_root / "raw"
    if not raw_dir.exists():
        log.error("raw/ directory not found at %s", raw_dir)
        sys.exit(1)

    # Process any existing pending sources on startup
    log.info("Checking for existing pending sources...")
    count = process_all_pending(project_root, token, model)
    if count:
        log.info("Processed %d existing pending source(s)", count)

    # Start watching
    handler = RawFileHandler(project_root, token, model)
    observer = Observer()
    observer.schedule(handler, str(raw_dir), recursive=False)
    observer.start()

    log.info("👀 Watching %s for new sources (debounce: %ss)", raw_dir, DEBOUNCE_SECONDS)

    try:
        while observer.is_alive():
            observer.join(timeout=POLL_INTERVAL)
    except KeyboardInterrupt:
        log.info("Shutting down...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
