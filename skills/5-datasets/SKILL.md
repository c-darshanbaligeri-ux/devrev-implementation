---
name: datasets
description: Use this skill when the user asks to "create a custom dataset", "Oasis dataset", "Ponos job", "PaaS job", "BigQuery dataset", "dataset schema", or otherwise wants to create, update, or manage custom datasets in DevRev for analytics dashboards. Routes to the correct dataset-builder plugin commands rather than duplicating their logic.
---

# DevRev Custom Datasets

This skill routes dataset requests to the installed `dataset-builder` Claude Code plugin (marketplace `devrev-aai-plugins`, registered in `.claude/settings.json` with GitHub source `devrev/aai-skills`; the clone at `repos/aai-skills` is the same code, kept for reading/grounding). The actual domain knowledge (Oasis platform APIs, BigQuery schemas, Ponos YAML structure, PaaS job execution) lives in the plugin's own skills at `repos/aai-skills/plugins/dataset-builder/skills/` — this file only routes and states the decision rules.

## Routing

| User wants to... | Do this |
|---|---|
| Set up prerequisites (first-time or troubleshoot) | `/dataset-builder:setup` — checks tools and auth |
| Discover what datasets already exist | `/dataset-builder:explore` — lists Oasis datasets, queries BigQuery schemas |
| Create a new custom dataset | `:explore` (verify nothing suitable exists) → `:create` (guided PaaS or Ponos flow) |
| Update an existing dataset or job | `/dataset-builder:update` |
| Delete a dataset or job | `/dataset-builder:delete` |
| Test a Ponos job locally | `/dataset-builder:test` |
| Validate a Ponos job YAML before commit | `/dataset-builder:validate` |
| Understand Oasis concepts (dim vs fact, partitioning) | Read the `dataset-concepts` skill at `repos/aai-skills/plugins/dataset-builder/skills/dataset-concepts/SKILL.md` |

## PaaS vs Ponos decision table

**Decision rule: PaaS for most cases; Ponos only for stock/shared cross-org datasets.**

| Aspect | Ponos | PaaS |
|--------|-------|------|
| **Scope** | Cross-org (all orgs) | Org-specific |
| **Setup** | YAML in ponos repo + PR | API calls |
| **Scheduling** | Built-in via YAML | Workflow Builder |
| **Use Case** | Stock datasets, metrics | Custom org analytics |
| **Complexity** | Higher | Lower |

**When to use PaaS:**
- Most cases — easier setup, pure API calls
- Org-specific analytics needs
- No need for cross-org shared data

**When to use Ponos:**
- Stock/shared datasets that every org needs
- Cross-org metrics or platform-wide analytics
- You have approval to commit YAML to the internal ponos repo

## Preconditions

Check these before routing to dataset commands:

### For PaaS (most cases):
1. **`.env` with `DEVREV_PAT`**: Must exist in the workspace root. If missing, tell the user to create from `.env.example` and STOP — never fabricate a token.
2. **Environment auto-detected**: The plugin decodes the PAT JWT to detect dev/qa/prod environment automatically — never ask the user.

### For Ponos path additionally:
1. **`gcloud` and `bq` CLI**: For querying BigQuery schemas and testing. NOT auto-installed (needs interactive `gcloud auth login`).
2. **AWS CLI**: For role assumption during testing. NOT auto-installed (needs AWS SSO setup).
3. **`kubectl`**: For port-forwarding services during integration tests. NOT auto-installed.

If the user chooses Ponos, run `/dataset-builder:setup` to detect and walk through the additional tool setup — prompt only when they choose that path. Do NOT pre-emptively install or configure Ponos tools for users who only need PaaS.

## Known gotchas

From the plugin's CLAUDE.md:

- **Dataset `title` is REQUIRED**: The `oasis.dataset.create` API requires both `name` (identifier) and `title` (human-readable).
- **Partition columns must be TIMESTAMP-typed**: Use `"sql": {"type": "TIMESTAMP"}` and `"devrev_field_type": "timestamp"` (not DATE).
- **No `dim_` or `fact_` name prefixes**: Those are reserved for stock datasets in BigQuery. Custom dataset names should NOT use those prefixes.
- **Custom datasets start zero-access**: After creation, grant access to roles/users.
- **PaaS query syntax differs from Ponos**: PaaS uses table names only (`FROM \`fact_ticket\``), `@param` syntax, and auto-scopes to the calling org; Ponos uses Go templates (`{{.variable}}`), three-part table names, and manual `dev_oid` filtering.

## Safety

Destructive operations require explicit confirmation:

- **Dataset delete** (`oasis.dataset.delete`): Irreversible — confirm with the user before executing.
- **Job delete** (`serengeti.jobs.delete`): Cannot be undone — confirm first.

State the impact clearly and get explicit user confirmation before running these operations.

## Why this indirection

The actual domain knowledge lives in `repos/aai-skills/plugins/dataset-builder/skills/`. This file intentionally does not duplicate that content — it only routes and states the decision rules. Read the target skill's SKILL.md or command file for the real implementation details.

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- **2026-07-18 · Raw dataset endpoints are plugin-internal — no direct REST access at `/internal/datasets.*`.** Verified live: `POST /internal/datasets.list`, `/internal/sources.list`, `/internal/datasets.summary` all return HTTP 404. The `dataset-builder` plugin talks to serengeti / Oasis endpoints under different paths that this repo does not document. If a user tries to hand-roll dataset REST calls, redirect them to `/dataset-builder:*` commands.
- **2026-07-18 · Ponos tools verified missing.** On a clean install: `gcloud`, `bq`, `kubectl` all absent (only `aws` was present + SSO-authenticated). Matches the design — Ponos tools require interactive login and are deliberately NOT auto-installed. `/dataset-builder:setup` correctly prompts for them; PaaS path continues to work without them.
