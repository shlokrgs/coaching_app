from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend import schemas

router = APIRouter(prefix="/sessions", tags=["Session Booking"])

@router.post("/", response_model=schemas.SessionRequestOut)
def request_session(
    request: schemas.SessionRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("user"))
):
    import backend.models as models

    coach = db.query(models.User).filter(models.User.id == request.coach_id, models.User.role == "coach").first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    new_request = models.SessionRequest(
        user_id=current_user.id,
        coach_id=request.coach_id,
        requested_at=datetime.utcnow(),
        status="pending",
        notes=request.notes
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/assigned", response_model=list[schemas.SessionRequestOut])
def get_assigned_sessions(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("coach", "admin"))
):
    import backend.models as models
    sessions = db.query(models.SessionRequest).filter(models.SessionRequest.coach_id == current_user.id).all()
    return sessions

@router.patch("/{request_id}", response_model=schemas.SessionRequestOut)
def update_session_status(
    request_id: UUID,
    update: schemas.SessionRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("coach", "admin"))
):
    import backend.models as models
    session_request = db.query(models.SessionRequest).filter(models.SessionRequest.id == request_id).first()

    if not session_request:
        raise HTTPException(status_code=404, detail="Session request not found")

    if session_request.coach_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    session_request.status = update.status
    db.commit()
    db.refresh(session_request)
    return session_request

@router.get("/mine", response_model=list[schemas.SessionRequestOut])
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("user"))
):
    import backend.models as models
    sessions = db.query(models.SessionRequest).filter(models.SessionRequest.user_id == current_user.id).all()
    return sessions
