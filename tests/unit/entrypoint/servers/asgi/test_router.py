from rinha_de_backend.entrypoints.web.servers.asgi.router import mount
import pytest


@pytest.mark.asyncio
async def test_mount():
    router = mount('/clientes/{user_id:int}/extrato')

    assert router('/clientes/1/extrato') == {'user_id': 1}
    assert router('/clientes/2/extrato') == {'user_id': 2}
    assert router('/clientes/2/extrato?param=1') == {'user_id': 2}
    assert not router('/clientes/abc/extrato')
    assert not router('/clientes/1/extrato/abc')
    assert not router('/clientes/1/extrato/abc?param=1')
    assert not router('/cliente/1/extrato')
