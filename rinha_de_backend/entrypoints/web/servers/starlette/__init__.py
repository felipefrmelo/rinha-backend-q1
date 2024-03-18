from typing import AsyncIterator
from starlette.applications import Starlette
from starlette.routing import Route
from contextlib import asynccontextmanager
from starlette.responses import Response

from ...data import Request
from ...controller import Controller

controller = Controller()

@asynccontextmanager
async def lifespan(_: Starlette) -> AsyncIterator[None]:
    print("Starting up starlette server...")
    await controller.setup()
    yield


async def get_body(request):
    if request.method == "POST":
        return await request.json()
    return {}


def adapter(handler):
    async def wrapper(request):
        params = request.path_params
        body = await get_body(request)
        response = await handler(Request(params=params, body=body))
        return Response(status_code=response.status_code, content=response.body)
    return wrapper




routes = [
    Route("/clientes/{user_id:int}/extrato", adapter(controller.get_transactions) , methods=["GET"]),
    Route("/clientes/{user_id:int}/transacoes", adapter(controller.create_transaction), methods=["POST"]),
]


app = Starlette(routes=routes, lifespan=lifespan, debug=False)

