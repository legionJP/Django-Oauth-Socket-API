from . import views
from django.urls import path
urlpatterns = [
    path('',views.Index, name='index'),
    path('<str:room_name>/',views.Chatspace,name='room')
]