from asgiref.sync import sync_to_async, async_to_sync


class Connection:
    def __init__(self):
        pass


    def setup(self, scope, receive, send):
        self.scope = scope
        self.ws_send = async_to_sync(send)
        self.ws_receive = receive


    async def start(self):
        while True:
            event = await self.ws_receive()

            if event['type'] == 'websocket.connect':
                await sync_to_async(self.connect)()

            elif event['type'] == 'websocket.disconnect':
                await sync_to_async(self.disconnect)()

            elif event['type'] == 'websocket.receive':
                await sync_to_async(self.receive)(event['text'])

    
    def accept(self):
        self.ws_send({
            'type': 'websocket.accept'
        })


    def connect(self):
        self.accept()

    
    def receive(self, data):
        pass

    
    def send(self, message):
        self.ws_send({
            'type': 'websocket.send',
            'text': message
        })


    def disconnect(self):
        pass

    def close(self):
        self.send({
            'type': 'websocket.close',
        })
