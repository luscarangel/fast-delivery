from typing import Optional
from uuid import UUID

from src.domain.entities.courier import Courier, CourierStatus
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)


class UpdateCourier:
    def __init__(self, courier_repository: CourierRepositoryInterface):
        self.courier_repository = courier_repository

    def execute(
        self,
        courier_id: UUID,
        name: Optional[str] = None,
        vehicle: Optional[str] = None,
        status: Optional[CourierStatus] = None,
    ) -> Courier:
        existing_courier = self.courier_repository.get_by_id(courier_id)

        if not existing_courier:
            raise ValueError("Courier not found")

        if name is not None:
            existing_courier.name = name
        if vehicle is not None:
            existing_courier.vehicle = vehicle
        if status is not None:
            existing_courier.status = status

        return self.courier_repository.save(existing_courier)
