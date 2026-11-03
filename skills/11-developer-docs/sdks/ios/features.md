# Features

Source: <https://developer.devrev.ai/sdks/ios/features>
Scraped: 2026-11-03

## Identification

To access certain features of the DevRev SDK, user identification is required.

The identification function should be placed appropriately in your app after the user logs in. If you have the user information available at app launch, call the function after your `DevRev.configure` call has completed.

> **Tip:**
>   If you haven't previously identified the user, the DevRev SDK will automatically create an anonymous user for you immediately after the SDK is configured.

> **Tip:**
>   The `Identity` structure allows for custom fields in the user, organization, and account traits. These fields must be configured through the DevRev app before they can be utilized. For more information, refer to [Object customization](https://devrev.ai/docs/product/object-customization).

You can select from the following methods to identify users within your application:

### Identify an unverified user

The unverified identification method identifies users with a unique identifier, but it does not verify their identity with the DevRev backend.

```swift
DevRev.identifyUnverifiedUser(_:)
```

The function accepts the `DevRev.Identity` structure, with the user identifier (`userID`) as the only required property, all other properties are optional.

### Identify a verified user

The verified identification method is used to identify users with an identifier unique to your system within the DevRev platform. The verification is done through a token exchange process between you and the DevRev backend.

The steps to identify a verified user are as follows:

1. Generate an AAT for your system (preferably through your backend).
2. Exchange your AAT for a session token for each user of your system.
3. Pass the user identifier and the exchanged session token to the `DevRev.identifyVerifiedUser(_:sessionToken:)` method.

  For security reasons, it is **strongly recommended** that the token exchange is executed on your backend to prevent exposing your application access token (AAT).

#### Generate an AAT

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Open the **PLuG Tokens** page.
3. Under the **Application access tokens** panel, click **New token** and copy the token that's displayed.

  Ensure that you copy the generated application access token, as you cannot view it again.

#### Exchange your AAT for a session token

To proceed with identifying the user, you need to exchange your AAT for a session token. This step helps you identify a user of your own system within the DevRev platform.

Here is a simple example of an API request to the DevRev backend to exchange your AAT for a session token:

  Make sure that you replace the `` and `<YOUR_USER_ID>` with the actual values.

```bash
curl \
--location 'https://api.devrev.ai/auth-tokens.create' \
--header 'accept: application/json, text/plain, */*' \
--header 'content-type: application/json' \
--header 'authorization: <AAT>' \
--data '{
  "rev_info": {
    "user_ref": "<YOUR_USER_ID>"
  }
}'
```

The response of the API call contains a session token that you can use with the verified identification method in your app.

  As a good practice, **your** app should retrieve the exchanged session token from **your** backend at app launch or any relevant app lifecycle event.

#### Identify the verified user

Pass the user identifier and the exchanged session token to the verified identification method:

```swift
DevRev.identifyVerifiedUser(_:sessionToken:)
```

Session tokens expire. To keep a verified user identified without re-identifying them, use the overload that accepts a token refresh handler. The SDK invokes the handler when the session token nears expiration and uses the returned token to continue making authenticated calls on the user's behalf. The handler returns a fresh session token using the same mechanism that produced the initial `sessionToken` (that is, exchanging your AAT on your backend):

```swift
await DevRev.identifyVerifiedUser(
    "foo@example.org",
    sessionToken: "bar-1337",
    tokenRefreshHandler: {
        // Fetch and return a fresh session token from your backend.
        try await yourBackend.fetchDevRevSessionToken()
    }
)
```

> **Tip:**
>   The handler runs off the SDK's internal queue and is bounded by a timeout, so a slow or failing refresh does not block other SDK operations. The refresh is single-flight: concurrent triggers await the same in-flight refresh and your handler is invoked at most once per refresh.

> **Note:**
>   Passing `nil` for `tokenRefreshHandler` matches `DevRev.identifyVerifiedUser(_:sessionToken:)`: an expired session token is not refreshed and authenticated calls start failing once it expires.

From Objective-C, use the completion-handler variant. Call the completion with a fresh session token, or with `nil` when a new token cannot be produced:

```objc
[DevRev identifyVerifiedUser:@"foo@example.org"
                sessionToken:@"bar-1337"
         tokenRefreshHandler:^(void (^completion)(NSString * _Nullable)) {
    // Fetch a fresh session token from your backend, then:
    completion(freshSessionToken); // or completion(nil) if none could be produced.
}];
```

### Update the user

You can update the user's information using the following method:

```swift
DevRev.updateUser(_:)
```

This function accepts the `DevRev.Identity` structure.

  The `userID` property cannot be updated.

> **Tip:**
>   The identification functions are asynchronous. Ensure you wrap them in a `Task` when calling from synchronous contexts.

Use this property to check whether the user is identified in the current session:

```swift
DevRev.isUserIdentified
```

### Logout

You can perform a logout of the current user by calling the following method:

```swift
DevRev.logout(deviceID:)
```

The user is logged out by clearing their credentials, as well as unregistering the device from receiving push notifications, and stopping the session recording.

For example:

```swift
// Identify an unverified user using their email address as the user identifier.
await DevRev.identifyUnverifiedUser(Identity(userID: "user@example.org"))

// Identify a verified user using their email address as the user identifier.
await DevRev.identifyVerifiedUser("foo@example.org", sessionToken: "bar-1337")

// Update the user's information.
await DevRev.updateUser(Identity(organizationID: "organization-1337"))

// Logout the identified user.
await DevRev.logout(deviceID: "dvc32423")
```

### Identity model

The `Identity` class is used to provide user, organization, and account information when identifying users or updating their details. This class is used primarily with the `identifyUnverifiedUser(_:)` and `updateUser(_:)` methods.

#### Properties

The `Identity` class contains the following properties:

| Property             | Type                  | Required | Description                                   |
| -------------------- | --------------------- | -------- | --------------------------------------------- |
| `userID`             | `String`              | ✅        | A unique identifier for the user              |
| `organizationID`     | `String?`             | ❌        | An identifier for the user's organization     |
| `accountID`          | `String?`             | ❌        | An identifier for the user's account          |
| `userTraits`         | `UserTraits?`         | ❌        | Additional information about the user         |
| `organizationTraits` | `OrganizationTraits?` | ❌        | Additional information about the organization |
| `accountTraits`      | `AccountTraits?`      | ❌        | Additional information about the account      |

> **Note:**
>   The custom fields properties defined as part of the user, organization, and account traits must be configured in the DevRev web app **before** they can be used.

##### User traits

The `UserTraits` class contains detailed information about the user:

> **Note:**
>   All properties in `UserTraits` are optional.

| Property          | Type             | Description                                      |
| ----------------- | ---------------- | ------------------------------------------------ |
| `displayName`     | `String?`        | The displayed name of the user                   |
| `email`           | `String?`        | The user's email address                         |
| `fullName`        | `String?`        | The user's full name                             |
| `userDescription` | `String?`        | A description of the user                        |
| `phoneNumbers`    | `[String]?`      | Array of the user's phone numbers                |
| `customFields`    | `[String: Any]?` | Dictionary of custom fields configured in DevRev |

##### Organization traits

The `OrganizationTraits` class contains detailed information about the organization:

> **Note:**
>   All properties in `OrganizationTraits` are optional.

| Property                  | Type             | Description                                      |
| ------------------------- | ---------------- | ------------------------------------------------ |
| `displayName`             | `String?`        | The displayed name of the organization           |
| `domain`                  | `String?`        | The organization's domain                        |
| `organizationDescription` | `String?`        | A description of the organization                |
| `phoneNumbers`            | `[String]?`      | Array of the organization's phone numbers        |
| `tier`                    | `String?`        | The organization's tier or plan level            |
| `customFields`            | `[String: Any]?` | Dictionary of custom fields configured in DevRev |

##### Account traits

The `AccountTraits` class contains detailed information about the account:

> **Note:**
>   All properties in `AccountTraits` are optional.

| Property             | Type             | Description                                      |
| -------------------- | ---------------- | ------------------------------------------------ |
| `displayName`        | `String?`        | The displayed name of the account                |
| `domains`            | `[String]?`      | Array of domains associated with the account     |
| `accountDescription` | `String?`        | A description of the account                     |
| `phoneNumbers`       | `[String]?`      | Array of the account's phone numbers             |
| `websites`           | `[String]?`      | Array of websites associated with the account    |
| `tier`               | `String?`        | The account's tier or plan level                 |
| `customFields`       | `[String: Any]?` | Dictionary of custom fields configured in DevRev |

## PLuG support chat

### UIKit

The support chat feature can be shown as a modal screen from a specific view controller or the top-most one, or can be pushed onto a navigation stack. 

To show the support chat screen in your app, you can use the following overloaded method:

```swift
DevRev.showSupport(from:isAnimated:)
```

* When a `UIViewController` is passed as the `from` parameter, the screen is shown modally.

* When a `UINavigationController` is passed as the `from` parameter, the screen is pushed onto the navigation stack.

If you want to display the support chat screen from the top-most view controller, use the following method:

```swift
DevRev.showSupport(isAnimated:)
```

For example:

```swift
// Push the support chat screen to a navigation stack.
await DevRev.showSupport(from: mainNavigationController)

// Show the support chat screen modally from a specific view controller.
await DevRev.showSupport(from: settingsViewController)

// Show the support chat screen from the top-most view controller, without an animation.
await DevRev.showSupport(isAnimated: false)
```

### SwiftUI

To display the support chat screen in a SwiftUI app, you can use the following view:

```swift
DevRev.supportView
```

### Create a new support conversation

You can initiate a new support conversation directly from your app. This method displays the support chat screen and simultaneously creates a new conversation.

```swift
DevRev.createSupportConversation(isAnimated:prefillMessage:)
```

You can optionally pass a plain-text message to prefill the conversation input field:

```swift
// Create a new support conversation with animation and a prefilled message.
await DevRev.createSupportConversation(isAnimated: true, prefillMessage: "I need help with billing for order #12345")

// Create a new support conversation with animation and without a prefilled message.
await DevRev.createSupportConversation(isAnimated: true)
```

### Handle new conversation closure

You can receive a callback when a user creates a new conversation by setting the following closure:

```swift
DevRev.conversationCreatedCompletion
```

This allows your app to access the ID of the newly created conversation.

For example:

```swift
DevRev.conversationCreatedCompletion = { conversationID in
	print("A new conversation has been created: \(conversationID).")
}
```

## In-app link handling

The DevRev SDK provides a mechanism to handle links opened from within any screen that is part of the DevRev SDK.

You can fully customize the link handling behavior by setting the specialized in-app link handler. That way you can decide what should happen when a link is opened from within the app.

```swift
DevRev.inAppLinkHandler: ((URL) -> Void)?
```

You can further customize the behavior by setting the `shouldDismissModalsOnOpenLink` boolean flag. This flag controls whether the DevRev SDK should dismiss the top-most modal screen when a link is opened.

```swift
DevRev.shouldDismissModalsOnOpenLink: Bool
```

## Configure dynamic theme

The DevRev SDK allows you to configure the theme dynamically based on the system appearance, or use the theme configured on the DevRev portal. By default, the theme is dynamic and follows the system appearance.

Use `SupportWidgetTheme` inside your `FeatureConfiguration` to align the support experience with your brand:

```swift
DevRev.updateFeatureConfiguration(
	FeatureConfiguration(
		enableFrameCapture: true,
		autoStartRecording: true,
		alwaysUseRemoteConfig: true,
		supportWidgetTheme: SupportWidgetTheme(
			prefersSystemTheme: false,
			primaryTextColor: "#202020",
			accentColor: "#34C759",
			conversationPageOptions: ConversationPageOptions(
				headerText: "Acme Support",
				subheaderText: "We're here to help"
			)
		),
		enableSupportChatStreaming: true
	)
)
```

  Directly mutating `DevRev.prefersSystemTheme` is maintained only for backward compatibility and is deprecated. Prefer configuring the theme through `SupportWidgetTheme` passed via `FeatureConfiguration`.

## PLuG article search filters

Set `FeatureConfiguration.supportWidgetArticleSearchFilters` to control which articles are returned by PLuG search (widget search and CMDK search). Filters are applied automatically when the support widget is ready.

Use `ArticleSearchFilters` to set separate filters for widget search (`widgetSearch`) and CMDK search (`searchBarSearch`). Each filter uses DQL-style expressions with an operator (`op`) and `operands` (field, op, value, valueType). Use `ArticleSearchFilterOperator` cases such as `.and`, `.or`, `.in`, `.eq`, `.ne`, `.gt`, `.gte`, `.lt`, `.lte` (plus other backend-supported operators), and `ArticleSearchFilterOperandValueType` (`.json` or `.part`) for each operand's `valueType`.

Example:

```swift
let filters = ArticleSearchFilters(
    widgetSearch: ArticleSearchFilter(
        op: .and,
        operands: [
            ArticleSearchFilterOperand(
                field: "article.tags.tag_id",
                op: .in,
                value: .stringArray(["don:core:dvrv-us-1:devo/1T6yocw2Y9:tag/32"]),
                valueType: .json
            )
        ]
    ),
    searchBarSearch: ArticleSearchFilter(
        op: .and,
        operands: [
            ArticleSearchFilterOperand(
                field: "article.tags.tag_id",
                op: .ne,
                value: .stringArray(["don:core:dvrv-us-1:devo/1T6yocw2Y9:tag/32"]),
                valueType: .json
            )
        ]
    )
)
DevRev.configure(
    appID: appID,
    featureConfiguration: FeatureConfiguration(
        enableFrameCapture: true,
        autoStartRecording: true,
        alwaysUseRemoteConfig: true,
        supportWidgetTheme: .systemDefault,
        supportWidgetArticleSearchFilters: filters
    )
)
```

To filter only one surface, pass a filter for that surface only (for example, `ArticleSearchFilters(widgetSearch: someFilter, searchBarSearch: nil)`). Pass `nil` for `supportWidgetArticleSearchFilters` for no filter.

> **Note:**
>   For the AI agent on the conversation page to use the same filtered article set, configure the Hybrid Search snap-in and attach it to the agent's skills in the DevRev app. See [DevRev docs](https://devrev.ai/docs) for snap-in setup.

## Track analytics

The DevRev SDK records custom analytic events using a name and a string dictionary. Track these events using the following function:

```swift
DevRev.trackEvent(name:properties:)
```

For example:

```swift
await DevRev.trackEvent(name: "open-message-screen", properties: ["id": "message-1337"])
```

> **Note:**
>   Custom events are captured as part of session replay. Event names must be non-empty, at most 250 characters, and match the regular expression `^[a-zA-Z0-9_-]+$`. Use only letters, digits, underscores, and hyphens. Calls that violate this are ignored. Keep event names and properties small, because large payloads bloat the device's local memory and can lead to missed recordings.

## Manage session analytics

The DevRev SDK offers session analytics features to help you understand how users interact with your app.

### Opt in or out

Session analytics features are opted-in by default, enabling them from the start. However, you can opt-out using the following method:

```swift
DevRev.stopAllMonitoring()
```

To opt back in, use the following method:

```swift
DevRev.resumeAllMonitoring()
```

### Session recording

You can enable session recording to capture user interactions with your app.

> **Note:**
>   The session recording feature is opt-out and is enabled by default.

The session recording feature includes the following methods to control the recording:

| Method                                | Action                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `DevRev.startRecording()`             | Starts the session recording.                                                                       |
| `DevRev.stopRecording()`              | Ends the session recording and uploads it to the portal.                                            |
| `DevRev.pauseRecording()`             | Pauses the ongoing session recording.                                                               |
| `DevRev.resumeRecording()`            | Resumes a paused session recording.                                                                 |
| `DevRev.processAllOnDemandSessions()` | Stops the ongoing user recording and sends all on-demand sessions along with the current recording. |

You can also check the following flags for session recording:

```swift
// Check if session recording is currently active.
let isRecording = DevRev.isRecording

// Check if session monitoring is enabled.
let isMonitoringEnabled = DevRev.isMonitoringEnabled

// Check if on-demand sessions are enabled.
let areOnDemandSessionsEnabled = DevRev.areOnDemandSessionsEnabled
```

### Session properties

You can add custom properties to the session recording to help you understand the context of the session. The properties are defined as a dictionary of string values.

```swift
DevRev.addSessionProperties(_:)
```

To clear the session properties in scenarios such as user logout or when the session ends, use the following method:

```swift
DevRev.clearSessionProperties()
```

  Avoid passing special characters in the session properties, as these characters can lead to file corruption and missed recordings.

### Mask sensitive data

To protect sensitive data, the DevRev SDK provides an auto-masking feature that masks data before sending to the server. Input views such as text fields, text views, and web views are automatically masked.

When `FeatureConfiguration.maskAllTextByDefault` is set to `true`, all text-bearing views — including labels, buttons, and SwiftUI `Text` views — are also automatically masked in session recordings. It is `false` by default, meaning only input fields are masked.

While the auto-masking feature may be sufficient for most situations, you can manually mark additional views as sensitive using the following method:

```swift
DevRev.markSensitiveViews(_:)
```

If any previously masked views need to be unmasked, you can use the following method:

```swift
DevRev.unmarkSensitiveViews(_:)
```

### Custom masking provider

For advanced use cases, you can provide a custom masking provider to specify exactly which regions of the UI should be masked in snapshots.

You can implement your own masking logic by conforming to the `DevRev.MaskLocationProviding` protocol and setting your custom object as the masking provider. This allows you to specify explicit regions to be masked or to skip snapshots entirely.

| Symbol                                                                        | Description                                                                                       |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `DevRev.setMaskingLocationProvider(_ provider: DevRev.MaskLocationProviding)` | A custom provider that determines which UI regions should be masked for privacy during snapshots. |
| `DevRev.MaskLocationProviding`                                                | A protocol for providing explicit masking locations for UI snapshots.                             |
| `DevRev.SnapshotMask`                                                         | An object that describes the regions of a snapshot to be masked.                                  |
| `DevRev.SnapshotMask.Location`                                                | An object that describes a masked region.                                                         |

For example:

```swift
import Foundation
import UIKit
import DevRevSDK

class MyMaskingProvider: NSObject, DevRev.MaskLocationProviding {
	func provideSnapshotMask() async -> DevRev.SnapshotMask {
        let region = CGRect(x: 10, y: 10, width: 100, height: 40)
        let location = DevRev.SnapshotMask.Location(location: region)
        let mask = DevRev.SnapshotMask(locations: [location], shouldSkip: false)
		return mask
	}
}
```

```swift
DevRev.setMaskingLocationProvider(MyMaskingProvider())
```

> **Tip:**
>   Setting a new provider overrides any previously set masking location provider.

### Track user interactions

The DevRev SDK automatically tracks user interactions such as taps, swipes, and scrolls. However, in some cases you may want to disable this tracking to prevent sensitive user actions from being recorded.

To temporarily disable user interaction tracking, use the following method:

```swift
DevRev.pauseUserInteractionTracking()
```

To resume user interaction tracking, use the following method:

```swift
DevRev.resumeUserInteractionTracking()
```

### Use timers

The DevRev SDK offers a timer mechanism to measure the time spent on specific tasks, allowing you to track events such as response time, loading time, or any other duration-based metrics.

The mechanism works using balanced start and stop methods that both accept a timer name and an optional dictionary of properties.

To start a timer, use the following method:

```swift
DevRev.startTimer(_:properties:)
```

To stop a timer, use the following method:

```swift
DevRev.endTimer(_:properties:)
```

For example:

```swift
DevRev.startTimer("response-time", properties: ["id": "task-1337"])

// Perform the task that you want to measure.

DevRev.endTimer("response-time", properties: ["id": "task-1337"])
```

Measure the time a user spends on a screen: start the timer when the screen appears and end it when the screen disappears.

```swift
.onAppear {
    DevRev.startTimer("screen-time", properties: ["screen": "profile"])
}
.onDisappear {
    DevRev.endTimer("screen-time", properties: ["screen": "profile"])
}
```

Measure screen navigation time: start the timer when navigation begins and end it when the destination screen is shown.

```swift
DevRev.startTimer("navigation-time", properties: ["to": "checkout"])

// Navigate to the destination screen.

DevRev.endTimer("navigation-time", properties: ["to": "checkout"])
```

  Avoid passing special characters in the timer properties, as these characters can lead to file corruption and missed recordings.

### Capture errors

You can report a handled error from a catch block using the `captureError` function.

This ensures that even if the error is handled in your app, it is still logged for diagnostics.

```swift
DevRev.captureError(
    _ error: Error,
    tag: String
)
```

For example:

```swift
do {
    try someFunction()
} catch {
    DevRev.captureError(
        error,
        tag: "network-failure"
    )
}
```

### Track screens

The DevRev SDK offers automatic screen tracking to help you understand how users navigate through your app. Although view controllers are automatically tracked, you can manually track screens using the following method:

```swift
DevRev.trackScreenName(_:)
```

For example:

```swift
DevRev.trackScreenName("profile-screen")
```

### Configure network observability

Network observability captures outgoing network requests (URL, method, status, and timing) and attaches them to session replays, enabling correlation of user activity with the underlying network traffic.

The feature is **off by default**. To enable it, pass a `NetworkObservabilityConfiguration` instance via `FeatureConfiguration.networkObservability` while configuring the SDK:

```swift
DevRev.configure(
	appID: "abcdefg12345",
	featureConfiguration: FeatureConfiguration(
		networkObservability: NetworkObservabilityConfiguration(
			enabled: true,
			allowlist: ["*.myapp.com/*", "https://api.example.org/*"],
			pathRedactionPatterns: ["users/*", "orders/*/items"],
			includeResponseBody: false,
			includeTimingBreakdown: true,
			maxBodySize: 64 * 1024,
			maxEventsPerSession: 5000,
			customSensitiveKeys: ["org_id", "session_token"]
		)
	)
)
```

> **Warning:**
>   Only requests matching the `allowlist` are captured. When the allowlist is `nil` or empty, **no requests are captured** even if `enabled` is `true`. Set the allowlist to the endpoints you want to observe.

### Network observability configuration reference

`NetworkObservabilityConfiguration` controls which requests are captured and how their data is sanitized before being recorded.

| Property                 | Type        | Default         | Description                                                                                                                                                                                                     |
| ------------------------ | ----------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`                | `Bool`      | `true`          | Master toggle for network observability.                                                                                                                                                                        |
| `allowlist`              | `[String]?` | `nil`           | Glob patterns matched against the full URL, where `*` matches any sequence. Only matching URLs are captured; when `nil` or empty, nothing is captured.                                                          |
| `pathRedactionPatterns`  | `[String]?` | `nil`           | Path patterns whose wildcard segments are replaced with `<redacted>`. `*` matches one segment, `**` matches zero or more. Prefix-based, e.g. `users/*` redacts the id in `users/42/profile`.                    |
| `includeResponseBody`    | `Bool`      | `false`         | When `true`, response bodies are captured and scrubbed.                                                                                                                                                         |
| `includeTimingBreakdown` | `Bool`      | `false`         | When `true`, the timing breakdown (DNS, TCP, TLS, TTFB) is captured.                                                                                                                                            |
| `maxBodySize`            | `Int`       | `65536` (64 KB) | Maximum response body size in bytes before truncation.                                                                                                                                                          |
| `maxEventsPerSession`    | `Int`       | `5000`          | Maximum number of events captured per session. Once reached, monitoring pauses for the rest of the session.                                                                                                     |
| `customSensitiveKeys`    | `[String]?` | `nil`           | Extra keys whose values are redacted in query params, JSON bodies, headers, and form data, merged with the built-in list. Matched case-insensitively as a substring, so `"org_id"` also redacts `"sub_org_id"`. |

> **Note:**
>   A ready-made `NetworkObservabilityConfiguration.default` is available: network observability enabled, but with no allowlist (so nothing is captured until you set one), no path redaction, and response bodies and timing breakdown excluded.

### Remote configuration in the DevRev web app

Network observability is controlled remotely from the DevRev web app, without shipping an app update. When remote configuration is fetched, it **overrides** the developer-set `NetworkObservabilityConfiguration` values.

* Setting `enabled` to `false` remotely stops all network interception immediately.
* Changes to the allowlist, path redaction patterns, and event caps apply immediately (hot-toggle); no relaunch required.
* If the settings fetch fails, the SDK falls back to the last cached configuration.

> **Tip:**
>   Because remote configuration overrides local values, an admin can enable or disable network observability for all app installs from the DevRev web app even if the app was configured with `networkObservability: nil`.

**Configure the remote flag in the DevRev web app:**

1. Go to [**Settings**](https://app.devrev.ai) in the DevRev web app.
2. Go to **Session Replays > iOS > General**.
3. Locate the **Network Observability** toggle (marked with the iOS and Android platform indicators, since it applies to mobile SDKs) and switch it on or off.
4. Select the toggle, then expand the **Advanced** section to configure the allowlist and path redaction patterns.
5. Save the changes. The updated configuration is delivered to the SDK on its next settings fetch (at startup and when the app enters the background).

The toggle reflects the current remote state on page load, persists across reloads, and surfaces success or error feedback when saving.

> **Note:**
>   When the fetch succeeds and no cached configuration exists yet, the SDK defaults to `enabled: true`. Only URLs matching the allowlist are ever captured, so an empty allowlist means no requests are recorded even while the feature is enabled.

## Configure push notifications

You can configure your app to receive push notifications from the DevRev SDK. The SDK is designed to handle push notifications and execute actions based on the notification's content.

The DevRev backend sends push notifications to your app to notify users about new messages in the support chat.

### Configure

To receive push notifications, you need to configure your DevRev organization by following the instructions in the [push notifications](https://developer.devrev.ai/sdks/mobile/push-notifications) section.

You need to ensure that your iOS app is configured to receive push notifications. You can follow the [Apple documentation](https://developer.apple.com/documentation/usernotifications/registering_your_app_with_apns) for guidance on registering your app with Apple Push Notification service (APNs).

### Register for push notifications

> **Tip:**
>   Push notifications require that the SDK has been configured and the user has been identified (unverified and verified users). The user identification is required to send the push notification to the correct user.

The DevRev SDK offers a method to register your device for receiving push notifications. You can register for push notifications using the following method:

```swift
DevRev.registerDeviceToken(_:deviceID:)
```

The method requires a device identifier, which can either be an identifier unique to your system or the Apple-provided Vendor Identifier (IDFV). Typically, the token registration is called from the `AppDelegate.application(_:didRegisterForRemoteNotificationsWithDeviceToken:)` method.

For example:

```swift
func application(
	_ application: UIApplication,
	didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
) {
	guard
		let deviceID = UIDevice.current.identifierForVendor?.uuidString
	else {
		return
	}

	Task {
		await DevRev.registerDeviceToken(
			deviceToken,
			deviceID: deviceID
		)
	}
}
```

### Unregister from push notifications

If your app no longer needs to receive push notifications, you can unregister the device.

Use the following method to unregister the device:

```swift
DevRev.unregisterDevice(_:)
```

This method requires the device identifier, which should be the same as the one used during registration. It is recommended to place this method after calling `UIApplication.unregisterForRemoteNotifications()` in your app.

For example:

```swift
UIApplication.shared.unregisterForRemoteNotifications()

Task {
	guard
		let deviceID = UIDevice.current.identifierForVendor?.uuidString
	else {
		return
	}

	await DevRev.unregisterDevice(deviceID)
}
```

### Handle push notifications

Push notifications coming to the DevRev SDK need to be handled manually. To properly handle them, implement the following method, typically in either the `UNUserNotificationCenterDelegate.userNotificationCenter(_:didReceive:)` or `UIApplicationDelegate.application(_:didReceiveRemoteNotification:fetchCompletionHandler:)`:

```swift
DevRev.processPushNotification(_:)
```

  For convenience, this method provides two overloads that accept `userInfo` as either `[AnyHashable: Any]` or `[String: any Sendable]` dictionary types.

For example:

```swift
func userNotificationCenter(
	_ center: UNUserNotificationCenter,
	didReceive response: UNNotificationResponse
) async {
	await DevRev.processPushNotification(response.notification.request.content.userInfo)
}
```
