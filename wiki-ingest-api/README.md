# Wiki Ingest API

FastAPI service for capturing sources into `raw/` from any device.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check |
| `POST` | `/api/ingest` | JSON body: text, URL, or note |
| `POST` | `/api/ingest/file` | Multipart: file upload |

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
