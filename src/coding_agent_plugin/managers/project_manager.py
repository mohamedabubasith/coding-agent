"""Project manager for creating and managing projects."""

from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

from coding_agent_plugin.models import Project, UserSettings, get_db_session, init_db
from coding_agent_plugin.models.database import AGENTIC_HOME


class ProjectManager:
    """Manages project creation, listing, and switching."""
    
    def __init__(self):
        """Initialize project manager."""
        # Ensure database is initialized
        init_db()
        self.projects_dir = AGENTIC_HOME / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """
        Create a new project.
        
        Args:
            name: Project name (must be unique)
            description: Optional project description
            
        Returns:
            Created Project object
            
        Raises:
            ValueError: If project with name already exists
        """
        # Sanitize project name for filesystem
        safe_name = name.lower().replace(" ", "-").replace("_", "-")
        storage_path = str(self.projects_dir / safe_name)
        
        with get_db_session() as session:
            # Check if project already exists
            existing = session.query(Project).filter_by(name=name).first()
            if existing:
                raise ValueError(f"Project '{name}' already exists")
            
            # Create project directory
            Path(storage_path).mkdir(parents=True, exist_ok=True)
            
            # Create .agentic metadata directory
            metadata_dir = Path(storage_path) / ".agentic"
            metadata_dir.mkdir(exist_ok=True)
            
            # Create project in database
            project = Project(
                name=name,
                description=description,
                storage_path=storage_path,
                project_metadata={}
            )
            session.add(project)
            session.flush()  # Get the generated ID
            
            # Get project data before session closes
            project_dict = project.to_dict()
            
        # Return project dict (session is closed)
        return project_dict
    
    def list_projects(self) -> List[Dict]:
        """
        List all projects.
        
        Returns:
            List of project dictionaries
        """
        with get_db_session() as session:
            projects = session.query(Project).order_by(Project.created_at.desc()).all()
            return [p.to_dict() for p in projects]
    
    def get_project(self, name_or_id: str) -> Optional[Project]:
        """
        Get project by name or ID.
        
        Args:
            name_or_id: Project name or ID
            
        Returns:
            Project object or None if not found
        """
        with get_db_session() as session:
            # Try by name first
            project = session.query(Project).filter_by(name=name_or_id).first()
            if project:
                # Detach from session
                session.expunge(project)
                return project
            
            # Try by ID
            project = session.query(Project).filter_by(id=name_or_id).first()
            if project:
                session.expunge(project)
            return project
    
    def delete_project(self, name_or_id: str) -> bool:
        """
        Delete a project and its files.
        
        Args:
            name_or_id: Project name or ID
            
        Returns:
            True if deleted, False if not found
        """
        with get_db_session() as session:
            # Find project
            project = session.query(Project).filter(
                (Project.name == name_or_id) | (Project.id == name_or_id)
            ).first()
            
            if not project:
                return False
            
            # Delete project directory
            import shutil
            storage_path = Path(project.storage_path)
            if storage_path.exists():
                shutil.rmtree(storage_path)
            
            # Delete from database (cascade will delete files and versions)
            session.delete(project)
            
            return True
    
    def get_current_project(self) -> Optional[str]:
        """
        Get current active project name.
        
        Returns:
            Current project name or None
        """
        with get_db_session() as session:
            setting = session.query(UserSettings).filter_by(key="current_project").first()
            return setting.value if setting else None
    
    def set_current_project(self, name_or_id: str) -> bool:
        """
        Set current active project.
        
        Args:
            name_or_id: Project name or ID
            
        Returns:
            True if set successfully, False if project not found
        """
        # Verify project exists
        project = self.get_project(name_or_id)
        if not project:
            return False
        
        with get_db_session() as session:
            # Update or create current_project setting
            setting = session.query(UserSettings).filter_by(key="current_project").first()
            if setting:
                setting.value = project.name
            else:
                setting = UserSettings(key="current_project", value=project.name)
                session.add(setting)
            
            return True
    
    def get_project_stats(self, name_or_id: str) -> Optional[Dict]:
        """
        Get project statistics.
        
        Args:
            name_or_id: Project name or ID
            
        Returns:
            Dictionary with project stats or None if not found
        """
        project = self.get_project(name_or_id)
        if not project:
            return None
        
        storage_path = Path(project.storage_path)
        
        # Count files and calculate total size
        file_count = 0
        total_size = 0
        
        if storage_path.exists():
            for file in storage_path.rglob("*"):
                if file.is_file() and not str(file).startswith(str(storage_path / ".agentic")):
                    file_count += 1
                    total_size += file.stat().st_size
        
        return {
            **project.to_dict(),
            "file_count": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
