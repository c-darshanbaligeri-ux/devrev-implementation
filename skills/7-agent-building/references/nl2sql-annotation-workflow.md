# NL2SQL annotation workflow

Moved verbatim from `SKILL.md`.

> `devrev.py` is the CLI from the `devrev/auto-annotations` repository, not part of this repo. `scripts/check-annotations.sh` clones it (to `$AUTO_ANNOTATIONS_DIR`); run the `./devrev.py ...` commands below from that directory.

## NL2SQL Annotation Workflow

**Critical**: Whenever an agent uses NL2SQL, annotations must be checked before any other work.

### Step 1: Check Annotations

```bash
bash skills/7-agent-building/scripts/check-annotations.sh "<table-id>" ${TMPDIR:-/tmp}/annotations
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
