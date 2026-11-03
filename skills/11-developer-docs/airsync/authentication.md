# Configure connections and authentication

Source: <https://developer.devrev.ai/airsync/authentication>
Scraped: 2026-11-03

## Worker connection contract

The SDK exposes `event.payload.connection_data` with these fields:

| Field      | Meaning                                             |
| ---------- | --------------------------------------------------- |
| `key`      | Credential supplied by the connection configuration |
| `key_type` | Credential type                                     |
| `org_id`   | Selected external organization/account identifier   |
| `org_name` | Selected external organization/account display name |

Use `key` only in the external client's authenticated requests. The external API determines whether it is a bearer token, API key or another format. Do not infer its authorization header from `key_type` alone. Construct the API base URL from verified connection/configuration data and the external API's contract.

## Secret connection example

This example uses an API token and requires an external subdomain. Replace the fictional hostname with your service's authenticated verification endpoint before deployment.

```yaml
keyring_types:
  - id: example-pat
    name: Example Connection
    description: Authenticate with Example
    external_system_name: Example
    kind: "Secret"
    is_subdomain: true
    secret_config:
      fields:
        - id: token
          name: API token
          description: Token with permission to read the selected workspace
      secret_transform: ".token"
      token_verification:
        url: "https://[SUBDOMAIN].example.com/v1/me"
        method: GET
        headers:
          Authorization: "Bearer [API_KEY]"
```

`secret_transform` selects the credential from the user's supplied secret fields. The configured verification request must test that credential. A public unauthenticated URL validates neither the token nor its scopes. Match the keyring ID with `imports[].allowed_connection_types`.

Set `is_subdomain` when the API uses a user-selected external subdomain. If users need to select an external organization, configure `organization_data` alongside `secret_config`, as shown in the public [Asana keyring](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/manifest.yaml#L90-L109). The discovery response identifies the external organization; it is not a DevRev organization ID.

## Permission requirements

Document external read permissions for sync-unit discovery, metadata, users, records and attachment downloads. Add external write permissions only for implemented reverse-sync operations. Explain what happens to inaccessible/private records and how changes in permission affect later syncs.

The [manifest service-account scopes](manifest.md#service-account-permissions) authorize DevRev operations. They do not increase the external token's access. Likewise, an external admin token does not grant DevRev permissions. Importing access rules is a separate [data-model capability](data-model/permissions.md).

## Failure behavior and verification

Treat an expired or revoked token as a credential failure, rather than retrying indefinitely. Distinguish it from API rate limiting and temporary server failures. Return SDK outcomes through the [runtime contract](runtime.md) and never include the credential in an error message.

Verify valid credentials, invalid credentials, expired/revoked credentials, insufficient scopes and a user who can access only some sync units. Test OAuth renewal for the configured provider. For attachments, also test credentials or signed URLs used by the download endpoint; access to a record does not guarantee access to its files.

Do not log raw events, request headers or serialized clients. Use sanitized fixtures and test secrets in [local development](local-development.md).

## OAuth and developer keyrings

Configure OAuth credentials and developer keyrings for the external system when token authentication is insufficient.

Prefer OAuth when the external service supports it and the integration's scopes can be granted through its authorization flow. Configure authorization/token endpoints, requested scopes, token verification and organization discovery according to the [OAuth keyring reference](../snapin-development/references/keyrings/oauth-configuration.md). The connection manages the configured OAuth credential lifecycle; workers still need to handle revoked access, changed scopes and failed external requests.

Publisher-owned OAuth client secrets belong in developer keyrings referenced by the manifest, not in source files or users' token fields. Create referenced developer keyrings in the deployment organization before creating the snap-in version. See the [developer keyring reference](../snapin-development/references/keyrings/developer-keyring.md) for creation and manifest binding. Keep the OAuth client/redirect configuration consistent with the environment where users will install the connector.

Next: [Choose connector capabilities](connector-capabilities.md).
