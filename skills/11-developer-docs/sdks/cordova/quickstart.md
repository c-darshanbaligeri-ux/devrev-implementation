# Quickstart guide

Source: <https://developer.devrev.ai/sdks/cordova/quickstart>
Scraped: 2026-11-03

This guide helps you integrate the DevRev SDK into your Cordova app.

## Requirements

* Cordova 12.0 or later.
* Android: minimum API level 24.
* iOS: minimum deployment target 15.0.
* Recommended: an SSH key configured locally and registered with [GitHub](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh).

## Install

To install the DevRev SDK, run the following command:

```sh
cordova plugin add @devrev/sdk-cordova
```

## Set up the DevRev SDK

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Under **PLuG settings**, copy the value under **Your unique App ID**.
3. Configure the DevRev SDK in your app using the obtained credentials.

  The DevRev SDK must be configured before you can use any of its features.

The SDK becomes ready for use once the configuration API is executed.

```javascript
DevRev.configure(appID, successCallback, errorCallback)
```

To provide a feature configuration during setup, call the overload that accepts it:

```javascript
DevRev.configure(appID, featureConfiguration, successCallback, errorCallback)
```

For default behavior, call the simpler form:

```javascript
DevRev.configure(appID, function() {
    console.log('DevRev SDK configured successfully.');
}, function(error) {
    console.error('Failed to configure DevRev SDK:', error);
});
```

To customize behavior such as frame capture, auto-start recording, or theme preferences, pass a full `FeatureConfiguration` object:

```javascript
DevRev.configure(appID, {
    enableFrameCapture: false,
    autoStartRecording: false,
    prefersDialogMode: false,
    alwaysUseRemoteConfig: true,
    supportWidgetTheme: {
        prefersSystemTheme: true,
    },
}, function() {
    console.log('DevRev SDK configured with FeatureConfiguration.');
}, function(error) {
    console.error('Failed to configure DevRev SDK:', error);
});
```

### Update the feature configuration

You can adjust the feature configuration without reconfiguring the SDK. Pass a **full** `FeatureConfiguration` object (all properties are required):

```javascript
DevRev.updateFeatureConfiguration({
    enableFrameCapture: true,
    autoStartRecording: true,
    prefersDialogMode: false,
    alwaysUseRemoteConfig: true,
    supportWidgetTheme: {
        prefersSystemTheme: true,
    },
}, function() {
    console.log('Feature configuration updated.');
}, function(error) {
    console.error('Failed to update feature configuration:', error);
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

```javascript
var customTheme = {
    prefersSystemTheme: false,
    primaryTextColor: '#1F2933',
    accentColor: '#F97316',
    spacing: {
        bottom: '20px',
        side: '16px'
    }
};
```

| Property             | Type                         | Default | Description                                                                                      |
| -------------------- | ---------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| `prefersSystemTheme` | `boolean`                    | `true`  | Follows the device appearance when `true`; otherwise uses your custom colors.                    |
| `primaryTextColor`   | `string?`                    | —       | Hex color string (for example, `'#000000'`, `'#1F2933'`) for primary text in the support widget. |
| `accentColor`        | `string?`                    | —       | Hex color string (for example, `'#F97316'`, `'#FF0000'`) applied to buttons and highlights.      |
| `spacing`            | `{ [key: string]: string }?` | —       | CSS-like overrides (`bottom` and `side` keys are recognized).                                    |

## Sample app

A sample app with use cases for the DevRev Cordova plugin is provided as part of our [public repository](https://github.com/devrev/devrev-sdk-cordova). To set up and run the sample app:

```sh
cd sample
npm install
cordova platform add android
cordova platform add ios
```

  #### Android
    ```sh
    cordova run android
    ```

    OR open `platforms/android` in Android Studio and run the app.
  

  #### iOS
    1. Open `platforms/ios/Podfile` and ensure it contains:

    ```ruby
    platform :ios, '15.0'
    ```

    2. Install dependencies:

    ```sh
    cd platforms/ios
    pod install
    ```

    3. Run the app:

    ```sh
    cordova run ios
    ```

    OR open `DevRevSDKSample.xcworkspace` in Xcode and run the app.
