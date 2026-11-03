# Quickstart guide (React Native)

Source: <https://developer.devrev.ai/sdks/react-native/quickstart>
Scraped: 2026-11-03

This guide helps you integrate the DevRev SDK into your React Native and Expo app.

## Requirements

* React Native 0.79.0 or later.
* For Expo apps, Expo 50.0.0 or later.
* Android: minimum API level 24.
* iOS: minimum deployment target 15.1.

## Installation

To install the DevRev SDK, run the following command:

```sh
npm install @devrev/sdk-react-native
```

### Expo

1. To install the DevRev SDK, run the following command:
   ```bash
   npx expo install @devrev/sdk-react-native-expo-plugin
   ```
2. Configure the Expo config plugin in your `app.json` or `app.config.js`:
   ```json
   {
     "expo": {
       "plugins": [
         "@devrev/sdk-react-native-expo-plugin"
       ]
     }
   }
   ```
3. Rebuild your app:
   ```bash
   npx expo prebuild --clean
   ```

## Set up the DevRev SDK

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Under **PLuG settings** copy the value under **Your unique App ID**.
3. Configure the DevRev SDK in your app using the obtained credentials.

> **Warning:**
>   The DevRev SDK must be configured before you can use any of its features.

The SDK becomes ready for use once the configuration API is executed.

```typescript
DevRev.configure(appID)
```

To provide a feature configuration during setup, call the overload that accepts it:

```typescript
DevRev.configure(appID, featureConfiguration)
```

For default behavior, call the simpler form:

```typescript
DevRev.configure('abcdefg12345')
```

To customize behavior such as frame capture, auto-start recording, or theme preferences, pass a full `FeatureConfiguration` object:

```typescript
DevRev.configure('abcdefg12345', {
  enableFrameCapture: false,
  autoStartRecording: false,
  prefersDialogMode: false,
  alwaysUseRemoteConfig: true,
  supportWidgetTheme: {
    prefersSystemTheme: true,
  },
});
```

### Update the feature configuration

You can adjust the feature configuration without reconfiguring the SDK. Pass a **full** `FeatureConfiguration` object (all properties are required):

```typescript
DevRev.updateFeatureConfiguration({
  enableFrameCapture: true,
  autoStartRecording: true,
  prefersDialogMode: false,
  alwaysUseRemoteConfig: true,
  supportWidgetTheme: {
    prefersSystemTheme: true,
  },
});
```

### Feature configuration reference

`FeatureConfiguration` controls how the SDK behaves both during initial setup and when calling `DevRev.updateFeatureConfiguration(...)`. All properties are required when providing a feature configuration.

| Property                | Type                 | Default | Description                                                                             |
| ----------------------- | -------------------- | ------- | --------------------------------------------------------------------------------------- |
| `enableFrameCapture`    | `boolean`            | `true`  | Enables the screen capture pipeline used by session replay.                             |
| `autoStartRecording`    | `boolean`            | `true`  | Automatically starts recording after the SDK finishes remote configuration.             |
| `prefersDialogMode`     | `boolean`            | `false` | Prefer dialog mode for the support UI (Android only).                                   |
| `alwaysUseRemoteConfig` | `boolean`            | `true`  | Always use remote config.                                                               |
| `supportWidgetTheme`    | `SupportWidgetTheme` | —       | Controls the appearance of the in-app support widget, including dynamic theme behavior. |

#### Support widget theme options

`SupportWidgetTheme` lets you fine-tune the support UI. Use the `supportWidgetTheme` property inside your feature configuration.

```typescript
const customTheme = {
  prefersSystemTheme: false,
  primaryTextColor: '#1F2933',
  accentColor: '#F97316',
  spacing: {
    bottom: '20px',
    side: '16px',
  },
};
```

| Property             | Type                         | Default | Description                                                                              |
| -------------------- | ---------------------------- | ------- | ---------------------------------------------------------------------------------------- |
| `prefersSystemTheme` | `boolean`                    | `true`  | Follows the device appearance when `true`; otherwise uses your custom colors.            |
| `primaryTextColor`   | `string?`                    | —       | Hex color string (e.g. `'#000000'`, `'#1F2933'`) for primary text in the support widget. |
| `accentColor`        | `string?`                    | —       | Hex color string (e.g. `'#F97316'`, `'#FF0000'`) applied to buttons and highlights.      |
| `spacing`            | `{ [key: string]: string }?` | —       | CSS-like spacing overrides (`bottom` and `side` keys are recognized).                    |

## Sample app (without framework)

A sample app with use cases for the DevRev SDK for React Native has been provided as a part of our [public repository](https://github.com/devrev/devrev-sdk-react-native). To set up and run the sample app:

1. Go to the sample directory:
   ```bash
   cd sample/react-native
   ```
2. Install the dependencies:
   ```bash
   yarn install
   ```
3. For iOS, run:
   ```bash
   pod install --project-directory=ios --repo-update
   ```
4. Start the React Native development server:
   ```bash
   npx react-native start
   ```
5. Run the app on Android using:
   ```bash
   npx react-native run-android
   ```
   or open the `android` directory in Android Studio and run the app from there.
6. Run the app on iOS using:
   ```bash
   npx react-native run-ios
   ```
   or open `ios/DevRevSDKSampleRN.xcworkspace` in Xcode and run the app from there.

## Sample app (Expo)

A sample app with use cases for the DevRev SDK for Expo has been provided as a part of our [public repository](https://github.com/devrev/devrev-sdk-react-native). To set up and run the sample app:

1. Go to the sample directory:
   ```bash
   cd sample/expo
   ```
2. Install the dependencies:
   ```bash
   yarn install
   ```
3. Run clean and prebuild:
   ```bash
   npx expo prebuild --clean
   ```
4. Run the app on Android using:
   ```bash
   npx expo run:android
   ```
   OR open the `android` directory in Android Studio and run the app.
5. Run the app on iOS:
   ```bash
   npx expo run:ios
   ```
   OR open `ios/DevRevSDKSample.xcworkspace` in Xcode and run the app.
