from src.domain.entities.courier import Courier
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)


class CreateCourier:
    def __init__(self, courier_repository: CourierRepositoryInterface):
        self.courier_repository = courier_repository

    def execute(self, name: str, vehicle: str) -> Courier:
        courier = Courier.create(name=name, vehicle=vehicle)
        return self.courier_repository.save(courier)
