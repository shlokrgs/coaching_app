from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from backend.database import get_db
from backend.dependencies import get_current_user, require_role

router = APIRouter(prefix="/module", tags=["Module"])


class Toolkit(BaseModel):
    title: str
    description: str
    link: HttpUrl
    role: str


toolkits_data = [
    Toolkit(title="Values Clarification Tool", description="Identify your values", link="https://example.com/values", role="user"),
    Toolkit(title="Weekly Reflection Journal", description="Structured weekly journal", link="https://example.com/journal", role="user"),
    Toolkit(title="Coach Feedback Tracker", description="Coach logs and notes", link="https://example.com/coach-feedback", role="coach"),
    Toolkit(title="Admin Analytics Dashboard", description="Analytics for admins", link="https://example.com/admin-analytics", role="admin"),
]


@router.get("/toolkits", response_model=List[Toolkit])
def get_toolkits(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return [t for t in toolkits_data if t.role == current_user.role]


# --- Module Section ---
class Module(BaseModel):
    id: int
    week_number: int
    title: str
    content: str
    video_link: Optional[HttpUrl] = None
    audio_link: Optional[HttpUrl] = None
    is_published: bool = True


# Simulated module list (should be a DB table)
mock_modules = [
    Module(id=1, week_number=1, title="Self-Awareness", content="Understand yourself deeply.", video_link="https://example.com/video1"),
    Module(id=2, week_number=2, title="Mindfulness", content="Be present in the moment.", audio_link="https://example.com/audio2"),
    # Extend up to week 8...
]


@router.get("/list", response_model=List[Module])
def get_all_modules(current_user=Depends(get_current_user)):
    return [m for m in mock_modules if m.is_published]


@router.post("/upload", response_model=Module)
def upload_module(module: Module, current_user=Depends(require_role("admin"))):
    mock_modules.append(module)  # Replace with DB insert in production
    return module
