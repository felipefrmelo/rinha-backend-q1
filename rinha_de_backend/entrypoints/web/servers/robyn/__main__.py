import os
from robyn import Robyn
from orjson import loads
from robyn.argument_parser import Config

from rinha_de_backend.entrypoints.web.data import Request
from ...controller import Controller


class SpecialConfig(Config):
    def __init__(self):
        super().__init__()
        self.workers = 2
        self.processes = 1
        self.log_level = "WARN"


app = Robyn(__file__, config=SpecialConfig())


async def startup_handler():
    global controller
    controller = await Controller().setup()


app.startup_handler(startup_handler)


@app.post("/clientes/:user_id/transacoes")
async def create_transaction(request):
    user_id = int(request.path_params.get("user_id"))
    body = loads(request.body)
    response = await controller.create_transaction(Request(params={"user_id": user_id}, body=body))
    return {
        "status_code": response.status_code,
        "description": response.body,
        "headers": {"Content-Type": "application/json"},
    }


@app.get("/clientes/:user_id/extrato")
async def get_transactions(request):
    user_id = int(request.path_params.get("user_id"))

    response = await controller.get_transactions(Request(params={"user_id": user_id}))
    return {
        "status_code": response.status_code,
        "description": response.body,
        "headers": {"Content-Type": "application/json"},
    }

app.start(port=int(os.getenv("PORT", 3000)), host="0.0.0.0")
