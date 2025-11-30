"""Audit Manager for logging events to database."""

from typing import Dict, Any, Optional
from coding_agent_plugin.schemas.audit import AuditLog
from coding_agent_plugin.managers.project_manager import get_db_session

class AuditManager:
    """
    Manages audit logging to the database.
    """
    
    def __init__(self):
        pass

    async def log_event(self, event_type: str, data: Dict[str, Any], project_id: Optional[str] = None) -> None:
        """
        Log an event to the audit database.
        
        Args:
            event_type: Type of event (e.g., 'agent_start', 'code_generated')
            data: Event data/payload
            project_id: Optional project ID context
        """
        try:
            with get_db_session() as session:
                log_entry = AuditLog(
                    project_id=project_id,
                    event_type=event_type,
                    data=data,
                    source="agentic-coder"
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            # Silently fail or log to stderr, don't crash the agent
            print(f"[Audit] Error saving log: {str(e)}")
