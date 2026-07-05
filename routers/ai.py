from fastapi import APIRouter
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter(prefix="/ai", tags=["AI"])


class SOSRequest(BaseModel):
    message: str


@router.post("/process-sos")
def process_sos(data: SOSRequest):

    text = data.message.lower()

    # Default values
    emergency_type = "General"
    severity_level = "Low"
    location = "Unknown"
    is_emergency = False

    # Simple classification
    if "burst" in text:
        emergency_type = "Pipe Burst"
        severity_level = "High"
        is_emergency = True

    elif "leak" in text:
        emergency_type = "Water Leak"
        severity_level = "Medium"
        is_emergency = True

    elif "flood" in text or "flooding" in text:
        emergency_type = "Flood"
        severity_level = "High"
        is_emergency = True

    # Try to extract location
    if "road no." in text:
        location = data.message[data.message.lower().find("road no."):]

    # Save only emergency tickets
    if is_emergency:
        ticket = {
            "source_type": "Citizen Chatbot",
            "description": data.message
        }

        try:
            supabase.table("emergency_tickets").insert(ticket).execute()
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    return {
        "status": "success",
        "emergency_type": emergency_type,
        "severity_level": severity_level,
        "location": location,
        "is_emergency": is_emergency,
        "message": data.message
    }