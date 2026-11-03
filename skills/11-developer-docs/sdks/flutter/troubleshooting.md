# Troubleshooting

Source: <https://developer.devrev.ai/sdks/flutter/troubleshooting>
Scraped: 2026-11-03

* **Issue**: Support chat doesn't show.
  **Solution**: Call one of the identification methods: `DevRev.identifyUnverifiedUser(...)` or `DevRev.identifyVerifiedUser(...)`.

* **Issue**: Not receiving push notifications.
  **Solution**: Configure your app to receive push notifications and register your device with the DevRev SDK.

* **Issue**: Encountering lags across the app.
  **Solution**:

1. In the DevRev org, go to **Settings** > **Session Replays** > **Android Tab** > **General Settings Tab**.
2. Change the **Video Quality** to Low and the **Screenshot Time Interval** to >=800.
3. Do the same under the **iOS** tab as well if facing slowness.
4. Raise a ticket with DevRev support if these settings are not available.

* **Issue**: Some of the sessions are missing from the portal.
  **Solution**: Sessions might not be ingested due to multiple reasons. Check the following:
  * Session length is less than the `Exclude sessions less than` time configured in the org settings.
  * The network bandwidth is insufficient for the files to be uploaded to the portal.
  * The app was killed but never launched again in the next 48 hours.
  * Session recordings were disabled for the app.
  * Incorrect app id was provided in the `DevRev.configure(...)` method.
  * Special characters in the session properties/events might lead to file corruption and eventually missed recording.

* **Issue**: Integrated the latest version of the SDK but the portal still shows recordings being ingested from an older version.
  **Solution**: This is a dependency caching issue. Please run the following commands to clear the cache:
  ```sh
  cd android && ./gradlew clean
  ./gradlew build
  cd ..
  flutter clean
  flutter pub get
  ```
