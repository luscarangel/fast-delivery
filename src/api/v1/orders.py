from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.dependencies import (
    create_order_use_case,
    delete_order_use_case,
    get_order_by_id_use_case,
    list_orders_use_case,
    update_order_use_case,
)
from src.api.v1.schemas import OrderCreate, OrderResponse, OrderUpdate
from src.use_cases.create_order import CreateOrder
from src.use_cases.delete_order import DeleteOrder
from src.use_cases.get_order_by_id import GetOrderById
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_order import UpdateOrder

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
def create_order(
    order_data: OrderCreate, use_case: CreateOrder = Depends(create_order_use_case)
):
    new_order = use_case.execute(
        customer_name=order_data.customer_name,
        address=order_data.address,
        value=order_data.value,
    )
    return new_order


@router.get(
    "/",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="List all orders",
)
def list_orders(use_case: ListOrders = Depends(list_orders_use_case)):
    return use_case.execute()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a order by ID",
)
def get_order(
    order_id: UUID, use_case: GetOrderById = Depends(get_order_by_id_use_case)
):
    order = use_case.execute(order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a order",
)
def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    use_case: UpdateOrder = Depends(update_order_use_case),
):
    try:
        update_data = order_data.model_dump(exclude_unset=True)
        updated_order = use_case.execute(order_id=order_id, **update_data)
        return updated_order
    except ValueError as e:
        error_message = str(e)
        if "not found" in error_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=error_message
            )


@router.delete(
    "/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a order"
)
def delete_order(
    order_id: UUID, use_case: DeleteOrder = Depends(delete_order_use_case)
):
    use_case.execute(order_id=order_id)
    return
