# Features

Source: <https://developer.devrev.ai/sdks/react-native/features>
Scraped: 2026-11-03

## Identification

To access certain features of the DevRev SDK, user identification is required.

The identification function should be placed appropriately in your app after the user logs in. If you have the user information available at app launch, call the function after the `DevRev.configure(appID: string)` method.

> **Tip:**
>   If you haven't previously identified the user, the DevRev SDK will automatically create an anonymous user for you immediately after the SDK is configured.

> **Tip:**
>   The `Identity` structure allows for custom fields in the user, organization, and account traits. These fields must be configured through the DevRev app before they can be used. For more information, refer to [Object customization](https://support.devrev.ai/devrev/article/ART-21854).

You can select from the following methods to identify users within your application:

### Identify an unverified user

The unverified identification method identifies users with a unique identifier, but it does not verify their identity with the DevRev backend.

```typescript
DevRev.identifyUnverifiedUser(userID: string, organizationID?: string)
```

### Identify a verified user

The verified identification method is used to identify users with an identifier unique to your system within the DevRev platform. The verification is done through a token exchange process between you and the DevRev backend.

The steps to identify a verified user are as follows:

1. Generate an AAT for your system (preferably through your backend).
2. Exchange your AAT for a session token for each user of your system.
3. Pass the user identifier and the exchanged session token to the `DevRev.identifyVerifiedUser(userID: string, sessionToken: string)` method.

> **Warning:**
>   For security reasons, it is **strongly recommended** that the token exchange is executed on your backend to prevent exposing your application access token (AAT).

#### Generate an AAT

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Open the **Plug Tokens** page.
3. Under the **Application access tokens** panel, click **New token** and copy the token that's displayed.

> **Warning:**
>   Ensure that you copy the generated application access token, as you cannot view it again.

#### Exchange your AAT for a session token

To proceed with identifying the user, you need to exchange your AAT for a session token. This step helps you identify a user of your own system within the DevRev platform.

Here is a simple example of an API request to the DevRev backend to exchange your AAT for a session token:

> **Warning:**
>   Make sure that you replace the `` and `<YOUR_USER_ID>` with the actual values.

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

> **Warning:**
>   As a good practice, **your** app should retrieve the exchanged session token from **your** backend at app launch or any relevant app lifecycle event.

#### Identify the verified user

Pass the user identifier and the exchanged session token to the verified identification method:

```typescript
DevRev.identifyVerifiedUser(userID: string, sessionToken: string)
```

### Update the user

You can update the user's information using the following method:

```typescript
DevRev.updateUser(identity: Identity)
```

> **Warning:**
>   The `userID` property cannot be updated.

### Logout

You can logout of the current user by using the following method:

```typescript
DevRev.logout(deviceID: string)
```

### Identity model

The `Identity` interface is used to provide user, organization, and account information when identifying users or updating their details. This class is used primarily with the `identifyUnverifiedUser` and `updateUser` methods.

#### Properties

The `Identity` class contains the following properties:

| Property             | Type                  | Required | Description                                   |
| -------------------- | --------------------- | -------- | --------------------------------------------- |
| `userRef`            | `string`              | ✅        | A unique identifier for the user              |
| `organizationRef`    | `string?`             | ❌        | An identifier for the user's organization     |
| `accountRef`         | `string?`             | ❌        | An identifier for the user's account          |
| `userTraits`         | `UserTraits?`         | ❌        | Additional information about the user         |
| `organizationTraits` | `OrganizationTraits?` | ❌        | Additional information about the organization |
| `accountTraits`      | `AccountTraits?`      | ❌        | Additional information about the account      |

> **Note:**
>   The custom fields properties defined as part of the user, organization and account traits, must be configured in the DevRev web app **before** they can be used. See [Object customization](https://support.devrev.ai/devrev/article/ART-21854) for more information.

##### Describe user traits

The `UserTraits` class contains detailed information about the user:

> **Note:**
>   All properties in `UserTraits` are optional.

| Property       | Type                     | Description                                      |
| -------------- | ------------------------ | ------------------------------------------------ |
| `displayName`  | `string?`                | The displayed name of the user                   |
| `email`        | `string?`                | The user's email address                         |
| `fullName`     | `string?`                | The user's full name                             |
| `description`  | `string?`                | A description of the user                        |
| `customFields` | `{ [key: string]: any }` | Dictionary of custom fields configured in DevRev |

##### Organization traits

The `OrganizationTraits` class contains detailed information about the organization:

> **Note:**
>   All properties in `OrganizationTraits` are optional.

| Property       | Type                     | Description                                      |
| -------------- | ------------------------ | ------------------------------------------------ |
| `displayName`  | `string?`                | The displayed name of the organization           |
| `domain`       | `string?`                | The organization's domain                        |
| `description`  | `string?`                | A description of the organization                |
| `phoneNumbers` | `string[]?`              | Array of the organization's phone numbers        |
| `tier`         | `string?`                | The organization's tier or plan level            |
| `customFields` | `{ [key: string]: any }` | Dictionary of custom fields configured in DevRev |

##### Account traits

The `AccountTraits` class contains detailed information about the account:

> **Note:**
>   All properties in `AccountTraits` are optional.

| Property       | Type                     | Description                                      |
| -------------- | ------------------------ | ------------------------------------------------ |
| `displayName`  | `string?`                | The displayed name of the account                |
| `domains`      | `string[]?`              | Array of domains associated with the account     |
| `description`  | `string?`                | A description of the account                     |
| `phoneNumbers` | `string[]?`              | Array of the account's phone numbers             |
| `websites`     | `string[]?`              | Array of websites associated with the account    |
| `tier`         | `string?`                | The account's tier or plan level                 |
| `customFields` | `{ [key: string]: any }` | Dictionary of custom fields configured in DevRev |

## Plug support chat

Once user identification is complete, you can start using the chat (conversations) dialog supported by our DevRev SDK. The support chat feature can be shown as a modal screen from the top-most screen.

```typescript
DevRev.showSupport()
```

### Create a new support conversation

You can initiate a new support conversation directly from your app. This method displays the support chat screen and simultaneously creates a new conversation.

```typescript
DevRev.createSupportConversation()
```

You can optionally pass a plain-text message to prefill the conversation input field:

```typescript
DevRev.createSupportConversation('I need help with billing for order #12345')
```

### In-app link handling

In certain cases, the links opened from the support chat are opened in the app instead of a browser. You can control whether the chat modal should be dismissed after the link is opened by calling the following method:

```typescript
DevRev.setShouldDismissModalsOnOpenLink(value: boolean)
```

Setting this flag to true applies the system's default behavior for opening links, which includes dismissing any DevRev modal screens to facilitate handling your own deep links.

### In-app link callback

> **Tip:**
>   This feature is supported only on Android.

For scenarios where custom handling is needed, links from the support chat can be captured with the following method:

```typescript
DevRev.setInAppLinkHandler((url) => {
	// Perform an action here.
});
```

## Dynamic theme configuration

The DevRev SDK allows you to configure the theme dynamically based on the system appearance, or use the theme configured on the DevRev portal. By default, the theme is dynamic and follows the system appearance.

```typescript
DevRev.setPrefersSystemTheme(value: boolean)
```

## Analytics

The DevRev SDK allows you to send custom analytic events by using a properties map. You can track these events using the following function:

```typescript
DevRev.trackEvent(name: string, properties?: { [key: string]: string })
```

> **Note:**
>   Event names must match the regular expression `^[a-zA-Z0-9_-]+$`. Use only letters, digits, underscores, and hyphens. Names containing other characters are rejected. Keep event names and properties small, because large payloads bloat the device's local memory and can lead to missed recordings.

## Manage session analytics

The DevRev SDK offers session analytics features to help you understand how users interact with your app.

### Opt in or out

Session analytics features are opted-in by default, enabling them from the start. However, you can opt-out using the following method:

```typescript
DevRev.stopAllMonitoring()
```

To opt back in, use the following method:

```typescript
DevRev.resumeAllMonitoring()
```

### Session recording

You can enable session recording to record user interactions with your app.

> **Note:**
>   The session recording feature is opt-out and is enabled by default.

The session recording feature includes the following methods to control the recording:

| Method                                | Action                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `DevRev.startRecording()`             | Starts the session recording.                                                                       |
| `DevRev.stopRecording()`              | Stops the session recording and uploads it to the portal.                                           |
| `DevRev.pauseRecording()`             | Pauses the ongoing session recording.                                                               |
| `DevRev.resumeRecording()`            | Resumes a paused session recording.                                                                 |
| `DevRev.processAllOnDemandSessions()` | Stops the ongoing user recording and sends all on-demand sessions along with the current recording. |

### Session properties

You can add custom properties to the session recording to help you understand the context of the session. The properties are defined as a map of string values.

```typescript
DevRev.addSessionProperties(properties: { [key: string]: string })
```

To clear the session properties in scenarios such as user logout or when the session ends, use the following method:

```typescript
DevRev.clearSessionProperties()
```

> **Warning:**
>   Avoid passing special characters in the session properties, as these characters can lead to file corruption and missed recordings.

### Mask sensitive data

To protect sensitive data, the DevRev SDK provides an auto-masking feature that masks data before sending to the server. Input views such as password text fields are automatically masked.

While the auto-masking feature is sufficient for most situations, you can manually mark additional views as sensitive using the following method:

```typescript
DevRev.markSensitiveViews(tags: any[])
```

If any previously masked views need to be unmasked, you can use the following method:

```typescript
DevRev.unmarkSensitiveViews(tags: any[])
```

For example:

```typescript
import * as DevRev from '@devrev/sdk-react-native';
import { View, Text, findNodeHandle } from "react-native";
import { useRef, useEffect } from "react";

const YourComponent = () => {
  const sensitiveViewRef = useRef(null);
  const insensitiveViewRef = useRef(null);

  useEffect(() => {
    // Mark sensitive view
    const sensitiveId = findNodeHandle(sensitiveViewRef.current);
    if (sensitiveId) {
      DevRev.markSensitiveViews([sensitiveId]);
    }

    // Unmark insensitive view
    const insensitiveId = findNodeHandle(insensitiveViewRef.current);
    if (insensitiveId) {
      DevRev.unmarkSensitiveViews([insensitiveId]);
    }
  }, []);

  return (
    <View>
      <View ref={sensitiveViewRef}>
        <Text>Sensitive content (masked in recordings)</Text>
      </View>
      <View ref={insensitiveViewRef}>
        <Text>Insensitive content (visible in recordings)</Text>
      </View>
    </View>
  );
};

export default YourComponent;
```

### Mask elements inside web views

To mark elements as sensitive inside a web view (`WebView`), apply the `devrev-mask` CSS class. To unmark them, use `devrev-unmask`.

* Mark an element as masked:
  ```html
  <label class="devrev-mask">OTP: 12345</label>
  ```
* Mark an element as unmasked:
  ```html
  <input type="text" placeholder="Enter Username" name="username" required class="devrev-unmask">
  ```

### Track user interactions

The DevRev SDK automatically tracks user interactions such as taps, swipes, and scrolls. However, in some cases you may want to disable this tracking to prevent sensitive user actions from being recorded.

To temporarily disable user interaction tracking, use the following method:

```typescript
DevRev.pauseUserInteractionTracking()
```

To resume user interaction tracking, use the following method:

```typescript
DevRev.resumeUserInteractionTracking()
```

### Use timers

The DevRev SDK offers a timer mechanism to measure the time spent on specific tasks, allowing you to track events such as response time, loading time, or any other duration-based metrics.

The mechanism uses balanced start and stop methods, both of which accept a timer name and an optional dictionary of properties.

To start a timer, use the following method:

```typescript
DevRev.startTimer(name: string, properties: { [key: string]: string })
```

To stop a timer, use the following method:

```typescript
DevRev.endTimer(name: string, properties: { [key: string]: string })
```

### Timer measurement

Measure the time spent on a screen by starting the timer when the screen mounts and ending it when it unmounts:

```typescript
useEffect(() => {
  DevRev.startTimer('screen-time', { screen: 'checkout' });
  return () => {
    DevRev.endTimer('screen-time', { screen: 'checkout' });
  };
}, []);
```

Measure screen navigation time by starting the timer when navigation begins and ending it once the destination screen is shown:

```typescript
DevRev.startTimer('navigation-time', { screen: 'checkout' });
navigation.navigate('Checkout');
// In the destination screen, once it is shown:
DevRev.endTimer('navigation-time', { screen: 'checkout' });
```

> **Warning:**
>   Avoid passing special characters in the timer properties, as these characters can lead to file corruption and missed recordings.

### Capture errors

You can report a handled error from a catch block using the `captureError` function.

This ensures that even if the error is handled in your app, it is still logged for diagnostics.

```typescript
DevRev.captureError(
    error: Error | string,
    tag: string
)
```

For example:

```typescript
try {
} catch (error) {
    DevRev.captureError(
        error,
        'network-failure'
    );
}
```

Example with `Error`:

```typescript
try {
    throw new Error('Something went wrong');
} catch (error) {
    DevRev.captureError(error, 'custom-error');
}
```

### Track screens

The DevRev SDK offers automatic screen tracking to help you understand how users navigate through your app. Although screens are automatically tracked, you can manually track screens using the following method:

```typescript
DevRev.trackScreenName(name: string)
```

### Manage screen transitions (Android only)

The DevRev SDK allows tracking of screen transitions to understand the user navigation within your app.
You can manually update the state using the following methods:

```javascript
// Mark the transition as started.
DevRev.setInScreenTransitioning(true)

// Mark the transition as ended.
DevRev.setInScreenTransitioning(false)
```

## Push notifications

You can configure your app to receive push notifications from the DevRev SDK. The SDK is able to handle push notifications and execute actions based on the notification's content.

The DevRev backend sends push notifications to your app to notify users about new messages in the Plug support chat.

### Configuration

To receive push notifications, you need to configure your DevRev organization by following the instructions in the [push notifications](../push-notifications.md) section.

### Register for push notifications

> **Tip:**
>   Push notifications require that the SDK has been configured and the user has been identified, to ensure delivery to the correct user.

The DevRev SDK offers a method to register your device for receiving push notifications. You can register for push notifications using the following method:

```typescript
DevRev.registerDeviceToken(deviceToken: string, deviceID: string)
```

On Android devices, the `deviceToken` should be the Firebase Cloud Messaging (FCM) token value, while on iOS devices, it should be the Apple Push Notification Service (APNs) token.

### Unregister from push notifications

If your app no longer needs to receive push notifications, you can unregister the device.

Use the following method to unregister the device:

```typescript
DevRev.unregisterDevice(deviceID: string)
```

The method requires the device identifier, which should be the same as the one used when registering the device.

### Handle push notifications

#### Android

On Android, notifications are implemented as data messages to offer flexibility. However, this means that automatic click processing isn't available. To handle notification clicks, developers need to intercept the click event, extract the payload, and pass it to a designated method for processing. This custom approach enables tailored notification handling in Android applications.

To process the notification, use the following method:

```typescript
DevRev.processPushNotification(payload: string)
```

Here, the `message` object from the notification payload needs to be passed to this function.

For example:

```typescript
const notificationPayload = {
	// message may be nested based on the notification library
	"message": {
		// ... (the entire message object)
	}
};
const messageJson = notificationPayload["message"];
DevRev.processPushNotification(JSON.stringify(messageJson));
```

#### iOS

On iOS, the `AppDelegate` must be updated to intercept notification clicks and forward the payload to the SDK.

In `didFinishLaunchingWithOptions`, set the `UNUserNotificationCenter` delegate:

```swift
UNUserNotificationCenter.current().delegate = self
```

Implement `userNotificationCenter(_:didReceive:)` to pass the notification payload to the SDK:

```swift
func userNotificationCenter(
    _ center: UNUserNotificationCenter,
    didReceive response: UNNotificationResponse
) async {
    await DevRev.processPushNotification(
        response.notification.request.content.userInfo
    )
}
```
