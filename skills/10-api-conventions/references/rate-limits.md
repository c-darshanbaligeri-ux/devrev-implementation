# Rate Limits

Source: <https://developer.devrev.ai/about/rate-limits>
Scraped: 2026-08-02

## Overview

DevRev applies rate limits to its APIs to ensure consistent access for all users and prevent overly aggressive clients from affecting others.

Rate limits are applied in aggregate across all requests from an authenticated user. When a user exceeds their limit, further requests are throttled until the rate limit *window* elapses. Per the docs: "this window resets every five minutes."

## 429 Response

When the rate limit is exceeded, the API returns:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

The `Retry-After` header indicates the number of seconds remaining until the rate limit window expires.

## Response Headers

Every response includes headers reflecting current quota and usage:

| Header | Description |
|---|---|
| `X-Ratelimit-Limit` | The user's total rate limit units for the current window. |
| `X-Ratelimit-Remaining` | The user's remaining rate limit units for the current window. |
| `X-Ratelimit-Reset` | The time at which the rate limit window resets, in seconds from the Unix epoch. |

## Example Header Values

```
X-Ratelimit-Limit: 1000
X-Ratelimit-Remaining: 900
X-Ratelimit-Reset: 1720636800
```

## Per-Endpoint Weighting

According to the documentation: "All APIs have the same weight when applying rate limiting, and there is no preference given to any individual API." The docs note this could change in the future.

## Summary of Key Facts

- **Window duration:** 5 minutes (resets every five minutes)
- **Exceeded status code:** HTTP 429 Too Many Requests
- **Retry guidance header:** `Retry-After` (value in seconds)
- **Quota inspection headers:** `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`
- **Reset header format:** Unix epoch seconds
- **Scope:** Aggregate across all requests from an authenticated user
- **Per-endpoint weighting:** Uniform across all APIs (subject to future change)

---

**Notes:**

- No specific numeric limit values (other than the example `1000`) are provided on the page as of scrape date 2026-08-02, and no per-endpoint limits are listed.
- Tiered limits (free vs. paid, standard vs. premium) are not documented on the page as of scrape date 2026-08-02.
- **Skill-8 field note (verified live 2026-07-24, contradicts the repo-root `rate limits.md`):** a real org on this token (`devo/24TiM4xJFF`) showed `x-ratelimit-limit: 8000` and a clean 60-second rolling window on ordinary `works.list` calls. The public page above only defines the *shape* (headers, 429/`Retry-After`, 5-minute window language) — not the numeric ceiling for a given org. Always read `X-Ratelimit-Limit`/`X-Ratelimit-Remaining` from the live response headers rather than hardcoding either the 1000 example value or the repo-root doc's numbers.
