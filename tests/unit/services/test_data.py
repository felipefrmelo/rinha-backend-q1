from rinha_de_backend.services.data import CreateTransaction
import pytest

from rinha_de_backend.services.exceptions import ValidationError


@pytest.mark.parametrize("type, value, description", [
    ('f', 1000, 'test'),
    ('c', -1, 'test'),
    ('c', 0, 'test'),
    ('c', 5, 'bigger_than_10'),
    ('d', '100', 'test'),
    ('c', 1.1, 'test'),
    ('c', 1.1, ''),
    ('c', 1, None),
])
def test_create_transactions(type, value, description):

    with pytest.raises(ValidationError):
        CreateTransaction(
            value=value, description=description, type=type)


def test_performance_create_transaction(benchmark):
    benchmark(CreateTransaction, 1000, 'test', 'c')
