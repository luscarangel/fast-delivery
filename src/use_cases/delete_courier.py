from uuid import UUID

from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class DeleteCourier:
    def __init__(
        self,
        courier_repository: CourierRepositoryInterface,
        order_repository: OrderRepositoryInterface,
    ):
        self.courier_repository = courier_repository
        self.order_repository = order_repository

    def execute(self, courier_id: UUID) -> None:
        courier_to_delete = self.courier_repository.get_by_id(courier_id)
        if not courier_to_delete:
            return

        associated_orders = self.order_repository.get_by_courier_id(courier_id)
        if associated_orders:
            raise ValueError("Cannot delete courier, as they have associated orders")

        self.courier_repository.delete(courier_id)
