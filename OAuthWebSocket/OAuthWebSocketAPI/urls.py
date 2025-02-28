from django.urls import path
from . import views 

urlpatterns=[
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('api/auth/', views.Oauth, name='Oauth'),
    path('api/google-callback/', views.google_callback, name='google-callback')
]