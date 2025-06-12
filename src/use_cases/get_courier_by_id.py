from typing import Optional
from uuid import UUID

from src.domain.entities.courier import Courier
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)


class GetCourierById:
    def __init__(self, courier_repository: CourierRepositoryInterface):
        self.courier_repository = courier_repository

    def execute(self, courier_id: UUID) -> Optional[Courier]:
        courier = self.courier_repository.get_by_id(courier_id)
        return courier
