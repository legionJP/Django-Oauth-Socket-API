import io
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from allauth.socialaccount.models import SocialAccount
from rest_framework import status
# Create your views here.

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect("/")

@api_view()
def Oauth(request):
    return render(request, 'auth.html')
    #return HttpResponse(template_name='home.html')            

@api_view()
@login_required
def google_callback(request):
    user = request.user
    try:
        social_account = SocialAccount.objects.get(user=user,provider='google')
        profile_data= social_account.extra_data

        auth_data = {
            'profile_data':profile_data,
            'first_name': profile_data.get('given_name'),
            'last_name': profile_data.get('family_name'),
            'email': profile_data.get('email')
        }
        return Response(auth_data)
    except SocialAccount.DoesNotExist:
        return Response({"message": "Account Not Found for the User"},status=status.HTTP_404_NOT_FOUND)
    
# Google Drive APIs

import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
logger =logging.getLogger(__name__)


# scopes for google drive 
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/drive'
]
# client secrets file.
CLIENT_SECRETS_FILE= "C:/Users/jjpsi/Projects_Repos_Notes/90NorthAssesment/Django-Oauth-Socket-API/OAuthWebSocket/credentials.json"

@api_view()
def google_drive_auth(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://127.0.0.1:8000/google/auth/callback/'

    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    logger.debug(f'Stored state in session: {state}')
    logger.debug(f'Session contents after storing state: {dict(request.session)}')
    return redirect(authorization_url)

@api_view()
def google_drive_callback(request):
    state = request.session.get('state')
    # if state is None:
    #     logger.error("State Parameter is Missiing")
    #     return Response({'error':'State pram is missing'}, status=400)
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri= request.build_absolute_uri('/google/auth/callback/')
    # flow.fetch_token(authorization_response=request.get_full_path())
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    return redirect('google_drive_upload')
  

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

@csrf_exempt
@api_view(['POST','GET'])
def google_drive_upload(request):
    if 'credentials' not in request.session:
        return redirect('google_drive_auth')
    
    credentials = Credentials(**request.session['credentials'])
    service = build('drive', 'v3', credentials=credentials)

    if request.method == 'POST':
        file = request.FILES['file']
        file_metadata = {'name': file.name}
        file_io = io.BytesIO(file.read())
        media = MediaIoBaseUpload(file_io, mimetype=file.content_type,resumable=True)
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return HttpResponse('File uploaded successfully.')
    return render(request, 'upload.html')


# List all the files: 
@csrf_exempt
@api_view(['GET'])
def google_drive_list(request):
    if 'credentials' not in request.session:
        return redirect('google_drive_auth')
    credentials = Credentials(**request.session['credentials'])
    service = build('drive', 'v3', credentials=credentials)

    # List files 
    results = service.files().list(fields="files(id, name, mimeType)").execute()
    files= results.get('files',[])
    context ={
        'files':files
    }
    return render(request, 'list_download.html',context)

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
    with open(file['name'],'wb') as f:
        f.write(fh.read())

    response = HttpResponse(fh.read(), content_type=file['mimeType']) # retrun file to download
    response['Content-Disposition'] = f'attachment; filename="{file["name"]}"'

    return response