# Quickstart guide

Source: <https://developer.devrev.ai/sdks/flutter/quickstart>
Scraped: 2026-11-03

## Requirements

* Flutter 3.3.0 or later.
* Dart SDK 3.5.0 or later.
* Android: minimum API level 24.
* iOS: minimum deployment target 15.0.

## Installation

To install the DevRev SDK, run the following command:

```sh
flutter pub add devrev_sdk_flutter
```

It automatically fetches the latest version of our package and adds it to your project's pubspec.yaml file:

```yaml
dependencies:
    devrev_sdk_flutter: <VERSION>
```

Alternatively, you can add the dependency manually by adding the package to your `pubspec.yaml` file under the `dependencies` section and run `flutter pub get` to install the package.

To get the latest version of the SDK, you can check the [pub.dev page](https://pub.dev/packages/devrev_sdk_flutter).

> **Note:**
>   Starting with version `2.2.5`, the iOS portion of the plugin ships with a CocoaPods podspec. Flutter uses CocoaPods by default, so no additional Swift Package Manager configuration is required. If you prefer to keep using Swift Package Manager (`flutter config --enable-swift-package-manager`), the package continues to publish a `Package.swift`.

## Set up the DevRev SDK

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Under **PLuG settings** copy the value under **Your unique App ID**.
3. Configure the DevRev SDK in your app using the obtained credentials.

  The DevRev SDK must be configured before you can use any of its features.

The SDK becomes ready for use once the configuration API is executed. Import the SDK and use `FeatureConfiguration` and `SupportWidgetTheme` when you need to customize behavior:

```dart
import 'package:devrev_sdk_flutter/devrev.dart';

// Configure with app ID only (defaults for all options).
await DevRev.configure(appID);
```

To provide a feature configuration during setup, pass a `FeatureConfiguration` as the second argument:

```dart
await DevRev.configure(appID, featureConfiguration);
```

For default behavior, call with just the app ID:

```dart
await DevRev.configure("abcdefg12345");
```

To customize behavior such as frame capture, auto-start recording, dialog mode (Android only), or theme preferences, pass a `FeatureConfiguration`:

```dart
final featureConfiguration = FeatureConfiguration(
  enableFrameCapture: true,
  autoStartRecording: true,
  alwaysUseRemoteConfig: true,
  prefersDialogMode: false,  // Android only
  supportWidgetTheme: SupportWidgetTheme(
    prefersSystemTheme: false,
    primaryTextColor: '#000000',
    accentColor: '#FF5733',
    spacing: {'bottom': '20px', 'side': '15px'},
  ),
);

await DevRev.configure(appID, featureConfiguration);
```

### Update the feature configuration

You can adjust the feature configuration without reconfiguring the SDK:

```dart
await DevRev.updateFeatureConfiguration(FeatureConfiguration(
  enableFrameCapture: true,
  autoStartRecording: false,
  alwaysUseRemoteConfig: true,
  prefersDialogMode: false,  // Android only
  supportWidgetTheme: SupportWidgetTheme(prefersSystemTheme: true),
));
```

### Feature configuration reference

`FeatureConfiguration` controls how the SDK behaves both during initial setup and when calling `DevRev.updateFeatureConfiguration`. All properties are required when providing a feature configuration.

| Property                | Type                 | Default | Description                                                                             |
| ----------------------- | -------------------- | ------- | --------------------------------------------------------------------------------------- |
| `enableFrameCapture`    | `bool`               | `true`  | Enables the screen capture pipeline used by session replay.                             |
| `autoStartRecording`    | `bool`               | `true`  | Automatically starts recording after the SDK finishes remote configuration.             |
| `prefersDialogMode`     | `bool`               | `false` | Prefer dialog mode for the support UI (Android only).                                   |
| `alwaysUseRemoteConfig` | `bool`               | `true`  | Always use remote config.                                                               |
| `supportWidgetTheme`    | `SupportWidgetTheme` | —       | Controls the appearance of the in-app support widget, including dynamic theme behavior. |

#### Support widget theme options

`SupportWidgetTheme` lets you fine-tune the support UI. Use the `supportWidgetTheme` property inside your feature configuration.

```dart
SupportWidgetTheme(
  prefersSystemTheme: false,
  primaryTextColor: '#1F2933',
  accentColor: '#F97316',
  spacing: {'bottom': '20px', 'side': '16px'},
)
```

| Property             | Type                   | Default | Description                                                                              |
| -------------------- | ---------------------- | ------- | ---------------------------------------------------------------------------------------- |
| `prefersSystemTheme` | `bool`                 | `true`  | Follows the device appearance when `true`; otherwise uses your custom colors.            |
| `primaryTextColor`   | `String?`              | —       | Hex color string (e.g. `'#000000'`, `'#1F2933'`) for primary text in the support widget. |
| `accentColor`        | `String?`              | —       | Hex color string (e.g. `'#F97316'`, `'#FF0000'`) applied to buttons and highlights.      |
| `spacing`            | `Map<String, String>?` | —       | CSS-like spacing overrides (`bottom` and `side` keys are recognized).                    |

## Sample app

A sample app with use cases for the DevRev SDK for Flutter has been provided as a part of our [public repository](https://github.com/devrev/devrev-sdk-flutter). To set up and run the sample app:

1. Go to the `sample` directory:
   ```sh
   cd sample
   flutter clean
   rm -rf ios android web linux macos windows
   flutter create --platforms=android,ios .
   ```

2. Install dependencies:
   ```sh
   flutter pub get
   ```

3. iOS app:
   Open the `ios/Runner.xcworkspace` in Xcode for running the iOS app or run the following command.

   ```sh
   flutter run -d ios
   ```

   Additional Steps for iOS before running the app:

   1. Change the minimum iOS deployment target version to `15.0`.
   2. Go to the `ios` directory and perform `pod install`.
   3. (Optional) If you have enabled Flutter's Swift Package Manager integration, open `ios/Runner.xcodeproj` in Xcode and set `Package dependencies -> FlutterGeneratedPluginSwiftPackage -> Package.swift` to use:
      ```swift
      platforms: [
         .iOS("15.0")
      ]
      ```
   4. Build and run the app.

4. Android app:
   Open the `android` directory in Android Studio or run the following command.
   ```sh
   flutter run -d android
   ```
