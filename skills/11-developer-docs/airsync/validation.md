# Check connector release readiness

Source: <https://developer.devrev.ai/airsync/validation>
Scraped: 2026-11-03

## Record the tested implementation

Record the connector commit, exact installed SDK version, Node version, manifest/import identity, fixture names and test environment. Resolve the latest stable major 2 release when refreshing examples or preparing a release, then commit and test the resulting lockfile.

From `code/`:

```bash
node --version
npm ls @devrev/airsync-sdk
npx tsc --noEmit
npm run lint
npm run build
npm test -- --runInBand
```

If the development server or runner is excluded from the main TypeScript configuration, type-check it separately. Compare failures with the baseline before an SDK upgrade. The checked public template currently includes the Jest command but no matching unit tests, so `npm test` exits with “No tests found.” Add meaningful connector tests before treating this check as passing; do not hide the absence with `--passWithNoTests`.

## Release acceptance

Use the intended installation and permissions without local-only secrets or unpublished tooling. Record unsupported scenarios in the public capability description. Retest existing imports on upgrade, including persisted state and mapping compatibility. When adapting [Asana](snap-in-examples.md), record the source revision and run its checks before changing the integration.

<span id="fixture-inputs-and-observable-outputs" />

<span id="capture-state-for-a-continuation-fixture" />

<span id="unit-test-contracts" />

<span id="live-initial-and-incremental-sync" />

<span id="live-reverse-sync-validation" />

Related:

* [Fixture testing](fixture-testing.md).
* [Continuation testing](continuation-testing.md).
* [Unit testing](unit-testing.md).
* [Live extraction testing](live-extraction-testing.md).
* [Live reverse-sync testing](live-loading-testing.md).

Next: [Publish to the marketplace](publish-to-marketplace.md).
