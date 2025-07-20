"""
FastAPI application for the content creation workflow.
Provides REST API endpoints for triggering content generation workflows.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.workflow import router as workflow_router

# Create FastAPI application
app = FastAPI(
    title="Content Creation API",
    description="API for generating creative content using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include workflow routes
app.include_router(workflow_router)

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Content Creation API",
        "version": "1.0.0",
        "docs": "/docs"
    }
