# Coverage — site endpoints vs. skills/8-devrev-api catalog

Scraped: 2026-11-03

- Public endpoints on the site: **212** (unique names; GET/POST pairs counted once)
- Beta endpoints on the site: **302**

- Names found in `00_API_Catalog.md`: **187**

## On the public site but not in the catalog (30)

Not listed *by name in a table row* of `00_API_Catalog.md`. Many are documented in other skill references instead (custom objects, schemas, stage diagrams in skills 1–2; `ping` in the root `CLAUDE.md`), so `grep -rF '<name>' skills/` before treating one as a real knowledge gap. Verify live before adding anything to the catalog.

- `custom-objects.count`
- `custom-objects.create`
- `custom-objects.delete`
- `custom-objects.get`
- `custom-objects.update`
- `dev-orgs.auth-connections.create`
- `dev-orgs.auth-connections.delete`
- `dev-orgs.auth-connections.get`
- `dev-orgs.auth-connections.list`
- `dev-orgs.auth-connections.toggle`
- `dev-orgs.auth-connections.update`
- `ping`
- `schemas.aggregated.get`
- `schemas.custom.get`
- `schemas.custom.set`
- `schemas.stock.get`
- `schemas.stock.list`
- `schemas.subtypes.prepare-update`
- `stage-diagrams.create`
- `stage-diagrams.get`
- `stage-diagrams.list`
- `stage-diagrams.update`
- `stages.custom.create`
- `stages.custom.get`
- `stages.custom.list`
- `stages.custom.update`
- `states.custom.create`
- `states.custom.get`
- `states.custom.list`
- `states.custom.update`

## In the catalog but not on the public site (5)

Internal, beta-only (marked below), renamed or removed endpoints. The catalog is live-verified in places where the docs are not — do not delete anything from it on this evidence alone.

- `link-types.custom.create` (beta page exists)
- `link-types.custom.get` (beta page exists)
- `link-types.custom.list` (beta page exists)
- `link-types.custom.update` (beta page exists)
- `objects.bulk-upgrade`
