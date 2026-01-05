"""Database Connection and ORM Setup"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/pos.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import models here so Base knows about them
    from backend.models.user_model import User
    from backend.models.task_model import Task
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def reset_db():
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All database tables dropped")

if __name__ == "__main__":
    print(f"Database URL: {DATABASE_URL}")
    init_db()
