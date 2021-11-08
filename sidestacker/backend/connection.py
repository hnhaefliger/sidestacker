class Connection:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.listen = receive
        self.transfer = send

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
        if self.scope['path'] != '/':
            # try to join game
            pass

            # possibly start game

        else:
            # create new game
            pass

        await self.accept()

    async def receive(self, data):
        print(data)
        await self.send('hello')

    async def disconnect(self):
        # end game
        pass
