import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from functools import partial
from bson import ObjectId
import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection

from app.models.schemas import Message
from app.services.memory.base import BaseMemory
from app.utils.logger import get_logger

logger = get_logger(__name__)

class MongoMemory(BaseMemory):
    """
    MongoDB-based memory storage for persistent conversation history.
    
    This memory storage uses MongoDB to store conversation messages,
    allowing for long-term persistence across application restarts.
    """

    def __init__(self,
                 connection_string: str = "mongodb://localhost:27017",
                 db_name: str = "agent_conversations"):
        """
        Initializes MongoDB connection. 
        
        Args:
            connection_string: MongoDB connection URI
            db_name: Name of the database to use
        """
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        self.messages_collection = None

        self._initialize_connection()

        logger.info(f"Initialized MongoDB memory with db: {db_name}")

    def _initialize_connection(self) -> None:
        """ Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.messages_collection = self.db["messages"]

            # Create indexes for efficient querying
            self.messages_collection.create_index([
                ("conversation_id", pymongo.ASCENDING),
                ("timestamp", pymongo.DESCENDING)
            ])

            logger.info("Successfully connected to MongoDB:")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise

    def _message_to_doc(self, message: Message, conversation_id: str) -> Dict[str, Any]:
        """ Convert a Message to a MongoDB doc."""
        return {
            "role": message.role,
            "content": message.content,
            "conversation_id": conversation_id,
            "timestamp": datetime.now()
        }

    def _doc_to_message(self, doc: Dict[str, Any]) -> Message:
        """ Convert a MongoDB document to a message object."""
        return Message(
            role=doc["role"],
            content=doc["content"]
        )
    
    async def save_message(self, message: Message, conversation_id: str = "default") -> None:
        """
        Save a message to MongoDB.
        
        Args:
            message: The message to save
            conversation_id: Identifier for the conversation
        """
        doc = self._message_to_doc(message, conversation_id)

        try:
            # Run MongoDB operations in a thread pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.messages_collection.insert_one(doc)
            )
            logger.debug(f"Saved message to MongoDB for conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Failed to save message to MongoDB: {str(e)}")
            raise

    async def load_messages(self, conversation_id: str = "default", limit: Optional[int] = None) -> List[Message]:
        """
        Load messages from MongoDB.
        
        Args:
            conversation_id: Identifier for the conversation
            limit: Max number of messages to load 
            
        Returns:
            List of messages (oldest first)
        """
        try:
            loop = asyncio.get_event_loop()

            # Define the pipeline for finding and sorting messages
            # We want oldest first for conversation history
            cursor_function = partial(
                self.messages_collection.find,
                {"conversation_id": conversation_id}
            )

            # Get documents from MongoDB
            docs = await loop.run_in_executor(
                None,
                lambda: list(cursor_function().sort("timestamp", pymongo.ASCENDING).limit(limit or 0))
            )

            # Convert to message 
            messages = [self._doc_to_message(doc) for doc in docs]
            logger.debug(f"Loaded {len(messages)} messages from MongoDB for conversation {conversation_id}")
            return messages
        except Exception as e:
            logger.error(f"Failed to load messages from MongoDB: {str(e)}")
            raise

    async def load_recent_messages(self, conversation_id: str = "default", limit: int = 10) -> List[Message]:
        """
        Load most recent messages from MongoDB.
        
        Args:
            conversation_id: Identifier for the conversation
            limit: Max number of messages to load


        returns:
            List of messages (oldest first)
        """
        try:
            loop = asyncio.get_event_loop()

            # First get the most recent messages in reverse order
            cursor_function = partial(
                self.messages_collection.find,
                {"conversation_id": conversation_id}
            )

            # Get documents from MongoDB (Newest first)
            docs = await loop.run_in_executor(
                None,
                lambda: list(cursor_function().sort("timestamp", pymongo.DESCENDING).limit(limit))
            )

            # Reverse to get chronologicail order (Oldest first)
            docs.reverse()

            # Convert to Message objects

            messages = [self._doc_to_message(doc) for doc in docs]
            logger.debug(f"Loaded {len(messages)} recent messages from MongoDB for conversation {conversation_id}")
            return messages
        except Exception as e:
            logger.error(f"Failed to load recent messages from MongoDB: {str(e)}")
            raise

    async def clear_conversation(self, conversation_id: str = "default") -> None:
        """
        Clear all messages for a conversation.
        
        Args:
            conversation_id: Identifier for the conversation to clear
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.messages_collection.delete_many({"conversation_id": conversation_id})
            )
            logger.info(f"Cleared {result.deleted_count} messages for conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Failed to clear conversation from MongoDB: {str(e)}")
            raise

    async def delete_message(self, message_id: str, conversation_id: str = "default") -> None:
        """
        Delete a specific message.
        
        Args:
            message_id: ID of the message to delete
            conversation_id: Identifier for the conversation
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.messages_collection.delete_one({
                    "_id": ObjectId(message_id),
                    "conversation_id": conversation_id
                })
            )
            logger.debug(f"Deleted message {message_id} from conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Failed to delete message from MongoDB: {str(e)}")
            raise

    async def get_all_conversation_ids(self) -> List[str]:
        """
        Get all available conversation IDs.
        
        Returns:
            List of unique conversation IDs
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.messages_collection.distinct("conversation_id")
            )
            return result
        except Exception as e:
            logger.error(f"Failed to get conversation IDs from MongoDB: {str(e)}")
            raise


