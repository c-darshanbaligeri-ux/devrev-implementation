# Versioning

Source: <https://developer.devrev.ai/about/versioning>
Scraped: 2026-08-02

## Public APIs

The current version of the DevRev public API is `2022-10-20`.

By default, requests implicitly use version `2022-10-20` unless you override the API version by passing in the `X-Devrev-Version` header with the requested version.

```
X-Devrev-Version: 2022-10-20
```

When backwards-incompatible changes occur, DevRev releases a new dated version. Customers can opt in by supplying the date string that appears in the documentation.

If a new version is introduced, DevRev gives users sufficient notice to migrate or adopt it. Per the docs: "All public API versions are supported for at least 1 year."

## Beta (early-access) APIs

DevRev offers newer, experimental functionality through beta APIs so early adopters can try them out. These endpoints are expected to evolve based on feedback and don't carry the same backward compatibility or versioning guarantees as the stable public APIs.

To use beta APIs, send the following header with your request:

```
X-Devrev-Scope: beta
```

### On this page

- Public APIs
- Beta (early-access) APIs

---

## Key headers summary

| Header | Value | Purpose |
|---|---|---|
| `X-Devrev-Version` | `2022-10-20` | Selects a specific public API version |
| `X-Devrev-Scope` | `beta` | Opts into beta/early-access APIs |

**Navigation context:** This page sits under the "About" section, between "Pagination" (previous) and "Rate Limits" (next).

**Notes:**

- The exact list of previously-released versions (other than the current `2022-10-20`) is not documented on the page as of scrape date 2026-08-02.
- The formal deprecation-notice mechanism (email? changelog entry? response header?) is not documented on the page as of scrape date 2026-08-02 beyond "sufficient notice".
