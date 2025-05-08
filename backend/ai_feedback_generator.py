# ✅ AI Feedback Engine (ai_feedback_generator.py)
def generate_ai_feedback(content: str) -> str:
    content = content.lower()
    if "stress" in content or "anxiety" in content:
        return "You seem stressed. Consider taking a break or journaling more."
    elif "happy" in content:
        return "Great to see your positive mood. Reflect on what caused it."
    else:
        return "Keep up the good reflections."