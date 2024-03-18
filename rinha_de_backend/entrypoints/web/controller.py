from rinha_de_backend.adapters.db import factory_pool, type_db

from .exceptions import handle_exceptions
from .data import Request, Response

from ...adapters import DatetimeAdapter

from ...services.handlers import create_transaction, get_transactions
from ...services.data import CreateTransaction
from ...services.protocols import Datetime


class Controller:

    def __init__(self, datetime: Datetime = DatetimeAdapter()):
        self.datetime = datetime

    @handle_exceptions
    async def create_transaction(self, request: Request):
        dto = CreateTransaction(
            value=request.body['valor'], description=request.body['descricao'], type=request.body['tipo'])

        uow = self.factory_uow()

        body = await create_transaction(uow, self.datetime, dto, request.params['user_id'])

        return Response(status_code=200, body=body.to_json())

    @handle_exceptions
    async def get_transactions(self, request: Request):

        uow = self.factory_uow()

        body = await get_transactions(uow, self.datetime, request.params['user_id'])

        return Response(status_code=200, body=body.to_json())

    async def setup(self, db: type_db = 'pg'):
        self.factory_uow = await factory_pool(db)
        return self
