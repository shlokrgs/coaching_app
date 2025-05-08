from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend import schemas, auth
from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend.auth import decode_token
from backend import models

router = APIRouter(prefix="/user", tags=["User"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post("/register", status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role=user.role if user.role in ["user", "coach", "admin"] else "user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user_info(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Allow only self or admins to view user profile
    if current_user.id != user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return user
