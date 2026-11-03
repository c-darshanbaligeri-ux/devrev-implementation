# UserExperior migration

Source: <https://developer.devrev.ai/sdks/web/migration>
Scraped: 2026-11-03

The DevRev Plug SDK serves as a direct replacement for the legacy UserExperior Web SDK. This section outlines the steps to facilitate a seamless migration from UserExperior to DevRev Plug.

> **Note:**
>   NPM package support is discontinued.

## Installation

Update your script tags as shown to migrate successfully to the DevRev Plug SDK.

  #### UserExperior implementation
    ```jsx

    <script src="https://unpkg.com/user-experior-web@latest/bundle/ue-web-bundle.js"></script>
    ```
  

  #### Replace with Plug
    ```jsx

    <script type="text/javascript" src="https://plug-platform.devrev.ai/static/plug.js"></script>
    ```
  

## Initialization

Update your initialization code to work with the DevRev Plug SDK, ensuring session recording is enabled and handling events appropriately.

  #### UserExperior implementation
    ```jsx

    const ue = new UserExperior.init();
    ue.startRecording("<your_unique_app_id>")
    .then(() => {
      // code you want to execute after recording starts
      // you can call the setUserIdentifer method here
    })
    .catch((error) => {
      // code you want to execute if recording fails
    });
    ```
  

  #### Replace with Plug
    > **Note:**
>       To enable session recordings, go to **Settings** > **Support** > **Session Replays** and enable recordings for your desired platforms.
>

    ```jsx

    window.plugSDK.init({
       app_id: "<your_unique_app_id>",
       disable_plug_chat_window: true,
    });
    window.plugSDK.onEvent((payload) => {
    	if (payload.type === 'ON_OBSERVABILITY_READY') {
        // code you want to execute after recording starts
    	}
    });
    ```

    If you have configured Content Security Policy (CSP) in your application, you need to allow access to the following domains.

    * [https://api.devrev.ai](https://api.devrev.ai)
    * [https://plug-platform.devrev.ai](https://plug-platform.devrev.ai)
    * [https://ingestion-useast1.devrev.ai](https://ingestion-useast1.devrev.ai) - For organizations in the US East region.
    * [https://ingestion-eucentral1.devrev.ai](https://ingestion-eucentral1.devrev.ai) - For organizations in the EU Central region.
    * [https://ingestion-apsouth1.devrev.ai](https://ingestion-apsouth1.devrev.ai) - For organizations in the AP South region.
    * [https://ingestion-apsoutheast1.devrev.ai](https://ingestion-apsoutheast1.devrev.ai) - For organizations in the AP South East 1 region.
    * [https://ingestion-apsoutheast2.devrev.ai](https://ingestion-apsoutheast2.devrev.ai) - For organizations in the AP South East 2 region.
    * [https://dvrv-in-1-api.devrev.ai/](https://dvrv-in-1-api.devrev.ai/) - For organizations in the India region.
  

## Recording options

  #### UserExperior implementation
    ```jsx

    ue.startRecording("243b0f40-db67-4f3e-b51d-c52001dd858a", {
    	sessionReplay: {
    		// To mask all the input fields pass the following.
    		maskAllInputs: true,
    		
    		// Available Mask Input Options:
    		maskInputOptions: {
    		    color: boolean,
    		    date: boolean,
    		    'datetime-local': boolean,
    		    month: boolean,
    		    number: boolean,
    		    range: boolean,
    		    search: boolean,
    		    text: boolean,
    		    time: boolean,
    		    url: boolean,
    		    week: boolean,
    		    textarea: boolean
    		},
    		
    		// Mouse moves are also ignored by default by the SDK to avoid unnecessary events increasing the payload size. To enable mouse move capture  
    		// you need to specify the following option to capture the mouse movements:
    		captureMouseMove: true 
    		
    		// By default we track network log in session. To disable network log tracking you can specify the following option:
    		captureNetworkLogs: false 
    		
    		// By default we track console errors in session. To disable console tracking you can specify the following option:
    		captureConsoleLogs: false 

    		// By default, images inside a masked ancestor (for example, a parent with the ue-mask class) are also masked.
    		// Set to false to mask only images that have the mask class directly on the <img> element.
    		maskImagesByAncestor: true
    	}
    });
    ```
  

  #### Replace with Plug
    ```jsx

    window.plugSDK.init({
      app_id: "<your_unique_app_id>",
      disable_plug_chat_window: true,
      session_recording_options: {
      		sessionReplay: {
      			maskAllInputs?: boolean;
      			maskInputOptions?: {
      				color: boolean;
      				date: boolean;
      				'datetime-local': boolean;
      				email: boolean;
      				month: boolean;
      				number: boolean;
      				range: boolean;
      				search: boolean;
      				tel: boolean;
      				text: boolean;
      				time: boolean;
      				url: boolean;
      				week: boolean;
      				textarea: boolean;
      				select: boolean;
      			};
      			captureMouseMove?: boolean;
      			captureNetworkLogs?: boolean;
      			captureConsoleLogs?: boolean;
      			maskImagesByAncestor?: boolean;
      		}
      },
    })
    ```
  

| Option                 | Type      | Default | Description                                                                                                                                                                                                                                |
| ---------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `maskImagesByAncestor` | `boolean` | `true`  | Controls whether `*[image: figure — see source page]*` elements are masked when a parent or ancestor has the `ue-mask` class. When `true`, images inside masked containers are masked. When `false`, only images with the mask class directly on the element are masked. |

## Masking

The same CSS classes from UserExperior are compatible with the DevRev Plug SDK without modifications.

**Specific HTML elements**

To mask a div:

```
<div class="ue-mask">Hello World</div>
```

**Input elements**

To mask input text:

```
<input class="ue-input-mask"/>
```

To completely block the input element:

```
<input class="ue-block"/>
```

These classes ensure elements are masked or blocked as required.

### Image masking

By default, images inside a masked ancestor are also masked in session replays. For example, an `*[image: figure — see source page]*` inside a `<div class="ue-mask">` is replaced with a blank placeholder during recording.

```html
<div class="ue-mask">
  <img src="profile.jpg" alt="Profile" />
  <!-- This image is masked by default -->
</div>
```

To mask only images that have the mask class directly on the `*[image: figure — see source page]*` element, set `maskImagesByAncestor` to `false` in `sessionReplay` options:

```jsx
window.plugSDK.init({
  app_id: "<your_unique_app_id>",
  disable_plug_chat_window: true,
  session_recording_options: {
    sessionReplay: {
      maskImagesByAncestor: false,
    },
  },
});
```

With `maskImagesByAncestor: false`, only images with the mask class on the element itself are masked:

```html
<div class="ue-mask">
  <img src="profile.jpg" alt="Profile" />
  <!-- Not masked: no mask class on the image -->
</div>

<img class="ue-mask" src="profile.jpg" alt="Profile" />
<!-- Masked: mask class is on the image -->
```

Use `ue-unmask` on an image to exclude it from masking even when it sits inside a masked ancestor.

## User identification

  #### UserExperior implementation
    ```jsx

    // Setting a user identifier
    ue.setUserIdentifier('unique-user-identifier');

    // Passing user properties
    ue.setUserIdentifier('unique-user-identifier', {
     key1: value1,
     key2: value2,
     // ...
    });
    ```
  

  #### Replace with Plug
    DevRev introduces the concept of a `RevUser` object for enhanced user identity management. Use this to associate sessions with users and attach properties. For more details, refer to the [DevRev user identity](user-identity.md).
  

## Logging custom events

This approach facilitates custom event tracking, similar to the process in UserExperior, with additional capabilities.

  #### UserExperior implementation
    ```jsx

    ue.logEvent("YOUR_EVENT", {
        key1: value1,
        key2: value2,
        ...
    })
    ```
  

  #### Replace with Plug
    ```jsx

    window.plugSDK.trackEvent("YOUR_EVENT", {
        key1: value1,
        key2: value2,
        ...
    })
    ```
  

For more details, see the [Track events](track-events.md).

## Session attributes (User properties)

UserExperior allowed setting session-level properties but didn’t have a global user object. DevRev utilizes the `RevUser` object and `addSessionProperties()` for enhanced functionality.

For setting user properties, refer to the [User Identification](user-identity.md).

  #### UserExperior implementation
    ```jsx

    ue.setUserProperties({
        key1: value1,
        key2: value2,
        ...
    })
    ```
  

  #### Replace with Plug
    ```jsx
     
    window.plugSDK.addSessionProperties({
        key1: value1,
        key2: value2,
        ...
    })
    ```
  

## Restart a session

Terminate the current session recording and start a new one.

  #### UserExperior implementation
    ```jsx

     ue.restartSession();
    ```
  

  #### Replace with Plug
    ```jsx

    await window.plugSDK.shutdown();
    window.plugSDK.init({
       app_id: "<your_unique_app_id>",
       disable_plug_chat_window: true,
    });
    ```
