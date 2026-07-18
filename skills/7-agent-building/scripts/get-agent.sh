#!/bin/bash
# get-agent.sh — Fetch an AI agent's full config + its workflow/plan skills via DevRev internal API
# Usage: ./get-agent.sh <agent-id-or-slug> [output_dir]
#
# Requires:
#   DEVREV_PAT — for public APIs (knowledge base, articles)
#   ORG_PAT    — for internal APIs (ai-agents, workflows)

set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: $0 <agent-id-or-slug> [output_dir]" >&2
  exit 1
fi

AGENT="$1"
OUTPUT_DIR="${2:-/tmp/devrev-agent-config}"
mkdir -p "$OUTPUT_DIR"

# ── Load PATs (check project-local .env first, then ~/.openclaw-autoclaw/.env) ──
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
  echo "  Copy .env.example to .env and fill in your tokens:" >&2
  echo "    cp .env.example .env" >&2
  exit 1
fi

if ! load_pat ORG_PAT; then
  echo "ERROR: ORG_PAT not found." >&2
  echo "  Copy .env.example to .env and fill in your tokens:" >&2
  echo "    cp .env.example .env" >&2
  exit 1
fi

INTERNAL_API="https://api.devrev.ai/internal"

# ── Step 1: Fetch agent config ──
echo "🔍 Fetching agent: $AGENT" >&2

AGENT_RESP=$(curl -s -X POST "$INTERNAL_API/ai-agents.get" \
  -H "Authorization: $ORG_PAT" \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$AGENT\"}" 2>/dev/null || echo '{}')

if ! echo "$AGENT_RESP" | jq -e '.agent' >/dev/null 2>&1; then
  echo "ERROR: Could not fetch agent from internal API." >&2
  echo "       Response: $(echo "$AGENT_RESP" | jq -r '.message // "unknown error"')" >&2
  echo "       Debug:    $(echo "$AGENT_RESP" | jq -r '.debug_message // ""')" >&2
  exit 1
fi

echo "$AGENT_RESP" | jq '.' > "$OUTPUT_DIR/agent.json"
AGENT_NAME=$(echo "$AGENT_RESP" | jq -r '.agent.service_account.display_name // .agent.name // .agent.display_id // "unknown"')
AGENT_DID=$(echo "$AGENT_RESP" | jq -r '.agent.display_id // "unknown"')
AGENT_VER=$(echo "$AGENT_RESP" | jq -r '.agent.default_version_id.display_id // "unknown"')
echo "  ✅ Agent: $AGENT_DID — $AGENT_NAME (version: $AGENT_VER)" >&2

# ── Step 2: Print skill summary ──
SKILL_COUNT=$(echo "$AGENT_RESP" | jq '[.agent.skills[]?] | length')
echo "  📦 Agent has $SKILL_COUNT skill(s):" >&2
echo "$AGENT_RESP" | jq -r '
  .agent.skills[]? |
  "    - \(.name) [" +
  (if .trigger.plan then "plan:\(.trigger.plan.id)"
   elif .trigger.workflow then "workflow:\(.trigger.workflow.id)"
   elif .trigger.operation then "op:\(.trigger.operation.id)"
   else "trigger:unknown"
   end) + "]"
' >&2 || true

echo "$AGENT_RESP" | jq -r '.agent.skills[]? | .name' > "$OUTPUT_DIR/skill-names.txt" 2>/dev/null || true

# ── Step 3: Fetch plan-triggered and workflow-triggered skill definitions ──
# Skills can have one of three trigger types (in GET response shape):
#   - operation-triggered:  .trigger.operation.id  → native DevRev ops, no separate fetch needed
#   - plan-triggered:       .trigger.plan.id        → custom ai_agent_plan (fetchable)
#   - workflow-triggered:   .trigger.workflow.id    → custom org workflow (fetchable)
#
# We collect both plan and workflow IDs and attempt to fetch each.

CUSTOM_TRIGGERS=$(echo "$AGENT_RESP" | jq -r '
  .agent.skills[]? |
  if .trigger.plan then "plan\t" + .trigger.plan.id
  elif .trigger.workflow then "workflow\t" + .trigger.workflow.id
  else empty
  end
' 2>/dev/null || true)

if [ -n "$CUSTOM_TRIGGERS" ]; then
  echo "" >&2
  echo "  🔧 Fetching custom-trigger skill definitions (plan / workflow)..." >&2
  while IFS=$'\t' read -r TRIG_TYPE TRIG_ID; do
    [ -z "$TRIG_ID" ] && continue

    echo "     $TRIG_TYPE: $TRIG_ID" >&2
    SAFE_ID=$(echo "$TRIG_ID" | tr ':/' '_')

    if [ "$TRIG_TYPE" = "plan" ]; then
      # NOTE: ai-agents.plans.get and ai-agents.plans.list do NOT exist (route not found).
      # Plan trigger definitions (ai_agent_plan objects) cannot be fetched via the current API.
      # The plan ID is preserved in the skill trigger for reference only.
      echo "       ℹ️  plan: $TRIG_ID" >&2
      echo "          (No fetch API exists for ai_agent_plan objects — DON ID preserved in output)" >&2
      echo "{\"plan_id\": \"$TRIG_ID\", \"note\": \"No fetch endpoint exists for ai_agent_plan objects\"}" \
        > "$OUTPUT_DIR/plan-${SAFE_ID}.json"
    else
      FETCH_ENDPOINT="workflows.get"
      FETCH_KEY="workflow"

      WF_RESP=$(curl -s -X POST "$INTERNAL_API/$FETCH_ENDPOINT" \
        -H "Authorization: $ORG_PAT" \
        -H "Content-Type: application/json" \
        -d "{\"id\": \"$TRIG_ID\"}" 2>/dev/null || echo '{}')

      if echo "$WF_RESP" | jq -e ".$FETCH_KEY" >/dev/null 2>&1; then
        WF_NAME=$(echo "$WF_RESP" | jq -r ".$FETCH_KEY.name // .$FETCH_KEY.display_id // \"unknown\"")
        echo "$WF_RESP" | jq '.' > "$OUTPUT_DIR/${TRIG_TYPE}-${SAFE_ID}.json"
        echo "       ✅ $TRIG_TYPE definition: $WF_NAME" >&2
      else
        echo "       ⚠️  Could not fetch $TRIG_TYPE definition for $TRIG_ID" >&2
        echo "          Response: $(echo "$WF_RESP" | jq -r '.message // "unknown error"')" >&2
      fi
    fi

    sleep 0.15
  done <<< "$CUSTOM_TRIGGERS"
else
  echo "  ℹ️  All skills use native operation triggers (no plan/workflow fetch needed)" >&2
fi

# ── Step 4: List all agents in the org (for reference) ──
echo "" >&2
echo "📋 Fetching all agents in org..." >&2
ALL_AGENTS=$(curl -s -X POST "$INTERNAL_API/ai-agents.list" \
  -H "Authorization: $ORG_PAT" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}' 2>/dev/null || echo '{}')

if echo "$ALL_AGENTS" | jq -e '.agents' >/dev/null 2>&1; then
  echo "$ALL_AGENTS" | jq '[.agents[] | {display_id, name: .service_account.display_name, slug, goal: (.goal | .[0:80])}]' > "$OUTPUT_DIR/all-agents.json"
  AGENT_TOTAL=$(echo "$ALL_AGENTS" | jq '.agents | length')
  echo "  ✅ Found $AGENT_TOTAL agent(s) in org" >&2
  echo "" >&2
  echo "  All agents:" >&2
  echo "$ALL_AGENTS" | jq -r '.agents[] | "    \(.display_id) — \(.service_account.display_name // "unnamed") [slug: \(.slug // "none")]"' >&2
else
  echo "  ⚠️  Could not list agents" >&2
fi

# ── Step 5: Print guardrails summary ──
echo "" >&2
GUARDRAIL_COUNT=$(echo "$AGENT_RESP" | jq '[.agent.guardrails[]?] | length')
if [ "$GUARDRAIL_COUNT" -gt 0 ]; then
  echo "🛡️  Guardrails ($GUARDRAIL_COUNT):" >&2
  echo "$AGENT_RESP" | jq -r '.agent.guardrails[]? | "  - type=\(.type) enabled=\(.enabled) applies_to=\(.applies_to | join(",")) topic=\(.topic_boundary.topic_name // "n/a")"' >&2
else
  echo "🛡️  No guardrails configured" >&2
fi

# ── Step 6: Print memory config ──
echo "" >&2
echo "🧠 Memory config:" >&2
echo "$AGENT_RESP" | jq '.agent.memory_config // "not configured"' >&2

# ── Summary ──
echo "" >&2
echo "📁 Output: $OUTPUT_DIR/" >&2
echo "  - agent.json               full agent config (GET response shape)" >&2
echo "  - plan-*.json              plan-triggered skill definitions" >&2
echo "  - workflow-*.json          workflow-triggered skill definitions" >&2
echo "  - all-agents.json          all agents in org" >&2
echo "  - skill-names.txt          list of skill names" >&2
echo "" >&2
echo "⚠️  IMPORTANT — GET response ≠ write payload shape:" >&2
echo "   Skills:     trigger.operation / trigger.plan / trigger.workflow are OBJECTS in agent.json" >&2
echo "               but must be STRING IDs in create/update payloads." >&2
echo "   Guardrails: topic_boundary is NESTED in agent.json (GET shape)" >&2
echo "               but must be FLAT (topic_name, description at top level)" >&2
echo "               in create/update payloads." >&2
echo "   Skills/Guardrails wrapper: plain ARRAY for create, {\"set\": [...]} for update." >&2
echo "   Guidance:   Check for &nbsp; entities, ═══ borders, truncated rules before reusing." >&2
echo "" >&2
echo "   See references/api-contracts.md for the full pre-flight checklist." >&2
