"""Custom tools for the autonomous agent"""

# Timer tools
from .timer_tool import set_timer

# Project management
from .project_tool import create_project, update_project, list_projects

# Memory management
from .memory_tool import update_memory, read_memory

# System monitoring
from .system_tool import check_system_health, list_processes

# Screenshots
from .screenshot_tool import take_screenshot, list_screenshots

# Journal and activity logging
from .journal_tool import log_thought, read_thoughts, log_activity

# File utilities
from .file_tool import find_files, quick_note

__all__ = [
    # Timer (1)
    "set_timer",
    # Projects (3)
    "create_project",
    "update_project",
    "list_projects",
    # Memory (2)
    "update_memory",
    "read_memory",
    # System (2)
    "check_system_health",
    "list_processes",
    # Screenshots (2)
    "take_screenshot",
    "list_screenshots",
    # Journal (3)
    "log_thought",
    "read_thoughts",
    "log_activity",
    # Files (2)
    "find_files",
    "quick_note",
]

# Total: 15 tools
