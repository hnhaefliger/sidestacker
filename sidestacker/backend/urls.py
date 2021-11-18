from .game import LogicHandler
from .routing import socket_path

urlpatterns = [
    socket_path('/<str:game_id>/', LogicHandler),
    socket_path('', LogicHandler),
]
