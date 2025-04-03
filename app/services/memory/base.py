from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.schemas import Message

class BaseMemory(ABC):
    """Abstract base class for memory management."""

    @abstractmethod
    async def save_message(self, message: Message, conversation_id: str = "default") -> None:
        """
        Save a message to memory.
        
        Args:
            message: the message to save
            conversation_id: Unique ID for the conversation
        """
        pass

    @abstractmethod
    async def load_messages(self, conversation_id: str = "default", limit: Optional[int] = None) -> List[Message]:
        """
        Load messages from memory.
        
        Args:
            conversation_id: ID for the convo
            limit: Max number of messages to load (newest first)
            
        Returns:
            List of messages
        """
        pass

    @abstractmethod
    async def clear_conversation(self, conversation_id: str = "default") -> None:
        """
        Clear all messages for a conversation.
        
        Args:
            conversation_id: Identifier for the conversation to clear
        """
        pass
    
    @abstractmethod
    async def delete_message(self, message_id: str, conversation_id: str = "default") -> None:
        """
        Delete a specfiic message from memory.
        
        Args:
            message_id: ID of the message to delete
            conversation_id: Identifier for the conversation
        """
        pass