# ✅ models.py
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from backend.db_base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    reflections = relationship("Reflection", back_populates="user", cascade="all, delete")
    coach = relationship("User", remote_side=[id], backref="assigned_users")

class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    submitted_at = Column(TIMESTAMP, nullable=False)
    last_edited_at = Column(TIMESTAMP, nullable=False)
    is_deleted = Column(Boolean, default=False)
    edit_count = Column(Integer, default=0)
    ai_feedback = Column(Text, nullable=True)

    user = relationship("User", back_populates="reflections")

class Toolkit(Base):
    __tablename__ = "toolkits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    link = Column(String)
    role = Column(String)

# ✅ Coach Notes (models.py)
class CoachNote(Base):
    __tablename__ = "coach_notes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reflection_id = Column(UUID(as_uuid=True), ForeignKey("reflections.id"))
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# ✅ Session Booking (models.py)
class SessionRequest(Base):
    __tablename__ = "session_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    requested_at = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String, default="pending")
    notes = Column(Text)

