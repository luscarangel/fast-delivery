from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.order import Order
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface
from src.infra.db.models.order_model import OrderModel


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        model = self.session.get(OrderModel, order_id)
        if not model:
            return None
        return Order(
            id=model.id,
            customer_name=model.customer_name,
            address=model.address,
            value=model.value,
            status=model.status,
            courier_id=model.courier_id,
        )

    def save(self, order: Order) -> Order:
        model = OrderModel(
            id=order.id,
            customer_name=order.customer_name,
            address=order.address,
            value=order.value,
            status=order.status,
            courier_id=order.courier_id,
        )
        self.session.merge(model)
        self.session.commit()
        return order

    def get_all(self) -> List[Order]:
        models = self.session.query(OrderModel).all()
        return [
            Order(
                id=model.id,
                customer_name=model.customer_name,
                address=model.address,
                value=model.value,
                status=model.status,
                courier_id=model.courier_id,
            )
            for model in models
        ]

    def delete(self, order_id: UUID) -> None:
        model = self.session.get(OrderModel, order_id)
        if model:
            self.session.delete(model)
            self.session.commit()

    def get_by_courier_id(self, courier_id: UUID) -> List[Order]:
        models = (
            self.session.query(OrderModel)
            .filter(OrderModel.courier_id == courier_id)
            .all()
        )
        return [
            Order(
                id=model.id,
                customer_name=model.customer_name,
                address=model.address,
                value=model.value,
                status=model.status,
                courier_id=model.courier_id,
            )
            for model in models
        ]
