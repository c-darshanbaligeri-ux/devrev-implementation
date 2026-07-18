#!/usr/bin/env bash
# Update every repo listed in repos.txt to its upstream default branch.
# Clones anything missing first. Skips (does not discard) repos with local changes.
# Usage: bash .claude/skills/update-repos/update_repos.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
REPOS_FILE="$ROOT_DIR/repos.txt"
DEST_DIR="$ROOT_DIR/repos"

mkdir -p "$DEST_DIR"

declare -a SUMMARY

while IFS= read -r url; do
  [[ -z "$url" || "$url" =~ ^[[:space:]]*# ]] && continue

  name="$(basename "$url" .git)"
  target="$DEST_DIR/$name"

  if [[ ! -d "$target/.git" ]]; then
    echo "CLONE $url"
    if err="$(git clone --depth 1 "$url" "$target" 2>&1)"; then
      sha="$(git -C "$target" rev-parse --short HEAD 2>/dev/null || echo '?')"
      SUMMARY+=("$name | cloned | -> $sha")
      echo "  OK -> $target"
    else
      oneline="$(echo "$err" | tr '\n' ' ' | cut -c1-160)"
      SUMMARY+=("$name | CLONE FAILED | $oneline")
      echo "  FAIL: $oneline"
    fi
    continue
  fi

  echo "CHECK $name"

  if [[ -n "$(git -C "$target" status --porcelain 2>/dev/null)" ]]; then
    SUMMARY+=("$name | SKIPPED (uncommitted local changes) | -")
    echo "  SKIP: local changes present, not touching this repo"
    continue
  fi

  old_sha="$(git -C "$target" rev-parse --short HEAD 2>/dev/null || echo '?')"

  if ! git -C "$target" fetch --quiet origin 2>/tmp/update_repos_fetch_err; then
    err="$(tr '\n' ' ' < /tmp/update_repos_fetch_err | cut -c1-160)"
    SUMMARY+=("$name | FETCH FAILED | $err")
    echo "  FAIL: fetch error: $err"
    continue
  fi

  default_branch="$(git -C "$target" remote show origin 2>/dev/null | sed -n '/HEAD branch/s/.*: //p')"
  if [[ -z "$default_branch" ]]; then
    default_branch="main"
  fi

  if ! git -C "$target" checkout --quiet "$default_branch" 2>/tmp/update_repos_co_err; then
    err="$(tr '\n' ' ' < /tmp/update_repos_co_err | cut -c1-160)"
    SUMMARY+=("$name | CHECKOUT FAILED ($default_branch) | $err")
    echo "  FAIL: checkout $default_branch: $err"
    continue
  fi

  git -C "$target" reset --quiet --hard "origin/$default_branch"
  new_sha="$(git -C "$target" rev-parse --short HEAD 2>/dev/null || echo '?')"

  if [[ "$old_sha" == "$new_sha" ]]; then
    SUMMARY+=("$name | up to date ($default_branch) | $new_sha")
    echo "  OK: already up to date at $new_sha"
  else
    SUMMARY+=("$name | updated ($default_branch) | $old_sha -> $new_sha")
    echo "  OK: $old_sha -> $new_sha"
  fi
done < "$REPOS_FILE"

rm -f /tmp/update_repos_fetch_err /tmp/update_repos_co_err

echo ""
echo "== Summary =="
# ${SUMMARY[@]+...} guards bash 3.2's set -u against an empty array
printf '%s\n' ${SUMMARY[@]+"${SUMMARY[@]}"}
