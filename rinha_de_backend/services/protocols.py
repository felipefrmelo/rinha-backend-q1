from abc import ABC
from datetime import datetime
from typing import AsyncGenerator, Protocol
from contextlib import asynccontextmanager

from rinha_de_backend.services.data import BalanceView

from ..domain.entities import User


class Datetime(Protocol):

    def now(self) -> datetime:
        ...


class UserRepository(Protocol):

    async def save(self, user):
        ...

    async def get(self, user_id) -> User | None:
        ...

    @asynccontextmanager
    async def lock(self, user_id) -> AsyncGenerator[None, int]:
        ...

    async def view(self, user_id, datetime: Datetime) -> BalanceView | None:
        ...


class UnitOfWork(ABC):
    users: UserRepository

    async def __aenter__(self):
        ...

    async def __aexit__(self, *_):
        ...
