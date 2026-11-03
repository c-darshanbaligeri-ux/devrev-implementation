# Troubleshoot deployment

Source: <https://developer.devrev.ai/airsync/deployment-troubleshooting>
Scraped: 2026-11-03

Use these checks when the connector fails during deployment.

## Deployment version never becomes ready

Inspect the created version and its failure reason:

```bash
devrev snap_in_version show YOUR_VERSION_ID
devrev snap_in_package logs YOUR_PACKAGE_ID
```

Check TypeScript/build errors, missing dependencies, manifest/function export mismatches and missing developer keyrings. A successfully created package does not imply a successfully built version. See [deployment](deploy-to-organization.md).

## Package slug conflict

Identify whether you intend to upgrade an existing package or create a new connector. For an upgrade, pass the existing package ID to version creation. For a new package, use a unique package slug. Do not delete a package with active imports merely to clear a naming conflict.

## CLI token expired or wrong organization selected

Reauthenticate to the intended organization:

```bash
devrev profiles authenticate --org YOUR_ORG_SLUG
```

This refreshes DevRev developer access. It does not refresh the external connection token. Check the active CLI profile/environment before creating or modifying a version.

Related: [troubleshooting index](faq.md).
