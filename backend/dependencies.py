# ✅ dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend import auth
from backend.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    import backend.models as models
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_role(*allowed_roles):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return checker