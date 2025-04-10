import httpx
from fastapi import APIRouter, HTTPException
from app.config import settings
from typing import List, Dict, Any
from app.models.schemas import OllamaModel

router = APIRouter(
    prefix="/models",
    tags=["models"],
)

@router.get("/", response_model=List[OllamaModel])
async def list_available_models():
    """Fetch all available models from Ollama"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                # Format models for frontend display
                formatted_models = [
                    OllamaModel(
                        id=f"ollama:{model['name']}",
                        name=model['name'],
                        size=model.get('size', 'Unknown'),
                        modified_at=model.get('modified_at', ''),
                        description=model.get('details', {}).get('description', '')
                    )
                    for model in models
                ]
                return formatted_models
            else:
                raise HTTPException(status_code=response.status_code, 
                                  detail="Failed to fetch models from Ollama")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama: {str(e)}")
