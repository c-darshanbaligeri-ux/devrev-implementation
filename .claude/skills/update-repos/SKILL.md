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

If `repos/devrev-qk-agents` changed (skill 9's snap-in build pipeline), tell the user to restart
Claude Code or run `/plugin marketplace update devrev-qk-agents`. Also warn them that any
`/devrev:improve-skill` patches previously applied inside `repos/devrev-qk-agents/` are now gone —
verify `skills/9-snapin-development/SKILL.md`'s Field notes captured them (per the skill's
"Self-learning is plugin-scoped" section) before treating the refresh as complete.

If `repos/aai-custom-computer-capabilities` changed, that repo is the original source of
`skills/7-agent-building/` (agent-building toolkit) and the Computer snap-ins routed via `skills/9`.
Nothing auto-reloads — the destination is inline, not routed — but flag any meaningful upstream
change to the user so they can decide whether to re-diff `skills/7-agent-building/`'s inlined copy
against the fresh clone (see `docs/SUMMARY.md` § "Fixups Applied" for the original adaptations to
preserve when re-inlining).

If `repos/computer-skill` changed (community fork of DevRev Computer Skills — 10 sales-oriented
skills), no plugin/marketplace refresh is needed. It's grounding material only; useful to skim if
`skills/6-workflows` or `skills/0-solution-architecture` might borrow a pattern from
`create-workflow-template`, `deal-review-meddpicc`, or the sales-agent recipes.

## Non-git references (not touched by this skill)

The Google Doc "Agent Skills Marketplace"
(`https://docs.google.com/document/d/16NFkXnoY4c4xASkmoBfkG2uP32MInqlxzA2HOmUye2o/`) is a
provenance pointer only — it requires Google auth, isn't a git repo, and can't be synced by this
script. If the user asks to "update everything from source", clarify that this doc is manually
reviewed, not auto-refreshed.
