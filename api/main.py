# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

# later we will import real DB logic
# from database.db import get_session
# from database.models import LLMRequest

app = FastAPI(
    title="AI Observability Platform",
    description="Local-first LLM observability ingestion service",
    version="0.1.0",
)


# ---------------------------
# Pydantic Schemas
# ---------------------------

class TelemetryEvent(BaseModel):
    app_id: str = Field(..., example="chatbot-v1")
    model_name: str = Field(..., example="gpt-4o-mini")
    prompt: str
    response: str
    latency_ms: int = Field(..., ge=0)
    token_count: Optional[int] = None
    timestamp: Optional[datetime] = None


class TelemetryResponse(BaseModel):
    request_id: str
    status: str


# ---------------------------
# Health Check
# ---------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------
# Telemetry Ingestion
# ---------------------------

@app.post("/log", response_model=TelemetryResponse)
def log_telemetry(event: TelemetryEvent):
    """
    Ingests LLM request/response telemetry.
    """

    request_id = str(uuid.uuid4())

    # ensure timestamp exists
    event_timestamp = event.timestamp or datetime.utcnow()

    # 🚧 TEMPORARY PLACEHOLDER
    # This will be replaced with real DB logic
    telemetry_record = {
        "id": request_id,
        "app_id": event.app_id,
        "model_name": event.model_name,
        "prompt": event.prompt,
        "response": event.response,
        "latency_ms": event.latency_ms,
        "token_count": event.token_count,
        "timestamp": event_timestamp,
    }

    # For now, just log to console
    print("Received telemetry:")
    print(telemetry_record)

    # Later:
    # with get_session() as session:
    #     session.add(LLMRequest(**telemetry_record))
    #     session.commit()

    return TelemetryResponse(
        request_id=request_id,
        status="logged"
    )
