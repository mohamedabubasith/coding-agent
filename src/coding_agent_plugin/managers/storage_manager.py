"""Storage manager for project files."""

from pathlib import Path
from typing import Optional, List, Dict
import hashlib
import shutil

from coding_agent_plugin.models import ProjectFile, get_db_session
from coding_agent_plugin.managers.project_manager import ProjectManager


class StorageManager:
    """Manages file storage for projects."""
    
    def __init__(self):
        """Initialize storage manager."""
        self.project_manager = ProjectManager()
    
    def save_file(self, project_name_or_id: str, file_path: str, content: str) -> bool:
        """
        Save file to project storage.
        
        Args:
            project_name_or_id: Project name or ID
            file_path: Relative file path within project
            content: File content
            
        Returns:
            True if saved successfully
            
        Raises:
            ValueError: If project not found
        """
        project = self.project_manager.get_project(project_name_or_id)
        if not project:
            raise ValueError(f"Project '{project_name_or_id}' not found")
        
        # Full file path
        full_path = Path(project.storage_path) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        full_path.write_text(content, encoding="utf-8")
        
        # Calculate hash and size
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        size_bytes = len(content.encode())
        
        # Update database
        with get_db_session() as session:
           # Check if file entry exists
            file_entry = session.query(ProjectFile).filter_by(
                project_id=project.id,
                file_path=file_path
            ).first()
            
            if file_entry:
                # Update existing
                file_entry.content_hash = content_hash
                file_entry.size_bytes = size_bytes
            else:
                # Create new
                file_entry = ProjectFile(
                    project_id=project.id,
                    file_path=file_path,
                    content_hash=content_hash,
                    size_bytes=size_bytes
                )
                session.add(file_entry)
        
        return True
    
    def get_file(self, project_name_or_id: str, file_path: str) -> Optional[str]:
        """
        Get file content from project storage.
        
        Args:
            project_name_or_id: Project name or ID
            file_path: Relative file path within project
            
        Returns:
            File content or None if not found
        """
        project = self.project_manager.get_project(project_name_or_id)
        if not project:
            return None
        
        full_path = Path(project.storage_path) / file_path
        if not full_path.exists():
            return None
        
        return full_path.read_text(encoding="utf-8")
    
    def list_files(self, project_name_or_id: str) -> List[str]:
        """
        List all files in project.
        
        Args:
            project_name_or_id: Project name or ID
            
        Returns:
            List of relative file paths
        """
        project = self.project_manager.get_project(project_name_or_id)
        if not project:
            return []
        
        storage_path = Path(project.storage_path)
        files = []
        
        for file in storage_path.rglob("*"):
            if file.is_file():
                # Skip .agentic directory
                if ".agentic" in file.parts:
                    continue
                relative_path = file.relative_to(storage_path)
                files.append(str(relative_path))
        
        return sorted(files)
    
    def delete_file(self, project_name_or_id: str, file_path: str) -> bool:
        """
        Delete file from project storage.
        
        Args:
            project_name_or_id: Project name or ID
            file_path: Relative file path within project
            
        Returns:
            True if deleted, False if not found
        """
        project = self.project_manager.get_project(project_name_or_id)
        if not project:
            return False
        
        full_path = Path(project.storage_path) / file_path
        if not full_path.exists():
            return False
        
        # Delete file
        full_path.unlink()
        
        # Delete from database
        with get_db_session() as session:
            file_entry = session.query(ProjectFile).filter_by(
                project_id=project.id,
                file_path=file_path
            ).first()
            
            if file_entry:
                session.delete(file_entry)
        
        return True
    
    def copy_to_project(self, source_path: str, project_name_or_id: str, dest_path: str) -> bool:
        """
        Copy file or directory to project storage.
        
        Args:
            source_path: Source file or directory path
            project_name_or_id: Project name or ID
            dest_path: Destination path within project
            
        Returns:
            True if copied successfully
        """
        project = self.project_manager.get_project(project_name_or_id)
        if not project:
            return False
        
        source = Path(source_path)
        dest = Path(project.storage_path) / dest_path
        
        if source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            
            # Track in database
            content = dest.read_text(encoding="utf-8")
            self.save_file(project.name, dest_path, content)
        elif source.is_dir():
            shutil.copytree(source, dest, dirs_exist_ok=True)
            
            # Track all files in database
            for file in dest.rglob("*"):
                if file.is_file():
                    relative_path = file.relative_to(Path(project.storage_path))
                    content = file.read_text(encoding="utf-8")
                    self.save_file(project.name, str(relative_path), content)
        
        return True
