from django.db import models


class Game(models.Model):
    game_id = models.CharField(max_length=36, unique=True)
    moves = models.CharField(max_length=7 * 7 * 2)
    winner = models.CharField(max_length=5)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.winner
    