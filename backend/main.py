"""
RehabSense Backend - FastAPI Application Entry Point

This module initializes the FastAPI application, configures CORS middleware
for frontend integration, and includes all API routers.

The backend runs on http://localhost:8000 and serves the frontend at http://localhost:3000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import session, websocket

# Initialize FastAPI application
app = FastAPI(
    title="RehabSense API",
    description="AI Physiotherapy Platform Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware to allow frontend requests
# Frontend runs on http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# All routes will be prefixed with /api
app.include_router(session.router, prefix="/api", tags=["sessions"])
app.include_router(websocket.router, prefix="/api", tags=["websocket"])


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    
    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to RehabSense API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "rehabsense-backend"}


if __name__ == "__main__":
    """
    Run the server using uvicorn when executed directly.
    
    Usage:
        python main.py
        or
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
