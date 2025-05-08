from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from backend.dependencies import get_current_user, require_role
from backend.database import get_db
from backend import schemas, models
from datetime import datetime
import csv, io

router = APIRouter(prefix="/admin", tags=["Admin"])

# ✅ Dashboard Overview
@router.get("/overview")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    users_count = db.query(models.User).count()
    reflections_count = db.query(models.Reflection).count()
    coach_count = db.query(models.User).filter(models.User.role == "coach").count()
    return {
        "total_users": users_count,
        "total_coaches": coach_count,
        "total_reflections": reflections_count,
        "message": f"Welcome Admin {current_user.email}"
    }

# ✅ Summary Stats
@router.get("/summary")
def get_admin_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return {
        "total_users": db.query(models.User).count(),
        "total_reflections": db.query(models.Reflection).count(),
        "total_sessions": db.query(models.SessionRequest).count(),
        "total_coach_notes": db.query(models.CoachNote).count()
    }

# ✅ Paginated User List
@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
    limit: int = Query(50, le=100),
    offset: int = 0
):
    return db.query(models.User).offset(offset).limit(limit).all()

# ✅ Paginated Reflection List
@router.get("/reflections", response_model=list[schemas.ReflectionOut])
def get_all_reflections(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
    limit: int = Query(50, le=100),
    offset: int = 0
):
    return db.query(models.Reflection).order_by(models.Reflection.submitted_at.desc()).offset(offset).limit(limit).all()

# ✅ Export: Reflections CSV
@router.get("/export-reflections")
def export_reflections_csv(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "Module ID", "Content", "Submitted At", "AI Feedback"])
    for r in db.query(models.Reflection).all():
        writer.writerow([r.user_id, r.module_id, r.content, r.submitted_at, r.ai_feedback])
    return Response(content=output.getvalue(), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=reflections_export.csv"
    })

# ✅ Export: Users CSV
@router.get("/export-users")
def export_users_csv(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Role"])
    for u in db.query(models.User).all():
        writer.writerow([u.id, u.name, u.email, u.role])
    return Response(content=output.getvalue(), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=users_export.csv"
    })

# ✅ Export: Sessions CSV
@router.get("/export-sessions")
def export_sessions_csv(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "Coach ID", "Requested At", "Status", "Notes"])
    for s in db.query(models.SessionRequest).all():
        writer.writerow([s.user_id, s.coach_id, s.requested_at, s.status, s.notes])
    return Response(content=output.getvalue(), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=sessions_export.csv"
    })
