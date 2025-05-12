from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# ✅ Import all routers
from backend.routers import user, reflection, module

app = FastAPI(
    title="ALIGN Coaching API",
    description="Backend API for the ALIGN Coaching Platform",
    version="1.0.0"
)

# ✅ CORS configuration for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static assets (from frontend Vite build)
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# ✅ Register API routers
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(reflection.router, prefix="/reflections", tags=["Reflections"])
app.include_router(module.router, prefix="/module", tags=["Module"])

# ✅ Serve frontend index.html for all unknown routes (SPA fallback)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend():
    index_file = static_dir / "index.html"
    if not index_file.exists():
        raise RuntimeError(f"index.html not found at {index_file}")
    return FileResponse(index_file)
