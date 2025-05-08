# ✅ seed_toolkits.py
from backend.db_base import Base
from backend.database import engine, SessionLocal
from sqlalchemy import Column, String, Integer

class Toolkit(Base):
    __tablename__ = "toolkits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    link = Column(String)
    role = Column(String)

Base.metadata.create_all(bind=engine)
db = SessionLocal()
db.query(Toolkit).delete()

toolkits = [
    Toolkit(title="Values Clarification Tool", description="Identify core values", link="https://example.com/values", role="user"),
    Toolkit(title="Weekly Reflection Journal", description="Structured reflection journal", link="https://example.com/journal", role="user"),
    Toolkit(title="Coach Feedback Tracker", description="Track feedback provided", link="https://example.com/coach-feedback", role="coach"),
    Toolkit(title="Admin Analytics Dashboard", description="Full analytics access", link="https://example.com/admin-analytics", role="admin"),
]

db.add_all(toolkits)
db.commit()
db.close()

print("✅ Toolkits seeded successfully.")
