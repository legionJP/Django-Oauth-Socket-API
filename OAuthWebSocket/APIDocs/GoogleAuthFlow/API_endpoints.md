#
## Google Auth Endpoints

1. **Google Login Endpoint:**
    - **API endpoint:** `GET`, `POST` redirected by Google
    - URL: `http://127.0.0.1:8000/accounts/google/login/`

2. **Google Callback Endpoint:**
    - **Endpoint where Google sends the auth data**
    - URL: `http://127.0.0.1:8000/accounts/google/login/callback/`

3. **Google Callback Data Endpoint:**
    - **API Endpoint to return the received Data**
    - URL: `http://127.0.0.1:8000/api/google-callback/`
