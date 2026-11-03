# Rev Users

Source: <https://developer.devrev.ai/api-reference/rev-users>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/rev-users.create` | [create](#create) |
| POST | `/rev-users.delete` | [delete](#delete) |
| GET | `/rev-users.get` | [get](#get) |
| POST | `/rev-users.get` | [get-post](#get-post) |
| GET | `/rev-users.list` | [list](#list) |
| POST | `/rev-users.list` | [list-post](#list-post) |
| POST | `/rev-users.merge` | [merge](#merge) |
| GET | `/rev-users.scan` | [scan](#scan) |
| POST | `/rev-users.scan` | [scan-post](#scan-post) |
| POST | `/rev-users.update` | [update](#update) |

<a id="create"></a>

## `POST /rev-users.create`

**Create Rev User**

Source: <https://developer.devrev.ai/api-reference/rev-users/create>

Creates a Rev user for a Rev organization. Rev user can be a customer or a lead of an organization.

**Required scopes:**

- `rev_user:write` OR `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `account` | no | `string` | The ID of the account to which the created Rev user is associated.<br>*Format: id* |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the Rev user. |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_fragments` | no | `array<string>` | **Deprecated.**<br>The schema fragment IDs associated with the Rev user. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description of the Rev user.<br>*Format: text* |
| `display_name` | no | `string` | The user's display name. The name is non-unique and mutable.<br>*Format: text* |
| `display_picture` | no | `string` | Artifact ID of a Rev user's display picture.<br>*Format: id* |
| `email` | no | `string` | Email address of the Rev user.<br>*Format: text* |
| `external_ref` | no | `string` | External ref is a mutable unique identifier for a user within the Dev organization from your primary customer record. If none is available, a good alternative is the email address/phone number which could uniquely identify the user. If none is specified, a system-generated identifier will be assigned to the user.<br>*Format: text* |
| `external_refs` | no | `array<string>` | External refs are mutable unique identifiers for a contact record. If none are available, a good alternative is the email address(es)/phone number(s) which could uniquely identify the contact. If no identifier is specified, a system-generated identifier will be assigned to the contact. For organizations with multi-association contacts support enabled, this field accepts multiple identifiers, where each identifier must be unique across your DevOrg. For organizations without multi-association contacts support, this field accepts a single identifier, maintaining functionality consistent with the existing external_uid field. |
| `phone_numbers` | no | `array<string>` | Phone numbers, in E.164 format, of the Rev user. |
| `rev_org` | no | `string` | The ID of the Rev organization to which the created Rev user is associated.<br>*Format: id* |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the Rev user. |

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
curl -X POST "https://api.devrev.ai/rev-users.create" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 201 response</summary>

```json
{
  "rev_user": {
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
    "artifacts": [
      {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "is_verified": true,
    "rev_org": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
          },
          "sync_metadata": {
            "external_reference": "string",
            "last_sync_in": {
              "status": "failed",
              "sync_unit": {
                "display_id": "string",
                "id": "string",
                "external_sync_unit_name": "string",
                "external_system_id": "string",
                "external_system_name": "string",
                "external_system_type": "adaas",
                "is_archived": true,
                "name": "string",
                "sync_run": {
                  "mode": "initial",
                  "progress": {
                    "state": "completed"
                  },
                  "reserved_rate_limit_percentage": 0
                },
                "sync_type": "manual"
              }
            },
            "origin_system": "string"
          }
        },
        "value": "string"
      }
    ]
  }
}
```

</details>


<a id="delete"></a>

## `POST /rev-users.delete`

**Delete Rev User**

Source: <https://developer.devrev.ai/api-reference/rev-users/delete>

Deletes a Rev user.

**Required scopes:**

- `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of Rev user to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/rev-users.delete" \
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

## `GET /rev-users.get`

**Get Rev User**

Source: <https://developer.devrev.ai/api-reference/rev-users/get>

Returns the Rev user of a Rev organization by its ID.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of Rev user to be retrieved.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/rev-users.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_user": {
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
    "artifacts": [
      {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "is_verified": true,
    "rev_org": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
          },
          "sync_metadata": {
            "external_reference": "string",
            "last_sync_in": {
              "status": "failed",
              "sync_unit": {
                "display_id": "string",
                "id": "string",
                "external_sync_unit_name": "string",
                "external_system_id": "string",
                "external_system_name": "string",
                "external_system_type": "adaas",
                "is_archived": true,
                "name": "string",
                "sync_run": {
                  "mode": "initial",
                  "progress": {
                    "state": "completed"
                  },
                  "reserved_rate_limit_percentage": 0
                },
                "sync_type": "manual"
              }
            },
            "origin_system": "string"
          }
        },
        "value": "string"
      }
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /rev-users.get`

**Get Rev User (POST)**

Source: <https://developer.devrev.ai/api-reference/rev-users/get-post>

Returns the Rev user of a Rev organization by its ID.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of Rev user to be retrieved.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/rev-users.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_user": {
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
    "artifacts": [
      {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "is_verified": true,
    "rev_org": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
          },
          "sync_metadata": {
            "external_reference": "string",
            "last_sync_in": {
              "status": "failed",
              "sync_unit": {
                "display_id": "string",
                "id": "string",
                "external_sync_unit_name": "string",
                "external_system_id": "string",
                "external_system_name": "string",
                "external_system_type": "adaas",
                "is_archived": true,
                "name": "string",
                "sync_run": {
                  "mode": "initial",
                  "progress": {
                    "state": "completed"
                  },
                  "reserved_rate_limit_percentage": 0
                },
                "sync_type": "manual"
              }
            },
            "origin_system": "string"
          }
        },
        "value": "string"
      }
    ]
  }
}
```

</details>


<a id="list"></a>

## `GET /rev-users.list`

**List Rev Users**

Source: <https://developer.devrev.ai/api-reference/rev-users/list>

Returns a list of all Rev Users belonging to the authenticated user's Dev organization.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `associations` | no | `array<string>` | Filters for Rev users with specified associations (account/workspace). |
| `created_by` | no | `array<string>` | Filters for Rev users that were created by the specified user(s). |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | List of emails of Rev users to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev users for. |
| `external_refs` | no | `array<string>` | Filters for Rev users with the provided external_refs. |
| `is_verified` | no | `boolean` | Value of is_verified field to filter the Rev users. |
| `limit` | no | `integer` | The maximum number of Rev users to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Rev users on. |
| `rev_org` | no | `array<string>` | List of IDs of Rev organizations to be filtered. |
| `sort_by` | no | `array<string>` | Fields to sort the Rev users by and the direction to sort them. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X GET "https://api.devrev.ai/rev-users.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "rev_users": [
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
      "artifacts": [
        {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "is_verified": true,
      "rev_org": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "tags": [
        {
          "tag": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "style_new": {
              "color": "string"
            },
            "sync_metadata": {
              "external_reference": "string",
              "last_sync_in": {
                "status": "failed",
                "sync_unit": {
                  "display_id": "string",
                  "id": "string",
                  "external_sync_unit_name": "string",
                  "external_system_id": "string",
                  "external_system_name": "string",
                  "external_system_type": "adaas",
                  "is_archived": true,
                  "name": "string",
                  "sync_run": {
                    "mode": "initial",
                    "progress": {
                      "state": "completed"
                    },
                    "reserved_rate_limit_percentage": 0
                  },
                  "sync_type": "manual"
                }
              },
              "origin_system": "string"
            }
          },
          "value": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /rev-users.list`

**List Rev Users (POST)**

Source: <https://developer.devrev.ai/api-reference/rev-users/list-post>

Returns a list of all Rev Users belonging to the authenticated user's Dev organization.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `associations` | no | `array<string>` | Filters for Rev users with specified associations (account/workspace). |
| `created_by` | no | `array<string>` | Filters for Rev users that were created by the specified user(s). |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | List of emails of Rev users to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev users for. |
| `external_refs` | no | `array<string>` | Filters for Rev users with the provided external_refs. |
| `is_verified` | no | `boolean` | Value of is_verified field to filter the Rev users. |
| `limit` | no | `integer` | The maximum number of Rev users to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter` |  |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Rev users on. |
| `rev_org` | no | `array<string>` | List of IDs of Rev organizations to be filtered. |
| `sort_by` | no | `array<string>` | Fields to sort the Rev users by and the direction to sort them. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X POST "https://api.devrev.ai/rev-users.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "rev_users": [
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
      "artifacts": [
        {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "is_verified": true,
      "rev_org": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "tags": [
        {
          "tag": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "style_new": {
              "color": "string"
            },
            "sync_metadata": {
              "external_reference": "string",
              "last_sync_in": {
                "status": "failed",
                "sync_unit": {
                  "display_id": "string",
                  "id": "string",
                  "external_sync_unit_name": "string",
                  "external_system_id": "string",
                  "external_system_name": "string",
                  "external_system_type": "adaas",
                  "is_archived": true,
                  "name": "string",
                  "sync_run": {
                    "mode": "initial",
                    "progress": {
                      "state": "completed"
                    },
                    "reserved_rate_limit_percentage": 0
                  },
                  "sync_type": "manual"
                }
              },
              "origin_system": "string"
            }
          },
          "value": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="merge"></a>

## `POST /rev-users.merge`

**Merge Rev Users**

Source: <https://developer.devrev.ai/api-reference/rev-users/merge>

Merges the secondary Rev user into the primary Rev user.

**Required scopes:**

- `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `primary_user` | yes | `string` | The ID of the primary Rev user, which will be retained.<br>*Format: id* |
| `secondary_user` | yes | `string` | The ID of the secondary Rev user, which will be merged into the Primary Rev user.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/rev-users.merge" \
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


<a id="scan"></a>

## `GET /rev-users.scan`

**Scan Rev Users**

Source: <https://developer.devrev.ai/api-reference/rev-users/scan>

Scans through all Rev users.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `associations` | no | `array<string>` | Filters for Rev users with specified associations (account/workspace). |
| `created_by` | no | `array<string>` | Filters for Rev users that were created by the specified user(s). |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration, otherwise the beginning if not provided.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | List of emails of Rev users to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev users for. |
| `external_refs` | no | `array<string>` | Filters for Rev users with the provided external_refs. |
| `is_verified` | no | `boolean` | Value of is_verified field to filter the Rev users. |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Rev users on. |
| `rev_org` | no | `array<string>` | List of IDs of Rev organizations to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X GET "https://api.devrev.ai/rev-users.scan"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "rev_users": [
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
      "artifacts": [
        {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "is_verified": true,
      "rev_org": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "tags": [
        {
          "tag": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "style_new": {
              "color": "string"
            },
            "sync_metadata": {
              "external_reference": "string",
              "last_sync_in": {
                "status": "failed",
                "sync_unit": {
                  "display_id": "string",
                  "id": "string",
                  "external_sync_unit_name": "string",
                  "external_system_id": "string",
                  "external_system_name": "string",
                  "external_system_type": "adaas",
                  "is_archived": true,
                  "name": "string",
                  "sync_run": {
                    "mode": "initial",
                    "progress": {
                      "state": "completed"
                    },
                    "reserved_rate_limit_percentage": 0
                  },
                  "sync_type": "manual"
                }
              },
              "origin_system": "string"
            }
          },
          "value": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="scan-post"></a>

## `POST /rev-users.scan`

**Scan Rev Users (POST)**

Source: <https://developer.devrev.ai/api-reference/rev-users/scan-post>

Scans through all Rev users.

**Required scopes:**

- `rev_user:read` OR `rev_user:write` OR `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `associations` | no | `array<string>` | Filters for Rev users with specified associations (account/workspace). |
| `created_by` | no | `array<string>` | Filters for Rev users that were created by the specified user(s). |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration, otherwise the beginning if not provided.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `email` | no | `array<string>` | List of emails of Rev users to be filtered. |
| `external_ref` | no | `array<string>` | List of external refs to filter Rev users for. |
| `external_refs` | no | `array<string>` | Filters for Rev users with the provided external_refs. |
| `is_verified` | no | `boolean` | Value of is_verified field to filter the Rev users. |
| `modified_date` | no | `date-time-filter` |  |
| `phone_numbers` | no | `array<string>` | List of phone numbers, in E.164 format, to filter Rev users on. |
| `rev_org` | no | `array<string>` | List of IDs of Rev organizations to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |

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
curl -X POST "https://api.devrev.ai/rev-users.scan" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "rev_users": [
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
      "artifacts": [
        {
          "display_id": "string",
          "id": "string",
          "file": {
            "type": "string",
            "name": "string",
            "size": 0
          }
        }
      ],
      "custom_fields": {},
      "custom_schema_fragments": [
        "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
      ],
      "description": "string",
      "external_ref": "string",
      "external_refs": [
        "string"
      ],
      "is_verified": true,
      "rev_org": {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
      "subtype": "string",
      "tags": [
        {
          "tag": {
            "display_id": "string",
            "id": "string",
            "name": "string",
            "style_new": {
              "color": "string"
            },
            "sync_metadata": {
              "external_reference": "string",
              "last_sync_in": {
                "status": "failed",
                "sync_unit": {
                  "display_id": "string",
                  "id": "string",
                  "external_sync_unit_name": "string",
                  "external_system_id": "string",
                  "external_system_name": "string",
                  "external_system_type": "adaas",
                  "is_archived": true,
                  "name": "string",
                  "sync_run": {
                    "mode": "initial",
                    "progress": {
                      "state": "completed"
                    },
                    "reserved_rate_limit_percentage": 0
                  },
                  "sync_type": "manual"
                }
              },
              "origin_system": "string"
            }
          },
          "value": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /rev-users.update`

**Update Rev User**

Source: <https://developer.devrev.ai/api-reference/rev-users/update>

Updates a Rev user.

**Required scopes:**

- `rev_user:write` OR `rev_user:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `rev-users-update-request-artifacts` |  |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_fragments` | no | `rev-users-update-request-custom-schema-fragments` |  |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Updated description of the Rev user.<br>*Format: text* |
| `display_name` | no | `string` | Updated display name of the Rev user.<br>*Format: text* |
| `display_picture` | no | `string\|null` | Artifact ID of a Rev user's updated display picture.<br>*Format: id* |
| `email` | no | `string` | Updated email address of the Rev user.<br>*Format: text* |
| `external_ref` | no | `string` | Updated external ref value of the Rev user.<br>*Format: text* |
| `external_refs` | no | `array<string>` | External refs are mutable unique identifiers for a contact record. If none are available, a good alternative is the email address(es)/phone number(s) which could uniquely identify the contact. If no identifier is specified, a system-generated identifier will be assigned to the contact. For organizations with multi-association contacts support enabled, this field accepts multiple identifiers, where each identifier must be unique across your DevOrg. For organizations without multi-association contacts support, this field accepts a single identifier, maintaining functionality consistent with the existing external_uid field. |
| `id` | yes | `string` | The ID of Rev user to update.<br>*Format: id* |
| `phone_numbers` | no | `array<string>` | The phone numbers, in E.164 format, of the Rev user. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the Rev user. |

### Response codes

- `200` — `application/json`
- `400` — `application/json`
- `401` — `application/json`
- `403` — `application/json`
- `404` — `application/json`
- `409` — `application/json`
- `413` — `application/json`
- `429` — `application/json`
- `500` — `application/json`
- `503` — `application/json`

### cURL example

```bash
curl -X POST "https://api.devrev.ai/rev-users.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "rev_user": {
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
    "artifacts": [
      {
        "display_id": "string",
        "id": "string",
        "file": {
          "type": "string",
          "name": "string",
          "size": 0
        }
      }
    ],
    "custom_fields": {},
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id"
    ],
    "description": "string",
    "external_ref": "string",
    "external_refs": [
      "string"
    ],
    "is_verified": true,
    "rev_org": {
      "type": "account",
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
    "stock_schema_fragment": "don:core:dvrv-us-1:devo/example:custom_type_fragment/custom-type-fragment-id",
    "subtype": "string",
    "tags": [
      {
        "tag": {
          "display_id": "string",
          "id": "string",
          "name": "string",
          "style_new": {
            "color": "string"
          },
          "sync_metadata": {
            "external_reference": "string",
            "last_sync_in": {
              "status": "failed",
              "sync_unit": {
                "display_id": "string",
                "id": "string",
                "external_sync_unit_name": "string",
                "external_system_id": "string",
                "external_system_name": "string",
                "external_system_type": "adaas",
                "is_archived": true,
                "name": "string",
                "sync_run": {
                  "mode": "initial",
                  "progress": {
                    "state": "completed"
                  },
                  "reserved_rate_limit_percentage": 0
                },
                "sync_type": "manual"
              }
            },
            "origin_system": "string"
          }
        },
        "value": "string"
      }
    ]
  }
}
```

</details>
