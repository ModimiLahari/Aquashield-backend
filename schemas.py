from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SensorReadingCreate(BaseModel):
    pipe_id: UUID
    flow_rate: float
    pressure: float


class SensorReadingResponse(BaseModel):
    id: UUID
    pipe_id: UUID
    flow_rate: float
    pressure: float
    anomaly_detected: bool
    created_at: datetime

    class Config:
        from_attributes = True