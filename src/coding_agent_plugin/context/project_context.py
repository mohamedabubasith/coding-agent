"""Project context system for understanding existing projects."""

import os
from pathlib import Path
from typing import Dict, List, Optional
import json


class ProjectContext:
    """Manages context and understanding of an existing project."""
    
    def __init__(self, project_path: str):
        """
        Initialize project context.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.files: Dict[str, str] = {}
        self.structure: Dict[str, List[str]] = {}
        self.agent_context_path = self.project_path / ".agent_context"
        
    def is_valid_project(self) -> bool:
        """Check if this is a valid coding-agent project."""
        return (self.agent_context_path.exists() and 
                (self.agent_context_path / "planning.md").exists())
    
    def load_project(self) -> bool:
        """
        Load and analyze the project structure.
        
        Returns:
            bool: True if successful
        """
        try:
            # Scan all files (excluding hidden and common dirs to ignore)
            ignore_dirs = {".git", ".agent_context", "__pycache__", "node_modules", ".venv", "venv"}
            ignore_exts = {".pyc", ".pyo", ".db", ".sqlite", ".log"}
            
            for root, dirs, files in os.walk(self.project_path):
                # Remove ignored directories from search
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                rel_root = Path(root).relative_to(self.project_path)
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip ignored extensions
                    if file_path.suffix in ignore_exts:
                        continue
                    
                    rel_path = file_path.relative_to(self.project_path)
                    
                    # Read text files only
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.files[str(rel_path)] = content
                    except (UnicodeDecodeError, PermissionError):
                        # Skip binary or unreadable files
                        continue
            
            # Build structure
            for file_path in self.files.keys():
                directory = str(Path(file_path).parent)
                if directory not in self.structure:
                    self.structure[directory] = []
                self.structure[directory].append(Path(file_path).name)
            
            return True
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get content of a specific file."""
        return self.files.get(file_path)
    
    def get_files_by_extension(self, extension: str) -> List[str]:
        """Get all files with a specific extension."""
        return [f for f in self.files.keys() if f.endswith(extension)]
    
    def get_main_files(self) -> List[str]:
        """Get likely main entry point files."""
        main_names = ["main.py", "app.py", "index.py", "__init__.py", "server.py"]
        return [f for f in self.files.keys() if Path(f).name in main_names]
    
    def save_conversation_history(self, request: str, changes: List[Dict]) -> bool:
        """
        Save a conversation turn to history.
        
        Args:
            request: User's improvement request
            changes: List of changes made
            
        Returns:
            bool: True if successful
        """
        try:
            history_file = self.agent_context_path / "conversation.json"
            
            # Load existing history
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = {"sessions": []}
            
            # Add new session
            import datetime
            history["sessions"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "request": request,
                "changes": changes
            })
            
            # Save
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Warning: Failed to save history: {e}")
            return False
    
    def get_project_summary(self) -> str:
        """Get a summary of the project for LLM context."""
        summary_parts = []
        
        summary_parts.append(f"Project Path: {self.project_path}")
        summary_parts.append(f"\nTotal Files: {len(self.files)}")
        
        # File breakdown by extension
        summary_parts.append("\nFile Types:")
        ext_count = {}
        for file in self.files.keys():
            ext = Path(file).suffix or "no extension"
            ext_count[ext] = ext_count.get(ext, 0) + 1
        
        for ext, count in sorted(ext_count.items(), key=lambda x: x[1], reverse=True):
            summary_parts.append(f"  {ext}: {count} files")
        
        # Main files
        main_files = self.get_main_files()
        if main_files:
            summary_parts.append(f"\nMain Files: {', '.join(main_files)}")
        
        # Directory structure
        summary_parts.append("\nDirectory Structure:")
        for directory, files in sorted(self.structure.items()):
            if directory == ".":
                summary_parts.append(f"  / ({len(files)} files)")
            else:
                summary_parts.append(f"  {directory}/ ({len(files)} files)")
        
        return "\n".join(summary_parts)
