# /feature-flags — Guide for updating feature flags in archon-policy

## Overview

Feature flags in DevRev are managed via **Rego policies** in the `archon-policy` repository (clone locally; policy files live under `policies/`). They control product behavior per environment (`dev`, `qa`, `prod`), per org, per user, and per agent.

Skill naming and retrieval order (**FetchObjectContext** vs **HybridSearch** vs NL2SQL) are set in **agent config and instructions**, not in these Rego files. Use `agent-create.md`, `../references/toolkit-guide.md` ("Naming retrieval in agent designs"), and ART-30502 for that; use this doc for **runtime** toggles (models, workers, guardrail enablement, etc.).

## Key Policy Files

| File | Package | Controls |
|---|---|---|
| `experience.rego` | `devrev.experience` | **UI feature flags** — the largest file. Snap-in enablement, agent builder, agent studio, dashboard features, etc. |
| `synapse.rego` | `devrev.synapse` | **Agent runtime** — agent routing, SQS timeouts, computer agent config, today's message, assistant settings. |
| `neuron.rego` | `devrev.neuron` | **AI/LLM config** — model overrides per agent, thinking tokens, guardrails, RAG settings, code sandbox, tracing. |
| `env.rego` | `devrev.env` | **Environment helpers** — `is_internal_prod_dev_org`, API URLs, dev/qa test emails. |
| `dev_org.rego` | `devrev.dev_org` | **Org-level config** — HIPAA compliance, demo orgs, org properties. |
| `archon.rego` | `devrev.archon` | **Core policy** — owner checks, global defaults. |
| `demo.rego` | `devrev.demo` | **Demo org enablement** — `demo.agent_builder_enabled`, `demo.agent_studio_enabled`, etc. |

## Common Feature Flag Patterns

### 1. Boolean flag (true/false)

```rego
# Default off in prod, on in dev/qa
ui_my_feature_enabled {
  input.cluster.env in ["dev", "qa"]
}

# On for specific prod orgs
ui_my_feature_enabled {
  input.cluster.env == "prod"
  input.actor.dev_org_id in [
    "0",       # DevRev internal
    "3fAHEC",  # Maple (test org)
  ]
}

# On for specific users in prod
ui_my_feature_enabled {
  input.cluster.env == "prod"
  lower(input.actor.email) in [
    "someone@devrev.ai",
  ]
}
```

### 2. Config value (not boolean)

```rego
# String config
ui_refetch_config_interval_in_seconds := 5*60 {
  input.cluster.env in ["prod"]
}

# JSON config
my_config := json.marshal({
  "key": "value",
  "nested": {"foo": true}
}) {
  input.cluster.env in ["prod"]
}
```

### 3. Model override per agent (neuron.rego)

```rego
override_model_name_provider_map := json.marshal({
    "goal_agent": {
        "model_name": "gpt-4.1-2025-04-14",
        "model_provider": "OPENAI"
    }
}) {
    input.cluster.env in ["prod"]
    input.data.agent_id in [
        "don:core:dvrv-us-1:devo/0:ai_agent/123",
    ]
}
```

Supported providers: `OPENAI`, `BEDROCK`, `VERTEXAI`, `LOCAL`, `CEREBRAS`

### 4. Disable specific agent workers (synapse.rego)

```rego
disable_ai_assistant_worker {
  input.cluster.env == "prod"
  input.actor.dev_org_id == "0"
  input.data.agent_id in [
    "104", "197", "259",
  ]
}
```

### 5. Thinking tokens per agent (neuron.rego)

```rego
max_allowed_thinking_tokens := 4096 {
    input.cluster.env in ["prod"
    input.data.agent_id in [
        "don:core:dvrv-us-1:devo/116f4TFiii:ai_agent/14",
    ]
} else := 0
```

### 6. Snap-in enablement (experience.rego)

```rego
# Snap-in visible to specific orgs
ui_computer_snap_ins_install_enabled {
  input.cluster.env in ["dev", "qa", "prod"]
}

# Snap-in function/operation flags
ui_agent_builder_enabled {
  input.cluster.env in ["dev", "qa"]
} else = true {
  demo.agent_builder_enabled
}
```

### 7. Guardrails per agent (neuron.rego)

```rego
agent_guardrails_enabled := false {
  input.cluster.env in ["dev"]
  # specific org/agent exclusions
} else := true {
  input.cluster.env in ["dev", "qa", "prod"]
}
```

## Available Input Fields

| Field | Description |
|---|---|
| `input.cluster.env` | `"dev"`, `"qa"`, `"prod"` |
| `input.cluster.region` | `"us-east-1"`, `"ap-south-1"`, `"eu-central-1"`, etc. |
| `input.actor.dev_org_id` | Org ID string |
| `input.actor.user_id` | User ID string |
| `input.actor.email` | User email (case-sensitive) |
| `input.actor.type` | `"devu"` (dev user), `"revu"` (rev user), `"svcacc"` (service account), `"sysu"` (system user) |
| `input.data.agent_id` | Agent DON (e.g. `"don:core:dvrv-us-1:devo/0:ai_agent/63"`) |
| `input.data.slug` | Agent slug (e.g. `"computer"`) |
| `input.data.access_level` | `"INTERNAL"` or external |

## Helper Variables

```rego
# From env.rego
env.is_internal_prod_dev_org   # DevRev employees in prod
env.devrev_api_url             # API base URL
env.internal                   # Internal user/org check

# From dev_org.rego
dev_org.hipaa_compliant        # HIPAA org checks

# From demo.rego
demo.agent_builder_enabled     # Demo org enablement
demo.agent_studio_enabled      # Demo org enablement

# Common sets (defined in experience.rego)
dev_e2e_test_emails            # E2E test emails for dev
qa_e2e_test_emails             # E2E test emails for QA
data_team_members              # Data team members
```

## Registering a Flag in the Export Map

After adding a new flag in `experience.rego`, add it to the `flags` map at the bottom of the file so it's exposed via the `experience.flags.get` endpoint:

```rego
flags = `{
  "experience.ui_my_new_feature_enabled": "ui_my_new_feature_enabled",
  ...
}`
```

- **Key**: `"experience.<package>.<flag_name>"` (full qualified name)
- **Value**: The short name to expose in the API response (usually the flag name without `ui_` prefix if you want, but conventionally the same name)

## Workflow

1. **Edit** the appropriate `.rego` file in `~/.CURSOR/repos/archon-policy/policies/`
2. **Test** locally if possible (archon has eval tooling)
3. **Commit and push** to `main` — archon auto-deploys
4. **Verify** using the Archon admin UI: `https://<env>.devrev.ai/tools/archon/admin`

## Key Sections in experience.rego for Agents & Snap-ins

Search for these flag names to find the relevant sections:

- `ui_agent_builder_enabled` — Agent builder UI
- `ui_agent_studio_enabled` — Agent studio UI
- `ui_agent_studio_mcp_enabled` — MCP in agent studio
- `ui_agent_studio_playground_enabled` — Agent playground
- `ui_agent_observability_enabled` — Agent observability dashboards
- `ui_agent_evals_enabled` — Agent evaluation framework
- `ui_agent_versioning_enabled` — Agent versioning
- `ui_enterprise_agent_enabled` — Enterprise agent features
- `ui_computer_snap_ins_install_enabled` — Snap-in install UI
- `ui_snap_in_details_tabs_enabled` — Snap-in detail page tabs
- `ui_snap_in_authorization_enabled` — Snap-in authorization/scopes
- `ui_computer_and_apps_enabled` — Computer/Agent app access

## Key Sections in neuron.rego for Agent Config

- `override_model_name_provider_map` — Per-agent model overrides
- `max_allowed_thinking_tokens` — Per-agent thinking token limits
- `agent_guardrails_enabled` — Guardrails on/off per org/agent
- `computer_agent_enabled` — Computer agent availability
- `code_sandbox_execute_code_enabled` — Code execution sandbox
- `agent_dynamic_skills_enabled` — Dynamic skill loading
- `publish_traces_to_langfuse_enabled` — Langfuse tracing
- `use_llm_gateway` — LLM gateway routing
- `agent_temporal_encryption_enabled` — Temporal workflow encryption
- `agent_session_encryption_enabled` — Session encryption
