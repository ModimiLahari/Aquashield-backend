import uuid
from sqlalchemy import Column, Boolean, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pipe_id = Column(UUID(as_uuid=True), nullable=False)

    flow_rate = Column(Numeric, nullable=False)

    pressure = Column(Numeric, nullable=False)

    anomaly_detected = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )