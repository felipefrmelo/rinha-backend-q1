import requests


BASE_URL = 'http://localhost:9999'


def get_extrato(user_id):
    response = requests.get(
        f'{BASE_URL}/clientes/{user_id}/extrato')

    assert response.status_code == 200

    extrato = response.json()

    assert extrato['saldo']['total'] is not None
    assert extrato['saldo']['data_extrato'] is not None
    assert extrato['saldo']['limite'] is not None
    assert extrato['ultimas_transacoes'] is not None
    return extrato


def post_transacao(user_id, valor, tipo, descricao, status_code=200):
    response = requests.post(
        f'{BASE_URL}/clientes/{user_id}/transacoes', json={"valor": valor, "tipo": tipo, "descricao": descricao})

    assert response.status_code == status_code
    return response


def test_get():
    get_extrato(1)


def test_post():

    extrato_antes_1 = get_extrato(1)
    extrato_antes_2 = get_extrato(2)

    post_transacao(1, 1, 'c', 'descricao')
    post_transacao(2, 10, 'd', 'abc')

    extrato_depois_1 = get_extrato(1)
    extrato_depois_2 = get_extrato(2)

    assert extrato_depois_1['saldo']['total'] == extrato_antes_1['saldo']['total'] + 1
    assert extrato_depois_2['saldo']['total'] == extrato_antes_2['saldo']['total'] - 10


def test_user_not_found():
    response = requests.get(
        f'{BASE_URL}/clientes/9999999/extrato')

    assert response.status_code == 404


def test_invalid_transaction():
    post_transacao(1, 999999999999, 'd', 'descricao', status_code=422)


def test_last_transaction():
    post_transacao(1, 1, 'c', 'last1')

    extrato = get_extrato(1)

    assert extrato['ultimas_transacoes'][0]['descricao'] == 'last1'
