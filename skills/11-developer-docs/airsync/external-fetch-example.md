# External API request example

Source: <https://developer.devrev.ai/airsync/external-fetch-example>
Scraped: 2026-11-03

## Bounded fetch example

This standalone example parses provider `Retry-After` values and reads JSON with a request timeout. It illustrates the client layer; a worker must additionally validate the JSON shape, normalize records and translate a `ProviderError` into the appropriate phase result.

```typescript
export class ProviderError extends Error {
  constructor(
    readonly status: number,
    readonly retryAfterSeconds?: number,
  ) {
    super(`Provider request failed with HTTP ${status}`);
  }
}

export function retryAfterSeconds(value: string | null): number | undefined {
  if (value === null || value.trim() === '') return undefined;
  const seconds = Number(value.trim());
  if (Number.isFinite(seconds) && seconds >= 0) return Math.ceil(seconds);
  const timestamp = Date.parse(value);
  if (!Number.isFinite(timestamp)) return undefined;
  return Math.max(0, Math.ceil((timestamp - Date.now()) / 1000));
}

export async function getProviderJson(
  url: URL,
  token: string,
  timeoutMs: number,
): Promise<unknown> {
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!response.ok) {
    await response.body?.cancel();
    throw new ProviderError(
      response.status,
      retryAfterSeconds(response.headers.get('Retry-After')),
    );
  }
  return response.json();
}
```

The provider may use a different auth scheme or rate-limit header. Follow its API contract. Validate numeric retry values and provide a finite fallback when a header is missing; `delaySeconds` must be nonnegative and finite.

Related: [External API clients](external-api-clients.md).
