Simple application to collect all Webex recordingIds and associated hostEmails and then download all recordings locally. This is meant to demonstrate the code logic for bulk downloading Webex Meeting recordings using the REST APIs.

It is a two step process which requires the app to be ran twice. 

On first run choose option 1 and provide your Webex site URL, for example *sitename.webex.com*, and enter the number of weeks you want to pull recordings for.
* This collects all recordingIds and hostEmails and stores them in the recordings.csv file.
* The app will terminate itself after completion. 

Run the app again choose option 2.
* This will download all recordings that were retrived from step 1 and save them to the "Downloaded-Recordings" folder.

--------------
**Setup**

Option 1:
- Login to the developer portal and copy your personal access token from https://developer.webex.com/docs/getting-started.
- When you first run the app it will ask you to provide the token you copied from the above page.
- This will allow the app to run for 12 hours as that is how long the personal access token is only valid for. You would need to login to the developer portal again to get a new personal access token if the current one has expired.

Option 2(this will allow the app to handle token refreshes): 
* Create an [Integration](https://developer.webex.com/docs/integrations) or [Service App](https://developer.webex.com/docs/service-apps) with the admin and compliance related recording scopes.
* Generate your access and refresh tokens
* Add your Client ID, Client Secret and Refresh Token to the [.env](.env) file. 
* You can also add your Access Token to the [token.json](token.json) file but the app will also ask you to enter one at first run if you haven't added it to the token.json file.

Start the app from terminal/command line:
* ``python recordings.py``
  
