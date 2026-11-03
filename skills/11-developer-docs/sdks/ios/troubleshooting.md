# Troubleshooting

Source: <https://developer.devrev.ai/sdks/ios/troubleshooting>
Scraped: 2026-11-03

* **Issue**: Can't import the SDK into my app.
  **Solution**: Double-check the setup process and ensure that `DevRevSDK` is correctly linked to your application.

* **Issue**: How does the DevRev SDK handle errors?
  **Solution**: The DevRev SDK reports all errors in the console using Apple's Unified Logging System. Look for error messages in the subsystem `ai.devrev.sdk`.

* **Issue**: Support chat doesn't show.
  **Solution**: Call one of the identification methods: `DevRev.identifyUnverifiedUser(...)` or `DevRev.identifyVerifiedUser(...)`.

* **Issue**: Not receiving push notifications.
  **Solution**: Configure your app to receive push notifications and register your device with the DevRev SDK.

* **Issue**: Encountering lags across the app.
  **Solution**: In the DevRev org, go to **Settings** > **Session Replays** > **iOS Tab** > **General Settings Tab**. Change the **Video Quality** to **Low** and the **Screenshot Time Interval** to >=800. If these settings are not available, raise a ticket with DevRev support.

* **Issue**: Some of the sessions are missing from the portal.
  **Solution**: Sessions might not be ingested due to multiple reasons. Check the following:
  * Session length is less than the `Exclude sessions less than` time configured in the org settings.
  * The network bandwidth is insufficient for the files to be uploaded to the portal.
  * The app was killed but never launched again in the next 48 hours.
  * Session recordings were disabled for the app.
  * Incorrect app id was provided in the `DevRev.configure(...)` method.
  * Special characters in the session properties/events might lead to file corruption and eventually missed recording.
