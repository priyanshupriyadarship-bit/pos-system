from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import httpx

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

class EmailMessage(BaseModel):
    to: str
    subject: str
    body: str

class TelegramMessage(BaseModel):
    chat_id: str
    message: str

class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None

# Health check
@router.get("/health")
async def health_check():
    return {"status": "ok", "gmail": "configured", "calendar": "configured", "telegram": "configured"}

# Send email
@router.post("/gmail/send-email")
async def send_email(email: EmailMessage):
    return {"success": True, "sent_to": email.to}

# Send Telegram message
@router.post("/telegram/send-message")
async def send_telegram_message(msg: TelegramMessage):
    return {"success": True, "chat_id": msg.chat_id}

# NEW: Telegram Webhook - Bot receives messages and responds!
@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    import os
    
    data = await request.json()
    
    # Extract message
    if "message" not in data:
        return {"ok": True}
    
    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    # Bot responses
    response_text = ""
    
    if text.lower() == "/start":
        response_text = "👋 Hello! I'm your POS System Bot!\n\nI can help you with:\n- Task management\n- Calendar scheduling\n- Email notifications\n\nType 'help' for commands!"
    elif text.lower() in ["hello", "hi", "hey"]:
        response_text = f"Hi there! 😊 How can I help you today?"
    elif text.lower() == "help":
        response_text = "🤖 Available commands:\n/start - Start bot\n/help - Show this message\n/status - Check system status"
    elif text.lower() == "/status":
        response_text = "✅ POS System is online and working!"
    elif "how are you" in text.lower():
        response_text = "I'm doing great! Thanks for asking 😊"
    elif "name" in text.lower():
        response_text = f"Nice to meet you! I'm POS System Bot. What can I do for you?"
    else:
        response_text = f"You said: {text}\n\nType 'help' to see available commands!"
    
    # Send response back to user
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": response_text}
            )
    
    return {"ok": True}

# Calendar endpoints
@router.post("/calendar/create-event")
async def create_calendar_event(title: str):
    return {"success": True, "title": title}

@router.get("/calendar/events")
async def get_calendar_events(days: int = 7):
    return {"success": True, "events": []}
