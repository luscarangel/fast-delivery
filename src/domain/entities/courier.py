from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4


class CourierStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DELIVERING = "delivering"


@dataclass
class Courier:
    id: UUID
    name: str
    vehicle: str
    status: CourierStatus = CourierStatus.AVAILABLE

    @staticmethod
    def create(name: str, vehicle: str) -> "Courier":
        return Courier(id=uuid4(), name=name, vehicle=vehicle)
