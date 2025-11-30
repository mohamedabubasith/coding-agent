"""Audit log database schema."""

from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from coding_agent_plugin.schemas.project import Base

class AuditLog(Base):
    """Audit log model for tracking agent activities."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    event_type = Column(String, nullable=False, index=True)
    data = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=func.now())
    source = Column(String, default="agentic-coder")
    
    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source": self.source
        }
