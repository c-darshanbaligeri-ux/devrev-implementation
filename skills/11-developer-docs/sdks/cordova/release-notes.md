# Release notes

Source: <https://developer.devrev.ai/sdks/cordova/release-notes>
Scraped: 2026-11-03

Notable changes, improvements, and fixes for the DevRev SDK for Cordova. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.3.4

### Changed

* \[iOS] Improved session replay performance.

### Fixed

* \[Android] Fixed an issue where dialogs were not captured correctly in session replays.
* \[iOS] Fixed an intermittent "session not found" error when uploading a killed or terminated session.

## 2.3.3

### Added

* \[Android] Added support for session recording on Android 17.
* \[iOS] Session replay masks the on-screen keyboard area to avoid capturing sensitive input.

### Fixed

* \[Android] A user whose account was deleted on the backend is re-identified automatically instead of failing subsequent requests.
* \[iOS] Fixed a crash related to flushing of log entries.

## 2.3.2

### Added

* Optional prefilled message support when creating support conversations.
* SDK version filter for session replay from the dashboard.
* Added support for UI-based rate limiting.

### Changed

* Improved session recording stability and reduced startup jank.

### Fixed

* Fixed crashes and ANRs related to session recording and WebView masking.
* \[iOS] Fixed support chat clearing on transient modal dismiss and landscape replay issues.

## 2.3.1

### Fixed

* Fixed session recordings associating events with the wrong DevRev workspace.
* \[iOS] Fixed crashes from thread-unsafe access.
* \[Android] Fixed masking issues on rapid scrolls.
* \[Android] Fixed an issue with missing crash types.

## 2.3.0

### Changed

* Reduced snapshot size and screen capture cost.
* Optimized masking performance for dynamic WebViews.

### Fixed

* Fixed multiple memory leaks and reduced CPU usage during paused recording.
* Fixed crashes and ANRs related to the session recording lifecycle.
* Improved WebView masking stability.
* Fixed incorrect session engagement time calculation.

## 2.2.1

### Changed

* Lowered the minimum supported Dart SDK to `3.5.0` across the plugin to match current Flutter stable toolchains.
* Improved session replay stability and performance.
* Reduced log noise.
* \[Android] Removed redundant dependencies for reduced SDK size and enhanced security.

### Fixed

* Fixed session data not found.

## 2.2.0

### Added

* \[Android] Support for session capturing on Android 16 devices.
* Support for tracking hybrid platforms and their versions.
* \[iOS] Added automatic restoration of sessions lost when the app is killed.
* Introduced a capture error API so apps can report runtime errors through the SDK.

### Changed

* Improved rage tap detection to avoid misclassifying double taps as rage taps.
* Improved performance and modularity by decoupling the screen recording functionality from the main tracking flow.
* \[Android] Optimized session recording and network request handling to reduce overhead during active sessions.

### Fixed

* Fixed an issue in the logout flow.
* \[iOS] Corrected timer response rounding to return accurate durations.
* \[Android] Fixed incorrect engagement time calculation in crash scenarios.
* \[Android] Fixed ANRs occurring during SDK initialization.

## 2.1.1

### Fixed

* Fixed an issue with manual unmasking of input components.
* Fixed an issue with session uploads when the app is rapidly killed.

## 2.1.0

### Added

* \[iOS] Introduced crash reporting integrated with session recordings.

### Changed

* Improved the support widget navigation.

### Fixed

* Fixed an issue with timer tracking to ensure correct session properties are recorded.

## 2.0.0

### Changed

* Improved the communication with the DevRev backend.
* Improved the encryption techniques used throughout the SDK.

### Removed

* The `getSessionURL` function has been removed.

## 1.0.0

### Added

* Introduced the Session Analytics feature, which allows you to monitor the health of your application and its components.
* Added support for Push Notifications for the Plug support chat.
* Added support to create new conversations in the Plug support chat.
