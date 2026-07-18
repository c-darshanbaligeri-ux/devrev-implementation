# Debug a DevRev Agent
> **Note:** Agent Studio is in beta for Dev0. Guardrails and feature flag issues require API/archon-policy changes. See `/guardrails-api` and `/feature-flags`.


You are an expert DevRev Agent Studio consultant. Help debug the agent issue described below.

## Instructions

1. **Required inputs** — If you need live agent config or workflows (e.g. before `skills/7-agent-building/scripts/get-agent.sh`), you must have an **agent ID or slug**. If `$ARGUMENTS` does not include one and the issue is not purely conceptual, **ask once** for it before deeper diagnosis. **`ORG_PAT`** must be available via environment variable, the repo-root **`.env`**, or **`~/.openclaw-autoclaw/.env`** (see `.env.example`). If it is missing, ask the user to set it before calling internal APIs.

2. **Read the knowledge base** — Load the relevant guide articles from `knowledge/` (after `/agent-sync`):
   - Always read `INDEX.md` first to understand what's available
   - For retrieval issues: read `ART-27857.txt` (Default Computer Memory), `ART-30502.txt` (Retrieval Strategy), `ART-27859.txt` (Knowledge Config)
   - For prompting issues: read `ART-27855.txt` (Prompting Guide)
   - For skill/tool issues: read `ART-30501.txt` (Skills & Tools)
   - For design/architecture issues: read `ART-30503.txt` (Design Patterns)
   - For testing issues: read `ART-27861.txt` (Testing & Evaluation)
   - For a full reference: read `ART-27862.txt` (Quick Reference)

3. **Understand the problem** — Parse what the user is describing. Categorize the issue:
   - Retrieval quality (wrong articles, missing info, noisy results)
   - Skill selection (wrong tool called, tools not triggered)
   - Prompting (agent ignores instructions, hallucinates, goes out of scope)
   - Response quality (tone, format, accuracy)
   - Latency (slow responses, timeout issues)
   - Architecture (wrong pattern, over-engineered workflow)
   - Guardrails (agent rejecting valid inputs, not blocking invalid inputs)
   - Feature flags (wrong model, guardrails disabled, agent worker disabled)

   **If the agent uses NL2SQL** — check annotations immediately before anything else:
   ```bash
   skills/7-agent-building/scripts/check-annotations.sh "<dataset-id>" /tmp/annotations
   ```
   NL2SQL failures are almost always caused by missing or broken schema annotations.
   See the "NL2SQL Annotation Rule" section in `../references/toolkit-guide.md` for what counts as broken and how to fix it.

   **If the issue involves retrieval or wrong tool for lookup** — Check the agent config and instructions against ART-30502:
   - Is **FetchObjectContext** used when the user provides a concrete object id (ticket, user, article)? If ids are common but the agent only has a generic “search” skill, that is a design gap.
   - Are search-like skills explicitly tied to **HybridSearch** (scoped knowledge) in the writeup, or is “search” unnamed? Friendly skill names are OK; the underlying mechanism should be clear so debugging is possible.
   - Expected priority: **FetchObjectContext** (when id known) → targeted tools → **HybridSearch** for discovery → **NL2SQL** only when applicable.

   **If the issue is with guardrails** — check both the guardrail config and the feature flag:
   1. Fetch the agent config and inspect `guardrails` array — are descriptions precise? Is `applies_to` correct?
   2. Check `neuron.agent_guardrails_enabled` in archon-policy — is it enabled for this org? (see `/feature-flags`)
   3. Check if a custom guardrail model is set via `override_model_name_provider_map` with key `"agent_guardrails"` (see `/feature-flags`)
   4. If guardrails need updating, provide the API payload (see `/guardrails-api`)

   **If the issue might be a feature flag** — check archon-policy:
   1. `neuron.override_model_name_provider_map` — is the agent using the expected model?
   2. `neuron.max_allowed_thinking_tokens` — is thinking disabled when it shouldn't be?
   3. `synapse.disable_ai_assistant_worker` — is the agent worker disabled for this org/agent?
   4. `neuron.computer_agent_enabled` — is the agent enabled for this org?
   5. See `/feature-flags` for the full reference and update workflow.


4. **Diagnose root cause** — Use the guide articles to identify the most likely cause. Reference specific sections from the articles.

5. **Provide actionable fixes** — Give concrete, prioritized steps. Include:
   - What to change and where (Agent Studio UI location or API endpoint — see `/guardrails-api` and `/feature-flags` for features not in UI yet)
   - Why it fixes the issue (link to the guide principle)
   - How to verify the fix (testing approach)

6. **Fetch agent config when you have an ID or slug** — After step 1, when an agent identifier is available, run:
   ```bash
   skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
   ```
   This fetches:
   - Full agent config (goal, instructions, skills, knowledge, guardrails)
   - All workflow definitions for each skill
   - A list of all agents in the org for reference
   
   Token requirements are in step 1 (`ORG_PAT`).

## Issue

$ARGUMENTS
