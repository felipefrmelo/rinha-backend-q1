from dataclasses import dataclass
from datetime import datetime
from orjson import dumps

from rinha_de_backend.domain.entities import Transaction
from rinha_de_backend.services.exceptions import ValidationError


types = {'d', 'c'}


@dataclass
class CreateTransaction:
    value: int
    description: str
    type: str

    def __post_init__(self):
        if self.type not in types:
            raise ValidationError('Invalid type')
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValidationError('Invalid value')
        if  not isinstance(self.description, str) or len(self.description) > 10 or len(self.description) < 1:
            raise ValidationError('Invalid description')

    def to_entity(self, date: datetime):
        return Transaction(self.value, self.description, self.type, date)


@dataclass
class UserResponse:
    limit: int
    balance: int

    def to_json(self):
        return dumps({'limite': self.limit, 'saldo': self.balance})


@dataclass
class TransactionView:
    value: int
    date: datetime
    description: str
    type: str


@dataclass
class BalanceView:
    total: int
    extract_date: datetime
    limit: int
    transactions: list[TransactionView]

    def to_json(self):
        return dumps({
            "saldo": {
                "total": self.total,
                "data_extrato": self.extract_date.strftime("%Y-%m-%d"),
                "limite": self.limit
            },
            "ultimas_transacoes": [
                {
                    "valor": t.value,
                    "data": t.date.strftime("%Y-%m-%d"),
                    "descricao": t.description,
                    "tipo": t.type
                } for t in self.transactions
            ]
        })
