from typing import List

from src.domain.entities.courier import Courier
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)


class ListCouriers:
    def __init__(self, courier_repository: CourierRepositoryInterface):
        self.courier_repository = courier_repository

    def execute(self) -> List[Courier]:
        return self.courier_repository.get_all()
