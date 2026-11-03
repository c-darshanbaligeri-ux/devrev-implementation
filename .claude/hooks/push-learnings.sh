#!/usr/bin/env bash
# PostToolUse hook (matcher: Bash) — after every shell command, check whether
# HEAD is a not-yet-pushed `learn:` commit (the capture-learnings protocol's
# commit convention). If so, run guardrails against its diff and push to
# origin/main only if all of them pass. Fires deterministically right when
# the commit happens, unlike a Stop hook (which depends on a turn boundary
# that a long/interrupted session may never reach).
#
# `git push` sends EVERY unpushed commit, so every guardrail looks at the whole
# range origin/main..HEAD, not just HEAD. It only acts on branch `main`.
# Guardrails (all must pass, or the commits stay local and this prints why):
#   1. Fast-forward check — origin/main hasn't diverged; never force-push.
#   2. Only learn: commits — an unreviewed fix:/feat:/docs: commit must not ride
#      along with a learning.
#   3. Secret scan — no PAT/token/API-key-shaped strings in the added lines.
#   4. Scope check — every changed file is inside the knowledge-base surface:
#      skills/**, docs/**, index/**, .claude/skills/**, CLAUDE.md, README.md.
#      The guard itself (.claude/hooks, .claude/settings.json), scripts, bin,
#      hooks and tests are NOT auto-pushable: changes to them need a review.
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

# Only auto-push from main: a learn: commit on another branch is not ours to publish.
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
[[ "$BRANCH" == "main" ]] || exit 0

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

RANGE="$UPSTREAM_SHA..$HEAD_SHA"

# block "<stderr text>" "<short message for the session>" — record, report, stop.
block() {
    echo "push-learnings: BLOCKED — $1" >&2
    touch "$MARKER_FILE" 2>/dev/null
    jq -n --arg m "push-learnings: blocked an auto-push — $2 The commits stay local; see stderr." '{systemMessage: $m}' 2>/dev/null
    exit 0
}

# --- Guardrail 1: fast-forward check -----------------------------------------
MERGE_BASE="$(git merge-base HEAD origin/main 2>/dev/null)"
if [[ "$MERGE_BASE" != "$UPSTREAM_SHA" ]]; then
    block "origin/main has diverged (merge-base != origin/main). Not force-pushing. Resolve manually (pull/rebase) then push yourself." "origin/main has diverged."
fi

# --- Guardrail 2: only learn: commits ----------------------------------------
NON_LEARN="$(git log --format='%h %s' "$RANGE" 2>/dev/null | grep -v ' learn:')"
if [[ -n "$NON_LEARN" ]]; then
    block "these unpushed commits are not learn: commits and would be pushed with this one (review and push them yourself):
$NON_LEARN" "unpushed commits that are not learn: commits are waiting."
fi

# --- Guardrail 3: secret scan (added lines of the whole range) ----------------
SECRET_PATTERN='eyJ[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|DEVREV_PAT[[:space:]]*=[[:space:]]*[^<[:space:]]|[Aa]pi[_-]?[Kk]ey[[:space:]]*[:=][[:space:]]*[A-Za-z0-9]{16,}'
if git diff --unified=0 "$UPSTREAM_SHA" "$HEAD_SHA" 2>/dev/null | grep -E '^\+' | grep -vE '^\+\+\+' | grep -Eq "$SECRET_PATTERN"; then
    block "the added lines in $RANGE match a secret-shaped pattern. Fix the leak (redact to <REDACTED_PAT>, or drop the file) and commit a correction before this will push." "the diff matched a secret-shaped pattern."
fi

# --- Guardrail 4: file-scope check --------------------------------------------
OUT_OF_SCOPE=""
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    case "$f" in
        skills/*|docs/*|index/*|.claude/skills/*|CLAUDE.md|README.md) ;;
        *) OUT_OF_SCOPE="${OUT_OF_SCOPE}  ${f}\n" ;;
    esac
done <<< "$(git diff --name-only "$UPSTREAM_SHA" "$HEAD_SHA" 2>/dev/null)"
if [[ -n "$OUT_OF_SCOPE" ]]; then
    block "$(printf '%s touches file(s) outside the knowledge-base surface (skills/, docs/, index/, .claude/skills/, CLAUDE.md, README.md):\n%b' "$RANGE" "$OUT_OF_SCOPE")" "files outside the knowledge-base surface changed."
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
