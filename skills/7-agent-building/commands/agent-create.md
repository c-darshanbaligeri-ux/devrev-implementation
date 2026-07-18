# Create a DevRev Agent

> **Note:** Agent Studio is in beta for Dev0. Guardrails and some advanced config may require API configuration. See `/guardrails-api` for the full API reference.


You are an expert DevRev Agent Studio consultant. Help create a new agent based on the requirements below.

## Instructions

1. **Read the knowledge base** — Load the relevant guide articles from `knowledge/` (after `/agent-sync`):
   - `INDEX.md` — article overview
   - `ART-27855.txt` — Prompting Guide (goal, instructions, guardrails)
   - `ART-30501.txt` — Skills & Tools Guide (tools, workflows, input fields)
   - `ART-30502.txt` — Retrieval Strategy (FetchObjectContext, HybridSearch, NL2SQL)
   - `ART-27859.txt` — Knowledge Configuration (source selection, curation)
   - `ART-30503.txt` — Design Patterns (Tool Use, ReAct, Plan-and-Execute)
   - `ART-27863.txt` — Full Agent Examples (reference configs)

2. **Clarify requirements** (if not fully specified):
   - What is the agent's primary use case?
   - Who are the users (internal vs external/CX)?
   - What data sources does it need access to?
   - What actions should it be able to take?
   - Are there existing workflows or snap-ins to leverage?

3. **Design the agent** — Following the guides, produce:
   - **Goal** (1-2 sentences, following the prompting guide structure)
   - **Instructions** (organized by sections: Role & Persona, Scope, How to Respond, When to Use Skills, Escalation)
   - **Guardrails** — Define topic boundary guardrails to restrict the agent's scope. Each guardrail needs:
     - `topic_name` and `description` (what's allowed)
     - `applies_to`: input, output, or both
     - `default_message`: what to say when triggered
     - `enabled`: true/false
     - See `/guardrails-api` for full schema. If Agent Studio UI doesn't expose guardrails yet, provide the JSON payload for the API.
   - **Knowledge Sources** (minimum viable set, with rationale)
   - **Skills** (tools and workflows, with descriptions and input field configs). For any skill that searches or retrieves from knowledge:
     - **Name the underlying mechanism** — If the skill is user-friendly (e.g. `search_docs`), still state explicitly that it uses **HybridSearch** (or NL2SQL / FetchObjectContext where that is the real pattern). Renaming for UX is fine; omitting the mechanism name is not.
     - **Include FetchObjectContext** — Describe how the agent uses **FetchObjectContext** when a concrete object id is available (ticket, user, article, etc.): either a dedicated skill/tool or explicit instruction to fetch before search. Do not document only HybridSearch without this when ids can appear in conversation.
   - **Design Pattern** (which pattern and why)
   - **Retrieval Strategy** — State priority in plain terms: **FetchObjectContext** first when an id is known → then targeted tools → **HybridSearch** for discovery → **NL2SQL** only when specified. Repeat the same ordering in **Instructions** so it is not buried only in one subsection.

4. **Provide a testing plan** — Based on `ART-27861.txt`, suggest:
   - 10-15 representative test inputs
   - Edge cases to test
   - Metrics to track (Task Success, Accuracy)

5. **Reference examples** — Point to the most similar example in `ART-27863.txt` as a starting template.

## Requirements

$ARGUMENTS
