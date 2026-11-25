"""Capture one GitHub issue event using a stable, repository-local filename."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def capture_issue(event: dict, raw_dir: Path) -> Path:
    if event.get("action") != "labeled" or event["label"]["name"] != "ingest":
        raise ValueError("expected the ingest label")
    issue = event["issue"]
    number = issue["number"]
    if type(number) is not int or number < 1:
        raise ValueError("invalid issue number")
    created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    day = created.astimezone(timezone.utc).date()
    path = raw_dir / f"{day}-github-issue-{number}.md"
    # JSON strings are valid double-quoted YAML scalars, including embedded
    # quotes and line breaks. Only trusted keys and types enter the header.
    fields = {
        "title": issue["title"],
        "type": "note",
        "captured": issue["updated_at"],
        "source": "github-issue",
        "issue_number": number,
        "tags": [],
        "status": "pending",
    }
    header = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in fields.items())
    text = f"---\n{header}\n---\n\n{issue['body'] or ''}\n"
    try:
        with path.open("x", encoding="utf-8") as capture:
            capture.write(text)
    except FileExistsError:
        # The watcher may already have updated the captured raw's status.
        if path.is_symlink():
            raise ValueError(f"capture path is a symbolic link: {path}") from None
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            raise ValueError(f"unrecognized file at {path}") from None
        metadata = lines[1:lines.index("---", 1)]
        if 'source: "github-issue"' not in metadata or f"issue_number: {number}" not in metadata:
            raise ValueError(f"existing capture has a different owner: {path}") from None
    return path


if __name__ == "__main__":
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    print(capture_issue(event, Path("raw")))
