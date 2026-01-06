import os
import json
from google.oauth2.credentials import Credentials

# ============================================
# GOOGLE CREDENTIALS LOADER
# ============================================
GOOGLE_CREDENTIALS = None
google_token_str = os.environ.get('GOOGLE_TOKEN')

if google_token_str:
    try:
        token_data = json.loads(google_token_str)
        GOOGLE_CREDENTIALS = Credentials(
            token=token_data.get('token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=token_data.get('scopes')
        )
        print("✅ Google credentials loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading Google credentials: {e}")
else:
    print("⚠️ GOOGLE_TOKEN not found in environment variables")

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import httpx
import os

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from email.mime.text import MIMEText
    import base64
    import json
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/calendar']

class EmailMessage(BaseModel):
    to: str
    subject: str
    body: str

class TelegramMessage(BaseModel):
    chat_id: str
    message: str

class CalendarEvent(BaseModel):
    title: str
    start_time: datetime
    duration_minutes: int = 60
    description: Optional[str] = None

def get_google_credentials():
    if not GOOGLE_AVAILABLE:
        return None
    try:
        creds_base64 = os.getenv('GOOGLE_CREDENTIALS_BASE64')
        if creds_base64:
            creds_json = base64.b64decode(creds_base64).decode()
            token = os.getenv('GOOGLE_TOKEN')
            if token:
                return Credentials.from_authorized_user_info(json.loads(token), SCOPES)
        return None
    except Exception as e:
        return None

@router.get("/health")
async def health_check():
    return {"status": "ok", "telegram": "configured" if os.getenv("TELEGRAM_BOT_TOKEN") else "not configured"}

@router.post("/telegram/send-message")
async def send_telegram_message(msg: TelegramMessage):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise HTTPException(status_code=500, detail="Telegram not configured")
    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": msg.chat_id, "text": msg.message})
    return {"success": True, "chat_id": msg.chat_id}

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    data = await request.json()
    if "message" not in data:
        return {"ok": True}
    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    if text.lower() == "/start":
        response_text = "👋 Hello! I'm your POS System Bot!"
    elif text.lower() in ["hello", "hi", "hey"]:
        response_text = "Hi there! 😊"
    elif text.lower() == "help":
        response_text = "🤖 Commands: /start, /help, /status"
    elif text.lower() == "/status":
        response_text = "✅ Online!"
    elif "how are you" in text.lower():
        response_text = "I'm great! 😊"
    else:
        response_text = f"You said: {text}"
    if bot_token:
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": response_text})
    return {"ok": True}

@router.post("/gmail/send-email")
async def send_email(email: EmailMessage):
    if not GOOGLE_AVAILABLE:
        return {"success": False, "error": "Google libraries not installed"}
    creds = get_google_credentials()
    if not creds:
        return {"success": False, "error": "Gmail not configured"}
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(email.body)
        message['to'] = email.to
        message['subject'] = email.subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return {"success": True, "message_id": result['id']}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/calendar/create-event")
async def create_calendar_event(event: CalendarEvent):
    if not GOOGLE_AVAILABLE:
        return {"success": False, "error": "Not installed"}
    creds = get_google_credentials()
    if not creds:
        return {"success": False, "error": "Not configured"}
    try:
        service = build('calendar', 'v3', credentials=creds)
        end_time = event.start_time + timedelta(minutes=event.duration_minutes)
        calendar_event = {'summary': event.title, 'start': {'dateTime': event.start_time.isoformat(), 'timeZone': 'Asia/Kolkata'}, 'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}}
        result = service.events().insert(calendarId='primary', body=calendar_event).execute()
        return {"success": True, "event_id": result['id']}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/calendar/events")
async def get_calendar_events(days: int = 7):
    if not GOOGLE_AVAILABLE:
        return {"success": False, "error": "Not installed"}
    return {"success": True, "events": []}
