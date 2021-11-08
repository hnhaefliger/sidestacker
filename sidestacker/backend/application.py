from .connection import Connection

async def websocket_application(scope, receive, send):
    connection = Connection(scope, receive, send)
    await connection.start()
