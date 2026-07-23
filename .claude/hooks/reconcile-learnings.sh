#!/usr/bin/env bash
# Stop hook — enforces that docs/LEARNINGS.md never carries unreconciled rows
# past a turn boundary. Rows appended below the RECONCILE-FROM-BELOW sentinel
# are newly-captured learnings that must be propagated into their owning
# skill/reference files (per .claude/skills/capture-learnings/SKILL.md,
# "End-of-session reconciliation") before the session is allowed to end.
#
# This script only detects pending rows and blocks the Stop event so the
# agent gets re-engaged to do the actual reconciliation (file edits,
# verification, row deletion, commit) — a shell script can't do that work
# itself. Caps at MAX_BLOCKS attempts per session so a stuck reconciliation
# can never hang a session indefinitely; past that it warns instead of
# blocking. Always exits 0 — a detection failure must never trap a session.

set +e

WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
LEARNINGS_FILE="$WORKSPACE_ROOT/docs/LEARNINGS.md"

# Drain stdin so the hook harness doesn't stall on an unread pipe.
INPUT_JSON="$(cat 2>/dev/null)"

[[ -f "$LEARNINGS_FILE" ]] || exit 0

if ! command -v jq >/dev/null 2>&1; then
    echo "reconcile-learnings: jq not found — skipping reconciliation check (fail-open)." >&2
    exit 0
fi

# Count table rows strictly after the sentinel row. The sentinel is matched
# only as the row's FIRST cell (anchored `| `RECONCILE-FROM-BELOW``) so prose
# mentioning the term elsewhere in the file (e.g. this doc's own header
# explaining the mechanism) can never be mistaken for the sentinel itself.
PENDING=$(awk '
  /^\| *`RECONCILE-FROM-BELOW`/ { seen=1; next }
  seen && $0 ~ /^\|/ { n++ }
  END { print n+0 }
' "$LEARNINGS_FILE")

if [[ "$PENDING" -eq 0 ]]; then
    exit 0
fi

SESSION_ID="$(echo "$INPUT_JSON" | jq -r '.session_id // "unknown"' 2>/dev/null)"
[[ -z "$SESSION_ID" || "$SESSION_ID" == "null" ]] && SESSION_ID="unknown"

STATE_DIR="$WORKSPACE_ROOT/.claude/.auto-setup"
mkdir -p "$STATE_DIR" 2>/dev/null
COUNT_FILE="$STATE_DIR/reconcile-block-count-${SESSION_ID}.txt"
COUNT=$(cat "$COUNT_FILE" 2>/dev/null || echo 0)
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNT_FILE" 2>/dev/null

MAX_BLOCKS=3
if [[ "$COUNT" -gt "$MAX_BLOCKS" ]]; then
    jq -n --arg msg "docs/LEARNINGS.md still has $PENDING unreconciled row(s) after $((COUNT - 1)) attempt(s) this session. Reconciliation was not completed — resolve manually or next session (see capture-learnings SKILL.md, 'End-of-session reconciliation')." \
       '{systemMessage: $msg}'
    exit 0
fi

REASON="docs/LEARNINGS.md has $PENDING row(s) below the RECONCILE-FROM-BELOW sentinel that have not been reconciled yet (attempt $COUNT of $MAX_BLOCKS). Before ending this turn: for each pending row, verify its fact is actually reflected in every file listed in its 'Files updated' column (fix or add it if not — the owning file is the permanent home for the fact, this journal is only staging), then delete that row from the table. If a row has no single owning file (a protocol-level or whole-repo synthesis finding), move it into the 'Standing notes' section instead of deleting it. Move the sentinel row back down so it sits immediately above the now-empty tail. Then git commit the result (commit only — do not push) per .claude/skills/capture-learnings/SKILL.md's 'End-of-session reconciliation' section."

jq -n --arg reason "$REASON" '{decision: "block", reason: $reason}'
exit 0
