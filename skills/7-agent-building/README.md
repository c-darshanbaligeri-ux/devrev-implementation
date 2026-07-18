# skills/7-agent-building/ — map

Start with `SKILL.md` (workflows, principles, API contract compliance). This folder's parts:

| Dir | Contents | Use when |
| --- | --- | --- |
| `commands/` | 8 playbooks: `agent-create`, `agent-debug`, `agent-improve`, `agent-test`, `agent-ask`, `agent-sync`, `feature-flags`, `guardrails-api` | The user asks to create/debug/improve/test an agent, ask the guides, refresh knowledge, or configure flags/guardrails. These are **reference playbooks the agent reads and follows** — not registered slash commands |
| `knowledge/` | 10 synced Agent Studio guide articles (`ART-*.txt` + `INDEX.md`) — prompting, skills/tools, memory, retrieval strategy, knowledge curation, design patterns (incl. multi-agent routing), testing, quick reference, full examples | Designing or reviewing any agent. Refresh with `scripts/sync-knowledge.sh` |
| `references/` | `api-contracts.md` (live-verified schema differences — the designated file for new API learnings), `guardrails-api.md`, `feature-flags.md`, `api-specs-and-api-safety.md`, `troubleshooting.md`, `toolkit-guide.md` | Before ANY internal-API payload; when a call errors |
| `scripts/` | `get-agent.sh`, `create-agent.sh` (validating create/update/delete), `sync-knowledge.sh`, `check-annotations.sh` (NL2SQL), `fetch-article-content.sh`, `update-article.sh`, `validate-schema.sh` | Deterministic execution — prefer these over hand-rolled curl |

**Auth**: `DEVREV_PAT` (repo-root `.env`) for public API (knowledge sync, annotations);
`ORG_PAT` (optional in `.env`) for internal API (agent configs, guardrails). Scripts resolve `.env`
from the repo root. **Never** POST to a mutating internal endpoint without explicit user approval.

**Knowledge freshness**: before designing an agent from `knowledge/`, check the `Synced:` timestamp
in `knowledge/INDEX.md`; if it's more than a few days old, offer to refresh via
`bash skills/7-agent-building/scripts/sync-knowledge.sh` first. (The upstream plugin enforced this
with a session hook; here it's a manual check.)
