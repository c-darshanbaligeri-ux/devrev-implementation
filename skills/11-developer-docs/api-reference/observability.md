# Observability

Source: <https://developer.devrev.ai/api-reference/observability>
Scraped: 2026-11-03

## Endpoints

| Method | Path | Page |
| --- | --- | --- |
| POST | `/observability.sessions.aggregate` | [sessions-aggregate](#sessions-aggregate) |
| GET | `/observability.sessions.data.get` | [sessions-data-get](#sessions-data-get) |
| POST | `/observability.sessions.data.get` | [sessions-data-get-post](#sessions-data-get-post) |
| GET | `/observability.sessions.developer-info.get` | [sessions-developer-info-get](#sessions-developer-info-get) |
| POST | `/observability.sessions.developer-info.get` | [sessions-developer-info-get-post](#sessions-developer-info-get-post) |
| GET | `/observability.sessions.get` | [sessions-get](#sessions-get) |
| POST | `/observability.sessions.get` | [sessions-get-post](#sessions-get-post) |
| GET | `/observability.sessions.list` | [sessions-list](#sessions-list) |
| POST | `/observability.sessions.list` | [sessions-list-post](#sessions-list-post) |

<a id="sessions-aggregate"></a>

## `POST /observability.sessions.aggregate`

**Aggregate Observability Sessions**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-aggregate>

Aggregates the sessions data.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `mobile-sessions-filter`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "mobile" \| "web"* |
| `aggregations` | no | `array<observability-sessions-aggregate-request-aggregation-config>` | List of aggregation configurations. Each aggregation has a key field for identification. |
| `partition_filters` | no | `object` | To filter indexes by partition fields. |
| `schema_type` | yes | `string` | *Value in: "mobile_custom_events" \| "mobile_network" \| "web_console" \| "web_custom_events" \| "web_event" \| "web_network"* |
| `time_range` | yes | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text*<br>*Length: 1 <= length* |
| `app_version` | no | `array<string>` | Filter by app versions. |
| `created_at` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `custom_events` | no | `mobile-sessions-filter-custom-events-filter` |  |
| `device_model` | no | `array<string>` | Filter by device models. |
| `has_exception_occurred` | no | `boolean` | Filter by exception occurrence. |
| `is_anonymous` | no | `boolean` | Filter by anonymous users. |
| `is_anr` | no | `boolean` | Filter by ANR occurrence. |
| `is_crash` | no | `boolean` | Filter by crash occurrence. |
| `manufacturer` | no | `array<string>` | Filter by device manufacturers. |
| `network_type` | no | `array<string>` | Filter by network types. |
| `os_version` | no | `array<string>` | Filter by OS versions. |
| `rage_tap` | no | `boolean` | Filter by rage tap. |
| `response_time_list` | no | `mobile-sessions-filter-response-time-list-filter` |  |
| `rev_org` | no | `array<string>` | Filter by Rev org. |
| `rev_user` | no | `array<string>` | Filter by Rev user. |
| `screen_name` | no | `array<string>` | Filter by screen name. |
| `session_attributes` | no | `array<session-custom-attribute-filter>` | Filter by session attributes. |
| `session_duration` | no | `mobile-sessions-filter-session-duration-range` |  |

#### Variant `web-sessions-filter`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

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
curl -X POST "https://api.devrev.ai/observability.sessions.aggregate" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "mobile",
    "schema_type": "mobile_custom_events",
    "time_range": {
      "type": "preset"
    },
    "version_key": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "aggregations": [
    {
      "key": "string",
      "result_type": "bucket_results",
      "buckets": [
        {
          "bucket_type": "bucket",
          "doc_count": 18446744073709552000,
          "key": null,
          "sub_aggregations": [
            {
              "key": "string",
              "result_type": "bucket_results",
              "buckets": []
            }
          ]
        }
      ]
    }
  ]
}
```

</details>


<a id="sessions-data-get"></a>

## `GET /observability.sessions.data.get`

**Get Observability Sessions Data**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-data-get>

Retrieves the recording data for a specific session ID and recording ID. For mobile sessions, requires both session_id and recording_id. For web sessions, requires both session_id and tab_id.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `session_id` | yes | `string` | The unique identifier of the session containing the recording.<br>*Format: text* |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text* |
| `include_replay_data` | no | `boolean` | Whether to include replay data in the response. Defaults to true. |
| `recording_id` | no | `string` | The unique identifier of the recording to retrieve in case of mobile sessions.<br>*Format: text* |
| `tab_id` | no | `string` | The unique identifier of the tab to retrieve in case of web sessions.<br>*Format: text* |

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
curl -X GET "https://api.devrev.ai/observability.sessions.data.get?session_id=string&version_key=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "recording": "mobile_recording",
  "app_launch": {
    "launch_time_ms": 0,
    "launch_type": "cold"
  },
  "available_ram": 0,
  "created_at": "2023-01-01T12:00:00.000Z",
  "device_metadata": {
    "app_version": "string",
    "manufacturer": "string",
    "model": "string",
    "network_type": "string",
    "os_version": "string",
    "plug_sdk_version": "string",
    "screen_height": 0,
    "screen_width": 0,
    "sdk_version": "string"
  },
  "observability_sessions_log_data": {
    "is_anr": true,
    "is_crash": true,
    "value": "string"
  },
  "recording_events_timeline": [
    {
      "coordinates": [
        {
          "x": 0.1,
          "y": 0.1
        }
      ],
      "custom_tag": "string",
      "event_name": "anr",
      "event_properties": {},
      "event_type": "plug",
      "exception_class_name": "string",
      "exception_tag": "string",
      "input_type": "system_event_os",
      "name": "string",
      "non_responsive": true,
      "object_name": "string",
      "request_properties": {},
      "response_properties": {},
      "screen": "string",
      "timestamp_offset_ms": 0
    }
  ],
  "recording_id": "string",
  "rev_org_id": "REV-AbCdEfGh",
  "rev_user_id": "string",
  "session_id": "string",
  "total_ram": 0,
  "user_attributes": {},
  "video_playback_data": [
    {
      "end_frame": "string",
      "frame_image_map": {
        "property1": "string",
        "property2": "string"
      },
      "frames": [
        "string"
      ],
      "presigned_url": "string",
      "start_frame": "string"
    }
  ]
}
```

</details>


<a id="sessions-data-get-post"></a>

## `POST /observability.sessions.data.get`

**Get Observability Sessions Data (POST)**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-data-get-post>

Retrieves the recording data for a specific session ID and recording ID. For mobile sessions, requires both session_id and recording_id. For web sessions, requires both session_id and tab_id.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `include_replay_data` | no | `boolean` | Whether to include replay data in the response. Defaults to true. |
| `recording_id` | no | `string` | The unique identifier of the recording to retrieve in case of mobile sessions.<br>*Format: text* |
| `session_id` | yes | `string` | The unique identifier of the session containing the recording.<br>*Format: text* |
| `tab_id` | no | `string` | The unique identifier of the tab to retrieve in case of web sessions.<br>*Format: text* |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text* |

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
curl -X POST "https://api.devrev.ai/observability.sessions.data.get" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "string",
    "version_key": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "recording": "mobile_recording",
  "app_launch": {
    "launch_time_ms": 0,
    "launch_type": "cold"
  },
  "available_ram": 0,
  "created_at": "2023-01-01T12:00:00.000Z",
  "device_metadata": {
    "app_version": "string",
    "manufacturer": "string",
    "model": "string",
    "network_type": "string",
    "os_version": "string",
    "plug_sdk_version": "string",
    "screen_height": 0,
    "screen_width": 0,
    "sdk_version": "string"
  },
  "observability_sessions_log_data": {
    "is_anr": true,
    "is_crash": true,
    "value": "string"
  },
  "recording_events_timeline": [
    {
      "coordinates": [
        {
          "x": 0.1,
          "y": 0.1
        }
      ],
      "custom_tag": "string",
      "event_name": "anr",
      "event_properties": {},
      "event_type": "plug",
      "exception_class_name": "string",
      "exception_tag": "string",
      "input_type": "system_event_os",
      "name": "string",
      "non_responsive": true,
      "object_name": "string",
      "request_properties": {},
      "response_properties": {},
      "screen": "string",
      "timestamp_offset_ms": 0
    }
  ],
  "recording_id": "string",
  "rev_org_id": "REV-AbCdEfGh",
  "rev_user_id": "string",
  "session_id": "string",
  "total_ram": 0,
  "user_attributes": {},
  "video_playback_data": [
    {
      "end_frame": "string",
      "frame_image_map": {
        "property1": "string",
        "property2": "string"
      },
      "frames": [
        "string"
      ],
      "presigned_url": "string",
      "start_frame": "string"
    }
  ]
}
```

</details>


<a id="sessions-developer-info-get"></a>

## `GET /observability.sessions.developer-info.get`

**Get Observability Sessions Developer Info**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-developer-info-get>

Retrieves detailed console and network data for debugging.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `session_id` | yes | `string` | The unique identifier of the session.<br>*Format: text*<br>*Length: 1 <= length* |
| `tab_id` | yes | `string` | unique tab id of the web session.<br>*Format: text*<br>*Length: 1 <= length* |
| `version_key` | yes | `string` | version key of the app.<br>*Format: text*<br>*Length: 1 <= length* |
| `console_log_types` | no | `array<console-log-type>` | Filter console logs by type. If empty, all types are returned. |
| `status_code_classes` | no | `array<status-code-class>` | Filter network logs by HTTP status code class. If empty, all classes are returned. |

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
curl -X GET "https://api.devrev.ai/observability.sessions.developer-info.get?session_id=string&tab_id=string&version_key=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "console_data": [
    {
      "type": "error",
      "full_url": "string",
      "properties": {
        "normalized_url": "string",
        "page_name": "string",
        "page_url": "string"
      },
      "timestamp": "2023-01-01T12:00:00.000Z",
      "value": "string"
    }
  ],
  "network_data": [
    {
      "type": "css",
      "request": {
        "method": "string",
        "start_time": "2023-01-01T12:00:00.000Z",
        "url": "string"
      },
      "response": {
        "end_time": "2023-01-01T12:00:00.000Z",
        "status": 0
      }
    }
  ]
}
```

</details>


<a id="sessions-developer-info-get-post"></a>

## `POST /observability.sessions.developer-info.get`

**Get Observability Sessions Developer Info (POST)**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-developer-info-get-post>

Retrieves detailed console and network data for debugging.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `console_log_types` | no | `array<console-log-type>` | Filter console logs by type. If empty, all types are returned. |
| `session_id` | yes | `string` | The unique identifier of the session.<br>*Format: text*<br>*Length: 1 <= length* |
| `status_code_classes` | no | `array<status-code-class>` | Filter network logs by HTTP status code class. If empty, all classes are returned. |
| `tab_id` | yes | `string` | unique tab id of the web session.<br>*Format: text*<br>*Length: 1 <= length* |
| `version_key` | yes | `string` | version key of the app.<br>*Format: text*<br>*Length: 1 <= length* |

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
curl -X POST "https://api.devrev.ai/observability.sessions.developer-info.get" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "string",
    "tab_id": "string",
    "version_key": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "console_data": [
    {
      "type": "error",
      "full_url": "string",
      "properties": {
        "normalized_url": "string",
        "page_name": "string",
        "page_url": "string"
      },
      "timestamp": "2023-01-01T12:00:00.000Z",
      "value": "string"
    }
  ],
  "network_data": [
    {
      "type": "css",
      "request": {
        "method": "string",
        "start_time": "2023-01-01T12:00:00.000Z",
        "url": "string"
      },
      "response": {
        "end_time": "2023-01-01T12:00:00.000Z",
        "status": 0
      }
    }
  ]
}
```

</details>


<a id="sessions-get"></a>

## `GET /observability.sessions.get`

**Get Observability Session**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-get>

Gets a specific session metadata by ID.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `platform` | yes | `string` | The platform type to filter sessions by.<br>*Value in: "android" \| "ios" \| "web"* |
| `session_id` | yes | `string` | The unique identifier of the session to retrieve.<br>*Format: text*<br>*Length: 1 <= length* |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text*<br>*Length: 1 <= length* |

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
curl -X GET "https://api.devrev.ai/observability.sessions.get?platform=android&session_id=string&version_key=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "session": {
    "type": "mobile",
    "platform": "android",
    "session_id": "string",
    "created_at": "2023-01-01T12:00:00.000Z",
    "device_metadata": {
      "app_version": "string",
      "manufacturer": "string",
      "model": "string",
      "network_type": "string",
      "os_version": "string",
      "plug_sdk_version": "string",
      "screen_height": 0,
      "screen_width": 0,
      "sdk_version": "string"
    },
    "has_exception_occurred": true,
    "is_anr": true,
    "is_crash": true,
    "rage_tap": true,
    "recording_ids": [
      "string"
    ],
    "rev_org_id": "REV-AbCdEfGh",
    "rev_user_id": "string",
    "session_duration_ms": 0
  }
}
```

</details>


<a id="sessions-get-post"></a>

## `POST /observability.sessions.get`

**Get Observability Session (POST)**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-get-post>

Gets a specific session metadata by ID.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `platform` | yes | `string` | The platform type for the device.<br>*Value in: "android" \| "ios" \| "web"* |
| `session_id` | yes | `string` | The unique identifier of the session to retrieve.<br>*Format: text*<br>*Length: 1 <= length* |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text*<br>*Length: 1 <= length* |

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
curl -X POST "https://api.devrev.ai/observability.sessions.get" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "android",
    "session_id": "string",
    "version_key": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "session": {
    "type": "mobile",
    "platform": "android",
    "session_id": "string",
    "created_at": "2023-01-01T12:00:00.000Z",
    "device_metadata": {
      "app_version": "string",
      "manufacturer": "string",
      "model": "string",
      "network_type": "string",
      "os_version": "string",
      "plug_sdk_version": "string",
      "screen_height": 0,
      "screen_width": 0,
      "sdk_version": "string"
    },
    "has_exception_occurred": true,
    "is_anr": true,
    "is_crash": true,
    "rage_tap": true,
    "recording_ids": [
      "string"
    ],
    "rev_org_id": "REV-AbCdEfGh",
    "rev_user_id": "string",
    "session_duration_ms": 0
  }
}
```

</details>


<a id="sessions-list"></a>

## `GET /observability.sessions.list`

**List Observability Sessions**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-list>

Lists sessions based on filter criteria.

**Required scopes:** No scopes required.

### Query Parameters

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `platform` | yes | `string` | Filter by platform type.<br>*Value in: "android" \| "ios" \| "web"* |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text*<br>*Length: 1 <= length* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of sessions to return.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use, otherwise if not set, then "after" is used.<br>*Value in: "after" \| "before"* |
| `sort_by` | no | `array<string>` | The fields to sort the sessions by and the direction to sort them. |

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
curl -X GET "https://api.devrev.ai/observability.sessions.list?platform=android&version_key=string"
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sessions": [
    {
      "type": "mobile",
      "platform": "android",
      "session_id": "string",
      "created_at": "2023-01-01T12:00:00.000Z",
      "device_metadata": {
        "app_version": "string",
        "manufacturer": "string",
        "model": "string",
        "network_type": "string",
        "os_version": "string",
        "plug_sdk_version": "string",
        "screen_height": 0,
        "screen_width": 0,
        "sdk_version": "string"
      },
      "has_exception_occurred": true,
      "is_anr": true,
      "is_crash": true,
      "rage_tap": true,
      "recording_ids": [
        "string"
      ],
      "rev_org_id": "REV-AbCdEfGh",
      "rev_user_id": "string",
      "session_duration_ms": 0
    }
  ]
}
```

</details>


<a id="sessions-list-post"></a>

## `POST /observability.sessions.list`

**List Observability Sessions (POST)**

Source: <https://developer.devrev.ai/api-reference/observability/sessions-list-post>

Lists sessions based on filter criteria.

**Required scopes:** No scopes required.

### Request Body (`application/json`)

The site presents this body as alternative variant schemas (tabs); each table below is one variant.

#### Variant `mobile-sessions-filter`

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| `type` | yes | `string` | *Value in: "mobile" \| "web"* |
| `cursor` | no | `string` | The cursor to resume iteration from. If not provided, then iteration starts from the beginning.<br>*Format: text* |
| `limit` | no | `integer` | The maximum number of sessions to return.<br>*Format: int32* |
| `mode` | no | `string` | The iteration mode to use. If "after", then entries after the provided cursor will be returned, or if no cursor is provided, then from the beginning. If "before", then entries before the provided cursor will be returned, or if no cursor is provided, then from the end. Entries will always be returned in the specified sort-by order.<br>*Value in: "after" \| "before"* |
| `platform` | yes | `string` | The platform type for the device.<br>*Value in: "android" \| "ios" \| "web"* |
| `sort_by` | no | `array<string>` | The fields to sort the sessions by and the direction to sort them. |
| `version_key` | yes | `string` | The unique app ID to which the session belongs.<br>*Format: text*<br>*Length: 1 <= length* |
| `app_version` | no | `array<string>` | Filter by app versions. |
| `created_at` | no | `date-time-filter\|date-time-preset` | Provides ways to specify date ranges on objects. |
| `custom_events` | no | `mobile-sessions-filter-custom-events-filter` |  |
| `device_model` | no | `array<string>` | Filter by device models. |
| `has_exception_occurred` | no | `boolean` | Filter by exception occurrence. |
| `is_anonymous` | no | `boolean` | Filter by anonymous users. |
| `is_anr` | no | `boolean` | Filter by ANR occurrence. |
| `is_crash` | no | `boolean` | Filter by crash occurrence. |
| `manufacturer` | no | `array<string>` | Filter by device manufacturers. |
| `network_type` | no | `array<string>` | Filter by network types. |
| `os_version` | no | `array<string>` | Filter by OS versions. |
| `rage_tap` | no | `boolean` | Filter by rage tap. |
| `response_time_list` | no | `mobile-sessions-filter-response-time-list-filter` |  |
| `rev_org` | no | `array<string>` | Filter by Rev org. |
| `rev_user` | no | `array<string>` | Filter by Rev user. |
| `screen_name` | no | `array<string>` | Filter by screen name. |
| `session_attributes` | no | `array<session-custom-attribute-filter>` | Filter by session attributes. |
| `session_duration` | no | `mobile-sessions-filter-session-duration-range` |  |

#### Variant `web-sessions-filter`

| Field | Required | Type | Description |
| --- | --- | --- | --- |

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
curl -X POST "https://api.devrev.ai/observability.sessions.list" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "mobile",
    "platform": "android",
    "version_key": "string"
  }'
```

<details><summary>Example 200 response</summary>

```json
{
  "next_cursor": "string",
  "prev_cursor": "string",
  "sessions": [
    {
      "type": "mobile",
      "platform": "android",
      "session_id": "string",
      "created_at": "2023-01-01T12:00:00.000Z",
      "device_metadata": {
        "app_version": "string",
        "manufacturer": "string",
        "model": "string",
        "network_type": "string",
        "os_version": "string",
        "plug_sdk_version": "string",
        "screen_height": 0,
        "screen_width": 0,
        "sdk_version": "string"
      },
      "has_exception_occurred": true,
      "is_anr": true,
      "is_crash": true,
      "rage_tap": true,
      "recording_ids": [
        "string"
      ],
      "rev_org_id": "REV-AbCdEfGh",
      "rev_user_id": "string",
      "session_duration_ms": 0
    }
  ]
}
```

</details>
