# Accounts

Source: <https://developer.devrev.ai/api-reference/accounts>
Scraped: 2026-11-03

`accounts` endpoint

ℹ️ An account represents a customer organization, and it holds information about the company, including its name, address, industry, domain, and website address.

📌 For more information about security tokens, refer to [Accounts](https://support.devrev.ai/devrev/article/ART-21830).

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/accounts.create` | [create](#create) |
| POST | `/accounts.delete` | [delete](#delete) |
| GET | `/accounts.export` | [export](#export) |
| POST | `/accounts.export` | [export-post](#export-post) |
| GET | `/accounts.get` | [get](#get) |
| POST | `/accounts.get` | [get-post](#get-post) |
| GET | `/accounts.list` | [list](#list) |
| POST | `/accounts.list` | [list-post](#list-post) |
| POST | `/accounts.merge` | [merge](#merge) |
| POST | `/accounts.update` | [update](#update) |

<a id="create"></a>

## `POST /accounts.create`

**Create Account**

Source: <https://developer.devrev.ai/api-reference/accounts/create>

Creates an account, which is a record representing a customer or an organization.

**Required scopes:**

- `account:write` OR `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `array<string>` | The IDs of the artifacts to associate with the account. |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description of the account.<br>*Format: text* |
| `display_name` | yes | `string` | Name of the account.<br>*Format: text* |
| `domains` | no | `array<string>` | List of company's domain names. Example - ['devrev.ai']. |
| `external_refs` | no | `array<string>` | External refs are unique identifiers from your customer system of records, stored as a list. |
| `owned_by` | no | `array<string>` | List of Dev users owning this account. |
| `schema_fragment_ids` | no | `array<string>` | **Deprecated.**<br>Schema fragment IDs associated with this account SOR. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the account. |
| `tier` | no | `string` | The tier of the account.<br>*Format: text* |
| `websites` | no | `array<string>` | List of company websites. Example - ['[www.devrev.ai](http://www.devrev.ai)', '[www.marketplace.devrev.ai](http://www.marketplace.devrev.ai)']. |

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
curl -X POST "https://api.devrev.ai/accounts.create" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "account": {
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
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
      {
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
      }
    ],
    "primary_account": {
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
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  },
  "default_rev_org": {
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
    "account": {
      "display_id": "string",
      "id": "string",
      "display_name": "string"
    },
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
    "domain": "string",
    "external_ref": "string",
    "primary_rev_org": {
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

## `POST /accounts.delete`

**Delete Account**

Source: <https://developer.devrev.ai/api-reference/accounts/delete>

Deletes an account.

**Required scopes:**

- `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of account to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/accounts.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ACC-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="export"></a>

## `GET /accounts.export`

**Export Accounts**

Source: <https://developer.devrev.ai/api-reference/accounts/export>

Exports a collection of accounts.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for accounts created by the specified user(s). |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of accounts to be filtered. |
| `domains` | no | `array<string>` | Domains for accounts to be filtered. |
| `external_refs` | no | `array<string>` | Array of references of accounts to be filtered. |
| `first` | no | `integer` | The number of accounts to return. The default is '50'.<br>*Format: int32*<br>*Range: 1 <= value <= 500* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `owned_by` | no | `array<string>` | Filters for accounts owned by the specified user(s). |
| `sort_by` | no | `array<string>` | Fields to sort the accounts by and the direction to sort them in. |
| `stage` | no | `array<string>` | Filters for accounts on specified stages. |
| `subtype` | no | `array<string>` | Subtypes of the accounts to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |
| `tier` | no | `array<string>` | Tier of the accounts to be filtered. |
| `websites` | no | `array<string>` | Array of websites of accounts to be filtered. |

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
curl -X GET "https://api.devrev.ai/accounts.export"
```

<details><summary>Example 200 response</summary>

```json
{
  "accounts": [
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
      "domains": [
        "string"
      ],
      "external_refs": [
        "string"
      ],
      "owned_by": [
        {
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
        }
      ],
      "primary_account": {
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
      ],
      "tier": "string",
      "websites": [
        "string"
      ]
    }
  ]
}
```

</details>


<a id="export-post"></a>

## `POST /accounts.export`

**Export Accounts (POST)**

Source: <https://developer.devrev.ai/api-reference/accounts/export-post>

Exports a collection of accounts.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for accounts created by the specified user(s). |
| `created_date` | no | `date-time-filter` |  |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of accounts to be filtered. |
| `domains` | no | `array<string>` | Domains for accounts to be filtered. |
| `external_refs` | no | `array<string>` | Array of references of accounts to be filtered. |
| `first` | no | `integer` | The number of accounts to return. The default is '50'.<br>*Format: int32*<br>*Range: 1 <= value <= 500* |
| `modified_date` | no | `date-time-filter` |  |
| `owned_by` | no | `array<string>` | Filters for accounts owned by the specified user(s). |
| `sort_by` | no | `array<string>` | Fields to sort the accounts by and the direction to sort them in. |
| `stage` | no | `array<string>` | Filters for accounts on specified stages. |
| `subtype` | no | `array<string>` | Subtypes of the accounts to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |
| `tier` | no | `array<string>` | Tier of the accounts to be filtered. |
| `websites` | no | `array<string>` | Array of websites of accounts to be filtered. |

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
curl -X POST "https://api.devrev.ai/accounts.export" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "accounts": [
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
      "domains": [
        "string"
      ],
      "external_refs": [
        "string"
      ],
      "owned_by": [
        {
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
        }
      ],
      "primary_account": {
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
      ],
      "tier": "string",
      "websites": [
        "string"
      ]
    }
  ]
}
```

</details>


<a id="get"></a>

## `GET /accounts.get`

**Get Account**

Source: <https://developer.devrev.ai/api-reference/accounts/get>

Retrieves an account's information.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the account to be retrieved.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/accounts.get?id=ACC-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "account": {
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
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
      {
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
      }
    ],
    "primary_account": {
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
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  }
}
```

</details>


<a id="get-post"></a>

## `POST /accounts.get`

**Get Account (POST)**

Source: <https://developer.devrev.ai/api-reference/accounts/get-post>

Retrieves an account's information.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the account to be retrieved.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/accounts.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ACC-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "account": {
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
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
      {
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
      }
    ],
    "primary_account": {
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
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  }
}
```

</details>


<a id="list"></a>

## `GET /accounts.list`

**List Accounts**

Source: <https://developer.devrev.ai/api-reference/accounts/list>

Gets a list of accounts.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for accounts created by the specified user(s). |
| `created_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `created_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of accounts to be filtered. |
| `domains` | no | `array<string>` | Domains for accounts to be filtered. |
| `external_refs` | no | `array<string>` | Array of references of accounts to be filtered. |
| `limit` | no | `integer` | The maximum number of accounts to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_date.after` | no | `string` | Filters for objects created after the provided timestamp (inclusive).<br>*Format: date-time* |
| `modified_date.before` | no | `string` | Filters for objects created before the provided timestamp (inclusive).<br>*Format: date-time* |
| `owned_by` | no | `array<string>` | Filters for accounts owned by the specified user(s). |
| `sort_by` | no | `array<string>` | Fields to sort the accounts by and the direction to sort them in. |
| `stage` | no | `array<string>` | Filters for accounts on specified stages. |
| `subtype` | no | `array<string>` | Subtypes of the accounts to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |
| `tier` | no | `array<string>` | Tier of the accounts to be filtered. |
| `websites` | no | `array<string>` | Array of websites of accounts to be filtered. |

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
curl -X GET "https://api.devrev.ai/accounts.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "accounts": [
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
      "domains": [
        "string"
      ],
      "external_refs": [
        "string"
      ],
      "owned_by": [
        {
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
        }
      ],
      "primary_account": {
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
      ],
      "tier": "string",
      "websites": [
        "string"
      ]
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="list-post"></a>

## `POST /accounts.list`

**List Accounts (POST)**

Source: <https://developer.devrev.ai/api-reference/accounts/list-post>

Gets a list of accounts.

**Required scopes:**

- `account:read` OR `account:write` OR `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for accounts created by the specified user(s). |
| `created_date` | no | `date-time-filter` |  |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `custom_fields` | no | `object` | Filters for custom fields. |
| `display_name` | no | `array<string>` | Array of display names of accounts to be filtered. |
| `domains` | no | `array<string>` | Domains for accounts to be filtered. |
| `external_refs` | no | `array<string>` | Array of references of accounts to be filtered. |
| `limit` | no | `integer` | The maximum number of accounts to return per page. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter` |  |
| `owned_by` | no | `array<string>` | Filters for accounts owned by the specified user(s). |
| `sort_by` | no | `array<string>` | Fields to sort the accounts by and the direction to sort them in. |
| `stage` | no | `array<string>` | Filters for accounts on specified stages. |
| `subtype` | no | `array<string>` | Subtypes of the accounts to be filtered. |
| `tags` | no | `array<string>` | List of tags to be filtered. |
| `tier` | no | `array<string>` | Tier of the accounts to be filtered. |
| `websites` | no | `array<string>` | Array of websites of accounts to be filtered. |

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
curl -X POST "https://api.devrev.ai/accounts.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "accounts": [
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
      "domains": [
        "string"
      ],
      "external_refs": [
        "string"
      ],
      "owned_by": [
        {
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
        }
      ],
      "primary_account": {
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
      ],
      "tier": "string",
      "websites": [
        "string"
      ]
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="merge"></a>

## `POST /accounts.merge`

**Merge Accounts**

Source: <https://developer.devrev.ai/api-reference/accounts/merge>

Merges two accounts.

**Required scopes:**

- `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `primary_account` | yes | `string` | The ID of the primary account, which will be retained post merge.<br>*Format: id* |
| `secondary_account` | yes | `string` | The ID of the secondary account, which will be merged into the primary account.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/accounts.merge" \
  -H "Content-Type: application/json" \
  -d '{
    "primary_account": "ACC-12345",
    "secondary_account": "ACC-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="update"></a>

## `POST /accounts.update`

**Update Account**

Source: <https://developer.devrev.ai/api-reference/accounts/update>

Updates an account's information.

**Required scopes:**

- `account:write` OR `account:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `artifacts` | no | `accounts-update-request-artifacts` |  |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Updated description of the account.<br>*Format: text* |
| `display_name` | no | `string` | Updated display name for the account.<br>*Format: text* |
| `domains` | no | `array<string>` | Updated list of company's domain names. Example - ['devrev.ai']. |
| `external_refs` | no | `array<string>` | Updated External Refs of account. |
| `id` | yes | `string` | The ID of account to update.<br>*Format: id* |
| `owned_by` | no | `array<string>` | Updated list of the users owning this account. |
| `schema_fragment_ids` | no | `array<string>` | **Deprecated.**<br>Schema fragment IDs associated with this account SOR. |
| `tags` | no | `array<set-tag-with-value>` | Updated tags list associated with the account. |
| `tier` | no | `string\|null` | Updated tier of the account.<br>*Format: text* |
| `websites` | no | `accounts-update-request-websites` |  |

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
curl -X POST "https://api.devrev.ai/accounts.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ACC-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "account": {
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
    "domains": [
      "string"
    ],
    "external_refs": [
      "string"
    ],
    "owned_by": [
      {
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
      }
    ],
    "primary_account": {
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
    ],
    "tier": "string",
    "websites": [
      "string"
    ]
  }
}
```

</details>
