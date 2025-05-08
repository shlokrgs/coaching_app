import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import engine
from backend.db_base import Base

# ✅ Routers
from backend.routers import user, coach, module, admin, reflection, coach_note, session_request

# ✅ App Instance
app = FastAPI(title="ALIGN Coaching Web App", version="2.0")

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register Routers
app.include_router(user.router)
app.include_router(coach.router)
app.include_router(module.router)
app.include_router(admin.router)
app.include_router(reflection.router)
app.include_router(coach_note.router)
app.include_router(session_request.router)

# ✅ Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ✅ Auto-create DB tables in development
if os.getenv("ENV") != "production":
    from backend import models
    Base.metadata.create_all(bind=engine)

# ✅ Static Files (React frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print(f"⚠️  Warning: Static directory '{static_dir}' not found.")

# ✅ Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

# ✅ Catch-all route for React Router
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    requested_path = os.path.join(static_dir, full_path)
    if os.path.exists(requested_path) and os.path.isfile(requested_path):
        return FileResponse(requested_path)
    return FileResponse(os.path.join(static_dir, "index.html"))
