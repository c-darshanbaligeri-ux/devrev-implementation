# Artifacts

Source: <https://developer.devrev.ai/api-reference/artifacts>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/artifacts.download` | [download](#download) |
| POST | `/artifacts.download` | [download-post](#download-post) |
| GET | `/artifacts.get` | [get](#get) |
| POST | `/artifacts.get` | [get-post](#get-post) |
| GET | `/artifacts.list` | [list](#list) |
| POST | `/artifacts.list` | [list-post](#list-post) |
| GET | `/artifacts.locate` | [locate](#locate) |
| POST | `/artifacts.locate` | [locate-post](#locate-post) |
| POST | `/artifacts.prepare` | [prepare](#prepare) |
| POST | `/artifacts.versions.delete` | [hard-delete-version](#hard-delete-version) |
| POST | `/artifacts.versions.prepare` | [versions-prepare](#versions-prepare) |

<a id="download"></a>

## `GET /artifacts.download`

**Download Artifacts**

Source: <https://developer.devrev.ai/api-reference/artifacts/download>

Redirects to the artifact's download URL.

**Required scopes:**

- `artifact:read`

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to be downloaded.<br>*Format: id* |
| `key` | no | `string` | The access key for the artifact.<br>*Format: text* |
| `version` | no | `string` | The version of the artifact that needs to be downloaded.<br>*Format: text* |

### Response codes

- `303` — `application/json`
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
curl -X GET "https://api.devrev.ai/artifacts.download?id=ARTIFACT-12345"
```


<a id="download-post"></a>

## `POST /artifacts.download`

**Download Artifacts (POST)**

Source: <https://developer.devrev.ai/api-reference/artifacts/download-post>

Redirects to the artifact's download URL.

**Required scopes:**

- `artifact:read`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to be downloaded.<br>*Format: id* |
| `key` | no | `string` | The access key for the artifact.<br>*Format: text* |
| `version` | no | `string` | The version of the artifact that needs to be downloaded.<br>*Format: text* |

### Response codes

- `303` — `application/json`
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
curl -X POST "https://api.devrev.ai/artifacts.download" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ARTIFACT-12345"
  }'
```


<a id="get"></a>

## `GET /artifacts.get`

**Get Artifact**

Source: <https://developer.devrev.ai/api-reference/artifacts/get>

Gets the requested artifact's information.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested artifact's ID.<br>*Format: id* |
| `version` | no | `string` | The version of the artifact that needs to be fetched.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/artifacts.get?id=ARTIFACT-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "artifact": {
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
    "file": {
      "type": "string",
      "name": "string",
      "size": 0
    }
  },
  "version": {
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
    "timestamp": "2023-01-01T12:00:00.000Z",
    "version": "string"
  }
}
```

</details>


<a id="get-post"></a>

## `POST /artifacts.get`

**Get Artifact (POST)**

Source: <https://developer.devrev.ai/api-reference/artifacts/get-post>

Gets the requested artifact's information.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The requested artifact's ID.<br>*Format: id* |
| `version` | no | `string` | The version of the artifact that needs to be fetched.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/artifacts.get" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ARTIFACT-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "artifact": {
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
    "file": {
      "type": "string",
      "name": "string",
      "size": 0
    }
  },
  "version": {
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
    "timestamp": "2023-01-01T12:00:00.000Z",
    "version": "string"
  }
}
```

</details>


<a id="list"></a>

## `GET /artifacts.list`

**List Artifacts**

Source: <https://developer.devrev.ai/api-reference/artifacts/list>

List the artifacts attached to an object.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `parent_id` | no | `string` | The ID of the object to filter artifacts.<br>*Format: id* |

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
curl -X GET "https://api.devrev.ai/artifacts.list"
```

<details><summary>Example 200 response</summary>

```json
{
  "artifacts": [
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
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    }
  ]
}
```

</details>


<a id="list-post"></a>

## `POST /artifacts.list`

**List Artifacts (POST)**

Source: <https://developer.devrev.ai/api-reference/artifacts/list-post>

List the artifacts attached to an object.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `parent_id` | no | `string` | The ID of the object to filter artifacts.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/artifacts.list" \
  -H "Content-Type: application/json" \
  -d '{}'
```

<details><summary>Example 200 response</summary>

```json
{
  "artifacts": [
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
      "file": {
        "type": "string",
        "name": "string",
        "size": 0
      }
    }
  ]
}
```

</details>


<a id="locate"></a>

## `GET /artifacts.locate`

**Locate Artifacts**

Source: <https://developer.devrev.ai/api-reference/artifacts/locate>

Gets the download URL for the artifact.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to get the URL for.<br>*Format: id* |
| `version` | no | `string` | The version of the artifact that needs to be fetched.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/artifacts.locate?id=ARTIFACT-12345"
```

<details><summary>Example 200 response</summary>

```json
{
  "expires_at": "2023-01-01T12:00:00.000Z",
  "url": "string"
}
```

</details>


<a id="locate-post"></a>

## `POST /artifacts.locate`

**Locate Artifacts (POST)**

Source: <https://developer.devrev.ai/api-reference/artifacts/locate-post>

Gets the download URL for the artifact.

**Required scopes:**

- `artifact:read`

Also needs parent read access.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to get the URL for.<br>*Format: id* |
| `version` | no | `string` | The version of the artifact that needs to be fetched.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/artifacts.locate" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ARTIFACT-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "expires_at": "2023-01-01T12:00:00.000Z",
  "url": "string"
}
```

</details>


<a id="prepare"></a>

## `POST /artifacts.prepare`

**Prepare Artifacts**

Source: <https://developer.devrev.ai/api-reference/artifacts/prepare>

Creates an artifact and generates an upload URL for its data.

**Required scopes:**

- `artifact:create`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `configuration_set` | no | `string` | Represents a set of configuration to be used with the artifacts object.<br>*Value in: "article_media" \| "default" \| "email_media" \| "favicon" \| "job_data" \| "marketplace_listing_icon" \| "marketplace_media" \| "meeting_recordings" \| "object_export" \| "org_logo" \| "plug_css" \| "plug_setting" \| "plug_setting_banner_card" \| "portal_css" \| "snap_in_functions_code" \| "snap_widget" \| "user_profile_picture" \| "work"* |
| `file_encoding` | no | `string` | The encoding of the file that's being uploaded.<br>*Format: text* |
| `file_name` | yes | `string` | The name of the file that's being uploaded.<br>*Format: text* |
| `file_type` | no | `string` | The type of file that's being uploaded.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/artifacts.prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "form_data": [
    {
      "key": "string",
      "value": "string"
    }
  ],
  "id": "ARTIFACT-12345",
  "url": "string"
}
```

</details>


<a id="hard-delete-version"></a>

## `POST /artifacts.versions.delete`

**Delete Artifacts Version**

Source: <https://developer.devrev.ai/api-reference/artifacts/hard-delete-version>

Permanently deletes a version of an artifact.

**Required scopes:**

- `artifact:create`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to delete the version for.<br>*Format: id* |
| `version` | no | `string` | The version of the artifact that needs to be deleted.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/artifacts.versions.delete" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ARTIFACT-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{}
```

</details>


<a id="versions-prepare"></a>

## `POST /artifacts.versions.prepare`

**Prepare Artifacts Versions**

Source: <https://developer.devrev.ai/api-reference/artifacts/versions-prepare>

Prepares a new version for an artifact, returning the URL and form data to upload the updated file.

**Required scopes:**

- `artifact:create`

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `id` | yes | `string` | The ID of the artifact to prepare a new version for.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/artifacts.versions.prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ARTIFACT-12345"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "form_data": [
    {
      "key": "string",
      "value": "string"
    }
  ],
  "url": "string"
}
```

</details>
