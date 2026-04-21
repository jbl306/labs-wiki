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

## Authentication

Set `WIKI_API_TOKEN` environment variable. Send as `Authorization: Bearer <token>`.

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
