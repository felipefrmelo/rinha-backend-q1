from ...data import Request, Response
from ...controller import Controller
from .router import Router
from orjson import loads


async def setup():
    global routes
    controller = await Controller().setup()

    print('Setting up routes...')
    routes = [
        Router('/clientes/{user_id:int}/extrato',
               'GET', controller.get_transactions),
        Router('/clientes/{user_id:int}/transacoes',
               'POST', controller.create_transaction),
    ]


routes: list


async def JsonResponse(send, response):
    await send({
        'type': 'http.response.start',
        'status': response.status_code,
        'headers': [
            [b'content-type', b'application/json'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': response.body,
        'more_body': False
    })


async def handle_404(send):
    content = b'Not found'
    await JsonResponse(send, Response(404, content))


def get_router(scope):
    for router in routes:
        if router.match(scope['path'], scope['method']):
            return router


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """

    message = await receive()
    body = message.get('body', b'')

    return loads(body if body else b'{}')


async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        message = await receive()
        if message['type'] == 'lifespan.startup':
            print('Starting up asgi server ...')
            await setup()
            print('Started up!')
            await send({'type': 'lifespan.startup.complete'})

            return

    router = get_router(scope)

    if not router:
        await handle_404(send)
        return

    request_body = await read_body(receive) if scope['method'] == 'POST' else {}
    request = Request(params=router.get_params(scope['path']), body=request_body)
    response = await router.handler(request)

    await JsonResponse(send, response)
