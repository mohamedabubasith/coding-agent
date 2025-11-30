from typing import Any, Dict, Optional
from pydantic import BaseModel

class AgentRunRequest(BaseModel):
    project_id: str
    prompt: str
    mode: str = "autonomous"
    config: Optional[Dict[str, Any]] = None

class AgentRunResponse(BaseModel):
    status: str
    results: Any
    project_id: str
