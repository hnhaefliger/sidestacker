import uuid
from asgiref.sync import sync_to_async

# we need to load all django modules before importing any models
import django
django.setup()

from .models import Game

global GAMESTATES
GAMESTATES = {}

class Connection:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.listen = receive
        self.transfer = send
        self.joined = False

    async def start(self):
        while True:
            event = await self.listen()

            if event['type'] == 'websocket.connect':
                await self.connect()

            if event['type'] == 'websocket.disconnect':
                await GAMESTATES[self.game_id].end()
                break

            if event['type'] == 'websocket.receive':
                await self.receive(event['text'])

    async def accept(self):
        await self.transfer({
            'type': 'websocket.accept'
        })

    async def send(self, data):
        return await self.transfer({
            'type': 'websocket.send',
            'text': data,
        })

    async def connect(self):
        await self.accept()
        self.game_id = self.scope['path'].replace('/', '')

        if self.game_id != '':
            if self.game_id in GAMESTATES:
                self.joined = await GAMESTATES[self.game_id].join(self)
            
        if not self.joined:
            self.game_id = str(uuid.uuid4())
            new_game = GameState(self.game_id)
            self.joined = await new_game.join(self)
            GAMESTATES[self.game_id] = new_game

    async def receive(self, data):
        await GAMESTATES[self.game_id].move(self, data)

    async def disconnect(self):
        try:
            await self.send('end')
            await self.transfer({
                'type': 'websocket.close',
            })

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

    async def join(self, player):
        if not self.white:
            self.white = player
            await self.white.send('wait|' + self.game_id)
            return True

        elif not self.black:
            self.black = player
            await self.send('start')
            return True

        else:
            return False

    async def send(self, message): 
        await self.white.send(message)
        await self.black.send(message)

    async def move(self, player, move):
        if (self.black != None) & (self.white != None):
            x, y = int(move[1]), int(move[0])

            if (0 <= x and x < 2) and (0 <= y and y < 7):
                if ((player == self.black) and (self.turn == 'black')) or ((player == self.white) and (self.turn == 'white')):
                    self.moves += move
                    
                    if x == 0:
                        for i in range(7):
                            if self.board[y][i] == '':
                                self.board[y][i] = self.turn
                                break

                    else:
                        for i in range(1, 8):
                            if self.board[y][-i] == '':
                                self.board[y][-i] = self.turn
                                break

                    await self.send('move|' + move + self.turn)
                    self.turn = 'white' if self.turn == 'black' else 'black'

    async def end(self):
        if not self.ended:
            self.ended = True

            if self.white != None:
                await self.white.disconnect()

            if self.black != None:
                await self.black.disconnect()

            if self.moves != '':
                await sync_to_async(self.save_game)()

            del GAMESTATES[self.game_id]

    def save_game(self):
        print(self.moves)

        Game(
            game_id=self.game_id,
            moves=self.moves,
            winner=self.winner,
        ).save()
