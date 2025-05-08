from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from backend.database import get_db
from backend.dependencies import require_role, get_current_user
from backend import schemas

router = APIRouter(prefix="/coach-notes", tags=["Coach Notes"])

@router.post("/", response_model=schemas.CoachNoteOut)
def create_coach_note(
    note: schemas.CoachNoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("coach", "admin"))
):
    import backend.models as models

    reflection = db.query(models.Reflection).filter(models.Reflection.id == note.reflection_id).first()
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")

    user = db.query(models.User).filter(models.User.id == reflection.user_id).first()
    if user.coach_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not assigned to this user")

    new_note = models.CoachNote(
        reflection_id=note.reflection_id,
        coach_id=current_user.id,
        content=note.content,
        created_at=datetime.utcnow()
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/{reflection_id}", response_model=list[schemas.CoachNoteOut])
def get_notes_for_reflection(
    reflection_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("coach", "admin"))
):
    import backend.models as models

    reflection = db.query(models.Reflection).filter(models.Reflection.id == reflection_id).first()
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")

    user = db.query(models.User).filter(models.User.id == reflection.user_id).first()
    if user.coach_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    notes = db.query(models.CoachNote).filter(models.CoachNote.reflection_id == reflection_id).all()
    return notes

@router.delete("/{note_id}")
def delete_coach_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("coach", "admin"))
):
    import backend.models as models
    note = db.query(models.CoachNote).filter(models.CoachNote.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.coach_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You cannot delete this note")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
