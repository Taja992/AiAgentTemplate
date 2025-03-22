from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models.schemas import Message

class BaseModelHandler(ABC):
    """
    Base class for all model handlers.
    
    This abstract class defines the interface that all model handlers must implement.
    """
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message objects with role and content
            model: The specific model to use
            temperature: Controls randomness (0-1)
            max_tokens: Maximum number of tokens to generate
            kwargs: Additional model-specific parameters
            
        Returns:
            Dict containing at least:
            - content: The generated text
            - usage: Token usage information (if available)
        """
        pass