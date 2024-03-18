from rinha_de_backend.adapters.db import factory_pool
from rinha_de_backend.services.exceptions import UserNotFound
from rinha_de_backend.services.handlers import create_transaction
from rinha_de_backend.services.data import CreateTransaction
import pytest
import asyncio


def createDTO(value: int = 1000, description: str = 'test', type: str = 'c'):
    return CreateTransaction(value, description, type)


user_1 = 1
user_2 = 2


class FakeDatetime:
    def now(self):
        pass


@pytest.fixture
def datetime():
    return FakeDatetime()


@pytest.fixture
async def uow():
    factory_uow = await factory_pool('memory')
    return factory_uow()


@pytest.mark.parametrize("type, value, expected", [('d', 1000, 0),
                                                   ('c', 1000, 2000),
                                                   ('d', 2000, -1000),
                                                   ])
@pytest.mark.asyncio
async def test_create_transactions(type, value, expected,  datetime, uow):
    dto = createDTO(type=type, value=value)

    result = await create_transaction(await uow, datetime, dto, user_1)

    assert result.balance == expected
    assert result.limit == 1000


@pytest.mark.asyncio
async def test_create_transaction_in_two_users(uow, datetime):
    uow = await uow

    await create_transaction(uow, datetime, createDTO(type='c'), user_1)

    user = await uow.users.get(user_1)

    assert user.balance == 2000

    await create_transaction(uow, datetime, createDTO(type='d'), user_2)

    user = await uow.users.get(user_2)

    assert user.balance == 0


@pytest.mark.asyncio
async def test_concurrent_transactions(datetime, uow):
    uow = await uow
    dto = createDTO()
    n_transactions = 10

    user_before = await uow.users.get(user_1)

    async def create_task():
        await create_transaction(uow, datetime, dto, user_1)

    await asyncio.gather(*[create_task() for _ in range(n_transactions)])

    user = await uow.users.get(user_1)

    assert user.balance == user_before.balance + \
        1000 * n_transactions


@pytest.mark.asyncio
async def test_should_throw_exception_when_user_does_not_exist(uow, datetime):

    with pytest.raises(UserNotFound):
        await create_transaction(await uow, datetime, createDTO(), 1000)


@pytest.mark.asyncio
async def test_should_save_a_transaction(uow, datetime):
    uow = await uow

    dto = createDTO()

    await create_transaction(uow, datetime, dto, user_1)

    user = await uow.users.get(user_1)

    assert len(user.transactions) == 1
