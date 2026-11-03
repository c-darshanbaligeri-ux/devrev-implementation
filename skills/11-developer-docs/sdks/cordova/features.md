# Features

Source: <https://developer.devrev.ai/sdks/cordova/features>
Scraped: 2026-11-03

## Identification

To access certain features of the DevRev SDK, user identification is required.

The identification function should be placed appropriately in your app after the user logs in. If you have the user information available at app launch, call the function after the `DevRev.configure(appID)` method.

> **Note:**
>   If you haven't previously identified the user, the DevRev SDK will automatically create an anonymous user for you immediately after the SDK is configured.

> **Note:**
>   The `Identity` structure allows for custom fields in the user, organization, and account traits. These fields must be configured through the DevRev app before they can be utilized. For more information, refer to [Object customization](https://support.devrev.ai/devrev/article/ART-21854).

You can select from the following methods to identify users within your application:

### Identify unverified users

The unverified identification method identifies users with a unique identifier, but it does not verify their identity with the DevRev backend.

```javascript
DevRev.identifyUnverifiedUser(identity, successCallback, errorCallback)
```

### Identify a verified user

The verified identification method is used to identify users with an identifier unique to your system within the DevRev platform. The verification is done through a token exchange process between you and the DevRev backend.

The steps to identify a verified user are as follows:

1. Generate an AAT for your system (preferably through your backend).
2. Exchange your AAT for a session token for each user of your system.
3. Pass the user identifier and the exchanged session token to the `DevRev.identifyVerifiedUser` method.

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

```javascript
DevRev.identifyVerifiedUser(userID, sessionToken, successCallback, errorCallback)
```

### Update the user

You can update the user's information using the following method:

```javascript
DevRev.updateUser(identity, successCallback, errorCallback)
```

> **Note:**
>   The `userID` property cannot be updated.

### Logout

You can log out the current user by using the following method:

```javascript
DevRev.logout(deviceID, successCallback, errorCallback)
```

The user will be logged out by clearing their credentials, as well as unregistering the device from receiving push notifications, and stopping the session recording.

## Plug support chat

Once user identification is complete, you can start using the chat (conversations) dialog supported by our DevRev SDK. The support chat feature can be shown as a modal screen from the top-most screen.

> **Note:**
>   This functionality requires the SDK to be configured and the user to be identified, whether they are unverified or verified.

To show the support chat screen in your app, you can use the following method:

```javascript
DevRev.showSupport(successCallback, errorCallback)
```

### Create a new support conversation

You can initiate a new support conversation directly from your app. This method displays the support chat screen and simultaneously creates a new conversation.

```javascript
DevRev.createSupportConversation(successCallback, errorCallback)
```

You can optionally pass a plain-text message to prefill the conversation input field:

```javascript
DevRev.createSupportConversation('I need help with billing for order #12345', successCallback, errorCallback)
```

## Handle in-app links

The DevRev SDK provides a mechanism to handle links opened from within any screen that is part of the DevRev SDK.

You can fully customize the link handling behavior by setting the specialized in-app link handler. That way you can decide what should happen when a link is opened from within the app.

```javascript
DevRev.setInAppLinkHandler(handler, successCallback, errorCallback)
```

You can further customize the behavior by setting the `setShouldDismissModalsOnOpenLink` boolean flag. This flag controls whether the DevRev SDK should dismiss the top-most modal screen when a link is opened.

```javascript
DevRev.setShouldDismissModalsOnOpenLink(value, successCallback, errorCallback)
```

## Configure dynamic theme

The DevRev SDK allows you to configure the theme dynamically based on the system appearance, or use the theme configured on the DevRev portal. By default, the theme is dynamic and follows the system appearance.

```javascript
DevRev.setPrefersSystemTheme(value, successCallback, errorCallback)
```

## Analytics

The DevRev SDK allows you to send custom analytic events by using a properties map. You can track these events using the following function:

```javascript
DevRev.trackEvent(name, properties, successCallback, errorCallback)
```

> **Note:**
>   Event names must match the regular expression `^[a-zA-Z0-9_-]+$`. Use only letters, digits, underscores, and hyphens. Names containing other characters are rejected. Keep event names and properties small, because large payloads bloat the device's local memory and can lead to missed recordings.

## Manage session analytics

The DevRev SDK offers session analytics features to help you understand how users interact with your app.

### Opt in or out

Session analytics features are opted-in by default, enabling them from the start. However, you can opt-out using the following method:

```javascript
DevRev.stopAllMonitoring(successCallback, errorCallback)
```

To opt back in, use the following method:

```javascript
DevRev.resumeAllMonitoring(successCallback, errorCallback)
```

### Session recording

You can enable session recording to capture user interactions with your app.

> **Note:**
>   The session recording feature is opt-out and is enabled by default.

The session recording feature includes the following methods to control the recording:

| Method                                                              | Action                                                                                              |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `DevRev.startRecording(successCallback, errorCallback)`             | Starts the session recording.                                                                       |
| `DevRev.stopRecording(successCallback, errorCallback)`              | Ends the session recording and uploads it to the portal.                                            |
| `DevRev.pauseRecording(successCallback, errorCallback)`             | Pauses the ongoing session recording.                                                               |
| `DevRev.resumeRecording(successCallback, errorCallback)`            | Resumes a paused session recording.                                                                 |
| `DevRev.processAllOnDemandSessions(successCallback, errorCallback)` | Stops the ongoing user recording and sends all on-demand sessions along with the current recording. |

### Session properties

You can add custom properties to the session recording to help you understand the context of the session. The properties are defined as a map of string values.

```javascript
DevRev.addSessionProperties(properties, successCallback, errorCallback)
```

To clear the session properties in scenarios such as user logout or when the session ends, use the following method:

```javascript
DevRev.clearSessionProperties(successCallback, errorCallback)
```

> **Warning:**
>   Avoid passing special characters in the session properties, as these characters can lead to file corruption and missed recordings.

### Mask sensitive data

To protect sensitive data, the DevRev SDK provides an auto-masking feature that masks data before sending to the server. Input views such as password text fields are automatically masked.

While the auto-masking feature is sufficient for most situations, you can manually mark or unmark additional views as sensitive.

To mark elements as sensitive inside a web view (`WebView`), apply the `devrev-mask` CSS class. To unmark them, use `devrev-unmask`.

1. Mark an element as masked.
   ```html
   <label class="devrev-mask">OTP: 12345</label>
   ```
2. Mark an element as unmasked.
   ```html
   <input type="text" placeholder="Enter Username" name="username" required class="devrev-unmask">
   ```

### Manage user interaction tracking

The DevRev SDK automatically tracks user interactions such as taps, swipes, and scrolls. However, in some cases you may want to disable this tracking to prevent sensitive user actions from being recorded.

To temporarily disable user interaction tracking, use the following method:

```javascript
DevRev.pauseUserInteractionTracking(successCallback, errorCallback)
```

To resume user interaction tracking, use the following method:

```javascript
DevRev.resumeUserInteractionTracking(successCallback, errorCallback)
```

### Implement timers

The DevRev SDK offers a timer mechanism to measure the time spent on specific tasks, allowing you to track events such as response time, loading time, or any other duration-based metrics.

The mechanism utilizes balanced start and stop methods, both of which accept a timer name and an optional dictionary of properties.

To start a timer, use the following method:

```javascript
DevRev.startTimer(name, properties, successCallback, errorCallback)
```

To stop a timer, use the following method:

```javascript
DevRev.endTimer(name, properties, successCallback, errorCallback)
```

### Timer usage examples

Measure the time spent on a screen by starting the timer when the screen appears and ending it when the screen is hidden.

```javascript
// On screen show
DevRev.startTimer('home-screen-view', { screen: 'home' }, function() {}, function(error) {});

// On screen hide
DevRev.endTimer('home-screen-view', { screen: 'home' }, function() {}, function(error) {});
```

Measure screen navigation time by starting the timer when navigation begins and ending it when the destination screen is shown.

```javascript
// When navigation begins
DevRev.startTimer('navigate-to-checkout', { from: 'cart', to: 'checkout' }, function() {}, function(error) {});

// When the destination screen is shown
DevRev.endTimer('navigate-to-checkout', { from: 'cart', to: 'checkout' }, function() {}, function(error) {});
```

> **Warning:**
>   Avoid passing special characters in the timer properties, as these characters can lead to file corruption and missed recordings.

### Capture errors

You can report a handled error from a catch block using the `captureError` function.

This ensures that even if the error is handled in your app, it is still logged for diagnostics.

```javascript
DevRev.captureError(
    error,
    tag
)
```

For example:

```javascript
try {
} catch (e) {
    DevRev.captureError(e, 'network-failure');
}
```

### Track screens

The DevRev SDK offers automatic screen tracking to help you understand how users navigate through your app. Although screens are automatically tracked, you can manually track screens using the following method:

```javascript
DevRev.trackScreenName(name, successCallback, errorCallback)
```

### Manage screen transitions (Android only)

The DevRev SDK allows tracking of screen transitions to understand the user navigation within your app.
You can manually update the state using the following methods:

```javascript
// Mark the transition as started.
DevRev.setInScreenTransitioning(true, successCallback, errorCallback)

// Mark the transition as ended.
DevRev.setInScreenTransitioning(false, successCallback, errorCallback)
```

## Push notifications

You can configure your app to receive push notifications from the DevRev SDK. The SDK is designed to handle push notifications and execute actions based on the notification's content.

The DevRev backend sends push notifications to your app to alert users about new messages in the Plug support chat.

### Configuration

To receive push notifications, you need to configure your DevRev organization by following the instructions in the [push notifications](../push-notifications.md) section.

### Register for push notifications

> **Note:**
>   Push notifications require SDK configuration and user identification, whether unverified or verified, to ensure delivery to the correct user.

The DevRev SDK offers a method to register your device for receiving push notifications. You can register for push notifications using the following method:

```javascript
DevRev.registerDeviceToken(deviceToken, deviceID, successCallback, errorCallback)
```

On Android devices, the `deviceToken` should be the Firebase Cloud Messaging (FCM) token value, while on iOS devices, it should be the Apple Push Notification Service (APNS) token.

### Unregister from push notifications

If your app no longer needs to receive push notifications, you can unregister the device.

Use the following method to unregister the device:

```javascript
DevRev.unregisterDevice(deviceID, successCallback, errorCallback)
```

### Processing push notifications

#### Android

On Android, notifications are implemented as data messages to offer flexibility. However, this means that automatic click processing isn't available. To handle notification clicks, developers need to intercept the click event, extract the payload, and pass it to a designated method for processing. This custom approach enables tailored notification handling in Android applications.

To process the notification, use the following method:

```javascript
DevRev.processPushNotification(payload, successCallback, errorCallback)
```

Here, the `message` object from the notification payload should be passed to this function.

For example:

```javascript
const notificationPayload = {
	"message": {
		"title": "New Message",
		"body": "You have received a new message.",
		"data": {
			"messageId": "12345",
			"sender": "John Doe"
		}
	}
};

const messageJson = notificationPayload["message"];

DevRev.processPushNotification(messageJson, function() {
	console.log("Push notification processed successfully.");
}, function(error) {
	console.error("Failed to process push notification:", error);
});
```

#### iOS

On iOS devices, pass the received push notification payload to the DevRev SDK for processing. The SDK handles the notification and executes the necessary actions.

```javascript
DevRev.processPushNotification(payload, successCallback, errorCallback)
```

For example:

```javascript
const notificationPayload = {
	"message": {
		"title": "New Message",
		"body": "You have received a new message.",
		"data": {
			"messageId": "12345",
			"sender": "John Doe"
		}
	}
};

const messageJson = notificationPayload["message"];

DevRev.processPushNotification(messageJson, function() {
	console.log("Push notification processed successfully.");
}, function(error) {
	console.error("Failed to process push notification:", error);
});
```
