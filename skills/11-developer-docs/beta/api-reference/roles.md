# Roles

Source: <https://developer.devrev.ai/beta/api-reference/roles>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/roles.apply` | [apply](#apply) |
| POST | `/roles.create` | [create](#create) |

<a id="apply"></a>

## `POST /roles.apply`

**Apply Roles**

Source: <https://developer.devrev.ai/beta/api-reference/roles/apply>

Deprecated: Use role-sets.apply instead. Assigns or revokes roles of a principal.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `assign` | no | `array<string>` | Roles to be additionally assigned to principal. |
| `principal` | yes | `string` | The ID of the principal.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/roles.apply" \
  -H "Content-Type: application/json" \
  -d '{
    "principal": "DEV-AbCdEfGh"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="create"></a>

## `POST /roles.create`

**Create Role**

Source: <https://developer.devrev.ai/beta/api-reference/roles/create>

Creates a new role.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `allow_private_access` | no | `boolean` | Whether to allow private access to the role. |
| `caveats` | no | `array<roles-create-request-caveat>` | The caveats on the role. |
| `description` | no | `string` | The description of the role.<br>*Format: text* |
| `include_all_subtypes` | no | `boolean` | Whether to include all subtypes of the leaf type as target of the role. |
| `name` | no | `string` | The name of the role.<br>*Format: text* |
| `privileges` | no | `array<role-privileges>` | The privileges the role provides on target.<br>*Items: 1 <= items* |
| `target` | yes | `string` | Target object type of the role.<br>*Value in: "article" \| "artifact" \| "capability" \| "conversation" \| "dev_user" \| "feature" \| "group" \| "issue" \| "linkable" \| "meeting" \| "opportunity" \| "product" \| "rev_user" \| "runnable" \| "ticket"* |
| `target_subtype` | no | `string` | The subtype of the target.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/roles.create" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "article"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "role": {
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
    "sync_metadata": {
      "external_record_id": "string",
      "external_record_type": "string",
      "external_reference": "string",
      "last_sync_in": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
      "last_sync_out": {
        "status": "failed",
        "sync_date": "2023-01-01T12:00:00.000Z",
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
  }
}
```

</details>
