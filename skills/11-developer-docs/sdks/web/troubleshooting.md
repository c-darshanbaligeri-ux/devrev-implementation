# Troubleshooting

Source: <https://developer.devrev.ai/sdks/web/troubleshooting>
Scraped: 2026-11-03

Most Web SDK problems surface in one of three places: an error in the browser console, a blocked request in the network tab, or a session that never appears in **Session Replays**. Start with those three signals, then work through the checks below.

## Debugging checklist

When a session, an event, or a session property doesn't appear as expected, verify the following in order:

1. The `plug.js` script loads successfully in the network tab, and `observability.js` loads after it.

2. Session recording is enabled in [**Settings > Plug & Portal > Session Replays**](https://app.devrev.ai/?setting=session-settings) for the web platform.

3. The app ID in your `init()` call belongs to the workspace and environment you're testing against.

4. All required DevRev domains are allow-listed in your Content Security Policy (CSP).

5. The `plug-settings.get` request returns successfully.

6. Calls to `trackEvent`, `addSessionProperties`, and `getSessionDetails` are wrapped in a readiness check.

7. Event and session properties are flat objects containing string keys and string values.

## Session lifecycle

Session boundaries explain most reports of missing or duplicated sessions:

* A session begins when the user opens the page and the SDK initializes.

* A session ends after 30 minutes of inactivity, or when it reaches its maximum length of 4 hours.

* Activity after a session ends starts a new session with a new session ID.

* A single session can span multiple browser tabs.

## Sessions and tabs

The Web SDK tracks sessions at the user level, so one user maps to one session within an activity window. When the same user opens five tabs, the result is one session that contains five tab recordings. Over time, a single user accumulates multiple sessions, and each of those sessions can contain recordings from several tabs.

Because the session model is keyed on the user, `user_ref` must be a stable, unique identifier for the person using your application. The following values break the model:

* Values that change on every page refresh: each refresh creates a new user identity and pollutes your user base.

* Values assigned when a new tab opens: every tab becomes a separate user.

* Transaction, journey, or proposal IDs: a single user can hold many of these simultaneously, so they don't identify a user.

If a value describes what the user is doing rather than who the user is, it doesn't belong in `user_ref`.

The SDK doesn't support splitting one user's activity into separate sessions per tab, per transaction, or per journey. To keep an individual journey searchable, send its identifier as a custom event instead:

```jsx
window.plugSDK.trackEvent("journey_started", {
  journey_id: "JRN-12345",
  proposal_id: "PROP-67890",
  customer_name: "John Doe"
});
```

You can then search for that event on the **Session Replays** page to narrow down which session contains the journey, though you still need to review the tab recordings within that session to find the specific one.

## Readiness pattern for session methods

Session recording initializes asynchronously, after `init()` returns. Before calling `trackEvent`, `addSessionProperties`, or `getSessionDetails`, confirm that the SDK is ready by checking `isObservabilityReady` and listening for the `ON_OBSERVABILITY_READY` event:

```jsx
function initTracking() {
  window.plugSDK.trackEvent('page_loaded');
  window.plugSDK.addSessionProperties({ plan: 'premium' });
}

if (window.plugSDK.isObservabilityReady) {
  initTracking();
} else {
  window.plugSDK.onEvent((payload) => {
    if (payload.type === 'ON_OBSERVABILITY_READY') {
      initTracking();
    }
  });
}
```

> **Warning:**
>   Both branches are required. Implementing only one of them causes silent data loss.

The `if` branch covers the case where session recording finished initializing before your code ran, which happens on cached page loads, inside delayed callbacks, and in handlers triggered by user interaction. Without it, `ON_OBSERVABILITY_READY` has already fired by the time you attach the listener, so your callback never runs.

The `else` branch covers the more common case where your code runs before initialization completes, such as on a slow network or when the tracking call sits at the top of a page script. Without it, the call is dropped because the SDK can't process it yet.

Calls made before the SDK is ready are dropped, aren't associated with a session ID, arrive without user properties or session metadata, and can land out of sequence.

To confirm your implementation handles both cases, add timing logs to each branch and test on a fast connection, on a throttled connection, and on a cached page load. A fast or cached load should execute the `if` branch, and a throttled load should execute the `else` branch.

## Installation issues

* **Issue**: The browser console reports `Refused to load the script 'https://plug-platform.devrev.ai/static/plug.js' because it violates the following Content Security Policy directive`.

  **Solution**: Allow the DevRev domains in your Content Security Policy. For the full list of domains, refer to [Install the Web SDK](installation.md).

* **Issue**: The `plug.js` script loads, but no session is recorded and requests to other DevRev domains are blocked.

  **Solution**: Allow-list every required DevRev domain rather than only `plug-platform.devrev.ai`. Session recording depends on `observability.js` and on the regional ingestion endpoint, so allowing the platform domain alone is not sufficient.

* **Issue**: The `init()` call fails with a 403 error.

  **Solution**: Verify that the app ID matches the workspace and environment you're testing against. Copy it again from **Settings > Support > Plug Settings** under the **Configuration** tab.

* **Issue**: Requests to DevRev time out.

  **Solution**: Determine whether the failure is specific to DevRev by loading unrelated control sites. If only DevRev requests fail, a corporate firewall or proxy is blocking DevRev, and your network team must allow `*.devrev.ai` on outbound HTTPS traffic over port 443. If control sites fail too, check the connection or VPN and retry.

## Session recording issues

* **Issue**: Sessions aren't recording after the SDK is installed.

  **Solution**: Work through the following checks:

  1. Confirm that session recording is enabled in [**Settings > Plug & Portal > Session Replays**](https://app.devrev.ai/?setting=session-settings) for the web platform.

  2. Confirm that the app ID is correct for the workspace and environment.

  3. Confirm that all required DevRev domains are allow-listed in your CSP.

  4. In the network tab, confirm that both `plug.js` and `observability.js` load successfully.

  5. Turn the session recording setting off and on again, then reload the page.

* **Issue**: Some sessions are missing from **Session Replays**.

  **Solution**: Check the following causes:

  1. The session is shorter than the **Exclude sessions less than** threshold configured in your workspace settings.

  2. Session recording was disabled for the app while the session was in progress.

  3. The app ID passed to `init()` belongs to a different workspace or environment.

  4. Special characters in session properties or event properties corrupted the recording file.

  5. The available network bandwidth was insufficient to upload the recording.

* **Issue**: More sessions are created for a user than expected.

  **Solution**: A new session after 30 minutes of inactivity, after the 4 hour maximum duration, or after `user_ref` changes is expected behavior. Investigate the following causes instead:

  1. A transaction, journey, or tab identifier is passed as `user_ref`.

  2. `user_ref` is auto-generated and changes on every page load.

  3. `shutdown()` and `init()` are called when the user identity hasn't changed.

  4. `shutdown()` is called without `await`, so `init()` runs before teardown completes.

* **Issue**: Custom fonts or other externally hosted assets don't render in a session replay.

  **Solution**: The asset is served from a domain that isn't allow-listed by the DevRev CSP, which permits assets only from known-safe sources such as Google Fonts. Contact DevRev support so that your asset source can be evaluated for allow-listing.

* **Issue**: Native browser UI doesn't appear in a replay, including the expanded option list of a `<select>` element, native date and color pickers, autofill suggestions, right-click context menus, and file picker dialogs. Hovering and scrolling inside these controls is also absent.

  **Solution**: Use a DOM-rendered component instead of the native browser element, such as a scripted dropdown or date picker that renders its contents as regular HTML elements. Session recording captures changes to the page's DOM, and the browser draws these native controls in a separate operating system layer that never becomes part of the DOM, so no data about them is captured. This is a browser-level constraint that affects DOM-based session recording generally. The outcome of the interaction is still captured: for a native `<select>`, the replay shows the selected value along with a **Form change** event.

## Event and session property issues

* **Issue**: Events don't appear in the session timeline.

  **Solution**: Check the following causes:

  1. The event was tracked before session recording was ready. Wrap the call in the readiness pattern.

  2. The properties object contains nested objects instead of flat string key-value pairs.

  3. The payload sets a reserved property name. Don't set `devrev_source_identifier`, `plugSessionId`, or `is_devrev_internal_event`.

* **Issue**: Event properties are dropped even though the event itself is recorded.

  **Solution**: Pass properties as a flat object rather than serializing them into a single key:

  ```jsx
  // Incorrect: the serialized payload is dropped
  window.plugSDK.trackEvent("error_log", {
    properties: JSON.stringify(errorData)
  });

  // Correct: flat string key-value pairs
  window.plugSDK.trackEvent("error_log", {
    statusCode: "500",
    message: "Server error",
    url: "/api/orders"
  });
  ```

* **Issue**: Property keys or values are truncated in the session timeline.

  **Solution**: Keep keys within 128 characters and values within 256 characters. Anything beyond those limits is truncated.

* **Issue**: Recordings go missing after session properties are added.

  **Solution**: Remove special characters from session property keys and values, because they can corrupt the recording file. Keep keys alphanumeric, use string values only, and set a minimal number of properties. Reserve session properties for filtering and segmentation attributes such as `plan_type`, `user_role`, and `region`, and never include authentication tokens.

## Masking issues

Masked content is removed before the recording is sent, so it never reaches DevRev. The SDK masks `password`, `email`, and `tel` inputs by default, and you can control the rest with CSS classes:

* `ue-mask`: masks the element and its descendants with an asterisk overlay.

* `ue-input-mask`: shows the input value as asterisks in the replay.

* `ue-block`: prevents the element from being captured at all.

* `ue-unmask`: explicitly unmasks an element inside a masked ancestor.

For initialization options such as `maskAllInputs`, `maskInputOptions`, and `maskImagesByAncestor`, refer to [UserExperior migration](migration.md).

* **Issue**: Static text isn't masked in the replay.

  **Solution**: Apply `ue-mask` to the element itself or to a parent that contains it. To mask an entire page, apply the class to `<body>`.

* **Issue**: Masked elements still show their content in the replay.

  **Solution**: Check the class spelling, since `ue-masked` and similar variants have no effect. Also confirm that the class is present in the markup before the SDK captures the element, and that your own CSS isn't overriding the mask styles.

* **Issue**: Images are still visible inside a container that has `ue-mask` applied.

  **Solution**: Check whether `maskImagesByAncestor` is set to `false` in your `init()` options, which limits masking to images that carry the class directly. Either remove that option or apply `ue-mask` to the `*[image: figure — see source page]*` element.

* **Issue**: Masking doesn't apply to tooltips or other dynamically rendered content.

  **Solution**: Confirm that the class is applied to the element that actually renders the content, since tooltips are often mounted outside the container they belong to visually.

* **Issue**: You need to confirm that masking works before releasing to production.

  **Solution**: Record a test session that exercises the masked elements, then open the replay and verify that each one shows asterisks. For a quick, code-free option in regulated environments, enable the full masking toggle in [**Settings > Plug & Portal > Session Replays**](https://app.devrev.ai/?setting=session-settings) for the web platform, which masks all content globally.

> **Note:**
>   To label an element in the web player timeline for easier navigation, add a `data-plug-label` attribute to it, for example `<h1 data-plug-label="Checkout page">`.

## Cross-domain and iframe issues

The SDK stores session state in browser storage, which the same-origin policy confines to a single domain. Subdomains such as `app.example.com` and `docs.example.com` are handled automatically by first-party cookies, but navigation between two distinct domains records separate, unconnected sessions unless you pass the session details across.

* **Issue**: A user journey that spans two domains is recorded as two separate sessions.

  **Solution**: Install the SDK on both domains with the same app ID, then carry the session details from the source domain to the destination domain. On the source domain, read the identifiers once session recording is ready:

  ```jsx
  window.plugSDK.onEvent((payload) => {
    if (payload.type === 'ON_OBSERVABILITY_READY') {
      const { sessionId, tabId } = window.plugSDK.getSessionDetails();
      // Pass these to the destination domain
    }
  });
  ```

  Pass the identifiers using URL query parameters, `window.postMessage` for iframe scenarios, or a server-side redirect. On the destination domain, supply them to `init()`:

  ```jsx
  window.plugSDK.init({
    app_id: '<your_unique_app_id>',
    session_recording_options: {
      sessionDetails: {
        sessionId: sessionId, // from the source domain
        tabId: tabId,         // from the source domain
      },
    },
  });
  ```

  For more information, refer to [Cross-domain session tracking](https://support.devrev.ai/devrev/article/ART-21920).

* **Issue**: Session details are passed between domains, but the sessions still don't stitch together.

  **Solution**: Log `window.plugSDK.getSessionDetails()` on both domains and compare the values, then confirm that the SDK is installed on both domains, that both use the same app ID, that both have session recording enabled, and that the destination domain receives the identifiers before `init()` runs.

* **Issue**: A cross-origin iframe isn't included in the recording.

  **Solution**: Install the SDK on both the parent page and the iframe page, use the same app ID on both, and set `recordCrossOriginIframes` to `true` in both `init()` calls so that the SDK can establish a communication bridge:

  ```jsx
  window.plugSDK.init({
    app_id: "<your_unique_app_id>",
    session_recording_options: {
      sessionReplay: {
        recordCrossOriginIframes: true
      }
    }
  });
  ```

  Initializing the SDK on the parent page that hosts the iframe is mandatory. This is a security restriction enforced by modern browsers rather than a DevRev constraint, so a setup that initializes only inside the iframe is not supported.

* **Issue**: A same-origin iframe isn't included in the recording.

  **Solution**: Install the SDK on the iframe page. Same-origin iframes need no additional configuration.

## Platform support

The Web SDK works with modern frontend frameworks, including React, Angular, Vue, and Next.js, and with JSP pages using the standard script tag approach. The bundle is roughly 300 KB, loads asynchronously, and adds under 100 ms to page load.

Framesets and Flutter web applications aren't supported. A cross-origin iframe that hosts a Flutter application can't be recorded even when the SDK is initialized inside it.

## Pre-launch verification

Before enabling the SDK in production, confirm the following:

1. The integration is tested in a staging environment on both fast and throttled connections.

2. All required DevRev domains are allow-listed in the production CSP.

3. Session recording is enabled in [**Settings > Plug & Portal > Session Replays**](https://app.devrev.ai/?setting=session-settings).

4. Masking rules are applied, verified in an actual replay, and documented for your team.

5. Key business events appear in the session timeline with the expected properties.

6. The login and logout flow sets and clears `user_ref` correctly, and the replay shows the anonymous to identified transition.

7. (Optional) Cross-domain stitching is tested with real navigation between the domains involved.
