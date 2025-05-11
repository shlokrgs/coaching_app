# ✅ backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend.routers import user

app = FastAPI(
    title="ALIGN Coaching API",
    description="Backend API for the ALIGN Coaching Platform",
    version="1.0.0"
)

# Allow frontend access (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user.router, prefix="/user", tags=["User"])

# Serve frontend static files
app.mount("/static", StaticFiles(directory="backend/static", html=True), name="static")

# Catch-all route to serve frontend index.html
@app.get("/{full_path:path}")
async def serve_frontend():
    return FileResponse(os.path.join("backend/static", "index.html"))
