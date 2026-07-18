# skills/6-workflows/references/ — which file, when

| File | Read it when |
| --- | --- |
| `manage-workflows-api.md` | CRUD/lifecycle verbs over existing workflows: list, get, create shell, update, publish, trigger, delete — all `/internal/workflows.*` endpoints, DON formats, error table |
| `template-json-format.md` | Authoring a template JSON (the main event): envelope format, step structure, ports, value types, trigger config, loops/variables, invoke_code rules, the validation checklist, the example-table (confirmed-working templates) |
| `ai-agent-skill-pattern.md` | Building an **agent-callable skill** — read IN ADDITION to template-json-format.md: the four-block skeleton, `labels: ["skill"]`, input schema on the trigger, output block, skill-specific checklist |

Operation lookup order while authoring: `../operations/triggers.md` / `actions.md` / `controls.md` /
`blockings.md` for discovery → `../operations/schemas/<slug>.md` for the exact field-level
input/output schema (130 ops resolved) → `../examples/working-*.json` for a proven pattern to
imitate.
