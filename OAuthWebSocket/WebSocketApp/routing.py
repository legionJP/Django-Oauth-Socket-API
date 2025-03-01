from django.urls import re_path
from . import consumers

websocket_urlpatterns=[
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

]

'''

The next step is to point the main ASGI configuration at the chat.routing module.
 In mysite/asgi.py, import AuthMiddlewareStack, URLRouter, 
and chat.routing; and insert a 'websocket' key in the ProtocolTypeRouter
'''

# (use re_path() due to limitations in URLRouter.)
'''
We call the as_asgi() classmethod in order to get an 
ASGI application that will instantiate an instance of our consumer for 
each user-connection. This is similar to Django’s as_view()

'''