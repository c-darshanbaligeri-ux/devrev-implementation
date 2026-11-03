# 04 — Maintenance

## Updating the cloned toolchain repos

The clones under `repos/` are **never updated automatically** — not on session start, not on a
schedule. They refresh only when you explicitly ask:

> "update the repos" / "pull latest" / "sync repos to main" / "refresh the cloned repos"

or run the script directly:

```bash
bash .claude/skills/update-repos/update_repos.sh
```

Per repo listed in `repos.txt`, the script:
1. Clones it (shallow) if missing — idempotent.
2. **Skips and reports** any repo with uncommitted local changes — it never discards work.
3. Otherwise detects the real default branch from `origin/HEAD` (not hardcoded `main`), fetches,
   and fast-forwards (`git checkout <default> && git reset --hard origin/<default>`).
4. Prints a summary table: repo | status | old SHA → new SHA.

**After `repos/aai-skills` updates**: the `dashboard-dev`/`dataset-builder` plugins come from that
repo, so restart Claude Code or run `/plugin marketplace update devrev-aai-plugins` to pick up new
commands, skills, or agents.

**After `repos/devrev-qk-agents` updates**: the `devrev` plugin (skill 9's snap-in pipeline) comes
from that repo. Restart Claude Code or run `/plugin marketplace update devrev-qk-agents`. Any
learnings captured via `/devrev:improve-skill` **inside that clone** get overwritten by the update —
so those must have already been mirrored into `skills/9-snapin-development/SKILL.md`'s Field notes
(the skill's playbook enforces this).

## Adding a new toolchain repo

Add its URL as a line in `repos.txt` (comments start with `#`), then run the update-repos skill.
Update the curated `docs/CLONE_RESULTS.md` if the change is durable (this file is the build-time
snapshot); the per-machine `docs/CLONE_RESULTS.local.md` is written by the bootstrap hook and is
gitignored. If a repo turns out to be inaccessible, mark it "NOT VERIFIED — repo not accessible"
rather than guessing its contents.

## Refreshing agent-building knowledge

The ten Agent Studio knowledge articles under `skills/7-agent-building/knowledge/` are synced copies
of DevRev's AI Agent Guide. To refresh them:

```bash
bash skills/7-agent-building/scripts/sync-knowledge.sh   # needs DEVREV_PAT in .env
```

This re-downloads all articles and rewrites `knowledge/INDEX.md` with the sync timestamp.

## The self-learning protocol (automatic)

The repo updates **itself** as it's used. Whenever the agent hits an unexpected error, a
permission/scope restriction, an API behavior that differs from the references, an undocumented
endpoint/field/limit, or receives a correction from you, it follows
`.claude/skills/capture-learnings/SKILL.md` immediately, mid-task:

1. **Verifies** the fact (real request/response or your explicit statement — never a guess).
2. **Updates the specific owning file** — a routing table maps each kind of learning to its exact
   target: the wrong passage in an API reference doc is fixed in place, new domain facts land in
   that skill's "Field notes" section, new import-failure causes join the workflow debugging
   checklist, Agent Studio contract discoveries go in `api-contracts.md`, bootstrap issues update
   the README troubleshooting table, misroutes add trigger phrases to the router. CLAUDE.md is only
   touched for truly global rules.
3. **Appends a row to `docs/LEARNINGS.md`** (the append-only journal — the audit trail of everything
   the repo has learned) and commits with a `learn:` message.

You can also trigger it explicitly: "remember this so we don't hit it again."

## The workflow learning loop

A specialization of the same idea: when a workflow template you asked for **imports successfully and
works**, tell the agent — it promotes the template into
`skills/6-workflows/examples/working-<name>.json` and adds it to the example index. Later requests
start from a confirmed-working template instead of regenerating from scratch.

## Credential rotation

When your PAT expires or rotates: edit `.env`, replace `DEVREV_PAT` (and `ORG_PAT` if set), start a
new session. Nothing else references the token — the MCP config, plugins, CLI, and scripts all read
it from `.env` (directly or via interpolation/aliasing).

## Keeping the repo itself current

The repo is a normal git repo with `main` pushed to the private GitHub remote. Commit and push your
own changes (new working examples, SKILL.md improvements, promoted templates) as you would any repo.
`.gitignore` already excludes everything machine-generated or secret: `.env`, `repos/*/` contents,
`logs/`, `config.yaml`, `.claude/.auto-setup/`, and the workspace output dirs (`dashboards/`,
`datasets/`, `plans/`, `templates/`).

## Session hygiene notes

- `.claude/.auto-setup/` holds the bootstrap's lock files, `install.log`, and the `init.done` marker.
  Deleting the folder is safe — the next session start simply re-verifies (and re-runs anything
  actually missing).
- The bootstrap hook is fully idempotent: with everything installed, it exits instantly at session
  start.
