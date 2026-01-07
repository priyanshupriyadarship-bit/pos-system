import os
import json
from google.oauth2.credentials import Credentials

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

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx

router = APIRouter()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

try:
    from googleapiclient.discovery import build
    import base64
    from email.mime.text import MIMEText
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class TelegramMessage(BaseModel):
    chat_id: str
    message: str

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

class CalendarEvent(BaseModel):
    title: str
    start_time: str
    duration_minutes: int = 60

@router.get("/api/integrations/health")
async def health_check():
    health_status = {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z", "services": {"telegram": {"status": "not_configured", "details": None}, "google": {"status": "not_configured", "details": None, "gmail": False, "calendar": False}}}
    if TELEGRAM_BOT_TOKEN:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    bot_info = response.json()
                    health_status["services"]["telegram"]["status"] = "configured"
                    health_status["services"]["telegram"]["details"] = {"bot_username": bot_info.get("result", {}).get("username"), "bot_name": bot_info.get("result", {}).get("first_name")}
        except Exception as e:
            health_status["services"]["telegram"]["status"] = "error"
    if GOOGLE_CREDENTIALS:
        health_status["services"]["google"]["status"] = "configured" if GOOGLE_AVAILABLE else "libraries_not_installed"
        if GOOGLE_AVAILABLE:
            scopes = GOOGLE_CREDENTIALS.scopes if hasattr(GOOGLE_CREDENTIALS, 'scopes') else []
            health_status["services"]["google"]["gmail"] = any("gmail" in s for s in scopes)
            health_status["services"]["google"]["calendar"] = any("calendar" in s for s in scopes)
    telegram_ok = health_status["services"]["telegram"]["status"] == "configured"
    google_ok = health_status["services"]["google"]["status"] == "configured"
    health_status["status"] = "healthy" if telegram_ok and google_ok else ("partial" if telegram_ok or google_ok else "unhealthy")
    return health_status

@router.post("/api/integrations/telegram/send-message")
async def send_telegram_message(message: TelegramMessage):
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="Telegram not configured")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"chat_id": message.chat_id, "text": message.message})
        response.raise_for_status()
        return {"success": True, "chat_id": message.chat_id}

@router.post("/api/integrations/telegram/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient() as client:
            await client.post(url, json={"chat_id": chat_id, "text": f"You said: {text}"})
    return {"ok": True}

@router.post("/api/integrations/gmail/send-email")
async def send_email(email: EmailRequest):
    if not GOOGLE_AVAILABLE or not GOOGLE_CREDENTIALS:
        return {"success": False, "error": "Gmail not configured"}
    try:
        service = build('gmail', 'v1', credentials=GOOGLE_CREDENTIALS)
        message = MIMEText(email.body)
        message['to'] = email.to
        message['subject'] = email.subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return {"success": True, "message_id": result['id']}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/api/integrations/calendar/create-event")
async def create_calendar_event(event: CalendarEvent):
    if not GOOGLE_AVAILABLE or not GOOGLE_CREDENTIALS:
        return {"success": False, "error": "Calendar not configured"}
    try:
        service = build('calendar', 'v3', credentials=GOOGLE_CREDENTIALS)
        start = datetime.fromisoformat(event.start_time.replace('Z', '+00:00'))
        end = start + timedelta(minutes=event.duration_minutes)
        cal_event = {'summary': event.title, 'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'}, 'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'}}
        result = service.events().insert(calendarId='primary', body=cal_event).execute()
        return {"success": True, "event_id": result['id']}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/api/integrations/calendar/events")
async def get_calendar_events(days: int = 7):
    if not GOOGLE_AVAILABLE or not GOOGLE_CREDENTIALS:
        return {"success": False, "error": "Calendar not configured"}
    try:
        service = build('calendar', 'v3', credentials=GOOGLE_CREDENTIALS)
        now = datetime.utcnow().isoformat() + 'Z'
        result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        return {"success": True, "events": result.get('items', [])}
    except Exception as e:
        return {"success": False, "error": str(e)}
