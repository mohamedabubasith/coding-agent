"""Git integration for automatic version control."""

import os
from pathlib import Path
from typing import Optional


class GitManager:
    """Manages git operations for generated projects."""
    
    def __init__(self, project_path: str):
        """
        Initialize GitManager.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.repo = None
    
    def init_repo(self) -> bool:
        """
        Initialize a git repository in the project directory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import git
            
            if (self.project_path / ".git").exists():
                self.repo = git.Repo(self.project_path)
                return True
            
            self.repo = git.Repo.init(self.project_path)
            
            # Create .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
.agent_context/
*.db
*.sqlite
.env
"""
            gitignore_path = self.project_path / ".gitignore"
            gitignore_path.write_text(gitignore_content)
            
            return True
            
        except Exception as e:
            print(f"Warning: Failed to initialize git: {e}")
            return False
    
    def commit(self, message: str, add_all: bool = True) -> bool:
        """
        Create a git commit.
        
        Args:
            message: Commit message
            add_all: Whether to add all files before committing
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.repo:
                return False
            
            if add_all:
                self.repo.git.add(A=True)
            
            self.repo.index.commit(message)
            return True
            
        except Exception as e:
            print(f"Warning: Failed to commit: {e}")
            return False
    
    def commit_file(self, file_path: str, message: str) -> bool:
        """
        Commit a specific file.
        
        Args:
            file_path: Path to the file (relative to project root)
            message: Commit message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.repo:
                return False
            
            self.repo.index.add([file_path])
            self.repo.index.commit(message)
            return True
            
        except Exception as e:
            print(f"Warning: Failed to commit file: {e}")
            return False
