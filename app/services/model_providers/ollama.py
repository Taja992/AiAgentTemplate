from typing import List, Dict, Any, Optional
import asyncio
from functools import partial
from ollama import Client

from app.services.model_providers.base import BaseModelHandler
from app.models.schemas import Message
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class OllamaModelHandler(BaseModelHandler):
    """Handler for Ollama-based models."""
    
    def __init__(self, host: Optional[str] = None):
        """
        Initialize the Ollama model handler.
        
        Args:
            host: Ollama API host (defaults to settings.OLLAMA_HOST)
        """
        self.host = host or settings.OLLAMA_HOST
        
        # Initialize Ollama client
        self.client = Client(host=self.host)
        logger.info(f"Initialized Ollama model handler with host: {self.host}")
    
    def _convert_to_ollama_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert our Message objects to the dict format Ollama expects."""
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    async def generate(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response using Ollama."""
        logger.debug(f"Generating response with Ollama model: {model}")
        
        # Convert messages to Ollama format
        ollama_messages = self._convert_to_ollama_messages(messages)
        
        try:
            # Ollama doesn't have native async support, so run in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(
                    self.client.chat,
                    model=model,
                    messages=ollama_messages,
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        **kwargs
                    }
                )
            )
            
            # Extract the response content
            content = response["message"]["content"]
            
            # Extract token usage if available
            usage = response.get("usage", {})
            
            return {
                "content": content,
                "usage": usage,
                "model": model,
                "provider": "ollama"
            }
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise