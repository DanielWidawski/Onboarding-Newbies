from uuid import UUID, uuid4

from orders.order_request import OrderRequest


def save_order_to_db(order_data: OrderRequest) -> UUID:
    """
    Fake database function. 
    In a real app, this would save to Postgres/MongoDB.
    Takes 2 seconds to simulate network latency.
    """
    import time
    time.sleep(2)
    id =  uuid4()
    print(f"Order {id} saved to DB: {order_data.model_dump()}")
    return id
