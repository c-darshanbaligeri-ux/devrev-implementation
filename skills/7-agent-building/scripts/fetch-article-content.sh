#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# fetch-article-content.sh - Robust article content extraction
# ============================================================================
# Handles multiple content formats: published_version, extracted_content, 
# resource artifacts, with fallback strategy
#
# Usage:
#   bash fetch-article-content.sh <article_id> <output_file>
#   bash fetch-article-content.sh don:core:dvrv-in-1:devo/X:article/Y output.txt
#
# Requires:
#   - ORG_PAT environment variable (for internal API)
#   - curl, jq
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Load environment variables
if [ -f "$WORKSPACE_ROOT/.env" ]; then
  set -a
  source "$WORKSPACE_ROOT/.env"
  set +a
else
  echo "Error: .env file not found at $WORKSPACE_ROOT/.env" >&2
  echo "Current script dir: $SCRIPT_DIR" >&2
  exit 1
fi

# Validate inputs
if [ $# -ne 2 ]; then
  echo "Usage: $0 <article_id> <output_file>" >&2
  echo "Example: $0 don:core:dvrv-in-1:devo/X:article/27 article27.txt" >&2
  exit 1
fi

ARTICLE_ID="$1"
OUTPUT_FILE="$2"

# Validate ORG_PAT
if [ -z "${ORG_PAT:-}" ]; then
  echo "Error: ORG_PAT not set in environment" >&2
  exit 1
fi

# ============================================================================
# Step 1: Fetch article metadata
# ============================================================================
echo "Fetching article metadata for ${ARTICLE_ID}..." >&2

ARTICLE_JSON=$(mktemp)
trap "rm -f $ARTICLE_JSON" EXIT

curl -s -X POST 'https://api.devrev.ai/internal/articles.get' \
  -H "Authorization: ${ORG_PAT}" \
  -H 'Content-Type: application/json' \
  -d "{\"id\": \"${ARTICLE_ID}\"}" > "$ARTICLE_JSON"

# Check for API errors
if jq -e '.type == "bad_request"' "$ARTICLE_JSON" > /dev/null 2>&1; then
  echo "Error: API request failed" >&2
  jq -r '.message // .debug_message' "$ARTICLE_JSON" >&2
  exit 1
fi

ARTICLE_TITLE=$(jq -r '.article.title' "$ARTICLE_JSON")
echo "Article: ${ARTICLE_TITLE}" >&2

# ============================================================================
# Step 2: Try published_version.body (fastest, for published articles)
# ============================================================================
BODY=$(jq -r '.article.published_version.body // empty' "$ARTICLE_JSON")
if [ -n "$BODY" ]; then
  echo "✓ Content found in published_version.body" >&2
  echo "$BODY" > "$OUTPUT_FILE"
  echo "Content written to: $OUTPUT_FILE" >&2
  exit 0
fi

# ============================================================================
# Step 3: Try extracted_content[0].original_url (for articles with extraction)
# ============================================================================
EXTRACTED_URL=$(jq -r '.article.extracted_content[0].original_url // empty' "$ARTICLE_JSON")
EXTRACTED_TYPE=$(jq -r '.article.extracted_content[0].file.type // empty' "$ARTICLE_JSON")

if [ -n "$EXTRACTED_URL" ]; then
  echo "✓ Content found in extracted_content" >&2
  echo "  File type: ${EXTRACTED_TYPE}" >&2
  
  if [[ "$EXTRACTED_TYPE" == "text/plain" ]]; then
    echo "  Downloading plain text content..." >&2
    curl -s "$EXTRACTED_URL" > "$OUTPUT_FILE"
    echo "Content written to: $OUTPUT_FILE" >&2
    exit 0
  else
    echo "  Warning: Content type is ${EXTRACTED_TYPE}, attempting download..." >&2
    curl -s "$EXTRACTED_URL" > "$OUTPUT_FILE"
    
    # Check if output is binary
    if file "$OUTPUT_FILE" | grep -q "ASCII text\|UTF-8"; then
      echo "Content written to: $OUTPUT_FILE" >&2
      exit 0
    else
      echo "Error: Downloaded content is binary (${EXTRACTED_TYPE})" >&2
      echo "  File may require special parsing (xlsx2csv, docx2txt, pdftotext)" >&2
      exit 1
    fi
  fi
fi

# ============================================================================
# Step 4: Try resource.artifacts[0].original_url (devrev/rt or attachments)
# ============================================================================
ARTIFACT_URL=$(jq -r '.article.resource.artifacts[0].original_url // empty' "$ARTICLE_JSON")
ARTIFACT_TYPE=$(jq -r '.article.resource.artifacts[0].file.type // empty' "$ARTICLE_JSON")

if [ -n "$ARTIFACT_URL" ]; then
  echo "✓ Content found in resource.artifacts" >&2
  echo "  File type: ${ARTIFACT_TYPE}" >&2
  
  if [[ "$ARTIFACT_TYPE" == "devrev/rt" ]]; then
    echo "  Warning: Content is in DevRev rich text format" >&2
    echo "  Attempting download, but content may not be human-readable..." >&2
  fi
  
  curl -s "$ARTIFACT_URL" > "$OUTPUT_FILE"
  
  # Check if output is text
  if file "$OUTPUT_FILE" | grep -q "ASCII text\|UTF-8"; then
    echo "Content written to: $OUTPUT_FILE" >&2
    exit 0
  else
    echo "Error: Downloaded content is binary (${ARTIFACT_TYPE})" >&2
    echo "  Original URL: ${ARTIFACT_URL}" >&2
    exit 1
  fi
fi

# ============================================================================
# No content found
# ============================================================================
echo "Error: No content found for article ${ARTICLE_ID}" >&2
echo "  Title: ${ARTICLE_TITLE}" >&2
echo "  Tried: published_version.body, extracted_content, resource.artifacts" >&2
echo "" >&2
echo "Article may be:" >&2
echo "  - A draft with no published content" >&2
echo "  - A binary attachment without text extraction" >&2
echo "  - An external link or reference" >&2
exit 1
