#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# If setup.sh is at repo root, SCRIPT_DIR is the root
# If it were inside scripts/, we'd go up one level
if [ -f "$SCRIPT_DIR/AGENTS.md" ]; then
    ROOT_DIR="$SCRIPT_DIR"
else
    ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

echo "=== labs-wiki setup ==="
echo "Shared workflow and testing policy: /home/jbl/.codex/AGENTS.md"

# 2. Validate Python
if command -v python3 &> /dev/null; then
    echo "✅ python3 found: $(python3 --version)"
else
    echo "❌ python3 not found"
fi

echo ""

# 3. Validate structure
echo "Checking directory structure..."
DIRS_OK=true
for dir in raw raw/assets wiki/sources wiki/concepts wiki/entities wiki/synthesis agents templates scripts docs; do
    if [ -d "$ROOT_DIR/$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ $dir/ missing"
        DIRS_OK=false
    fi
done

echo ""

# 4. Validate key files
echo "Checking key files..."
for file in AGENTS.md README.md; do
    if [ -s "$ROOT_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file missing or empty"
    fi
done

echo ""

# Domain personas are local; personal skills are loaded on demand.
AGENT_COUNT=$(find "$ROOT_DIR/agents" -name '*.agent.md' | wc -l)
echo "Domain personas in agents/: $AGENT_COUNT"

if [ "$DIRS_OK" != true ]; then
    exit 1
fi
echo "=== Setup complete ==="
