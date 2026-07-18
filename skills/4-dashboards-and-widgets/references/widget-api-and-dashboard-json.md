# Widget & dashboard — platform API and JSON structure

What the dashboard-dev tooling ultimately calls. Sourced from DevRev's API
reference and dashboard docs. Verify exact fields against the live API reference
and the cloned repo's skills, since schemas evolve.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <PAT>` |

---

## Widget endpoints

- `POST /widgets.create` — create a widget.
- `GET /widgets.get` — retrieve a widget.

`widgets.create` body includes (partial, from the API reference):
- `apps` — app fragment names installed by the widget.
- `data_sources` — the backing data tables for the widget.
- `description` — brief summary of what the widget displays.
- `identifier` — widget identifier.
- (plus dimensions/measures/filters/visualization config — confirm current
  schema in the API reference and in the dashboard-dev widget skill).

Related: `snap-widgets.create` (`POST`) is a **different** object (snap-kit
widgets for timelines/PLuG), not analytics dashboard widgets. Don't conflate them.

---

## Dashboard JSON structure

Dashboards are defined as JSON assembled from existing widgets:

```json
{
  "description": "Brief description of the dashboard",
  "id": "unique-dashboard-identifier",
  "title": "Display Title",
  "layout": [],
  "sections": [],
  "tabs": [],
  "widgets": [],
  "filters": []
}
```

Key rule: **all widgets must be created in the org first**, then referenced when
assembling the dashboard.

---

## Validate-then-create flow (what the Sync CLI does)

1. Generate widget JSON (per the widget skill's spec).
2. Validate locally (Widget Validator: JSON → SQL → DuckDB against Parquet;
   emulate filters + group-by). Fix errors from the feedback and re-validate.
3. `widgets.create` each validated widget → capture returned DON IDs.
4. Assemble dashboard JSON referencing those widget IDs.
5. Validate the dashboard structure (hooks: structural + semantic checks).
6. Create the dashboard on the platform (validate-then-create call).
7. Result: live dashboard with persisted DON IDs.

---

## Manual builder surfaces (JSON editors)

- Widget preview: `https://app.devrev.ai/<org-slug>/widget-preview`
- Dashboard preview: `https://app.devrev.ai/<org-slug>/dashboard-preview`

Both are a JSON editor + live preview. The dashboard preview assembles
already-created widgets into a dashboard.

---

## Accuracy notes

- Endpoint field lists here are partial and can change between releases —
  confirm against the current DevRev API reference and the cloned
  `dashboard-dev` skills before relying on any payload.
- `widgets.*` / dashboard endpoints are standard DevRev public REST (Widgets /
  Vistas area), distinct from AI agents / workflows / AirSync connectors.
