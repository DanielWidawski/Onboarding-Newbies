from uuid import UUID

from fastapi import APIRouter

from orders.order_manager import OrderManager
from orders.order_request import OrderRequest

router = APIRouter(prefix="/orders")
order_manager = OrderManager()


@router.post("/")
def create_order(order: OrderRequest) -> dict[str, float | UUID]:
    return order_manager.manage_order(order=order)
