from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, text, update, insert, desc
import os

from sqlalchemy import String, INT, DATETIME


from ...services.protocols import Datetime, UnitOfWork
from ...domain.entities import User
from ...services.data import BalanceView, TransactionView
from contextlib import asynccontextmanager

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = 'clientes'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    saldo: Mapped[int] = mapped_column(INT, nullable=False)
    limite: Mapped[int] = mapped_column(INT, nullable=False)

    def to_domain(self):
        return User(id=self.id, name=self.nome, limit=self.limite, balance=self.saldo)


class Transacao(Base):
    __tablename__ = 'transacoes'

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(INT, nullable=False)
    valor: Mapped[int] = mapped_column(INT, nullable=False)
    tipo: Mapped[str] = mapped_column(String(1), nullable=False)
    descricao: Mapped[str] = mapped_column(String(10), nullable=False)
    realizada_em: Mapped[datetime] = mapped_column(
        DATETIME(timezone=True), nullable=False)

    def to_view(self):
        return TransactionView(self.valor, self.realizada_em,
                               self.descricao, self.tipo)


class PostgresUserRepository:

    def __init__(self, session:  AsyncSession):
        self.session = session

    async def save(self, user: User):
        await self.session.execute(
            update(Cliente).
            where(Cliente.id == user.id).
            values(saldo=user.balance)
        )
        transaction = user.transactions[0]
        await self.session.execute(
            insert(Transacao).
            values(cliente_id=user.id, valor=transaction.value,
                   descricao=transaction.description, tipo=transaction.type,
                   realizada_em=transaction.created_at)
        )
        await self.session.commit()

    async def get(self, user_id: int):
        result = await self.session.execute(select(Cliente).
                                            where(Cliente.id == user_id))
        row = result.scalars().first()
        return row.to_domain() if row else None

    @ asynccontextmanager
    async def lock(self, user_id: int):
        async with self.session.begin():
            stmt = text(
                'SELECT pg_advisory_xact_lock(:user_id)')

            await self.session.execute(stmt, {'user_id': user_id})
            yield

    async def view(self, user_id: int, datetime: Datetime):
        result = await self.session.execute(select(Cliente).
                                            where(Cliente.id == user_id))
        row = result.scalars().first()
        if row:
            transactions = await self.session.execute(select(Transacao).
                                                      filter(Transacao.cliente_id == user_id).
                                                      order_by(desc(Transacao.realizada_em)).
                                                      limit(10))
            transaction_views = [t.to_view()
                                 for t in transactions.scalars()]
            return BalanceView(row.saldo, datetime.now(), row.limite,
                               transaction_views)

    async def delete_all_transactions(self):
        async with self.session.begin():
            await self.session.execute(text('DELETE FROM transacoes'))
            await self.session.commit()


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def __aenter__(self):

        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)()
        self.users = PostgresUserRepository(self.async_session)

    async def __aexit__(self, *_):
        await self.async_session.close()


def create_asyncpg_engine():
    return create_async_engine(
        "postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER', 'admin')}:{
            os.getenv('POSTGRES_PASSWORD', '123')}"
        f"@{os.getenv('POSTGRES_HOST', 'localhost')
            }/{os.getenv('POSTGRES_DB', 'rinha')}", pool_size=5)
