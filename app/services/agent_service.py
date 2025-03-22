from typing import List, Dict, Any, Optional
from app.models.schemas import Message, AgentResponse
from app.services.model_service import ModelService
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AgentService:
    """
    Service that processes agent requests and routes them to the appropriate model.
    
    This service acts as a facade over different model implementations,
    providing a consistent interface regardless of the underlying model provider.
    """
    
    def __init__(self, model_service: ModelService):
        """
        Initialize the agent service with a model service.
        
        Args:
            model_service: Service that handles interactions with different LLM providers
        """
        self.model_service = model_service
    
    async def process_request(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **additional_params
    ) -> AgentResponse:
        """
        Process a chat request using the specified model.
        
        Args:
            messages: List of message objects with role and content
            model: Name of the model to use (defaults to configured default)
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum number of tokens to generate
            additional_params: Any additional model-specific parameters
            
        Returns:
            AgentResponse with the model's response
        """
        logger.info(f"Processing request with model: {model or settings.DEFAULT_MODEL}")
        
        # Pre-processing logic
        # (You could add things like content filtering, prompt enhancement, etc. here)
        
        # Use the model service to get a response
        model_response = await self.model_service.generate(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **additional_params
        )
        
        # Post-processing logic
        # (You could add things like response filtering, formatting, etc. here)
        
        # Construct and return the response
        return AgentResponse(
            response=model_response["content"],
            model=model_response["model"],
            usage=model_response.get("usage", {})
        )