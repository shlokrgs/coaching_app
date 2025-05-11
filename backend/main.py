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
    allow_origins=["*"],  # ⚠️ Replace with allowed domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Locate the static build directory (Vite output)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"

# Mount /static (optional, already served via fallback below)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include API routes
app.include_router(user.router, prefix="/user", tags=["User"])

# Serve frontend for all non-API routes (catch-all)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    """
    Serves the frontend index.html for any route not starting with /user or /static.
    This supports client-side routing in React/Vite apps.
    """
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    else:
        return {"error": "Frontend not built yet. Please run `npm run build`."}
