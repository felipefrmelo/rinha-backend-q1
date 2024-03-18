from contextlib import asynccontextmanager
from fastapi import FastAPI, Response

from rinha_de_backend.entrypoints.web.controller import Controller
from rinha_de_backend.entrypoints.web.data import Request
from pydantic import BaseModel


class CreateTransaction(BaseModel):
    valor: int
    descricao: str
    tipo: str


controller = Controller()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Setting up")
    await controller.setup()
    print("Set up")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/clientes/{user_id}/extrato")
async def get_transactions(user_id: int):
    request = Request(params={"user_id": user_id})
    response = await controller.get_transactions(request)
    return Response(content=response.body, status_code=response.status_code, media_type="application/json")


@app.post("/clientes/{user_id}/transacoes")
async def create_transaction(user_id: int, create_transaction: CreateTransaction):
    request = Request(params={"user_id": user_id},
                      body=create_transaction.model_dump())
    response = await controller.create_transaction(request)
    return Response(content=response.body, status_code=response.status_code, media_type="application/json")
