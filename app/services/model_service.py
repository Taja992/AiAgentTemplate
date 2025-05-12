from typing import List, Dict, Any, Optional, Union
from app.models.schemas import Message
from app.config import settings
from app.utils.logger import get_logger
from app.services.chains.model_chains import CodeLlamaChain
import importlib

logger = get_logger(__name__)

class ModelService:
    """
    Service that handles interactions with different LLM providers.
    
    This service manages the connections to different model providers
    and provides a unified interface for generating responses.
    """
    
    def __init__(self):
        """Initialize the model service with available model handlers."""
        # Dictionary to store initialized model handlers
        self.model_handlers = {}

        self.model_chains = {}
        
        # Register available model providers
        self._register_model_handlers()

        # Register model chains (e.g., CodeLlamaChain)
        self._register_model_chains()
        
        logger.info(f"ModelService initialized with handlers: {list(self.model_handlers.keys())}")
        logger.info(f"ModelService initialized with chains: {list(self.model_chains.keys())}")
    
    def _register_model_handlers(self):
        """Register all available model handlers."""
        # Start with Ollama as the default provider
        try:
            from app.services.model_providers.ollama import OllamaModelHandler
            self.model_handlers["ollama"] = OllamaModelHandler()
            logger.info("Registered Ollama model handler")
        except ImportError:
            logger.warning("Ollama handler could not be registered")
        
        # Additional providers can be registered here in the future
        # For example:
        # try:
        #     from app.services.model_providers.huggingface import HuggingFaceModelHandler
        #     self.model_handlers["huggingface"] = HuggingFaceModelHandler()
        # except ImportError:
        #     logger.warning("HuggingFace handler could not be registered")

    def _register_model_chains(self):
        """Register all specialized model chains."""
        # CodeLlamachain registration
        self.model_chains["code_llama"] = CodeLlamaChain()
        logger.info("Registered CodeLlamaChain")

        # self.model_chains["customizable"] = CustomizableChain()
        # logger.info("Registered CustomizableChain")
    

        #more chains added here
    
    def _get_provider_from_model(self, model: str) -> str:
        """
        Determine the provider from the model name.
        
        Format can be either:
        - "provider:model" (e.g., "ollama:llama2")
        - Just "model" (will use default provider)
        """
        if ":" in model:
            provider, _ = model.split(":", 1)
            return provider
        
        # Default to Ollama if no provider specified
        return "ollama"
    
    def _get_model_name(self, model: str) -> str:
        """Extract the actual model name without provider prefix."""
        if ":" in model:
            _, model_name = model.split(":", 1)
            return model_name
        
        return model
    
    def _should_use_specialized_chain(self, model_name: str) -> bool:
        """Does this model require a chain? - This checks that"""
        # First we get the model name without provider prefix
        actual_model = self._get_model_name(model_name).lower()

        # Check if model has a chain
        for chain_model in self.model_chains.keys():
            if chain_model in actual_model:
                return True
        return False
    
    def _get_specialized_chain(self, model_name: str):
        """Gets the chain for the model"""
        actual_model = self._get_model_name(model_name).lower()

        for chain_model, chain in self.model_chains.items():
            if chain_model in actual_model:
                return chain
        return None
    
    async def generate(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **additional_params
    ) -> Dict[str, Any]:
        """
        Generate a response using the specified model.
        
        Args:
            messages: List of message objects with role and content
            model: Name of the model to use (defaults to configured default)
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum number of tokens to generate
            additional_params: Any additional model-specific parameters
            
        Returns:
            Dict containing response content, model name, and usage information
        """
        # Use default model if none specified
        model_name = model or settings.DEFAULT_MODEL

        if self._should_use_specialized_chain(model_name):
            # get the chain here
            chain = self._get_specialized_chain(model_name)
            logger.info(f"Using specialized chain {chain.__class__.__name__} for model {model_name}")

            # Generate reply with chain
            response = await chain.run(
                messages=messages,
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                **additional_params
            )

            return response


        # Determine which provider to use
        provider = self._get_provider_from_model(model_name)
        
        # Get the actual model name (without provider prefix)
        actual_model = self._get_model_name(model_name)
        
        # Check if we have a handler for this provider
        if provider not in self.model_handlers:
            raise ValueError(f"Unsupported model provider: {provider}")
        
        # Use the appropriate handler to generate the response
        handler = self.model_handlers[provider]
        
        try:
            response = await handler.generate(
                messages=messages,
                model=actual_model,
                temperature=temperature,
                max_tokens=max_tokens,
                **additional_params
            )
            
            return {
                "content": response["content"],
                "model": model_name,  # Return the full model name with provider
                "usage": response.get("usage", {})
            }
        except Exception as e:
            logger.error(f"Error generating response with model {model_name}: {str(e)}")
            raise