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

# ----------------------------------------------------------------------------
# Subcommand: inject the canonical AGENTS.md snippet into every sibling project.
# Idempotent. Edits existing AGENTS.md between the LABS-WIKI-SNIPPET markers, or
# appends the snippet if no markers are present.
# ----------------------------------------------------------------------------
inject_snippet() {
    local snippet_file="$ROOT_DIR/docs/agents-snippet.md"
    if [ ! -f "$snippet_file" ]; then
        echo "❌ $snippet_file not found"
        return 1
    fi

    # Extract just the content between START/END markers
    local tmp
    tmp=$(mktemp)
    awk '
        /<!-- LABS-WIKI-SNIPPET-START -->/ {flag=1}
        flag {print}
        /<!-- LABS-WIKI-SNIPPET-END -->/   {flag=0}
    ' "$snippet_file" > "$tmp"

    if [ ! -s "$tmp" ]; then
        echo "❌ snippet markers not found in $snippet_file"
        rm -f "$tmp"
        return 1
    fi

    local projects_root
    projects_root="$(cd "$ROOT_DIR/.." && pwd)"
    local count=0
    for proj_agents in "$projects_root"/*/AGENTS.md; do
        [ -f "$proj_agents" ] || continue
        # Skip labs-wiki itself
        case "$proj_agents" in *"labs-wiki/AGENTS.md") continue ;; esac

        if grep -q '<!-- LABS-WIKI-SNIPPET-START -->' "$proj_agents"; then
            # Replace existing block
            python3 - "$proj_agents" "$tmp" <<'PY'
import sys, re, pathlib
target = pathlib.Path(sys.argv[1])
snippet = pathlib.Path(sys.argv[2]).read_text()
content = target.read_text()
pattern = re.compile(
    r"<!-- LABS-WIKI-SNIPPET-START -->.*?<!-- LABS-WIKI-SNIPPET-END -->",
    re.DOTALL,
)
new = pattern.sub(snippet.strip(), content, count=1)
if new != content:
    target.write_text(new)
PY
            echo "  ♻️  updated $proj_agents"
        else
            {
                echo ""
                cat "$tmp"
                echo ""
            } >> "$proj_agents"
            echo "  ➕ appended to $proj_agents"
        fi
        count=$((count + 1))
    done
    rm -f "$tmp"
    echo "=== snippet injected into $count project(s) ==="
}

case "${1:-}" in
    --inject-snippet)
        inject_snippet
        exit $?
        ;;
esac

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
