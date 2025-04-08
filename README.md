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
    D <-->|Store/Retrieve Messages| N[MemoryService]
    
    %% RAG System - UPDATED
    C -->|RAG Request| W[RAG Router]
    W -->|Document Processing/Query| X[RAGService]
    X -->|Embedding Generation| Y[OllamaEmbeddingService]
    X -->|Document Storage| Z[DocumentStore]
    X -->|Vector Search| AA[VectorStore]
    X -->|Document Retrieval| AB[Retriever]
    X -->|Document Splitting| AC[DocumentSplitter]
    X -->|File Loading| AD[FileLoader]
    Z -.->|Persistence| AE[(File System)]
    AA -.->|FAISS Index| AF[(Vector DB)]
    
    %% Collection Management - NEW
    C -->|Collection Management| W
    W -->|List Collections| X
    W -->|Delete Collection| X
    W -->|Retrieve from Collection| X
    
    %% AgentService-RAG Integration - NEW
    D <-->|Retrieve Relevant Documents| X
    X -->|Document Context| D
    D -->|Context-Augmented Request| E
    
    %% Memory Layer
    N -->|Short-term Storage| O[ConversationBufferMemoryWrapper]
    N -->|Long-term Storage| P[MongoMemory]
    P <-->|Persistence| Q[(MongoDB)]
    
    %% Model Provider Layer
    E -->|Provider Selection| F{Provider?}
    F -->|Ollama| G[OllamaModelHandler]
    F -->|Future Provider| H[Other Providers]
    E -->|Special Tasks| R[ModelChains]
    R -->|Code Tasks| S[CodeLlamaChain]
    
    %% RAG also uses ModelService
    X -->|Generate Answers| E
    
    %% Model Interaction
    G -->|API Call| I[Ollama API]
    H -->|API Call| J[Other Model APIs]
    Y -->|Embedding API Call| I
    
    %% Response Flow - UPDATED
    I -->|Response| K[Model Response]
    J -->|Response| K
    S -->|Response| K
    K -->|Processed Response| E
    E -->|Model Result| D
    D -->|RAG-Enhanced Response| C
    X -->|RAG Response| W
    W -->|HTTP Response| B
    C -->|HTTP Response| B
    B -->|JSON Response| A
    
    %% Memory Integration with LangChain
    O <-.->|Integration| T[LangChain]
    D <-.->|Create Chains| T
    S <-.->|Uses| T
    AB <-.->|Uses| T
    X <-.->|RetrievalQA Chain| T
    
    %% Optional Components
    L[Configuration] -.->|Settings| D
    L -.->|Settings| E
    L -.->|Settings| G
    L -.->|Settings| N
    L -.->|Settings| X
    
    %% Logging
    M[Logging] -.->|Log Events| D
    M -.->|Log Events| E
    M -.->|Log Events| G
    M -.->|Log Events| N
    M -.->|Log Events| O
    M -.->|Log Events| P
    M -.->|Log Events| X
    M -.->|Log Events| Y
    M -.->|Log Events| Z
    M -.->|Log Events| AA
    M -.->|Log Events| AB
    
    %% Conversation Management
    U[Conversation IDs] -.->|Organizes| N
    N -.->|List All Convos| V[API Endpoints]
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

# Breaking Down the Mermaid Diagram

1. **Core System Architecture**: Shows the basic request-response flow and main service components
2. **Model Provider Architecture**: Focuses on model selection and interaction
3. **Memory System Architecture**: Details the dual-layer memory system
4. **RAG System Architecture**: Highlights RAG components and their integration

## 1. Core System Architecture

```mermaid
graph TD
    %% API Layer
    A[Client Request] -->|HTTP Request| B[FastAPI Endpoint]
    B -->|Input Validation| C[API Router]
    
    %% Service Layer 
    C -->|Request| D[AgentService]
    D -->|Process Request| E[ModelService]
    D <-->|Store/Retrieve Messages| N[MemoryService]
    D <-->|Retrieve Documents| X[RAGService]
    
    %% Collections Endpoints - NEW
    C -->|Collection Management| W[RAG Router]
    W -->|List Collections| X
    W -->|Delete Collection| X
    W -->|Retrieve from Collection| X
    
    %% Response Flow (Simplified)
    E -->|Model Result| D
    D -->|RAG-Enhanced Response| C
    C -->|HTTP Response| B
    B -->|JSON Response| A
    
    %% Configuration & Logging
    L[Configuration] -.->|Settings| D
    L -.->|Settings| E
    L -.->|Settings| N
    L -.->|Settings| X
    M[Logging] -.->|Log Events| D
    M -.->|Log Events| E
    M -.->|Log Events| N
    M -.->|Log Events| X
```

## 2. Model Provider Architecture

```mermaid
graph TD
    %% Model Provider Layer
    E[ModelService] -->|Provider Selection| F{Provider?}
    F -->|Ollama| G[OllamaModelHandler]
    F -->|Future Provider| H[Other Providers]
    E -->|Special Tasks| R[ModelChains]
    R -->|Code Tasks| S[CodeLlamaChain]
    
    %% Model Interaction
    G -->|API Call| I[Ollama API]
    H -->|API Call| J[Other Model APIs]
    
    %% Response Flow
    I -->|Response| K[Model Response]
    J -->|Response| K
    S -->|Response| K
    K -->|Processed Response| E
    
    %% AgentService-RAG Integration - UPDATED
    D[AgentService] -->|Context-Augmented Request| E
    D <-->|Retrieve Relevant Documents| X[RAGService]
    X -->|Document Context| D
    
    %% LangChain Integration
    S <-.->|Uses| T[LangChain]
    
    %% Configuration & Logging
    L[Configuration] -.->|Settings| E
    L -.->|Settings| G
    L -.->|Settings| D
    M[Logging] -.->|Log Events| E
    M[Logging] -.->|Log Events| G
    M[Logging] -.->|Log Events| D
```

## 3. Memory System Architecture

```mermaid
graph TD
    %% Memory Service
    D[AgentService] <-->|Store/Retrieve Messages| N[MemoryService]
    
    %% Memory Components
    N -->|Short-term Storage| O[ConversationBufferMemoryWrapper]
    N -->|Long-term Storage| P[MongoMemory]
    P <-->|Persistence| Q[(MongoDB)]
    
    %% Memory Integration & Management
    O <-.->|Integration| T[LangChain]
    U[Conversation IDs] -.->|Organizes| N
    N -.->|List All Convos| V[API Endpoints]
    
    %% Configuration & Logging
    L[Configuration] -.->|Settings| N
    M[Logging] -.->|Log Events| N
    M -.->|Log Events| O
    M -.->|Log Events| P
```

## 4. RAG System Architecture

```mermaid
graph TD
    %% RAG API - UPDATED
    C[API Router] -->|RAG Request| W[RAG Router]
    W -->|Document Processing/Query| X[RAGService]
    
    %% Collection Management - NEW
    W -->|List Collections| X
    W -->|Delete Collection| X
    W -->|Retrieve from Collection| X
    
    %% Agent Integration - UPDATED
    D[AgentService] <-->|Document Retrieval| X
    X -->|Context Documents| D
    D -->|Enhance Prompts| E[ModelService]
    
    %% RAG Components
    X -->|Embedding Generation| Y[OllamaEmbeddingService]
    X -->|Document Storage| Z[DocumentStore]
    X -->|Vector Search| AA[VectorStore]
    X -->|Document Retrieval| AB[Retriever]
    X -->|Document Splitting| AC[DocumentSplitter]
    X -->|File Loading| AD[FileLoader]
    
    %% RAG Persistence
    Z -.->|Persistence| AE[(File System)]
    AA -.->|FAISS Index| AF[(Vector DB)]
    
    %% RAG Integration with Models
    X -->|Generate Answers| E
    Y -->|Embedding API Call| I[Ollama API]
    
    %% RAG Response Flow
    X -->|RAG Response| W
    W -->|HTTP Response| B[FastAPI Endpoint]
    
    %% LangChain Integration
    AB <-.->|Uses| T[LangChain]
    X <-.->|RetrievalQA Chain| T
    
    %% Configuration & Logging
    L[Configuration] -.->|Settings| X
    M[Logging] -.->|Log Events| X
    M -.->|Log Events| Y
    M -.->|Log Events| Z
    M -.->|Log Events| AA
    M -.->|Log Events| AB
```

