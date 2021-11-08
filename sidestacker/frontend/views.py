from django.shortcuts import render


def index(request):
    return render(request, 'frontend/index.html')

def game(request, game_id=''):
    return render(request, 'frontend/game.html', {
        'game_id': game_id
    })
