from uuid import UUID

from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class DeleteOrder:
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository

    def execute(self, order_id: UUID) -> None:
        self.order_repository.delete(order_id)
