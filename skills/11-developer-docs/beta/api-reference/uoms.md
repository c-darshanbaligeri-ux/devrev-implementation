# Uoms

Source: <https://developer.devrev.ai/beta/api-reference/uoms>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/uoms.count` | [count](#count) |
| POST | `/uoms.count` | [count-post](#count-post) |
| POST | `/uoms.create` | [create](#create) |
| POST | `/uoms.delete` | [delete](#delete) |
| GET | `/uoms.get` | [get](#get) |
| POST | `/uoms.get` | [get-post](#get-post) |
| GET | `/uoms.list` | [list](#list) |
| POST | `/uoms.list` | [list-post](#list-post) |
| POST | `/uoms.update` | [update](#update) |

<a id="count"></a>

## `GET /uoms.count`

**Count UOMs**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/count>

Counts the number of Unit of Measurements based on the given filters.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_types` | no | `array<aggregation-detail-aggregation-type>` | List of aggregation types for filtering list of UOMs. |
| `ids` | no | `array<string>` | List of Unit of Measurement (UOM) DONs to be used in filtering complete list of UOMs defined in a Dev Org. |
| `metric_names` | no | `array<string>` | List of metric names for filtering list of UOMs. |
| `part_ids` | no | `array<string>` | List of part IDs for filtering list of UOMs. |
| `product_ids` | no | `array<string>` | List of product IDs for filtering list of UOMs. |
| `unit_types` | no | `array<unit-type>` | List of unit types for filtering list of UOMs. |

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
curl -X GET "https://api.devrev.ai/uoms.count"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="count-post"></a>

## `POST /uoms.count`

**Count UOMs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/count-post>

Counts the number of Unit of Measurements based on the given filters.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_types` | no | `array<aggregation-detail-aggregation-type>` | List of aggregation types for filtering list of UOMs. |
| `ids` | no | `array<string>` | List of Unit of Measurement (UOM) DONs to be used in filtering complete list of UOMs defined in a Dev Org. |
| `metric_names` | no | `array<string>` | List of metric names for filtering list of UOMs. |
| `part_ids` | no | `array<string>` | List of part IDs for filtering list of UOMs. |
| `product_ids` | no | `array<string>` | List of product IDs for filtering list of UOMs. |
| `unit_types` | no | `array<unit-type>` | List of unit types for filtering list of UOMs. |

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
curl -X POST "https://api.devrev.ai/uoms.count" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="create"></a>

## `POST /uoms.create`

**Create UOM**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/create>

Creates a Unit of Measurement on a part.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_detail` | yes | `aggregation-detail` | Stores aggregation type and dimension information. |
| `description` | no | `string` | Description of the Unit of Measurement (UOM).<br>*Format: text* |
| `dimensions` | no | `array<string>` | The list of dimensions that can be emitted as part of metrics data. Dimensions consist of list of key-value pairs. For example, if the UOM is 'number_of_api_calls', then dimensions can be ['api_name', 'api_version'].Dimension keys can only contain alphanumeric characters (A-Z, a-z, and 0-9) and underscores (_). Dimension keys cannot start with a number and is case-insensitive.Dimension keys must be unique and it is not allowed to have more than one value with the same key.Metrics data ingested in DevRev metrics format will be grouped and aggregated based on the dimensions specified in UOM.<br>*Length: 1 <= length <= 64*<br>*Items: items <= 12* |
| `metric_name` | yes | `string` | Name of the Unit of Measurement (UOM). Unit of Measurement is a unit of measure defined over a part offered by a Dev Org. A single part can have multiple unit of measurements defined over it. For example, a part can be 'video call', one UOM defined on this can be 'number_of_calls', other UOM can be 'call_duration' etc.Metric name should be unique across all UOMs in a Dev Org.Metric name can only contain alphanumeric characters (A-Z, a-z, and 0-9) and underscores (_). Metric name cannot start with a number and is case-insensitive.<br>*Format: text*<br>*Length: 1 <= length <= 64* |
| `name` | yes | `string` | Human readable name of the Unit of Measurement (UOM).<br>*Format: text* |
| `part_id` | no | `string` | The part ID for which the Unit of Measurement (UOM) is defined. When defined, ingested metrics data will be associated with part and product specified in UOM.<br>*Format: id* |
| `product_id` | yes | `string` | The product ID for which the Unit of Measurement (UOM) is defined.<br>*Format: id* |
| `unit` | yes | `unit` | Unit encapsulates the name of the unit and the type of the unit. For example, '#Number of API calls' where name is 'number_of_api_calls' and type is 'number'. |

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
curl -X POST "https://api.devrev.ai/uoms.create" \
  -H "Content-Type: application/json" \
  -d '{
    "aggregation_detail": {
      "aggregation_type": "duration"
    },
    "metric_name": "string",
    "name": "string",
    "product_id": "PROD-12345",
    "unit": {
      "type": "boolean",
      "name": "string"
    }
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "uom": {
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
    "aggregation_details": {
      "aggregation_type": "duration",
      "unique_dimension": "string"
    },
    "description": "string",
    "dimensions": [
      "string"
    ],
    "is_enabled": true,
    "metric_name": "string",
    "metric_scope": "org",
    "name": "string",
    "part": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "product": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "unit": {
      "type": "boolean",
      "name": "string"
    }
  }
}
```

</details>


<a id="delete"></a>

## `POST /uoms.delete`

**Delete UOM**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/delete>

Deletes a Unit of Measurement.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The Unit of Measurement (UOM)'s DON.<br>*Format: id* |

### Response codes

- `204` — empty body
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
curl -X POST "https://api.devrev.ai/uoms.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```


<a id="get"></a>

## `GET /uoms.get`

**Get UOM**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/get>

Gets a Unit of Measurement.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The Unit of Measurement (UOM)'s DON.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/uoms.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "uom": {
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
    "aggregation_details": {
      "aggregation_type": "duration",
      "unique_dimension": "string"
    },
    "description": "string",
    "dimensions": [
      "string"
    ],
    "is_enabled": true,
    "metric_name": "string",
    "metric_scope": "org",
    "name": "string",
    "part": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "product": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "unit": {
      "type": "boolean",
      "name": "string"
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /uoms.get`

**Get UOM (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/get-post>

Gets a Unit of Measurement.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The Unit of Measurement (UOM)'s DON.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/uoms.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "uom": {
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
    "aggregation_details": {
      "aggregation_type": "duration",
      "unique_dimension": "string"
    },
    "description": "string",
    "dimensions": [
      "string"
    ],
    "is_enabled": true,
    "metric_name": "string",
    "metric_scope": "org",
    "name": "string",
    "part": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "product": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "unit": {
      "type": "boolean",
      "name": "string"
    }
  }
}
```

</details>


<a id="list"></a>

## `GET /uoms.list`

**List UOMs**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/list>

Gets the Unit of Measurements based on the given filters.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_types` | no | `array<aggregation-detail-aggregation-type>` | List of aggregation types for filtering list of UOMs. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `ids` | no | `array<string>` | List of Unit of Measurement (UOM) DONs to be used in filtering complete list of UOMs defined in a Dev Org. |
| `limit` | no | `integer` | The maximum number of UOMs to be returned in a response. The default is '50'.<br>*Format: int32* |
| `metric_names` | no | `array<string>` | List of metric names for filtering list of UOMs. |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `part_ids` | no | `array<string>` | List of part IDs for filtering list of UOMs. |
| `product_ids` | no | `array<string>` | List of product IDs for filtering list of UOMs. |
| `sort_by` | no | `array<string>` | Fields to sort the Unit Of Measuments (UOMs) by and the direction to sort them. |
| `unit_types` | no | `array<unit-type>` | List of unit types for filtering list of UOMs. |

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
curl -X GET "https://api.devrev.ai/uoms.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "uoms": [
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
      "aggregation_details": {
        "aggregation_type": "duration",
        "unique_dimension": "string"
      },
      "description": "string",
      "dimensions": [
        "string"
      ],
      "is_enabled": true,
      "metric_name": "string",
      "metric_scope": "org",
      "name": "string",
      "part": {
        "type": "capability",
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "product": {
        "type": "capability",
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "unit": {
        "type": "boolean",
        "name": "string"
      }
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /uoms.list`

**List UOMs (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/list-post>

Gets the Unit of Measurements based on the given filters.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_types` | no | `array<aggregation-detail-aggregation-type>` | List of aggregation types for filtering list of UOMs. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `ids` | no | `array<string>` | List of Unit of Measurement (UOM) DONs to be used in filtering complete list of UOMs defined in a Dev Org. |
| `limit` | no | `integer` | The maximum number of UOMs to be returned in a response. The default is '50'.<br>*Format: int32* |
| `metric_names` | no | `array<string>` | List of metric names for filtering list of UOMs. |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `part_ids` | no | `array<string>` | List of part IDs for filtering list of UOMs. |
| `product_ids` | no | `array<string>` | List of product IDs for filtering list of UOMs. |
| `sort_by` | no | `array<string>` | Fields to sort the Unit Of Measuments (UOMs) by and the direction to sort them. |
| `unit_types` | no | `array<unit-type>` | List of unit types for filtering list of UOMs. |

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
curl -X POST "https://api.devrev.ai/uoms.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "uoms": [
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
      "aggregation_details": {
        "aggregation_type": "duration",
        "unique_dimension": "string"
      },
      "description": "string",
      "dimensions": [
        "string"
      ],
      "is_enabled": true,
      "metric_name": "string",
      "metric_scope": "org",
      "name": "string",
      "part": {
        "type": "capability",
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "product": {
        "type": "capability",
        "display_id": "string",
        "id": "string",
        "name": "string",
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
      "unit": {
        "type": "boolean",
        "name": "string"
      }
    }
  ]
}
```

</details>


<a id="update"></a>

## `POST /uoms.update`

**Update UOM**

Source: <https://developer.devrev.ai/beta/api-reference/uoms/update>

Updates a Unit of Measurement.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `aggregation_type` | no | `string` | Aggregation type to be used while aggregating the metering data for the UOM. 1] Sum - sum of all the values for the meter in a given period Ex. { M1:2, M1:4 } => {M1:6} 2] Minimum - min of all the values for the meter in a given period Ex. { M1:2, M1:4 } => {M1:2} 3] Maximum - max of all the values for the meter in a given period Ex. { M1:2, M1:4 } => {M1:4} 4] Unique Count - Sum of distinct unique dimension observed for the meter in the given period (not considering the data from the previous billing period) Ex. January {M1:{VM:VM0}}, February {M1:{VM:VM1}, M1:{VM:VM2}, M1:{VM:VM1}} => {M1:2} 5] Running Total - Sum of distinct active unique dimension observed for a meter in the given period, taking into consideration the active data from the previous billing cycle Ex. January {M1:{VM:VM0,on}, {M1:{VM:VM1,off} February {M1:{VM:VM2, on}, M1:{VM:VM2, off}, M1:{VM:VM3, on}} => {M1:3} 6] Duration - Sum of distinct active unique dimension duration for a meter in the given period, taking into consideration the active data from the previous month Ex. January15 {M1:{VM:VM0,on, 4}} February15 {M1:{VM:VM0,off}, February18 {M1:{VM:VM1,on,5} => M1-> 30*4*charge_per_day + 10*5*charge_per_day 7] Latest - consider the latest/last meter in the given period 8] Oldest - consider the oldest/first record in the given period.<br>*Value in: "duration" \| "latest" \| "maximum" \| "minimum" \| "oldest" \| "running_total" \| "sum" \| "unique_count"* |
| `description` | no | `string` | Description of the Unit of Measurement (UOM).<br>*Format: text* |
| `dimensions` | no | `uoms-update-request-dimensions` |  |
| `id` | yes | `string` | The Unit of Measurement (UOM)'s DON.<br>*Format: id* |
| `is_enabled` | no | `boolean` | Flag used to enable/disable the Unit of Measurement (UOM). When disabled, any metricsrecords ingested against this UOM will be dropped. |
| `name` | no | `string` | Human readable name of the Unit of Measurement (UOM).<br>*Format: text* |
| `part_id` | no | `string` | The part ID such as feature or capability for which the Unit of Measurement (UOM) is defined.<br>*Format: id* |
| `product_id` | no | `string` | The product ID for which the Unit of Measurement (UOM) is defined.<br>*Format: id* |
| `unit` | no | `string` | Unit name of the Unit of Measurement (UOM).<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/uoms.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "uom": {
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
    "aggregation_details": {
      "aggregation_type": "duration",
      "unique_dimension": "string"
    },
    "description": "string",
    "dimensions": [
      "string"
    ],
    "is_enabled": true,
    "metric_name": "string",
    "metric_scope": "org",
    "name": "string",
    "part": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "product": {
      "type": "capability",
      "display_id": "string",
      "id": "string",
      "name": "string",
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
    "unit": {
      "type": "boolean",
      "name": "string"
    }
  }
}
```

</details>
