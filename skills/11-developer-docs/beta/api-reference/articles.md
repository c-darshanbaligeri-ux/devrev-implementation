# Articles

Source: <https://developer.devrev.ai/beta/api-reference/articles>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/articles.count` | [count](#count) |
| POST | `/articles.count` | [count-post](#count-post) |
| POST | `/articles.create` | [create-article](#create-article) |
| POST | `/articles.delete` | [delete-article](#delete-article) |
| GET | `/articles.get` | [get-article](#get-article) |
| POST | `/articles.get` | [get-article-post](#get-article-post) |
| GET | `/articles.list` | [list-articles](#list-articles) |
| POST | `/articles.list` | [list-articles-post](#list-articles-post) |
| POST | `/articles.update` | [update-article](#update-article) |

<a id="count"></a>

## `GET /articles.count`

**Count Articles**

Source: <https://developer.devrev.ai/beta/api-reference/articles/count>

Get count of articles matching given filter.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `ancestor` | no | `string` | The ancestor directory of the articles.<br>*Format: id* |
| `applies_to_parts` | no | `array<string>` | Filters for articles belonging to any of the provided parts. |
| `article_type` | no | `array<article-type>` | Filter for the type of articles. If this is not provided, then articles that are not content blocks are returned. |
| `authored_by` | no | `array<string>` | Filters for articles authored by any of the provided users. |
| `brands` | no | `array<string>` | Filters for articles belonging to any of the provided brands. |
| `created_by` | no | `array<string>` | Filters for articles created by any of the provided users. |
| `modified_by` | no | `array<string>` | Filters for articles modified by any of the provided users. |
| `owned_by` | no | `array<string>` | Filters for articles owned by any of the provided users. |
| `parent` | no | `array<string>` | Filters for articles with the provided parent directories. |
| `scope` | no | `array<integer>` | Filter for the scope of the articles. |
| `shared_with.member` | no | `string` | ID of the group/member with whom the item is shared.<br>*Format: id* |
| `shared_with.role` | no | `string` | Role ID of the group/member with whom the item is shared.<br>*Format: id* |
| `status` | no | `array<article-status>` | Filters for status of the articles. |
| `sync_metadata.external_record` | no | `array<string>` | Filters for issues with this specific external record. |
| `sync_metadata.external_record_type` | no | `array<string>` | Filters for issues with this specific external record type. |
| `sync_metadata.external_reference` | no | `array<string>` | Filters for issues with this specific external reference. |
| `sync_metadata.last_sync_in.status` | no | `array<sync-metadata-filter-sync-in-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_in.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_in.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.last_sync_out.status` | no | `array<sync-metadata-filter-sync-out-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_out.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_out.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.origin_system` | no | `array<string>` | Filters for issues synced from this specific origin system. |
| `tags` | no | `array<string>` | Filters for article with any of the provided tags. |

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
curl -X GET "https://api.devrev.ai/articles.count"
```

<details><summary>Example 200 response</summary>

```json
{
  "count": 0
}
```

</details>


<a id="count-post"></a>

## `POST /articles.count`

**Count Articles (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/articles/count-post>

Get count of articles matching given filter.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `ancestor` | no | `string` | The ancestor directory of the articles.<br>*Format: id* |
| `applies_to_parts` | no | `array<string>` | Filters for articles belonging to any of the provided parts. |
| `article_type` | no | `array<article-type>` | Filter for the type of articles. If this is not provided, then articles that are not content blocks are returned. |
| `authored_by` | no | `array<string>` | Filters for articles authored by any of the provided users. |
| `brands` | no | `array<string>` | Filters for articles belonging to any of the provided brands. |
| `created_by` | no | `array<string>` | Filters for articles created by any of the provided users. |
| `modified_by` | no | `array<string>` | Filters for articles modified by any of the provided users. |
| `owned_by` | no | `array<string>` | Filters for articles owned by any of the provided users. |
| `parent` | no | `array<string>` | Filters for articles with the provided parent directories. |
| `scope` | no | `array<integer>` | Filter for the scope of the articles. |
| `shared_with` | no | `array<shared-with-membership-filter>` | Filter for articles based on intended audience. |
| `status` | no | `array<article-status>` | Filters for status of the articles. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for article with any of the provided tags. |

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
curl -X POST "https://api.devrev.ai/articles.count" \
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


<a id="create-article"></a>

## `POST /articles.create`

**Create Article**

Source: <https://developer.devrev.ai/beta/api-reference/articles/create-article>

Article is an object which can contain a URL or artifacts in the resource. It also contains the data regarding the owner, author, status and published date of the object. This call creates an article.

**Required scopes:**

- `article:write` OR `article:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `access_level` | no | `string` | *Value in: "external" \| "internal" \| "private" \| "public" \| "restricted"* |
| `aliases` | no | `array<string>` | The aliases of the article.<br>*Items: items <= 5* |
| `applies_to_parts` | no | `array<string>` | The parts that the article applies to. |
| `article_type` | no | `string` | Type of the article.<br>*Value in: "article" \| "content_block" \| "page"* |
| `authored_by` | no | `array<string>` | The authors of the article. |
| `brand` | no | `string` | The brand associated with the article.<br>*Format: id* |
| `content_format` | no | `string` | Content format of the article.<br>*Value in: "drdfv2" \| "rt"* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `data_sources` | no | `array<article-data-source-create>` | Data sources provide the backing data for the article. |
| `description` | no | `string` | Description for the article.<br>*Format: text* |
| `extracted_content` | no | `array<string>` | ID of the extracted content artifact. |
| `language` | no | `string` | Language of the article.<br>*Format: text* |
| `notify` | no | `boolean` | Whether to notify the users when the article is published. |
| `owned_by` | yes | `array<string>` | The users that own the article. |
| `parent` | no | `string` | The parent directory of the article.<br>*Format: id* |
| `published_at` | no | `string` | The published date of the article.<br>*Format: date-time* |
| `release_notes` | no | `string` | The release notes of the article.<br>*Format: text* |
| `resource` | yes | `articles-create-request-resource` |  |
| `scope` | no | `integer` | The scope of the article.<br>*Format: int64* |
| `shared_with` | no | `array<set-shared-with-membership>` | Information about the role the member receives due to the share. |
| `status` | no | `string` | Status of the article.<br>*Value in: "archived" \| "draft" \| "published" \| "review_needed"* |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the article. |
| `title` | yes | `string` | Name of the article.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/articles.create" \
  -H "Content-Type: application/json" \
  -d '{
    "owned_by": [
      "DEVU-12345"
    ],
    "resource": {},
    "title": "string"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "article": {
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
}
```

</details>


<a id="delete-article"></a>

## `POST /articles.delete`

**Delete Article**

Source: <https://developer.devrev.ai/beta/api-reference/articles/delete-article>

Deletes an article.

**Required scopes:**

- `article:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the article to delete.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/articles.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ART-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="get-article"></a>

## `GET /articles.get`

**Get Article**

Source: <https://developer.devrev.ai/beta/api-reference/articles/get-article>

Gets an article.

**Required scopes:**

- `article:read` OR `article:write` OR `article:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the required article.<br>*Format: id* |
| `parent_article_id` | no | `string` | The parent article of the content block. The id field is expected to contain the content block ID.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/articles.get?id=ART-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "article": {
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
}
```

</details>


<a id="get-article-post"></a>

## `POST /articles.get`

**Get Article (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/articles/get-article-post>

Gets an article.

**Required scopes:**

- `article:read` OR `article:write` OR `article:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the required article.<br>*Format: id* |
| `parent_article_id` | no | `string` | The parent article of the content block. The id field is expected to contain the content block ID.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/articles.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ART-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "article": {
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
}
```

</details>


<a id="list-articles"></a>

## `GET /articles.list`

**List Articles**

Source: <https://developer.devrev.ai/beta/api-reference/articles/list-articles>

Lists a collection of articles.

**Required scopes:**

- `article:read` OR `article:write` OR `article:all`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_parts` | no | `array<string>` | Filters for articles belonging to any of the provided parts. |
| `article_type` | no | `array<article-type>` | Filter for the type of articles. If this is not provided, then articles that are not content blocks are returned. |
| `authored_by` | no | `array<string>` | Filters for articles authored by any of the provided users. |
| `brands` | no | `array<string>` | Filters for articles belonging to any of the provided brands. |
| `created_by` | no | `array<string>` | Filters for articles created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of articles to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for articles modified by any of the provided users. |
| `owned_by` | no | `array<string>` | Filters for articles owned by any of the provided users. |
| `parent` | no | `array<string>` | Filters for articles with the provided parent directories. |
| `scope` | no | `array<integer>` | Filter for the scope of the articles. |
| `shared_with.member` | no | `string` | ID of the group/member with whom the item is shared.<br>*Format: id* |
| `shared_with.role` | no | `string` | Role ID of the group/member with whom the item is shared.<br>*Format: id* |
| `status` | no | `array<article-status>` | Filters for status of the articles. |
| `sync_metadata.external_record` | no | `array<string>` | Filters for issues with this specific external record. |
| `sync_metadata.external_record_type` | no | `array<string>` | Filters for issues with this specific external record type. |
| `sync_metadata.external_reference` | no | `array<string>` | Filters for issues with this specific external reference. |
| `sync_metadata.last_sync_in.status` | no | `array<sync-metadata-filter-sync-in-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_in.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_in.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.last_sync_out.status` | no | `array<sync-metadata-filter-sync-out-filter-status>` | Filters for works with selected sync statuses. |
| `sync_metadata.last_sync_out.sync_history` | no | `array<string>` | Filters for works modified with selected sync history. |
| `sync_metadata.last_sync_out.sync_unit` | no | `array<string>` | Filters for works modified with selected sync units. |
| `sync_metadata.origin_system` | no | `array<string>` | Filters for issues synced from this specific origin system. |
| `tags` | no | `array<string>` | Filters for article with any of the provided tags. |

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
curl -X GET "https://api.devrev.ai/articles.list"
```

<details><summary>Example 200 response</summary>

```json
{
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
  ],
  "next_cursor": "string",
  "prev_cursor": "string",
  "total": 0
}
```

</details>


<a id="list-articles-post"></a>

## `POST /articles.list`

**List Articles (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/articles/list-articles-post>

Lists a collection of articles.

**Required scopes:**

- `article:read` OR `article:write` OR `article:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_parts` | no | `array<string>` | Filters for articles belonging to any of the provided parts. |
| `article_type` | no | `array<article-type>` | Filter for the type of articles. If this is not provided, then articles that are not content blocks are returned. |
| `authored_by` | no | `array<string>` | Filters for articles authored by any of the provided users. |
| `brands` | no | `array<string>` | Filters for articles belonging to any of the provided brands. |
| `created_by` | no | `array<string>` | Filters for articles created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of articles to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `modified_by` | no | `array<string>` | Filters for articles modified by any of the provided users. |
| `owned_by` | no | `array<string>` | Filters for articles owned by any of the provided users. |
| `parent` | no | `array<string>` | Filters for articles with the provided parent directories. |
| `scope` | no | `array<integer>` | Filter for the scope of the articles. |
| `shared_with` | no | `array<shared-with-membership-filter>` | Filter for articles based on intended audience. |
| `status` | no | `array<article-status>` | Filters for status of the articles. |
| `sync_metadata` | no | `sync-metadata-filter` |  |
| `tags` | no | `array<string>` | Filters for article with any of the provided tags. |

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
curl -X POST "https://api.devrev.ai/articles.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
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
  ],
  "next_cursor": "string",
  "prev_cursor": "string",
  "total": 0
}
```

</details>


<a id="update-article"></a>

## `POST /articles.update`

**Update Article**

Source: <https://developer.devrev.ai/beta/api-reference/articles/update-article>

Updates an article.

**Required scopes:**

- `article:write` OR `article:all`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `access_level` | no | `string` | *Value in: "external" \| "internal" \| "private" \| "public" \| "restricted"* |
| `aliases` | no | `articles-update-request-aliases` |  |
| `applies_to_parts` | no | `articles-update-request-applies-to-parts` |  |
| `artifacts` | no | `articles-update-request-artifacts` |  |
| `attachments` | no | `articles-update-request-attachments` |  |
| `authored_by` | no | `articles-update-request-authored-by` |  |
| `brand` | no | `string\|null` | The updated brand of the article.<br>*Format: id* |
| `content_artifact` | no | `string` | Updates the content artifact of the article. This should be used with 'file' type of articles. Use versioning for devrev/rt and drdfv2 format of articles.<br>*Format: id* |
| `content_blocks` | no | `articles-update-request-content-blocks` |  |
| `content_format` | no | `string` | Content format of the article.<br>*Value in: "drdfv2" \| "rt"* |
| `custom_fields` | no | `object` | Application-defined custom fields. |
| `custom_schema_spec` | no | `custom-schema-spec` | Custom schemas described using identifiers. Each custom field in the request must have the corresponding schema specified; omission results in a Bad Request error. If a custom schema is not included in the specifier, it remains unchanged. For surfaces with human interactors, it is recommended to provide tenant_fragment: true and validate_required_fields: true. |
| `data_sources` | no | `articles-update-request-article-data-source-update` |  |
| `description` | no | `string` | Updated description of the article object, or unchanged if not provided.<br>*Format: text* |
| `extracted_content` | no | `articles-update-request-extracted-content` |  |
| `id` | yes | `string` | The article's ID.<br>*Format: id* |
| `language` | no | `string` | Updates the language of the article.<br>*Format: text* |
| `notify` | no | `boolean` | Whether to notify the users when the article is published. |
| `owned_by` | no | `articles-update-request-owned-by` |  |
| `parent` | no | `string\|null` | The updated parent directory for the article.<br>*Format: id* |
| `published_version` | no | `string` | Updates the the latest published version.<br>*Format: text* |
| `release_notes` | no | `string` | Updates the release notes of the article.<br>*Format: text* |
| `reorder` | no | `articles-update-request-reorder` |  |
| `shared_with` | no | `articles-update-request-shared-with` |  |
| `status` | no | `string` | Status of the article.<br>*Value in: "archived" \| "draft" \| "published" \| "review_needed"* |
| `tags` | no | `articles-update-request-tags` |  |
| `title` | no | `string` | Updated title of the article object, or unchanged if not provided.<br>*Format: text* |
| `url` | no | `string` | Updates the URL of the external article.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/articles.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ART-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "article": {
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
}
```

</details>
