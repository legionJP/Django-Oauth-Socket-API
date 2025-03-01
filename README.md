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

1. Configure ASGI
2. Create the Consumers or Channels 
3. Routing 
4. WebSockets API to initate the Handshakes

##  consumer that accepts WebSocket connections on the path /ws/chat/ROOM_NAME/ that takes any message it receives on the WebSocket and echos it back to the same WebSocket.
## path prefix like /ws/ to distinguish WebSocket connections

- the ProtocolTypeRouter will first inspect the type of connection. If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack

-  AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. (Scopes will be discussed later in this tutorial.) Then the connection will be given to the URLRouter.

# Enable a channel layer
A channel layer provides the following abstractions:

- A channel layer is a kind of communication system. It allows multiple consumer instances to talk with each other, and with other parts of Django.

- A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.

- A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.
```py
$ python3 manage.py shell
import channels.layers
channel_layer = channels.layers.get_channel_layer()
from asgiref.sync import async_to_sync
async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
async_to_sync(channel_layer.receive)('test_channel')
{'type': 'hello'}

```
# DB for the WebSocket
The Django ORM is a synchronous piece of code, and so if you want to access it from asynchronous code you need to do special handling to make sure its connections are closed properly

If you are writing asynchronous code, however, you will need to call database methods in a safe, synchronous context, using database_sync_to_async or by using the asynchronous methods prefixed with a like Model.objects.aget().