from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# =========================
# Simple "AI-style" reply generator (NO OpenAI)
# =========================

def generate_reply(subject: str, body: str, tone: str, instructions: str) -> str:
    """
    Offline, rule-based reply generator for demo.
    Builds a reply using subject, tone and extra instructions.
    """
    tone = (tone or "neutral").lower()

    if "friendly" in tone:
        opening = "Hi,\n\nThanks for your email."
    elif "professional" in tone:
        opening = "Dear Sir/Madam,\n\nThank you for your message."
    elif "casual" in tone:
        opening = "Hey,\n\nThanks for reaching out!"
    else:
        opening = "Hello,\n\nThank you for contacting me."

    core = (
        f"\n\nRegarding your email about \"{subject}\", "
        f"I have read the details and will respond/act accordingly."
    )

    extra = ""
    if instructions:
        extra = f"\n\nNote: {instructions}"

    closing = "\n\nBest regards,\nSurya"

    return opening + core + extra + closing


# =========================
# Pydantic models
# =========================

class MessageSummary(BaseModel):
    uid: str
    subject: str
    from_: str
    to: List[str] = []
    date: str = ""
    snippet: str = ""


class ListRequest(BaseModel):
    username: str
    password: str
    limit: int = 20


class GetRequest(BaseModel):
    username: str
    password: str
    uid: str


class DraftRequest(BaseModel):
    username: str
    password: str
    uid: str
    tone: Optional[str] = "neutral"
    instructions: Optional[str] = ""


class DraftResponse(BaseModel):
    uid: str
    draft_subject: str
    draft_body: str


class SendRequest(BaseModel):
    username: str
    password: str
    to: List[str]
    subject: str
    body: str


class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPDiscoverResponse(BaseModel):
    tools: List[MCPTool]


# =========================
# Demo email data (in-memory)
# =========================

DEMO_EMAILS = {
    "1": {
        "subject": "Project submission deadline",
        "from_": "teacher@example.com",
        "to": ["ramamarni4@gmail.com"],
        "date": "2025-11-20 10:00",
        "body": "Hi student, please submit your AI assignment by tomorrow. "
                "Let me know if you have any questions.",
        "snippet": "Please submit your AI assignment by tomorrow..."
    },
    "2": {
        "subject": "Interview schedule",
        "from_": "hr@company.com",
        "to": ["ramamarni4@gmail.com"],
        "date": "2025-11-18 16:30",
        "body": "We would like to invite you for an interview. "
                "Please share your availability.",
        "snippet": "We would like to schedule your interview..."
    },
    "3": {
        "subject": "College fest invitation",
        "from_": "events@college.edu",
        "to": ["ramamarni4@gmail.com"],
        "date": "2025-11-15 09:15",
        "body": "You are invited to join the college tech fest happening this weekend!",
        "snippet": "You are invited to participate in the tech fest..."
    },
}


# =========================
# FastAPI app
# =========================

app = FastAPI(
    title="MCP Email Assistant",
    version="1.0",
    description="Demo email automation assistant using MCP."
)


# =========================
# MCP Discover endpoint
# =========================

@app.get("/mcp/discover", response_model=MCPDiscoverResponse)
async def mcp_discover():
    """
    MCP entrypoint: describes available tools.
    """
    tools = [
        MCPTool(
            name="list_unread",
            description="List unread emails (demo inbox).",
            input_schema={"type": "object", "properties": {"limit": {"type": "integer"}}},
        ),
        MCPTool(
            name="get_message",
            description="Get full message content by UID (demo inbox).",
            input_schema={"type": "object", "properties": {"uid": {"type": "string"}}},
        ),
        MCPTool(
            name="draft_reply",
            description="Generate an AI-style draft reply for a message.",
            input_schema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "tone": {"type": "string"},
                    "instructions": {"type": "string"},
                },
            },
        ),
        MCPTool(
            name="send_message",
            description="Send an email (demo: prints to console).",
            input_schema={
                "type": "object",
                "properties": {
                    "to": {"type": "array", "items": {"type": "string"}},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
            },
        ),
    ]
    return MCPDiscoverResponse(tools=tools)


# =========================
# Tools: list_unread
# =========================

@app.post("/tools/list_unread", response_model=List[MessageSummary])
async def api_list_unread(req: ListRequest):
    """
    DEMO: Return list of unread emails from DEMO_EMAILS.
    """
    summaries: List[MessageSummary] = []
    for uid, data in list(DEMO_EMAILS.items())[: req.limit]:
        summaries.append(
            MessageSummary(
                uid=uid,
                subject=data["subject"],
                from_=data["from_"],
                to=data["to"],
                date=data["date"],
                snippet=data["snippet"],
            )
        )
    return summaries


# =========================
# Tools: get_message
# =========================

@app.post("/tools/get_message")
async def api_get_message(req: GetRequest):
    """
    DEMO: Return full message content from DEMO_EMAILS by UID.
    """
    msg = DEMO_EMAILS.get(req.uid)
    if not msg:
        return {"error": "Message not found"}

    return {
        "uid": req.uid,
        "subject": msg["subject"],
        "from_": msg["from_"],
        "to": msg["to"],
        "date": msg["date"],
        "body": msg["body"],
    }


# =========================
# Tools: draft_reply
# =========================

@app.post("/tools/draft_reply", response_model=DraftResponse)
async def api_draft_reply(req: DraftRequest):
    """
    Generate an AI-style draft reply without calling OpenAI.
    Uses DEMO_EMAILS + rule-based generator.
    """
    msg = DEMO_EMAILS.get(req.uid)
    if not msg:
        # Fallback for unknown UID
        subject = "Your email"
        body = ""
    else:
        subject = msg["subject"]
        body = msg["body"]

    reply_text = generate_reply(
        subject=subject,
        body=body,
        tone=req.tone or "neutral",
        instructions=req.instructions or "",
    )

    return DraftResponse(
        uid=req.uid,
        draft_subject=f"Re: {subject}",
        draft_body=reply_text,
    )


# =========================
# Tools: send_message
# =========================

@app.post("/tools/send_message")
async def api_send_message(req: SendRequest):
    """
    DEMO: Simulate sending an email by printing it to the console.
    """
    print("\n===== EMAIL SENT (DEMO) =====")
    print("TO:", req.to)
    print("SUBJECT:", req.subject)
    print("BODY:\n", req.body)
    print("=============================\n")

    return {"status": "sent (demo)", "to": req.to}
