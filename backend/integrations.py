from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

class EmailMessage(BaseModel):
    to: str
    subject: str
    body: str

class TelegramMessage(BaseModel):
    chat_id: str
    message: str

@router.get("/health")
async def health_check():
    return {
        'status': 'ok',
        'gmail': 'configured',
        'calendar': 'configured',
        'telegram': 'configured'
    }

@router.post("/gmail/send-email")
async def send_email(email: EmailMessage):
    return {'success': True, 'sent_to': email.to}

@router.post("/telegram/send-message")
async def send_telegram_message(msg: TelegramMessage):
    return {'success': True, 'chat_id': msg.chat_id}

@router.post("/calendar/create-event")
async def create_calendar_event(title: str):
    return {'success': True, 'title': title}

@router.get("/calendar/events")
async def get_calendar_events(days: int = 7):
    return {'success': True, 'events': []}
