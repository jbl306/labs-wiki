#!/usr/bin/env bash
set -euo pipefail

# ntfy → Wiki Ingest API bridge
# Subscribes to an ntfy topic and forwards messages to the ingest API.
#
# Usage:
#   WIKI_API_URL=https://wiki-api.internal WIKI_API_TOKEN=xxx NTFY_TOPIC=wiki-capture ./ntfy-wiki-watcher.sh
#
# Messages should be plain text (captured as type: note) or URLs (captured as type: url).

WIKI_API_URL="${WIKI_API_URL:-http://localhost:8000}"
WIKI_API_TOKEN="${WIKI_API_TOKEN:?WIKI_API_TOKEN is required}"
NTFY_TOPIC="${NTFY_TOPIC:?NTFY_TOPIC is required}"
NTFY_SERVER="${NTFY_SERVER:-https://ntfy.sh}"

echo "🔔 Watching ntfy topic: ${NTFY_TOPIC}"
echo "📡 Forwarding to: ${WIKI_API_URL}/api/ingest"

curl -s "${NTFY_SERVER}/${NTFY_TOPIC}/raw" | while read -r message; do
    [ -z "$message" ] && continue

    # Detect if the message is a URL
    if echo "$message" | grep -qE '^https?://'; then
        TYPE="url"
    else
        TYPE="note"
    fi

    echo "📥 Captured (${TYPE}): ${message:0:80}"

    curl -s -X POST "${WIKI_API_URL}/api/ingest" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${WIKI_API_TOKEN}" \
        -d "$(printf '{"type":"%s","content":"%s","source":"ntfy"}' "$TYPE" "$message")" \
        | head -c 200
    echo ""
done
