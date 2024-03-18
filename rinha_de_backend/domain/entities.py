from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque

from .exceptions import LimitExceeded


@dataclass
class Transaction:
    value: int
    description: str
    type: str
    created_at: datetime


@dataclass
class User:
    id: int
    name: str
    limit: int
    balance: int
    transactions: Deque[Transaction] = field(default_factory=deque)

    def add_transaction(self, transaction: Transaction):
        if transaction.type == 'c':
            self.balance += transaction.value
        else:
            self.balance -= transaction.value

        if self.balance < -self.limit:
            raise LimitExceeded()

        self.transactions.appendleft(transaction)
