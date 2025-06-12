from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.courier import Courier


class CourierRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        pass

    @abstractmethod
    def save(self, courier: Courier) -> Courier:
        pass

    @abstractmethod
    def get_all(self) -> List[Courier]:
        pass

    @abstractmethod
    def delete(self, courier_id: UUID) -> None:
        pass
