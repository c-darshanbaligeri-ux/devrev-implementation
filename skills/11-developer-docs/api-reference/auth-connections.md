# Auth Connections

Source: <https://developer.devrev.ai/api-reference/auth-connections>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/dev-orgs.auth-connections.create` | [dev-org-auth-connections-create](#dev-org-auth-connections-create) |
| POST | `/dev-orgs.auth-connections.delete` | [dev-org-auth-connections-delete](#dev-org-auth-connections-delete) |
| GET | `/dev-orgs.auth-connections.get` | [dev-org-auth-connections-get](#dev-org-auth-connections-get) |
| POST | `/dev-orgs.auth-connections.get` | [dev-org-auth-connections-get-post](#dev-org-auth-connections-get-post) |
| GET | `/dev-orgs.auth-connections.list` | [dev-org-auth-connections-list](#dev-org-auth-connections-list) |
| POST | `/dev-orgs.auth-connections.list` | [dev-org-auth-connections-list-post](#dev-org-auth-connections-list-post) |
| POST | `/dev-orgs.auth-connections.toggle` | [dev-org-auth-connections-toggle](#dev-org-auth-connections-toggle) |
| POST | `/dev-orgs.auth-connections.update` | [dev-org-auth-connections-update](#dev-org-auth-connections-update) |

<a id="dev-org-auth-connections-create"></a>

## `POST /dev-orgs.auth-connections.create`

**Create Dev Orgs Auth Connection**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-create>

Creates a new enterprise authentication connection for a Dev organization. This authentication connection will not be enabled by default for the organization and the user will need to explicitly enable this. Only 5 authentication connections can be created by an organization.

**Required scopes:** Cannot be called via service account.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `dev-org-auth-connections-create-request-azure-ad-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | Defines the type for the authentication connection. Different types of authentication connections have different configuration parameters.<br>*Value in: "google_apps" \| "oidc" \| "okta" \| "samlp" \| "waad"* |
| `display_name` | no | `string` | Display name of the authentication connection. This name will be visible to all the users when they sign in to this Dev organization. For example, if the display_name is 'abclogin', then it would appear on the login button as 'Log in to abclogin'.<br>*Format: text*<br>*Length: 1 <= length <= 128* |
| `client_id` | yes | `string` | Client ID for the Azure authentication connection.<br>*Format: text* |
| `client_secret` | yes | `string` | Client secret for the Azure authentication connection.<br>*Format: text* |
| `domain` | yes | `string` | Domain URL of the Azure authentication connection.<br>*Format: text* |

#### Variant `dev-org-auth-connections-create-request-google-apps-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-create-request-oidc-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-create-request-okta-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-create-request-saml-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.create" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "google_apps",
    "client_id": "string",
    "client_secret": "string",
    "domain": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "auth_connection": {
    "type": "google_apps",
    "display_name": "string",
    "enabled": true,
    "id": "string",
    "client_id": "string",
    "domain": "string"
  }
}
```

</details>


<a id="dev-org-auth-connections-delete"></a>

## `POST /dev-orgs.auth-connections.delete`

**Delete Dev Orgs Auth Connection**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-delete>

Deletes an authentication connection. Only enterprise connections which are explicitly set up for a Dev organization can be deleted. Default connections can not be deleted using this method.

**Required scopes:** Cannot be called via service account.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the authentication connection to be deleted.<br>*Format: text* |

### Response codes

- `200` — empty body
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```


<a id="dev-org-auth-connections-get"></a>

## `GET /dev-orgs.auth-connections.get`

**Get Dev Orgs Auth Connection**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-get>

Retrieves the details for an authentication connection.

**Required scopes:**

- `Cannot be called via service account.`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the authentication connection.<br>*Format: text* |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X GET "https://api.devrev.ai/dev-orgs.auth-connections.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "auth_connection": {
    "type": "google_apps",
    "display_name": "string",
    "enabled": true,
    "id": "string",
    "client_id": "string",
    "domain": "string"
  }
}
```

</details>


<a id="dev-org-auth-connections-get-post"></a>

## `POST /dev-orgs.auth-connections.get`

**Get Dev Orgs Auth Connection (POST)**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-get-post>

Retrieves the details for an authentication connection.

**Required scopes:**

- `Cannot be called via service account.`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the authentication connection.<br>*Format: text* |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "auth_connection": {
    "type": "google_apps",
    "display_name": "string",
    "enabled": true,
    "id": "string",
    "client_id": "string",
    "domain": "string"
  }
}
```

</details>


<a id="dev-org-auth-connections-list"></a>

## `GET /dev-orgs.auth-connections.list`

**List Dev Orgs Auth Connections**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-list>

Lists all the authentication connections available for a Dev organization. This list will include both social and enterprise connections which are either available by default or are explicitly created by the user.

**Required scopes:** Cannot be called via service account.

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X GET "https://api.devrev.ai/dev-orgs.auth-connections.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "auth_connections": [
    {
      "type": "google_apps",
      "display_name": "string",
      "enabled": true,
      "id": "string",
      "client_id": "string",
      "domain": "string"
    }
  ]
}
```

</details>


<a id="dev-org-auth-connections-list-post"></a>

## `POST /dev-orgs.auth-connections.list`

**List Dev Orgs Auth Connections (POST)**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-list-post>

Lists all the authentication connections available for a Dev organization. This list will include both social and enterprise connections which are either available by default or are explicitly created by the user.

**Required scopes:** Cannot be called via service account.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `[key: string]` | no | `never` |  |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "auth_connections": [
    {
      "type": "google_apps",
      "display_name": "string",
      "enabled": true,
      "id": "string",
      "client_id": "string",
      "domain": "string"
    }
  ]
}
```

</details>


<a id="dev-org-auth-connections-toggle"></a>

## `POST /dev-orgs.auth-connections.toggle`

**Toggle Dev Orgs Auth Connections**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-toggle>

Enable or disable an authentication connection for a Dev organization. Atleast one authentication connection must be enabled for a Dev organization.

**Required scopes:** Cannot be called via service account.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the authentication connection to be toggled.<br>*Format: text* |
| `toggle` | no | `string` | *Value in: "disable" \| "enable"* |

### Response codes

- `200` — empty body
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.toggle" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```


<a id="dev-org-auth-connections-update"></a>

## `POST /dev-orgs.auth-connections.update`

**Update Dev Orgs Auth Connection**

Source: <https://developer.devrev.ai/api-reference/auth-connections/dev-org-auth-connections-update>

Updates an authentication connection.

**Required scopes:** Cannot be called via service account.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `dev-org-auth-connections-update-request-azure-ad-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | no | `string` | Specifies the type for the authentication connection. Different types of authentication connections have different configuration parameters that can be updated.<br>*Value in: "google_apps" \| "none" \| "oidc" \| "okta" \| "samlp" \| "waad"* |
| `display_name` | no | `string` | New display name of the authentication connection. This name will be visible to all the users when they sign in to this Dev organization. For example, if the display_name is 'abclogin', then it would appear on the login button as 'Log in to abclogin'.<br>*Format: text* |
| `id` | yes | `string` | ID of the authentication connection which is to be updated.<br>*Format: text* |
| `client_id` | no | `string` | Client ID for the Azure authentication connection.<br>*Format: text* |
| `client_secret` | no | `string` | Client secret for the Azure authentication connection.<br>*Format: text* |
| `domain` | no | `string` | Domain URL of the Azure authentication connection.<br>*Format: text* |

#### Variant `dev-org-auth-connections-update-request-google-apps-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-update-request-oidc-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-update-request-okta-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `dev-org-auth-connections-update-request-saml-options`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

#### Variant `empty`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/dev-orgs.auth-connections.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "auth_connection": {
    "type": "google_apps",
    "display_name": "string",
    "enabled": true,
    "id": "string",
    "client_id": "string",
    "domain": "string"
  }
}
```

</details>
