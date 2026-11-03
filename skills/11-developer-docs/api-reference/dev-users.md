# Dev Users

Source: <https://developer.devrev.ai/api-reference/dev-users>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/dev-users.activate` | [activate](#activate) |
| POST | `/dev-users.create` | [create](#create) |
| POST | `/dev-users.deactivate` | [deactivate](#deactivate) |
| GET | `/dev-users.get` | [get](#get) |
| POST | `/dev-users.get` | [get-post](#get-post) |
| POST | `/dev-users.identities.link` | [identities-link](#identities-link) |
| POST | `/dev-users.identities.unlink` | [identities-unlink](#identities-unlink) |
| GET | `/dev-users.list` | [list](#list) |
| POST | `/dev-users.list` | [list-post](#list-post) |
| POST | `/dev-users.merge` | [merge](#merge) |
| GET | `/dev-users.self` | [self](#self) |
| POST | `/dev-users.self` | [self-post](#self-post) |
| POST | `/dev-users.self.update` | [self-update](#self-update) |
| POST | `/dev-users.update` | [update](#update) |

<a id="activate"></a>

## `POST /dev-users.activate`

**Activate Dev Users**

Source: <https://developer.devrev.ai/api-reference/dev-users/activate>

Activates the requested user.

**Required scopes:**

- `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `groups` | no | `array<string>` | IDs of the groups assigned to user during activation. |
| `id` | yes | `string` | The ID for the Dev user.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/dev-users.activate" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "invite_sent": true
}
```

</details>


<a id="create"></a>

## `POST /dev-users.create`

**Create Dev User**

Source: <https://developer.devrev.ai/api-reference/dev-users/create>

Creates a Dev user for a Dev organization.

**Required scopes:**

- `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `email` | yes | `string` | Email of the Dev user.<br>*Format: text* |
| `full_name` | no | `string` | Full name of the Dev user.<br>*Format: text* |
| `reports_to` | no | `string` | The ID of the user that the user reports to.<br>*Format: id* |
| `state` | yes | `string` | *Value in: "shadow"* |

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
curl -X POST "https://api.devrev.ai/dev-users.create" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "string",
    "state": "shadow"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="deactivate"></a>

## `POST /dev-users.deactivate`

**Deactivate Dev Users**

Source: <https://developer.devrev.ai/api-reference/dev-users/deactivate>

Deactivates the requested user.

**Required scopes:**

- `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID for the Dev user.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/dev-users.deactivate" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get"></a>

## `GET /dev-users.get`

**Get Dev User**

Source: <https://developer.devrev.ai/api-reference/dev-users/get>

Gets the requested user's information.

**Required scopes:**

- `dev_user:read` OR `dev_user:write` OR `dev_user:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | User ID of the requested Dev user.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/dev-users.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /dev-users.get`

**Get Dev User (POST)**

Source: <https://developer.devrev.ai/api-reference/dev-users/get-post>

Gets the requested user's information.

**Required scopes:**

- `dev_user:read` OR `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | User ID of the requested Dev user.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/dev-users.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="identities-link"></a>

## `POST /dev-users.identities.link`

**Link Dev Users Identities**

Source: <https://developer.devrev.ai/api-reference/dev-users/identities-link>

Links an external/secondary identity to the Dev user.

**Required scopes:**

- `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dev_user` | yes | `string` | The ID of the Dev user to link the external identity to.<br>*Format: id* |
| `display_name` | no | `string` | Display name of the Dev user in the external source.<br>*Format: text* |
| `id` | yes | `string` | Unique ID of the Dev user in the external source.<br>*Format: text* |
| `issuer` | yes | `string` | Issuer of the external identity of the Dev user.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/dev-users.identities.link" \
  -H "Content-Type: application/json" \
  -d '{
    "dev_user": "string",
    "id": "string",
    "issuer": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="identities-unlink"></a>

## `POST /dev-users.identities.unlink`

**Unlink Dev Users Identities**

Source: <https://developer.devrev.ai/api-reference/dev-users/identities-unlink>

Unlinks an external/secondary identity from the Dev user.

**Required scopes:**

- `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dev_user` | yes | `string` | The ID of the Dev user to unlink the external identity from.<br>*Format: id* |
| `issuer` | yes | `string` | Issuer that needs to be unlinked from a Dev user.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/dev-users.identities.unlink" \
  -H "Content-Type: application/json" \
  -d '{
    "dev_user": "string",
    "issuer": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /dev-users.list`

**List Dev Users**

Source: <https://developer.devrev.ai/api-reference/dev-users/list>

Lists users within your organization.

**Required scopes:**

- `dev_user:read` OR `dev_user:write` OR `dev_user:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | Filters Dev users based on email addresses. |
| `external_identity.id` | no | `string` | Unique ID of the user in the external source.<br>*Format: text* |
| `external_identity.issuer` | no | `string` | Issuer of the external identity of the user.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of Dev users to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Dev users on. |
| `sort_by` | no | `array<string>` | Fields to sort the Dev users by and the direction to sort them. |
| `staged_info.is_staged` | no | `boolean` | Filters for issues that are staged. |
| `state` | no | `array<user-state>` | Filters Dev users based on state. |
| `timezone` | no | `array<string>` | Filters for Dev users in the specified time zone in IANA format (e.g., 'America/Los_Angeles'). |

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
curl -X GET "https://api.devrev.ai/dev-users.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_users": [
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
      "phone_numbers": [
        "string"
      ],
      "primary_identity": {
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
      "state": "active",
      "availability_modes": [
        {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "experience_start_date": "2023-01-01T12:00:00.000Z",
      "external_identities": [
        {
          "display_name": "string",
          "id": "string",
          "is_verified": true,
          "issuer": "string"
        }
      ],
      "is_invited": true,
      "job_history": [
        {
          "employment_status": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
          "end_date": "2023-01-01T12:00:00.000Z",
          "is_current": true,
          "location": "string",
          "start_date": "2023-01-01T12:00:00.000Z",
          "title": "string"
        }
      ],
      "reports_to": {
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
      "skills": [
        {
          "name": "string"
        }
      ],
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "timezone": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /dev-users.list`

**List Dev Users (POST)**

Source: <https://developer.devrev.ai/api-reference/dev-users/list-post>

Lists users within your organization.

**Required scopes:**

- `dev_user:read` OR `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | Filters Dev users based on email addresses. |
| `external_identity` | no | `array<dev-user-external-identity-filter>` | Filters Dev users based on external identity. |
| `limit` | no | `integer` | The maximum number of Dev users to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Dev users on. |
| `sort_by` | no | `array<string>` | Fields to sort the Dev users by and the direction to sort them. |
| `staged_info` | no | `staged-info-filter` |  |
| `state` | no | `array<user-state>` | Filters Dev users based on state. |
| `timezone` | no | `array<string>` | Filters for Dev users in the specified time zone in IANA format (e.g., 'America/Los_Angeles'). |

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
curl -X POST "https://api.devrev.ai/dev-users.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_users": [
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
      "phone_numbers": [
        "string"
      ],
      "primary_identity": {
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
      "state": "active",
      "availability_modes": [
        {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "experience_start_date": "2023-01-01T12:00:00.000Z",
      "external_identities": [
        {
          "display_name": "string",
          "id": "string",
          "is_verified": true,
          "issuer": "string"
        }
      ],
      "is_invited": true,
      "job_history": [
        {
          "employment_status": {
            "color": "string",
            "id": 0,
            "label": "string",
            "ordinal": 0,
            "value": null
          },
          "end_date": "2023-01-01T12:00:00.000Z",
          "is_current": true,
          "location": "string",
          "start_date": "2023-01-01T12:00:00.000Z",
          "title": "string"
        }
      ],
      "reports_to": {
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
      "skills": [
        {
          "name": "string"
        }
      ],
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "timezone": "string"
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="merge"></a>

## `POST /dev-users.merge`

**Merge Dev Users**

Source: <https://developer.devrev.ai/api-reference/dev-users/merge>

Merges the identity of a secondary Dev user with the primary Dev user. The account of the secondary Dev user will be deactivated and will no longer be able to log into DevRev. All objects - issues, tickets, parts etc. owned by the secondary Dev user will be transferred to the primary Dev user.

**Required scopes:**

- `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `primary_user` | yes | `string` | The unique ID of the primary user.<br>*Format: id* |
| `secondary_user` | yes | `string` | The unique ID of the secondary user.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/dev-users.merge" \
  -H "Content-Type: application/json" \
  -d '{
    "primary_user": "string",
    "secondary_user": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="self"></a>

## `GET /dev-users.self`

**Self Dev User**

Source: <https://developer.devrev.ai/api-reference/dev-users/self>

Gets the authenticated user's information.

**Required scopes:** Default Scopes unavailable for this API

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
curl -X GET "https://api.devrev.ai/dev-users.self"
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="self-post"></a>

## `POST /dev-users.self`

**Self Dev User (POST)**

Source: <https://developer.devrev.ai/api-reference/dev-users/self-post>

Gets the authenticated user's information.

**Required scopes:** Default Scopes unavailable for this API

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
curl -X POST "https://api.devrev.ai/dev-users.self" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="self-update"></a>

## `POST /dev-users.self.update`

**Update Dev Users Self**

Source: <https://developer.devrev.ai/api-reference/dev-users/self-update>

Updates the authenticated user.

**Required scopes:** Default Scopes unavailable for this API

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `availability_modes` | no | `array<integer>` | Availability modes of the Dev user. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "Ticket",<br>    "ordinal": 1,<br>    "overridable": false<br>  },<br>  {<br>    "id": 2,<br>    "label": "Conversation",<br>    "ordinal": 2,<br>    "overridable": false<br>  },<br>  {<br>    "id": 3,<br>    "label": "Issue",<br>    "ordinal": 3,<br>    "overridable": false<br>  },<br>  {<br>    "id": 4,<br>    "label": "Incident",<br>    "ordinal": 4,<br>    "overridable": false<br>  },<br>  {<br>    "id": 5,<br>    "label": "Away",<br>    "ordinal": 5,<br>    "overridable": false<br>  },<br>  {<br>    "id": 6,<br>    "label": "Sick",<br>    "ordinal": 6,<br>    "overridable": false<br>  },<br>  {<br>    "id": 7,<br>    "label": "Lunch",<br>    "ordinal": 7,<br>    "overridable": false<br>  },<br>  {<br>    "id": 8,<br>    "label": "Travel",<br>    "ordinal": 8,<br>    "overridable": false<br>  },<br>  {<br>    "id": 9,<br>    "label": "Vacation",<br>    "ordinal": 9,<br>    "overridable": false<br>  }<br>``` |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `display_name` | no | `string` | The updated display name of the Dev user.<br>*Format: text* |
| `experience_start_date` | no | `string` | Start date of Dev user's experience.<br>*Format: date-time* |
| `full_name` | no | `string` | The updated full name of the Dev user.<br>*Format: text* |
| `job_function` | no | `string` | The job function of the Dev user.<br>*Format: text* |
| `job_history` | no | `array<dev-users-update-job-history-item>` | Job history of the Dev user. |
| `job_title` | no | `string` | Job title of the Dev User.<br>*Value in: "customer_success_manager" \| "cxo" \| "designer" \| "developer" \| "head_of_support" \| "operations" \| "others" \| "product_manager" \| "qa" \| "revenue_leader" \| "support" \| "tech_lead"* |
| `reports_to` | no | `string` | The ID of the Dev user that the user reports to.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/dev-users.self.update" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>


<a id="update"></a>

## `POST /dev-users.update`

**Update Dev User**

Source: <https://developer.devrev.ai/api-reference/dev-users/update>

Updates the user corresponding to the input Id.

**Required scopes:**

- `dev_user:write` OR `dev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `availability_modes` | no | `array<integer>` | Availability modes of the Dev user. Stock allowed values:<br>```<br>  {<br>    "id": 1,<br>    "label": "Ticket",<br>    "ordinal": 1,<br>    "overridable": false<br>  },<br>  {<br>    "id": 2,<br>    "label": "Conversation",<br>    "ordinal": 2,<br>    "overridable": false<br>  },<br>  {<br>    "id": 3,<br>    "label": "Issue",<br>    "ordinal": 3,<br>    "overridable": false<br>  },<br>  {<br>    "id": 4,<br>    "label": "Incident",<br>    "ordinal": 4,<br>    "overridable": false<br>  },<br>  {<br>    "id": 5,<br>    "label": "Away",<br>    "ordinal": 5,<br>    "overridable": false<br>  },<br>  {<br>    "id": 6,<br>    "label": "Sick",<br>    "ordinal": 6,<br>    "overridable": false<br>  },<br>  {<br>    "id": 7,<br>    "label": "Lunch",<br>    "ordinal": 7,<br>    "overridable": false<br>  },<br>  {<br>    "id": 8,<br>    "label": "Travel",<br>    "ordinal": 8,<br>    "overridable": false<br>  },<br>  {<br>    "id": 9,<br>    "label": "Vacation",<br>    "ordinal": 9,<br>    "overridable": false<br>  }<br>``` |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `display_name` | no | `string` | The updated display name of the Dev user.<br>*Format: text* |
| `experience_start_date` | no | `string` | Start date of Dev user's experience.<br>*Format: date-time* |
| `full_name` | no | `string` | The updated full name of the Dev user.<br>*Format: text* |
| `id` | yes | `string` | The ID for the Dev user to be updated.<br>*Format: id* |
| `job_function` | no | `string` | The job function of the Dev user.<br>*Format: text* |
| `job_history` | no | `array<dev-users-update-job-history-item>` | Job history of the Dev user. |
| `job_title` | no | `string` | Job title of the Dev User.<br>*Value in: "customer_success_manager" \| "cxo" \| "designer" \| "developer" \| "head_of_support" \| "operations" \| "others" \| "product_manager" \| "qa" \| "revenue_leader" \| "support" \| "tech_lead"* |
| `reports_to` | no | `string` | The ID of the Dev user that the user reports to.<br>*Format: id* |
| `staged_info` | no | `dev-users-update-request-staged-info-update` |  |

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
curl -X POST "https://api.devrev.ai/dev-users.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "dev_user": {
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
    "phone_numbers": [
      "string"
    ],
    "primary_identity": {
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
    "state": "active",
    "availability_modes": [
      {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "experience_start_date": "2023-01-01T12:00:00.000Z",
    "external_identities": [
      {
        "display_name": "string",
        "id": "string",
        "is_verified": true,
        "issuer": "string"
      }
    ],
    "is_invited": true,
    "job_history": [
      {
        "employment_status": {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        },
        "end_date": "2023-01-01T12:00:00.000Z",
        "is_current": true,
        "location": "string",
        "start_date": "2023-01-01T12:00:00.000Z",
        "title": "string"
      }
    ],
    "reports_to": {
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
    "skills": [
      {
        "name": "string"
      }
    ],
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "timezone": "string"
  }
}
```

</details>
