from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

from backend.routers import user

app = FastAPI(
    title="ALIGN Coaching API",
    description="Backend API for the ALIGN Coaching Platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# Include API routes
app.include_router(user.router, prefix="/user", tags=["User"])

# Serve frontend for all non-API routes
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend():
    index_file = static_dir / "index.html"
    if not index_file.exists():
        raise RuntimeError(f"index.html not found at {index_file}")
    return FileResponse(index_file)
