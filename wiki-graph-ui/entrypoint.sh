#!/bin/sh
# Rewrite the placeholder with the runtime PUBLIC_API_URL before nginx starts.
# Also stamp a per-container BUILD_ID into ?v= cache-bust placeholders so each
# rebuild forces fresh fetches from CDNs (Cloudflare in particular ignores
# origin Cache-Control on .js/.css under "Cache Everything", so a unique URL
# is the only reliable bust).
set -eu

: "${PUBLIC_API_URL:=}"

CONFIG_FILE=/usr/share/nginx/html/config.js
if [ -f "$CONFIG_FILE" ]; then
    # Escape slashes in the replacement.
    ESC=$(printf '%s' "$PUBLIC_API_URL" | sed -e 's/[\/&]/\\&/g')
    sed -i "s/__API_BASE__/${ESC}/g" "$CONFIG_FILE"
fi

# Use the container's start-time as the build id. Recreating the container
# (the standard deploy step) yields a new id and a new asset URL.
BUILD_ID=$(date +%s)
find /usr/share/nginx/html -type f \( -name '*.html' -o -name '*.js' -o -name '*.css' \) \
    -exec sed -i "s/__BUILD_ID__/${BUILD_ID}/g" {} +

exec nginx -g 'daemon off;'
