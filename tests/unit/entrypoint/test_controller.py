from rinha_de_backend.entrypoints.web.controller import Controller
from rinha_de_backend.entrypoints.web.data import Request
import pytest
from orjson import dumps, loads


def make_request(valor=1, descricao='test', tipo='c', user_id=1):
    return Request(body={'valor': valor,
                         'descricao': descricao,
                         'tipo': tipo},
                   params={'user_id': user_id})


async def make_app():
    return await Controller().setup('memory')


@pytest.mark.asyncio
async def test_should_return_200_when_create_transaction():

    app = await make_app()

    request = make_request()

    response = await app.create_transaction(request)

    assert response.status_code == 200
    assert response.body == dumps({'limite': 1000, "saldo": 1001})


@pytest.mark.asyncio
async def test_should_return_422_when_create_transaction_payload_is_invalid():

    app = await make_app()

    request = make_request(valor=-1)

    response = await app.create_transaction(request)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_should_return_404_when_user_not_found():

    app = await make_app()

    request = make_request(user_id=999)

    response = await app.create_transaction(request)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_should_return_422_when_create_transaction_with_limit_exceeded():

    app = await make_app()

    request = make_request(valor=2001, tipo='d')

    response = await app.create_transaction(request)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_should_return_200_when_get_transactions():

    app = await make_app()

    request = Request(params={'user_id': 1})

    response = await app.get_transactions(request)

    assert response.status_code == 200
    assert ['saldo', 'ultimas_transacoes'] == list(loads(response.body).keys())


@pytest.mark.asyncio
async def test_should_return_404_when_get_transactions_user_not_found():

    app = await make_app()

    request = Request(params={'user_id': 999})

    response = await app.get_transactions(request)

    assert response.status_code == 404
