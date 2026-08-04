"""
===========================================================
Project : AI SQL Generator
File    : main.py
Author  : Praveen
===========================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import router
from app.logger import get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------
# Application Startup
# -----------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup Events
    """

    logger.info("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Application Started Successfully")

    yield

    logger.info("Application Shutdown")


# -----------------------------------------------------------
# FastAPI App
# -----------------------------------------------------------
app = FastAPI(
    title="AI SQL Generator",
    description="""
Generate SQL from Natural Language using LLMs.

Features

- Generate SQL
- Validate SQL
- Execute SQL
- Explain SQL
- Query History
- Health Check
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# -----------------------------------------------------------
# CORS
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Change in Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
# Include Routers
# -----------------------------------------------------------
app.include_router(router)


# -----------------------------------------------------------
# Root API
# -----------------------------------------------------------
@app.get("/", tags=["Home"])
def home():
    """
    Home Endpoint
    """

    return {
        "application": "AI SQL Generator",
        "version": "1.0.0",
        "status": "Running",
        "swagger": "/docs",
    }


# -----------------------------------------------------------
# Health Check
# -----------------------------------------------------------
@app.get("/health", tags=["Health"])
def health():
    """
    Health Check Endpoint
    """

    return {
        "status": "Healthy"
    }


# -----------------------------------------------------------
# Run Application
# -----------------------------------------------------------
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
