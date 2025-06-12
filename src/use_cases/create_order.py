from src.domain.entities.order import Order
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class CreateOrder:
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, customer_name: str, address: str, value: float) -> Order:
        order = Order.create(customer_name=customer_name, address=address, value=value)
        return self.order_repository.save(order)
