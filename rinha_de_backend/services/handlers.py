
from .data import CreateTransaction, UserResponse
from .exceptions import UserNotFound
from .protocols import UnitOfWork, Datetime


async def create_transaction(uow: UnitOfWork, datetime: Datetime, dto: CreateTransaction, user_id: int) -> UserResponse:

    async with uow:
        async with uow.users.lock(user_id):
            user = await uow.users.get(user_id)

            if not user:
                raise UserNotFound()

            user.add_transaction(dto.to_entity(datetime.now()))

            await uow.users.save(user)

            return UserResponse(user.limit, user.balance)


async def get_transactions(uow: UnitOfWork, datetime: Datetime, user_id: int):

    async with uow:
        view = await uow.users.view(user_id, datetime)

        if not view:
            raise UserNotFound()

        return view
