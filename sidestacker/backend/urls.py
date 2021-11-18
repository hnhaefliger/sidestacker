from .game import LogicHandler
from .routing import socket_path

urlpatterns = [
    socket_path('', LogicHandler),
    socket_path('<str:game_id>', LogicHandler),
]
