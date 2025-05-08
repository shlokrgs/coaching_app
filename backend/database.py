# ✅ database.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.db_base import Base
from backend.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    from backend import models
    Base.metadata.create_all(bind=engine)

