# Auth Tokens

Source: <https://developer.devrev.ai/api-reference/auth-tokens>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/auth-tokens.create` | [create](#create) |
| POST | `/auth-tokens.delete` | [delete](#delete) |
| GET | `/auth-tokens.get` | [get](#get) |
| POST | `/auth-tokens.get` | [get-post](#get-post) |
| GET | `/auth-tokens.info` | [info](#info) |
| POST | `/auth-tokens.info` | [info-post](#info-post) |
| GET | `/auth-tokens.list` | [list](#list) |
| POST | `/auth-tokens.list` | [list-post](#list-post) |
| POST | `/auth-tokens.self.delete` | [self-delete](#self-delete) |
| POST | `/auth-tokens.update` | [update](#update) |

<a id="create"></a>

## `POST /auth-tokens.create`

**Create Auth Token**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/create>

Creates a JWT corresponding to the requested token type for the authenticated user.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `act_as` | no | `string` | The unique ID of the Dev user or the service account to impersonate.<br>*Format: id* |
| `aud` | no | `array<string>` | The expected audience values with respect to the token. |
| `client_id` | no | `string` | An identifier that represents the application which is requesting the token. If no client_id is present in the request to generate an application access token (AAT), DevRev will generate a client_id. This client_id is only associated with an AAT.<br>*Format: text* |
| `expires_in` | no | `integer` | The expected validity lifetime of the token in number of days. The value must be less than or equal to 1825 days (5 years).<br>*Range: 0 <= value <= 1825* |
| `expires_in_mins` | no | `integer` | The expected validity lifetime of the token in number of minutes. The value must be less than or equal to 1440 minutes (1 day).<br>*Range: 0 <= value <= 1440* |
| `grant_type` | no | `string` | Specifies the process of obtaining a token.<br>*Value in: "urn:devrev:params:oauth:grant-type:token-issue" \| "urn:ietf:params:oauth:grant-type:token-exchange"* |
| `requested_token_type` | no | `string` | The type of the requested token.<br>*Value in: "urn:devrev:params:oauth:token-type:aat" \| "urn:devrev:params:oauth:token-type:aat:act-as" \| "urn:devrev:params:oauth:token-type:aat:public" \| "urn:devrev:params:oauth:token-type:dev" \| "urn:devrev:params:oauth:token-type:dev:act-as:agent" \| "urn:devrev:params:oauth:token-type:dev:connect" \| "urn:devrev:params:oauth:token-type:gat" \| "urn:devrev:params:oauth:token-type:pat" \| "urn:devrev:params:oauth:token-type:pat:act-as" \| "urn:devrev:params:oauth:token-type:rat" \| "urn:devrev:params:oauth:token-type:rev" \| "urn:devrev:params:oauth:token-type:session" \| "urn:devrev:params:oauth:token-type:session:dev" \| "urn:devrev:params:oauth:token-type:session:dev0" \| "urn:devrev:params:oauth:token-type:session:onetime" \| "urn:devrev:params:oauth:token-type:session:rev" \| "urn:devrev:params:oauth:token-type:session:rev:act-as" \| "urn:devrev:params:oauth:token-type:session:rev:public" \| "urn:devrev:params:oauth:token-type:super" \| "urn:devrev:params:oauth:token-type:sys" \| "urn:ietf:params:oauth:token-type:jwt"* |
| `rev_info` | no | `auth-tokens-rev-info` | Carries info corresponding to the Rev user to be provisioned and/or issue a Rev session token. |
| `scope` | no | `string` | The requested set of scopes associated with the issued token. A space-delimited list of values in which the order of values does not matter.<br>*Format: text* |
| `subject_token` | no | `string` | Represents the entity that requests the token. Not required when requesting an application access token (AAT).<br>*Format: text* |
| `subject_token_type` | no | `string` | The type of the subject token.<br>*Value in: "urn:devrev:params:oauth:token-type:jwt:auth0" \| "urn:devrev:params:oauth:token-type:jwt:dev" \| "urn:devrev:params:oauth:token-type:rat" \| "urn:devrev:params:oauth:token-type:rev" \| "urn:devrev:params:oauth:token-type:revinfo" \| "urn:devrev:params:oauth:token-type:session" \| "urn:devrev:params:oauth:token-type:sysu" \| "urn:devrev:params:oauth:token-type:userinfo" \| "urn:ietf:params:oauth:token-type:jwt"* |
| `token_hint` | no | `string` | A hint that identifies the token.<br>*Format: text* |

### Response codes

- `201` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `409` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/auth-tokens.create" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 201 response</summary>

```json
{
  "access_token": "string",
  "client_id": "string",
  "expires_in": 0,
  "refresh_token": "string",
  "scope": "string",
  "token_type": "bearer"
}
```

</details>


<a id="delete"></a>

## `POST /auth-tokens.delete`

**Delete Auth Token**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/delete>

Revokes the token that matches the given token ID issued under the given Dev organization.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `token_id` | no | `string` | The unique identifier for the token under a given Dev organization. If no token ID is provided, then the token ID will be set from the JTI claim of the token in the authorization header.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/auth-tokens.delete" \
  -H "Content-Type: application/json" \
  -d '{}'
```


<a id="get"></a>

## `GET /auth-tokens.get`

**Get Auth Token**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/get>

Gets the token metadata corresponding to the given token ID under the given Dev organization.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `token_id` | yes | `string` | The unique identifier of the token under a given Dev organization.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/auth-tokens.get?token_id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "token": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "client_id": "string",
    "expires_at": "2023-01-01T12:00:00.000Z",
    "issued_at": "2023-01-01T12:00:00.000Z",
    "requested_token_type": "urn:devrev:params:oauth:token-type:aat",
    "scopes": [
      "string"
    ],
    "status": "active",
    "subject": "string",
    "token_hint": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /auth-tokens.get`

**Get Auth Token (POST)**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/get-post>

Gets the token metadata corresponding to the given token ID under the given Dev organization.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `token_id` | yes | `string` | The unique identifier of the token under a given Dev organization.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/auth-tokens.get" \
  -H "Content-Type: application/json" \
  -d '{
    "token_id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "token": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "client_id": "string",
    "expires_at": "2023-01-01T12:00:00.000Z",
    "issued_at": "2023-01-01T12:00:00.000Z",
    "requested_token_type": "urn:devrev:params:oauth:token-type:aat",
    "scopes": [
      "string"
    ],
    "status": "active",
    "subject": "string",
    "token_hint": "string"
  }
}
```

</details>


<a id="info"></a>

## `GET /auth-tokens.info`

**Info Auth Tokens**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/info>

Returns the Dev organization, user and token attributes extracted from the auth token.

**Required scopes:** No scopes required.

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
curl -X GET "https://api.devrev.ai/auth-tokens.info"
```

<details><summary>Example 200 response</summary>

```json
{
  "organization": {
    "display_id": "string",
    "id": "DEV-AbCdEfGh",
    "slug": "string"
  },
  "token": {
    "expiry": 0,
    "issued_at": 0,
    "issuer": "string",
    "subject": "string"
  },
  "user": {
    "type": "dev_user",
    "display_id": "string",
    "display_name": "string",
    "email": "string",
    "full_name": "string",
    "id": "string"
  }
}
```

</details>


<a id="info-post"></a>

## `POST /auth-tokens.info`

**Info Auth Tokens (POST)**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/info-post>

Returns the Dev organization, user and token attributes extracted from the auth token.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `[key: string]` | no | `never` |  |

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
curl -X POST "https://api.devrev.ai/auth-tokens.info" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "organization": {
    "display_id": "string",
    "id": "DEV-AbCdEfGh",
    "slug": "string"
  },
  "token": {
    "expiry": 0,
    "issued_at": 0,
    "issuer": "string",
    "subject": "string"
  },
  "user": {
    "type": "dev_user",
    "display_id": "string",
    "display_name": "string",
    "email": "string",
    "full_name": "string",
    "id": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /auth-tokens.list`

**List Auth Tokens**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/list>

Gets the token metadata for all the tokens corresponding to the given token type issued for a given subject.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `client_id` | no | `string` | An identifier that represents the application, which requested the token. Only relevant for application access tokens.<br>*Format: text* |
| `requested_token_type` | no | `string` | The type of the requested token. If no value is specified, the response will include tokens of all the types.<br>*Value in: "urn:devrev:params:oauth:token-type:aat" \| "urn:devrev:params:oauth:token-type:aat:act-as" \| "urn:devrev:params:oauth:token-type:aat:public" \| "urn:devrev:params:oauth:token-type:dev" \| "urn:devrev:params:oauth:token-type:dev:act-as:agent" \| "urn:devrev:params:oauth:token-type:dev:connect" \| "urn:devrev:params:oauth:token-type:gat" \| "urn:devrev:params:oauth:token-type:pat" \| "urn:devrev:params:oauth:token-type:pat:act-as" \| "urn:devrev:params:oauth:token-type:rat" \| "urn:devrev:params:oauth:token-type:rev" \| "urn:devrev:params:oauth:token-type:session" \| "urn:devrev:params:oauth:token-type:session:dev" \| "urn:devrev:params:oauth:token-type:session:dev0" \| "urn:devrev:params:oauth:token-type:session:onetime" \| "urn:devrev:params:oauth:token-type:session:rev" \| "urn:devrev:params:oauth:token-type:session:rev:act-as" \| "urn:devrev:params:oauth:token-type:session:rev:public" \| "urn:devrev:params:oauth:token-type:super" \| "urn:devrev:params:oauth:token-type:sys" \| "urn:ietf:params:oauth:token-type:jwt"* |
| `subject` | no | `string` | The subject associated with the token. In the absence of this parameter, the ID of the authenticated entity is treated as the subject.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/auth-tokens.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "tokens": [
    {
      "created_by": {
        "type": "dev_user",
        "display_id": "string",
        "id": "string",
        "display_name": "string",
        "display_picture": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "email": "string",
        "full_name": "string",
        "state": "active"
      },
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {
        "type": "dev_user",
        "display_id": "string",
        "id": "string",
        "display_name": "string",
        "display_picture": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "email": "string",
        "full_name": "string",
        "state": "active"
      },
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object_version": 0,
      "client_id": "string",
      "expires_at": "2023-01-01T12:00:00.000Z",
      "issued_at": "2023-01-01T12:00:00.000Z",
      "requested_token_type": "urn:devrev:params:oauth:token-type:aat",
      "scopes": [
        "string"
      ],
      "status": "active",
      "subject": "string",
      "token_hint": "string"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /auth-tokens.list`

**List Auth Tokens (POST)**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/list-post>

Gets the token metadata for all the tokens corresponding to the given token type issued for a given subject.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `client_id` | no | `string` | An identifier that represents the application, which requested the token. Only relevant for application access tokens.<br>*Format: text* |
| `requested_token_type` | no | `string` | The type of the requested token.<br>*Value in: "urn:devrev:params:oauth:token-type:aat" \| "urn:devrev:params:oauth:token-type:aat:act-as" \| "urn:devrev:params:oauth:token-type:aat:public" \| "urn:devrev:params:oauth:token-type:dev" \| "urn:devrev:params:oauth:token-type:dev:act-as:agent" \| "urn:devrev:params:oauth:token-type:dev:connect" \| "urn:devrev:params:oauth:token-type:gat" \| "urn:devrev:params:oauth:token-type:pat" \| "urn:devrev:params:oauth:token-type:pat:act-as" \| "urn:devrev:params:oauth:token-type:rat" \| "urn:devrev:params:oauth:token-type:rev" \| "urn:devrev:params:oauth:token-type:session" \| "urn:devrev:params:oauth:token-type:session:dev" \| "urn:devrev:params:oauth:token-type:session:dev0" \| "urn:devrev:params:oauth:token-type:session:onetime" \| "urn:devrev:params:oauth:token-type:session:rev" \| "urn:devrev:params:oauth:token-type:session:rev:act-as" \| "urn:devrev:params:oauth:token-type:session:rev:public" \| "urn:devrev:params:oauth:token-type:super" \| "urn:devrev:params:oauth:token-type:sys" \| "urn:ietf:params:oauth:token-type:jwt"* |
| `subject` | no | `string` | The subject associated with the token. In the absence of this parameter, the ID of the authenticated entity is treated as the subject.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/auth-tokens.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "tokens": [
    {
      "created_by": {
        "type": "dev_user",
        "display_id": "string",
        "id": "string",
        "display_name": "string",
        "display_picture": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "email": "string",
        "full_name": "string",
        "state": "active"
      },
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {
        "type": "dev_user",
        "display_id": "string",
        "id": "string",
        "display_name": "string",
        "display_picture": {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        },
        "email": "string",
        "full_name": "string",
        "state": "active"
      },
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object_version": 0,
      "client_id": "string",
      "expires_at": "2023-01-01T12:00:00.000Z",
      "issued_at": "2023-01-01T12:00:00.000Z",
      "requested_token_type": "urn:devrev:params:oauth:token-type:aat",
      "scopes": [
        "string"
      ],
      "status": "active",
      "subject": "string",
      "token_hint": "string"
    }
  ]
}
```

</details>


<a id="self-delete"></a>

## `POST /auth-tokens.self.delete`

**Delete Auth Tokens Self**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/self-delete>

Revokes all the tokens that matches the given token type created by the authenticated user.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `requested_token_type` | no | `string` | The type of the requested token.<br>*Value in: "urn:devrev:params:oauth:token-type:aat" \| "urn:devrev:params:oauth:token-type:aat:act-as" \| "urn:devrev:params:oauth:token-type:aat:public" \| "urn:devrev:params:oauth:token-type:dev" \| "urn:devrev:params:oauth:token-type:dev:act-as:agent" \| "urn:devrev:params:oauth:token-type:dev:connect" \| "urn:devrev:params:oauth:token-type:gat" \| "urn:devrev:params:oauth:token-type:pat" \| "urn:devrev:params:oauth:token-type:pat:act-as" \| "urn:devrev:params:oauth:token-type:rat" \| "urn:devrev:params:oauth:token-type:rev" \| "urn:devrev:params:oauth:token-type:session" \| "urn:devrev:params:oauth:token-type:session:dev" \| "urn:devrev:params:oauth:token-type:session:dev0" \| "urn:devrev:params:oauth:token-type:session:onetime" \| "urn:devrev:params:oauth:token-type:session:rev" \| "urn:devrev:params:oauth:token-type:session:rev:act-as" \| "urn:devrev:params:oauth:token-type:session:rev:public" \| "urn:devrev:params:oauth:token-type:super" \| "urn:devrev:params:oauth:token-type:sys" \| "urn:ietf:params:oauth:token-type:jwt"* |

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
curl -X POST "https://api.devrev.ai/auth-tokens.self.delete" \
  -H "Content-Type: application/json" \
  -d '{}'
```


<a id="update"></a>

## `POST /auth-tokens.update`

**Update Auth Token**

Source: <https://developer.devrev.ai/api-reference/auth-tokens/update>

Updates token metadata of a token issued under a given Dev organization.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `token_hint` | yes | `string` | A hint that identifies the token.<br>*Format: text* |
| `token_id` | yes | `string` | The unique identifier of the token under a given Dev organization.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/auth-tokens.update" \
  -H "Content-Type: application/json" \
  -d '{
    "token_hint": "string",
    "token_id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "token": {
    "created_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "created_date": "2023-01-01T12:00:00.000Z",
    "display_id": "string",
    "id": "string",
    "modified_by": {
      "type": "dev_user",
      "display_id": "string",
      "id": "string",
      "display_name": "string",
      "display_picture": {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      },
      "email": "string",
      "full_name": "string",
      "state": "active"
    },
    "modified_date": "2023-01-01T12:00:00.000Z",
    "object_version": 0,
    "client_id": "string",
    "expires_at": "2023-01-01T12:00:00.000Z",
    "issued_at": "2023-01-01T12:00:00.000Z",
    "requested_token_type": "urn:devrev:params:oauth:token-type:aat",
    "scopes": [
      "string"
    ],
    "status": "active",
    "subject": "string",
    "token_hint": "string"
  }
}
```

</details>
