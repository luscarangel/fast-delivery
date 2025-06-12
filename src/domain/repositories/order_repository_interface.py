from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_courier_id(self, courier_id: UUID) -> List[Order]:
        pass
