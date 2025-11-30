from coding_agent_plugin.models.database import get_db_session
from coding_agent_plugin.schemas.audit import AuditLog

print("--- Verifying Audit Logs ---")
with get_db_session() as session:
    logs = session.query(AuditLog).all()
    print(f"Total Logs: {len(logs)}")
    for log in logs:
        print(f"[{log.timestamp}] {log.event_type} (Project: {log.project_id})")
        print(f"  Data: {log.data}")
print("--- End Verification ---")
