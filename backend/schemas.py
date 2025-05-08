from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


# ---------------------
# User Schemas
# ---------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


# ---------------------
# Reflection Schemas
# ---------------------

class ReflectionCreate(BaseModel):
    module_id: int
    content: str


class ReflectionUpdate(BaseModel):
    content: str


class ReflectionOut(BaseModel):
    id: UUID
    module_id: int
    content: str
    submitted_at: datetime
    last_edited_at: datetime
    edit_count: int
    ai_feedback: str | None = None

    model_config = {"from_attributes": True}


# ---------------------
# Toolkit Schema
# ---------------------

class ToolkitOut(BaseModel):
    id: int
    title: str
    description: str
    link: str
    role: str

    model_config = {"from_attributes": True}  # Modern replacement for orm_mode


# ---------------------
# Coach Note Schemas
# ---------------------

class CoachNoteCreate(BaseModel):
    reflection_id: UUID
    content: str


class CoachNoteOut(BaseModel):
    id: UUID
    reflection_id: UUID
    coach_id: UUID
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------
# Session Request Schemas
# ---------------------

class SessionRequestCreate(BaseModel):
    coach_id: UUID
    notes: str | None = None


class SessionRequestUpdate(BaseModel):
    status: str  # e.g., "approved", "rejected", "pending"


class SessionRequestOut(BaseModel):
    id: UUID
    user_id: UUID
    coach_id: UUID
    requested_at: datetime
    status: str
    notes: str | None = None

    model_config = {"from_attributes": True}
