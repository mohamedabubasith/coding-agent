from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel

class AuditLogCreate(BaseModel):
    project_id: str | None = None
    event_type: str
    data: Dict[str, Any] = {}
    source: str = "agentic-coder"

class AuditLogResponse(BaseModel):
    id: int
    project_id: str | None
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str

    class Config:
        from_attributes = True
