# Django-Oauth-Socket-API
Django Project assesment for API end Point to Intregrate Google Auth, Google drive, WebSocket 



# 1. Google Authentication Flow:
- Immplemented the Google Auth api endpint using the django-allauth
- pip install django-allauth dj-rest-auth

    -  ### API endpoint: GET,  [POST] redirected by google
    http://127.0.0.1:8000/accounts/google/login/

    - ###  Endpoint where google sends the auth data
        - http://127.0.0.1:8000/accounts/google/login/callback/

- "GET /accounts/google/login/callback/?state=----J-_serinfo.profile HTTP/1.1" 302 0
    - The GET request to the callback URL includes this authorization code and the state parameter.

   - ### API Endpoint to return the received Data
        - http://127.0.0.1:8000/api/google-callback/

# 2. Google Drive Integration
. Develop an endpoint that allows users to connect their Google Drive.
· Implement functionality for users to upload files to their Google Drive.
. Provide an option to fetch and download files locally from Google Drive.

 - # Libraries for the google auth and picker drvier 
- pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 3. WebSocket for User Chat
· Implement a WebSocket that enables real-time chat between two pre-
configured users.
. Ensure that messages are sent and received in real-time.