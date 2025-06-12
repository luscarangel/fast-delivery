from typing import List

from src.domain.entities.order import Order
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class ListOrders:
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self) -> List[Order]:
        return self.order_repository.get_all()
