# Wiki Ingest API

FastAPI service for capturing sources into `raw/` from any device. File uploads
land in `raw/assets/`, and the auto-ingest service converts supported document
formats (for example PDF, DOCX, PPTX, XLSX/XLS, and EPUB) to markdown before
wiki compilation, persisting that extraction back into the corresponding raw
source.

## Endpoints

| Method | Path | Content-Type | Purpose |
|--------|------|-------------|---------|
| `GET` | `/health` | — | Health check |
| `POST` | `/api/ingest` | `application/json` | JSON body: text, URL, or note |
| `POST` | `/api/ingest/form` | `application/x-www-form-urlencoded` | Form fields: same as above (for Android/HTTP Shortcuts) |
| `POST` | `/api/ingest/file` | `multipart/form-data` | File upload |
| `GET`, `POST`, `PUT` | `/api/debug` | Any | Authenticated method and body-length diagnostics |

## Authentication

Set `WIKI_API_TOKEN` environment variable. Send it as
`Authorization: Bearer <token>`. Capture endpoints fail closed with
`503 Service Unavailable` when the server token is unset.

All capture endpoints are non-idempotent. Repeating an accepted request creates
a new raw source with a numeric filename suffix. File uploads preserve both raw
records and their separate assets; concurrent captures cannot overwrite an
existing raw record.
Clients should not automatically retry an ambiguous timeout without accepting
that a duplicate may be created.

The debug endpoint requires the same bearer token and returns only the request
method and body length. Application diagnostics omit request bodies, query
values, and headers.

URL capture is an operator-trusted capability because the downstream ingest
pipeline may fetch the submitted URL. Do not expose it to untrusted callers.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WIKI_API_TOKEN` | Yes | — | Bearer token for auth |
| `RAW_DIR` | No | `/app/raw` | Path to raw/ directory |
| `NTFY_SERVER` | No | `https://ntfy.sh` | ntfy server URL |
| `NTFY_TOPIC` | No | — | ntfy topic for notifications |

## Local Development

```bash
cd wiki-ingest-api
pip install -r requirements.txt
WIKI_API_TOKEN=dev RAW_DIR=../raw uvicorn app:app --reload --port 8000
```
