# commands/ — read-and-follow playbooks (NOT slash commands)

These eight files are **prompt playbooks**: when a request matches one (create/debug/improve/test an
agent, ask the guides, sync knowledge, configure feature flags or guardrails), open the file and
follow it as instructions, substituting the user's request for `$ARGUMENTS`. They are **not
registered as `/slash` commands** in this repo — references like `/agent-create` inside them mean
"the agent-create playbook in this folder".

All script paths run from **repo root**: `bash skills/7-agent-building/scripts/<name>.sh`.
Auth: `DEVREV_PAT` (repo-root `.env`) for public API; `ORG_PAT` (optional in `.env`) for internal
agent-config APIs — if missing, ask the user and stop.
