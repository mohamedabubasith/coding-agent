"""Coding agent for generating code."""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent


class CodingAgent(BaseAgent):
    """Agent responsible for generating code based on user prompt."""

    def __init__(self, name: str, openapi_instance: Any = None):
        super().__init__(name, openapi_instance)
        from coding_agent_plugin.core.config import LLM_MODEL, LLM_BASE_URL, LLM_API_KEY
        model_name = LLM_MODEL or "gpt-4o"
        
        # Set up ChatOpenAI with custom base_url and api_key if using NVIDIA or other providers
        kwargs = {"model": model_name, "temperature": 0.2}
        if LLM_API_KEY:
            kwargs["api_key"] = LLM_API_KEY
        if LLM_BASE_URL:
            kwargs["base_url"] = LLM_BASE_URL
            
        self.model = ChatOpenAI(**kwargs)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the coding task."""
        user_prompt = task.get("user_prompt")
        project_id = task.get("project_id")
        file_path_relative = task.get("file_path") # Optional: specific file to write to
        
        if not user_prompt or not project_id:
            raise ValueError("Missing user_prompt or project_id")

        self.log(f"Generating code for: {user_prompt}")
        
        existing_content = None
        if file_path_relative:
            full_path = os.path.join(f"projects/{project_id}", file_path_relative)
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    existing_content = f.read()
        
        code_content = await self.generate_code(user_prompt, existing_content)
        
        saved_path = self.save_code(project_id, code_content, file_path_relative)
        
        return {"file_path": saved_path, "code": code_content}

    async def generate_code(self, prompt: str, existing_content: str | None = None) -> str:
        """Generate code using LLM."""
        system_content = """You are an expert coding assistant. Generate clean, production-ready code for the given task.
IMPORTANT RULES:
- Return ONLY the code itself
- Do NOT include any markdown formatting (no ```python or ``` blocks)
- Do NOT include explanations or comments outside the code
- Write complete, working code that can be directly executed
"""
        
        user_content = prompt
        if existing_content:
            user_content += f"\n\nExisting content of the file:\n{existing_content}\n\nPlease update the code based on the request."
            
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=user_content)
        ]
        
        response = await self.model.ainvoke(messages)
        raw_content = response.content
        
        # Log the raw response for debugging
        self.log(f"Raw LLM response length: {len(raw_content)} chars")
        
        # Strip markdown code blocks if present
        import re
        
        # Remove markdown code blocks (```language ... ``` or ``` ... ```)
        # Find content between triple backticks
        code_block_pattern = r"```(?:\w+)?\n?(.*?)```"
        matches = re.findall(code_block_pattern, raw_content, re.DOTALL)
        
        if matches:
            # Use the first code block found
            cleaned_content = matches[0].strip()
            self.log(f"Extracted code from markdown block: {len(cleaned_content)} chars")
        else:
            # No code blocks found, use the entire content
            cleaned_content = raw_content.strip()
            
        if not cleaned_content:
            self.log("WARNING: Generated code is empty!")
            
        return cleaned_content

    def save_code(self, project_id: str, content: str, filename: str | None = None) -> str:
        """Save code to a file."""
        directory = f"projects/{project_id}"
        os.makedirs(directory, exist_ok=True)
        
        if not filename:
            filename = "generated_code.py" # Default filename
            
        # Ensure filename doesn't start with / to avoid absolute path issues
        if filename.startswith("/"):
            filename = filename[1:]
            
        file_path = os.path.join(directory, filename)
        
        # Ensure subdirectories exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        mode = "w"
        if os.path.exists(file_path):
            # "If the file already exists, it should update the file instead of creating a new one."
            # 'w' mode overwrites, which effectively updates.
            pass
            
        with open(file_path, mode) as f:
            f.write(content)
            
        return file_path
