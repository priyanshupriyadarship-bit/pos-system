"""
Task Model - Database schema for tasks
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from backend.models.database import Base
import enum

class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    avatar_name = Column(String(100), nullable=True)
    xp_reward = Column(Integer, default=10)
    estimated_minutes = Column(Integer, nullable=True)
    actual_minutes = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, default=False)
    is_quest = Column(Boolean, default=False)
    source = Column(String(50), nullable=True)
    source_id = Column(String(255), nullable=True)
    paei_tag = Column(String(10), nullable=True)
    goal_id = Column(String(36), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "avatar_name": self.avatar_name,
            "xp_reward": self.xp_reward,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
