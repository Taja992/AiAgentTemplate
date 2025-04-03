from typing import List, Dict, Any, Optional
from app.models.schemas import Message
from app.services.memory.mongo_memory import MongoMemory
from app.services.memory.buffer_memory import ConversationBufferMemoryWrapper
from app.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryService:
    """
    Service for managing conversation memory using both short and long term memory storage.
    
    Short-term: Langchain's ConversationBufferMemory for active conversations
    Long-term: MongoDB for persistent memory storage
    """


    def __init__(self, use_mongo: bool = True, connection_string: str = "mongodb://localhost:27017/"):
        """
        Initialize memory service with short and long term storage


        Args:
            use_mongo: Flag to use MongoDB for long-term memory
            connection_string: MongoDB connection string
        """
        # Initialize buffer memory (always used)
        self.buffer_memory = ConversationBufferMemoryWrapper()

        self.use_mongo = use_mongo
        self.mongo_memory = None

        if use_mongo:
            try:
                self.mongo_memory = MongoMemory(connection_string=connection_string)
                logger.info("Initialized MongoDB memory")
            except Exception as e:
                logger.error(f"Failed to initialize MongoDB memory: {str(e)}")
                logger.warning("Falling back to buffer memory only")
                self.use_mongo = False

    async def save_message(self, message: Message, conversation_id: str = "default") -> None:
        """
        Save a message to both short and long term memory
        
        
        Args:
            message: The message to save
            conversation_id: Unique ID for the conversation
        """
        # Always save to buffer memory
        await self.buffer_memory.save_message(message, conversation_id)

        # Save to MongoDB if enabled

        if self.use_mongo and self.mongo_memory:
            try:
                await self.mongo_memory.save_message(message, conversation_id)
            except Exception as e:
                logger.error(f"Failed to save message to MongoDB: {str(e)}")

    
    async def load_recent_messages(self, conversation_id: str = "default", limit: int = 20) -> List[Message]:
        """
        Load recent messages for conversation, preferring MongoDB if available.
        
        Args:
            conversation_id: Unique ID for the conversation
            limit: Number of messages to load (default is 20)
            
        Returns:
            List of messages
        """
        if self.use_mongo and self.mongo_memory:
            try:
                return await self.mongo_memory.load_recent_messages(conversation_id, limit)
            except Exception as e:
                logger.error(f"Failed to load messages from MongoDB: {str(e)}")
                logger.warning("falling back to buffer memory")

        # Fall back to buffer memory
        return await self.buffer_memory.load_messages(conversation_id, limit)
    
    async def load_all_messages(self, conversation_id: str = "default") -> List[Message]:
        """
        Load all messages for a conversation, preferring MongoDB
        
        
        Args:
            conversation_id: Unique ID for the conversation
            
            
        Returns:
            List of messages
        """
        if self.use_mongo and self.mongo_memory:
            try:
                return await self.mongo_memory.load_messages(conversation_id)
            except Exception as e:
                logger.error(f"Failed to load messages from MongoDB: {str(e)}")
                logger.warning("Falling back to buffer memory")

        # Fall back to buffer memory
        return await self.buffer_memory.load_messages(conversation_id)
    
    async def clear_conversation(self, conversation_id: str = "default") -> None:
        """
        Clear all messages from both memory stores
        
        Args:
            conversation_id: Unique ID for the conversation
        """

        await self.buffer_memory.clear_conversation(conversation_id)

        if self.use_mongo and self.mongo_memory:
            try:
                await self.mongo_memory.clear_conversation(conversation_id)
            except Exception as e:
                logger.error(f"Failed to clear conversation in MongoDB: {str(e)}")


    async def get_conversation_ids(self) -> List[str]:
        """
        Get all available conversation IDs from MongoDB
        
        Returns:
            List of unique conversation IDs
        """
        if self.use_mongo and self.mongo_memory:
            try:
                return await self.mongo_memory.get_all_conversation_ids()
            except Exception as e:
                logger.error(f"Failed to get conversation IDs from MongoDB: {str(e)}")
        
        logger.warning("Cannot retrieve all conversation IDs from MongoDB")
        return []
    
    def get_langchain_memory(self, conversation_id: str = "default") -> Any:
        """
        Get the LangChain memory object for use with Langchain Components.
        
        Args:
            conversation_id: Unique ID for the conversation
            
            
        Returns:
            Langchain-compatible memory object"""
        return self.buffer_memory.get_langchain_memory(conversation_id)

            

