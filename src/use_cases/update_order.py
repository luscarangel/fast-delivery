from typing import Optional
from uuid import UUID

from src.domain.entities.courier import CourierStatus
from src.domain.entities.delivery_status import DeliveryStatus
from src.domain.entities.order import Order
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface


class UpdateOrder:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        courier_repository: CourierRepositoryInterface,
    ):
        self.order_repository = order_repository
        self.courier_repository = courier_repository

    def execute(
        self,
        order_id: UUID,
        customer_name: Optional[str] = None,
        address: Optional[str] = None,
        value: Optional[float] = None,
        status: Optional[DeliveryStatus] = None,
        courier_id: Optional[UUID] = None,
    ) -> Order:
        if courier_id:
            courier = self.courier_repository.get_by_id(courier_id)
            if not courier:
                raise ValueError("Courier not found")
            if courier.status != CourierStatus.AVAILABLE:
                raise ValueError(f"Courier {courier.name} is not available")

        existing_order = self.order_repository.get_by_id(order_id)

        if not existing_order:
            raise ValueError("Order not found")

        if customer_name is not None:
            existing_order.customer_name = customer_name
        if address is not None:
            existing_order.address = address
        if value is not None:
            existing_order.value = value
        if status is not None:
            existing_order.status = status
        if courier_id is not None:
            existing_order.courier_id = courier_id

        return self.order_repository.save(existing_order)
