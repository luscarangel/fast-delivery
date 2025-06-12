from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.courier import CourierStatus
from src.domain.entities.delivery_status import DeliveryStatus


class CourierBase(BaseModel):
    name: str = Field(..., examples=["Lucas Rangel"])
    vehicle: str = Field(..., examples=["Kawasaki Ninja"])


class CourierCreate(CourierBase):
    pass


class CourierUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Lucas Rangel"])
    vehicle: Optional[str] = Field(None, examples=["Kawasaki Ninja"])
    status: Optional[CourierStatus] = Field(None, examples=[CourierStatus.UNAVAILABLE])


class CourierResponse(CourierBase):
    id: UUID
    status: CourierStatus

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    customer_name: str = Field(..., examples=["Lucas Rangel"])
    address: str = Field(..., examples=["Rua das Flores, 123, Sao Paulo, SP"])
    value: float = Field(..., gt=0, examples=[99.90])


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, examples=["Lucas Rangel"])
    address: Optional[str] = Field(
        None, examples=["Rua das Flores, 123, Sao Paulo, SP"]
    )
    value: Optional[float] = Field(None, gt=0, examples=[120.50])
    status: Optional[DeliveryStatus] = Field(None, examples=[DeliveryStatus.DELIVERED])
    courier_id: Optional[UUID] = Field(None)


class OrderResponse(OrderBase):
    id: UUID
    status: DeliveryStatus
    courier_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
