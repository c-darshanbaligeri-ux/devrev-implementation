# Surveys

Source: <https://developer.devrev.ai/beta/api-reference/surveys>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/surveys.create` | [create](#create) |
| POST | `/surveys.delete` | [delete](#delete) |
| GET | `/surveys.get` | [get](#get) |
| POST | `/surveys.get` | [get-post](#get-post) |
| GET | `/surveys.list` | [list](#list) |
| POST | `/surveys.list` | [list-post](#list-post) |
| GET | `/surveys.responses.list` | [responses-list](#responses-list) |
| POST | `/surveys.responses.list` | [responses-list-post](#responses-list-post) |
| POST | `/surveys.responses.update` | [responses-update](#responses-update) |
| POST | `/surveys.send` | [send](#send) |
| POST | `/surveys.submit` | [submit](#submit) |
| POST | `/surveys.update` | [update](#update) |

<a id="create"></a>

## `POST /surveys.create`

**Create Survey**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/create>

Creates a schema for survey, which includes name and description of schema.

**Required scopes:**

- `survey:write` OR `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | Description about the survey.<br>*Format: text*<br>*Length: length <= 1000* |
| `header` | no | `string` | Header of the survey.<br>*Format: text*<br>*Length: length <= 1000* |
| `introductory_text` | no | `string` | Text posted when introducing the survey to the responder.<br>*Format: text*<br>*Length: length <= 1000* |
| `name` | yes | `string` | The survey's name.<br>*Format: text*<br>*Length: 1 <= length <= 100* |
| `response_text` | no | `string` | Text posted after the response is collected.<br>*Format: text*<br>*Length: length <= 1000* |
| `schema` | no | `array<field-descriptor>` | Schema for the survey. |
| `schema_with_metadata` | no | `array<survey-field-with-metadata>` | The schema with metadata for the survey. |
| `title` | no | `string` | Title of the survey.<br>*Format: text*<br>*Length: length <= 1000* |

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
curl -X POST "https://api.devrev.ai/surveys.create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "survey": {
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
    "header": "string",
    "introductory_text": "string",
    "name": "string",
    "response_text": "string",
    "schema": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "schema_with_metadata": [
      {
        "field": {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        },
        "metadata": {},
        "question": "string"
      }
    ],
    "title": "string"
  }
}
```

</details>


<a id="delete"></a>

## `POST /surveys.delete`

**Delete Survey**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/delete>

Deletes the specified survey.

**Required scopes:**

- `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | ID of the survey being deleted.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/surveys.delete" \
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

## `GET /surveys.get`

**Get Survey**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/get>

Gets a survey given the ID.

**Required scopes:**

- `survey:read` OR `survey:write` OR `survey:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the survey to get.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/surveys.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "survey": {
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
    "header": "string",
    "introductory_text": "string",
    "name": "string",
    "response_text": "string",
    "schema": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "schema_with_metadata": [
      {
        "field": {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        },
        "metadata": {},
        "question": "string"
      }
    ],
    "title": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /surveys.get`

**Get Survey (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/get-post>

Gets a survey given the ID.

**Required scopes:**

- `survey:read` OR `survey:write` OR `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the survey to get.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/surveys.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "survey": {
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
    "header": "string",
    "introductory_text": "string",
    "name": "string",
    "response_text": "string",
    "schema": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "schema_with_metadata": [
      {
        "field": {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        },
        "metadata": {},
        "question": "string"
      }
    ],
    "title": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /surveys.list`

**List Surveys**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/list>

List surveys requested by the user.

**Required scopes:**

- `survey:read` OR `survey:write` OR `survey:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for surveys created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of surveys to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `name` | no | `array<string>` | Filters for surveys by name(s). |
| `sort_by` | no | `array<string>` | Fields to sort the surveys by and the direction to sort them. |

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
curl -X GET "https://api.devrev.ai/surveys.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "surveys": [
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
      "description": "string",
      "header": "string",
      "introductory_text": "string",
      "name": "string",
      "response_text": "string",
      "schema": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "schema_with_metadata": [
        {
          "field": {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          },
          "metadata": {},
          "question": "string"
        }
      ],
      "title": "string"
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /surveys.list`

**List Surveys (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/list-post>

List surveys requested by the user.

**Required scopes:**

- `survey:read` OR `survey:write` OR `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for surveys created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of surveys to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `name` | no | `array<string>` | Filters for surveys by name(s). |
| `sort_by` | no | `array<string>` | Fields to sort the surveys by and the direction to sort them. |

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
curl -X POST "https://api.devrev.ai/surveys.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "surveys": [
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
      "description": "string",
      "header": "string",
      "introductory_text": "string",
      "name": "string",
      "response_text": "string",
      "schema": [
        {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        }
      ],
      "schema_with_metadata": [
        {
          "field": {
            "field_type": "array",
            "description": "string",
            "is_derived": true,
            "is_filterable": true,
            "is_immutable": true,
            "is_pii": true,
            "is_required": true,
            "mfz": {},
            "name": "string",
            "oasis": {},
            "origin": "string",
            "ui": {
              "card_view": {
                "is_visible": true
              },
              "client_overrides": [
                {
                  "client_name": "string",
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_overrides": [
                    {
                      "decimal_places": 0,
                      "display_name": "string",
                      "is_groupable": true,
                      "is_hidden": true,
                      "is_required": true,
                      "order": 0,
                      "placeholder": "string",
                      "search_query": "string",
                      "tooltip": "string",
                      "use_shorthand_notation": true,
                      "view_name": "string"
                    }
                  ]
                }
              ],
              "create_view": {
                "is_hidden": true
              },
              "decimal_places": 0,
              "detail_view": {
                "is_hidden": true
              },
              "display_name": "string",
              "filter_view": {
                "is_hidden": true
              },
              "group_name": "string",
              "is_active_in_detail_view": true,
              "is_bulk_action_enabled": true,
              "is_currency_field": true,
              "is_groupable": true,
              "is_hidden": true,
              "is_hidden_during_create": true,
              "is_read_only": true,
              "is_required": true,
              "is_shown_in_summary": true,
              "is_sortable": true,
              "list_view": {
                "is_hidden": true
              },
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "summary_view": {
                "is_hidden": true
              },
              "tooltip": "string",
              "unit": "string",
              "use_shorthand_notation": true
            },
            "default_value": true
          },
          "metadata": {},
          "question": "string"
        }
      ],
      "title": "string"
    }
  ]
}
```

</details>


<a id="responses-list"></a>

## `GET /surveys.responses.list`

**List Surveys Responses**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/responses-list>

List survey responses requested by the user.

**Required scopes:**

- `survey_response:read` OR `survey_response:write` OR `survey_response:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for survey responses created by any of these users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `dispatch_ids` | no | `array<string>` | Filters for survey responses associated with these unique IDs. |
| `limit` | no | `integer` | The maximum number of survey responses to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `objects` | no | `array<string>` | Filters for survey responses created for the objects. |
| `recipient` | no | `array<string>` | Filters for survey responses dispatched to any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the survey responses by and the direction to sort them. |
| `stages` | no | `array<integer>` | Filters for survey response stages. |
| `surveys` | no | `array<string>` | Filters for survey responses for the provided survey IDs. |

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
curl -X GET "https://api.devrev.ai/surveys.responses.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "survey_responses": [
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
      "dispatch_id": "string",
      "dispatched_channels": [
        {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        }
      ],
      "object": "string",
      "recipient": {
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
      "response": {},
      "response_channel": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "stage": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "survey": "string"
    }
  ]
}
```

</details>


<a id="responses-list-post"></a>

## `POST /surveys.responses.list`

**List Surveys Responses (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/responses-list-post>

List survey responses requested by the user.

**Required scopes:**

- `survey_response:read` OR `survey_response:write` OR `survey_response:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `created_by` | no | `array<string>` | Filters for survey responses created by any of these users. |
| `created_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `dispatch_ids` | no | `array<string>` | Filters for survey responses associated with these unique IDs. |
| `limit` | no | `integer` | The maximum number of survey responses to return. If not set, then the default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_date` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `objects` | no | `array<string>` | Filters for survey responses created for the objects. |
| `recipient` | no | `array<string>` | Filters for survey responses dispatched to any of these users. |
| `sort_by` | no | `array<string>` | Fields to sort the survey responses by and the direction to sort them. |
| `stages` | no | `array<integer>` | Filters for survey response stages. |
| `surveys` | no | `array<string>` | Filters for survey responses for the provided survey IDs. |

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
curl -X POST "https://api.devrev.ai/surveys.responses.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "survey_responses": [
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
      "dispatch_id": "string",
      "dispatched_channels": [
        {
          "color": "string",
          "id": 0,
          "label": "string",
          "ordinal": 0,
          "value": null
        }
      ],
      "object": "string",
      "recipient": {
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
      "response": {},
      "response_channel": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "stage": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "survey": "string"
    }
  ]
}
```

</details>


<a id="responses-update"></a>

## `POST /surveys.responses.update`

**Update Surveys Response**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/responses-update>

Updates a user's survey response for the provided dispatch ID.

**Required scopes:**

- `survey_response:write` OR `survey_response:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dispatch_id` | yes | `string` | The unique ID associated with the dispatched survey.<br>*Format: id* |
| `response` | no | `object` | Survey response submitted for the object. |
| `response_channel` | no | `integer` | The source channel ordinal which recorded the survey response.<br>*Format: int64* |
| `response_score` | no | `integer` | The response score for the survey. Only applicable for CSAT and NPS.<br>*Format: int32*<br>*Range: 1 <= value <= 10* |
| `stage` | no | `integer` | The stage ordinal of the survey response object.<br>*Format: int64* |

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
curl -X POST "https://api.devrev.ai/surveys.responses.update" \
  -H "Content-Type: application/json" \
  -d '{
    "dispatch_id": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{}
```

</details>


<a id="send"></a>

## `POST /surveys.send`

**Send Surveys**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/send>

Sends a survey on the specified channels.

**Required scopes:**

- `survey:write` OR `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `email` | yes | `surveys-send-request-email` |  |

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
curl -X POST "https://api.devrev.ai/surveys.send" \
  -H "Content-Type: application/json" \
  -d '{
    "email": {
      "body": "string",
      "recipients": [
        "string"
      ],
      "sender": "string",
      "subject": "string"
    }
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="submit"></a>

## `POST /surveys.submit`

**Submit Surveys**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/submit>

Submits a user response to a survey, which is defined by the survey ID.

**Required scopes:**

- `survey_response:write` OR `survey_response:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dispatch_id` | no | `string` | The unique ID associated with the dispatched survey.<br>*Format: id* |
| `dispatched_channels` | no | `array<integer>` | The ordinals of the source channels on which the survey is sent. |
| `object` | yes | `string` | The ID of the object this survey is on (e.g. ticket, conversation, etc).<br>*Format: id* |
| `recipient` | no | `string` | The unique ID associated with the recipient of the survey.<br>*Format: id* |
| `response` | no | `object` | Survey response submitted for the object. |
| `response_score` | no | `integer` | The response score for the survey. Only applicable for CSAT and NPS.<br>*Format: int32* |
| `source_channel` | no | `string` | The source channel from which survey response is submitted.<br>*Format: text* |
| `stage` | no | `integer` | The stage ordinal of the survey response object.<br>*Format: int64* |
| `survey` | yes | `string` | The ID of the survey to submit the response to.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/surveys.submit" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "ACC-12345",
    "survey": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{}
```

</details>


<a id="update"></a>

## `POST /surveys.update`

**Update Survey**

Source: <https://developer.devrev.ai/beta/api-reference/surveys/update>

Updates a survey's metadata.

**Required scopes:**

- `survey:write` OR `survey:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `description` | no | `string` | The updated description about the survey.<br>*Format: text*<br>*Length: length <= 1000* |
| `header` | no | `string` | Header of the survey.<br>*Format: text*<br>*Length: length <= 1000* |
| `id` | yes | `string` | The ID of the survey to update.<br>*Format: id* |
| `introductory_text` | no | `string` | The updated text posted when introducing the survey to the responder.<br>*Format: text*<br>*Length: length <= 1000* |
| `name` | no | `string` | The survey's updated name.<br>*Format: text*<br>*Length: 1 <= length <= 100* |
| `response_text` | no | `string` | Text posted after the response is collected.<br>*Format: text*<br>*Length: length <= 1000* |
| `schema_with_metadata` | no | `array<survey-field-with-metadata>` | The updated schema with metadata for the survey. |
| `survey` | no | `string` | **Deprecated.**<br>The ID of the survey to update.<br>*Format: id* |
| `title` | no | `string` | Title of the survey.<br>*Format: text*<br>*Length: length <= 1000* |

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
curl -X POST "https://api.devrev.ai/surveys.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "survey": {
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
    "header": "string",
    "introductory_text": "string",
    "name": "string",
    "response_text": "string",
    "schema": [
      {
        "field_type": "array",
        "description": "string",
        "is_derived": true,
        "is_filterable": true,
        "is_immutable": true,
        "is_pii": true,
        "is_required": true,
        "mfz": {},
        "name": "string",
        "oasis": {},
        "origin": "string",
        "ui": {
          "card_view": {
            "is_visible": true
          },
          "client_overrides": [
            {
              "client_name": "string",
              "decimal_places": 0,
              "display_name": "string",
              "is_groupable": true,
              "is_hidden": true,
              "is_required": true,
              "order": 0,
              "placeholder": "string",
              "search_query": "string",
              "tooltip": "string",
              "use_shorthand_notation": true,
              "view_overrides": [
                {
                  "decimal_places": 0,
                  "display_name": "string",
                  "is_groupable": true,
                  "is_hidden": true,
                  "is_required": true,
                  "order": 0,
                  "placeholder": "string",
                  "search_query": "string",
                  "tooltip": "string",
                  "use_shorthand_notation": true,
                  "view_name": "string"
                }
              ]
            }
          ],
          "create_view": {
            "is_hidden": true
          },
          "decimal_places": 0,
          "detail_view": {
            "is_hidden": true
          },
          "display_name": "string",
          "filter_view": {
            "is_hidden": true
          },
          "group_name": "string",
          "is_active_in_detail_view": true,
          "is_bulk_action_enabled": true,
          "is_currency_field": true,
          "is_groupable": true,
          "is_hidden": true,
          "is_hidden_during_create": true,
          "is_read_only": true,
          "is_required": true,
          "is_shown_in_summary": true,
          "is_sortable": true,
          "list_view": {
            "is_hidden": true
          },
          "order": 0,
          "placeholder": "string",
          "search_query": "string",
          "summary_view": {
            "is_hidden": true
          },
          "tooltip": "string",
          "unit": "string",
          "use_shorthand_notation": true
        },
        "default_value": true
      }
    ],
    "schema_with_metadata": [
      {
        "field": {
          "field_type": "array",
          "description": "string",
          "is_derived": true,
          "is_filterable": true,
          "is_immutable": true,
          "is_pii": true,
          "is_required": true,
          "mfz": {},
          "name": "string",
          "oasis": {},
          "origin": "string",
          "ui": {
            "card_view": {
              "is_visible": true
            },
            "client_overrides": [
              {
                "client_name": "string",
                "decimal_places": 0,
                "display_name": "string",
                "is_groupable": true,
                "is_hidden": true,
                "is_required": true,
                "order": 0,
                "placeholder": "string",
                "search_query": "string",
                "tooltip": "string",
                "use_shorthand_notation": true,
                "view_overrides": [
                  {
                    "decimal_places": 0,
                    "display_name": "string",
                    "is_groupable": true,
                    "is_hidden": true,
                    "is_required": true,
                    "order": 0,
                    "placeholder": "string",
                    "search_query": "string",
                    "tooltip": "string",
                    "use_shorthand_notation": true,
                    "view_name": "string"
                  }
                ]
              }
            ],
            "create_view": {
              "is_hidden": true
            },
            "decimal_places": 0,
            "detail_view": {
              "is_hidden": true
            },
            "display_name": "string",
            "filter_view": {
              "is_hidden": true
            },
            "group_name": "string",
            "is_active_in_detail_view": true,
            "is_bulk_action_enabled": true,
            "is_currency_field": true,
            "is_groupable": true,
            "is_hidden": true,
            "is_hidden_during_create": true,
            "is_read_only": true,
            "is_required": true,
            "is_shown_in_summary": true,
            "is_sortable": true,
            "list_view": {
              "is_hidden": true
            },
            "order": 0,
            "placeholder": "string",
            "search_query": "string",
            "summary_view": {
              "is_hidden": true
            },
            "tooltip": "string",
            "unit": "string",
            "use_shorthand_notation": true
          },
          "default_value": true
        },
        "metadata": {},
        "question": "string"
      }
    ],
    "title": "string"
  }
}
```

</details>
