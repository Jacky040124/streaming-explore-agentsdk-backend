"""
FastAPI server startup script.
Run this to start the content creation API server.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )