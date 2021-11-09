import uuid

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
                await self.disconnect()
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
        # end game
        pass


class GameState:
    def __init__(self, game_id):
        self.game_id = game_id
        self.black = None
        self.white = None
        self.board = [['' for i in range(7)] for j in range(7)]
        self.moves = ''
        self.turn = 'white'

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
            # check legal move

            self.moves += move

            if (player == self.black) & (self.turn == 'black'):
                await self.send('move|' + move + 'black')
                self.turn = 'white'

            elif (player == self.white) & (self.turn == 'white'):
                await self.send('move|' + move + 'white')
                self.turn = 'black'

            # check winner

            # if winner save game and disconnect
