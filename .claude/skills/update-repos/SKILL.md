---
name: update-repos
description: This skill should be used when the user asks to "update the repos", "pull latest", "sync repos to main", "refresh the cloned repos", "update everything to main branch", or otherwise wants the git repositories under repos/ brought up to date with their upstream default branch. Only runs on explicit user request — never automatically.
---

# Update Repos

Bring every repo under `repos/` up to date with its upstream default branch, and clone any
repo listed in `repos.txt` (repo root) that isn't present yet. This is an on-demand refresh — it
does not run automatically on session start. (The initial clone on a fresh machine is handled by
the bootstrap hook; this skill is for refreshing after that.)

## Usage

```bash
bash .claude/skills/update-repos/update_repos.sh
```

## What it does, per repo listed in `repos.txt`

1. Clones it into `repos/<name>` if missing (safe/idempotent, shallow).
2. If present: checks for uncommitted local changes. **If dirty, skips that repo and reports it**
   rather than discarding work — these are reference clones, but the script never assumes that.
3. If clean: detects the actual default branch from the remote (`origin/HEAD`, not a hardcoded
   `main`, in case a repo's default branch differs), fetches it, and fast-forwards
   (`git checkout <default-branch> && git reset --hard origin/<default-branch>`).
4. Prints a summary table (repo, old SHA → new SHA, status) at the end.

## After updating

If `repos/aai-skills` changed, the `dashboard-dev`/`dataset-builder` plugins come from that repo
(marketplace `devrev-aai-plugins`, registered in `.claude/settings.json`) — restart Claude Code or
run `/plugin marketplace update devrev-aai-plugins` so new commands/skills/agents load. Mention
this to the user after a successful `aai-skills` update.
