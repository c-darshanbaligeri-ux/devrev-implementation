# Safety: what is destructive, and what to do first

Moved here from the repo's `CLAUDE.md`. The safety hook classifies every `curl` to the DevRev API: **read** calls run without a prompt, **write** calls ask the user, **destructive** calls ask loudly. You still state the impact yourself and get explicit confirmation **in this session** before anything on this list. The evidence for each fact is in the owning skill's Field notes (named below).

## Treat as destructive or irreversible

| Operation | Why, and what to do |
| --- | --- |
| Any `*.delete` | `works.delete`, `custom-objects.delete`, `workflows.delete`, `tags.delete` and `links.delete` all genuinely work (HTTP 200 `{}`, then `.get` 404s), so records are not "permanent by default". Treat each as a real delete. |
| Bulk deletes driven by a `*.list` / `*.count` | The matching set can grow under live automation. Snapshot the full id set into a manifest file first, then delete exactly that manifest. |
| `*.merge` (accounts, works) | Not undoable. |
| `states.custom.create`, `stages.custom.create` | Permanent: `stages.custom.delete` / `states.custom.delete` return 404 and no deprecation field is accepted on `.update`. Only manual UI cleanup removes them. Prefer listing and reusing existing ids (skill 2). |
| Retiring a stage in a diagram | `is_deprecated: true` on a stage node is rejected (HTTP 400) at both `stage-diagrams.create` and `.update`. No working way to retire a stage exists in the public API, so every stage added to a diagram is permanent for its lifetime (skill 2). |
| `schemas.custom.set` | A **versioned create**: two calls with the same `leaf_type` make two fragments and nothing deletes them. Run `schemas.custom.list` first (for a custom leaf type pass `is_custom_leaf_type: true`; a bare list or a `leaf_type`-only filter returns zero rows, which looks like "no fragment" and invites a duplicate). `id_prefix` must match `^[A-Z]{2,10}$` and `leaf_type` `[a-z_]+` or you get HTTP 400. If a tenant fragment already exists, `.set` must replay the COMPLETE existing `fields` array plus the new fields; a partial replay returns 400 with no field name, so `schemas.custom.get` first (skill 1). |
| Retiring a custom fragment | `schemas.custom.set` with `deprecated: true` and a full field replay works and acts like a delete for that leaf type: `custom-objects.create` then fails with "no tenant fragment found" and the fragment disappears from `schemas.custom.list` (skill 1). |
| `objects.bulk-upgrade` | Internal-only (`/internal/objects.bulk-upgrade`); touches every record of a type org-wide. |
| Custom link types | Deprecate only, via `link-types.custom.update` with `deprecated: true`. |
| `web-crawler-jobs.control` (`stop` / `reset`) | Cannot be resumed. |
| Dataset or PaaS/Ponos job deletion | Destructive via `/dataset-builder:delete` (skill 5). |
| `devrev snap_in_version delete-one` | Needed before a new version (one non-published version per package) but destroys that version's state (skill 9). |

## High impact: writes that change what a live automation does

These are ordinary writes (the hook always asks), but the prompt says HIGH IMPACT because they act on live automation. State the target org and what will change, and get the user's yes in this session first. A plain `devrev-import-workflow` run only creates a **draft** and asks like any other write; `--dry-run` and `devrev-validate-workflow` change nothing and run without a prompt.

| Operation | Why |
| --- | --- |
| `workflows.update-status` (`active` / `inactive`) | Publishes a new workflow and switches it on, or switches a live one off. |
| `workflow-versions.publish` | Publishes a new version of a workflow that is already live. |
| `workflows.templates.instantiate` with `override_draft: true` | Replaces the workflow's existing draft; look at the draft first. |
| `devrev-import-workflow --publish`, `--attach-connection`, `--override-draft` | The same three actions, wrapped by the import script (which makes its API calls from inside Python, so the hook matches the script and its flags). It publishes only after server-side validation succeeds. |

## Always

- **Verify after any change** with the matching read endpoint (`*.get`, `*.list`, or `schemas.aggregated.get`). If custom fields or fragments were involved, re-read an affected record and confirm the fields appear.
- **Never commit `.env`** (it is gitignored) and never write a real PAT anywhere except `.env`. In notes or logs write `<REDACTED_PAT>`.
- **Never record** real org ids, customer names or local paths in the repo (use `<ORG_ID>`, "a customer", `<workspace>/`).
