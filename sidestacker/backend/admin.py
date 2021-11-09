from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    fields = ('id', 'game_id', 'moves', 'winner', 'time')
    readonly_fields = ('id', 'game_id', 'moves', 'winner', 'time')

    def id(self, obj): return obj.id
    def game_id(self, obj): return obj.game_id
    def moves(self, obj): return obj.moves
    def winner(self, obj): return obj.winner
    def time(self, obj): return obj.time


admin.site.register(Game, GameAdmin)
