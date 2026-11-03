# Release notes

Source: <https://developer.devrev.ai/sdks/ios/release-notes>
Scraped: 2026-11-03

All notable changes, improvements, and fixes for the DevRev SDK for iOS. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.0.8

### Changed

* Improved session replay performance.

### Fixed

* Fixed an intermittent “session not found” error when uploading a killed or terminated session.

## 3.0.7

### Added

* Added support for masking all text option in session replays.

### Changed

* Improved SwiftUI session replay performance.

### Fixed

* Fixed a crash related to flushing of log entries.

## 3.0.6

### Added

* Session Replay now masks the on-screen keyboard area to avoid capturing sensitive input.

## 3.0.5

### Fixed

* Fixed a session replay crash during high-frequency capture.

## 3.0.4

### Added

* Optional token refresh handler for verified user identification to renew expired session tokens without re-identifying the user.

### Changed

* Session replay recording now respects the server-provided admission gate, skipping capture when the session is rate-limited.

### Fixed

* Fixed a use-after-free crash when a network-intercepted `URLSession` completion handler fired.

## 3.0.3

### Changed

* Refined network monitoring to track the SDK's essential API calls while excluding the SDK's own internal API traffic.
* Improved logs traceability.

## 3.0.2

### Changed

* Computer+ Observe now responds to runtime `FeatureConfiguration` updates, applying changes immediately without requiring a restart.

### Removed

* Removed an unused internal analytics network request. Custom events sent via `trackEvent(name:properties:)` continue to be captured as part of session replay.

## 3.0.1

### Added

* Remote SDK version-based control for session replay recording, without requiring app updates.

## 3.0.0

### Added

* Computer+ Observe provides automatic, privacy-aware capture of API requests with network events attached to session replays, configurable via `FeatureConfiguration.networkObservability`.

### Changed

* Improved diagnostics for the key SDK.

### Fixed

* Fixed a race condition that could affect network event counts during concurrent requests.

## 2.3.9

### Added

* `ConversationPageOptions` on `SupportWidgetTheme` to customize the support chat conversation page header and subheader text.

### Changed

* Reduced memory allocation during session replay uploads with staged per-session processing and early validation guards.

### Fixed

* Fixed UI lag during native menu dropdown animations by skipping session replay capture while the menu platter is animating.

## 2.3.8

### Fixed

* Fixed unknown network type in session events by correctly identifying the cellular data service, radio generation, and Wi-Fi/cellular transitions.
* Fixed session replay snapshot quality and touch coordinate rendering in landscape orientation.
* Fixed support chat conversation being cleared when a transient modal is dismissed.
* Fixed a trait collection initialization crash.

## 2.3.7

### Added

* Optional prefilled message support for the support chat input field.
* Feature configuration flag `maskAllTextByDefault` to automatically mask all visible text.

### Fixed

* Fixed crashes from thread-unsafe access.
* Fixed pause and resume user interaction tracking APIs.
* Fixed session recordings associating events with the wrong DevRev workspace.

## 2.3.6

### Fixed

* Fixed a missing crash type not appearing on the dashboard by exposing the crash type field in the iOS crash event.
* Fixed push notifications not being delivered in sandbox environments due to incorrect APNs push type.

## 2.3.5

### Changed

* Reduced snapshot size and screen capture cost.

## 2.3.4

### Fixed

* Fixed UI lag when multiple simultaneous gestures were active during session touch tracking.

## 2.3.3

### Fixed

* Fixed screen tracking performance issues with embedded view controllers.

## 2.3.2

### Changed

* Freed up memory and reduced CPU usage to zero on pause screen recording.

### Fixed

* Fixed a crash for exceeding the nested views limit while screen recording.
* Handled WebView masking edge cases.
* Fixed a few memory leaks.

## 2.3.1

### Added

* Optional Plug article search filters via `FeatureConfiguration.supportWidgetArticleSearchFilters` (widget search and command palette), with typed filter operators and operand value types.
* Feature configuration flag to enable real-time AI agent response streaming in Plug support chat.

### Fixed

* Resolved performance lag during paused recording by ensuring complete termination of all background processes.
* Avoided a potential runtime crash during decoding.
* Fixed a crash when a view was created before the trait collection was available.

## 2.3.0

### Added

* Feature configuration for screen capture, auto-start recording, Plug chat theme, and remote config (fresh vs cached/lazy fetch).

### Changed

* Session upload now enforces a minimum visit duration before uploading.

### Fixed

* Fixed frame capture flag injection so the flag is set at the correct place.
* Fixed native logs ingestion.

## 2.2.10

### Added

* Implemented caching and lazy fetch for SDK configuration to improve startup performance.
* Improved sample apps to showcase error capture APIs and camera screen recordings.

### Fixed

* Fixed SwiftUI screen name injection in session events.

## 2.2.9

### Fixed

* Fixed crash session missing for the frame capture feature.

## 2.2.8

### Added

* Enabled internal native logging to improve diagnostics and troubleshooting.

### Changed

* Modernized legacy components and aligned for better performance.

### Removed

* Removed deprecated and non-public iOS APIs.

## 2.2.7

### Added

* Added feature configuration options to enable or disable screen capture, auto-start recording, and configuring Plug chat theme locally.

### Changed

* Improved session replay performance.
* Reduced log noise.

## 2.2.6

### Added

* Introduced a capture error API so apps can report runtime errors through the SDK.
* Improved rage tap detection to avoid misclassifying double taps as rage taps.

### Fixed

* Corrected timer response rounding to return accurate durations.

## 2.2.5

### Added

* Added automatic restoration of sessions lost when the app is killed.

### Changed

* Improved crash log parsing and formatting for clearer diagnostics.
* Refined the session upload pipeline for improved reliability.

## 2.2.4

### Added

* Added support to track user interactions within WebView components, improving analytics and engagement insights.

### Changed

* Simplified the identification flow by deprecating redundant anonymous API usage.

### Fixed

* Fixed issues in the logout process to ensure complete session termination and improved reliability.

## 2.2.3

### Added

* Added the ability to pause and resume user interaction event tracking, offering more security on confidential screens.

### Changed

* Improved performance and modularity by decoupling the screen recording functionality from the main tracking flow.

### Fixed

* Corrected incorrect or missing device model names on certain iPhone versions.
* Fixed visual distortion issues when zooming inside a WebView.

## 2.2.2

### Changed

* Improved the infrastructure for custom masking.

## 2.2.1

### Added

* Extended the sample app with masking of WebViews, table views, and lists.

### Changed

* Improved the API reference and integration guide.

### Fixed

* Fixed the broken Objective-C signature for the `identifyVerifiedUser:sessionToken:` method.
* Fixed user properties missing in session recording.

## 2.2.0

### Added

* Introduced custom masking controls for improved privacy management.

### Fixed

* Fixed an issue where manual unmasking did not work during session capture.
* Resolved a session recording issue affecting SwiftUI views.

## 2.1.0

### Added

* Introduced crash reporting integrated with session recordings.
* Improved support widget navigation.

### Fixed

* Fixed an issue with timer tracking to ensure correct session properties are recorded.

## 2.0.2

### Fixed

* Included the actual changes intended for version 2.0.1 related to improved masking support for WebViews and plugins.

## 2.0.1

### Fixed

* Improved masking support for WebViews and plugins.

## 2.0.0

### Changed

* Improved the communication with the DevRev backend.
* Improved the encryption techniques used throughout the SDK.

### Removed

* The `DevRevDelegate` protocol has been removed.

## 1.1.7

### Fixed

* Fixed an issue with sandbox detection.

### Deprecated

* The `DevRevDelegate` protocol is deprecated and is removed in version 2.0.0.

## 1.1.6

### Fixed

* Fixed an issue where the DevRev SDK would go into an unrecoverable state.

## 1.1.5

### Changed

* Added a flag to enforce the preferred theme for the DevRev UI, overriding the system theme when enabled.
* Added support for sandbox notification testing in debug mode.

## 1.1.4

### Changed

* Improved the handling of custom fields in user, account, and organization traits.

## 1.1.3

### Added

* Created a brand-new sample app showcasing the DevRev SDK's features.
* Added support for CSS masking classes using the `devrev-mask` and `devrev-unmask` classes.

### Changed

* Improved the handling of automatic session recording.

## 1.1.2

### Changed

* Enhanced the Computer+ Observe feature to work better across different environments.

### Removed

* Removed support for automatic processing of DevRev push notifications. For more information, refer to the integration guide (README.md).

## 1.1.1

### Fixed

* Improved the stability of the on-demand sessions feature.

## 1.1.0

### Added

* Introduced a logout mechanism that clears the user's credentials, unregisters the device from receiving push notifications, and stops the session recording.
* Added a boolean flag to check if the SDK has been configured.
* Added a boolean flag to check if the user has been identified.
* Added a boolean flag to check if the session is being recorded.
* Added a boolean flag to check if monitoring is enabled.
* Added a boolean flag to check if on-demand sessions are enabled.

## 1.0.3

### Fixed

* Fixed an issue where an already identified user could not be switched with a new user of the same type.

### Deprecated

* Support for iOS versions below 15 is removed in this version.

## 1.0.2

### Fixed

* Fixed an issue with verified user identification.

## 1.0.1

### Changed

* Improved the user identification mechanism.

## 1.0.0

### Added

* The Computer+ Observe feature monitors the health of your application and its components.
* Added support for Push Notifications for the Plug support chat.
* Added support for on-demand (offline) sessions.
* Added support to create new conversations in the Plug support chat.
* Added support for in-app link handling.
