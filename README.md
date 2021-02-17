## Project work for course **TJTS5901**

Made by Aleksi, Hoa, Juha and Markus (Group 16)


Access to Application: http://nodal-figure-301713.ew.r.appspot.com/

Access to admin interface: http://nodal-figure-301713.ew.r.appspot.com/admin

---

## Reporting issues

1. Click the link below these instructions
2. Write a descriptive title for the issue (e.g. "Application crashes when trying to delete a suggestion")
3. Set issue type to "Issue" (default)
4. Choose issue template "Bug" if you are reporting a bug. For security related issues the "Security" template should be used.
5. Follow the templates instructions under each applicable header
6. If you are reporting a **security issue, always mark the issue as confidental**. Use your judgment whether to report bug as confidental.
7. Proofread your issue
8. Click the "Submit issue" button
9. Thank you for your service! You may be asked further questions about the issue you submitted once we start working on it. Please, answer them.

[Report an issue](https://gitlab.jyu.fi/beeware/beemapbeeware/-/issues/new).

## Short Setup

1. Clone this repo
`git clone https://gitlab.jyu.fi/beeware/beemapbeeware.git`

2. Install dependencies
`pip install -r requirements.txt`

3. Setup your Google Application Credentials: [Setup Link](https://cloud.google.com/docs/authentication/getting-started?hl=de)

4. Setup an instance-configuration file, where some variables are specified
    - flask secret key (needed for hashing in the application)
    - environment (not mandatory)
    - APPLICATIONINSIGHTS_CONNECTION_STRING (-> That one is for Azure logging)


5. Start Application
`python main.py`
