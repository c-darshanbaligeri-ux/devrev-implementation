# Release notes

Source: <https://developer.devrev.ai/sdks/react-native/release-notes>
Scraped: 2026-11-03

All notable changes, improvements, and fixes for the DevRev SDK for React Native and Expo are documented here. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## \[2.3.12]

### Fixed

* \[Android] Fixed an issue where dialogs were not captured correctly in session replays.
* \[iOS] Fixed lag during session recording when screens are within navigation flows.
* \[iOS] Fixed an intermittent "session not found" error when uploading a killed or terminated session.

## \[2.3.11]

### Added

* \[Android] - Added support for session recording on Android 17
* \[iOS] - Session Replay now masks the on-screen keyboard area to avoid capturing sensitive input.

### Fixed

* \[Android] A user whose account was deleted on the backend is now re-identified automatically instead of failing subsequent requests.
* \[iOS] Fixed a crash related to flushing of log entries.

## 2.3.10

### Added

* Added support for UI-based rate limiting.

### Fixed

* \[Android] Fixed a race condition when starting session recording that could cause unstable recording startup.

## 2.3.9

### Changed

* \[Android] Reduced startup jank and ANRs during session recording.
* Improved logs traceability.

## 2.3.8

### Added

* Added an SDK version filter for session replay, allowing replay to be enabled or disabled for specific SDK versions from the dashboard.

### Fixed

* \[Android] Fixed masks on the base page being dropped while a dialog or modal bottom sheet was open.
* \[Android] Fixed a main-thread deadlock when resolving external masks.
* \[Android] Fixed a crash in the screenshot capturer caused by a recycled bitmap on cancel.
* \[Android] Fixed an issue with mask coordinate clipping.
* \[iOS] Fixed a race condition that could affect network event counts during concurrent requests.

## 2.3.7

### Added

* Added agent response streaming, article search filters, and conversation page header branding to the feature configuration.
* Added prefilled message support when creating support conversations.

### Fixed

* \[Android] Fixed a crash related to null pointer exceptions on activities.

## 2.3.6

### Changed

* \[iOS] Improved memory usage during offline session replay uploads.
* Enhanced overall performance during screen navigations.

### Fixed

* \[Android] Fixed an issue related to rapid navigations.
* \[Android] Fixed an ANR related to animated dialog captures.
* \[Android] Fixed an issue related to keyboard scrolls on WebViews.
* \[Android] Fixed an issue related to dispatch window callback mutations.

## 2.3.5

### Fixed

* \[iOS] Fixed unknown network type in session events by correctly identifying the cellular data service, radio generation, and Wi-Fi/cellular transitions.
* \[iOS] Fixed session replay snapshot quality and touch coordinate rendering in landscape orientation.
* \[iOS] Fixed support chat conversation being cleared when a transient modal is dismissed.
* \[iOS] Fixed a trait collection initialization crash.

## 2.3.4

### Fixed

* Fixed session recordings associating events with the wrong DevRev workspace.
* \[iOS] Fixed crashes from thread-unsafe access.
* \[Android] Fixed masking issues on rapid scrolls.
* \[Android] Fixed an issue with missing crash types.

## 2.3.3

### Fixed

* \[Android] Implemented WebView masking for Canvas Technology.
* \[Android] Fixed an issue with WebView masking.
* \[Android] Fixed an issue with masking displacement on fast scrolling.

## 2.3.2

### Fixed

* Fixed an issue where Ktor classes were getting stripped due to ProGuard rules.
* Fixed an issue related to blank user identifier in identification calls.
* Added a fix for masking stability during scrolls.
* Fixed an issue related to garbage characters in custom events.
* \[iOS] Fixed an issue with empty crash types.
* \[iOS] Fixed an issue with push notifications not being delivered in sandbox environments.

## 2.3.1

### Fixed

* Improved session recording stability and reduced resource usage on both platforms.
* Fixed multiple crashes and ANRs during session recording and app termination.
* \[Android] Fixed incorrect session engagement time calculations.

## 2.3.0

### Added

* Feature configuration for screen capture, auto-start recording, Plug chat theme, and remote config (fresh vs cached: lazy fetch).
* Support for React Native versions >= 0.79.

### Changed

* Improved the frame-capture-disabled session replay experience.
* \[iOS] Session upload now enforces a minimum visit duration before uploading.

### Fixed

* Fixed a few memory leaks and crashes.

## 2.2.6

### Fixed

* \[Android] Fixed an issue with session recordings on QR scan screens.

## 2.2.5

### Changed

* Modernized legacy components and aligned for better performance.

### Removed

* Removed deprecated and non-public iOS APIs.

## 2.2.4

### Changed

* Improved session replay stability and performance.
* Reduced log noise.
* \[Android] Removed redundant dependencies for reduced SDK size and enhanced security.

### Fixed

* Fixed session data not found.

## 2.2.3

### Added

* \[Android] Added a capture error API to allow apps to report runtime errors through the SDK.

### Changed

* \[Android] Refined rage tap detection logic to avoid misclassifying double taps as rage taps.
* \[Android] Optimized session recording and network request handling to reduce overhead during active sessions.

### Fixed

* Fixed timer response rounding to return accurate duration values.
* Fixed incorrect engagement time calculation in crash scenarios.
* \[Android] Fixed ANRs occurring during SDK initialization.

## 2.2.2

### Added

* Support for session capturing on Android 16 devices.
* Support for tracking hybrid platforms and their versions.
* \[iOS] Added automatic restoration of sessions lost when the app is killed.

### Changed

* Improved masking behavior on `RecyclerView` scrolls.
* Improved session upload reliability and stability.
* Optimized network bandwidth usage.
* \[iOS] Improved crash log parsing and formatting for clearer diagnostics.

### Fixed

* Fixed an issue in the logout flow.

## 2.2.1

### Added

* Added the ability to pause and resume user interaction event tracking, offering more security on confidential screens.

### Changed

* Simplified the identification flow by removing redundant anonymous API usage.

### Fixed

* Resolved potential out of memory crashes.
* Corrected incorrect or missing device model names on certain iPhone versions.
* Fixed visual distortion issues when zooming inside a WebView.
* Fixed issues in the logout process to ensure complete session termination and improved reliability.

## 2.2.0

### Changed

* \[iOS] Improved the infrastructure for custom masking.
* Unified the screen tracking feature naming across platforms.

### Deprecated

* Deprecated the `startScreenTransition` and `endScreenTransition` functions; use the `setInScreenTransitioning` function instead.

### Fixed

* \[iOS] Fixed push notifications not opening conversations.
* \[Android] Resolved potential issues that could cause app crashes during network operations.
* \[Android] When adding session properties before initialization, they are now properly queued and executed.
* \[Android] Added extra safeguards to prevent crashes related to uninitialized properties.
* \[Android] Enhanced the stability of session-recording flows for a more reliable experience.

## 2.1.3

### Added

* Added detailed Computer+ Observe logging for SDK configuration and identification steps.

## 2.1.2

### Added

* Added a caching mechanism for identification calls.

### Fixed

* Improved the presentation of the support widget in edge-to-edge scenarios.
* Improved the Computer+ Observe and metrics.
* Fixed an issue related to long session engagement times.

## 2.1.1

### Fixed

* Fixed an issue with manual unmasking of input components.
* Fixed an issue with session uploads when the app is rapidly killed.

## 2.1.0

### Added

* Added support for the React Native new architecture.
* \[iOS] Introduced crash reporting integrated with session recordings.

### Changed

* Bumped the React Native version of the SDK to 0.79.0.
* Bumped the iOS minimum deployment target to 15.1.
* \[iOS] Improved the support widget navigation.

### Fixed

* Fixed an issue with timer tracking to ensure correct session properties are recorded.

## 2.0.0

### Changed

* Improved the communication with the DevRev backend.
* Improved the encryption techniques used throughout the SDK.

### Removed

* The `getSessionURL` function has been removed.

## 1.1.8

### Fixed

* \[iOS] Fixed an issue with sandbox detection.

### Deprecated

* \[iOS] The `DevRevDelegate` protocol is deprecated and is scheduled for removal in the next major release.

## 1.1.7

### Fixed

* \[Android] Fixed an issue where the Android bridge would throw a compiler error.

## 1.1.6

### Added

* \[iOS] Added a flag to enforce the preferred theme for the DevRev UI, overriding the system theme when enabled.

### Fixed

* \[iOS] Fixed an issue where the DevRev SDK would go into an unrecoverable state.

## 1.1.5

### Changed

* Fixed a data type mismatch issue in the `addSessionProperties` method for the iOS build.

## 1.1.4

### Changed

* Updated the `trackEvent`, `addSessionProperties`, `startTimer`, and `endTimer` functions to accept plain objects instead of a map.

### Fixed

* Fixed the crash in the `trackEvent` function due to a type casting issue.

## 1.1.3

### Changed

* Improved the handling of custom fields in user, account, and organization traits.

## 1.1.2

### Added

* Created a brand-new sample app showcasing the DevRev SDK's features.
* Added support for CSS masking classes using the `devrev-mask` and `devrev-unmask` classes.

### Changed

* Enhanced the Computer+ Observe feature to work better across different environments.
* \[iOS] Improved the handling of automatic session recording.

### Fixed

* \[Android] Fixed bugs related to on-demand sessions, providing a more stable experience.

### Removed

* \[iOS] Removed support for automatic processing of DevRev push notifications.

## 1.1.1

### Added

* Added support for on-demand (offline) sessions.
* \[Android] Added screen transition tracking.

## 1.1.0

### Added

* Introduced a logout mechanism that clears the user's credentials, unregisters the device from receiving push notifications, and stops the session recording.

## 1.0.3

### Fixed

* \[iOS] Fixed an issue where a user could not be re-identified with the same identification type.
* \[Android] Fixed a crash where the application theme was not a descendant of `Theme.AppCompat`.
* \[Android] Fixed an issue where the physical back button was not being handled properly.
* \[Android] Fixed an issue where inputs were getting reset on configuration changes.

## 1.0.2

### Added

* Added support for verified user identification.
* Added support for on-demand (offline) sessions.

## 1.0.0

### Added

* Initial release of the DevRev SDK for React Native.
