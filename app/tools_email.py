# app/tools_email.py
"""
Email tools for MCP Email Assistant.

For this assignment version, we run in DEMO mode:
- Emails are loaded from sample_emails.json (local file)
- No real IMAP/SMTP connection is required
You can later switch DEMO_MODE = False and implement real IMAP logic.
"""

import json
import os
from typing import List
from email.message import EmailMessage

from .models import MessageSummary, GetMessageResponse
from .config import settings

DEMO_MODE = True  # keep True for assignment demo

SAMPLE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "sample_emails.json"
)

def _load_demo_emails():
    if not os.path.exists(SAMPLE_FILE):
        return []
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def list_unread(username: str, password: str, folder: str = "INBOX", limit: int = 20) -> List[MessageSummary]:
    """
    DEMO: Return emails from sample_emails.json as 'unread'.
    """
    emails = _load_demo_emails()
    summaries: List[MessageSummary] = []
    for e in emails[:limit]:
        summaries.append(
            MessageSummary(
                uid=str(e["uid"]),
                subject=e["subject"],
                from_=e["from"],
                to=e.get("to", []),
                date=e.get("date", ""),
                snippet=e.get("snippet", ""),
            )
        )
    return summaries

async def get_message(username: str, password: str, uid: str, folder: str = "INBOX") -> GetMessageResponse:
    """
    DEMO: Return full email details from sample_emails.json by uid.
    """
    emails = _load_demo_emails()
    for e in emails:
        if str(e["uid"]) == str(uid):
            return GetMessageResponse(
                uid=str(e["uid"]),
                subject=e["subject"],
                from_=e["from"],
                to=e.get("to", []),
                date=e.get("date", ""),
                body_text=e.get("body_text", ""),
                body_html=None,
                attachments=[],
            )
    # not found
    return GetMessageResponse(
        uid=str(uid),
        subject="(not found)",
        from_="",
        to=[],
        date="",
        body_text="",
        body_html=None,
        attachments=[],
    )

async def send_message_smtp(username: str, password: str, message: EmailMessage):
    """
    DEMO: Instead of actually sending, just print to console.
    """
    print("=== DEMO send_message_smtp ===")
    print("From:", message["From"])
    print("To:", message["To"])
    print("Subject:", message["Subject"])
    print("Body:", message.get_content())
    print("=== END DEMO ===")
    # In a real implementation you would call aiosmtplib.send(...) here.
