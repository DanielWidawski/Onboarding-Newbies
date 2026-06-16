from abc import ABC, abstractmethod
from typing import Self
from uuid import UUID

from orders.order_request import OrderRequest


class DbHandler(ABC):
    @abstractmethod
    def save_order(self: Self, order: OrderRequest) -> UUID:
        pass
