#!/bin/bash
# update-article.sh — Update a DevRev KB article via API
# Usage: ./update-article.sh <article-display-id> <content-file> [--title "New Title"] [--publish]
#
# Updates an article's content artifact and optionally its title and status.
#
# Workflow:
#   1. Read the article metadata (get current content artifact)
#   2. Prepare a new artifact upload (staged content)
#   3. Upload the file content to the staged URL
#   4. Validate the staged content
#   5. Create a new artifact from the staged content
#   6. Update the article with the new artifact (and optionally title/status)
#
# Requires DEVREV_PAT env var (reads from ~/.openclaw-autoclaw/.env or env)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

load_pat() {
  local name="$1"
  if [ -n "$(eval echo \${$name:-})" ]; then
    return 0
  fi
  for f in "$PROJECT_ROOT/.env" "$HOME/.openclaw-autoclaw/.env"; do
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

if [ $# -lt 2 ]; then
  echo "Usage: $0 <article-display-id> <content-file> [--title \"New Title\"] [--publish] [--dry-run]"
  echo ""
  echo "Options:"
  echo "  --title     Update the article title"
  echo "  --publish   Set article status to published"
  echo "  --dry-run   Show what would be updated without making changes"
  exit 1
fi

ARTICLE_DID="$1"
CONTENT_FILE="$2"
shift 2

TITLE=""
PUBLISH=false
DRY_RUN=false

while [ $# -gt 0 ]; do
  case "$1" in
    --title) TITLE="$2"; shift 2 ;;
    --publish) PUBLISH=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ ! -f "$CONTENT_FILE" ]; then
  echo "ERROR: Content file not found: $CONTENT_FILE"
  exit 1
fi

API="https://api.devrev.ai"
FILE_NAME="$(basename "$CONTENT_FILE")"

echo "📋 Article: $ARTICLE_DID"
echo "📄 Content: $CONTENT_FILE ($FILE_NAME)"

# Step 1: Get current article metadata
echo ""
echo "Step 1: Fetching article metadata..."
ARTICLE_META=$(curl -s -X POST "$API/articles.get" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$ARTICLE_DID\"}")

ARTICLE_ID=$(echo "$ARTICLE_META" | jq -r '.article.id // empty')
CURRENT_TITLE=$(echo "$ARTICLE_META" | jq -r '.article.title // empty')
CURRENT_STATUS=$(echo "$ARTICLE_META" | jq -r '.article.status // empty')
CURRENT_EXTRACTED=$(echo "$ARTICLE_META" | jq -r '.article.extracted_content[0].id // empty')

if [ -z "$ARTICLE_ID" ]; then
  echo "ERROR: Article $ARTICLE_DID not found."
  exit 1
fi

echo "  ID:     $ARTICLE_ID"
echo "  Title:  $CURRENT_TITLE"
echo "  Status: $CURRENT_STATUS"
echo "  Extracted content artifact: ${CURRENT_EXTRACTED:-none}"

if $DRY_RUN; then
  echo ""
  echo "--- DRY RUN ---"
  echo "Would update article $ARTICLE_DID with content from $CONTENT_FILE"
  [ -n "$TITLE" ] && echo "Would set title to: $TITLE"
  $PUBLISH && echo "Would set status to: published"
  echo "---------------"
  exit 0
fi

# Step 2: Prepare staged content upload
echo ""
echo "Step 2: Preparing upload..."
PREPARE_RESPONSE=$(curl -s -X POST "$API/artifacts.contents.prepare" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"file_type\": \"text/plain\"}")

STAGED_CONTENT_ID=$(echo "$PREPARE_RESPONSE" | jq -r '.staged_content.id // empty')
UPLOAD_URL=$(echo "$PREPARE_RESPONSE" | jq -r '.url // empty')
FORM_DATA=$(echo "$PREPARE_RESPONSE" | jq -r '.form_data // []')

if [ -z "$STAGED_CONTENT_ID" ] || [ -z "$UPLOAD_URL" ]; then
  echo "ERROR: Failed to prepare upload. Response:"
  echo "$PREPARE_RESPONSE" | jq .
  exit 1
fi

echo "  Staged content ID: $STAGED_CONTENT_ID"
echo "  Upload URL: $UPLOAD_URL"

# Step 3: Upload the file
echo ""
echo "Step 3: Uploading content..."

# Build multipart form data
FORM_ARGS=()
for i in $(seq 0 $(($(echo "$FORM_DATA" | jq '. | length') - 1))); do
  KEY=$(echo "$FORM_DATA" | jq -r ".[$i].key")
  VALUE=$(echo "$FORM_DATA" | jq -r ".[$i].value")
  FORM_ARGS+=(-F "$KEY=$VALUE")
done
FORM_ARGS+=(-F "file=@$CONTENT_FILE")

curl -s -X POST "$UPLOAD_URL" "${FORM_ARGS[@]}" > /dev/null

echo "  ✅ Uploaded"

# Step 4: Validate staged content
echo ""
echo "Step 4: Validating staged content..."
sleep 2  # Give the system a moment to process

VALIDATE_RESPONSE=$(curl -s -X POST "$API/artifacts.contents.validate" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$STAGED_CONTENT_ID\"}")

VALIDATION_STATUS=$(echo "$VALIDATE_RESPONSE" | jq -r '.staged_content.status // "unknown"')
echo "  Status: $VALIDATION_STATUS"

if [ "$VALIDATION_STATUS" != "validated" ]; then
  echo "WARNING: Staged content not yet validated (status: $VALIDATION_STATUS). Attempting to continue..."
fi

# Step 5: Create artifact from staged content
echo ""
echo "Step 5: Creating artifact..."

CREATE_RESPONSE=$(curl -s -X POST "$API/artifacts.create-from-content" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"staged_content_id\": \"$STAGED_CONTENT_ID\", \"file_name\": \"$FILE_NAME\"}")

NEW_ARTIFACT_ID=$(echo "$CREATE_RESPONSE" | jq -r '.artifact.id // empty')

if [ -z "$NEW_ARTIFACT_ID" ]; then
  echo "ERROR: Failed to create artifact. Response:"
  echo "$CREATE_RESPONSE" | jq .
  exit 1
fi

echo "  ✅ New artifact: $NEW_ARTIFACT_ID"

# Step 6: Update the article
echo ""
echo "Step 6: Updating article..."

UPDATE_BODY=$(jq -n \
  --arg id "$ARTICLE_ID" \
  --arg artifact "$NEW_ARTIFACT_ID" \
  '{
    id: $id,
    content_artifact: $artifact
  }')

# Add optional title
if [ -n "$TITLE" ]; then
  UPDATE_BODY=$(echo "$UPDATE_BODY" | jq --arg title "$TITLE" '. + {title: $title}')
fi

# Add optional publish
if $PUBLISH; then
  UPDATE_BODY=$(echo "$UPDATE_BODY" | jq '. + {status: "published"}')
fi

echo "  Payload: $(echo "$UPDATE_BODY" | jq -c .)"

UPDATE_RESPONSE=$(curl -s -X POST "$API/articles.update" \
  -H "Authorization: $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_BODY")

UPDATED_ID=$(echo "$UPDATE_RESPONSE" | jq -r '.article.id // empty')

if [ -z "$UPDATED_ID" ]; then
  echo "ERROR: Failed to update article. Response:"
  echo "$UPDATE_RESPONSE" | jq .
  exit 1
fi

echo ""
echo "✅ Article updated successfully!"
echo "  Article: $UPDATED_ID"
echo "  New artifact: $NEW_ARTIFACT_ID"
[ -n "$TITLE" ] && echo "  Title: $TITLE"
$PUBLISH && echo "  Status: published"
