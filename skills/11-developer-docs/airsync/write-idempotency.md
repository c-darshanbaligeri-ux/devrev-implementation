# Retry external writes safely

Source: <https://developer.devrev.ai/airsync/write-idempotency>
Scraped: 2026-11-03

## Idempotency across retries

SDK file positions do not make external writes and DevRev mapper persistence atomic. A timeout, lost external response or mapper failure can cause a write to be replayed. For creates, use the external API's idempotency key or a stable identifier that can be looked up before creating again. For updates, prefer operations that converge to the requested state over additive operations that repeat on replay.

Keep idempotency keys stable across continuation; a fresh invocation or run-specific random value cannot identify a replayed write. Include the relevant external account and sync-unit scope where IDs are not globally unique.

Related: [Reverse-sync ordering](reverse-sync-ordering.md).

Continue with testing: [Run connector events locally](local-development.md).
