#!/bin/sh
# Rewrite the placeholder with the runtime PUBLIC_API_URL before nginx starts.
set -eu

: "${PUBLIC_API_URL:=}"

CONFIG_FILE=/usr/share/nginx/html/config.js
if [ -f "$CONFIG_FILE" ]; then
    # Escape slashes in the replacement.
    ESC=$(printf '%s' "$PUBLIC_API_URL" | sed -e 's/[\/&]/\\&/g')
    sed -i "s/__API_BASE__/${ESC}/g" "$CONFIG_FILE"
fi

# Per-deploy cache-bust: stamp BUILD_ID into ?v= query strings on every
# html/js/css asset so Cloudflare's edge cache (which ignores origin
# Cache-Control on static assets) sees a fresh URL each rebuild.
BUILD_ID=$(date +%s)
find /usr/share/nginx/html -type f \( -name '*.html' -o -name '*.js' -o -name '*.css' \) \
    -exec sed -i "s/__BUILD_ID__/${BUILD_ID}/g" {} +

exec nginx -g 'daemon off;'
