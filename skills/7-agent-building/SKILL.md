---
name: agent-building
description: Builds, debugs, improves and tests DevRev AI agents in Agent Studio, covering prompting, retrieval strategy (FetchObjectContext, HybridSearch, NL2SQL), skills configuration, guardrails and knowledge sync. Use for "configure the agent", "add a skill to the agent", "test the agent guardrails", "why is the agent answering wrong". Not for authoring the workflow that an agent-callable skill wraps (use 6-workflows).
---

# DevRev Agent Building Toolkit

Expert toolkit for working with DevRev Agent Studio: build, debug, improve, and test AI agents with comprehensive knowledge base support.

## Overview

This skill provides access to DevRev's AI Agent Guides knowledge base and expert workflows for:
- **Syncing** the latest agent documentation
- **Creating** new agents with best practices
- **Debugging** agent issues systematically
- **Improving** existing agents
- **Testing** agents comprehensively
- **Configuring** guardrails and feature flags

## API Tokens Setup

Configure tokens in `.env` at the repo root:

| Token | Purpose | API |
|-------|---------|-----|
| `DEVREV_PAT` | Knowledge base sync (public API) + NL2SQL annotations | `api.devrev.ai` |
| `ORG_PAT` | Agent configs, workflows, sessions (internal API) — optional | `api.devrev.ai/internal` |

**Env & auth**: `DEVREV_PAT` from repo-root `.env` (public API: knowledge sync, annotations). `ORG_PAT` optional in `.env` (internal API: agent configs/guardrails) — if a command needs `ORG_PAT` and it's absent, tell the user and stop.

Example `.env`:
```bash
DEVREV_PAT=your-personal-access-token
ORG_PAT=your-org-access-token
```

**Network access**: calls to DevRev need to reach `api.devrev.ai`. If a call fails with curl exit code 56 or a connection error, a sandbox or network policy is probably blocking the domain. Tell the user to allow `api.devrev.ai` in Claude Code's sandbox network settings (or approve running the command outside the sandbox) instead of retrying.

## Core Principles

When working with DevRev agents, follow these principles from the guides:

1. **Deterministic first** — If it can be a workflow, make it a workflow. Use AI only where it adds value.
2. **FetchObjectContext > Search** — If you have an object ID, fetch it directly. Search is for discovery. **Caveat (live 2026-09-09):** it caps every long text field at 2,000 characters (`is_truncated: true` / `[truncated to 2000 characters]`) — use it for structure and short fields; read long text through `ExecuteSQL` (project `length(field)` to prove completeness) or a direct API read. See `references/toolkit-guide.md` § Naming retrieval.
3. **Minimal knowledge sources** — Fewer sources = less noise = better results.
4. **Task Success before Accuracy** — Fix whether the problem is solved before fixing whether the info is correct.
5. **Test before publish** — Always run bulk tests before going live.
6. **Start simple** — Begin with Tool Use pattern. Add complexity only when the simple pattern fails.
7. **Narrow the search space** — Scope searches (directory → articles) before evaluating results.
8. **NL2SQL requires annotations** — Schema annotations are not optional.

## Workflows

Each workflow has a command file with the step-by-step procedure; the long-form text is in `references/agent-workflows.md`.

| Goal | Open |
| --- | --- |
| Sync the AI Agent Guide knowledge base into `knowledge/` | `commands/agent-sync.md` |
| Create a new agent | `commands/agent-create.md` |
| Debug an agent | `commands/agent-debug.md` |
| Improve an agent | `commands/agent-improve.md` |
| Create and run a test set | `commands/agent-test.md` |
| Answer questions about agents | `commands/agent-ask.md` |
| Fix broken NL2SQL annotations (6-phase workflow) | `references/nl2sql-annotation-workflow.md` |
| Check a payload before calling the API (create vs update schemas, flat guardrails, string trigger ids) | `references/api-contract-quickref.md` |

## Guardrails Configuration

Guardrails restrict agents to specific topics. See [references/guardrails-api.md](references/guardrails-api.md) for full schema and API examples.

Key fields (write/create/update — **flat format**):
- `type`: `"topic_boundary"` or `"none"`
- `applies_to`: `["input"]`, `["output"]`, or both
- `enabled`: boolean
- `default_message`: shown when guardrail triggers
- `topic_name`: topic name (**flat**, not nested under `topic_boundary`)
- `description`: what's allowed (**flat**, not nested under `topic_boundary`)

> ⚠️ The GET response nests `topic_name`/`description` under `topic_boundary`. The write API requires them **flat**. See [references/api-contracts.md](references/api-contracts.md) Issue #4.

## Feature Flags

See [references/feature-flags.md](references/feature-flags.md) for archon-policy feature flag reference.

Key flags:
- `neuron.override_model_name_provider_map` — model overrides
- `neuron.agent_guardrails_enabled` — guardrails active/inactive
- `neuron.max_allowed_thinking_tokens` — thinking enabled/disabled
- `synapse.disable_ai_assistant_worker` — agent worker status

## API Safety

When changing agents via API:

1. **Ask before any mutating call** — No POST to internal create/update/delete/deploy/execute endpoints without explicit user approval
2. **Ground requests in api-specs** — Use `devrev/api-specs` repo, `specs/next/openapi-internal.yaml` for `/internal/ai-agents.*`
3. **Persist drafts first** — Write proposed JSON/diff to file, then call API after approval
4. **Validate before calling** — Use `create-agent.sh check` on every payload before sending

See [references/api-specs-and-api-safety.md](references/api-specs-and-api-safety.md) and [references/api-contracts.md](references/api-contracts.md) for details.

## Key Case Study: a customer support agent

The fix wasn't a better search algorithm — it was better search architecture:
- ❌ Flat search across entire KB + 2 tools with ambiguous handoff + 1,500-word prompt
- ✅ Two-stage scoped search (directory → articles) + 1 tool used in sequence + 250-word prompt

See `knowledge/ART-30502.txt` for full case study.

## Retrieval Naming Convention

Always name the underlying mechanism in agent designs:

- **FetchObjectContext** — When concrete object ID is available
- **HybridSearch** — For scoped search over configured knowledge
- **NL2SQL** — For structured data queries (only when annotations exist)

User-friendly skill names are fine, but document the mechanism for debugging.

## Scripts Reference

All scripts are in `scripts/` directory:

- `sync-knowledge.sh` — Sync KB articles from DevRev (uses DEVREV_PAT)
- `get-agent.sh` — Fetch agent config + skill workflows + org agent list (uses ORG_PAT)
- `create-agent.sh` — Create/update/delete agents with payload validation (uses ORG_PAT):
  - `create <file>` — Validate then create
  - `update <file>` — Validate then update
  - `convert <agent.json> [out]` — Transform GET response to valid update payload (strips null guidance, flattens guardrails, converts trigger objects to IDs)
  - `check <file> [mode]` — Client-side validation without API call
  - `delete <agent-id>` — Delete agent (3 second abort window; accepts DON ID or display_id)
- `check-annotations.sh` — Check NL2SQL schema annotations (uses DEVREV_PAT)
- `fetch-article-content.sh` — Robust article content extraction with fallback strategy (uses ORG_PAT)
- `validate-schema.sh` — List/describe/validate custom object schemas (uses ORG_PAT):
  - `list` — Show all custom object types in org
  - `describe <type>` — Show schema fields for a type
  - `check <type> <payload>` — Validate payload against schema

## Verified API Facts (Live-Tested 2026-06-01)

| Endpoint | Key behavior |
|---|---|
| `ai-agents.list` | Limit 1–99; empty body OK; strict on unknown fields |
| `ai-agents.get` | Accepts DON ID **or** `display_id` (ai_agent-N) in `id` field |
| `ai-agents.create` | Only `goal` is required; `name` is optional (auto-assigned) |
| `ai-agents.update` | Accepts DON ID or display_id; partial update preserves untouched fields |
| `ai-agents.delete` | `{ "id": "<don-id or display_id>" }` → `{}` on success |
| `ai-agents.versions.list` | Filter field: `"agent"` (not `"agent_id"`); filter required; response: `agent_versions` |
| `ai-agents.versions.get` | Use version DON ID from `default_version_id.id`; response: `agent_version` |
| `ai-agents-plans.get/list` | Hyphenated (not `ai-agents.plans.*`, which 404s) — **corrected 2026-07-19: these work**, `/internal/`-only, `id` must be an `ai_agent_plan` DON. Returns real system plans including `guidance` runbook text. |

## When to Use This Skill

Use this skill when:
- Building a new DevRev agent
- Debugging an existing agent
- Improving agent performance
- Creating test sets for agents
- Configuring guardrails or feature flags
- Questions about DevRev Agent Studio
- Working with NL2SQL and schema annotations
- Implementing retrieval strategies

## Additional Resources

- [API Contracts Reference](references/api-contracts.md) — Comprehensive API schema details and pitfalls
- [Troubleshooting Guide](references/troubleshooting.md) — Common issues and solutions from real-world usage
- [Guardrails API Reference](references/guardrails-api.md)
- [Feature Flags Reference](references/feature-flags.md)
- [API Specs and Safety](references/api-specs-and-api-safety.md)

---

## Troubleshooting Quick Reference

**Network errors (curl exit code 56 or connection failures):**
- A sandbox or network policy is probably blocking `api.devrev.ai`. Ask the user to allow the domain (or approve running outside the sandbox) rather than retrying.

**Article content extraction issues:**
- Use `scripts/fetch-article-content.sh <article_id> output.txt` for robust extraction
- Handles `published_version`, `extracted_content`, and `resource.artifacts` with fallback

**Custom object schema validation:**
- Use `scripts/validate-schema.sh list` to see all types
- Use `scripts/validate-schema.sh describe <type>` to inspect fields
- Use `scripts/validate-schema.sh check <type> payload.json` to validate payloads

**For detailed troubleshooting, see `references/troubleshooting.md`**

## Capturing new learnings

`references/api-contracts.md` is this domain's designated live-verified contract file — when a real
API call reveals a schema difference, restriction, or new behavior, add a dated entry there (and fix
any wrong claim in place). Guardrails/feature-flag discoveries go in `references/guardrails-api.md`
/ `references/feature-flags.md`. Then append a row to `${CLAUDE_PLUGIN_ROOT}/docs/LEARNINGS.md` and commit — full
protocol: `.claude/skills/capture-learnings/SKILL.md`.
