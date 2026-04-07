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
echo "Root: $ROOT_DIR"
echo ""

# 1. Create .opencode/skills symlink
OPENCODE_DIR="$ROOT_DIR/.opencode"
SKILLS_LINK="$OPENCODE_DIR/skills"
GITHUB_SKILLS="$ROOT_DIR/.github/skills"

if [ -d "$GITHUB_SKILLS" ]; then
    mkdir -p "$OPENCODE_DIR"
    if [ -L "$SKILLS_LINK" ]; then
        echo "✅ .opencode/skills/ symlink already exists"
    elif [ -d "$SKILLS_LINK" ]; then
        echo "⚠️  .opencode/skills/ is a directory, not a symlink. Skipping."
    else
        ln -s "../.github/skills" "$SKILLS_LINK"
        echo "✅ Created .opencode/skills/ → .github/skills/"
    fi
else
    echo "❌ .github/skills/ not found. Run scaffold.py first."
fi

echo ""

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
for dir in raw raw/assets wiki/sources wiki/concepts wiki/entities wiki/synthesis agents templates scripts docs .github/instructions .github/agents .github/prompts; do
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
for file in AGENTS.md README.md .github/copilot-instructions.md opencode.json; do
    if [ -s "$ROOT_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file missing or empty"
    fi
done

echo ""

# 5. Check skills
SKILL_COUNT=$(find "$ROOT_DIR/.github/skills" -name 'SKILL.md' 2>/dev/null | wc -l)
echo "✅ Found $SKILL_COUNT skills in .github/skills/"

# 6. Check custom agents
AGENT_COUNT=$(find "$ROOT_DIR/.github/agents" -name '*.agent.md' 2>/dev/null | wc -l)
echo "✅ Found $AGENT_COUNT custom agents in .github/agents/"

# 7. Check instructions
INSTRUCTION_COUNT=$(find "$ROOT_DIR/.github/instructions" -name '*.instructions.md' 2>/dev/null | wc -l)
echo "✅ Found $INSTRUCTION_COUNT scoped instructions in .github/instructions/"

# 8. Check prompt files
PROMPT_COUNT=$(find "$ROOT_DIR/.github/prompts" -name '*.prompt.md' 2>/dev/null | wc -l)
echo "✅ Found $PROMPT_COUNT prompt files in .github/prompts/"

echo ""
echo "=== Setup complete ==="
