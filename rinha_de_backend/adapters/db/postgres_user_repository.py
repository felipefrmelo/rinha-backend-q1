import os
from typing import AsyncGenerator


from ...services.protocols import Datetime, UnitOfWork
from ...domain.entities import User
from ...services.data import BalanceView, TransactionView
from contextlib import asynccontextmanager
from asyncpg import Connection
import asyncpg


class PostgresUserRepository:

    def __init__(self, connection: Connection):
        self.connection = connection

    async def save(self, user: User):
        await self.connection.execute(
            "UPDATE clientes SET saldo = $1 WHERE id = $2",
            user.balance,
            user.id
        )
        transaction = user.transactions[0]
        await self.connection.execute(
            "INSERT INTO transacoes (cliente_id, valor, descricao, tipo, realizada_em) VALUES ($1, $2, $3, $4, $5)",
            user.id,
            transaction.value,
            transaction.description,
            transaction.type,
            transaction.created_at,
        )

    async def get(self, user_id: int):
        row = await self.connection.fetchrow(
            "SELECT nome, saldo, limite FROM clientes WHERE id = $1", user_id
        )
        if row is not None:
            return User(user_id, row["nome"], row["limite"], row["saldo"])

    @asynccontextmanager
    async def lock(self, user_id: int) -> AsyncGenerator[None, None]:
        async with self.connection.transaction():
            await self.connection.execute(
                'SELECT pg_advisory_xact_lock($1)', user_id)
            yield

    async def view(self, user_id: int, datetime: Datetime):

        if row := await self.connection.fetchrow(
                "SELECT nome, saldo, limite FROM clientes WHERE id = $1", user_id):

            transaction = await self.connection.fetch(
                "SELECT valor, descricao, tipo, realizada_em FROM transacoes WHERE cliente_id = $1 ORDER BY realizada_em DESC LIMIT 10",
                user_id
            )

            transaction = [
                TransactionView(
                    t["valor"], t["realizada_em"], t["descricao"], t["tipo"]
                ) for t in transaction
            ]

            return BalanceView(row["saldo"], datetime.now(), row["limite"], transaction)


class PostgresUnitOfWork(UnitOfWork):

    def __init__(self, pool):

        self._pool = pool

    async def __aenter__(self):
        self.connection = await self._pool.acquire()
        self.users = PostgresUserRepository(self.connection)

    async def __aexit__(self, *_):
        await self._pool.release(self.connection)


def create_asyncpg_pool():
    return asyncpg.create_pool(
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "123"),
        database=os.getenv("POSTGRES_DB", "rinha"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        max_size=int(os.getenv("POSTGRES_MAX_CONNECTIONS", 10)),
        min_size=int(os.getenv("POSTGRES_MIN_CONNECTIONS", 10)),
    )
