from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game', views.game, name='game'),
    path('game/', views.game, name='game'),
    path('game/<str:game_id>', views.game, name='game'),
    path('replay/<str:game_id>', views.replay, name='replay'),
]
