#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# validate-schema.sh - Validate custom object schema and payload
# ============================================================================
# Discovers custom object schemas in the org and validates payloads against them
#
# Usage:
#   bash validate-schema.sh list
#   bash validate-schema.sh describe raw_test_case
#   bash validate-schema.sh check raw_test_case payload.json
#
# Commands:
#   list                    - List all custom object types in org
#   describe <type>         - Show schema fields for a type
#   check <type> <payload>  - Validate payload against schema
#
# Requires:
#   - ORG_PAT environment variable
#   - curl, jq
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Script is in scripts/, go up 1 level to workspace root
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

# Validate ORG_PAT
if [ -z "${ORG_PAT:-}" ]; then
  echo "Error: ORG_PAT not set in environment" >&2
  exit 1
fi

COMMAND="${1:-}"

# ============================================================================
# Command: list - Show all custom object types
# ============================================================================
if [ "$COMMAND" = "list" ]; then
  echo "Fetching custom object schemas..."
  
  curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
    -H "Authorization: ${ORG_PAT}" \
    -H 'Content-Type: application/json' \
    -d '{}' | jq -r '
      ["TYPE", "PREFIX", "DESCRIPTION"],
      ["----", "------", "-----------"],
      (.schemas[] | [.leaf_type, .id_prefix, (.description // "N/A")])
      | @tsv' | column -t -s $'\t'
  
  exit 0
fi

# ============================================================================
# Command: describe - Show schema fields for a type
# ============================================================================
if [ "$COMMAND" = "describe" ]; then
  if [ $# -ne 2 ]; then
    echo "Usage: $0 describe <object_type>" >&2
    echo "Example: $0 describe raw_test_case" >&2
    exit 1
  fi
  
  OBJECT_TYPE="$2"
  echo "Fetching schema for: ${OBJECT_TYPE}..."
  
  SCHEMA_JSON=$(curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
    -H "Authorization: ${ORG_PAT}" \
    -H 'Content-Type: application/json' \
    -d "{}")
  
  # Check if type exists
  if ! echo "$SCHEMA_JSON" | jq -e ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\")" > /dev/null; then
    echo "Error: Custom object type '${OBJECT_TYPE}' not found" >&2
    echo "" >&2
    echo "Available types:" >&2
    echo "$SCHEMA_JSON" | jq -r '.schemas[] | "  - \(.leaf_type)"'
    exit 1
  fi
  
  # Display schema info
  echo "$SCHEMA_JSON" | jq -r ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\") | 
    \"Type: \(.leaf_type)
ID Prefix: \(.id_prefix)
Description: \(.description // \"N/A\")

Fields:\"" 
  
  echo ""
  echo "$SCHEMA_JSON" | jq -r ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\") |
    [\"NAME\", \"TYPE\", \"REQUIRED\", \"FILTERABLE\", \"DESCRIPTION\"],
    [\"----\", \"----\", \"--------\", \"----------\", \"-----------\"],
    (.fields[] | [
      .name,
      .field_type,
      (if .is_required then \"✓\" else \"\" end),
      (if .is_filterable then \"✓\" else \"\" end),
      (.description // \"N/A\")
    ])
    | @tsv" | column -t -s $'\t'
  
  exit 0
fi

# ============================================================================
# Command: check - Validate payload against schema
# ============================================================================
if [ "$COMMAND" = "check" ]; then
  if [ $# -ne 3 ]; then
    echo "Usage: $0 check <object_type> <payload_file>" >&2
    echo "Example: $0 check raw_test_case payload.json" >&2
    exit 1
  fi
  
  OBJECT_TYPE="$2"
  PAYLOAD_FILE="$3"
  
  if [ ! -f "$PAYLOAD_FILE" ]; then
    echo "Error: Payload file not found: ${PAYLOAD_FILE}" >&2
    exit 1
  fi
  
  echo "Validating payload against schema: ${OBJECT_TYPE}..."
  
  # Fetch schema
  SCHEMA_JSON=$(curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
    -H "Authorization: ${ORG_PAT}" \
    -H 'Content-Type: application/json' \
    -d "{}")
  
  # Check if type exists
  if ! echo "$SCHEMA_JSON" | jq -e ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\")" > /dev/null; then
    echo "Error: Custom object type '${OBJECT_TYPE}' not found" >&2
    exit 1
  fi
  
  # Extract required fields
  REQUIRED_FIELDS=$(echo "$SCHEMA_JSON" | jq -r ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\") | 
    .fields[] | select(.is_required == true) | .name")
  
  # Extract all field names
  ALL_FIELDS=$(echo "$SCHEMA_JSON" | jq -r ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\") | 
    .fields[] | .name")
  
  # Load payload
  PAYLOAD=$(cat "$PAYLOAD_FILE")
  
  ERRORS=0
  
  # Check required fields
  echo ""
  echo "Checking required fields..."
  for field in $REQUIRED_FIELDS; do
    if echo "$PAYLOAD" | jq -e ".${field}" > /dev/null 2>&1; then
      echo "  ✓ ${field}"
    else
      echo "  ✗ ${field} (MISSING - REQUIRED)"
      ERRORS=$((ERRORS + 1))
    fi
  done
  
  # Check for unknown fields
  echo ""
  echo "Checking for unknown fields..."
  PAYLOAD_FIELDS=$(echo "$PAYLOAD" | jq -r 'keys[]')
  for field in $PAYLOAD_FIELDS; do
    if echo "$ALL_FIELDS" | grep -q "^${field}$"; then
      echo "  ✓ ${field}"
    else
      echo "  ⚠ ${field} (unknown field - will be ignored or rejected)"
      ERRORS=$((ERRORS + 1))
    fi
  done
  
  # Check field types (basic validation)
  echo ""
  echo "Checking field types..."
  while IFS= read -r field; do
    FIELD_TYPE=$(echo "$SCHEMA_JSON" | jq -r ".schemas[] | select(.leaf_type == \"${OBJECT_TYPE}\") | 
      .fields[] | select(.name == \"${field}\") | .field_type")
    
    if echo "$PAYLOAD" | jq -e ".${field}" > /dev/null 2>&1; then
      PAYLOAD_TYPE=$(echo "$PAYLOAD" | jq -r ".${field} | type")
      
      case "$FIELD_TYPE" in
        "int")
          if [ "$PAYLOAD_TYPE" != "number" ]; then
            echo "  ✗ ${field}: expected int, got ${PAYLOAD_TYPE}"
            ERRORS=$((ERRORS + 1))
          else
            echo "  ✓ ${field}: int"
          fi
          ;;
        "bool")
          if [ "$PAYLOAD_TYPE" != "boolean" ]; then
            echo "  ✗ ${field}: expected bool, got ${PAYLOAD_TYPE}"
            ERRORS=$((ERRORS + 1))
          else
            echo "  ✓ ${field}: bool"
          fi
          ;;
        "tokens"|"text"|"rich_text"|"timestamp"|"enum")
          if [ "$PAYLOAD_TYPE" != "string" ]; then
            echo "  ✗ ${field}: expected string, got ${PAYLOAD_TYPE}"
            ERRORS=$((ERRORS + 1))
          else
            echo "  ✓ ${field}: string"
          fi
          ;;
        "double")
          if [ "$PAYLOAD_TYPE" != "number" ]; then
            echo "  ✗ ${field}: expected number, got ${PAYLOAD_TYPE}"
            ERRORS=$((ERRORS + 1))
          else
            echo "  ✓ ${field}: double"
          fi
          ;;
        *)
          echo "  ? ${field}: ${FIELD_TYPE} (validation not implemented)"
          ;;
      esac
    fi
  done <<< "$ALL_FIELDS"
  
  # Summary
  echo ""
  if [ $ERRORS -eq 0 ]; then
    echo "✓ Validation passed: payload is valid"
    exit 0
  else
    echo "✗ Validation failed: ${ERRORS} error(s) found"
    exit 1
  fi
fi

# ============================================================================
# Invalid command
# ============================================================================
echo "Usage: $0 <command> [args]" >&2
echo "" >&2
echo "Commands:" >&2
echo "  list                      - List all custom object types" >&2
echo "  describe <type>           - Show schema fields for a type" >&2
echo "  check <type> <payload>    - Validate payload against schema" >&2
echo "" >&2
echo "Examples:" >&2
echo "  $0 list" >&2
echo "  $0 describe raw_test_case" >&2
echo "  $0 check raw_test_case payload.json" >&2
exit 1
