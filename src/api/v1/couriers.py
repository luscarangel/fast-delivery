from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.dependencies import (
    create_courier_use_case,
    delete_courier_use_case,
    get_courier_by_id_use_case,
    list_couriers_use_case,
    update_courier_use_case,
)
from src.api.v1.schemas import CourierCreate, CourierResponse, CourierUpdate
from src.use_cases.create_courier import CreateCourier
from src.use_cases.delete_courier import DeleteCourier
from src.use_cases.get_courier_by_id import GetCourierById
from src.use_cases.list_couriers import ListCouriers
from src.use_cases.update_courier import UpdateCourier

router = APIRouter(prefix="/couriers", tags=["Couriers"])


@router.post(
    "/",
    response_model=CourierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new courier",
)
def create_courier(
    courier_data: CourierCreate,
    use_case: CreateCourier = Depends(create_courier_use_case),
):
    new_courier = use_case.execute(name=courier_data.name, vehicle=courier_data.vehicle)
    return new_courier


@router.get(
    "/",
    response_model=List[CourierResponse],
    status_code=status.HTTP_200_OK,
    summary="List all couriers",
)
def list_couriers(use_case: ListCouriers = Depends(list_couriers_use_case)):
    return use_case.execute()


@router.get(
    "/{courier_id}",
    response_model=CourierResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a courier by ID",
)
def get_courier(
    courier_id: UUID, use_case: GetCourierById = Depends(get_courier_by_id_use_case)
):
    courier = use_case.execute(courier_id=courier_id)

    if not courier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found"
        )

    return courier


@router.put(
    "/{courier_id}",
    response_model=CourierResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a courier",
)
def update_courier(
    courier_id: UUID,
    courier_data: CourierUpdate,
    use_case: UpdateCourier = Depends(update_courier_use_case),
):
    try:
        update_data = courier_data.model_dump(exclude_unset=True)

        updated_courier = use_case.execute(courier_id=courier_id, **update_data)
        return updated_courier
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{courier_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a courier"
)
def delete_courier(
    courier_id: UUID, use_case: DeleteCourier = Depends(delete_courier_use_case)
):
    try:
        use_case.execute(courier_id=courier_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return
