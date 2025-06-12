from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from src.domain.entities.delivery_status import DeliveryStatus


@dataclass
class Order:
    id: UUID
    customer_name: str
    address: str
    value: float
    status: DeliveryStatus = DeliveryStatus.IN_PROGRESS
    courier_id: Optional[UUID] = None

    @staticmethod
    def create(customer_name: str, address: str, value: float) -> "Order":
        return Order(
            id=uuid4(),
            customer_name=customer_name,
            address=address,
            value=value,
        )
