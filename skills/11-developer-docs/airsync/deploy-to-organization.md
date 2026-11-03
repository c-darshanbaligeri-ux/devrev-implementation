# Deploy to a test organization

Source: <https://developer.devrev.ai/airsync/deploy-to-organization>
Scraped: 2026-11-03

## Preconditions

Use the [public DevRev CLI](../snapin-development/references/cli-install.md), Node.js 20 or newer and an organization where your account can create and install snap-ins. Complete [validation](validation.md), configure a real [connection type](authentication.md) and declare only implemented capabilities in the [manifest](manifest.md).

Install the public CLI on macOS/Linux if needed:

```bash
npm install -g devrev
devrev --version
devrev profiles authenticate --org YOUR_ORG_SLUG
```

Use the CLI installation reference for Windows. Run deployment commands against the intended organization/profile. Create any developer keyrings referenced by the manifest in that organization before creating a version.

## Create and activate a built version

From `code/`, validate the build and your connector tests. The checked template has no matching unit tests until you add them:

```bash
npm ci
npm run build
npm run lint
npm test -- --runInBand
```

From the project root containing `manifest.yaml` and `code/`:

```bash
devrev snap_in_version create-one --path . --create-package
```

The CLI builds and packages the snap-in. Record the returned package and version IDs. Check the version rather than assuming creation means it is ready:

```bash
devrev snap_in_version show YOUR_VERSION_ID
```

Proceed once its state is `ready`. For `build_failed` or `deployment_failed`, inspect `failure_reason` and fix the underlying problem. Create a draft for the ready version and activate the returned snap-in:

```bash
devrev snap_in draft --snap_in_version YOUR_VERSION_ID
devrev snap_in activate YOUR_SNAP_IN_ID
```

Configure the external connection and start an import in the DevRev AirSync interface. Verify a small test sync before using production data. The public template also offers `npm run deploy` from `code/`; review its interactive deployment choices and target organization before running it.

## Observe the deployed connector

```bash
devrev snap_in_package logs YOUR_PACKAGE_ID --follow
```

Correlate logs with the sync unit and phase. Check the AirSync run status, record/error counts, attachment visibility and external-system state. Keep access tokens, raw events and credential-bearing URLs out of logs. See [snap-in debugging](../snapin-development/debugging.md) and [AirSync troubleshooting](faq.md).

## Upgrade an existing connector

Keep package and import identities stable when upgrading an existing connector. Test existing imports and persisted state.

For an unpublished snap-in installation, keep the package/import identity stable and use the CLI's compatible upgrade operation from the project root:

```bash
devrev snap_in_version upgrade YOUR_EXISTING_VERSION_ID --path .
```

The current public CLI takes the existing version ID as a positional argument; confirm the syntax with `devrev snap_in_version upgrade --help` if using another release. A compatible upgrade creates the replacement version and upgrades the installed snap-in. Check the package's version list and installation after completion:

```bash
devrev snap_in_version list
devrev snap_in show YOUR_SNAP_IN_ID
```

Do not use `--force` as a routine retry: an incompatible forced upgrade can delete the existing snap-in. Review changed connections, inputs and service-account scopes before proceeding. Validate existing imports as well as a fresh installation: state, mappings, connections and external IDs must remain compatible. See the [snap-in upgrade reference](../snapin-development/upgrade-snap-ins.md).

To create a separate new version in an existing package without upgrading its installation, use `devrev snap_in_version create-one --path . --package YOUR_PACKAGE_ID`. Version creation and installation upgrade are distinct operations.

Before deploying code that changes connector state or mappings, document how existing values migrate and test with representative persisted state. Finish active runs before a v1-to-v2 upgrade; see [SDK migration](sdk-migration.md). Rollback requires compatible persisted state, not merely an older code archive.

For marketplace installations, publish a new item for the existing listing. Automatic upgrade requires an update that does not require new user input, global variables or connections; see [marketplace publication](publish-to-marketplace.md).

Next: [Verify a live data import](live-extraction-testing.md).
