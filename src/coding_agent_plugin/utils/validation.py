"""Input validation utilities."""

import re
from pathlib import Path
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_project_id(project_id: str) -> str:
    """
    Validate project ID format.
    
    Args:
        project_id: Project identifier to validate
        
    Returns:
        Cleaned project ID
        
    Raises:
        ValidationError: If project ID is invalid
    """
    if not project_id:
        raise ValidationError("Project ID cannot be empty")
    
    if len(project_id) > 100:
        raise ValidationError("Project ID too long (max 100 characters)")
    
    # Only allow alphanumeric, underscores, hyphens
    if not re.match(r'^[a-zA-Z0-9_-]+$', project_id):
        raise ValidationError(
            "Project ID can only contain letters, numbers, underscores, and hyphens"
        )
    
    return project_id


def validate_prompt(prompt: str) -> str:
    """
    Validate user prompt.
    
    Args:
        prompt: User's project description
        
    Returns:
        Cleaned prompt
        
    Raises:
        ValidationError: If prompt is invalid
    """
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt cannot be empty")
    
    if len(prompt) < 5:
        raise ValidationError("Prompt too short (minimum 5 characters)")
    
    if len(prompt) > 1000:
        raise ValidationError("Prompt too long (maximum 1000 characters)")
    
    return prompt.strip()


def validate_file_path(file_path: str, must_exist: bool = False) -> Path:
    """
    Validate file path.
    
    Args:
        file_path: Path to validate
        must_exist: Whether the file must exist
        
    Returns:
        Path object
        
    Raises:
        ValidationError: If path is invalid
    """
    try:
        path = Path(file_path)
    except Exception as e:
        raise ValidationError(f"Invalid file path: {e}")
    
    if must_exist and not path.exists():
        raise ValidationError(f"File does not exist: {file_path}")
    
    # Security: prevent path traversal
    if ".." in str(path):
        raise ValidationError("Path traversal not allowed")
    
    return path


def validate_model_name(model_name: Optional[str]) -> Optional[str]:
    """
    Validate LLM model name.
    
    Args:
        model_name: Model name to validate
        
    Returns:
        Model name or None
        
    Raises:
        ValidationError: If model name is invalid
    """
    if not model_name:
        return None
    
    # Basic validation - could be extended
    if len(model_name) > 200:
        raise ValidationError("Model name too long")
    
    return model_name


def sanitize_project_id(prompt: str, max_length: int = 50) -> str:
    """
    Generate a safe project ID from a prompt.
    
    Args:
        prompt: User's prompt
        max_length: Maximum length of project ID
        
    Returns:
        Safe project ID
    """
    # Convert to lowercase, replace spaces with underscores
    project_id = prompt.lower()
    project_id = re.sub(r'[^a-z0-9]+', '_', project_id)
    project_id = project_id[:max_length].strip('_')
    
    # Ensure it's not empty
    if not project_id:
        project_id = "project"
    
    return project_id
