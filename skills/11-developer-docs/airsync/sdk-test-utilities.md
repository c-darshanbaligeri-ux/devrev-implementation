# SDK test utilities

Source: <https://developer.devrev.ai/airsync/sdk-test-utilities>
Scraped: 2026-11-03

## Loading and test support

`LoadingAdapter.loadItemTypes` and `loadAttachments` drive reverse sync; their callbacks and reports are specified in [data loading](load-data.md) and [attachment loading](load-attachments.md). `Mappers` and its exported parameter/result types provide sync identity operations.

Public test utilities include `createMockEvent`, `createTestExtractionAdapter`, `createTestLoadingAdapter`, `MockServer` and their parameter types. Test adapters support isolated worker logic tests. Fixture execution may still call a real external API; see [local development](local-development.md).

The complete exported type list and implementation are available in the public [SDK entry point](https://github.com/devrev/airsync-sdk/blob/main/src/index.ts). Verify new code against the declarations of the installed stable release, then test [runtime continuation](runtime.md) and every capability it implements.

Related: [SDK entry points](sdk-reference.md).
