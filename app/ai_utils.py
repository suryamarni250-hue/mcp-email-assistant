# app/ai_utils.py
import os
from typing import Optional
from .config import settings
# optional OpenAI usage
try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

DEFAULT_PROMPT = """
You are an assistant drafting an email reply. Original subject: {subject}
Original message (text): {body}

Tone: {tone}
Instructions: {instructions}

Write a clear reply, include a short greeting, body, and closing signature.
"""

async def generate_reply(subject: str, body: str, tone: str="professional", instructions: Optional[str]=None) -> str:
    prompt = DEFAULT_PROMPT.format(subject=subject, body=body[:4000], tone=tone, instructions=instructions or "")
    if OPENAI_AVAILABLE:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # replace with your allowed model
            messages=[{"role":"user","content":prompt}],
            max_tokens=400
        )
        return resp.choices[0].message.content.strip()
    # fallback simple heuristic
    return f"Hi,\n\nThanks for your message about '{subject}'.\n\n{instructions or 'I will get back to you shortly.'}\n\nBest regards,\n[Your Name]"
