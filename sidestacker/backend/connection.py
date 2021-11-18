class Connection:
    def __init__(self, scope, receive, send, handler, *args, **kwargs):
        self.scope = scope
        self.transfer = send
        self.receive = receive
        self.handler = handler(*args, **kwargs)

    async def send(self, message):
        await self.transfer(message)

    async def accept(self):
        await self.send({
            'type': 'websocket.accept',
        })

    async def start(self):
        while True:
            event = await self.receive()

            if event['type'] == 'websocket.connect':
                await self.handler.connect(self)

            elif event['type'] == 'websocket.disconnect':
                await self.handler.disconnect(self)
                await self.send({
                    'type': 'websocket.close',
                })

            elif event['type'] == 'websocket.receive':
                await self.handler.receive(self, event['text'])