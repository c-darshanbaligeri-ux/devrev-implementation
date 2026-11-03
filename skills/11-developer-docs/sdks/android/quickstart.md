# Quickstart guide

Source: <https://developer.devrev.ai/sdks/android/quickstart>
Scraped: 2026-11-03

## Requirements

* Android Studio 2025.1.1 or later.
* Android Gradle Plugin 8.2 or later.
* Gradle 8.9 or later.
* Minimum Android API level 24.

## Integration

To integrate the latest version of our SDK into your app, follow these steps:

  #### Kotlin
    1. Add the following dependencies to your app's `build.gradle.kts` file:

       ```kotlin
       dependencies {
        implementation("ai.devrev.sdk:devrev-sdk:")
       }
       ```
    2. Add `mavenCentral` to your root `build.gradle.kts` file:
       ```kotlin
       repositories {
        mavenCentral()
       }
       ```
  

  #### Groovy
    1. Add the following dependencies to your app's `build.gradle` file:

       ```groovy
       dependencies {
        implementation 'ai.devrev.sdk:devrev-sdk:'
       }
       ```

    2. Add `mavenCentral` to your root `build.gradle` file:
       ```groovy
       repositories {
           mavenCentral()
       }
       ```
  

### ProGuard rules

If you are using ProGuard in your project, add the following lines to your configuration:

```bash
-keep class ai.devrev.** { *; }
-keep class com.userexperior.* { *; }
```

## Set up the DevRev SDK

1. Open the DevRev web app at [https://app.devrev.ai](https://app.devrev.ai) and go to the **Settings** page.
2. Copy the value under **Your unique App ID** from **PLuG settings**.
3. Configure the DevRev SDK in your app using the obtained credentials.

  The DevRev SDK must be configured before you can use any of its features.

The SDK becomes ready for use once the configuration API is executed. Remote configuration is fetched from the backend and cached locally. On subsequent launches, you can use the cached configuration to avoid a network round-trip and speed up cold start (see [Configuration caching](#configuration-caching)).

  #### Kotlin
    ```kotlin
    DevRev.configure(context: Context, appId: String)
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.configure(Context context, String appId, FeatureConfiguration featureConfiguration);
    ```
  

To provide a feature configuration during setup, call the overload that accepts it:

  #### Kotlin
    ```kotlin
    DevRev.configure(context: Context, appId: String, featureConfiguration: FeatureConfiguration)
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.configure(Context context, String appId, FeatureConfiguration featureConfiguration);
    ```
  

For default behavior, call the simpler overload:

  #### Kotlin
    ```kotlin
    DevRev.configure(context = this, appId = "<APP_ID>")
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.configure(this, "<APP_ID>", new FeatureConfiguration());
    ```
  

To customize behavior such as frame capture, auto-start recording, configuration caching, or theme preferences, pass a `FeatureConfiguration` instance:

  #### Kotlin
    ```kotlin
    DevRev.configure(
        context = this,
        appId = "<APP_ID>",
        featureConfiguration = FeatureConfiguration(
            enableFrameCapture = false,
            autoStartRecording = false,
            prefersDialogMode = false,
            alwaysUseRemoteConfig = true,
            supportWidgetTheme = SupportWidgetTheme(prefersSystemTheme = true)
        )
    )
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.configure(
        this,
        "<APP_ID>",
        new FeatureConfiguration(
            false,   // enableFrameCapture
            false,   // autoStartRecording
            false,   // prefersDialogMode
            true,    // alwaysUseRemoteConfig
            new SupportWidgetTheme(true, null, null, null)
        )
    );
    ```
  

Ensure that the custom application is specified in the `AndroidManifest.xml`:

```xml
<application
    android:name=".MyApp">
</application>
```

Use this property to check whether the DevRev SDK has been configured:

  #### Kotlin
    ```kotlin
    DevRev.isConfigured
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.isConfigured();
    ```
  

4. Call the following method inside your `Application` class to configure the SDK.

> **Tip:**
>   If you don’t have a custom `Application` class, create one as shown below.

  #### Kotlin
    ```kotlin
    import ai.devrev.sdk.DevRev

    class FooApplication : Application() {

       override fun onCreate() {
          super.onCreate()
          DevRev.configure(
                context = this,
                appId = "<APP_ID>"
          )
       }
    }
    ```
  

  #### Java
    ```java
    import ai.devrev.sdk.DevRev;
    import ai.devrev.sdk.model.FeatureConfiguration;

    public class FooApplication extends Application {

       @Override
       public void onCreate() {
          super.onCreate();
          DevRev.INSTANCE.configure(
                this,
                "<APP_ID>",
                new FeatureConfiguration()
          );
       }
    }
    ```
  

5. In the `onCreate` method of your `Application`, configure the DevRev SDK with the required parameters using the credentials obtained earlier.
6. Ensure that the custom application is specified in the `AndroidManifest.xml`, as shown below:

```xml
<application
    android:name=".FooApplication">
</application>
```

### Update the feature configuration

You can adjust the feature configuration without reconfiguring the SDK:

  #### Kotlin
    ```kotlin
    DevRev.updateFeatureConfiguration(
        context = this,
        featureConfiguration = FeatureConfiguration(
            enableFrameCapture = true,
            autoStartRecording = true,
            prefersDialogMode = false,
            alwaysUseRemoteConfig = true,
            supportWidgetTheme = SupportWidgetTheme(prefersSystemTheme = true)
        )
    )
    ```
  

  #### Java
    ```java
    DevRev.INSTANCE.updateFeatureConfiguration(
        this,
        new FeatureConfiguration(
            true,    // enableFrameCapture
            true,    // autoStartRecording
            false,   // prefersDialogMode
            true,    // alwaysUseRemoteConfig
            new SupportWidgetTheme(true, null, null, null)
        )
    );
    ```
  

> **Note:**
>   The `autoStartRecording`, `prefersDialogMode`, and `alwaysUseRemoteConfig` flags are set during initial configuration only and do not change at runtime. To control recording manually, use `DevRev.startRecording()` and `DevRev.stopRecording()`.

### Feature configuration reference

`FeatureConfiguration` controls how the SDK behaves both during initial setup and when calling `DevRev.updateFeatureConfiguration`.

  #### Kotlin
    ```kotlin
    val configuration = FeatureConfiguration.default
    ```
  

  #### Java
    ```java
    FeatureConfiguration configuration = new FeatureConfiguration();
    ```
  

| Property                            | Type                    | Default | Description                                                                                                                                                                                                              |
| ----------------------------------- | ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `enableFrameCapture`                | `Boolean`               | `true`  | Enables the screen capture pipeline used by session replay.                                                                                                                                                              |
| `autoStartRecording`                | `Boolean`               | `true`  | Automatically starts recording after the SDK finishes remote configuration (or when using cached config).                                                                                                                |
| `prefersDialogMode`                 | `Boolean`               | `false` | Opens SDK screens as a bottom sheet instead of a separate activity.                                                                                                                                                      |
| `alwaysUseRemoteConfig`             | `Boolean`               | `true`  | When `true`, the SDK always fetches remote configuration at startup and when the app enters foreground. When `false`, the SDK uses cached configuration when available and skips the remote fetch, improving cold start. |
| `supportWidgetTheme`                | `SupportWidgetTheme?`   | `null`  | Controls the appearance of the in-app support widget, including dynamic theme behavior.                                                                                                                                  |
| `enableSupportChatStreaming`        | `Boolean`               | `false` | When `true`, enables real-time AI agent response streaming in PLuG conversations (WebSocket streaming, optimistic UI, animated text).                                                                                    |
| `supportWidgetArticleSearchFilters` | `ArticleSearchFilters?` | `null`  | Optional filters for PLuG article search (widget and CMDK). Applied automatically when the support widget is ready.                                                                                                      |

Use the constructor to override any combination of options:

  #### Kotlin
    ```kotlin
    val configuration = FeatureConfiguration(
        enableFrameCapture = false,
        autoStartRecording = false,
        prefersDialogMode = false,
        alwaysUseRemoteConfig = false,
        supportWidgetTheme = SupportWidgetTheme(prefersSystemTheme = true),
        enableSupportChatStreaming = true,
        supportWidgetArticleSearchFilters = myArticleSearchFilters
    )
    ```
  

  #### Java
    ```java
    FeatureConfiguration configuration = new FeatureConfiguration(
        false,   // enableFrameCapture
        false,   // autoStartRecording
        false,   // prefersDialogMode
        false,   // alwaysUseRemoteConfig
        new SupportWidgetTheme(true, null, null, null),
        true,    // enableSupportChatStreaming
        myArticleSearchFilters
    );
    ```
  

#### Configuration caching

When `alwaysUseRemoteConfig` is `false`, the SDK uses the last successfully fetched configuration stored on the device. If a cached configuration exists, the SDK skips the remote config request at startup and applies the cached settings (for example, session replay, observability). This reduces cold-start latency and allows the app to work offline with the last known config. The first launch (or after clearing app data) still performs a remote fetch when network is available. Set `alwaysUseRemoteConfig` to `true` (the default) to retain the previous behavior of always fetching remote configuration at startup and when the app enters foreground.

#### Support widget theme options

`SupportWidgetTheme` lets you fine-tune the support UI. Provide explicit values to customize:

  #### Kotlin
    ```kotlin
    val customTheme = SupportWidgetTheme(
        prefersSystemTheme = false,
        primaryTextColor = "#1F2933",
        accentColor = "#F97316",
        spacing = mapOf("bottom" to "20px", "side" to "16px")
    )
    ```
  

  #### Java
    ```java
    SupportWidgetTheme customTheme = new SupportWidgetTheme(
        false,       // prefersSystemTheme
        "#1F2933",   // primaryTextColor
        "#F97316",   // accentColor
        new HashMap<String, String>() {{
            put("bottom", "20px");
            put("side", "16px");
        }}
    );
    ```
  

| Property                  | Type                       | Default | Description                                                                   |
| ------------------------- | -------------------------- | ------- | ----------------------------------------------------------------------------- |
| `prefersSystemTheme`      | `Boolean?`                 | `null`  | Follows the device appearance when `true`; otherwise uses your custom colors. |
| `primaryTextColor`        | `String?`                  | `null`  | Hex or RGB value for primary text in the support widget.                      |
| `accentColor`             | `String?`                  | `null`  | Hex or RGB value applied to buttons and highlights.                           |
| `spacing`                 | `Map<String, String>?`     | `null`  | CSS-like spacing overrides; `"bottom"` and `"side"` keys are recognized.      |
| `conversationPageOptions` | `ConversationPageOptions?` | `null`  | Customizes the conversation page header and subheader text.                   |

#### Conversation page options

`ConversationPageOptions` lets you customize the header branding shown at the top of the PLuG conversation screen:

  #### Kotlin
    ```kotlin
    val theme = SupportWidgetTheme(
        prefersSystemTheme = true,
        conversationPageOptions = ConversationPageOptions(
            headerText = "Acme Support",
            subheaderText = " "   // single space blanks the subheader
        )
    )
    ```
  

  #### Java
    ```java
    ConversationPageOptions options = new ConversationPageOptions(
        "Acme Support",   // headerText
        " "               // subheaderText — single space blanks the subheader
    );
    SupportWidgetTheme theme = new SupportWidgetTheme(
        true,    // prefersSystemTheme
        null,    // primaryTextColor
        null,    // accentColor
        null,    // spacing
        options
    );
    ```
  

| Property        | Type      | Default | Description                                                                           |
| --------------- | --------- | ------- | ------------------------------------------------------------------------------------- |
| `headerText`    | `String?` | `null`  | Custom text for the conversation header. Uses the server default when `null`.         |
| `subheaderText` | `String?` | `null`  | Custom text for the subheader. Pass `" "` (single space) to render a blank subheader. |

## Use the sample app

A sample app demonstrates use cases with both XML-based UI and Jetpack Compose as part our [public repository](https://github.com/devrev/devrev-sdk-android).

Before running the sample app, make sure to configure it with your DevRev credentials. To do this, update the `ai.devrev.sdk.sample.DevRevApplication` class with your credentials.
