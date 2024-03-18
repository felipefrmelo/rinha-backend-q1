from collections import defaultdict
from typing import AsyncGenerator

from rinha_de_backend.services.data import BalanceView, TransactionView

from ...services.protocols import UnitOfWork

from ...domain.entities import User
import copy
import asyncio
from contextlib import asynccontextmanager


class InmemoryConnection:

    MILLISECOND = 0.001

    def __init__(self):
        self.locks = defaultdict(asyncio.Lock)
        self.users = {
            i: User(i, f"a_{i}", 1000, 1000) for i in range(1, 6)
        }

    def get_lock(self, user_id: int):
        return self.locks[user_id]

    async def sleep(self, t=MILLISECOND):
        await asyncio.sleep(t)

    async def get(self, user_id: int):
        await self.sleep()
        return copy.copy(self.users.get(user_id))

    async def save(self, user: User):
        await self.sleep()
        self.users[user.id] = user


class InMemmoryUserRepository:
    def __init__(self, connection: InmemoryConnection):
        self.connection = connection

    async def save(self, user: User):
        await self.connection.save(user)

    async def get(self, user_id: int):
        return await self.connection.get(user_id)

    @asynccontextmanager
    async def lock(self, user_id: int) -> AsyncGenerator[None, None]:
        async with self.connection.get_lock(user_id):
            yield

    async def view(self, user_id: int, datetime):

        if user := await self.get(user_id):
            transactions = [TransactionView(t.value, t.created_at, t.description, t.type)
                            for t in user.transactions][::-1]
            return BalanceView(user.balance, datetime.now(), user.limit, transactions)


class InMemmoryUnitOfWork(UnitOfWork):

    def __init__(self, in_memory_connection: InmemoryConnection):
        self.users = InMemmoryUserRepository(in_memory_connection)
