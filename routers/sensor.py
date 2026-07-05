from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter(prefix="/sensor", tags=["Sensor"])


class SensorReading(BaseModel):
    pipe_id: str
    flow_rate: float
    pressure: float


@router.post("/data")
def receive_sensor_data(data: SensorReading):

    anomaly = data.pressure < 15

    # Insert into sensor_readings
    sensor_payload = {
        "pipe_id": data.pipe_id,
        "flow_rate": data.flow_rate,
        "pressure": data.pressure,
        "anomaly_detected": anomaly
    }

    try:
        sensor_response = (
            supabase.table("sensor_readings")
            .insert(sensor_payload)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Insert emergency ticket if pressure < 15
    if anomaly:
        ticket = {
            "source_type": "Sensor Anomaly",
            "description": f"Critical pressure drop on {data.pipe_id}"
        }

        try:
            supabase.table("emergency_tickets").insert(ticket).execute()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Emergency Ticket Error: {str(e)}"
            )

    return {
        "message": "Sensor data inserted successfully",
        "anomaly_detected": anomaly,
        "data": sensor_response.data
    }


@router.get("/data")
def get_sensor_data():
    response = (
        supabase.table("sensor_readings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data

@router.get("/data")
def get_sensor_data():
    response = (
        supabase.table("sensor_readings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


class SOSRequest(BaseModel):
    message: str


@router.post("/process-sos")
def process_sos(data: SOSRequest):

    severity = "medium"
    emergency_type = "General"

    if "burst" in data.message.lower():
        severity = "high"
        emergency_type = "Pipe Burst"
    elif "leak" in data.message.lower():
        severity = "medium"
        emergency_type = "Water Leak"

    if severity == "high":
        ticket = {
            "source_type": "Citizen Chatbot",
            "description": data.message
        }

        supabase.table("emergency_tickets").insert(ticket).execute()

    return {
        "severity_level": severity,
        "emergency_type": emergency_type
    }