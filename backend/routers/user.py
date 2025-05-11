from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from backend.database import get_db
from backend import models, auth

router = APIRouter(prefix="/user", tags=["User"])

# ----------------------------
# Pydantic Schemas
# ----------------------------

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----------------------------
# Register Route
# ----------------------------

@router.post("/register", status_code=201)
def register_user(user: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

# ----------------------------
# Login Route (using form or raw JSON)
# ----------------------------

@router.post("/login", response_model=TokenOut)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token(data={"sub": user.email, "user_id": user.id, "role": user.role})
    return {"access_token": token}

# ----------------------------
# Get Current User ID from JWT
# ----------------------------

@router.get("/me")
def get_current_user_id(current_user: models.User = Depends(auth.get_current_user)):
    return {"user_id": current_user.id}

# ----------------------------
# Get Full User by ID
# ----------------------------

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
