# DevRev API Rate Limits - Reference Guide

## Overview

DevRev API implements rate limiting to ensure fair usage and system stability. This guide provides comprehensive information on rate limits and best practices for handling them during data uploads.

---

## Rate Limit Specifications

<!-- corrected 2026-07-24: the table below is confirmed WRONG for at least one real org/token; see the note immediately after it. Kept for reference/comparison, not as ground truth. -->

### API Rate Limits (as originally documented — see correction below)

| Tier | Requests per Minute | Requests per Hour | Burst Allowance |
|------|---------------------|-------------------|-----------------|
| **Standard** | 600 | 10,000 | 100 |
| **Premium** | 1,200 | 20,000 | 200 |
| **Enterprise** | Custom | Custom | Custom |

**CORRECTED 2026-07-24 — live-verified, and it's much higher than the table above:**
a real token/org (`don:core:dvrv-in-1:devo/24TiM4xJFF`) returned
`x-ratelimit-limit: 8000` on ordinary `works.list` calls, with a clean 60-second
rolling window (`x-ratelimit-reset` landed on an exact 60s boundary measured from
request time). That's over 13x the "Standard" figure this table claims. Tier
naming/exact numbers likely vary per org or plan — **do not hardcode either this
table's numbers or the 8000 figure as a planning assumption for a different
org/token.** Always read `x-ratelimit-limit` / `x-ratelimit-remaining` from the
live response headers and pace off those. See
`skills/8-devrev-api/SKILL.md` → "Accuracy notes" for the full write-up and
`docs/LEARNINGS.md` for the dated journal entry.

**Doc vs. reality on the window (2026-07-31):** `developer.devrev.ai/about/rate-limits`
publicly states the window "resets every five minutes" and treats all APIs as
equal-weight against a single per-token pool (no per-endpoint quotas, no burst
allowance detail). The 2026-07-24 live observation above was a **60-second**
rolling window on `works.list`, i.e. 5× shorter than the docs claim. Both may be
true depending on org/plan — the public doc is the general policy, the observed
value is what this org actually returned. **Trust the response headers over
either number** (`X-Ratelimit-Reset` is the definitive next-reset timestamp;
`Retry-After` is the definitive wait on 429). Neither the public doc nor the
live observation documents burst behavior — treat `Retry-After` as the only
safe retry cadence.

### Headers

DevRev returns these headers with each API response:

```
X-Ratelimit-Limit: 600          # Total requests allowed in window
X-Ratelimit-Remaining: 543      # Requests remaining in current window
X-Ratelimit-Reset: 1716479200   # Unix timestamp when limit resets
Retry-After: 60                 # Seconds to wait (on 429 errors)
```

---

## HTTP 429 Response

When rate limit is exceeded, DevRev returns:

```json
{
  "type": "https://developer.devrev.ai/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "API rate limit exceeded. Please retry after 60 seconds.",
  "retry_after": 60
}
```

---

## Best Practices

### 1. Monitor Rate Limit Headers

Always extract and monitor rate limit headers from responses:

```python
def extract_rate_limit_headers(response):
    limit = response.headers.get('X-Ratelimit-Limit')
    remaining = response.headers.get('X-Ratelimit-Remaining')
    reset = response.headers.get('X-Ratelimit-Reset')
```

### 2. Dynamic Delay Strategy

Adjust upload speed based on quota remaining:

| Quota Remaining | Delay | Strategy |
|----------------|-------|----------|
| **> 80%** | 0.01s | Fast upload (minimal delay) |
| **50-80%** | 0.05s | Moderate throttling |
| **20-50%** | 0.2s | Significant throttling |
| **10-20%** | 0.5s | Conservative |
| **< 10%** | 1.0s | Very conservative |

### 3. Exponential Backoff

On 429 errors, implement exponential backoff:

```python
def calculate_retry_delay(attempt):
    base_delay = 1.0  # Start with 1 second
    max_delay = 60.0  # Cap at 60 seconds
    delay = min(base_delay * (2 ** attempt), max_delay)
    return delay
```

**Retry Schedule:**
- Attempt 1: 1s
- Attempt 2: 2s
- Attempt 3: 4s
- Attempt 4: 8s
- Attempt 5: 16s
- Attempt 6: 32s
- Attempt 7+: 60s (capped)

### 4. Respect Retry-After Header

Always respect the `Retry-After` header when present:

```python
if 'Retry-After' in response.headers:
    wait_time = int(response.headers['Retry-After'])
    time.sleep(wait_time)
```

### 5. Batch Processing

Process records in batches with progress tracking:

```python
BATCH_SIZE = 100  # Update progress every 100 records
```

### 6. Circuit Breaker Pattern

Implement circuit breaker for persistent rate limit errors:

```python
MAX_CONSECUTIVE_RATE_LIMITS = 5
consecutive_rate_limits = 0

if is_rate_limited:
    consecutive_rate_limits += 1
    if consecutive_rate_limits >= MAX_CONSECUTIVE_RATE_LIMITS:
        # Trigger circuit breaker: pause uploads
        wait_time = 300  # 5 minutes
else:
    consecutive_rate_limits = 0  # Reset counter on success
```

---

## Upload Script Configuration

### Recommended Settings

For large uploads (100,000+ records):

```python
# Rate limiting settings
BATCH_SIZE = 100                # Progress update frequency
MAX_RETRIES = 5                 # Max retry attempts per record
MIN_RETRY_DELAY = 1.0          # Min delay on retry (1 second)
MAX_RETRY_DELAY = 120.0        # Max delay on retry (2 minutes)
MIN_REQUEST_DELAY = 0.01       # Min delay between requests (10ms)
MAX_REQUEST_DELAY = 2.0        # Max delay between requests (2 seconds)

# Circuit breaker
MAX_CONSECUTIVE_RATE_LIMITS = 5
CIRCUIT_BREAKER_COOLDOWN = 300  # 5 minutes
```

### Adaptive Upload Speed

The script should automatically adjust speed:

```python
# High quota (>80%): ~100 records/sec (0.01s delay)
# Medium quota (50-80%): ~20 records/sec (0.05s delay)
# Low quota (20-50%): ~5 records/sec (0.2s delay)
# Very low quota (<20%): ~1-2 records/sec (0.5-1.0s delay)
```

---

## Error Handling

### 1. Transient Errors (Retry)

- `429 Too Many Requests` - Rate limit exceeded
- `503 Service Unavailable` - Temporary server issue
- `504 Gateway Timeout` - Request timeout
- Network errors (connection timeout, DNS failure)

**Action:** Retry with exponential backoff

### 2. Permanent Errors (Don't Retry)

- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Invalid API token
- `403 Forbidden` - Permission denied
- `404 Not Found` - Endpoint doesn't exist
- `422 Unprocessable Entity` - Validation error

**Action:** Log error, skip record, continue

### 3. Rate Limit Specific Handling

```python
if http_code == 429:
    # Extract retry-after from headers
    retry_after = response.headers.get('Retry-After', 60)
    
    # Also check response body
    error_data = response.json()
    retry_after = error_data.get('retry_after', retry_after)
    
    # Wait the specified time
    time.sleep(int(retry_after))
    
    # Retry request
```

---

## Monitoring & Logging

### Track These Metrics

1. **Rate Limit Hits:** Count of 429 errors
2. **Retry Attempts:** Total retries across all requests
3. **Current Quota:** Real-time quota percentage
4. **Upload Rate:** Records per second
5. **ETA:** Estimated time to completion

### Example Progress Output

```
--- Progress: 10,000/154,065 (6.5%) ---
    Success: 9,987 | Failed: 13 | Skipped: 0
    Rate: 8.2/sec | ETA: 4.8 hours
    API Quota: 520/600 (86.7% remaining)
    Rate Limits: 2 hits | Retries: 7
    Current Delay: 0.01s
```

---

## Optimization Tips

### 1. Off-Peak Hours

Upload during off-peak hours for better quota availability:
- Weekends
- Late night (timezone dependent)
- Early morning

### 2. Parallel Uploads (Advanced)

For very large datasets, consider:
- Multiple API tokens (if available)
- Split data into chunks
- Upload in parallel with separate processes

**Warning:** Be careful not to exceed total account limits

### 3. Resume Capability

Always implement resume functionality:

```bash
# Start upload
python upload_script.py

# If interrupted, resume from record 5000
python upload_script.py 5000
```

### 4. Pre-Validation

Validate all records before upload to minimize API calls:
- Date format validation
- Enum value validation
- Numeric field validation
- Required field validation

---

## Troubleshooting

### "Rate limit persists despite waiting"

**Possible causes:**
1. Multiple upload processes running
2. Other API usage in same account
3. Shared rate limit across team

**Solution:**
- Check for other running uploads
- Increase `MAX_RETRY_DELAY` to 120-300 seconds
- Implement longer circuit breaker cooldown

### "Upload too slow"

**Possible causes:**
1. Conservative delay settings
2. Low API quota
3. Network latency

**Solution:**
- Reduce `MIN_REQUEST_DELAY` (careful!)
- Verify rate limit headers are being read
- Check network connection
- Upload during off-peak hours

### "Too many failures"

**Possible causes:**
1. Data validation issues
2. API token expired
3. Schema mismatch

**Solution:**
- Review failed records CSV
- Validate API token
- Verify schema matches data
- Check error messages carefully

---

## Example Implementation

See `upload_radico_procurement.py` for a complete implementation with:

- ✅ Dynamic delay adjustment
- ✅ Exponential backoff
- ✅ Retry-After support
- ✅ Circuit breaker pattern
- ✅ Real-time quota monitoring
- ✅ Comprehensive error handling
- ✅ Resume capability
- ✅ Progress tracking
- ✅ Failed records logging

---

## API Limits Summary

| Limit Type | Standard Tier |
|-----------|---------------|
| **Requests per minute** | 600 |
| **Requests per hour** | 10,000 |
| **Burst allowance** | 100 |
| **Max retries recommended** | 5 |
| **Max retry delay** | 60-120s |
| **Recommended base delay** | 0.01-0.05s |

---

## Additional Resources

- DevRev API Documentation: https://developer.devrev.ai/
- Best practices for handling rate limits
- Error code reference guide
- API status page for service incidents

---

**Last Updated:** 2026-05-23  
**Version:** 1.0
