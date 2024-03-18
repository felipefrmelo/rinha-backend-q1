from typing import Callable, Literal

from rinha_de_backend.adapters.db.sql_alchey_user_repository import SqlAlchemyUnitOfWork, create_asyncpg_engine
from .in_memmory_user_repository import InMemmoryUnitOfWork, InmemoryConnection
from ...services.protocols import UnitOfWork
from .postgres_user_repository import PostgresUnitOfWork, create_asyncpg_pool
from datetime import datetime, timezone


class DatetimeAdapter:

    def now(self):
        return datetime.now(timezone.utc)


type_db = Literal['pg', 'memory', 'SQLAlchemy']


async def factory_pool(db: type_db = 'pg') -> Callable[[], UnitOfWork]:

    match db:
        case 'pg':
            pool = await create_asyncpg_pool()
            return lambda: PostgresUnitOfWork(pool)

        case 'memory':
            in_memory = InmemoryConnection()
            return lambda: InMemmoryUnitOfWork(in_memory)

        case 'SQLAlchemy':
            pool = create_asyncpg_engine()
            return lambda: SqlAlchemyUnitOfWork(pool)

        case _:
            raise Exception("Invalid db")
