from rinha_de_backend.domain.entities import User, Transaction
from rinha_de_backend.domain.exceptions import LimitExceeded
from datetime import datetime
import pytest


def test_should_not_allow_balance_below_limit():

    user = User(id=1, name='test', limit=1000, balance=1000)

    transaction = Transaction(
        value=2001, description='test', type='d', created_at=datetime.now())

    with pytest.raises(LimitExceeded):
        user.add_transaction(transaction)
