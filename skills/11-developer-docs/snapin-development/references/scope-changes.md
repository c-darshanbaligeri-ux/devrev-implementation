# Snap-in scope enforcement

Source: <https://developer.devrev.ai/snapin-development/references/scope-changes>
Scraped: 2026-11-03

Snap-ins now use a scopes-based permissions model. Instead of granting broad system-level access through the systems group, each snap-in must declare the specific permissions its service account needs in the manifest. These permissions are granted at installation time.

## Changes

* **New snap-ins** must define scopes in the manifest before publishing. Without scopes, publishing is blocked.
* **Previously published snap-ins** continue to work without changes.
* **Updates to an existing snap-in** require adding scopes to the manifest before you can republish.

## Install experience

When installing a snap-in, users are prompted to review and grant the permissions the snap-in requests. Installation proceeds only after all required permissions have been accepted.

## Next steps

For complete information on scope syntax, how to declare scopes in your manifest, scope types, best practices, and the full API-to-scope mapping, see [Snap-in scopes](scopes.md).
