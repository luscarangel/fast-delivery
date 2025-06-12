from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api.v1 import couriers, orders, system

app = FastAPI(title="FastDelivery API")

Instrumentator().instrument(app).expose(app)

app.include_router(system.router)

app.include_router(couriers.router, prefix="/api/v1")

app.include_router(orders.router, prefix="/api/v1")
