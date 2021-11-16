from django.shortcuts import render
from backend.models import Game


def index(request):
    return render(request, 'frontend/index.html')


def game(request, game_id=''):
    return render(request, 'frontend/game.html', {
        'game_id': game_id
    })


def replay(request, game_id=''):
    try:
        game = Game.objects.get(game_id=game_id).moves

    except:
        game = 'invalid'
        
    return render(request, 'frontend/replay.html', {
        'game': game
    })
