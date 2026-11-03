# Troubleshooting

Source: <https://developer.devrev.ai/sdks/cordova/troubleshooting>
Scraped: 2026-11-03

* **Issue**: Support chat doesn't show.
  **Solution**: Ensure you have correctly called one of the identification methods: `DevRev.identifyUnverifiedUser(...)` or `DevRev.identifyVerifiedUser(...)`.

* **Issue**: Push notifications are not being received.
  **Solution**: Ensure that your app is configured to receive push notifications and that your device is registered with the DevRev SDK.

* **Issue**: Lags are encountered across the app.
  **Solution**:

1. Go to **Settings** > **Session Replays** > **Android Tab** > **General Settings Tab** in the DevRev org.
2. Change the **Video Quality** to Low and the **Screenshot Time Interval** to >=800.
3. Do the same under the **iOS tab** as well if facing slowness.
4. If these settings are not available, raise a ticket with DevRev support.

* **Issue**: Some of the sessions are missing from the portal.
  **Solution**: Sessions might not be ingested due to multiple reasons. Please check the following:
  * Session length is less than the `Exclude sessions less than` time configured in the org settings.
  * The network bandwidth is insufficient for the files to be uploaded to the portal.
  * The app was killed but never launched again in the next 48 hours.
  * Session recordings were disabled for the app.
  * Incorrect app id was provided in the `DevRev.configure(...)` method.
  * Special characters in the session properties/events might lead to file corruption and eventually missed recording.
