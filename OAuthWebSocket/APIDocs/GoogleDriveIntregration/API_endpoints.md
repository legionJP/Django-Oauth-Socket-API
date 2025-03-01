
### Google Drive Endpoints
1. **Google Drive Download Endpoint:**

# 1. Authentication Initializer:

#### 1.  http://127.0.0.1:8000/google/authenticate/

#### 2. http://127.0.0.1:8000/google/upload/

#### 3. http://127.0.0.1:8000/google/download/{file_id}

    ```python
    import io
    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.decorators import api_view
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    @csrf_exempt
    @api_view()
    def google_drive_download(request, file_id):
        if 'credentials' not in request.session:
            return redirect('google_drive_auth')

        credentials = Credentials(**request.session['credentials'])
        service = build('drive', 'v3', credentials=credentials)

        file = service.files().get(fileId=file_id).execute()
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        fh.seek(0)
        
        # Save file locally
        with open(file['name'], 'wb') as f:
            f.write(fh.read())

        response = HttpResponse(fh.read(), content_type=file['mimeType'])
        response['Content-Disposition'] = f'attachment; filename="{file["name"]}"'
        return response
    ```