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


# 2. Google Drive Integrations :
