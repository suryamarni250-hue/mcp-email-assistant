# app/models.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class MessageSummary(BaseModel):
    uid: str
    subject: str
    from_: str
    to: List[str]
    date: str
    snippet: Optional[str]

class GetMessageResponse(BaseModel):
    uid: str
    subject: str
    from_: str
    to: List[str]
    date: str
    body_text: Optional[str]
    body_html: Optional[str]
    attachments: List[Dict] = []

class DraftRequest(BaseModel):
    uid: str
    tone: Optional[str] = "professional"
    template_name: Optional[str] = None
    brief_instructions: Optional[str] = None

class DraftResponse(BaseModel):
    uid: str
    draft_subject: str
    draft_body: str

class CategorizeResponse(BaseModel):
    uid: str
    category: str
    priority: int
