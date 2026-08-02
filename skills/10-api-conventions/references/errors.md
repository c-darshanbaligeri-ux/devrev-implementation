# Errors

Source: <https://developer.devrev.ai/about/errors>
Scraped: 2026-08-02

DevRev's APIs use standard HTTP status codes in responses. Successful requests return a `20X` status code with any response data per the OpenAPI specification.

## Success Status Codes

| Status Code | Status | Description |
|---|---|---|
| `200` | `OK` | The request succeeded and the result is contained in the response. |
| `201` | `Created` | The request successfully created an object and the result is contained in the response. |
| `204` | `No Content` | The request succeeded and contains no response data. This is common for object deletions. |

## Error Response Format

When errors occur across APIs, the response includes a JSON object with a `message` field providing supplemental information about the error.

Example error response:

```
HTTP/1.1 404 Not Found
Content-Type: application/json
Content-Length: 29
{"message":"route not found"}
```

## Common Error Status Codes

| Status Code | Status | Description |
|---|---|---|
| `400` | `Bad Request` | The request was malformed or contained invalid arguments. |
| `401` | `Unauthorized` | "The user attempted to access an endpoint that requires authentication and no credentials were provided or their validation failed." |
| `403` | `Forbidden` | The user isn't authorized to perform the requested action. |
| `404` | `Not Found` | The requested endpoint doesn't exist. |
| `429` | `Too Many Requests` | The user is currently throttled due to exceeding their permitted rate limit. The `Retry-After` response header contains the number of seconds before the user should retry. |
| `500` | `Internal Server Error` | "An internal error was encountered in the handling of the request which couldn't be processed to completion." DevRev is automatically alerted; retry after a short delay and contact DevRev support if the issue continues. |
| `503` | `Service Unavailable` | A transient error was encountered and the user should retry after a short delay. |

## Endpoint-Specific Status Codes

Individual endpoints may include additional status codes in the OpenAPI specification to denote special behavior.

| Status Code | Status | Description |
|---|---|---|
| `301` | `Moved Permanently` | The target resource's ID has changed, where the `Location` response header contains the updated ID. |
| `404` | `Not Found` | The target object or requested resource doesn't exist. |
| `409` | `Conflict` | "The attempted object creation conflicted with an existing object, for example, a group with the same name already exists." |

---

**Notes:**

- A structured error `type`/`code` enum (e.g. `invalid_field`, `missing_required_field`, `customization_validation_error`) is not documented on this page as of scrape date 2026-08-02, even though skill-1/skill-8 live findings observe such fields in real 4xx bodies (`{"type":"invalid_field","field_name":"..."}`, `{"type":"customization_validation_error","subtype":"field_not_in_schema", ...}`). The public "About > Errors" page only documents the `message` field; the additional `type`/`field_name`/`subtype`/`reason` keys observed in practice are not called out on the page.
- Per-endpoint status codes beyond the three examples (`301`, `404`, `409`) are not enumerated on this page as of scrape date 2026-08-02 — the OpenAPI spec is the authoritative source per the page itself.
