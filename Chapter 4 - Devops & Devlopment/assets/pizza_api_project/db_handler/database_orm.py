from uuid import UUID, uuid4

from db_handler.db_handler import DbHandler
from orders.order_request import OrderRequest


class OrmDbBackend(DbHandler):
    def save_order(self, order: OrderRequest) -> UUID:
        """
        Fake database function.
        In a real app, this would save to Postgres/MongoDB.
        Takes 2 seconds to simulate network latency.
        """
        import time

        time.sleep(2)
        id = uuid4()
        print(f"Order {id} saved to DB: {order.model_dump()}")

        return id
