## Google Authentication Flow

### Setup and Installation
1. Install required packages:
    ```bash
    pip install django-allauth dj-rest-auth
    ```

2. Add `allauth` and `dj-rest-auth` to `INSTALLED_APPS` in `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...,
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'dj_rest_auth',
        'dj_rest_auth.registration',
        ...,
    ]
    ```

3. Configure the Google provider in `settings.py`:
    ```python
    SOCIALACCOUNT_PROVIDERS = {
        'google': {
            'SCOPE': [
                'profile',
                'email',
            ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
        }
    }
    SITE_ID = 1
    ```