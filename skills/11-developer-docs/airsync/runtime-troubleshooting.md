# Troubleshoot worker execution

Source: <https://developer.devrev.ai/airsync/runtime-troubleshooting>
Scraped: 2026-11-03

Use these checks when the connector fails during runtime.

## Worker emits twice or never finishes

Workers return a `TaskResult`; the SDK emits the platform callback. Return nested helper results instead of emitting manually. Match `progress`, `delay`, `success` and `error` to the intended continuation behavior. A missing result is a contract error even if TypeScript was bypassed.

## SDK upgrade compiles but behavior changed

Use the migration guide shipped with the installed v2 package. Check mapper `null` handling, result statuses, delay units, connector cursor migration and local runners. Compilation cannot prove state compatibility. Run [fixture and live validation](validation.md) on an existing import as well as a fresh one.

Related: [troubleshooting index](faq.md).
