# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import user  # Adjust if your path is different

app = FastAPI(
    title="ALIGN Coaching API",
    description="Backend API for the ALIGN Coaching Platform",
    version="1.0.0"
)

# Allow frontend access (adjust origins for production security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/user", tags=["User"])

# Health check endpoint (optional but useful)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "ALIGN Coaching API is running"}
