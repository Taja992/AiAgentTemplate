from typing import List, Dict, Any, Optional
from app.models.schemas import Message, AgentResponse
from app.services.model_service import ModelService
from app.services.memory_service import MemoryService
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
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
    
    def __init__(self, model_service: ModelService, memory_service: MemoryService = None):
        """
        Initialize the agent service with a model service.
        
        Args:
            model_service: Service that handles interactions with different LLM providers
        """
        self.model_service = model_service
        self.memory_service = memory_service

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
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        conversation_id: str = "default",
        skip_memory: bool = False,
        **additional_params
        ) -> AgentResponse:

        """
        Process a chat request, automatically selecting the best model if none specified.
    
        Args:
            messages: List of message objects with role and content
            model: Name of the model to use (if None, will be auto-selected)
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum number of tokens to generate
            conversation_id: Unique ID for convo
            additional_params: Any additional model-specific parameters
        
        Returns:
            AgentResponse with the model's response
        """
        # Only use memory if not skipping
        # If we have memory service, save the latest user message to memory
        if self.memory_service and not skip_memory:
            # Find the latest user message
            for msg in reversed(messages):
                if msg.role.lower() == "user":
                    logger.debug(f"Saving user message to conversation {conversation_id}")
                    await self.memory_service.save_message(msg, conversation_id)
                    break

        if self.memory_service and not skip_memory:
            # Load prior conversation history
            conversation_history = await self.memory_service.load_recent_messages(conversation_id)
            # If we have history, prepend it to the current messages (except the last one)
            if conversation_history and len(conversation_history) > 1:
                # Remove the most recent message since it's already in 'messages'
                conversation_history = conversation_history[:-1]
                messages = conversation_history + messages
                logger.debug(f"Loaded {len(conversation_history)} messages from memory for conversation {conversation_id}")


        # Auto-select model if none provided
        if model is None:
            model = await self.select_model_for_task(messages)
    
        logger.info(f"Processing request with model: {model}")

        task_type = "DEFAULT"
        if model == settings.CODE_MODEL:
            task_type = "CODE"
        elif model == settings.TRANSLATION_MODEL:
            task_type = "TRANSLATION"
        elif model == settings.CREATIVE_MODEL:
            task_type = "CREATIVE"
        elif model == settings.MATH_MODEL:
            task_type = "MATH"

        task_params = settings.TASK_PARAMS.get(task_type, settings.TASK_PARAMS["DEFAULT"])

        temp = temperature if temperature is not None else task_params.get("temperature")
        tokens = max_tokens if max_tokens is not None else task_params.get("max_tokens")

        logger.info(f"Using task type: {task_type}, temperature: {temp}, max_tokens: {tokens}")
    
        # Use the model service to get a response
        model_response = await self.model_service.generate(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **additional_params
        )
    
    # Construct and return the response
        response = AgentResponse(
            response=model_response["content"],
            model=model_response["model"],
            usage=model_response.get("usage", {})
        )

        # if we have memory service, save assistant's response
        if self.memory_service and not skip_memory:
            assistant_message = Message(role="assistant", content=response.response)
            logger.debug(f"Saving assistant response to memory for conversation {conversation_id}")
            await self.memory_service.save_message(assistant_message, conversation_id)

        return response
    
    async def create_conversation_chain(self, model: str = None, system_message: str = None):
        """
        Create a LangChain ConversationChain with memory.
        
        Args:
            model: Model to use
            system_message: Optional system message to set context
            
            Returns:
                A LangChain ConversationChain
        """
        if not self.memory_service:
            raise ValueError("Memory service is required for conversation chains")
        
        model_name = model or settings.DEFAULT_MODEL

        # Extract the model name without provider prefix
        if ":" in model_name:
            provider, actual_model = model_name.split(":", 1)
        else:
            actual_model = model_name

        llm = ChatOllama(model=actual_model)

        if system_message:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
        else:
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])

            # Create the chain with memory

        chain = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=self.memory_service.get_langchain_memory(),
            verbose=True
        )

        return chain
    

    async def load_conversation_history(self, conversation_id: str = "default") -> List[Message]:
        """
        Load all messages for a specific conversation
        
        Args:
            conversation_id: Unique ID for the conversation
            
        Returns:
            List of message objects from convo
        """
        if not self.memory_service:
            return []
        return await self.memory_service.load_all_messages(conversation_id)

        

    
