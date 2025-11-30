from typing import List, Optional

from coding_agent_plugin.repository.audit import audit_repository
from coding_agent_plugin.models.audit import AuditLogCreate, AuditLogResponse
from coding_agent_plugin.schemas.audit import AuditLog

class AuditService:
    """Service for managing audit logs."""

    def __init__(self):
        self.repository = audit_repository

    async def create_audit_log(self, audit_in: AuditLogCreate) -> AuditLogResponse:
        """Create a new audit log entry."""
        new_audit = await self.repository.create_audit_log(audit_in)
        return AuditLogResponse.model_validate(new_audit)

    async def list_audit_logs(self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[AuditLogResponse]:
        """List audit logs."""
        logs = await self.repository.list_audit_logs(project_id, skip, limit)
        return [AuditLogResponse.model_validate(log) for log in logs]

audit_service = AuditService()
