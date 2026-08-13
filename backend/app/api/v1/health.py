from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from datetime import datetime, timezone
import os

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

class ReadinessResponse(BaseModel):
    status: str
    dependencies: dict

@router.get("/health", response_model=HealthResponse, tags=["health"])
async def check_health():
    """
    Liveness probe: Indicates if the FastAPI application process is running and can accept requests.
    """
    return HealthResponse(
        status="alive",
        version="0.1.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@router.get("/ready", response_model=ReadinessResponse, tags=["health"])
async def check_readiness(response: Response):
    """
    Readiness probe: Indicates if the FastAPI application can communicate with its required dependencies.
    For MS-002, this is a simulated check as infrastructure is present but not deeply integrated yet.
    """
    # In a real scenario, this would ping Redis and Postgres.
    # For MS-002, we just return simulated readiness or check env vars.
    dependencies = {
        "redis": "simulated_connected",
        "postgres": "simulated_connected"
    }
    
    # If a dependency fails, set response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return ReadinessResponse(
        status="ready",
        dependencies=dependencies
    )
