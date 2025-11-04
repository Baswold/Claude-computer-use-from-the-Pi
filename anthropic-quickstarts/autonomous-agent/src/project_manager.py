"""Project manager for tracking agent's projects"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ProjectManager:
    """Manages projects that the agent is working on"""

    def __init__(self, data_file: str = "data/projects.json"):
        self.data_file = Path(data_file)
        self.projects: List[Dict] = []
        self.load()

    def load(self):
        """Load projects from file"""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.projects = []
            return

        try:
            with open(self.data_file, "r") as f:
                self.projects = json.load(f)
            logger.info(f"Loaded {len(self.projects)} projects")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading projects: {e}")
            self.projects = []

    def save(self):
        """Save projects to file"""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump(self.projects, f, indent=2, default=str)
            logger.debug(f"Saved {len(self.projects)} projects")
        except IOError as e:
            logger.error(f"Error saving projects: {e}")

    def create_project(
        self, name: str, description: str, tasks: Optional[List[str]] = None
    ) -> int:
        """
        Create a new project

        Returns:
            project_id: The ID of the newly created project
        """
        project_id = len(self.projects)

        project = {
            "id": project_id,
            "name": name,
            "description": description,
            "tasks": tasks or [],
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notes": [],
        }

        self.projects.append(project)
        self.save()

        logger.info(f"Created project {project_id}: {name}")
        return project_id

    def update_project(
        self,
        project_id: int,
        status: Optional[str] = None,
        tasks: Optional[List[str]] = None,
        note: Optional[str] = None,
    ) -> bool:
        """
        Update a project

        Returns:
            True if successful, False if project not found
        """
        if project_id >= len(self.projects):
            logger.error(f"Project {project_id} not found")
            return False

        project = self.projects[project_id]

        if status:
            project["status"] = status
        if tasks is not None:
            project["tasks"] = tasks
        if note:
            project["notes"].append({"timestamp": datetime.now().isoformat(), "text": note})

        project["updated_at"] = datetime.now().isoformat()
        self.save()

        logger.info(f"Updated project {project_id}")
        return True

    def get_project(self, project_id: int) -> Optional[Dict]:
        """Get a project by ID"""
        if project_id < len(self.projects):
            return self.projects[project_id]
        return None

    def list_projects(self, status_filter: Optional[str] = None) -> List[Dict]:
        """
        List projects, optionally filtered by status

        Args:
            status_filter: Filter by status (active, paused, completed, cancelled)

        Returns:
            List of projects
        """
        if status_filter:
            return [p for p in self.projects if p["status"] == status_filter]
        return self.projects

    def get_active_projects(self) -> List[Dict]:
        """Get all active projects"""
        return self.list_projects(status_filter="active")

    def get_project_count(self, status: Optional[str] = None) -> int:
        """Get count of projects, optionally by status"""
        if status:
            return len([p for p in self.projects if p["status"] == status])
        return len(self.projects)
