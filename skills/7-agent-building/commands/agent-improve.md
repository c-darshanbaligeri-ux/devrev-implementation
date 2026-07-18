# Improve a DevRev Agent
> **Note:** Agent Studio is in beta for Dev0. Some improvements (guardrails, model overrides) may require API changes. See `/guardrails-api` and `/feature-flags`.


You are an expert DevRev Agent Studio consultant. Analyze and improve the agent described below.

## Instructions

1. **Required inputs** — Improvement against a **live** agent needs an **agent ID or slug**. If `$ARGUMENTS` does not include one, **ask once** before running `skills/7-agent-building/scripts/get-agent.sh` or deep analysis. **`ORG_PAT`** must be available via environment variable, the repo-root **`.env`**, or **`~/.openclaw-autoclaw/.env`** (see `.env.example`). If it is missing, ask the user to set it.

2. **Read the knowledge base** — Load the relevant guide articles from `knowledge/` (after `/agent-sync`):
   - `INDEX.md` — article overview
   - `ART-27855.txt` — Prompting Guide
   - `ART-30501.txt` — Skills & Tools Guide
   - `ART-27857.txt` — Default Computer Memory limitations
   - `ART-30502.txt` — Retrieval Strategy (includes the PeopleStrong case study)
   - `ART-27859.txt` — Knowledge Configuration
   - `ART-30503.txt` — Design Patterns
   - `ART-27861.txt` — Testing & Evaluation

3. **Get the current agent config** — Once you have an agent ID or slug (from `$ARGUMENTS` or step 1), run:
   ```bash
   skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
   ```
   This fetches the full agent config + all skill workflows + org agent list. Token requirements are in step 1 (`ORG_PAT`).

4. **Analyze across all dimensions:**
   - **Goal clarity** — Is it specific, scoped, and actionable? (ART-27855 §1)
   - **Instructions quality** — Are they organized, minimal, and free of branching logic? (ART-27855 §2, PeopleStrong case study in ART-30502)
   - **Skill design** — Are there overlapping tools? Ambiguous handoffs? Too many skills? (ART-30501, PeopleStrong case study in ART-30502)
   - **Knowledge configuration** — Too many sources? Wrong object types? No curation? (ART-27857, ART-27859)
   - **Retrieval strategy** — Is **FetchObjectContext** used when object ids are available? Are search skills explicitly grounded as **HybridSearch** (or NL2SQL) in docs/instructions, not only a vague “search” name? (ART-30502)
   - **NL2SQL annotations** — If the agent uses NL2SQL, run the annotation check first:
     ```bash
     skills/7-agent-building/scripts/check-annotations.sh "<dataset-id>" /tmp/annotations
     ```
     Missing or broken annotations are the #1 cause of NL2SQL failures. See `../references/toolkit-guide.md` → "NL2SQL Annotation Rule".
   - **Design pattern fit** — Is the pattern right for the task? Over-engineered? (ART-30503)
   - **Guardrails** — Are they specific with trigger conditions? (ART-27855 §3)
     - Check: Are `topic_boundary` descriptions precise enough to catch off-topic queries?
     - Check: Is `applies_to` set correctly (input, output, or both)?
     - Check: Is `default_message` helpful to the user?
     - Check: Are there gaps in coverage (topics the agent should be restricted from but isn't)?
     - If guardrails need updating and UI doesn't support it, provide the API payload (see `/guardrails-api`)
   - **Feature flags** — Is the agent configured correctly in archon-policy? (see `/feature-flags`)
     - Check: `neuron.override_model_name_provider_map` — is the right model configured for this agent?
     - Check: `neuron.max_allowed_thinking_tokens` — is thinking enabled if needed?
     - Check: `neuron.agent_guardrails_enabled` — are guardrails active for this org?
     - Check: `synapse.disable_ai_assistant_worker` — is this agent accidentally disabled?
   - **Testing coverage** — Does it have a test set? Are metrics being tracked? (ART-27861)

5. **Prioritize improvements** — Rank findings by impact:
   - 🔴 Critical: Issues that directly cause wrong answers or wrong actions
   - 🟡 Important: Issues that degrade quality or reliability
   - 🟢 Nice-to-have: Optimizations and polish

6. **Provide concrete changes** — For each improvement:
   - What to change (specific text/config)
   - Where to change it (Agent Studio location)
   - Expected impact
   - How to verify (test case)
   - If UI doesn't support the change yet, provide the full API JSON payload

## Agent to Improve

$ARGUMENTS
