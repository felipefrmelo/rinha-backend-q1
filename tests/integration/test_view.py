
from datetime import datetime
import pytest
from sqlalchemy import text
from rinha_de_backend.services.data import CreateTransaction
from rinha_de_backend.services.exceptions import UserNotFound
from rinha_de_backend.services.handlers import create_transaction, get_transactions
from orjson import dumps

from rinha_de_backend.adapters.db import factory_pool


class FakeDatetime:

    def now(self):
        return datetime(2024, 1, 1)


user_1 = 1


@pytest.fixture
async def uow():
    factory_uow = await factory_pool('SQLAlchemy')
    uow = factory_uow()
    async with uow:
        if "connection" in dir(uow):
            await uow.connection.execute("DELETE FROM transacoes")
        if "async_session" in dir(uow):
            await uow.users.delete_all_transactions()

    return uow


@pytest.mark.asyncio
async def test_should_return_a_view(uow):
    uow = await uow

    async with uow:
        user = await uow.users.get(user_1)

    if user is None:
        raise Exception("User not found")

    view = await get_transactions(uow, FakeDatetime(), user_1)

    assert view.to_json() == dumps({
        "saldo": {
            "total": user.balance,
            "data_extrato": "2024-01-01",
            "limite": user.limit
        },
        "ultimas_transacoes": []
    })


async def create_transactions(uow, n):
    for value in range(1, 1 + n):
        dto = CreateTransaction(value, "test", "c")
        await create_transaction(uow, FakeDatetime(), dto, user_1)


@pytest.mark.asyncio
async def test_should_return_a_view_with_transactions(uow):
    uow = await uow

    await create_transactions(uow, 2)

    async with uow:
        user = await uow.users.get(user_1)

    if user is None:
        raise Exception("User not found")

    view = await get_transactions(uow, FakeDatetime(), user_1)

    assert view.to_json() == dumps({
        "saldo": {
            "total": user.balance,
            "data_extrato": "2024-01-01",
            "limite": user.limit
        },
        "ultimas_transacoes": [
            {
                "valor": 1,
                "data": "2024-01-01",
                "descricao": "test",
                "tipo": "c"
            },
            {
                "valor": 2,
                "data": "2024-01-01",
                "descricao": "test",
                "tipo": "c"
            }
        ]
    })


@pytest.mark.asyncio
async def test_should_raise_user_not_found_exception(uow):
    uow = await uow
    with pytest.raises(UserNotFound):
        await get_transactions(uow, FakeDatetime(), 1000)


@pytest.mark.asyncio
async def test_benchmark(uow):
    uow = await uow

    await create_transactions(uow, 100)

    async def mean_duration():
        n = 50
        start = datetime.now()
        for _ in range(n):
            await get_transactions(uow, FakeDatetime(), user_1)
        end = datetime.now()
        return (end - start).total_seconds() * 1000 / n

    duration_ms = await mean_duration()
    assert duration_ms < 0.5
