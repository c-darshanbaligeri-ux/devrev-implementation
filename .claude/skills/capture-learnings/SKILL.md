---
name: capture-learnings
description: Self-learning protocol for this repo. Use IMMEDIATELY whenever, while executing any DevRev task from this repo, you (the agent) encounter an unexpected error, a permission/scope restriction, an API behavior that differs from what the references say, an undocumented endpoint/field/enum/limit, a workflow import failure with a new cause, a plugin/CLI quirk, or any correction from the user about how something actually works. Routes the learning into the SPECIFIC owning file (not just CLAUDE.md) and records it in the journal so the mistake is never repeated. Also triggers on "remember this", "note that down", "so we don't hit this again".
---

# Capture Learnings — the self-learning protocol

**Purpose**: this repo must get smarter every time it's used. A lesson that lives only in a chat
session is lost; a lesson written into the owning reference file is permanent. Whenever reality
disagrees with this repo's documentation — or teaches something the docs don't cover — update the
repo **immediately, as part of finishing the task**, not as an optional afterthought.

## When this fires (any of these, mid-task)

- An API call fails in a way the references didn't predict (wrong scope listed, extra required
  field, different error semantics, rate limit, deprecated endpoint).
- A documented payload/format turns out wrong or incomplete (field renamed, enum value missing,
  different response shape).
- You discover an undocumented endpoint, parameter, field, limit, or behavior (from a live
  response, an error message, or user-provided knowledge).
- A restriction is hit: permission/scope denial, org-level feature flag, immutable property,
  UI-only operation.
- A workflow template import fails for a cause NOT already in the debugging checklist.
- A plugin command, CLI invocation, or bootstrap step behaves unexpectedly.
- The user corrects you about DevRev behavior ("actually it works like this…").

**Does NOT fire for**: your own one-off mistakes the docs already warn about (e.g. you forgot
`custom_schema_spec` — the docs are right, you erred); transient network failures; org-specific
data (DON ids of a customer's objects) — keep those in the task's scratchpad, not the repo.

## The three steps (do all three, in order)

### 1. Verify before writing

Only record what you can back with evidence: the actual request + response/error, a reproduced
behavior, or an explicit user statement. Never record a guess. If unsure whether the behavior is
general or org-specific, say so in the entry ("observed in one org; may be org-specific").

### 2. Update the SPECIFIC owning file(s)

Route by what the learning is about — this table is the heart of the protocol:

| Learning about… | Update this file (and section) |
| --- | --- |
| Solution-design guidance (which primitive to pick, blueprint template, decision framework) proves wrong or incomplete | `skills/0-solution-architecture/SKILL.md` → "Field notes" (+ the wrong passage in its `references/` copy if applicable) |
| An endpoint's existence, method, or scope | `skills/8-devrev-api/references/00_API_Catalog.md` (the domain's table) AND the matching domain doc in `skills/8-devrev-api/references/` |
| Payload/field/enum behavior of a specific API domain | The domain doc in `skills/8-devrev-api/references/` (e.g. `Work_Items_Timeline_Tags_Links_API.md`) — fix the wrong passage in place, or add to its pitfalls |
| A cross-cutting API accuracy fact | `skills/8-devrev-api/SKILL.md` → "Accuracy notes" section |
| Custom objects, schemas, fragments, subtypes, custom links | `skills/1-object-schema-customization/SKILL.md` → "Field notes" + the wrong passage in its `references/` copy if applicable |
| States, stages, stage diagrams, lifecycle | `skills/2-stage-lifecycle-customization/SKILL.md` → "Field notes" (+ its reference copy) |
| Artifacts, org-build sequencing, data loading | `skills/3-data-upload-and-org-build/SKILL.md` → "Field notes" (+ its reference copy) |
| dashboard-dev plugin / dashboard-sync CLI behavior | `skills/4-dashboards-and-widgets/SKILL.md` → "Field notes". NEVER edit files under `repos/` — they're upstream clones; our router skill is where OUR knowledge lives |
| dataset-builder plugin, Oasis/Serengeti APIs, PaaS/Ponos | `skills/5-datasets/SKILL.md` → "Known gotchas" or "Field notes" |
| Workflow template format, import errors | `skills/6-workflows/SKILL.md` → "Debugging a failed import" checklist AND `skills/6-workflows/references/template-json-format.md` validation checklist |
| A new confirmed-working workflow template | `skills/6-workflows/examples/working-<name>.json` + a row in `template-json-format.md`'s example table (the existing learning loop) |
| Workflow operation schemas (a field the schema doc missed) | The op's file in `skills/6-workflows/operations/schemas/<slug>.md` |
| Agent Studio API contracts (ai-agents.create/update etc.) | `skills/7-agent-building/references/api-contracts.md` (it is the designated live-verified contract file — add a dated entry) |
| Guardrails/feature-flags behavior | `skills/7-agent-building/references/guardrails-api.md` / `feature-flags.md` |
| Agent-building script or knowledge issues | `skills/7-agent-building/SKILL.md` or the script itself (fix the bug) |
| Bootstrap/hook/CLI-install/plugin-loading issues | `.claude/hooks/bootstrap-workspace.sh` (fix) + `README.md` troubleshooting table (symptom/fix row) |
| MCP server behavior | `.mcp.json` (if config) + `skills/8-devrev-api/references/devrev-mcp-claude-code-setup.md` |
| Routing mistakes (request went to the wrong skill) | `.claude/skills/implementation-router/SKILL.md` + the misrouted skill's frontmatter description (add the trigger phrase) |
| A truly global rule (affects every call) | `CLAUDE.md` → "Global API rules" — this is the ONLY case where CLAUDE.md is the primary target |
| Snap-in/AirSync connector build behavior, MCP tool quirks, or a `devrev-qk-agents` plugin mistake | `skills/9-snapin-development/SKILL.md` → "Field notes". If the plugin's own `/devrev:improve-skill` proposes a patch inside `repos/devrev-qk-agents/`, that satisfies THIS repo's "never edit `repos/`" rule only if you ALSO record the same fact here — the `repos/` patch is disposable and will be overwritten by `update-repos` |

**How to write the entry in the owning file**:
- If the file states something now known to be WRONG → **fix the statement in place** (don't leave
  wrong text with a correction note beside it), and add `<!-- corrected YYYY-MM-DD: was "<old claim>"; see docs/LEARNINGS.md -->` adjacent.
- If it's NEW knowledge → add a concise, dated bullet in the file's "Field notes" / pitfalls /
  checklist section: `- (YYYY-MM-DD) <fact>. Evidence: <error message / endpoint response>.`
- Keep entries short and factual — a future agent reads them cold.
- **2026-07-18 · Field note on this protocol itself**: a full end-to-end test pass across skills 1–9 produced numerous in-place corrections (wrong reference examples, overgeneralized prior findings) but in every case the dated Field-notes-bullet convention was used and the inline `<!-- corrected YYYY-MM-DD: was "..." -->` HTML-comment convention was NOT — none of the corrections this session added that comment, even though it's the letter of this section. In practice, a clearly-worded "CORRECTED YYYY-MM-DD: ..." bolded lead-in inside the Field notes bullet itself served the same purpose (says what was wrong, when, and why) without the separate inline comment. Future agents: either convention is acceptable as long as the correction is unambiguous about what it's superseding — but if striving for strict compliance with this file's own instruction, add the HTML comment too.

### 3. Append to the journal and commit

Append one row **below the `RECONCILE-FROM-BELOW` sentinel row** at the bottom of the table in
`docs/LEARNINGS.md` (this is a *staging* append now, not a permanent one — see "End-of-session
reconciliation" below):

```
| YYYY-MM-DD | <one-line what happened> | <root cause / fact learned> | <files updated> |
```

Then commit (local git; do not push unless the user's asked for pushes generally):

```bash
git add -A && git commit -m "learn: <one-line summary>"
```

If a commit isn't possible (mid-task with unrelated staged changes), stage only the learning files
(`git add <files>`) and commit just those.

## End-of-session reconciliation

**Why this exists**: step 2 above already puts the permanent copy of every fact in its owning
skill/reference file. The journal row from step 3 is therefore temporary scaffolding — useful
mid-session as a running list of what's been captured and where, but redundant (and a drift risk)
once the owning-file edit is confirmed in place. Rather than let `docs/LEARNINGS.md` grow forever
as a second copy of every fact, it gets reconciled down to zero pending rows at the end of each
session.

**Mechanism**: a `Stop` hook (`.claude/hooks/reconcile-learnings.sh`, registered in
`.claude/settings.json`) runs whenever a turn is about to end. It checks whether any row sits below
the sentinel row (Date column `RECONCILE-FROM-BELOW`) near the end of the journal table. If so, it
blocks the Stop event with `decision: "block"` and a `reason` that re-engages you to do the actual
reconciliation — the hook itself is a shell script and cannot edit files or judge whether a fact
was correctly propagated, so it only detects and re-prompts.

**What you do when re-engaged** (do this before ending the turn again):
1. For each pending row (below the sentinel), open every file listed in its "Files updated" column
   and confirm the fact described in the row is actually present there. If it's missing or wrong,
   fix it now — the owning file, not the journal, is the permanent home for the fact.
2. Once confirmed, delete that row from the table entirely. Do not leave a placeholder.
3. **Exception**: if a row has no single owning file — a protocol-level finding about this
   skill's own process, or a whole-repo synthesis note that doesn't map to one file — do not
   delete it. Move it into the "Standing notes" section at the top of `docs/LEARNINGS.md` instead;
   that section is the one place this journal is itself the permanent home.
4. Move the sentinel row back down so it immediately precedes the (now-empty) space below it,
   ready to receive the next session's new rows.
5. Commit the result: `git add docs/LEARNINGS.md <any files fixed in step 1> && git commit -m
   "learn: reconcile journal"` — commit only, do not push (matches the standing rule for this
   protocol; pushing anything, including reconciliation commits, requires an explicit user ask).

**Historical rows are exempt.** Rows already in the table above the sentinel as of 2026-07-23
predate this lifecycle and stay in place permanently as an audit trail — the hook only ever counts
and acts on rows below the sentinel.

**Safety valve**: the hook caps itself at 3 block attempts per session (tracked in a per-session
counter file under `.claude/.auto-setup/`, gitignored). If reconciliation still isn't done on the
4th attempt, it emits a `systemMessage` instead of blocking, so a stuck reconciliation can never
hang a session indefinitely — the leftover rows just carry into next session's check.

## Guardrails

- **Never edit anything under `repos/`** — upstream clones. Learnings about their tools go in OUR
  skill files.
- **Never record secrets** — no tokens, no real customer DON ids; redact to `<REDACTED>`.
- **Never delete existing knowledge** to make room for new — correct it or append.
- One learning = one journal row. If a task surfaced three lessons, that's three rows.
- If the learning invalidates something in `docs/` user documentation claims, update that too.
