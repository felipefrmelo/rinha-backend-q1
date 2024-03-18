from collections import defaultdict

from orjson import loads
from rinha_de_backend.entrypoints.web.controller import Controller
from rinha_de_backend.entrypoints.web.data import Request
import asyncio
import yappi
import random

yappi.set_clock_type("WALL")

count = defaultdict(int)


def get_random_int():
    r = random.randint(1, 5)
    count[r] += 1
    return r


def make_request(valor=1, descricao='test', tipo='c'):
    return Request(body={'valor': valor,
                         'descricao': descricao,
                         'tipo': tipo},
                   params={'user_id': get_random_int()})


async def main():

    controller = Controller()

    await controller.setup('pg')

    user_before = await controller.get_transactions(Request(params={'user_id': 1}))

    num_transactions = 1000

    tasks = [controller.create_transaction(make_request())
             for _ in range(num_transactions)]

    await asyncio.gather(*tasks)

    tasks_view = [controller.get_transactions(Request(params={'user_id': 1}))
                  for _ in range(num_transactions)]

    await asyncio.gather(*tasks_view)

    user_after = await controller.get_transactions(Request(params={'user_id': 1}))

    assert loads(user_after.body)["saldo"]["total"] == loads(
        user_before.body)["saldo"]["total"] + count[1]


if __name__ == "__main__":
    with yappi.run():
        asyncio.run(main())

    stats = yappi.get_func_stats(
        filter_callback=lambda x: "rinha_de_backend" in x.module
    )

    stats.print_all()
