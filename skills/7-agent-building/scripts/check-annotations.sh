#!/bin/bash
# check-annotations.sh — Check NL2SQL schema annotations for a DevRev data table.
#
# Usage: ./scripts/check-annotations.sh <table-id> [output_dir]
#
# Requires:
#   DEVREV_PAT — DevRev personal access token (used by devrev.py)
#
# What this does:
#   1. Clones devrev/auto-annotations (if not already present) and sets up devrev.py
#   2. Runs `devrev.py table-schema` to fetch the current schema + any existing descriptions
#   3. Checks annotation quality (missing, placeholder, no examples)
#   4. If annotations are broken: prints the SKILL.md workflow for the AI agent to follow
#
# Note: Annotation GENERATION is an AI-agent workflow (6 phases). This script handles
# detection and setup only. After running this, have the agent follow the SKILL.md.

set -euo pipefail

TABLE_ID="${1:-}"
OUTPUT_DIR="${2:-/tmp/devrev-annotations}"
mkdir -p "$OUTPUT_DIR"

# ── Load DEVREV_PAT ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

load_pat() {
  local name="$1"
  if [ -n "$(eval echo \${$name:-})" ]; then
    return 0
  fi
  for f in "$(pwd)/.env" "$PROJECT_ROOT/.env" "$HOME/.openclaw-autoclaw/.env"; do
    if [ -f "$f" ]; then
      val=$(grep "^${name}=" "$f" | head -1 | cut -d'=' -f2-)
      if [ -n "$val" ]; then
        eval "$name=\$val"
        return 0
      fi
    fi
  done
  return 1
}

if ! load_pat DEVREV_PAT; then
  echo "ERROR: DEVREV_PAT not found." >&2
  echo "  Add DEVREV_PAT=your-token to .env (DevRev → Settings → Tokens)" >&2
  exit 1
fi

export DEVREV_PAT

if [ -z "$TABLE_ID" ]; then
  echo "Usage: ./scripts/check-annotations.sh <table-id> [output_dir]" >&2
  echo "" >&2
  echo "To list available tables, run:" >&2
  echo "  ./scripts/check-annotations.sh list" >&2
  exit 1
fi

# ── Step 1: Clone / update devrev/auto-annotations ──
AUTO_ANNOTATIONS_DIR="$OUTPUT_DIR/auto-annotations"

if [ -d "$AUTO_ANNOTATIONS_DIR/.git" ]; then
  echo "♻️  Updating devrev/auto-annotations..." >&2
  git -C "$AUTO_ANNOTATIONS_DIR" pull --quiet 2>&1 | sed 's/^/  /' >&2
else
  echo "📦 Cloning devrev/auto-annotations..." >&2
  git clone https://github.com/devrev/auto-annotations "$AUTO_ANNOTATIONS_DIR" 2>&1 | sed 's/^/  /' >&2
fi

DEVREV_PY="$AUTO_ANNOTATIONS_DIR/devrev.py"
SKILL_MD="$AUTO_ANNOTATIONS_DIR/SKILL.md"

if [ ! -f "$DEVREV_PY" ]; then
  echo "ERROR: devrev.py not found after clone. Check the repo." >&2
  exit 1
fi
chmod +x "$DEVREV_PY"

# ── Step 2: List tables (if requested) ──
if [ "$TABLE_ID" = "list" ]; then
  echo "📋 Available data tables:" >&2
  "$DEVREV_PY" tables-list
  exit 0
fi

# ── Step 3: Fetch table schema ──
echo "" >&2
echo "🔍 Fetching schema for table: $TABLE_ID" >&2

SCHEMA_OUTPUT=$("$DEVREV_PY" table-schema "$TABLE_ID" 2>&1) || {
  echo "ERROR: Could not fetch schema for table '$TABLE_ID'." >&2
  echo "       Run './scripts/check-annotations.sh list' to see valid table IDs." >&2
  echo "       Raw output: $SCHEMA_OUTPUT" >&2
  exit 1
}

echo "$SCHEMA_OUTPUT" > "$OUTPUT_DIR/schema-raw.txt"

# ── Step 4: Parse annotation quality ──
# Count columns and descriptions from the schema output.
# devrev.py table-schema returns JSON — parse description fields.
TOTAL_COLS=$(echo "$SCHEMA_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
cols = data.get('fields', data.get('columns', data.get('schema', {}).get('fields', [])))
print(len(cols))
" 2>/dev/null || echo "0")

ANNOTATED=$(echo "$SCHEMA_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
cols = data.get('fields', data.get('columns', data.get('schema', {}).get('fields', [])))
count = sum(1 for c in cols if c.get('description','').strip() and len(c.get('description','').strip()) >= 20)
print(count)
" 2>/dev/null || echo "0")

PLACEHOLDER=$(echo "$SCHEMA_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
cols = data.get('fields', data.get('columns', data.get('schema', {}).get('fields', [])))
count = sum(1 for c in cols if 0 < len(c.get('description','').strip()) < 20)
print(count)
" 2>/dev/null || echo "0")

UNANNOTATED=$((TOTAL_COLS - ANNOTATED - PLACEHOLDER))

echo "" >&2
echo "📊 Annotation status for: $TABLE_ID" >&2
echo "  Total columns:       $TOTAL_COLS" >&2
echo "  Well-annotated:      $ANNOTATED  (description ≥20 chars)" >&2
echo "  Placeholder/broken:  $PLACEHOLDER  (description <20 chars — too short for NL2SQL)" >&2
echo "  No annotation:       $UNANNOTATED" >&2

# Save summary
cat > "$OUTPUT_DIR/annotation-check.json" <<EOF
{
  "table_id": "$TABLE_ID",
  "total_columns": $TOTAL_COLS,
  "well_annotated": $ANNOTATED,
  "placeholder_broken": $PLACEHOLDER,
  "unannotated": $UNANNOTATED,
  "needs_annotation": $([ "$((UNANNOTATED + PLACEHOLDER))" -gt 0 ] && echo "true" || echo "false")
}
EOF

# ── Step 5: Result ──
NEEDS_FIX=$((UNANNOTATED + PLACEHOLDER))

if [ "$NEEDS_FIX" -eq 0 ] && [ "$ANNOTATED" -eq "$TOTAL_COLS" ]; then
  echo "" >&2
  echo "✅ All $TOTAL_COLS columns are well-annotated. NL2SQL should work correctly." >&2
  echo "   Schema saved to: $OUTPUT_DIR/schema-raw.txt" >&2
  exit 0
fi

# ── Step 6: Annotations needed — print agent instructions ──
echo "" >&2
echo "⚠️  $NEEDS_FIX column(s) need annotation before NL2SQL will work reliably." >&2
echo "" >&2
echo "════════════════════════════════════════════════════════════" >&2
echo "  ACTION REQUIRED: Run the auto-annotations agent workflow" >&2
echo "════════════════════════════════════════════════════════════" >&2
echo "" >&2
echo "The devrev/auto-annotations tool uses a 6-phase AI-agent workflow." >&2
echo "It cannot be run as a simple CLI command — it requires an agent." >&2
echo "" >&2
echo "Setup (already done):" >&2
echo "  ✅ Repo cloned:    $AUTO_ANNOTATIONS_DIR" >&2
echo "  ✅ devrev.py:      $DEVREV_PY" >&2
echo "  ✅ DEVREV_PAT:     set" >&2
echo "  ✅ SKILL.md:       $SKILL_MD" >&2
echo "" >&2
echo "To run the annotation workflow:" >&2
echo "  1. Read the SKILL.md:  cat '$SKILL_MD'" >&2
echo "  2. Follow the 6-phase workflow with devrev.py in $AUTO_ANNOTATIONS_DIR" >&2
echo "  3. Output will be written to: {table}_field_descriptions.json" >&2
echo "  4. Apply generated descriptions via Agent Studio → Knowledge → Datasets → Edit Schema" >&2
echo "" >&2
echo "Or tell the AI agent:" >&2
echo "  'Run the devrev/auto-annotations SKILL.md workflow for table $TABLE_ID'" >&2
echo "   using devrev.py at $DEVREV_PY'" >&2
echo "" >&2
echo "📁 Output: $OUTPUT_DIR/" >&2
echo "  - schema-raw.txt         (full table schema)" >&2
echo "  - annotation-check.json  (annotation quality summary)" >&2
