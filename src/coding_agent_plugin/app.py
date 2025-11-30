from fastapi import FastAPI
from contextlib import asynccontextmanager
from coding_agent_plugin.core.config import BACKEND_SERVER_REQUIRED
from coding_agent_plugin.core.database import db_manager
from coding_agent_plugin.api.v1.routers import project_routes, audit_routes, agent_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_manager.setup()
    yield
    # Shutdown
    await db_manager.close()

app = FastAPI(
    title="Coding Agent Plugin API",
    description="Backend API for Coding Agent Plugin",
    version="0.1.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(project_routes.router, prefix="/api/v1")
app.include_router(audit_routes.router, prefix="/api/v1")
app.include_router(agent_routes.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "backend_required": BACKEND_SERVER_REQUIRED}
