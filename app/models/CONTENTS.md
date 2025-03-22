### Models Directory
- Contains **data structures** and schemas
- Defines **what** data looks like
- Example: `Message`, `AgentRequest`, `AgentResponse` classes
- These are primarily Pydantic models that define shapes of data

## Architectural Pattern

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Models      │     │   Services    │     │     API       │
│  (Structure)  │◄────┤  (Behavior)   │◄────┤  (Interface)  │
└───────────────┘     └───────────────┘     └───────────────┘
```
