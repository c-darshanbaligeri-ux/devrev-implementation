#!/bin/bash
# create-agent.sh — Create or update a DevRev AI agent via internal API
#
# Usage:
#   create:  ./create-agent.sh create  <payload-file.json>
#   update:  ./create-agent.sh update  <payload-file.json>
#   convert: ./create-agent.sh convert <get-response.json>   # convert GET response to update payload
#   check:   ./create-agent.sh check   <payload-file.json>   # validate payload without calling API
#   delete:  ./create-agent.sh delete  <agent-id>            # delete agent (3s confirmation delay)
#
# Requires:
#   ORG_PAT — for internal APIs (ai-agents)
#
# Payload structure:
#   See references/api-contracts.md for the full schema and pre-flight checklist.
#   See references/guardrails-api.md for guardrail schema details.
#
# Key rules (enforced by --check):
#   CREATE:  guardrails = plain array, skills = plain array, no slug field
#   UPDATE:  guardrails = {"set":[...]}, skills = {"set":[...]}, id required, no slug
#   BOTH:    topic_name/description FLAT in guardrail (not nested under topic_boundary)
#            trigger.operation / trigger.plan / trigger.workflow must be STRING IDs, not objects

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# ── Load PATs ──
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

INTERNAL_API="https://api.devrev.ai/internal"

# ── Helpers ──
check_jq() {
  if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is required. Install with: brew install jq" >&2
    exit 1
  fi
}

red()    { echo -e "\033[31m$*\033[0m" >&2; }
yellow() { echo -e "\033[33m$*\033[0m" >&2; }
green()  { echo -e "\033[32m$*\033[0m" >&2; }

# ── Validate payload ──
validate_payload() {
  local mode="$1"  # "create" or "update"
  local file="$2"
  local errors=0

  echo "🔍 Validating $mode payload: $file" >&2

  if [ ! -f "$file" ]; then
    red "  ✗ File not found: $file"
    return 1
  fi

  if ! jq -e '.' "$file" >/dev/null 2>&1; then
    red "  ✗ Invalid JSON"
    return 1
  fi

  # ── Common checks ──
  if jq -e '.slug' "$file" >/dev/null 2>&1; then
    red "  ✗ 'slug' field is not accepted by the API. Remove it."
    errors=$((errors+1))
  fi

  # ── Guardrails checks ──
  GUARDRAILS_TYPE=$(jq -r 'if .guardrails then (.guardrails | type) else "absent" end' "$file")

  if [ "$mode" = "create" ]; then
    if [ "$GUARDRAILS_TYPE" = "object" ]; then
      red "  ✗ 'guardrails' must be a plain ARRAY for create, not an object."
      yellow "    Fix: change 'guardrails: {...}' to 'guardrails: [...]'"
      errors=$((errors+1))
    fi
  fi

  if [ "$mode" = "update" ]; then
    if [ "$GUARDRAILS_TYPE" = "array" ]; then
      red "  ✗ 'guardrails' must be wrapped as {'set': [...]} for update, not a plain array."
      yellow "    Fix: change 'guardrails: [...]' to 'guardrails: {\"set\": [...]}'"
      errors=$((errors+1))
    fi
    if [ "$GUARDRAILS_TYPE" = "object" ]; then
      HAS_SET=$(jq -r 'if .guardrails.set then "yes" else "no" end' "$file")
      if [ "$HAS_SET" = "no" ]; then
        red "  ✗ 'guardrails' object is missing required 'set' key."
        errors=$((errors+1))
      fi
    fi
    # Check id present on update
    HAS_ID=$(jq -r 'if .id then "yes" else "no" end' "$file")
    if [ "$HAS_ID" = "no" ]; then
      red "  ✗ 'id' field is required for update."
      errors=$((errors+1))
    fi
  fi

  # ── topic_boundary nesting check ──
  NESTED_COUNT=0
  if [ "$GUARDRAILS_TYPE" = "array" ]; then
    NESTED_COUNT=$(jq '[.guardrails[]? | select(.topic_boundary != null)] | length' "$file")
  elif [ "$GUARDRAILS_TYPE" = "object" ]; then
    NESTED_COUNT=$(jq '[.guardrails.set[]? | select(.topic_boundary != null)] | length' "$file")
  fi
  if [ "$NESTED_COUNT" -gt 0 ]; then
    red "  ✗ $NESTED_COUNT guardrail(s) use nested 'topic_boundary' object — this is the GET response shape."
    yellow "    Fix: flatten 'topic_name' and 'description' to the guardrail's top level."
    yellow "    Wrong: { \"topic_boundary\": { \"topic_name\": \"...\", \"description\": \"...\" } }"
    yellow "    Right: { \"topic_name\": \"...\", \"description\": \"...\" }"
    errors=$((errors+1))
  fi

  # ── Skills checks ──
  SKILLS_TYPE=$(jq -r 'if .skills then (.skills | type) else "absent" end' "$file")

  if [ "$mode" = "create" ]; then
    if [ "$SKILLS_TYPE" = "object" ]; then
      red "  ✗ 'skills' must be a plain ARRAY for create, not an object."
      errors=$((errors+1))
    fi
  fi

  if [ "$mode" = "update" ]; then
    if [ "$SKILLS_TYPE" = "array" ]; then
      red "  ✗ 'skills' must be wrapped as {'set': [...]} for update, not a plain array."
      yellow "    Fix: change 'skills: [...]' to 'skills: {\"set\": [...]}'"
      errors=$((errors+1))
    fi
    if [ "$SKILLS_TYPE" = "object" ]; then
      HAS_SET=$(jq -r 'if .skills.set then "yes" else "no" end' "$file")
      if [ "$HAS_SET" = "no" ]; then
        red "  ✗ 'skills' object is missing required 'set' key."
        errors=$((errors+1))
      fi
    fi
  fi

  # ── Skill trigger object check (operation, plan, workflow) ──
  OP_OBJECT_COUNT=0
  PLAN_OBJECT_COUNT=0
  WF_OBJECT_COUNT=0
  if [ "$SKILLS_TYPE" = "array" ]; then
    OP_OBJECT_COUNT=$(jq '[.skills[]? | select(.trigger.operation != null and (.trigger.operation | type) == "object")] | length' "$file")
    PLAN_OBJECT_COUNT=$(jq '[.skills[]? | select(.trigger.plan != null and (.trigger.plan | type) == "object")] | length' "$file")
    WF_OBJECT_COUNT=$(jq '[.skills[]? | select(.trigger.workflow != null and (.trigger.workflow | type) == "object")] | length' "$file")
  elif [ "$SKILLS_TYPE" = "object" ]; then
    OP_OBJECT_COUNT=$(jq '[.skills.set[]? | select(.trigger.operation != null and (.trigger.operation | type) == "object")] | length' "$file")
    PLAN_OBJECT_COUNT=$(jq '[.skills.set[]? | select(.trigger.plan != null and (.trigger.plan | type) == "object")] | length' "$file")
    WF_OBJECT_COUNT=$(jq '[.skills.set[]? | select(.trigger.workflow != null and (.trigger.workflow | type) == "object")] | length' "$file")
  fi
  if [ "$OP_OBJECT_COUNT" -gt 0 ]; then
    red "  ✗ $OP_OBJECT_COUNT skill(s) have 'trigger.operation' as an OBJECT — must be a STRING (DON ID)."
    yellow "    Wrong: { \"operation\": { \"id\": \"don:...\", \"name\": \"...\" } }"
    yellow "    Right: { \"operation\": \"don:...\" }"
    errors=$((errors+1))
  fi
  if [ "$PLAN_OBJECT_COUNT" -gt 0 ]; then
    red "  ✗ $PLAN_OBJECT_COUNT skill(s) have 'trigger.plan' as an OBJECT — must be a STRING (DON ID)."
    yellow "    Wrong: { \"plan\": { \"id\": \"don:...\", \"display_id\": \"...\" } }"
    yellow "    Right: { \"plan\": \"don:...\" }"
    errors=$((errors+1))
  fi
  if [ "$WF_OBJECT_COUNT" -gt 0 ]; then
    red "  ✗ $WF_OBJECT_COUNT skill(s) have 'trigger.workflow' as an OBJECT — must be a STRING (DON ID)."
    yellow "    Wrong: { \"workflow\": { \"id\": \"don:...\", \"display_id\": \"...\" } }"
    yellow "    Right: { \"workflow\": \"don:...\" }"
    errors=$((errors+1))
  fi

  if [ "$errors" -eq 0 ]; then
    green "  ✅ Payload is valid for $mode"
    return 0
  else
    red "  ✗ $errors validation error(s) found. Fix before calling the API."
    return 1
  fi
}

# ── Convert GET response to update payload ──
convert_get_to_update() {
  local input_file="$1"
  local output_file="${2:-/tmp/agent-update-payload.json}"

  echo "🔄 Converting GET response to update payload..." >&2
  echo "   Input:  $input_file" >&2
  echo "   Output: $output_file" >&2

  if ! jq -e '.agent' "$input_file" >/dev/null 2>&1; then
    red "ERROR: Input file does not look like an ai-agents.get response (missing .agent)"
    exit 1
  fi

  # Convert each trigger type (operation / plan / workflow) from hydrated object → string ID.
  # Notes:
  #   - guidance=null is rejected by update API (expects STRING, not NULL).
  #     The key is omitted when absent so the field is left unchanged by the update.
  #   - GET omits skills/guardrails keys when they're empty; []? handles this safely.
  jq '{
    id: .agent.id,
    goal: .agent.goal,
    guidance: .agent.guidance,
    memory_config: .agent.memory_config,
    guardrails: {
      set: [
        .agent.guardrails[]? |
        {
          type: .type,
          applies_to: .applies_to,
          enabled: (.enabled // true),
          default_message: (.default_message // ""),
          topic_name: (.topic_boundary.topic_name // null),
          description: (.topic_boundary.description // null)
        } |
        with_entries(select(.value != null))
      ]
    },
    skills: {
      set: [
        .agent.skills[]? |
        {
          name: .name,
          description: (.description // null),
          act_as_user: (.act_as_user // false),
          needs_approval: (.needs_approval // null),
          trigger: (
            if .trigger.plan then
              { plan: .trigger.plan.id }
            elif .trigger.workflow then
              { workflow: .trigger.workflow.id }
            elif .trigger.operation then
              { operation: .trigger.operation.id }
            else
              null
            end
          )
        } |
        with_entries(select(.value != null))
      ]
    }
  }
  # Remove null-valued top-level keys to avoid sending null strings to update API.
  # guidance=null causes: "Unexpected JSON type for field: guidance, expected: STRING, actual: NULL"
  | with_entries(select(.value != null))
  ' "$input_file" > "$output_file"

  green "  ✅ Converted. Review before using:"
  echo "" >&2
  jq '.' "$output_file" >&2
}

# ── Main ──
check_jq

COMMAND="${1:-help}"
PAYLOAD_FILE="${2:-}"

case "$COMMAND" in
  check)
    if [ -z "$PAYLOAD_FILE" ]; then
      echo "Usage: $0 check <payload-file.json> [create|update]" >&2
      exit 1
    fi
    MODE="${3:-create}"
    validate_payload "$MODE" "$PAYLOAD_FILE"
    ;;

  convert)
    if [ -z "$PAYLOAD_FILE" ]; then
      echo "Usage: $0 convert <get-response.json> [output-file.json]" >&2
      exit 1
    fi
    OUTPUT="${3:-/tmp/agent-update-payload.json}"
    convert_get_to_update "$PAYLOAD_FILE" "$OUTPUT"
    ;;

  create)
    if [ -z "$PAYLOAD_FILE" ]; then
      echo "Usage: $0 create <payload-file.json>" >&2
      exit 1
    fi

    if ! load_pat ORG_PAT; then
      red "ERROR: ORG_PAT not found. Copy .env.example to .env and fill in your tokens."
      exit 1
    fi

    if ! validate_payload "create" "$PAYLOAD_FILE"; then
      red "Aborting — fix validation errors before calling the API."
      exit 1
    fi

    echo "" >&2
    echo "📤 Calling ai-agents.create..." >&2
    RESP=$(curl -s -X POST "$INTERNAL_API/ai-agents.create" \
      -H "Authorization: $ORG_PAT" \
      -H "Content-Type: application/json" \
      -d @"$PAYLOAD_FILE")

    if echo "$RESP" | jq -e '.agent.id' >/dev/null 2>&1; then
      AGENT_ID=$(echo "$RESP" | jq -r '.agent.id')
      AGENT_DID=$(echo "$RESP" | jq -r '.agent.display_id')
      green "  ✅ Created agent: $AGENT_DID ($AGENT_ID)"
      echo "$RESP" | jq '{ id: .agent.id, display_id: .agent.display_id, name: .agent.service_account.display_name, version: .agent.default_version_id.display_id }' >&2
    else
      red "  ✗ Create failed:"
      echo "$RESP" | jq '{type, message, debug_message, field_name}' >&2
      exit 1
    fi
    ;;

  update)
    if [ -z "$PAYLOAD_FILE" ]; then
      echo "Usage: $0 update <payload-file.json>" >&2
      exit 1
    fi

    if ! load_pat ORG_PAT; then
      red "ERROR: ORG_PAT not found. Copy .env.example to .env and fill in your tokens."
      exit 1
    fi

    if ! validate_payload "update" "$PAYLOAD_FILE"; then
      red "Aborting — fix validation errors before calling the API."
      exit 1
    fi

    echo "" >&2
    echo "📤 Calling ai-agents.update..." >&2
    RESP=$(curl -s -X POST "$INTERNAL_API/ai-agents.update" \
      -H "Authorization: $ORG_PAT" \
      -H "Content-Type: application/json" \
      -d @"$PAYLOAD_FILE")

    if echo "$RESP" | jq -e '.agent.id' >/dev/null 2>&1; then
      AGENT_ID=$(echo "$RESP" | jq -r '.agent.id')
      AGENT_DID=$(echo "$RESP" | jq -r '.agent.display_id')
      SKILLS_COUNT=$(echo "$RESP" | jq '.agent.skills | length')
      GUARDRAILS_COUNT=$(echo "$RESP" | jq '.agent.guardrails | length')
      green "  ✅ Updated agent: $AGENT_DID ($AGENT_ID)"
      echo "$RESP" | jq '{ id: .agent.id, display_id: .agent.display_id, name: .agent.service_account.display_name, version: .agent.default_version_id.display_id, skills: (.agent.skills | length), guardrails: (.agent.guardrails | length) }' >&2
    else
      red "  ✗ Update failed:"
      echo "$RESP" | jq '{type, message, debug_message, field_name}' >&2
      exit 1
    fi
    ;;

  delete)
    if [ -z "$PAYLOAD_FILE" ]; then
      echo "Usage: $0 delete <agent-id-or-display-id>" >&2
      exit 1
    fi

    if ! load_pat ORG_PAT; then
      red "ERROR: ORG_PAT not found. Copy .env.example to .env and fill in your tokens."
      exit 1
    fi

    AGENT_TO_DELETE="$PAYLOAD_FILE"
    echo "⚠️  About to DELETE agent: $AGENT_TO_DELETE" >&2
    echo "   Press Ctrl+C within 3 seconds to abort..." >&2
    sleep 3

    echo "" >&2
    echo "🗑️  Calling ai-agents.delete..." >&2
    RESP=$(curl -s -X POST "$INTERNAL_API/ai-agents.delete" \
      -H "Authorization: $ORG_PAT" \
      -H "Content-Type: application/json" \
      -d "{\"id\": \"$AGENT_TO_DELETE\"}")

    if echo "$RESP" | jq -e '. == {}' >/dev/null 2>&1; then
      green "  ✅ Deleted agent: $AGENT_TO_DELETE"
    else
      ERR=$(echo "$RESP" | jq -r '.type // "unknown"')
      MSG=$(echo "$RESP" | jq -r '.debug_message // .message // ""')
      red "  ✗ Delete failed: $ERR '$MSG'"
      exit 1
    fi
    ;;

  help|*)
    cat >&2 << 'USAGE'
create-agent.sh — Create or update a DevRev AI agent

Usage:
  ./create-agent.sh create  <payload-file.json>        Create a new agent
  ./create-agent.sh update  <payload-file.json>        Update an existing agent
  ./create-agent.sh convert <get-response.json> [out]  Convert GET response to update payload
  ./create-agent.sh check   <payload-file.json> [mode] Validate payload without calling API
  ./create-agent.sh delete  <agent-id>                 Delete an agent (with 3s confirmation delay)

Examples:
  # Fetch current config, convert to update payload, edit, validate, then apply
  bash scripts/get-agent.sh "don:core:..." /tmp/my-agent
  bash scripts/create-agent.sh convert /tmp/my-agent/agent.json /tmp/update.json
  # ... edit /tmp/update.json ...
  bash scripts/create-agent.sh check  /tmp/update.json update
  bash scripts/create-agent.sh update /tmp/update.json

  # Create a new agent from scratch
  bash scripts/create-agent.sh check  /tmp/new-agent.json create
  bash scripts/create-agent.sh create /tmp/new-agent.json

  # Delete a test agent (accepts DON ID or display_id format)
  bash scripts/create-agent.sh delete don:core:dvrv-in-1:devo/<id>:ai_agent/<n>
  bash scripts/create-agent.sh delete ai_agent-12

Key rules (enforced by check/create/update):
  CREATE:  guardrails = plain array, skills = plain array, no slug field, goal required
  UPDATE:  guardrails = {"set":[...]}, skills = {"set":[...]}, id required, no slug
  BOTH:    topic_name/description FLAT in guardrail (not nested under topic_boundary)
           trigger.operation / trigger.plan / trigger.workflow must be STRING IDs, not objects

See references/api-contracts.md for the full schema reference.
USAGE
    ;;
esac
