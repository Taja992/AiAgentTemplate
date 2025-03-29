from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import platform
import time
import socket
import psutil
import os
from pydantic import BaseModel
from app.api.dependencies import get_agent_service
from app.services.agent_service import AgentService
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    """ Model for Health Check Response """
    status: str
    version: str
    timestamp: float
    uptime: float
    environment: str
    system_info: Dict[str, Any]
    services: Dict[str, str]

start_time = time.time()


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check(agent_service: AgentService = Depends(get_agent_service)):
    """ Health Check Endpoint 
    
    Checks:
    - Application status
    - Version Info
    - System resources
    - Connected services status
    """
    services_status = {}

    # Check model service health by testing if providers are available
    try: 
        provider_name = list(agent_service.model_service.model_handlers.keys())
        services_status["model_service"] = "OK" if provider_name else "Unavailable"
    except Exception as e:
        logger.error(f"Health check failed for model service: {str(e)}")
        services_status["model_service"] = f"ERROR: {str(e)}"

    # Get System Information
    system_info = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "python_version": platform.python_version(),
        "processors": os.cpu_count()
    }

    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development")

    response = HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=time.time(),
        uptime=time.time() - start_time,
        environment=environment,
        system_info=system_info,
        services=services_status
    )

    # If any service is down return 503 Service Unavailable
    if any("ERROR" in status for status in services_status.values()):
        response.status = "degraded"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response.dict()
        )
    
    return response
