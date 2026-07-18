# DevRev AI Agent Building Tools

You have access to a comprehensive knowledge base of DevRev AI Agent guides, synced from the DevRev knowledge base. Use these guides as the authoritative reference for any question about building, debugging, improving, or testing DevRev agents.

## Knowledge Base

> **Agent Studio is currently in beta for Dev0.** Some features (guardrails, advanced config) may only be configurable via API. See [Guardrails API](../commands/guardrails-api.md) and [Feature Flags](../commands/feature-flags.md) for details on configuring features not yet exposed in the UI.


The `../knowledge/` directory contains all articles from the **AI Agent Guides** directory (directory-257). Key articles:

| ID | Title | When to Read |
|----|-------|-------------|
| ART-27854 | AAI AI Agent Guide Directory | Overview of all guides |
| ART-27855 | 01 Prompting Guide | Writing goals, instructions, guardrails |
| ART-30501 | 02 Skills & Tools Guide | Configuring tools, workflows, input fields |
| ART-27857 | 03 Default Computer Memory | Knowledge graph limitations, curation needs |
| ART-30502 | 04 Retrieval Strategy | HybridSearch vs NL2SQL vs FetchObjectContext |
| ART-27859 | 05 Knowledge Configuration | Source selection, article optimization |
| ART-30503 | 06 Agent Design Patterns | Tool Use, ReAct, Plan-and-Execute, Multi-Agent |
| ART-27861 | 07 Testing & Evaluation | Playground, bulk tests, metrics, debugging |
| ART-27862 | 08 Agent Studio Quick Reference | UI reference, config fields |
| ART-27863 | 09 Full Agent Examples | Complete production configs |

After you run `/agent-sync`, check `../knowledge/INDEX.md` for the current list and sync time. If that file is missing, see `../knowledge/README.md`.

## Core Principles (from the guides)

1. **Deterministic first** — If it can be a workflow, make it a workflow. Use AI only where it adds value.
2. **FetchObjectContext > Search** — If you have an object ID, fetch it directly. Search is for discovery.
3. **Minimal knowledge sources** — Fewer sources = less noise = better results.
4. **Task Success before Accuracy** — Fix whether the problem is solved before fixing whether the info is correct.
5. **Test before publish** — Always run bulk tests before going live.
6. **Start simple** — Begin with Tool Use pattern. Add complexity only when the simple pattern fails.
7. **Narrow the search space** — Scope searches (directory → articles) before evaluating results.
8. **NL2SQL requires annotations** — Schema annotations are not optional. If an agent uses NL2SQL and the results are wrong or empty, always check annotations first (see below).

### Naming retrieval in agent designs (`/agent-create`, `/agent-improve`)

When you document skills or retrieval for a new or updated agent:

- **FetchObjectContext** — Always spell out how the agent will fetch by **object id** when the user provides one (ticket, user, article, etc.). This is separate from search.
- **HybridSearch** — If a skill is a friendly name (e.g. `search_docs`) but behavior is article/object search, **explicitly say it uses HybridSearch** (scoped per knowledge config). Friendly names are OK; hiding the mechanism is not.

## NL2SQL Annotation Rule

**Whenever an agent uses NL2SQL**, annotations must be checked before any other debugging or configuration work.

NL2SQL performance depends entirely on schema annotations. Without them, the model guesses at column meanings and generates broken SQL. This is the most common cause of NL2SQL failures.

### Step 1 — Run the Annotation Check

```bash
# Check annotation quality for a specific table
skills/7-agent-building/scripts/check-annotations.sh "<table-id>" /tmp/annotations

# List all available tables first (if you don't know the ID)
skills/7-agent-building/scripts/check-annotations.sh list
```

Requires `DEVREV_PAT` in `.env`. This will:
1. Clone `devrev/auto-annotations` (first run only) and set up `devrev.py`
2. Fetch the table schema and count annotated vs. unannotated columns
3. Flag placeholder/broken descriptions (<20 chars — too short for NL2SQL)
4. If annotations are broken: print exact instructions for running the fix workflow

### Step 2 — Fix with the auto-annotations Agent Workflow

If the check finds missing or broken annotations, run the **6-phase auto-annotations workflow**. This is an AI-agent-driven process — not a single CLI command. The tool is at `devrev/auto-annotations` and uses `devrev.py` for all API interactions.

**Auth**: Set `DEVREV_PAT` (not `ORG_PAT`) — this tool uses your DevRev personal access token.

**CLI commands available in devrev.py:**
```bash
./devrev.py tables-list               # List all data tables
./devrev.py table-schema <table-id>   # Get schema (columns, types, existing descriptions)
./devrev.py query "SELECT ..."        # Execute SQL against DevRev data
./devrev.py search "keyword"          # Search DevRev records
./devrev.py object-get <object-id>    # Get full context for a DevRev object
```

**SQL syntax rules** (required for `./devrev.py query`):
- Single-letter aliases: `FROM devrev.ticket as t`
- Parenthesize field refs: `(t).priority`, `(t).stage.stage_id`
- Arrays use UNNEST: `UNNEST((t).arr) as (a)`
- Always project the base `id` field
- Never project struct fields directly — use dot notation

**The 6-phase workflow** (follow in order, do not skip phases):

**Phase 1 — Schema-Only Analysis**
Run `./devrev.py tables-list` then `./devrev.py table-schema <id>`. Before querying, extract what the schema already tells you: enum lists, types, id_types (foreign keys), field name suffixes (`_c` = Salesforce custom, `_usd_c` = USD, `_date_c` = date). Cluster related fields by prefix (e.g., all `contract_*` fields). Flag ambiguous acronyms (e.g., PAS, TTV, VaaS) that can't be inferred from context.

**Phase 2 — Data Profiling**
Run standardized queries for every field. Limit to 3-4 concurrent queries at a time.
- NULL rate for all fields: `SELECT COUNT((t).id) as total, COUNT((t).{field}) as non_null FROM {table} as t`
- VARCHAR: distinct values + frequency (top 25)
- DOUBLE/INT: min, max, avg; check if 0 is a sentinel value
- DATE/TIMESTAMP: range (earliest, latest)

**Phase 3 — Conditional Profiling**
Determine *when and why* fields are populated — the most important phase.
- NULL co-occurrence within clusters (are related fields always NULL together?)
- Population conditioned on categorical fields (e.g., "only populated for Active accounts")
- Side-by-side comparison of similar-sounding fields to find the difference

**Phase 4 — Human Input (Batch)**
Collect *all* unresolvable ambiguities and surface them in a **single batch** — never drip-feed. Ask about: overlapping fields with differing values, business acronyms, ambiguous NULL semantics, contradictory data, enum inconsistencies, multiple fields mapping to the same user question.

**Phase 5 — Write Descriptions**
Write descriptions from the perspective of an LLM generating SQL, not a human reading docs. Cover:
- Semantic meaning in business terms
- When populated vs. NULL, and what NULL means
- Sentinel values (0 = zero or "not applicable"?)
- Field relationships and which field answers which user question
- Gotchas (enum spelling inconsistencies, unexpected patterns)

**Do NOT write absolute counts** — they go stale. Use proportions, qualitative sparsity, and structural observations instead:
- ❌ "Populated for ~1,520 accounts" → ✅ "Sparsely populated, mostly for Active accounts"
- ❌ "56,690 Prospects" → ✅ "~91% are Prospects"

**Phase 6 — Verification**
Generate 3-5 realistic natural language test questions. For each: write the SQL using your new descriptions, run it with `./devrev.py query`, sanity-check results against Phase 2 profiling. Revise descriptions if results look wrong.

**Output**: `{table}_field_descriptions.json` (field name → description mapping)

**Apply**: Agent Studio → Knowledge → Datasets → Edit Schema

### What Good Annotations Look Like

```
Column: priority
Description: Urgency level of the ticket. Use for questions about "priority" or
"severity". Values: p0 (critical/outage), p1 (high/data loss), p2 (medium/feature
broken), p3 (low/cosmetic). NULL means priority was never set. P0 and P1 trigger
automatic escalation. Set by the routing agent at ticket creation.
```

### When to Run the Annotation Check

- Agent uses NL2SQL and returns wrong, empty, or nonsensical results
- Configuring NL2SQL for an agent for the first time
- A new dataset or schema change is added to an existing NL2SQL agent
- Agent improvement analysis flags retrieval quality as a concern

## Key Case Study: PeopleStrong SupportGPT

The fix wasn't a better search algorithm — it was better search architecture:
- ❌ Flat search across entire KB + 2 tools with ambiguous handoff + 1,500-word prompt
- ✅ Two-stage scoped search (directory → articles) + 1 tool used in sequence + 250-word prompt

See ART-30502 for the full case study.


## Guardrails

Guardrails restrict agents to specific topics and are checked at input and/or output stages. Currently the only type is `topic_boundary`.

### How to Configure

**Via API** (recommended until UI exposes this):
- Guardrails are embedded in agent/version payloads — no standalone endpoints
- See `guardrails-api.md` (this folder) for full schema, examples, and update patterns

**Via Feature Flags** (neuron.rego):
- `agent_guardrails_enabled` — controls whether guardrails are active per org/agent
- `override_model_name_provider_map` with key `"agent_guardrails"` — override the model used for guardrail evaluation

### Schema Summary

| Field | Type | Description |
|---|---|---|
| `type` | `enum` | `"topic_boundary"` (only type today) or `"none"` (to remove) |
| `applies_to` | `array[enum]` | `["input"]`, `["output"]`, or `["input", "output"]` |
| `enabled` | `boolean` | Active or not |
| `default_message` | `string` | Shown to user when guardrail triggers |
| `topic_boundary.topic_name` | `string` | Topic name |
| `topic_boundary.description` | `string` | What's allowed within this topic |

Max 16 guardrails per agent on creation. Guardrails appear in both `ai-agent` and `ai-agent-version` payloads.

## API Access

Configure two tokens in the environment, in `~/.openclaw-autoclaw/.env` if you use that convention, or in `.env` beside the plugin (see `.env.example`):

| Token | Purpose | API |
|-------|---------|-----|
| `DEVREV_PAT` | Knowledge base articles (public API) + NL2SQL annotation tool (`devrev.py`) | `api.devrev.ai` |
| `ORG_PAT` | Agent configs, workflows, sessions (internal API) | `api.devrev.ai/internal` |

**Network Permissions Note**: All API calls to DevRev require `full_network` permissions. If you encounter "exit code 56" errors, ensure Shell commands include `required_permissions: ["full_network"]`.

### Scripts
- `sync-knowledge.sh` — Syncs all KB articles (uses `DEVREV_PAT`)
- `get-agent.sh` — Fetches agent config + all skill workflows (uses `ORG_PAT`)
- `check-annotations.sh` — Checks NL2SQL schema annotations; sets up `devrev/auto-annotations` fix workflow if broken (uses `DEVREV_PAT`)
- `create-agent.sh` — Create/update/delete agents with payload validation (uses `ORG_PAT`):
  - `create <file>` — Validate then create
  - `update <file>` — Validate then update
  - `convert <agent.json> [out]` — Transform GET response to valid update payload
  - `check <file> [mode]` — Client-side validation without API call
  - `delete <agent-id>` — Delete agent (3 second abort window)
- `fetch-article-content.sh` — Robust article content extraction with fallback strategy (uses `ORG_PAT`)
- `validate-schema.sh` — List/describe/validate custom object schemas (uses `ORG_PAT`):
  - `list` — Show all custom object types in org
  - `describe <type>` — Show schema fields for a type
  - `check <type> <payload>` — Validate payload against schema

If `ORG_PAT` is not set, agent/workflow operations will fail with a clear error message.

## API Safety, Contracts, and Persistence

When changing agents **via API** (not only advice):

1. **Ask before any mutating call** — No `POST` to internal create/update/delete/deploy/execute endpoints without **explicit user approval** in-session (endpoint + ids + what changes). See **`api-specs-and-api-safety.md`** (this folder).
2. **Ground requests in `api-specs`** — The spec repo is already cloned at **`repos/api-specs`** (repo root); use **`repos/api-specs/specs/next/openapi-internal.yaml`** for `/internal/ai-agents.*` request shapes and `$ref` schemas. (`DEVREV_API_SPECS` may point at it: `DEVREV_API_SPECS=repos/api-specs`.)
3. **Persist drafts first** — Write proposed JSON/diff to a file, then call the API after approval; save snapshots after successful changes if the user wants audit history.
4. **Validate before calling** — Use `../scripts/create-agent.sh check` (i.e. `skills/7-agent-building/scripts/create-agent.sh check` from repo root) on every payload before sending.

### API Contract Compliance

> **Always read `api-contracts.md` (this folder) before building any create/update payload.**

Key schema differences:
- **CREATE**: `guardrails` = plain array, `skills` = plain array, no `slug` field
- **UPDATE**: `guardrails` = `{"set": [...]}`, `skills` = `{"set": [...]}`, `id` required, no `slug`
- **BOTH**: `topic_name`/`description` must be FLAT in guardrails (not nested under `topic_boundary`); trigger fields must be STRING IDs, not objects

### Additional References
- [API Contracts](api-contracts.md) — Comprehensive API schema details and pitfalls
- [Troubleshooting Guide](troubleshooting.md) — Common issues and solutions from real-world usage
- [Guardrails API](guardrails-api.md) — Full guardrail schema and examples
- [Feature Flags](feature-flags.md) — archon-policy feature flag reference

## Command playbooks

These are **read-and-follow playbooks** in `../commands/` (not registered slash commands in this
repo — see `../commands/README.md`). Use `agent-sync.md` to refresh the knowledge base, then:
- `agent-debug.md <issue>` — Debug an agent problem
- `agent-create.md <requirements>` — Create a new agent
- `agent-improve.md <agent-id-or-config>` — Analyze and improve an existing agent
- `agent-test.md <agent-id-or-config>` — Create a comprehensive test set
- `agent-ask.md <question>` — Ask anything about DevRev agents
- `guardrails-api.md` — Guardrail configuration via API (schema, examples, feature flag control)
- `feature-flags.md` — archon-policy feature flag reference (model overrides, agent config, snap-in enablement)
