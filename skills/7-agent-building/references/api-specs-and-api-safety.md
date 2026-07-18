# DevRev API specs (agents) and safe change workflow

Use this when designing or applying **API** changes to AI agents (not UI-only edits).

## Where the contracts live

Clone **`https://github.com/devrev/api-specs`** and set:

- **`DEVREV_API_SPECS`** (recommended) to the repo root, e.g. `~/dev/devrev/api-specs`, or
- Open the same paths under your normal DevRev checkout.

Primary file for **internal** agent endpoints:

| File | Use |
|------|-----|
| `specs/next/openapi-internal.yaml` | `/internal/...` routes, request/response `$ref`s for ai-agents |

Public surface (if applicable) is under `specs/next/openapi-public*.yaml` — prefer **internal** for Agent Studio operations that match `get-agent.sh` / org tooling.

### How to navigate quickly

From **`$DEVREV_API_SPECS`** (repo root):

```bash
# List internal ai-agent path entries (paths are authoritative)
rg '^  /internal/ai-agents' specs/next/openapi-internal.yaml

# Jump to a path block, e.g. update
rg -n '/internal/ai-agents\.update:' specs/next/openapi-internal.yaml
```

Resolve **`$ref:`** in the same YAML (`#/components/schemas/...`) for request bodies (e.g. `ai-agents-update-request`).

## Internal routes (mutating vs read)

**Treat anything that creates, updates, deletes, deploys, or executes as mutating** — require **explicit user approval** before calling (see below).

Representative **`/internal`** routes under **`openapi-internal.yaml`** (non-exhaustive; re-scan file for additions):

| Risk | Route prefix / path |
|------|---------------------|
| **Mutate** | `/internal/ai-agents.create`, `.update`, `.delete`, `.deploy` |
| **Mutate** | `/internal/ai-agents.versions.create`, `.update`, `.delete`, `.update-state` |
| **Mutate** | `/internal/ai-agents.skill-config-overrides.create`, `.update`, `.delete` |
| **Mutate** | `/internal/ai-agents.skills.create`, `.update` |
| **Mutate** | `/internal/ai-agents-plans.create`, `.update`, `.delete` |
| **Mutate** | `/internal/ai-agents.events.execute-async`, `.execute-sync` |
| **Mutate** | `/internal/ai-agents.callback` (if used) |
| **Usually read** | `/internal/ai-agents.get`, `.list`, `.configs.list` |
| **Usually read** | `/internal/ai-agents.versions.get`, `.list` |

Workflows (skills) often have separate paths — search `workflows` / `openapi-internal.yaml` for the workflow IDs you touch.

## Rules: permission before API runs

1. **No silent mutations** — Do not `curl` / SDK **POST** internal mutating endpoints without the user **explicitly approving** the exact operation in this session (endpoint name + agent/version id + summary of body or field diff).
2. **Prefer read-first** — Use **`./scripts/get-agent.sh`** (or `ai-agents.get` / `ai-agents.versions.get` per spec) to snapshot current config before proposing changes.
3. **Persist proposals locally** — Before any mutate call, write the **proposed** JSON (or unified diff) to a file under the user’s project or `/tmp` (e.g. `agent-update.proposed.json`) and show it. After approval, run the API once.
4. **Redact secrets** — Never paste `ORG_PAT` / tokens into summaries; use env vars only.
5. **Versioning** — Agent changes often go through **agent** vs **agent version** resources; follow the spec for `ai-agents.update` vs `ai-agents.versions.*` and your org’s release process (`deploy` if applicable).

## Rules: persisting outcomes

After a successful mutate (only after user approval):

1. Save the **API response** (or a fresh `get`) as **`agent-snapshot-<date>.json`** in the repo or task folder when the user wants history.
2. Note **which route** was used and **agent / version ids** in the commit message or a short `CHANGELOG-agent.md` if the team tracks agent drift.

## Cross-references

- **`references/api-contracts.md`** — Comprehensive API schema details, pitfalls, and pre-flight checklists.
- **`references/guardrails-api.md`** — Guardrail fields on create/update payloads (aligns with schemas in `openapi-internal.yaml`).
- **`references/troubleshooting.md`** — Common issues and solutions from real-world usage.
- **`scripts/get-agent.sh`** — Read path for config + workflows without hand-rolling every call.
- **`scripts/create-agent.sh`** — Create/update/delete agents with payload validation.
- **`CLAUDE.md`** (section *Naming retrieval in agent designs*) — **FetchObjectContext** vs **HybridSearch** in agent writeups; applies across `/agent-create`, `/agent-debug`, `/agent-test`, `/agent-ask`.
