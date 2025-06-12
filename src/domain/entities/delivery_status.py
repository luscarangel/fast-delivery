from enum import Enum


class DeliveryStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    FAILED = "failed"
