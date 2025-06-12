from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.courier import CourierStatus
from src.domain.entities.delivery_status import DeliveryStatus
from src.infra.db.models.base_model import Base
from src.infra.db.models.courier_model import CourierModel
from src.infra.db.models.order_model import OrderModel
from src.infra.db.session import SessionLocal, engine

Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()
    try:
        if db.query(CourierModel).count() > 0 or db.query(OrderModel).count() > 0:
            print("Data already exists. Ignoreing the seed")
            return

        print("Starting data seed")

        now = datetime.now(timezone.utc)

        couriers = [
            CourierModel(
                id=uuid4(),
                name=f"Entregador {i}",
                vehicle="Moto",
                status=CourierStatus.AVAILABLE,
                created_at=now,
                updated_at=now,
            )
            for i in range(1, 11)
        ]

        db.add_all(couriers)
        db.flush()

        orders = [
            OrderModel(
                id=uuid4(),
                customer_name=f"Cliente {i}",
                address=f"Rua Exemplo {i}, Nº {100 + i}",
                value=round(50.0 + i * 3.75, 2),
                status=DeliveryStatus.IN_PROGRESS,
                courier_id=None,
                created_at=now,
                updated_at=now,
            )
            for i in range(1, 11)
        ]

        db.add_all(orders)
        db.commit()
        print("Seed completed successfully")
    except Exception as e:
        print(f"Error applying seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
