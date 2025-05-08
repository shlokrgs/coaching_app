from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas
from backend.database import get_db
from datetime import datetime
import uuid
from backend.dependencies import get_current_user
import openai
import os

router = APIRouter(prefix="/reflections", tags=["Reflections"])

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# 🧠 GPT-based feedback engine
def generate_feedback(text: str) -> str:
    try:
        prompt = (
            "You're an expert leadership coach. Given this user reflection, respond with 1–2 personalized insights, encouragement, or questions to deepen their self-awareness and progress."
            f"\n\nReflection:\n{text}\n\nFeedback:"
        )
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an empathetic leadership coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI feedback error:", e)
        return "⚠️ Unable to generate feedback right now. Please try again later."

@router.post("/", response_model=schemas.ReflectionOut)
def create_reflection(
    reflection: schemas.ReflectionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    import backend.models as models
    ai_feedback = generate_feedback(reflection.content)
    new_reflection = models.Reflection(
        id=uuid.uuid4(),
        user_id=current_user.id,
        module_id=reflection.module_id,
        content=reflection.content,
        submitted_at=datetime.utcnow(),
        last_edited_at=datetime.utcnow(),
        ai_feedback=ai_feedback
    )
    db.add(new_reflection)
    db.commit()
    db.refresh(new_reflection)
    return new_reflection

@router.get("/", response_model=list[schemas.ReflectionOut])
def get_all_reflections(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    import backend.models as models
    reflections = db.query(models.Reflection).filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).order_by(models.Reflection.submitted_at.desc()).all()
    return reflections

@router.put("/{reflection_id}", response_model=schemas.ReflectionOut)
def update_reflection(
    reflection_id: uuid.UUID,
    reflection_update: schemas.ReflectionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    import backend.models as models
    reflection = db.query(models.Reflection).filter_by(
        id=reflection_id,
        user_id=current_user.id,
        is_deleted=False
    ).first()

    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")

    reflection.content = reflection_update.content
    reflection.last_edited_at = datetime.utcnow()
    reflection.ai_feedback = generate_feedback(reflection_update.content)
    db.commit()
    db.refresh(reflection)
    return reflection

@router.delete("/{reflection_id}")
def delete_reflection(
    reflection_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    import backend.models as models
    reflection = db.query(models.Reflection).filter_by(
        id=reflection_id,
        user_id=current_user.id
    ).first()

    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")

    reflection.is_deleted = True
    db.commit()
    return {"message": "Reflection deleted"}
