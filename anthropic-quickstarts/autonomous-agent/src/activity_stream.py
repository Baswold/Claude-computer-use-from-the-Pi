"""Beautiful real-time activity stream display"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ActivityStream:
    """Real-time activity stream for the autonomous agent"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.stream_file = project_root / "data" / "activity_stream.log"
        self.stream_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize stream
        if not self.stream_file.exists():
            self._write_header()

    def _write_header(self):
        """Write stream header"""
        header = """
╔══════════════════════════════════════════════════════════════════════════╗
║                   AUTONOMOUS CLAUDE AGENT v3.0                           ║
║                      Real-Time Activity Stream                            ║
╚══════════════════════════════════════════════════════════════════════════╝

"""
        self.stream_file.write_text(header)

    def _append(self, message: str):
        """Append to stream"""
        try:
            with open(self.stream_file, "a") as f:
                f.write(message + "\n")
                f.flush()  # Ensure immediate write
        except Exception as e:
            logger.error(f"Error writing to activity stream: {e}")

    def log_event(self, event_type: str, message: str, details: Optional[str] = None):
        """Log an event to the activity stream"""

        timestamp = datetime.now().strftime("%H:%M:%S")

        # Event type emoji mapping
        emoji_map = {
            "checkin": "🔔",
            "thought": "💭",
            "tool": "🔧",
            "error": "❌",
            "success": "✅",
            "start": "🚀",
            "stop": "🛑",
            "memory": "🧠",
            "project": "📊",
            "screenshot": "📸",
            "system": "💻",
            "timer": "⏰",
            "file": "📁",
            "web": "🌐",
            "code": "💻",
            "note": "📝",
        }

        emoji = emoji_map.get(event_type, "•")

        # Format message
        formatted = f"[{timestamp}] {emoji} {message}"

        if details:
            formatted += f"\n         └─ {details}"

        self._append(formatted)

        # Also log to logger
        logger.info(f"{event_type.upper()}: {message}")

    def log_tool_use(self, tool_name: str, success: bool = True, details: Optional[str] = None):
        """Log a tool use"""

        # Clean tool name
        clean_name = tool_name.replace("mcp__agent_tools__", "")

        status = "✅" if success else "❌"
        message = f"{status} Using tool: {clean_name}"

        self.log_event("tool", message, details)

    def log_checkin_start(self):
        """Log check-in start"""
        separator = "\n" + "─" * 80 + "\n"
        self._append(separator)
        self.log_event("checkin", "Check-in starting...")

    def log_checkin_end(self, tool_count: int, duration: float):
        """Log check-in end"""
        message = f"Check-in completed: {tool_count} tools used, {duration:.1f}s"
        self.log_event("success", message)

    def log_thought(self, thought: str):
        """Log a thought"""
        # Truncate long thoughts
        if len(thought) > 100:
            thought = thought[:97] + "..."
        self.log_event("thought", thought)

    def log_error(self, error: str, retry_attempt: Optional[int] = None):
        """Log an error"""
        if retry_attempt:
            message = f"Error (attempt {retry_attempt}): {error}"
        else:
            message = f"Error: {error}"
        self.log_event("error", message)

    def log_system_status(self, cpu: float, memory: float, disk: float):
        """Log system status"""
        message = f"System: CPU {cpu:.0f}%, Memory {memory:.0f}%, Disk {disk:.0f}%"
        self.log_event("system", message)

    def clear(self):
        """Clear the activity stream"""
        self._write_header()

    def get_recent(self, lines: int = 50) -> str:
        """Get recent activity"""
        try:
            if not self.stream_file.exists():
                return "No activity yet."

            with open(self.stream_file, "r") as f:
                all_lines = f.readlines()
                recent = all_lines[-lines:]
                return "".join(recent)
        except Exception as e:
            logger.error(f"Error reading activity stream: {e}")
            return f"Error reading activity stream: {e}"


def create_visual_separator(title: str = "", width: int = 80) -> str:
    """Create a visual separator"""
    if title:
        padding = (width - len(title) - 2) // 2
        return "═" * padding + f" {title} " + "═" * padding
    return "═" * width


def format_tool_list(tools: list) -> str:
    """Format a list of tools nicely"""
    if not tools:
        return "No tools used"

    # Group by category
    categories = {
        "memory": ["update_memory", "read_memory"],
        "project": ["create_project", "update_project", "list_projects"],
        "system": ["check_system_health", "list_processes"],
        "screenshot": ["take_screenshot", "list_screenshots"],
        "journal": ["log_thought", "read_thoughts", "log_activity"],
        "file": ["find_files", "quick_note"],
        "standard": ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch"],
    }

    grouped = {}
    for tool in tools:
        clean_name = tool.replace("mcp__agent_tools__", "")
        for cat, cat_tools in categories.items():
            if clean_name in cat_tools:
                if cat not in grouped:
                    grouped[cat] = []
                grouped[cat].append(clean_name)
                break

    # Format output
    result = []
    category_emoji = {
        "memory": "🧠",
        "project": "📊",
        "system": "💻",
        "screenshot": "📸",
        "journal": "📝",
        "file": "📁",
        "standard": "🔧",
    }

    for cat, cat_tools in grouped.items():
        emoji = category_emoji.get(cat, "•")
        result.append(f"{emoji} {cat.title()}: {', '.join(cat_tools)}")

    return "\n".join(result)
