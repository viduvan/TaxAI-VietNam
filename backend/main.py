"""
TaxAI Vietnam - Tax Service (FastAPI)
Main entry point for the backend API.
Routes requests to n8n agents and manages data.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from routes import chat, calculator, calendar, updates
from services.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database connection on startup."""
    await init_db()
    yield


app = FastAPI(
    title="TaxAI Vietnam",
    description="Trợ lý thuế TNCN thông minh - Multi-Agent API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(calculator.router, prefix="/api", tags=["Calculator"])
app.include_router(calendar.router, prefix="/api", tags=["Calendar"])
app.include_router(updates.router, prefix="/api", tags=["Updates"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "taxai-service",
        "version": "1.0.0",
    }


@app.get("/api/llm/providers")
async def list_llm_providers():
    """List available LLM providers and current selection."""
    current = os.getenv("LLM_PROVIDER", "ollama")
    return {
        "current": current,
        "available": ["ollama", "openai", "anthropic", "groq"],
    }
