---
applyTo: "wiki-ingest-api/**"
---
# Wiki Ingest API Standards

The `wiki-ingest-api/` is a FastAPI capture service that receives sources from multiple channels and writes them to `raw/`.

## Architecture

- FastAPI application with Docker deployment
- Receives content via POST endpoints
- Writes raw markdown files to `raw/` with proper frontmatter
- Binary files go to `raw/assets/`
- Token-based authentication

## Endpoint Conventions

- POST `/ingest` — Accept URL, text, note, or file sources
- POST `/ingest/file` — Accept binary file uploads
- GET `/health` — Health check
- All endpoints return JSON with `status`, `message`, and `filename` fields
- Use HTTP 201 for successful ingestion, 400 for validation errors, 401 for auth failures

## Source Channels

| Channel | Source field value |
|---------|-------------------|
| iOS/Android share sheet | `ios-share` / `android-share` |
| Browser bookmarklet | `browser` |
| Terminal (`wa`/`waf`) | `terminal` |
| GitHub Issue | `github-issue` |
| ntfy message | `ntfy` |

## File Generation

- Generated filenames: `YYYY-MM-DD-<slug>.md`
- Slug derived from title or URL domain
- Always set `status: pending` in frontmatter
- Compute `content_hash` as SHA-256 of the body content
