# Create a Test Set for a DevRev Agent
> **Note:** Agent Studio is in beta for Dev0. Test sets may need to account for API-only features (guardrails, model-specific behavior). See `/guardrails-api` and `/feature-flags`.


You are an expert DevRev Agent Studio consultant. Create a comprehensive test set for the agent described below.

## Instructions

1. **Required inputs** — A concrete test set tied to a **live** agent needs an **agent ID or slug**. If `$ARGUMENTS` does not include one, **ask once** before running `./scripts/get-agent.sh` or designing tests from production config. **`ORG_PAT`** must be available via environment variable, **`skills/7-agent-building in repo-root .env`**, or **`~/.openclaw-autoclaw/.env`** (see `.env.example`). If it is missing, ask the user to set it.

2. **Read the knowledge base** — Load the relevant guide articles from `knowledge/` (after `/agent-sync`):
   - `ART-27861.txt` — Testing & Evaluation Guide (PRIMARY — this is the testing bible)
   - `ART-27855.txt` — Prompting Guide (for testing instruction quality)
   - `ART-30501.txt` — Skills & Tools Guide (for testing skill selection)
   - `ART-30502.txt` — Retrieval Strategy (for testing retrieval quality)
   - `ART-27863.txt` — Full Agent Examples (for reference test patterns)

3. **Understand the agent** — Once you have an agent ID or slug (from `$ARGUMENTS` or step 1), run:
   ```bash
   ./scripts/get-agent.sh "<agent-id-or-slug>" /tmp/agent-config
   ```
   This fetches the full agent config + all skill workflows. Token requirements are in step 1 (`ORG_PAT`).
   
   Analyze:
   - Goal and scope
   - Skills and their trigger conditions — note which behaviors are **FetchObjectContext** (object id in hand), **HybridSearch** (discovery), or **NL2SQL**; vague “search” without naming the mechanism is a test gap
   - Knowledge sources
   - Guardrails — inspect `guardrails` array for topic_boundary configs. Check `applies_to` (input/output/both) and `description` precision. See `/guardrails-api` for schema details.
   - Response format expectations

4. **Design the test set** — Following `ART-27861`'s framework, create tests in these categories:

   **Happy Path Tests** (agent should succeed):
   - Core use cases the agent is designed for
   - Each skill/tool should be tested at least once
   - Each knowledge source should be queried
   - **Retrieval paths**: Include cases with a **concrete object id** in the message (expect **FetchObjectContext** path first, per ART-30502) and cases with **no id** that require **HybridSearch** (or NL2SQL if configured). Name the expected mechanism in the test row.

   **Out-of-Scope Tests** (agent should refuse/escalate):
   - Questions outside the agent's domain
   - Requests for actions the agent shouldn't take
   - Sensitive topics that should trigger guardrails
   - **Guardrail-specific tests**: inputs that match the `topic_boundary` description (should pass) vs. inputs clearly outside it (should return `default_message`)
   - **Guardrail edge cases**: inputs that are borderline — partially on-topic, rephrased off-topic questions, multi-turn conversations that drift off-topic

   **Edge Case Tests** (ambiguous or tricky inputs):
   - Ambiguous questions that could match multiple skills
   - Multi-part questions
   - Questions with conflicting information
   - Missing or incomplete context

   **Adversarial Tests** (designed to trigger wrong behavior):
   - Prompt injection attempts
   - Questions that should trigger the wrong skill
   - Questions from outside the configured knowledge scope

   **Regression Tests** (common failure patterns):
   - Questions that previously caused wrong answers
   - Boundary conditions between skills

5. **Format the test set** — For each test, provide:
   ```
   Input: <user message>
   Expected Behavior: <what the agent should do>
   Expected Skill: <which skill(s) should be invoked, if any — name HybridSearch / FetchObjectContext / NL2SQL where relevant, not only friendly skill names>
   Expected Knowledge Source: <which source(s) should be searched, if any>
   Category: <happy-path | out-of-scope | edge-case | adversarial | regression>
   Priority: <P0 (must-pass) | P1 (should-pass) | P2 (nice-to-have)>
   ```

6. **Output a ready-to-use format** — Produce the test set in a format that can be pasted directly into Agent Studio's Bulk Tests, plus a summary of coverage gaps.

## Agent to Test

$ARGUMENTS
