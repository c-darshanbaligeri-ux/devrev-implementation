---
name: devrev-agent-toolkit
description: Build, debug, improve, and test DevRev AI agents using Agent Studio. Syncs AI Agent Guide knowledge base, provides expert guidance on agent prompting, retrieval strategies (FetchObjectContext, HybridSearch, NL2SQL), skills configuration, guardrails, and testing. Use when working with DevRev agents, Agent Studio, or when asked about agent debugging, creation, improvement, or testing.
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

**Network Permissions Note**: All API calls to DevRev require `full_network` permissions. If you encounter "exit code 56" errors, ensure Shell commands include `required_permissions: ["full_network"]`.

## Core Principles

When working with DevRev agents, follow these principles from the guides:

1. **Deterministic first** — If it can be a workflow, make it a workflow. Use AI only where it adds value.
2. **FetchObjectContext > Search** — If you have an object ID, fetch it directly. Search is for discovery.
3. **Minimal knowledge sources** — Fewer sources = less noise = better results.
4. **Task Success before Accuracy** — Fix whether the problem is solved before fixing whether the info is correct.
5. **Test before publish** — Always run bulk tests before going live.
6. **Start simple** — Begin with Tool Use pattern. Add complexity only when the simple pattern fails.
7. **Narrow the search space** — Scope searches (directory → articles) before evaluating results.
8. **NL2SQL requires annotations** — Schema annotations are not optional.

## Available Workflows

### 1. Sync Knowledge Base

Sync all AI Agent Guide articles from DevRev knowledge base to local files.

```bash
bash skills/7-agent-building/scripts/sync-knowledge.sh
```

After syncing, article files will be available in `knowledge/` directory with an `INDEX.md` overview.

### 2. Create a New Agent

When asked to create a DevRev agent:

1. **Read the knowledge base** from `knowledge/` directory:
   - `INDEX.md` — article overview
   - `ART-27855.txt` — Prompting Guide (goal, instructions, guardrails)
   - `ART-30501.txt` — Skills & Tools Guide (tools, workflows, input fields)
   - `ART-30502.txt` — Retrieval Strategy (FetchObjectContext, HybridSearch, NL2SQL)
   - `ART-27859.txt` — Knowledge Configuration (source selection, curation)
   - `ART-30503.txt` — Design Patterns (Tool Use, ReAct, Plan-and-Execute)
   - `ART-27863.txt` — Full Agent Examples (reference configs)

2. **Clarify requirements** if not fully specified:
   - Primary use case
   - Users (internal vs external/CX)
   - Data sources needed
   - Actions the agent should take
   - Existing workflows or snap-ins

3. **Design the agent** with:
   - **Goal** (1-2 sentences)
   - **Instructions** (Role & Persona, Scope, How to Respond, When to Use Skills, Escalation)
   - **Guardrails** (topic_boundary with description, applies_to, default_message)
   - **Knowledge Sources** (minimum viable set)
   - **Skills** — Name the underlying mechanism:
     - **FetchObjectContext** when object ID is available
     - **HybridSearch** for scoped knowledge discovery
     - **NL2SQL** only when configured for structured data
   - **Design Pattern** (Tool Use, ReAct, Plan-and-Execute, Multi-Agent)
   - **Retrieval Strategy** priority: FetchObjectContext → targeted tools → HybridSearch → NL2SQL

4. **Provide testing plan**:
   - 10-15 representative test inputs
   - Edge cases
   - Metrics to track (Task Success, Accuracy)

5. **Reference examples** from `ART-27863.txt`

### 3. Debug an Agent

When asked to debug an agent issue:

1. **Get agent identifier** — Request agent ID or slug if not provided

2. **Fetch agent config** (requires `ORG_PAT`):
```bash
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
```

3. **Read relevant guides** based on issue type:
   - Retrieval issues: `ART-27857.txt`, `ART-30502.txt`, `ART-27859.txt`
   - Prompting issues: `ART-27855.txt`
   - Skill/tool issues: `ART-30501.txt`
   - Design issues: `ART-30503.txt`
   - Testing issues: `ART-27861.txt`

4. **For NL2SQL agents** — Check annotations FIRST:
```bash
bash skills/7-agent-building/scripts/check-annotations.sh "<table-id>" /tmp/annotations
```

5. **Categorize the issue**:
   - Retrieval quality (wrong articles, missing info, noisy results)
   - Skill selection (wrong tool called, tools not triggered)
   - Prompting (agent ignores instructions, hallucinates, goes out of scope)
   - Response quality (tone, format, accuracy)
   - Latency (slow responses, timeout issues)
   - Architecture (wrong pattern, over-engineered workflow)
   - Guardrails (agent rejecting valid inputs, not blocking invalid inputs)
   - Feature flags (wrong model, guardrails disabled)

6. **Check retrieval strategy**:
   - Is FetchObjectContext used when user provides object ID?
   - Are search skills explicitly using HybridSearch?
   - Expected priority: FetchObjectContext → targeted tools → HybridSearch → NL2SQL

7. **Provide actionable fixes**:
   - What to change and where
   - Why it fixes the issue
   - How to verify the fix

### 4. Improve an Agent

When asked to improve an agent:

1. **Get agent identifier** — Request agent ID or slug if not provided

2. **Fetch current config** (requires `ORG_PAT`):
```bash
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
```

3. **Read all relevant guides** from `knowledge/`

4. **Analyze across dimensions**:
   - **Goal clarity** — Specific, scoped, actionable? (ART-27855 §1)
   - **Instructions quality** — Organized, minimal, no branching logic? (ART-27855 §2)
   - **Guidance text integrity** — Scan the raw `guidance` field for corruption before reusing or improving it:
     - `&nbsp;` HTML entities visible in text (should be stripped)
     - `═══...═══` decorative borders (replace with `---`)
     - `[S.No](http://S.No)` or similar markdown link artifacts (replace with plain text)
     - Rules that end abruptly mid-sentence or mid-list (truncated during copy-paste)
     - References to an "operator appendix" or external doc that doesn't exist in the guidance
     - If any are found, clean the guidance before analyzing or improving it
   - **Skill design** — Overlapping tools? Ambiguous handoffs? (ART-30501)
   - **Skill name/trigger coherence** — Does the skill name accurately reflect what it does?
     - A skill named `FetchObjectContext` that actually triggers a custom workflow (`trigger.workflow`) misleads debugging — rename it to describe the actual function (e.g. `FetchConversionRules`)
     - A skill named `RunPipeline` triggering a native operation is similarly misleading
   - **Knowledge configuration** — Too many sources? Wrong object types? (ART-27857, ART-27859)
   - **Retrieval strategy** — FetchObjectContext first? HybridSearch explicit? (ART-30502)
   - **NL2SQL annotations** — Check if broken:
     ```bash
     bash skills/7-agent-building/scripts/check-annotations.sh "<dataset-id>" /tmp/annotations
     ```
   - **Design pattern fit** — Right pattern? Over-engineered? (ART-30503)
   - **Guardrails** — Specific with trigger conditions? (ART-27855 §3)
   - **Feature flags** — Correctly configured in archon-policy?
   - **Testing coverage** — Test set exists? Metrics tracked? (ART-27861)

5. **Prioritize improvements**:
   - 🔴 Critical: Issues causing wrong answers or actions
   - 🟡 Important: Issues degrading quality or reliability
   - 🟢 Nice-to-have: Optimizations and polish

6. **Provide concrete changes** with:
   - What to change (specific text/config)
   - Where to change it (Agent Studio location or API)
   - Expected impact
   - How to verify (test case)

### 5. Create Test Set

When asked to create tests for an agent:

1. **Get agent identifier** — Request agent ID or slug if not provided

2. **Fetch agent config** (requires `ORG_PAT`):
```bash
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
```

3. **Read testing guides**:
   - `ART-27861.txt` — Testing & Evaluation Guide (PRIMARY)
   - `ART-27855.txt`, `ART-30501.txt`, `ART-30502.txt`, `ART-27863.txt`

4. **Analyze the agent**:
   - Goal and scope
   - Skills and trigger conditions (note FetchObjectContext vs HybridSearch vs NL2SQL)
   - Knowledge sources
   - Guardrails configuration
   - Response format expectations

5. **Design test categories**:

   **Happy Path Tests** (agent should succeed):
   - Core use cases
   - Each skill tested at least once
   - Each knowledge source queried
   - Both FetchObjectContext (with object ID) and HybridSearch (without ID) paths

   **Out-of-Scope Tests** (agent should refuse/escalate):
   - Questions outside domain
   - Requests for unauthorized actions
   - Sensitive topics triggering guardrails
   - Guardrail edge cases

   **Edge Case Tests** (ambiguous/tricky):
   - Ambiguous questions matching multiple skills
   - Multi-part questions
   - Conflicting information
   - Missing/incomplete context

   **Adversarial Tests** (trigger wrong behavior):
   - Prompt injection attempts
   - Questions triggering wrong skill
   - Out-of-scope knowledge questions

   **Regression Tests** (common failures):
   - Previously failed questions
   - Boundary conditions between skills

6. **Format each test**:
   ```
   Input: <user message>
   Expected Behavior: <what agent should do>
   Expected Skill: <which skill(s), name HybridSearch/FetchObjectContext/NL2SQL>
   Expected Knowledge Source: <which source(s)>
   Category: <happy-path | out-of-scope | edge-case | adversarial | regression>
   Priority: <P0 (must-pass) | P1 (should-pass) | P2 (nice-to-have)>
   ```

7. **Output ready-to-use format** for Agent Studio's Bulk Tests

### 6. Answer Questions About Agents

When asked questions about DevRev agents:

1. **Read relevant guides** from `knowledge/` based on topic
2. **Use correct terminology**:
   - **FetchObjectContext** — Direct fetch when object ID is known
   - **HybridSearch** — Scoped search over configured knowledge
   - **NL2SQL** — Structured data queries (requires annotations)
3. **Explain priority**: FetchObjectContext → targeted tools → HybridSearch → NL2SQL

## NL2SQL Annotation Workflow

**Critical**: Whenever an agent uses NL2SQL, annotations must be checked before any other work.

### Step 1: Check Annotations

```bash
bash skills/7-agent-building/scripts/check-annotations.sh "<table-id>" /tmp/annotations
```

This checks:
- Annotated vs. unannotated columns
- Placeholder/broken descriptions (<20 chars)
- Provides fix instructions if broken

### Step 2: Fix Annotations (6-Phase Workflow)

If annotations are broken, follow this AI-agent-driven workflow using `devrev.py`:

**Phase 1 — Schema-Only Analysis**
- Run `./devrev.py tables-list` then `./devrev.py table-schema <id>`
- Extract info from schema: enum lists, types, id_types, field suffixes
- Cluster related fields by prefix
- Flag ambiguous acronyms

**Phase 2 — Data Profiling**
- NULL rate: `SELECT COUNT((t).id) as total, COUNT((t).{field}) as non_null FROM {table} as t`
- VARCHAR: distinct values + frequency (top 25)
- DOUBLE/INT: min, max, avg; check for sentinel values
- DATE/TIMESTAMP: range (earliest, latest)
- Limit to 3-4 concurrent queries at a time

**Phase 3 — Conditional Profiling**
- NULL co-occurrence within clusters
- Population conditioned on categorical fields
- Side-by-side comparison of similar fields

**Phase 4 — Human Input (Batch)**
- Collect ALL unresolvable ambiguities in a single batch
- Ask about: overlapping fields, business acronyms, ambiguous NULL semantics

**Phase 5 — Write Descriptions**
- Write from LLM's perspective generating SQL
- Cover: semantic meaning, when populated vs NULL, sentinel values, field relationships
- Use proportions, not absolute counts (they go stale)

**Phase 6 — Verification**
- Generate 3-5 realistic test questions
- Write SQL using new descriptions
- Run with `./devrev.py query`
- Sanity-check results

**Output**: `{table}_field_descriptions.json`

**Apply**: Agent Studio → Knowledge → Datasets → Edit Schema

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

## API Contract Compliance

> **Always read this section before building any create/update payload.**
> See [references/api-contracts.md](references/api-contracts.md) for the full reference with examples.

### Critical Schema Differences: Create vs Update

| Field | `ai-agents.create` | `ai-agents.update` |
|---|---|---|
| `slug` | ❌ Not accepted | ❌ Not accepted |
| `guardrails` | Plain array `[...]` | Object `{"set": [...]}` |
| `skills` | Plain array `[...]` | Object `{"set": [...]}` |

### Guardrail Fields Must Be Flat (Not Nested)

The GET response returns guardrails with `topic_boundary` nested. **This shape is rejected by write endpoints.** Always flatten `topic_name` and `description` to the top level of each guardrail object:

```json
// ❌ Wrong — copied from GET response
{ "type": "topic_boundary", "topic_boundary": { "topic_name": "...", "description": "..." } }

// ✅ Correct — for both create and update
{ "type": "topic_boundary", "topic_name": "...", "description": "..." }
```

### Skill Trigger IDs Must Be Strings

The GET response returns `trigger.operation`, `trigger.plan`, and `trigger.workflow` as full hydrated objects. Write endpoints require a plain string (the DON ID). There are three trigger types:

```json
// ❌ Wrong — copied from GET response (any trigger type)
{ "trigger": { "operation": { "id": "don:...", "name": "..." } } }
{ "trigger": { "workflow": { "id": "don:...", "display_id": "..." } } }

// ✅ Correct — string ID for whichever trigger type applies
{ "trigger": { "operation": "don:integration:dvrv-in-1:operation/devrev.fetch_object_context" } }
{ "trigger": { "plan": "don:core:dvrv-in-1:devo/<id>:ai_agent_plan/<n>" } }
{ "trigger": { "workflow": "don:integration:dvrv-in-1:devo/<id>:workflow/<n>" } }
```

### Pre-Flight Checklist (use before every API call)

**Create:**
- [ ] No `slug` field
- [ ] `guardrails` is a plain array
- [ ] `skills` is a plain array
- [ ] Each guardrail: `topic_name` and `description` are flat (not nested under `topic_boundary`)
- [ ] Each skill trigger: `operation`, `plan`, or `workflow` is a string, not an object
- [ ] Each skill name accurately describes its function (not a misleading generic name)

**Update:**
- [ ] `id` field present (DON ID or display_id format)
- [ ] No `slug` field
- [ ] `guidance` is a string or absent — never `null` (causes `unexpected_json_type`)
- [ ] `memory_config` is an object or absent — never `null`
- [ ] `guardrails` wrapped as `{"set": [...]}`
- [ ] `skills` wrapped as `{"set": [...]}`
- [ ] Each guardrail: `topic_name` and `description` are flat
- [ ] Each skill trigger: `operation`, `plan`, or `workflow` is a string, not an object

### Using the create-agent.sh Script

The `create-agent.sh` script enforces all the above rules automatically:

```bash
# Validate a payload before calling the API (no network call)
bash skills/7-agent-building/scripts/create-agent.sh check /tmp/my-agent.json create
bash skills/7-agent-building/scripts/create-agent.sh check /tmp/my-agent.json update

# Create a new agent
bash skills/7-agent-building/scripts/create-agent.sh create /tmp/new-agent.json

# Update an existing agent
bash skills/7-agent-building/scripts/create-agent.sh update /tmp/update.json

# Convert a GET response (agent.json) to a valid update payload
bash skills/7-agent-building/scripts/create-agent.sh convert /tmp/agent-config/agent.json /tmp/update.json
```

### Common Error → Fix Reference

| Error | Fix |
|---|---|
| `Invalid field: slug` | Remove `slug` from payload |
| `Missing required field: goal` | `goal` is required on create; `name` is optional |
| `expected: 'OBJECT', actual: 'ARRAY'` on `skills` or `guardrails` | Wrap in `{"set": [...]}` on update |
| `Invalid field: topic_boundary` | Flatten `topic_name`/`description` to guardrail top level |
| `expected: 'STRING', actual: 'OBJECT'` on `operation`, `plan`, or `workflow` | Use the DON ID string, not the full hydrated object |
| `expected: 'STRING', actual: 'NULL'` on `guidance` | Omit the key or set `""` — never send `guidance: null` |
| `Invalid field: agent_id` on `versions.list` | Use `"agent"` as the filter key, not `"agent_id"` |
| `ai agent id is required` on `versions.list` | The `agent` filter is required — cannot list all versions |
| `limit must be > 0` | list limit must be between 1 and 99 |
| `invalid val for PerPage, should be less than '100'` | list limit maximum is 99 |

## API Safety

When changing agents via API:

1. **Ask before any mutating call** — No POST to internal create/update/delete/deploy/execute endpoints without explicit user approval
2. **Ground requests in api-specs** — Use `devrev/api-specs` repo, `specs/next/openapi-internal.yaml` for `/internal/ai-agents.*`
3. **Persist drafts first** — Write proposed JSON/diff to file, then call API after approval
4. **Validate before calling** — Use `create-agent.sh check` on every payload before sending

See [references/api-specs-and-api-safety.md](references/api-specs-and-api-safety.md) and [references/api-contracts.md](references/api-contracts.md) for details.

## Key Case Study: PeopleStrong SupportGPT

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

**Network permission errors (exit code 56):**
- Add `required_permissions: ["full_network"]` to all Shell commands calling DevRev APIs

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
/ `references/feature-flags.md`. Then append a row to `docs/LEARNINGS.md` and commit — full
protocol: `.claude/skills/capture-learnings/SKILL.md`.
