from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from app.models.schemas import Message

class BaseChain(ABC):
    """Base class for all model-specific LangChain implementations."""

    @abstractmethod
    async def run(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Run the chain with the given inputs."""
        pass

    