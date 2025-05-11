from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db
from backend import models, auth
from backend.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["User"])

# ----------------------------
# Schemas
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

    hashed_pw = get_password_hash(user.password)
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
# Login Route (expects form data)
# ----------------------------

@router.post("/login", response_model=TokenOut)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------------
# Get Current User Info
# ----------------------------

@router.get("/me", response_model=UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# ----------------------------
# Get User by ID (Admin Use)
# ----------------------------

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
