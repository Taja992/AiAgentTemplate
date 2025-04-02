from typing import List, Dict, Any, Optional
from app.models.schemas import Message, AgentResponse
from app.services.model_service import ModelService
from app.config import settings
from app.utils.logger import get_logger
from app.utils.keywords import (PROGRAMMING_LANGUAGES, CODE_RELATED_TERMS,
                                 TRANSLATION_TERMS, MATH_TERMS, CREATIVE_TERMS)

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

    async def select_model_for_task(self, messages: List[Message]) -> str:
        """
        Analyze the request content and select the most appropriate model.
    
        Args:
            messages: The conversation history
        
        Returns:
            The selected model identifier (e.g., "ollama:llama2")
        """
        # Get the most recent user message
        user_messages = [msg for msg in messages if msg.role.lower() == "user"]
        if not user_messages:
            return settings.DEFAULT_MODEL
    
        last_user_message = user_messages[-1].content.lower()
    
    
        # Check if the message mentions a programming language
        code_keywords = PROGRAMMING_LANGUAGES + CODE_RELATED_TERMS
        if any(keyword in last_user_message for keyword in code_keywords):
            logger.info(f"Detected programming language in query, routing to code model")
            return settings.CODE_MODEL
    
        if any(keyword in last_user_message for keyword in CREATIVE_TERMS):
            logger.info(f"Detected creative task, routing to creative model")
            return settings.CREATIVE_MODEL
        
        if any(keyword in last_user_message for keyword in MATH_TERMS):
            logger.info(f"Detected mathematical task, routing to math model")
            return settings.MATH_MODEL
        
        if any(keyword in last_user_message for keyword in TRANSLATION_TERMS):
            logger.info(f"Detected translation task, routing to translation model")
            return settings.TRANSLATION_MODEL
    
        # Default model for general queries
        return settings.DEFAULT_MODEL
    
    async def process_request(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **additional_params
        ) -> AgentResponse:
        """
        Process a chat request, automatically selecting the best model if none specified.
    
        Args:
            messages: List of message objects with role and content
            model: Name of the model to use (if None, will be auto-selected)
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum number of tokens to generate
            additional_params: Any additional model-specific parameters
        
        Returns:
            AgentResponse with the model's response
        """
        # Auto-select model if none provided
        if model is None:
            model = await self.select_model_for_task(messages)
    
        logger.info(f"Processing request with model: {model}")
    
        # Use the model service to get a response
        model_response = await self.model_service.generate(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **additional_params
        )
    
    # Construct and return the response
        return AgentResponse(
            response=model_response["content"],
            model=model_response["model"],
            usage=model_response.get("usage", {})
        )