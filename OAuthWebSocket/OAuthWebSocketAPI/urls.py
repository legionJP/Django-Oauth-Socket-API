from django.urls import path
from . import views 

urlpatterns=[
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('api/auth/', views.Oauth, name='Oauth'),
    path('api/google-callback/', views.google_callback, name='google-callback'),
    # path('api/gdrive/authenticate',views),
    path('google/authenticate/', views.google_drive_auth, name='google_drive_auth'),
    path('google/auth/callback/', views.google_drive_callback, name='google_drive_callback'),
    path('google/download/<str:file_id>/',views.google_drive_download, name='google_drive_download'),
    path('google/upload/', views.google_drive_upload, name='google_drive_upload'),
    path('google/list/', views.google_drive_list, name='google_drive_list'),



] 