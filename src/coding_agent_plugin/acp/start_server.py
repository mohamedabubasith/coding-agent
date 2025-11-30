#!/usr/bin/env python3
"""Start the ACP server to expose agents over HTTP REST API.

This script registers all agents with the IBM ACP Server and starts
the server to make them accessible via HTTP.

Usage:
    python -m coding_agent_plugin.acp.start_server
    
Or:
    agentic-coder serve
"""

import asyncio
from coding_agent_plugin.agents.planning import PlanningAgent
from coding_agent_plugin.agents.coding import CodingAgent
from coding_agent_plugin.agents.execution import ExecutionAgent
from coding_agent_plugin.agents.task import TaskAgent
from coding_agent_plugin.agents.error import ErrorAgent
from coding_agent_plugin.acp.server import register_agents, start_acp_server


async def main():
    """Initialize agents and start the ACP server."""
    print("🤖 Initializing agents...")
    
    # Create agent instances
    planning_agent = PlanningAgent(name="planning")
    coding_agent = CodingAgent(name="coding")
    execution_agent = ExecutionAgent(name="execution")
    task_agent = TaskAgent(name="task")
    error_agent = ErrorAgent(name="error")
    
    print("✅ Agents initialized:")
    print("   • Planning Agent")
    print("   • Coding Agent")
    print("   • Execution Agent")
    print("   • Task Agent")
    print("   • Error Agent")
    
    # Register agents with ACP server
    print("\n📝 Registering agents with ACP Server...")
    await register_agents(
        planning_agent=planning_agent,
        coding_agent=coding_agent,
        execution_agent=execution_agent,
        task_agent=task_agent,
        error_agent=error_agent
    )
    print("✅ All agents registered")
    
    # Start the ACP server
    print("\n🚀 Starting ACP Server...")
    print("📡 Agents will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    start_acp_server()


if __name__ == "__main__":
    asyncio.run(main())
