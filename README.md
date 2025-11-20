**MCP Email Automation Assistant**

An AI-powered email automation system built using Model Context Protocol (MCP), FastAPI, and OpenAI.
This assistant reads emails, categorizes them, and generates smart AI replies with adjustable tone and custom instructions.

**Features**
Email Automation

Read inbox emails using IMAP

Categorize emails by priority

Draft AI-generated replies

Adjustable tone (formal, friendly, urgent, etc.)

Short or long reply styles

**MCP Integration**

MCP server-style structure

Tools exposed as clean API endpoints

Context-aware reply generation

**Security**

Secrets not stored in GitHub

.env ignored using .gitignore

Email configuration stored securely

Safe IMAP/SMTP access handling

Project Structure
mcp-email-assistant/
│── app/
│   ├── main.py           # FastAPI endpoints (MCP tools)
│   ├── ai_utils.py       # OpenAI reply generator
│   ├── tools_email.py    # IMAP/SMTP email tools
│   ├── models.py         # Request/Response models
│   ├── config.py         # Environment variable loader
│── sample_emails.json.txt
│── .gitignore
│── requirements.txt
│── README.md

**Setup Instructions**

1. Create Virtual Environment
python -m venv venv

2. Activate Virtual Environment (Windows)
.\venv\Scripts\Activate.ps1

3. Install Dependencies
pip install -r requirements.txt

4. Create .env File
OPENAI_API_KEY=your_key_here
IMAP_HOST=imap.gmail.com
SMTP_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

Note: This file must not be committed to GitHub.

Running the Server
python -m uvicorn app.main:app --reload --port 8000

API Endpoints (Swagger UI)

Open in browser:

http://127.0.0.1:8000/docs

**Available Tools**
Tool Name	Endpoint	Description
List Emails	/tools/list_unread	Fetch unread inbox emails
Get Email	/tools/get_message	Retrieve a specific email
Draft Reply	/tools/draft_reply	Generate an AI-based reply
