from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.dependencies import get_current_user, require_role
from backend.database import get_db
from backend import schemas, models

router = APIRouter(prefix="/coach", tags=["Coach"])


@router.get("/dashboard", response_model=list[schemas.UserOut])
def get_assigned_users(
        db: Session = Depends(get_db),
        current_user=Depends(require_role("coach", "admin")),
        limit: int = Query(50, le=100),
        offset: int = 0
):
    query = db.query(models.User)
    if current_user.role == "coach":
        query = query.filter(models.User.coach_id == current_user.id)
    return query.offset(offset).limit(limit).all()


@router.get("/user-reflections/{user_id}", response_model=list[schemas.ReflectionOut])
def get_user_reflections(
        user_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_role("coach", "admin")),
        limit: int = Query(50, le=100),
        offset: int = 0
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role == "coach" and user.coach_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    reflections = db.query(models.Reflection) \
        .filter(models.Reflection.user_id == user_id) \
        .order_by(models.Reflection.created_at.desc()) \
        .offset(offset).limit(limit).all()

    return reflections
