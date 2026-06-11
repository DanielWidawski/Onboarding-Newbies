from abc import ABC, abstractmethod
from uuid import UUID

from orders.order_request import OrderRequest


class BackendStore(ABC):
    @abstractmethod
    def save_order(self, order: OrderRequest) -> UUID:
        pass