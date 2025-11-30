from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from coding_agent_plugin.models.agent import AgentRunRequest, AgentRunResponse
from coding_agent_plugin.services.agent import agent_service
import json
import logging

router = APIRouter(prefix="/agent", tags=["Agent"])
logger = logging.getLogger(__name__)

@router.post("/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest):
    """Run the agent via HTTP request."""
    try:
        result = await agent_service.run_agent(
            mode=request.mode,
            prompt=request.prompt,
            project_id=request.project_id
        )
        return AgentRunResponse(
            status=result.get("status", "completed"),
            results=result,
            project_id=request.project_id
        )
    except Exception as e:
        logger.error(f"Agent run failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for agent interaction."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")
                
                if action == "run":
                    project_id = message.get("project_id")
                    prompt = message.get("prompt")
                    mode = message.get("mode", "autonomous")
                    
                    if not project_id or not prompt:
                        await websocket.send_json({"status": "error", "message": "Missing project_id or prompt"})
                        continue
                        
                    await websocket.send_json({"status": "started", "message": "Agent started"})
                    
                    # Run agent
                    try:
                        result = await agent_service.run_agent(
                            mode=mode,
                            prompt=prompt,
                            project_id=project_id
                        )
                        await websocket.send_json({
                            "status": "completed", 
                            "results": result,
                            "project_id": project_id
                        })
                    except Exception as e:
                        logger.error(f"Agent run failed: {e}")
                        await websocket.send_json({"status": "failed", "error": str(e)})
                        
                elif action == "ping":
                    await websocket.send_json({"status": "pong"})
                else:
                    await websocket.send_json({"status": "error", "message": "Unknown action"})
                    
            except json.JSONDecodeError:
                await websocket.send_json({"status": "error", "message": "Invalid JSON"})
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
