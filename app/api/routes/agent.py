from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import AgentRequest, AgentResponse
from app.services.agent_service import AgentService
from app.api.dependencies import get_agent_service

router = APIRouter(tags=["agents"])

@router.post("/chat", response_model=AgentResponse)
async def chat(request: AgentRequest, agent_service: AgentService = Depends(get_agent_service)):
    """
    Chat with an AI agent using various models.
    
    the model is specified in the request, defaulting to the configurted default model.
    This endpoint works with all supported model providers (Ollama, Huggingface, etc.)
    without changing the API contract
    """
    try:
        response = await agent_service.process_request(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            **request.additional_params
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Processing Request: {str(e)}")
    