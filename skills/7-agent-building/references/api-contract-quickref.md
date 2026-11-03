# API contract quick reference

Moved verbatim from `SKILL.md`; the full contract is in `api-contracts.md`.

> The example DON ids use the `dvrv-in-1` shard, the org they were verified on. Your org's shard may differ (for example `dvrv-us-1`): copy it from any DON id the API returns and never mix shards.

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
bash skills/7-agent-building/scripts/create-agent.sh check ${TMPDIR:-/tmp}/my-agent.json create
bash skills/7-agent-building/scripts/create-agent.sh check ${TMPDIR:-/tmp}/my-agent.json update

# Create a new agent
bash skills/7-agent-building/scripts/create-agent.sh create ${TMPDIR:-/tmp}/new-agent.json

# Update an existing agent
bash skills/7-agent-building/scripts/create-agent.sh update ${TMPDIR:-/tmp}/update.json

# Convert a GET response (agent.json) to a valid update payload
bash skills/7-agent-building/scripts/create-agent.sh convert ${TMPDIR:-/tmp}/agent-config/agent.json ${TMPDIR:-/tmp}/update.json
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
