"""Service for managing LLM prompts."""

class PromptService:
    """Centralized service for managing system prompts and message templates."""
    
    @staticmethod
    def get_planning_system_prompt(files_context: str = "") -> str:
        """Get the system prompt for the Planning Agent."""
        return f"""You are a software architect. Create a comprehensive plan for the user's request.
        {files_context}
        Return a JSON object with the following structure:
        {{
            "architecture": {{
                "component_name": ["file1", "file2"]
            }},
            "tasks": [
                {{
                    "id": 1,
                    "phase": "scaffold|coding|verification",
                    "description": "Task description",
                    "agent": "task|coding|execution",
                    "details": {{
                        "action": "create_dirs", 
                        "paths": ["dir1"],
                        "file_path": "path/to/file",
                        "prompt": "Instructions for coding agent",
                        "command": "Shell command for execution agent"
                    }}
                }}
            ]
        }}
        Ensure the plan is detailed and covers scaffolding, coding, and verification.
        IMPORTANT: Return ONLY the JSON object. Do not include any markdown formatting or explanation.
        """

    @staticmethod
    def get_coding_system_prompt() -> str:
        """Get the system prompt for the Coding Agent."""
        return """You are an expert coding assistant. Generate clean, production-ready code for the given task.
IMPORTANT RULES:
- Return ONLY the code itself
- Do NOT include any markdown formatting (no ```python or ``` blocks)
- Do NOT include explanations or comments outside the code
- Write complete, working code that can be directly executed
- USE EXISTING FILE PATHS to determine correct imports (e.g. if 'app/auth/routers.py' exists, import from 'app.auth.routers').
"""

    @staticmethod
    def get_error_fixing_system_prompt() -> str:
        """Get the system prompt for the Error Agent."""
        return "You are an error fixing agent. Fix the errors in the provided code. Return ONLY the fixed code."
