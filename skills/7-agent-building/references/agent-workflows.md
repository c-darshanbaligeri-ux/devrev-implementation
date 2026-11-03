# Agent workflows: the long-form procedures

## Contents
<!-- toc -->
- [Available Workflows](#available-workflows)
  - [1. Sync Knowledge Base](#1-sync-knowledge-base)
  - [2. Create a New Agent](#2-create-a-new-agent)
  - [3. Debug an Agent](#3-debug-an-agent)
  - [4. Improve an Agent](#4-improve-an-agent)
  - [5. Create Test Set](#5-create-test-set)
  - [6. Answer Questions About Agents](#6-answer-questions-about-agents)
<!-- /toc -->

Moved verbatim from `SKILL.md`. Each workflow also has a command file in `commands/` (`agent-sync`, `agent-create`, `agent-debug`, `agent-improve`, `agent-test`, `agent-ask`).

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
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" ${TMPDIR:-/tmp}/agent-config
```

3. **Read relevant guides** based on issue type:
   - Retrieval issues: `ART-27857.txt`, `ART-30502.txt`, `ART-27859.txt`
   - Prompting issues: `ART-27855.txt`
   - Skill/tool issues: `ART-30501.txt`
   - Design issues: `ART-30503.txt`
   - Testing issues: `ART-27861.txt`

4. **For NL2SQL agents** — Check annotations FIRST:
```bash
bash skills/7-agent-building/scripts/check-annotations.sh "<table-id>" ${TMPDIR:-/tmp}/annotations
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
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" ${TMPDIR:-/tmp}/agent-config
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
     bash skills/7-agent-building/scripts/check-annotations.sh "<dataset-id>" ${TMPDIR:-/tmp}/annotations
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
bash skills/7-agent-building/scripts/get-agent.sh "<agent-id-or-slug>" ${TMPDIR:-/tmp}/agent-config
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
