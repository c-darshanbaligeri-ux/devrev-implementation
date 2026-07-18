#!/bin/bash
# sync-knowledge.sh — Fetch all AI Agent Guide articles from DevRev KB
# Usage: ./sync-knowledge.sh [output_dir]
# Default output_dir: ./knowledge (relative to current working directory)
#
# Requires DEVREV_PAT (environment, ~/.openclaw-autoclaw/.env, or plugin/.env)

set -euo pipefail

OUTPUT_DIR="${1:-knowledge}"
mkdir -p "$OUTPUT_DIR"

# Load PATs (check project-local .env first, then ~/.openclaw-autoclaw/.env)
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
  echo "ERROR: DEVREV_PAT not found."
  echo "  Copy .env.example to .env and fill in your tokens:"
  echo "    cp .env.example .env"
  exit 1
fi

API="https://api.devrev.ai"
DIRECTORY_ID="don:core:dvrv-us-1:devo/0:directory/257"

echo "🔍 Fetching articles from AI Agent Guides directory..."

# Step 1: List all articles in the directory
ARTICLES=$(curl -s -X POST "$API/articles.list" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"parent\": [\"$DIRECTORY_ID\"], \"limit\": 100}" | jq -r '.articles[].id')

if [ -z "$ARTICLES" ] || [ "$ARTICLES" = "null" ]; then
  echo "ERROR: No articles found in directory."
  exit 1
fi

COUNT=0
for ARTICLE_ID in $ARTICLES; do
  # Get article metadata
  META=$(curl -s -X POST "$API/articles.get" \
    -H "Authorization: $DEVREV_PAT" \
    -H "Content-Type: application/json" \
    -d "{\"id\": \"$ARTICLE_ID\"}")

  DISPLAY_ID=$(echo "$META" | jq -r '.article.display_id')
  TITLE=$(echo "$META" | jq -r '.article.title')
  EXTRACTED_ARTIFACT=$(echo "$META" | jq -r '.article.extracted_content[0].id // empty')

  # Get extracted content (plain text)
  if [ -n "$EXTRACTED_ARTIFACT" ]; then
    DOWNLOAD_URL=$(curl -s -o /dev/null -w "%{redirect_url}" \
      "$API/artifacts.download?id=$EXTRACTED_ARTIFACT" \
      -H "Authorization: $DEVREV_PAT")
    curl -sL "$DOWNLOAD_URL" -o "$OUTPUT_DIR/$DISPLAY_ID.txt" 2>/dev/null
  fi

  # Get resource artifact (rich text) — used as fallback
  RESOURCE_ARTIFACT=$(echo "$META" | jq -r '.article.resource.artifacts[0].id // empty')
  if [ -n "$RESOURCE_ARTIFACT" ] && [ ! -s "$OUTPUT_DIR/$DISPLAY_ID.txt" ]; then
    DOWNLOAD_URL=$(curl -s -o /dev/null -w "%{redirect_url}" \
      "$API/artifacts.download?id=$RESOURCE_ARTIFACT" \
      -H "Authorization: $DEVREV_PAT")
    curl -sL "$DOWNLOAD_URL" -o "$OUTPUT_DIR/$DISPLAY_ID.txt" 2>/dev/null
  fi

  # Create a metadata sidecar
  echo "$META" | jq '{display_id: .article.display_id, title: .article.title, type: .article.article_type, status: .article.status, parent: .article.parent.display_id, tags: [(.article.tags // [])[] | .tag.name?]}' > "$OUTPUT_DIR/$DISPLAY_ID.meta.json"

  COUNT=$((COUNT + 1))
  printf "  ✅ %s — %s\n" "$DISPLAY_ID" "$TITLE"
  sleep 0.15
done

echo ""
echo "📚 Synced $COUNT articles to $OUTPUT_DIR/"
echo ""
echo "Article index:"
for f in "$OUTPUT_DIR"/*.meta.json; do
  [ -f "$f" ] || continue
  DID=$(jq -r '.display_id' "$f")
  TITLE=$(jq -r '.title' "$f")
  printf "  %-12s %s\n" "$DID" "$TITLE"
done

# Write an index file
echo "# AI Agent Guide — Knowledge Base Index" > "$OUTPUT_DIR/INDEX.md"
echo "" >> "$OUTPUT_DIR/INDEX.md"
echo "Synced: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUTPUT_DIR/INDEX.md"
echo "" >> "$OUTPUT_DIR/INDEX.md"
echo "## Articles" >> "$OUTPUT_DIR/INDEX.md"
for f in "$OUTPUT_DIR"/*.meta.json; do
  [ -f "$f" ] || continue
  DID=$(jq -r '.display_id' "$f")
  TITLE=$(jq -r '.title' "$f")
  echo "- **$DID** — $TITLE" >> "$OUTPUT_DIR/INDEX.md"
done
