from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.repositories.courier_repository_interface import (
    CourierRepositoryInterface,
)
from src.domain.repositories.order_repository_interface import OrderRepositoryInterface
from src.infra.db.session import get_db
from src.infra.repositories.courier_repository import CourierRepository
from src.infra.repositories.order_repository import OrderRepository
from src.use_cases.create_courier import CreateCourier
from src.use_cases.create_order import CreateOrder
from src.use_cases.delete_courier import DeleteCourier
from src.use_cases.delete_order import DeleteOrder
from src.use_cases.get_courier_by_id import GetCourierById
from src.use_cases.get_order_by_id import GetOrderById
from src.use_cases.list_couriers import ListCouriers
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_courier import UpdateCourier
from src.use_cases.update_order import UpdateOrder


# Repositórios
def get_courier_repository(db: Session = Depends(get_db)) -> CourierRepositoryInterface:
    return CourierRepository(db)


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepositoryInterface:
    return OrderRepository(db)


# Couriers use cases
def create_courier_use_case(
    repo: CourierRepositoryInterface = Depends(get_courier_repository),
) -> CreateCourier:
    return CreateCourier(courier_repository=repo)


def list_couriers_use_case(
    repo: CourierRepositoryInterface = Depends(get_courier_repository),
) -> ListCouriers:
    return ListCouriers(courier_repository=repo)


def update_courier_use_case(
    repo: CourierRepositoryInterface = Depends(get_courier_repository),
) -> UpdateCourier:
    return UpdateCourier(courier_repository=repo)


def delete_courier_use_case(
    courier_repo: CourierRepositoryInterface = Depends(get_courier_repository),
    order_repo: OrderRepositoryInterface = Depends(get_order_repository),
) -> DeleteCourier:
    return DeleteCourier(courier_repository=courier_repo, order_repository=order_repo)


def get_courier_by_id_use_case(
    repo: CourierRepositoryInterface = Depends(get_courier_repository),
) -> GetCourierById:
    return GetCourierById(courier_repository=repo)


# Orders use cases
def create_order_use_case(
    repo: OrderRepositoryInterface = Depends(get_order_repository),
) -> CreateOrder:
    return CreateOrder(order_repository=repo)


def list_orders_use_case(
    repo: OrderRepositoryInterface = Depends(get_order_repository),
) -> ListOrders:
    return ListOrders(order_repository=repo)


def update_order_use_case(
    order_repo: OrderRepositoryInterface = Depends(get_order_repository),
    courier_repo: CourierRepositoryInterface = Depends(get_courier_repository),
) -> UpdateOrder:
    return UpdateOrder(
        order_repository=order_repo,
        courier_repository=courier_repo,
    )


def delete_order_use_case(
    repo: OrderRepositoryInterface = Depends(get_order_repository),
) -> DeleteOrder:
    return DeleteOrder(order_repository=repo)


def get_order_by_id_use_case(
    repo: OrderRepositoryInterface = Depends(get_order_repository),
) -> GetOrderById:
    return GetOrderById(order_repository=repo)
