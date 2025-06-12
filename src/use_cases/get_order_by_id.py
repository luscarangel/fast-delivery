from typing import Optional
from uuid import UUID

from src.domain.entities.order import Order
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class GetOrderById:
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, order_id: UUID) -> Optional[Order]:
        order = self.order_repository.get_by_id(order_id)
        return order
