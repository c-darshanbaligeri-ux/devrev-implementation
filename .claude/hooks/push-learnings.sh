#!/usr/bin/env bash
# PostToolUse hook (matcher: Bash) — after every shell command, check whether
# HEAD is a not-yet-pushed `learn:` commit (the capture-learnings protocol's
# commit convention). If so, run guardrails against its diff and push to
# origin/main only if all of them pass. Fires deterministically right when
# the commit happens, unlike a Stop hook (which depends on a turn boundary
# that a long/interrupted session may never reach).
#
# Guardrails (all must pass, or the commit stays local and this prints why):
#   1. Secret scan — no PAT/token/API-key-shaped strings in the diff.
#   2. Scope check — every changed file matches an allow-listed path
#      (skills/**, docs/**, CLAUDE.md, rate limits.md, README.md, .claude/**,
#      plans/** for learning-related scripts/artifacts) — never a commit that
#      also touches something outside the knowledge-base surface.
#   3. Fast-forward check — origin/main hasn't diverged; never force-push.
#
# Always exits 0 — a hook failure must never block or fail the triggering
# Bash command itself.

set +e

WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$WORKSPACE_ROOT" 2>/dev/null || exit 0

# Drain stdin (PostToolUse hooks receive the tool-call JSON; we don't need it,
# but must read it so the harness doesn't stall on an unread pipe).
cat >/dev/null 2>&1

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

HEAD_SUBJECT="$(git log -1 --format=%s 2>/dev/null)"
case "$HEAD_SUBJECT" in
    learn:*) ;;
    *) exit 0 ;;
esac

# Only act once per commit: skip if this exact commit SHA was already handled
# (pushed, or already found guardrail-failing) in a prior hook firing.
STATE_DIR="$WORKSPACE_ROOT/.claude/.auto-setup"
mkdir -p "$STATE_DIR" 2>/dev/null
HEAD_SHA="$(git rev-parse HEAD 2>/dev/null)"
MARKER_FILE="$STATE_DIR/push-learnings-handled-${HEAD_SHA}.txt"
[[ -f "$MARKER_FILE" ]] && exit 0

# Nothing to push if this commit is already on origin/main.
git fetch origin main --quiet 2>/dev/null
UPSTREAM_SHA="$(git rev-parse origin/main 2>/dev/null)"
if [[ "$HEAD_SHA" == "$UPSTREAM_SHA" ]]; then
    touch "$MARKER_FILE" 2>/dev/null
    exit 0
fi

# --- Guardrail 1: secret scan -------------------------------------------------
DIFF="$(git show --unified=0 "$HEAD_SHA" 2>/dev/null)"
SECRET_PATTERN='eyJ[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|DEVREV_PAT[[:space:]]*=[[:space:]]*[^<[:space:]]|[Aa]pi[_-]?[Kk]ey[[:space:]]*[:=][[:space:]]*[A-Za-z0-9]{16,}'
if echo "$DIFF" | grep -Eq "$SECRET_PATTERN"; then
    echo "push-learnings: BLOCKED — commit $HEAD_SHA's diff matches a secret-shaped pattern. Not pushing. Fix the leak (redact to <REDACTED_PAT>, or drop the file) and commit a correction before this will push." >&2
    touch "$MARKER_FILE" 2>/dev/null
    jq -n '{systemMessage: "push-learnings: blocked a learn: commit from auto-push — its diff matched a secret-shaped pattern. Commit is local only; see stderr for detail."}' 2>/dev/null
    exit 0
fi

# --- Guardrail 2: file-scope check -------------------------------------------
CHANGED_FILES="$(git show --name-only --format='' "$HEAD_SHA" 2>/dev/null)"
OUT_OF_SCOPE=""
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    case "$f" in
        skills/*|docs/*|.claude/*|plans/*|CLAUDE.md|README.md|"rate limits.md"|documentation/*)
            ;;
        *)
            OUT_OF_SCOPE="${OUT_OF_SCOPE}${f}\n"
            ;;
    esac
done <<< "$CHANGED_FILES"

if [[ -n "$OUT_OF_SCOPE" ]]; then
    echo "push-learnings: BLOCKED — commit $HEAD_SHA touches file(s) outside the known knowledge-base surface, not pushing:" >&2
    echo -e "$OUT_OF_SCOPE" >&2
    touch "$MARKER_FILE" 2>/dev/null
    jq -n '{systemMessage: "push-learnings: blocked a learn: commit from auto-push — it touches file(s) outside skills/docs/.claude/plans/CLAUDE.md/README.md. Commit is local only."}' 2>/dev/null
    exit 0
fi

# --- Guardrail 3: fast-forward check -----------------------------------------
MERGE_BASE="$(git merge-base HEAD origin/main 2>/dev/null)"
if [[ "$MERGE_BASE" != "$UPSTREAM_SHA" ]]; then
    echo "push-learnings: BLOCKED — origin/main has diverged (merge-base != origin/main). Not force-pushing. Resolve manually (pull/rebase) then push yourself." >&2
    touch "$MARKER_FILE" 2>/dev/null
    jq -n '{systemMessage: "push-learnings: blocked a learn: commit from auto-push — origin/main has diverged. Resolve manually."}' 2>/dev/null
    exit 0
fi

# --- All guardrails passed: push ---------------------------------------------
PUSH_OUT="$(git push origin main 2>&1)"
PUSH_STATUS=$?
touch "$MARKER_FILE" 2>/dev/null

if [[ $PUSH_STATUS -eq 0 ]]; then
    echo "push-learnings: pushed $HEAD_SHA ('$HEAD_SUBJECT') to origin/main." >&2
    jq -n --arg sha "$HEAD_SHA" --arg subj "$HEAD_SUBJECT" \
        '{systemMessage: ("push-learnings: auto-pushed " + $sha[0:8] + " (\"" + $subj + "\") to origin/main.")}' 2>/dev/null
else
    echo "push-learnings: push FAILED for $HEAD_SHA: $PUSH_OUT" >&2
    jq -n '{systemMessage: "push-learnings: git push failed for a learn: commit — see stderr. Commit is local only, push it manually."}' 2>/dev/null
fi

exit 0
