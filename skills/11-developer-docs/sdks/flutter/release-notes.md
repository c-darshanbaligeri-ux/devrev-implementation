# Release notes

Source: <https://developer.devrev.ai/sdks/flutter/release-notes>
Scraped: 2026-11-03

All notable changes, improvements, and fixes for the DevRev SDK for Flutter are documented here. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.3.11

### Changed

* \[iOS] Improved session replay performance.

### Fixed

* \[Android] Fixed an issue where dialogs were not captured correctly in session replays.
* \[iOS] Fixed an intermittent "session not found" error when uploading a killed or terminated session.

## 2.3.10

### Added

* \[Android] Added support for session recording on Android 17.
* \[iOS] Session replay masks the on-screen keyboard area to avoid capturing sensitive input.

### Fixed

* \[Android] A user whose account was deleted on the backend is re-identified automatically instead of failing subsequent requests.
* \[iOS] Fixed a crash related to flushing of log entries.

## 2.3.9

### Added

* Added support for UI-based rate limiting.

### Fixed

* \[Android] Fixed a race condition when starting session recording that could cause unstable recording startup.

## 2.3.8

### Added

* \[Android] Added correlation headers to network requests for improved traceability.

### Changed

* \[iOS] Improved logs traceability.

### Fixed

* \[Android] Fixed masking when multiple Flutter engines or channels are active, so the foreground channel is used for mask reads.

## 2.3.7

### Added

* Added an SDK version filter for session replay, allowing replay to be enabled or disabled for specific SDK versions from the dashboard.

### Fixed

* \[Android] Fixed masks on the base page being dropped while a dialog or modal bottom sheet was open.
* \[Android] Fixed a main-thread deadlock when resolving external masks with Flutter.
* \[Android] Fixed a crash in the screenshot capturer caused by a recycled bitmap on cancel.
* \[Android] Fixed an issue with mask coordinate clipping.
* \[iOS] Fixed a race condition that could affect network event counts during concurrent requests.

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

### Added

* Optional prefilled message support for the support chat input field.

### Changed

* Improved privacy (masking) stability.
* \[iOS] Improved Flutter lifecycle handling to prevent crashes when Flutter is unavailable during session replays in a hybrid Flutter + native setup.

### Fixed

* Fixed session recordings associating events with the wrong DevRev workspace.
* \[iOS] Fixed crashes from thread-unsafe access.

## 2.3.4

### Fixed

* \[Android] Fixed the fractional masking delay during navigation.

## 2.3.3

### Fixed

* Fixed an issue where Ktor classes were getting stripped due to ProGuard rules.
* Fixed an issue related to blank user identifier in identification calls.
* Added a fix for masking stability during scrolls.
* Fixed an issue related to garbage characters in custom events.
* \[iOS] Fixed an issue with empty crash types.
* \[iOS] Fixed an issue with push notifications not being delivered in sandbox environments.

## 2.3.2

### Changed

* \[iOS] Reduced memory and CPU usage during paused screen recording.

### Fixed

* \[iOS] Fixed crashes and memory leaks during screen recording.
* \[Android] Fixed VerifyError crash.

## 2.3.1

### Changed

* Broader stability improvements (recording, sessions, masking, memory).
* \[iOS] Screen recording uses less memory and stays idle when paused.

### Fixed

* \[Android] Fixed fractional masking delay during rapid screen transitions and fast scrolling.
* \[Android] Corrected engagement time for sessions still uploading.
* Improved rare Android long startup time and configuration issues.

## 2.3.0

### Added

* Feature configuration for screen capture, auto-start recording, Plug chat theme, and remote config (fresh vs cached/lazy fetch).

### Changed

* Improved the frame-capture-disabled session replay experience.
* \[iOS] Session upload enforces a minimum visit duration before uploading.

### Fixed

* Fixed a few memory leaks and crashes.
* \[Android] Fixed device-specific distorted session replays.

## 2.2.5

### Added

* \[Android] Added masking support for multiple Flutter method channels.
* \[iOS] Added CocoaPods support.

## 2.2.4

### Changed

* Lowered the minimum supported Dart SDK to `3.5.0` across the plugin to match current Flutter stable toolchains.
* Improved session replay stability and performance.
* Reduced log noise.
* \[Android] Removed redundant dependencies for reduced SDK size and enhanced security.

### Fixed

* Fixed session data not found.

## 2.2.3

### Added

* Added a capture error API so apps can report runtime errors through the SDK.

### Changed

* Improved rage tap detection to avoid misclassifying double taps as rage taps.
* \[Android] Optimized session recording and network request handling to reduce overhead during active sessions.

### Fixed

* \[iOS] Corrected timer response rounding to return accurate durations.
* \[Android] Fixed incorrect engagement time calculation in crash scenarios.
* \[Android] Fixed ANRs occurring during SDK initialization.

## 2.2.2

### Added

* \[Android] Support for session capturing on Android 16 devices.
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
* Added a `sendException` method to track handled exceptions.

### Changed

* Improved performance and modularity by decoupling the screen recording functionality from the main tracking flow.

### Fixed

* \[Android] Resolved potential out of memory crashes.
* \[iOS] Corrected incorrect or missing device model names on certain iPhone versions.
* \[iOS] Fixed visual distortion issues when zooming inside a WebView.

## 2.2.0

> 📝 **Note**: This release aligns with version `2.2.0` of all supported DevRev SDK platforms to maintain consistency across the ecosystem.

### Added

* Identification of users as anonymous, unverified, or verified.
* In-app support chat for users, including push notification support and the ability to create new conversations.
* Controlling modal behavior when links are opened from within the chat.
* Tracking custom user events and actions with rich event properties.
* Gaining session-level behavior with features like timers and screen tracking.
