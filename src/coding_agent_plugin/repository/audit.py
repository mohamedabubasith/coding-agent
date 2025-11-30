from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from coding_agent_plugin.core.database import db_manager
from coding_agent_plugin.schemas.audit import AuditLog
from coding_agent_plugin.models.audit import AuditLogCreate

class AuditRepository:
    """Repository for AuditLog database operations."""

    async def create_audit_log(self, audit_in: AuditLogCreate) -> AuditLog:
        """Create a new audit log entry."""
        async with db_manager.session_factory() as session:
            new_audit = AuditLog(
                project_id=audit_in.project_id,
                event_type=audit_in.event_type,
                data=audit_in.data,
                source=audit_in.source
            )
            session.add(new_audit)
            await session.commit()
            await session.refresh(new_audit)
            return new_audit

    async def list_audit_logs(self, project_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """List audit logs, optionally filtered by project."""
        async with db_manager.session_factory() as session:
            stmt = select(AuditLog).offset(skip).limit(limit)
            
            if project_id:
                stmt = stmt.where(AuditLog.project_id == project_id)
                
            result = await session.execute(stmt)
            return result.scalars().all()

audit_repository = AuditRepository()
