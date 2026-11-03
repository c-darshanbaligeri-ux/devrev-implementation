# Troubleshooting

Source: <https://developer.devrev.ai/sdks/react-native/troubleshooting>
Scraped: 2026-11-03

* **Issue**: Support chat doesn't show.
  **Solution**: Ensure you have correctly called one of the identification methods: `DevRev.identifyUnverifiedUser(...)`, `DevRev.identifyVerifiedUser(...)`, or `DevRev.identifyAnonymousUser(...)`.

* **Issue**: Not receiving push notifications.
  **Solution**: Configure your app to receive push notifications and register your device with the DevRev SDK.

* **Issue**: Encountering lags across the app.
  **Solution**: In the DevRev org, go to **Settings** > **Session Replays** > **Android Tab** > **General Settings Tab**. Change the **Video Quality** to **Low** and the **Screenshot Time Interval** to >=800. Do the same under the **iOS tab** as well if facing slowness. If these settings are not available, raise a ticket with DevRev support.

* **Issue**: Some of the sessions are missing from the portal.
  **Solution**: Sessions might not be ingested due to multiple reasons. Check the following:
  1. Session length is less than the `Exclude sessions less than` time configured in the org settings.
  2. The network bandwidth is insufficient for the files to be uploaded to the portal.
  3. The app was killed but never launched again in the next 48 hours.
  4. Session recordings were disabled for the app.
  5. Incorrect app id was provided in the `DevRev.configure(...)` method.
  6. Special characters in the session properties/events might lead to file corruption and eventually missed recording.
