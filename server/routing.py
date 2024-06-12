from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import DataConsumer

websocket_urlpatterns = [
    path('ws/', DataConsumer.as_asgi()),
]