from typing import List
from fastapi import APIRouter, status

from coding_agent_plugin.models.audit import AuditLogCreate, AuditLogResponse
from coding_agent_plugin.services.audit import audit_service

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.post("/", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
async def create_audit_log(audit_in: AuditLogCreate):
    """Create a new audit log entry."""
    return await audit_service.create_audit_log(audit_in)

@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    project_id: str | None = None, 
    skip: int = 0, 
    limit: int = 100
):
    """List audit logs, optionally filtered by project."""
    return await audit_service.list_audit_logs(project_id, skip, limit)
