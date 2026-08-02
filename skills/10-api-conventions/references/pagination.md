# Pagination

Source: <https://developer.devrev.ai/about/pagination>
Scraped: 2026-08-02

## Overview

When making calls to the DevRev API, results can be extensive, so pagination is used to make responses easier to handle. The DevRev API uses **cursor-based pagination** to provide consistency and support large data sets.

For example, if your initial call requests all users in an org, the result could span hundreds of thousands of pages — not a good starting point.

## How it works

When you make an API call, it returns a cursor with a random code. If there are more pages available, the response will include a field called `next_cursor` which points to the next page.

### Response

```json
{
  "next_cursor": "ufhe492s",
  /* ... Rest of the payload ... */
}
```

If there are no more pages to paginate, the response will not include the `next_cursor` field.

## Advancing to the next page

To advance to the next page, include the `cursor` parameter in your query like this:

```
.../internal/works.list?cursor="u4hf9fd"
```

---

**Navigation:**

- Previous page: [Authentication](/about/authentication)
- Next page: [Versioning](/about/versioning)

**Notes:**

- Per-page size / `limit` semantics, default page size, and maximum page size are not documented on the page as of scrape date 2026-08-02.
- Backwards / reverse pagination (e.g. a `prev_cursor` field) is not documented on the page as of scrape date 2026-08-02.
