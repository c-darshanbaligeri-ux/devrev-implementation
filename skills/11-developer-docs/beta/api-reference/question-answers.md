# Question Answers

Source: <https://developer.devrev.ai/beta/api-reference/question-answers>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/question-answers.create` | [create-question-answer](#create-question-answer) |
| POST | `/question-answers.delete` | [delete-question-answer](#delete-question-answer) |
| GET | `/question-answers.get` | [get-question-answer](#get-question-answer) |
| POST | `/question-answers.get` | [get-question-answer-post](#get-question-answer-post) |
| GET | `/question-answers.list` | [list-question-answers](#list-question-answers) |
| POST | `/question-answers.list` | [list-question-answers-post](#list-question-answers-post) |
| POST | `/question-answers.update` | [update-question-answer](#update-question-answer) |

<a id="create-question-answer"></a>

## `POST /question-answers.create`

**Create Question Answer**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/create-question-answer>

Creates a question-answer.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `access_level` | no | `string` | *Value in: "external" \| "internal" \| "private" \| "public" \| "restricted"* |
| `answer` | yes | `string` | Answer of the question-answer.<br>*Format: text* |
| `applies_to_articles` | no | `array<string>` | The articles that the question-answer applies to. |
| `applies_to_parts` | yes | `array<string>` | The parts that the question-answer applies to.<br>*Items: 1 <= items* |
| `owned_by` | yes | `array<string>` | The users that own the question-answer. |
| `question` | yes | `string` | Question of the question-answer.<br>*Format: text* |
| `shared_with` | no | `array<set-shared-with-membership>` | Information about the role the member receives due to the share. |
| `sources` | no | `array<string>` | The source of the question-answer. |
| `status` | yes | `string` | Status of the question answer.<br>*Value in: "archived" \| "discarded" \| "draft" \| "published" \| "review_needed"* |
| `suggested_answer` | no | `string` | Alternative answer for the question-answer sugested by Q/A Discovery.<br>*Format: text* |
| `suggested_for_deletion` | no | `boolean` | Whether the question-answer was suggeste to be deleted by Q/A Discovery. |
| `tags` | no | `array<set-tag-with-value>` | Tags associated with the question-answer. |
| `topic` | no | `string` | Topic of the question-answer.<br>*Format: text* |
| `verified` | no | `boolean` | Whether the question-answer was verified by a user or not. |

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
curl -X POST "https://api.devrev.ai/question-answers.create" \
  -H "Content-Type: application/json" \
  -d '{
    "answer": "string",
    "applies_to_parts": [
      "PROD-12345"
    ],
    "owned_by": [
      "DEVU-12345"
    ],
    "question": "string",
    "status": "archived"
  }'
```

<details><summary>Example 201 response</summary>

```json
{
  "question_answer": {
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
    "answer": "string",
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
    "question": "string",
    "sources": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "status": "archived",
    "suggested_answer": "string",
    "suggested_for_deletion": true,
    "topic": "string",
    "verified": true
  }
}
```

</details>


<a id="delete-question-answer"></a>

## `POST /question-answers.delete`

**Delete Question Answer**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/delete-question-answer>

Deletes a question-answer.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the question-answer.<br>*Format: id* |
| `question_answer_id` | no | `string` | **Deprecated.**<br>The ID of the question-answer.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/question-answers.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```


<a id="get-question-answer"></a>

## `GET /question-answers.get`

**Get Question Answer**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/get-question-answer>

Gets a question-answer.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the required question-answer.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/question-answers.get?id=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "question_answer": {
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
    "answer": "string",
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
    "question": "string",
    "sources": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "status": "archived",
    "suggested_answer": "string",
    "suggested_for_deletion": true,
    "topic": "string",
    "verified": true
  }
}
```

</details>


<a id="get-question-answer-post"></a>

## `POST /question-answers.get`

**Get Question Answer (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/get-question-answer-post>

Gets a question-answer.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the required question-answer.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/question-answers.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "question_answer": {
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
    "answer": "string",
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
    "question": "string",
    "sources": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "status": "archived",
    "suggested_answer": "string",
    "suggested_for_deletion": true,
    "topic": "string",
    "verified": true
  }
}
```

</details>


<a id="list-question-answers"></a>

## `GET /question-answers.list`

**List Question Answers**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/list-question-answers>

Lists a collection of question-answers.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_articles` | no | `array<string>` | Filters for question-answer belonging to any of the provided articles. |
| `applies_to_parts` | no | `array<string>` | Filters for question-answer belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for question-answers created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of question-answers to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `owned_by` | no | `array<string>` | Filters for question-answers owned by any of the provided users. |

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
curl -X GET "https://api.devrev.ai/question-answers.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "question_answers": [
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
      "answer": "string",
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
      "question": "string",
      "sources": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ],
      "status": "archived",
      "suggested_answer": "string",
      "suggested_for_deletion": true,
      "topic": "string",
      "verified": true
    }
  ],
  "total": 0
}
```

</details>


<a id="list-question-answers-post"></a>

## `POST /question-answers.list`

**List Question Answers (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/list-question-answers-post>

Lists a collection of question-answers.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `applies_to_articles` | no | `array<string>` | Filters for question-answer belonging to any of the provided articles. |
| `applies_to_parts` | no | `array<string>` | Filters for question-answer belonging to any of the provided parts. |
| `created_by` | no | `array<string>` | Filters for question-answers created by any of the provided users. |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of question-answers to return. The default is '50'.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `owned_by` | no | `array<string>` | Filters for question-answers owned by any of the provided users. |

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
curl -X POST "https://api.devrev.ai/question-answers.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "question_answers": [
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
      "answer": "string",
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
      "question": "string",
      "sources": [
        {
          "type": "account",
          "display_id": "string",
          "id": "string",
          "display_name": "string"
        }
      ],
      "status": "archived",
      "suggested_answer": "string",
      "suggested_for_deletion": true,
      "topic": "string",
      "verified": true
    }
  ],
  "total": 0
}
```

</details>


<a id="update-question-answer"></a>

## `POST /question-answers.update`

**Update Question Answer**

Source: <https://developer.devrev.ai/beta/api-reference/question-answers/update-question-answer>

Updates a question-answer.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `access_level` | no | `string` | *Value in: "external" \| "internal" \| "private" \| "public" \| "restricted"* |
| `answer` | no | `string` | Updated answer of the question-answer object, or unchanged if not provided.<br>*Format: text* |
| `applies_to_articles` | no | `question-answers-update-request-applies-to-articles` |  |
| `applies_to_parts` | no | `question-answers-update-request-applies-to-parts` |  |
| `id` | yes | `string` | The question-answer's ID.<br>*Format: id* |
| `owned_by` | no | `question-answers-update-request-owned-by` |  |
| `question` | no | `string` | Updated question of the question-answer object, or unchanged if not provided.<br>*Format: text* |
| `shared_with` | no | `question-answers-update-request-shared-with` |  |
| `sources` | no | `question-answers-update-request-sources` |  |
| `status` | no | `string` | Status of the question answer.<br>*Value in: "archived" \| "discarded" \| "draft" \| "published" \| "review_needed"* |
| `suggested_answer` | no | `string` | Updated suggested_answer of the question-answer object, or unchanged if not provided.<br>*Format: text* |
| `suggested_for_deletion` | no | `boolean` | Updated suggested_for_deletion of the question-answer object, or unchanged if not provided. |
| `tags` | no | `question-answers-update-request-tags` |  |
| `topic` | no | `string` | Updated topic of the question-answer object, or unchanged if not provided.<br>*Format: text* |
| `verified` | no | `boolean` | Updates whether the question-answer was verified by a user or not. |

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
curl -X POST "https://api.devrev.ai/question-answers.update" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "question_answer": {
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
    "answer": "string",
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
    "question": "string",
    "sources": [
      {
        "type": "account",
        "display_id": "string",
        "id": "string",
        "display_name": "string"
      }
    ],
    "status": "archived",
    "suggested_answer": "string",
    "suggested_for_deletion": true,
    "topic": "string",
    "verified": true
  }
}
```

</details>
