### Services Directory
- Contains **business logic** and behaviors
- Defines **how** things work
- Example: `ModelService`, `AgentService` - these process data
- These are classes that perform actions and operations



# Why Use Services Directory Instead of Models Directory

You're going deeper into the services directory because you're implementing **behavior** (how things work), not **structure** (what things are). Here's the key distinction in your architecture:

## Directory Purposes

### Models Directory
- Contains **data structures** and schemas
- Defines **what** data looks like
- Example: `Message`, `AgentRequest`, `AgentResponse` classes
- These are primarily Pydantic models that define shapes of data

### Services Directory
- Contains **business logic** and behaviors
- Defines **how** things work
- Example: `ModelService`, `AgentService` - these process data
- These are classes that perform actions and operations

## Why Model Providers Go in Services

The `model_providers` should be in the services directory because:

1. **They provide functionality**, not just data structure
2. They're an implementation detail of the `ModelService`
3. They represent **how** to interact with different LLM backends
4. They contain behavior code (API calls, processing logic)

## Architectural Pattern

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Models      │     │   Services    │     │     API       │
│  (Structure)  │◄────┤  (Behavior)   │◄────┤  (Interface)  │
└───────────────┘     └───────────────┘     └───────────────┘
```
