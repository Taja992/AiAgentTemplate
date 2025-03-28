from app.services.model_service import ModelService
from app.services.agent_service import AgentService

# Create singleton instances
model_service = ModelService()
agent_service = AgentService(model_service)

def get_agent_service():
    """Dependency to get the agent service."""
    return agent_service