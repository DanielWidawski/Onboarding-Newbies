import time
from typing import Self
from uuid import UUID, uuid4

from db_handler.db_handler import DbHandler
from orders.order_request import OrderRequest


class OrmDbBackend(DbHandler):
    def save_order(self: Self, order: OrderRequest) -> UUID:
        """Fake database function.
        In a real app, this would save to Postgres/MongoDB.
        Takes 2 seconds to simulate network latency.
        """

        time.sleep(2)
        # It is the only one that is random,
        # which is good for order id
        # because we dont want users to be able to guess their id.
        gen_id = uuid4()
        print(f"Order {gen_id} saved to DB: {order.model_dump()}")

        return gen_id
