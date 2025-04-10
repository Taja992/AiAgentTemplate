from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    """A message in a conversation with a model."""
    # C# equivalent: public required string Role { get; set; }
    # The '...' means this field is required (no default value)
    role: str = Field(..., description="The role of the messeng sender (ex. 'user, 'assistant', 'system').")
    
    # C# equivalent: public required string Content { get; set; }
    content: str = Field(..., description="The content of the message.")

class AgentRequest(BaseModel):
    """    Represents the complete request from a client to the agent.
    
    Similar to C# API controller request model.
    Contains all parameters needed to generate a response, including
    conversation history, model selection, and generation parameters."""
    # C# equivalent: public required List<Message> Messages { get; set; }
    messages: List[Message] = Field(..., description="List of conversation messages")
    
    # C# equivalent: public string? Model { get; set; } = null;
    model: Optional[str] = Field(None, description="Model to use for generating response (Like ollama:llama2)")
    
    # C# equivalent: public float Temperature { get; set; } = 0.7f;
    temperature: float = Field(0.7, description="Creativity parameter (0-1)")
    
    # C# equivalent: public int MaxTokens { get; set; } = 1000;
    max_tokens: int = Field(1000, description="Maximum number of tokens to generate")
    
    # C# equivalent: public Dictionary<string, object> AdditionalParams { get; set; } = new Dictionary<string, object>();
    # default_factory=dict means "initialize with an empty dictionary"
    additional_params: Dict[str, Any] = Field(default_factory=dict, description="Additional model-specific parameters")


class TokenUsage(BaseModel):
    """Tracks Token usage info from model reply"""
    # C# equivalent: public int? PromptTokens { get; set; } = null;
    prompt_tokens: Optional[int] = None
    
    # C# equivalent: public int? CompletionTokens { get; set; } = null;
    completion: Optional[int] = None
    
    # C# equivalent: public int? TotalTokens { get; set; } = null;
    total_tokens: Optional[int] = None

class AgentResponse(BaseModel):
    """Response schema for agent interactions"""
    # C# equivalent: public required string Response { get; set; }
    response: str = Field(..., description="Response from the model")
    
    # C# equivalent: public required string Model { get; set; }
    model: str = Field(..., description="Model used for generating the response")
    
    # C# equivalent: public Dictionary<string, object> Usage { get; set; } = new Dictionary<string, object>();
    usage: Dict[str, Any] = Field(default_factory=dict, description="Token usage information")

class OllamaModel(BaseModel):
    """Schema for Ollama model information"""
    id: str = Field(..., description="Model identifier(format: ollama:{model_name})")
    name: str = Field(..., description="Model name")
    size: Any = Field(..., description="Model size in bytes")
    modified_at: Optional[str] = Field(None, description="Last modified date of the model")
    description: Optional[str] = Field(None, description="Description of the model")