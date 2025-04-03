from typing import List, Dict, Any, Optional
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage

from app.models.schemas import Message
from app.services.memory.base import BaseMemory
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ConversationBufferMemoryWrapper(BaseMemory):
    """
    Wrapper for LangChain's ConversationBufferMemory.
    
    This provides a short-term memory storage for active conversations,
    implementing the BaseMemory interface.
    """

    def __init__(self):
        """Initialize the buffer memory."""
        # Dictionary to store conversatoin memory objects for each conversation ID
        self.memories: Dict[str, ConversationBufferMemory] = {}
        logger.info("Initialized ConversationBufferMemoryWrapper")

    def _get_or_create_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Get an existing memory or create a new one for the conversation ID."""
        if conversation_id not in self.memories:
            self.memories[conversation_id] = ConversationBufferMemory(
                return_messages=True,
                ai_prefix="assistant",  # This needs to match the message schema
                human_prefix="user"
            )
            logger.debug(f"Created new buffer memory for conversation ID: {conversation_id}")

        return self.memories[conversation_id]
    
    def _convert_to_langchain_message(self, message: Message) -> BaseMessage:
        """Convert our message model to a langchain message."""
        role = message.role.lower()

        if role == "user":
            return HumanMessage(content=message.content)
        elif role == "assistant":
            return AIMessage(content=message.content)
        elif role == "system":
            return SystemMessage(content=message.content)
        else:
            # Default to HumanMessage if role is unknown
            logger.warning(f"Unknown role '{role}' in message. Defaulting to HumanMessage.")
            return HumanMessage(content=message.content)
        

    def _convert_from_langchain_message(self, message: BaseMessage) -> Message:
        """Convert a langchain message back to our message model."""
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        elif isinstance(message, SystemMessage):    
            role = "system"
        else:
            logger.warning(f"Unknown langchain message type '{type(message)}'. Defaulting to HumanMessage.")
            role = "user"

        return Message(role=role, content=message.content)
    
    async def save_message(self, message: Message, conversation_id: str = "default") -> None:
        """
        Save a message to the buffer memory.
        
        
        Args:
            message: the message to save
            conversation_id: Unique ID for the conversation
        """
        memory = self._get_or_create_memory(conversation_id)

        # Save to memory based on role

        role = message.role.lower()
        if role == "user":
            memory.chat_memory.add_user_message(message.content)
        elif role == "assistant":
            memory.chat_memory.add_ai_message(message.content)
        elif role == "system":
            # System messages aren't directly supported by ConversationBufferMemory
            # If needed add custom handling
            logger.warning("System messages are not directly supported in ConversationBufferMemory.")
            pass
        else:
            logger.warning(f"Unknown message role: {role}. Message not saved.")

        logger.debug(f"Saved {role} message to buffer memory for conversation {conversation_id}")


    async def load_messages(self, conversation_id: str = "default", limit: Optional[int] = None) -> List[Message]:
        """
        Load messages from the buffer memory.
        
        
        Args:
            conversation_id: Unique ID for the conversation
            limit: Max number of messages to load (ignored in buffer memory)
            
            
        Returns:
            List of messages
        """
        memory = self._get_or_create_memory(conversation_id)

        # Get messages from memory

        langchain_messages = memory.chat_memory.messages

        # Convert to our message model

        messages = [self._convert_from_langchain_message(msg) for msg in langchain_messages]

        # Apply limit if provided
        if limit is not None and limit > 0:
            messages = messages[-limit:]

        logger.debug(f"Loaded {len(messages)} messages from buffer memory for conversation {conversation_id}")
        return messages
    

    async def clear_conversation(self, conversation_id: str = "default") -> None:
        """
        Clear all messages for a conversation.
        
        
        Args:
            conversation_id: Identifier for the conversation to clear
        """
        if conversation_id in self.memories:
            self.memories[conversation_id].clear()
            logger.info(f"Cleared buffer memory for conversation {conversation_id}")
        else:
            logger.debug(f"No buffer memory found for conversation {conversation_id}")


    async def delete_message(self, message_id: str, conversation_id: str = "default") -> None:
        """
        Delete a specific message from memory.
        
        Note: ConversionBufferMemory doesn't support deleting individual messages.
        This is a stub implementation to satisfy the BaseMemory interface.
        Args:
            message_id: ID of the message to delete
            conversation_id: Identifier for the conversation
        """
        # Not implemented in buffer memory
        logger.warning("Delete message not implemented in buffer memory.")
        


    def get_langchain_memory(self, conversation_id: str = "default") -> ConversationBufferMemory:
        """
        Get the LangChain memory object for a specific conversation ID.
        
        
        Args:
            conversation_id: Unique ID for the conversation
            
            
        Returns:
            LangChain ConversationBufferMemory object
        """
        return self._get_or_create_memory(conversation_id)
    
    
