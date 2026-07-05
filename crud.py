from sqlalchemy.orm import Session
import models
import schemas


def create_sensor_reading(db: Session, reading: schemas.SensorReadingCreate):
    db_reading = models.SensorReading(
        pipe_id=reading.pipe_id,
        flow_rate=reading.flow_rate,
        pressure=reading.pressure,
        anomaly_detected=reading.anomaly_detected
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading


def get_sensor_readings(db: Session, limit: int = 100):
    return (
        db.query(models.SensorReading)
        .order_by(models.SensorReading.created_at.desc())
        .limit(limit)
        .all()
    )