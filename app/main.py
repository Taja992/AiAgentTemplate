from fastapi import FastAPI
from app.api.routes import agent, health
from app.config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)


# Include the agent router
app.include_router(agent.router, prefix="/api")
app.include_router(health.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)