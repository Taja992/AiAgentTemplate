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
    C -->|RAG Request| RAG[RAG API Router]
    D -->|Process Request| E[ModelService]
    D <-->|Store/Retrieve Messages| N[MemoryService]
    
    %% RAG Components
    RAG -->|Document Processing| R1[RAGService]
    R1 <-->|Vector Search| R2[FAISS VectorStore]
    R1 <-->|Document Storage| R3[FileSystemDocumentStore]
    R1 <-->|Text Embedding| R4[OllamaEmbeddingService]
    R1 <-->|Retrieval| R5[VectorStoreRetriever]
    R1 <-->|Document Splitting| R6[DocumentSplitter]
    R1 <-->|File Processing| R7[FileLoader]
    
    %% Potential Agent-RAG Connection (Not Yet Implemented)
    D -.->|Future Integration| R1
    
    %% Memory Layer
    N -->|Short-term Storage| O[ConversationBufferMemoryWrapper]
    N -->|Long-term Storage| P[MongoMemory]
    P <-->|Persistence| Q[(MongoDB)]
    
    %% Model Provider Layer
    E -->|Provider Selection| F{Provider?}
    F -->|Ollama| G[OllamaModelHandler]
    F -->|Future Provider| H[Other Providers]
    E -->|Special Tasks| X[ModelChains]
    X -->|Code Tasks| S[CodeLlamaChain]
    
    %% Model Interaction
    G -->|API Call| I[Ollama API]
    H -->|API Call| J[Other Model APIs]
    R4 -->|Embedding Request| I
    R1 -->|LLM Request| I
    
    %% Response Flow
    I -->|Response| K[Model Response]
    J -->|Response| K
    S -->|Response| K
    K -->|Processed Response| E
    E -->|Model Result| D
    D -->|Agent Response| C
    C -->|HTTP Response| B
    B -->|JSON Response| A
    
    %% RAG Response Flow
    R2 <-->|Store/Retrieve Vectors| R8[(Vector Files)]
    R3 <-->|Store/Retrieve Documents| R9[(Document Files)]
    R1 -->|RAG Results| RAG
    RAG -->|Document/Answer| B
    
    %% Memory Integration with LangChain
    O <-.->|Integration| T[LangChain]
    D <-.->|Create Chains| T
    S <-.->|Uses| T
    R1 <-.->|RetrievalQA Chain| T
    
    %% Optional Components
    L[Configuration] -.->|Settings| D
    L -.->|Settings| E
    L -.->|Settings| G
    L -.->|Settings| N
    L -.->|Settings| R1
    
    %% Logging
    M[Logging] -.->|Log Events| D
    M -.->|Log Events| E
    M -.->|Log Events| G
    M -.->|Log Events| N
    M -.->|Log Events| O
    M -.->|Log Events| P
    M -.->|Log Events| R1
    M -.->|Log Events| R2
    M -.->|Log Events| R3
    M -.->|Log Events| R4
    M -.->|Log Events| R5
    
    %% Style for Not Yet Implemented Components
    classDef notImplemented fill:#f9f,stroke:#333,stroke-dasharray: 5 5;
    class "D -.->|Future Integration| R1" notImplemented;
    
    %% Component Types
    classDef ragComponents fill:#d4f1f9,stroke:#333;
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 ragComponents;
```

## Key Components

- **API Layer**: Handles HTTP requests and routes them to appropriate services
- **Agent Service**: Orchestrates the processing of requests
- **Model Service**: Manages access to different model providers
- **Model Handlers**: Provider-specific implementations for model interaction
- **Memory Service**: Coordinates short-term and long-term memory storage
- **MongoDB Memory**: Provides persistent storage for conversation history
- **Buffer Memory**: Wraps LangChain's memory for active sessions

## Features

- Unified API for multiple AI model providers
- Extensible architecture for adding new model providers
- Consistent interface regardless of underlying model
- Configurable settings for model parameters
- Comprehensive logging
- Persistent conversation history with MongoDB
- Multi-conversation support with unique IDs
- LangChain integration for advanced chains and memory

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

  ### Memory System

The Agent Template features a dual-layer memory architecture:

- **Short-Term Memory**: Uses LangChain's ConversationBufferMemory for active sessions
  - Fast in-memory storage for current conversations
  - Direct integration with LangChain chains and models
  - Automatically manages conversation context

- **Long-Term Memory**: MongoDB-based persistent storage
  - Stores full conversation history across application restarts
  - Supports multiple conversation IDs for organization
  - Efficient retrieval of recent or complete conversation history

- **Seamless Fallback**: If MongoDB is unavailable, the system continues working with in-memory storage only

### Conversation Management

The system supports multiple simultaneous conversations:

- **Conversation IDs**: Each conversation has a unique identifier
- **Default Conversation**: Conversations without an explicit ID use the "default" conversation
- **History Retrieval**: API support for loading full or recent message history
- **Conversation Listing**: Ability to enumerate all available conversations
- **Conversation Clearing**: Support for clearing conversation history when needed

## Technical Requirements

- **Python 3.9+**
- **MongoDB**: For persistent conversation storage
- **Ollama**: For local model deployment
- **FastAPI**: For API endpoints and request handling
- **LangChain**: For conversation chains and memory integration