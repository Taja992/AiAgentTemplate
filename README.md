# AI Agent Template

A flexible, modular API for interacting with various AI models through a unified interface.

## Architecture Flow

The AI Agent Template follows a clean, layered architecture with clear separation of concerns:

```mermaid
graph TD
    %% API Layer
    A[Client Request] -->|HTTP Request| B[FastAPI Endpoint]
    B -->|Input Validation| C[API Router]
    
    %% Service Layer 
    C -->|Request| D[AgentService]
    D -->|Process Request| E[ModelService]
    
    %% Model Provider Layer
    E -->|Provider Selection| F{Provider?}
    F -->|Ollama| G[OllamaModelHandler]
    F -->|Future Provider| H[Other Providers]
    
    %% Model Interaction
    G -->|API Call| I[Ollama API]
    H -->|API Call| J[Other Model APIs]
    
    %% Response Flow
    I -->|Response| K[Model Response]
    J -->|Response| K
    K -->|Processed Response| E
    E -->|Model Result| D
    D -->|Agent Response| C
    C -->|HTTP Response| B
    B -->|JSON Response| A
    
    %% Optional Components
    L[Configuration] -.->|Settings| D
    L -.->|Settings| E
    L -.->|Settings| G
    
    M[Logging] -.->|Log Events| D
    M -.->|Log Events| E
    M -.->|Log Events| G
```

## Key Components

- **API Layer**: Handles HTTP requests and routes them to appropriate services
- **Agent Service**: Orchestrates the processing of requests
- **Model Service**: Manages access to different model providers
- **Model Handlers**: Provider-specific implementations for model interaction

## Features

- Unified API for multiple AI model providers
- Extensible architecture for adding new model providers
- Consistent interface regardless of underlying model
- Configurable settings for model parameters
- Comprehensive logging

### Intelligent Model Selection

The Agent Service includes content-based model routing:

- Code-related tasks → CodeLlama
- Creative content → Mistral
- Mathematical queries → Llama2
- Translation tasks → DeepSeek-R1
- General queries → Default model (configurable)

### Supported Model Providers

- **Ollama**: Local model deployment with support for:
  - Llama2
  - CodeLlama
  - Mistral
  - DeepSeek-R1
  
- **Future Providers**:
  - Architecture prepared for LM Studio
  - Support for additional cloud-based models