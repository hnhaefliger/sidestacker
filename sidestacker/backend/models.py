from django.db import models

# Create your models here.

class Game:
    moves = models.CharField(max_length=7 * 7 * 2)
    winner = models.CharField(max_length=5)
    