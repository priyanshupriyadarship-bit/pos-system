import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Global configuration for POS"""
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/pos_db"
    )
    
    # LLM Services
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # Google APIs
    GOOGLE_CALENDAR_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY")
    GOOGLE_GMAIL_API_KEY = os.getenv("GOOGLE_GMAIL_API_KEY")
    
    # Notion
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    
    # Fireflies.ai
    FIREFLIES_API_KEY = os.getenv("FIREFLIES_API_KEY")
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # WHOOP
    WHOOP_API_KEY = os.getenv("WHOOP_API_KEY")
    
    # App config
    DEBUG = os.getenv("DEBUG", "False") == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
