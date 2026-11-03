# DevRev toolkit: guide for Claude Code in this repository

This repo is a toolkit that Claude Code uses to operate DevRev organizations. A human gives a generic goal ("onboard Acme and open a ticket for them"); you find the right playbook and API here and finish the work. It is not a buildable software project.

## For any DevRev task

Read `skills/devrev-start/SKILL.md` and follow it: preflight, `./bin/devrev-find "<goal>"`, brief, act, verify. It carries the global API rules, the safety list, a goal map and troubleshooting. Never reconstruct API formats, payloads, scopes or JSON from memory.

## Layout

| Path | What it is |
| --- | --- |
| `skills/devrev-start/` | Entry skill: procedure, global API rules, safety list, goal map, troubleshooting |
| `skills/0-…` to `skills/11-…` | Domain playbooks. Skill 8 holds the API reference docs; skill 11 is a generated mirror of developer.devrev.ai |
| `bin/devrev-find`, `index/`, `scripts/`, `evals/`, `tests/` | The finder, its generated index, and the quality gate |
| `docs/LEARNINGS.md` | Append-only journal of live-verified corrections (the finder surfaces the relevant rows) |
| `.claude/` | Maintainer-only: settings and hooks, plus the `capture-learnings` and `update-repos` skills |
| `repos/` | Cloned upstream toolchains. Read-only: never edit anything under it |

## Rules for working in this repo

- **Paths.** `${CLAUDE_PLUGIN_ROOT}` in skill files means this repo's root when you work in a checkout; it is the install directory when the plugin is installed.
- **Self-learning is mandatory.** When you hit an error the docs did not predict, an undocumented restriction, endpoint, field or limit, or a user correction: verify it, fix the *owning* file, append one row to `docs/LEARNINGS.md` (append-only), and commit as `learn: <summary>`. A hook auto-pushes `learn:` commits after a secret scan and an allow-list check. Full protocol: `.claude/skills/capture-learnings/SKILL.md`. Never record secrets, real org ids, customer names or local paths.
- **Commit prefixes.** `learn:` is reserved for single learnings (it auto-pushes). Use `fix:`, `feat:`, `docs:` or `refactor:` for everything else; those never auto-push.
- **Regenerate and test.** After changing a skill, the mirror or the journal run `python3 -I scripts/build_index.py`; before committing run `python3 -m unittest discover -s tests`.
- **The mirror is generated.** `skills/11-developer-docs` comes from `scripts/fetch_docs.py` and `build_docs.py`. Never hand-edit it, and never write a learning into it: record the learning in the owning skill. Facts verified live here win over what the mirror says.
- **Updating `repos/`** happens only when the user explicitly asks ("update the repos"): use `.claude/skills/update-repos`.

## Bootstrap

With a `.env` (`DEVREV_PAT`, `DEVREV_ENDPOINT`; template in `.env.example`) a SessionStart hook (`.claude/hooks/bootstrap-workspace.sh`) creates the workspace directories (`dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/`), clones `repos.txt` into `repos/` (background, once), installs the `dashboard-sync` CLI with pipx (background, once) and runs `dashboard-sync init`. Progress is logged to `.claude/.auto-setup/install.log`. After the first install start a new session so PATH picks up `~/.local/bin`. Without a `.env` the hook only prints what to create: tell the user exactly what to put in it and stop, never fabricate a token. Ponos-only tools (`gcloud`/`bq`, AWS CLI with SSO, `kubectl`) are never auto-installed.

## Guardrails

- Never bypass the dashboard pipeline (skill 4) or hand-write widget JSON, and never use the third-party snap-in plugin's own "Implementation" vertical (skill 9).
- AI-agent-skill workflows start from `skills/6-workflows/examples/default-ai-agent-skill-template.json` (rules in skill 6); ask once if "workflow" is ambiguous.
- No unattended network installs beyond the bootstrap above.
- Never fabricate an API field, DON id, scope, JSON structure or file path; look it up or stop.
- Determinism first: reasoning produces plans, and scripts, templates and validators execute them. Failures must be loud.
