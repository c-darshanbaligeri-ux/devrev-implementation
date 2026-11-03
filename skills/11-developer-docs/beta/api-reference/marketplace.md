# Marketplace

Source: <https://developer.devrev.ai/beta/api-reference/marketplace>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/marketplace-item-features.list` | [item-features-list](#item-features-list) |
| POST | `/marketplace-item-features.list` | [item-features-list-post](#item-features-list-post) |
| POST | `/marketplace-items.install` | [items-install](#items-install) |

<a id="item-features-list"></a>

## `GET /marketplace-item-features.list`

**List Marketplace Item Features**

Source: <https://developer.devrev.ai/beta/api-reference/marketplace/item-features-list>

Lists marketplace item features.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | To start listing marketplace item features cursor field should not be provided. Set cursor to value returned by the previous call to list marketplace item features in the next page.<br>*Format: text* |
| `feature_type` | no | `array<marketplace-item-feature-feature-type>` | Filters on feature type for marketplace item features. |
| `import_capabilities` | no | `array<string>` | Filters on import capabilities for marketplace item import features. |
| `limit` | no | `integer` | Limit for how many marketplace item features to be retrieved per page. Default is 50.<br>*Format: int32* |
| `marketplace` | no | `string` | Marketplace ID where to list marketplace item features.<br>*Format: id* |
| `marketplace_item` | no | `array<string>` | Filters on marketplace item IDs for marketplace item features. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `operation_type` | no | `array<marketplace-item-operation-feature-operation-type>` | Filters on operation type for marketplace item operation features. |
| `server_type` | no | `array<marketplace-item-mcp-server-feature-server-type>` | Filters on server type for marketplace item MCP server features. |
| `sort_by` | no | `array<string>` | List of fields to sort the marketplace item feature objects, by and how to sort them. Default is to sort by created_date in descending order. |

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
curl -X GET "https://api.devrev.ai/marketplace-item-features.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "marketplace_item_features": [
    {
      "type": "marketplace_item_import_feature",
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
      "description": "string",
      "feature_type": "import",
      "marketplace_item": {
        "display_id": "string",
        "id": "string",
        "item_type": "app",
        "meta_score": 0,
        "name": "string",
        "slug": "string",
        "tagline": "string",
        "version": {}
      },
      "name": "string",
      "capabilities": [
        "string"
      ]
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="item-features-list-post"></a>

## `POST /marketplace-item-features.list`

**List Marketplace Item Features (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/marketplace/item-features-list-post>

Lists marketplace item features.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | To start listing marketplace item features cursor field should not be provided. Set cursor to value returned by the previous call to list marketplace item features in the next page.<br>*Format: text* |
| `feature_type` | no | `array<marketplace-item-feature-feature-type>` | Filters on feature type for marketplace item features. |
| `import_capabilities` | no | `array<string>` | Filters on import capabilities for marketplace item import features. |
| `limit` | no | `integer` | Limit for how many marketplace item features to be retrieved per page. Default is 50.<br>*Format: int32* |
| `marketplace` | no | `string` | Marketplace ID where to list marketplace item features.<br>*Format: id* |
| `marketplace_item` | no | `array<string>` | Filters on marketplace item IDs for marketplace item features. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `operation_type` | no | `array<marketplace-item-operation-feature-operation-type>` | Filters on operation type for marketplace item operation features. |
| `server_type` | no | `array<marketplace-item-mcp-server-feature-server-type>` | Filters on server type for marketplace item MCP server features. |
| `sort_by` | no | `array<string>` | List of fields to sort the marketplace item feature objects, by and how to sort them. Default is to sort by created_date in descending order. |

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
curl -X POST "https://api.devrev.ai/marketplace-item-features.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "marketplace_item_features": [
    {
      "type": "marketplace_item_import_feature",
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
      "description": "string",
      "feature_type": "import",
      "marketplace_item": {
        "display_id": "string",
        "id": "string",
        "item_type": "app",
        "meta_score": 0,
        "name": "string",
        "slug": "string",
        "tagline": "string",
        "version": {}
      },
      "name": "string",
      "capabilities": [
        "string"
      ]
    }
  ],
  "next_cursor": "string",
  "prev_cursor": "string"
}
```

</details>


<a id="items-install"></a>

## `POST /marketplace-items.install`

**Install Marketplace Items**

Source: <https://developer.devrev.ai/beta/api-reference/marketplace/items-install>

Installs a flow or vista for the marketplace item.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `activate` | no | `boolean` | Whether to activate the installed object. |
| `slug` | no | `string` | The slug of the marketplace item to install.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/marketplace-items.install" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "created_object": {
    "type": "account",
    "display_id": "string",
    "id": "string",
    "display_name": "string"
  }
}
```

</details>
