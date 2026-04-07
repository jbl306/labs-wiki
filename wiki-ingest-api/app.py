"""Wiki Ingest API — FastAPI service for capturing sources to raw/."""

import hashlib
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="Wiki Ingest API", version="1.0.0")

RAW_DIR = Path(os.getenv("RAW_DIR", "/app/raw"))
ASSETS_DIR = RAW_DIR / "assets"
API_TOKEN = os.getenv("WIKI_API_TOKEN", "")
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


class IngestRequest(BaseModel):
    type: str  # url | text | note
    content: str
    title: str | None = None
    tags: list[str] = []
    source: str = "api"


class IngestResponse(BaseModel):
    status: str
    path: str


def verify_token(authorization: str | None = Header(None)) -> None:
    """Verify Bearer token authentication."""
    if not API_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    token = authorization.removeprefix("Bearer ").strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug[:60] if slug else "untitled"


def generate_raw_path(title: str) -> Path:
    """Generate a timestamped raw source file path."""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = slugify(title)
    return RAW_DIR / f"{date_str}-{slug}.md"


def write_raw_source(
    path: Path,
    title: str,
    source_type: str,
    content: str,
    source_channel: str,
    tags: list[str],
    url: str | None = None,
) -> None:
    """Write a raw source file with standardized frontmatter."""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    captured = datetime.now(timezone.utc).isoformat()
    tags_str = ", ".join(tags)

    frontmatter = f"""---
title: "{title}"
type: {source_type}
captured: {captured}
source: {source_channel}
"""
    if url:
        frontmatter += f'url: "{url}"\n'

    frontmatter += f"""content_hash: "sha256:{content_hash}"
tags: [{tags_str}]
status: pending
---
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter + "\n" + content + "\n")


async def notify(title: str) -> None:
    """Send ntfy notification about captured source."""
    if not NTFY_TOPIC:
        return
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{NTFY_SERVER}/{NTFY_TOPIC}",
                content=f"📥 New source captured: {title}",
                headers={"Title": "Wiki Ingest"},
                timeout=5.0,
            )
    except Exception:
        pass  # Don't fail ingest if notification fails


def sanitize_filename(filename: str) -> str:
    """Sanitize uploaded filename to prevent path traversal."""
    name = Path(filename).name
    name = re.sub(r"[^\w\s\-.]", "", name)
    if not name or name.startswith("."):
        name = f"upload-{uuid.uuid4().hex[:8]}"
    return name


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_json(
    request: IngestRequest,
    authorization: str | None = Header(None),
) -> IngestResponse:
    """Ingest a text, URL, or note source."""
    verify_token(authorization)

    if request.type not in ("url", "text", "note"):
        raise HTTPException(status_code=400, detail="type must be: url, text, or note")

    if not request.content:
        raise HTTPException(status_code=400, detail="content is required")

    title = request.title or request.content[:80]
    path = generate_raw_path(title)

    # Avoid overwriting existing files
    counter = 1
    original_path = path
    while path.exists():
        path = original_path.with_stem(f"{original_path.stem}-{counter}")
        counter += 1

    url = request.content if request.type == "url" else None
    write_raw_source(
        path=path,
        title=title,
        source_type=request.type,
        content=request.content,
        source_channel=request.source,
        tags=request.tags,
        url=url,
    )

    await notify(title)

    return IngestResponse(status="ok", path=str(path.relative_to(RAW_DIR.parent)))


@app.post("/api/ingest/file", response_model=IngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    title: str = Form(""),
    tags: str = Form(""),
    source: str = Form("api"),
    authorization: str | None = Header(None),
) -> IngestResponse:
    """Ingest a file upload (image, PDF, etc.)."""
    verify_token(authorization)

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")

    safe_name = sanitize_filename(file.filename or "upload")
    ext = Path(safe_name).suffix or ".bin"
    asset_name = f"{uuid.uuid4().hex[:12]}{ext}"

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    asset_path = ASSETS_DIR / asset_name
    asset_path.write_bytes(content)

    file_title = title or safe_name
    raw_path = generate_raw_path(file_title)

    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    write_raw_source(
        path=raw_path,
        title=file_title,
        source_type="file",
        content=f"See `raw/assets/{asset_name}`\n\nOriginal filename: {safe_name}",
        source_channel=source,
        tags=tag_list,
    )

    await notify(file_title)

    return IngestResponse(status="ok", path=str(raw_path.relative_to(RAW_DIR.parent)))
