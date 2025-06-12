from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.courier import Courier
from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)
from src.infra.db.models.courier_model import CourierModel


class CourierRepository(CourierRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        model = self.session.get(CourierModel, courier_id)
        if not model:
            return None
        return Courier(
            id=model.id,
            name=model.name,
            vehicle=model.vehicle,
            status=model.status,
        )

    def save(self, courier: Courier) -> Courier:
        model = CourierModel(
            id=courier.id,
            name=courier.name,
            vehicle=courier.vehicle,
            status=courier.status,
        )
        self.session.merge(model)
        self.session.commit()
        return courier

    def get_all(self) -> List[Courier]:
        models = self.session.query(CourierModel).all()
        return [
            Courier(
                id=model.id, name=model.name, vehicle=model.vehicle, status=model.status
            )
            for model in models
        ]

    def delete(self, courier_id: UUID) -> None:
        model = self.session.get(CourierModel, courier_id)
        if model:
            self.session.delete(model)
            self.session.commit()
