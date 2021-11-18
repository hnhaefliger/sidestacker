from .urls import urlpatterns


async def websocket_application(scope, receive, send):
    for router in urlpatterns:
        match = router(scope, receive, send)

        if match:
            await match.start()

    else:
        await send({
            'type': 'websocket.disconnect'
        })
