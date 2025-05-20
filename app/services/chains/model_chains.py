from typing import List, Dict, Any, Optional
import asyncio
from functools import partial

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama

from app.services.chains.base import BaseChain
from app.models.schemas import Message
from app.utils.logger import get_logger

logger = get_logger(__name__)

class CodeLlamaChain(BaseChain):
    """Chain for CodeLlama that enforces programming-focused responses."""

    async def run(
            self,
            messages: List[Message],
            model: str,
            temperature: float = 0.7,
            max_tokens: int = 1000,
            **kwargs
    ) -> Dict[str, Any]:
        # Prompt template to follow
        system_message = """You are a professional programming assistant specializing in:
        
        1. Providing clear, efficient code examples
        2. Explaining programming concepts and algorithms
        3. Debugging and fixing code problems
        4. Suggesting best practices for software development
        
        Focus exclusively on programming-related topics. If asked about non-programming subjects,
        politely redirect to programming assistance. Prioritize clarity, correctness, and 
        educational value in your responses."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        model_name = model.split(":", 1)[1] if ":" in model else model


        # Create the LangChain LLM
        llm = ChatOllama(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Create and run the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Convert messages to history format
        history = [{"role": msg.role, "content": msg.content} for msg in messages[:-1]]

        # Get the last user message as input
        input_message = next ((msg.content for msg in reversed(messages) if msg.role.lower() == "user" ), "")

        try:
            # Run in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(chain.invoke, {"history": history, "input": input_message})
            )

            return {
                "content": response["text"] if isinstance(response, dict) and "text" in response else response,
                "model": model,
                "usage": {}
            }
        except Exception as e:
            logger.error(f"Error in CodeLlamaChain: {str(e)}")
            raise


class CustomizableChain(BaseChain):
    """
    A configurable chain that allows for dynamic system messages
    can be updated via the API
    """

    def __init__(self):
        """Initialize with default config"""
        self.system_message = "You are a helpful AI assistant."
        self.parameters = {}
        self.enabled = False

    def update_configuration(self, system_message: str = None, parameters: dict = None, enabled: bool = None):
        """ Update the chain's config with the new sys message and params"""
        if system_message is not None:
            self.system_message = system_message

        if parameters is not None:
            self.parameters = parameters
        
        if enabled is not None:
            self.enabled = enabled

        
    async def run(
            self,
            messages: List[Message],
            model: str,
            temperature: float = 0.7,
            max_tokens: int = 1000,
            **kwargs
    ) -> Dict[str, Any]:
        """Run the chain with configured system message and params
        """

        processed_messages = messages.copy()
        
        
        # Check for existing system messages
        has_system_message = any(msg.role.lower() == "system" for msg in processed_messages)
        
        # Always add system message when chain is used via API parameter
        if not has_system_message and self.system_message:
            processed_messages.insert(0, Message(role="system", content=self.system_message))
    
        # Extract model name without provider
        if ":" in model:
            provider, model_name = model.split(":", 1)
        else:
            provider = "ollama"  # default
            model_name = model

        # Extract just the base model without version tags
        # For "gemma3:1b", use "gemma3"
        base_model = model_name.split(":")[0] if ":" in model_name else model_name
        
        logger.info(f"Using model {base_model} for CustomizableChain")

        try:
            # Use direct API call to Ollama instead of ChatOllama
            from app.services.model_providers.ollama import OllamaModelHandler
            
            # Prepare messages with system prompt if needed
            messages_to_send = processed_messages.copy()
            
            # Get handler
            handler = OllamaModelHandler()
            
            # Use the handler to generate a response
            response = await handler.generate(
                messages=messages_to_send,
                model=model_name,  # Use full model name as your handler already handles it
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                "content": response["content"],
                "model": model,
                "usage": response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"Error in CustomizableChain: {str(e)}")
            raise

