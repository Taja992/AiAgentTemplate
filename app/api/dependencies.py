from app.services.model_service import ModelService
from app.services.agent_service import AgentService
from app.services.memory_service import MemoryService

# Create singleton instances
model_service = ModelService()
memory_service = MemoryService()
agent_service = AgentService(model_service, memory_service)


def get_agent_service():
    """Dependency to get the agent service."""
    return agent_service

def get_memory_service():
    """Dependency for memory service."""
    return memory_service