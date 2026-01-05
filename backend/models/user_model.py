"""
User Model - Database schema for users
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from backend.models.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    timezone = Column(String(50), default="UTC")
    llm_provider = Column(String(20), default="openai")
    avatar_stats = Column(JSON, nullable=True)
    total_tasks_completed = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_stats": self.avatar_stats,
            "total_tasks_completed": self.total_tasks_completed,
            "total_xp_earned": self.total_xp_earned,
            "created_at": self.created_at.isoformat()
        }
    
    def update_avatar_stats(self, avatar_name: str, xp_gained: int):
        if not self.avatar_stats:
            self.avatar_stats = {}
        
        if avatar_name not in self.avatar_stats:
            self.avatar_stats[avatar_name] = {"level": 1, "xp": 0, "tasks_completed": 0}
        
        self.avatar_stats[avatar_name]["xp"] += xp_gained
        self.avatar_stats[avatar_name]["tasks_completed"] += 1
        new_level = (self.avatar_stats[avatar_name]["xp"] // 100) + 1
        self.avatar_stats[avatar_name]["level"] = new_level
        self.total_xp_earned += xp_gained
