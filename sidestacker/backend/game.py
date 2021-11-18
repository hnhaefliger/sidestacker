import uuid
from .connection import Connection

# we need to load all django modules before importing any models
import django
django.setup()

from .models import Game

global GAMESTATES
GAMESTATES = {}


class LogicHandler(Connection):
    def __init__(self, game_id=''):
        self.joined = False
        self.game_id = game_id

    def connect(self):
        self.accept()

        if self.game_id != '':
            if self.game_id in GAMESTATES:
                self.joined = GAMESTATES[self.game_id].join(self)
            
        if not self.joined:
            self.game_id = str(uuid.uuid4())
            new_game = GameState(self.game_id)
            self.joined = new_game.join(self)
            GAMESTATES[self.game_id] = new_game

    def receive(self, data):
        GAMESTATES[self.game_id].move(self, data)

    def disconnect(self):
        try:
            self.send('end')
            self.close()

        except:
            pass

        del self

    
class GameState:
    def __init__(self, game_id):
        self.game_id = game_id
        self.black = None
        self.white = None
        self.board = [['' for i in range(7)] for j in range(7)]
        self.moves = ''
        self.turn = 'white'
        self.winner = 'none'
        self.ended = False

    def join(self, player):
        if not self.white:
            self.white = player
            self.white.send('wait|' + self.game_id)
            return True

        elif not self.black:
            self.black = player
            self.send('start')
            return True

        else:
            return False

    def send(self, message): 
        self.white.send(message)
        self.black.send(message)

    def move(self, player, move):
        if (self.black != None) & (self.white != None):
            x, y = int(move[1]), int(move[0])

            if (0 <= x and x < 2) and (0 <= y and y < 7):
                if ((player == self.black) and (self.turn == 'black')) or ((player == self.white) and (self.turn == 'white')):
                    self.moves += move

                    position = [0, y]
                    
                    if x == 0:
                        for i in range(7):
                            if self.board[y][position[0]] == '':
                                break

                            position[0] += 1

                    else:
                        position[0] = len(self.board[y]) - 1
                        for i in range(1, 8):
                            if self.board[y][-i] == '':
                                break

                            position[0] -= 1

                    self.board[position[1]][position[0]] = self.turn

                    self.send('move|' + move + self.turn)

                    if check_win(self.board, position[0], position[1]):
                        self.winner = self.turn
                        self.send('win|' + self.turn)
                        self.end()

                    self.turn = 'white' if self.turn == 'black' else 'black'

    def end(self):
        if not self.ended: # prevent occasional duplicate calls because of both sockets
            self.ended = True

            if self.white != None:
                self.white.disconnect()

            if self.black != None:
                self.black.disconnect()

            if self.moves != '':
                self.save_game()

            del GAMESTATES[self.game_id]


    def save_game(self):
        Game(
            game_id=self.game_id,
            moves=self.moves,
            winner=self.winner,
        ).save()


def check_win(board, x, y):
    a, b = max((0, x-3)), min((6, x+3)) + 1
    c, d = max((0, y-3)), min((6, y+3)) + 1

    line = 0

    # Horizontal
    for i in range(b - a):
        if board[y][x] == board[y][a+i]:
            line += 1

            if line == 4:
                return True

        else:
            line = 0

    line = 0

    # Vertical
    for i in range(d - c):
        if board[y][x] == board[c+i][x]:
            line += 1

            if line == 4:
                return True

        else:
            line = 0

    line = 0

    # Diagonal 1
    for i in range(min([b - a, d - c])):
        if board[y][x] == board[c+i][a+i]:
            line += 1

            if line == 4:
                return True

        else:
            line = 0

    line = 0

    # Diagonal 2
    for i in range(min([b - a, d - c])):
        if board[y][x] == board[c+i][b-i-2]:
            line += 1

            if line == 4:
                return True

        else:
            line = 0

    return False
