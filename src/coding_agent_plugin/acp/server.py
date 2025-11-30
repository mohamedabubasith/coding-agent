"""ACP Server implementation using IBM's ACP SDK.

This module sets up the Agent Communication Protocol server and wraps
our existing agents to be ACP-compliant.
"""

from typing import AsyncGenerator
from collections.abc import AsyncGenerator as AsyncGen
from acp_sdk.models import Message
from acp_sdk.models.models import MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
import os

# Create the ACP server instance
acp_server = Server()


def format_input_messages(messages: list[Message]) -> dict:
    """Convert ACP Message format to our internal agent format.
    
    Args:
        messages: List of ACP Message objects
        
    Returns:
        Dictionary with user_prompt and other extracted fields
    """
    # Extract content from all message parts
    query = " ".join(
        part.content
        for m in messages
        for part in m.parts
    )
    
    # Parse the query to extract structured data
    # For now, treat the entire query as the user_prompt
    return {
        "user_prompt": query,
    }


def format_output_message(result: dict) -> Message:
    """Convert agent result dict to ACP Message format.
    
    Args:
        result: Agent's response dictionary
        
    Returns:
        ACP-compliant Message object
    """
    # Convert the result dict to a string representation
    content = str(result)
    
    # Create ACP Message with MessagePart
    return Message(parts=[MessagePart(content=content)])


async def register_agents(planning_agent, coding_agent, execution_agent, task_agent, error_agent):
    """Register all agents with the ACP server.
    
    This function wraps existing agents to make them ACP-compliant by:
    1. Converting ACP Message format to internal agent format
    2. Invoking the existing agent
    3. Converting the result back to ACP Message format
    
    Args:
        planning_agent: PlanningAgent instance
        coding_agent: CodingAgent instance
        execution_agent: ExecutionAgent instance
        task_agent: TaskAgent instance
        error_agent: ErrorAgent instance
    """
    
    @acp_server.agent()
    async def planning(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ACP-compliant planning agent."""
        # Convert ACP messages to internal format
        agent_input = format_input_messages(messages)
        
        # Invoke the actual planning agent
        result = await planning_agent.execute(agent_input)
        
        # Convert result to ACP Message
        response_message = format_output_message(result)
        
        # Yield the response
        yield {"messages": [response_message]}
    
    @acp_server.agent()
    async def coding(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ACP-compliant coding agent."""
        # Convert ACP messages to internal format
        agent_input = format_input_messages(messages)
        
        # Invoke the actual coding agent
        result = await coding_agent.execute(agent_input)
        
        # Convert result to ACP Message
        response_message = format_output_message(result)
        
        # Yield the response
        yield {"messages": [response_message]}
    
    @acp_server.agent()
    async def execution(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ACP-compliant execution agent."""
        # Convert ACP messages to internal format
        agent_input = format_input_messages(messages)
        
        # Invoke the actual execution agent
        result = await execution_agent.execute(agent_input)
        
        # Convert result to ACP Message
        response_message = format_output_message(result)
        
        # Yield the response
        yield {"messages": [response_message]}
    
    @acp_server.agent()
    async def task(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ACP-compliant task agent."""
        # Convert ACP messages to internal format
        agent_input = format_input_messages(messages)
        
        # Invoke the actual task agent
        result = await task_agent.execute(agent_input)
        
        # Convert result to ACP Message
        response_message = format_output_message(result)
        
        # Yield the response
        yield {"messages": [response_message]}
    
    @acp_server.agent()
    async def error(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ACP-compliant error agent."""
        # Convert ACP messages to internal format
        agent_input = format_input_messages(messages)
        
        # Invoke the actual error agent
        result = await error_agent.execute(agent_input)
        
        # Convert result to ACP Message
        response_message = format_output_message(result)
        
        # Yield the response
        yield {"messages": [response_message]}


def start_acp_server():
    """Start the ACP server to expose agents over HTTP."""
    print("🚀 Starting ACP Server...")
    print("📡 Agents will be available over HTTP REST API")
    acp_server.run()
