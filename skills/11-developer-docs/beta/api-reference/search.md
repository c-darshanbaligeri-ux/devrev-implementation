# Search

Source: <https://developer.devrev.ai/beta/api-reference/search>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/objects.list` | [objects-list](#objects-list) |
| POST | `/objects.list` | [objects-list-post](#objects-list-post) |
| GET | `/search.core` | [core](#core) |
| POST | `/search.core` | [core-post](#core-post) |
| GET | `/search.hybrid` | [hybrid](#hybrid) |
| POST | `/search.hybrid` | [hybrid-post](#hybrid-post) |

<a id="objects-list"></a>

## `GET /objects.list`

**List Objects**

Source: <https://developer.devrev.ai/beta/api-reference/search/objects-list>

Get list of objects matching the given filter.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dql_query.cursor` | no | `string` | Opaque cursor token that represents a position in the result set. Use the cursor from previous responses to fetch next/previous iteration.<br>*Format: text* |
| `dql_query.expression.query` | no | `string` | The search query to filter the objects. Required if any dql_query.expression.* fields are provided.<br>*Format: text* |
| `dql_query.expression.scope` | no | `array<string>` | Fields on which the search query will be scoped on. |
| `dql_query.group_by.field` | no | `string` | Field name to group results by. Required if any dql_query.group_by.* fields are provided.<br>*Format: text* |
| `dql_query.group_by.order` | no | `string` | Criterion used to order groups<br>*Value in: "count" \| "lexical" \| "ordinal"* |
| `dql_query.group_by.sort_direction` | no | `string` | Sorting direction to be applied on the ordered groups<br>*Value in: "asc" \| "desc"* |
| `dql_query.limit` | no | `integer` | Maximum number of items to return per iteration. If not specified, the service will use its default limit.<br>*Format: int32* |
| `dql_query.mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `dql_query.search_query` | no | `string` | **Deprecated.**<br>The search query to filter the objects.<br>*Format: text* |
| `dql_query.sort_by` | no | `array<string>` | Fields to sort the records by and the direction to sort them. |

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
curl -X GET "https://api.devrev.ai/objects.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "type": "articles",
  "next_cursor": "string",
  "prev_cursor": "string",
  "articles": [
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
      "applies_to_parts": [
        {
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
        }
      ],
      "article_type": "article",
      "authored_by": [
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
      "description": "string",
      "extracted_content": [
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
      "num_downvotes": 0,
      "num_upvotes": 0,
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
      "parent": {
        "display_id": "string",
        "id": "string",
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
        },
        "title": "string"
      },
      "rank": "string",
      "resource": {
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
        "url": "string"
      },
      "scope": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "status": "archived",
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
      },
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
      "title": "string"
    }
  ]
}
```

</details>


<a id="objects-list-post"></a>

## `POST /objects.list`

**List Objects (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/search/objects-list-post>

Get list of objects matching the given filter.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `dql_query` | no | `devrev-query` | A unified query language for DevRev objects. |

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
curl -X POST "https://api.devrev.ai/objects.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "type": "articles",
  "next_cursor": "string",
  "prev_cursor": "string",
  "articles": [
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
      "applies_to_parts": [
        {
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
        }
      ],
      "article_type": "article",
      "authored_by": [
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
      "description": "string",
      "extracted_content": [
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
      "num_downvotes": 0,
      "num_upvotes": 0,
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
      "parent": {
        "display_id": "string",
        "id": "string",
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
        },
        "title": "string"
      },
      "rank": "string",
      "resource": {
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
        "url": "string"
      },
      "scope": {
        "color": "string",
        "id": 0,
        "label": "string",
        "ordinal": 0,
        "value": null
      },
      "status": "archived",
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
      },
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
      "title": "string"
    }
  ]
}
```

</details>


<a id="core"></a>

## `GET /search.core`

**Core Search**

Source: <https://developer.devrev.ai/beta/api-reference/search/core>

Searches for records based on a given query.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `query` | yes | `string` | The query string. Search query language: [https://docs.devrev.ai/product/search#fields](https://docs.devrev.ai/product/search#fields). Text and text phrases will be truncated if they exceed 50 characters respectively; filters will not be truncated.<br>*Format: text* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of items to return in a page. The default is '10'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `namespaces` | no | `array<search-namespace>` | The namespaces to search in. |
| `sort_by` | no | `string` | The property on which to sort the search results. The default is RELEVANCE.<br>*Value in: "created_date" \| "modified_date" \| "relevance"* |
| `sort_order` | no | `string` | Sorting order. The default is DESCENDING.<br>*Value in: "asc" \| "desc"* |

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
curl -X GET "https://api.devrev.ai/search.core?query=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "next_cursor": "string",
  "prev_cursor": "string",
  "results": [
    {
      "type": "account",
      "modified_date": "2023-01-01T12:00:00.000Z",
      "snippet": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "comments": [
        {
          "comment": {
            "display_id": "string",
            "id": "string",
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
          "object": "string",
          "panels": [
            "alerts"
          ],
          "references": [
            {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          ],
          "snippet": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="core-post"></a>

## `POST /search.core`

**Core Search (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/search/core-post>

Searches for records based on a given query.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of items to return in a page. The default is '10'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `namespaces` | no | `array<search-namespace>` | The namespaces to search in. |
| `query` | yes | `string` | The query string. Search query language: [https://docs.devrev.ai/product/search#fields](https://docs.devrev.ai/product/search#fields). Text and text phrases will be truncated if they exceed 50 characters respectively; filters will not be truncated.<br>*Format: text* |
| `sort_by` | no | `string` | Search sort by parameters.<br>*Value in: "created_date" \| "modified_date" \| "relevance"* |
| `sort_order` | no | `string` | Search sort order parameters.<br>*Value in: "asc" \| "desc"* |

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
curl -X POST "https://api.devrev.ai/search.core" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "cursor": "string",
  "next_cursor": "string",
  "prev_cursor": "string",
  "results": [
    {
      "type": "account",
      "modified_date": "2023-01-01T12:00:00.000Z",
      "snippet": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "comments": [
        {
          "comment": {
            "display_id": "string",
            "id": "string",
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
          "object": "string",
          "panels": [
            "alerts"
          ],
          "references": [
            {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          ],
          "snippet": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="hybrid"></a>

## `GET /search.hybrid`

**Hybrid Search**

Source: <https://developer.devrev.ai/beta/api-reference/search/hybrid>

Performs search, using a combination of syntactic and semantic search.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `namespace` | yes | `string` | The hybrid namespace to search in.<br>*Value in: "account" \| "ai_agent" \| "article" \| "capability" \| "component" \| "conversation" \| "custom_object" \| "custom_part" \| "dashboard" \| "dataset" \| "dev_user" \| "directory" \| "enhancement" \| "feature" \| "group" \| "incident" \| "issue" \| "linkable" \| "meeting" \| "microservice" \| "object_member" \| "opportunity" \| "part" \| "product" \| "question_answer" \| "rev_org" \| "rev_user" \| "runnable" \| "service_account" \| "sys_user" \| "tag" \| "task" \| "ticket" \| "vista" \| "widget" \| "work"* |
| `limit` | no | `integer` | The maximum number of items to return in a page. The default is '10'.<br>*Format: int32*<br>*Range: 0 <= value <= 50* |
| `query` | no | `string` | The query string. Text and text phrases will be truncated if they exceed 50 characters respectively; filters will not be truncated.<br>*Format: text*<br>*Length: 1 <= length <= 400* |

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
curl -X GET "https://api.devrev.ai/search.hybrid?namespace=account"
```

<details><summary>Example 200 response</summary>

```json
{
  "results": [
    {
      "type": "account",
      "modified_date": "2023-01-01T12:00:00.000Z",
      "snippet": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "comments": [
        {
          "comment": {
            "display_id": "string",
            "id": "string",
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
          "object": "string",
          "panels": [
            "alerts"
          ],
          "references": [
            {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          ],
          "snippet": "string"
        }
      ]
    }
  ]
}
```

</details>


<a id="hybrid-post"></a>

## `POST /search.hybrid`

**Hybrid Search (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/search/hybrid-post>

Performs search, using a combination of syntactic and semantic search.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `limit` | no | `integer` | The maximum number of items to return in a page. The default is '10'.<br>*Format: int32*<br>*Range: 0 <= value <= 50* |
| `namespace` | yes | `string` | The namespaces for hybrid search.<br>*Value in: "account" \| "ai_agent" \| "article" \| "capability" \| "component" \| "conversation" \| "custom_object" \| "custom_part" \| "dashboard" \| "dataset" \| "dev_user" \| "directory" \| "enhancement" \| "feature" \| "group" \| "incident" \| "issue" \| "linkable" \| "meeting" \| "microservice" \| "object_member" \| "opportunity" \| "part" \| "product" \| "question_answer" \| "rev_org" \| "rev_user" \| "runnable" \| "service_account" \| "sys_user" \| "tag" \| "task" \| "ticket" \| "vista" \| "widget" \| "work"* |
| `query` | no | `string` | The query string. Text and text phrases will be truncated if they exceed 50 characters respectively; filters will not be truncated.<br>*Format: text*<br>*Length: 1 <= length <= 400* |

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
curl -X POST "https://api.devrev.ai/search.hybrid" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "account"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "results": [
    {
      "type": "account",
      "modified_date": "2023-01-01T12:00:00.000Z",
      "snippet": "string",
      "account": {
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      },
      "comments": [
        {
          "comment": {
            "display_id": "string",
            "id": "string",
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
          "object": "string",
          "panels": [
            "alerts"
          ],
          "references": [
            {
              "type": "account",
              "display_id": "string",
              "id": "string",
              "display_name": "string"
            }
          ],
          "snippet": "string"
        }
      ]
    }
  ]
}
```

</details>
