"""Project management tools for Claude"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from claude_agent_sdk import tool


# Project storage file
PROJECTS_FILE = Path("data/projects.json")


def load_projects() -> List[Dict]:
    """Load projects from file"""
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        return []

    try:
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_projects(projects: List[Dict]) -> None:
    """Save projects to file"""
    PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2, default=str)


@tool(
    name="create_project",
    description="Create a new project to work on",
    input_schema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Project name",
            },
            "description": {
                "type": "string",
                "description": "What this project is about",
            },
            "tasks": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Initial list of tasks (optional)",
            },
        },
        "required": ["name", "description"],
    },
)
async def create_project(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new project"""
    projects = load_projects()

    project_id = len(projects)
    new_project = {
        "id": project_id,
        "name": args["name"],
        "description": args["description"],
        "tasks": args.get("tasks", []),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    projects.append(new_project)
    save_projects(projects)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Project created successfully!\n"
                f"ID: {project_id}\n"
                f"Name: {args['name']}\n"
                f"Description: {args['description']}\n"
                f"Tasks: {len(args.get('tasks', []))}",
            }
        ]
    }


@tool(
    name="update_project",
    description="Update an existing project's status, tasks, or other fields",
    input_schema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "integer",
                "description": "ID of the project to update",
            },
            "status": {
                "type": "string",
                "enum": ["active", "paused", "completed", "cancelled"],
                "description": "New status (optional)",
            },
            "tasks": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Updated task list (optional)",
            },
            "notes": {
                "type": "string",
                "description": "Additional notes to append (optional)",
            },
        },
        "required": ["project_id"],
    },
)
async def update_project(args: Dict[str, Any]) -> Dict[str, Any]:
    """Update a project"""
    projects = load_projects()
    project_id = args["project_id"]

    if project_id >= len(projects):
        return {
            "content": [
                {"type": "text", "text": f"Error: Project {project_id} not found"}
            ]
        }

    project = projects[project_id]

    # Update fields
    if "status" in args:
        project["status"] = args["status"]
    if "tasks" in args:
        project["tasks"] = args["tasks"]
    if "notes" in args:
        if "notes" not in project:
            project["notes"] = []
        project["notes"].append({"timestamp": datetime.now().isoformat(), "text": args["notes"]})

    project["updated_at"] = datetime.now().isoformat()

    save_projects(projects)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Project {project_id} updated successfully!\n"
                f"Name: {project['name']}\n"
                f"Status: {project['status']}\n"
                f"Tasks: {len(project['tasks'])}",
            }
        ]
    }


@tool(
    name="list_projects",
    description="List all projects and their current status",
    input_schema={
        "type": "object",
        "properties": {
            "status_filter": {
                "type": "string",
                "enum": ["all", "active", "paused", "completed", "cancelled"],
                "description": "Filter by status (default: all)",
            },
        },
    },
)
async def list_projects(args: Dict[str, Any]) -> Dict[str, Any]:
    """List all projects"""
    projects = load_projects()
    status_filter = args.get("status_filter", "all")

    if status_filter != "all":
        projects = [p for p in projects if p["status"] == status_filter]

    if not projects:
        return {"content": [{"type": "text", "text": "No projects found."}]}

    output_lines = [f"Found {len(projects)} project(s):\n"]

    for project in projects:
        output_lines.append(f"\n--- Project {project['id']}: {project['name']} ---")
        output_lines.append(f"Status: {project['status']}")
        output_lines.append(f"Description: {project['description']}")
        output_lines.append(f"Tasks: {len(project['tasks'])}")
        output_lines.append(f"Created: {project['created_at']}")
        output_lines.append(f"Updated: {project['updated_at']}")

    return {"content": [{"type": "text", "text": "\n".join(output_lines)}]}
