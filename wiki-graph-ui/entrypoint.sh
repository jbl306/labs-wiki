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

exec nginx -g 'daemon off;'
