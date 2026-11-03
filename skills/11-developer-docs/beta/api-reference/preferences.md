# Preferences

Source: <https://developer.devrev.ai/beta/api-reference/preferences>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| GET | `/preferences.get` | [get](#get) |
| POST | `/preferences.get` | [get-post](#get-post) |
| POST | `/preferences.update` | [update](#update) |

<a id="get"></a>

## `GET /preferences.get`

**Get Preference**

Source: <https://developer.devrev.ai/beta/api-reference/preferences/get>

Get the preferences object.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `object` | yes | `string` | The ID of the target object for which preferences object is to be fetched.<br>*Format: id* |
| `type` | yes | `string` | Type of the preference object to be fetched.<br>*Value in: "user_preferences"* |
| `language_code` | no | `string` | Language code for which to get the preferences for.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/preferences.get?object=DEV-AbCdEfGh&type=user_preferences"
```

<details><summary>Example 200 response</summary>

```json
{
  "preference": {
    "type": "user_preferences",
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
    "general_preferences": {
      "availability": {
        "manual_away": true
      },
      "preferred_locale": "string"
    }
  }
}
```

</details>


<a id="get-post"></a>

## `POST /preferences.get`

**Get Preference (POST)**

Source: <https://developer.devrev.ai/beta/api-reference/preferences/get-post>

Get the preferences object.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "user_preferences"* |
| `language_code` | no | `string` | Language code for which to get the preferences for.<br>*Format: text* |
| `object` | yes | `string` | The ID of the target object for which preferences object is to be fetched.<br>*Format: id* |

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
curl -X POST "https://api.devrev.ai/preferences.get" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "user_preferences",
    "object": "DEV-AbCdEfGh"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "preference": {
    "type": "user_preferences",
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
    "general_preferences": {
      "availability": {
        "manual_away": true
      },
      "preferred_locale": "string"
    }
  }
}
```

</details>


<a id="update"></a>

## `POST /preferences.update`

**Update Preference**

Source: <https://developer.devrev.ai/beta/api-reference/preferences/update>

Updates the preference for a particular object.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `update-user-preferences`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "user_preferences"* |
| `language_code` | no | `string` | Language code for which to update the preferences for.<br>*Format: text* |
| `object` | yes | `string` | The ID of the object for which the preferences are to be updated.<br>*Format: id* |
| `general_preferences` | no | `update-general-preferences-group` | Update object for GeneralPreferencesGroup. |

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
curl -X POST "https://api.devrev.ai/preferences.update" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "user_preferences",
    "object": "DEV-AbCdEfGh"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "preferences": {
    "type": "user_preferences",
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
    "general_preferences": {
      "availability": {
        "manual_away": true
      },
      "preferred_locale": "string"
    }
  }
}
```

</details>
