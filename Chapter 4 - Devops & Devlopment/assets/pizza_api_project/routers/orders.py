from fastapi import APIRouter

from models import default_menu

from orders.order_manager import OrderManager
from orders.order_request import OrderRequest

router = APIRouter(prefix="/orders")
oreder_manager = OrderManager()


@router.post("/")
def create_order(order: OrderRequest):
    """
    TODO: INCOMPLETE ENDPOINT!
    1. Calculate total price.
    2. Call 'save_order_to_db(order_data)' to save it.
    3. Return a success message with the total price and an order ID.
    4. Handle cases where the pizza list is empty (raise 400 exception).
    """
    return oreder_manager.manage_order(order=order, menu=default_menu)
        
