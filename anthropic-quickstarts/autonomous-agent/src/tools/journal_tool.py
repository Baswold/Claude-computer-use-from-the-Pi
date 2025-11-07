"""Activity logging and thought journal for Claude"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from claude_agent_sdk import tool

logger = logging.getLogger(__name__)


@tool(
    name="log_thought",
    description="Log a thought, observation, or note for future reference. Use this as your personal journal.",
    input_schema={
        "type": "object",
        "properties": {
            "thought": {
                "type": "string",
                "description": "Your thought, observation, or note",
            },
            "category": {
                "type": "string",
                "enum": ["idea", "observation", "decision", "learning", "question", "todo", "note"],
                "description": "Category of the thought",
                "default": "note",
            },
        },
        "required": ["thought"],
    },
)
async def log_thought(args: Dict[str, Any]) -> Dict[str, Any]:
    """Log a thought or observation"""

    try:
        project_root = Path(__file__).parent.parent.parent
        thoughts_dir = project_root / "data" / "thoughts"
        thoughts_dir.mkdir(parents=True, exist_ok=True)

        # Organize by date
        today = datetime.now().strftime("%Y-%m-%d")
        thoughts_file = thoughts_dir / f"thoughts_{today}.md"

        thought = args["thought"]
        category = args.get("category", "note")
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Category emoji mapping
        emoji_map = {
            "idea": "💡",
            "observation": "👁️",
            "decision": "✅",
            "learning": "📚",
            "question": "❓",
            "todo": "📝",
            "note": "📌",
        }

        emoji = emoji_map.get(category, "📌")

        # Append to file
        entry = f"\n## {emoji} {category.title()} - {timestamp}\n\n{thought}\n"

        with open(thoughts_file, "a") as f:
            # Add header if new file
            if thoughts_file.stat().st_size == 0:
                f.write(f"# Thoughts for {today}\n")
            f.write(entry)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"{emoji} Thought logged successfully!\n\n"
                    f"Category: {category}\n"
                    f"Time: {timestamp}\n"
                    f"File: thoughts/{thoughts_file.name}",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error logging thought: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error logging thought: {str(e)}",
                }
            ]
        }


@tool(
    name="read_thoughts",
    description="Read your recent thoughts and observations",
    input_schema={
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "Number of days to look back (default: 7)",
                "default": 7,
            },
            "category": {
                "type": "string",
                "enum": ["all", "idea", "observation", "decision", "learning", "question", "todo", "note"],
                "description": "Filter by category (default: all)",
                "default": "all",
            },
        },
    },
)
async def read_thoughts(args: Dict[str, Any]) -> Dict[str, Any]:
    """Read recent thoughts"""

    try:
        project_root = Path(__file__).parent.parent.parent
        thoughts_dir = project_root / "data" / "thoughts"

        if not thoughts_dir.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No thoughts logged yet. Use log_thought to start your journal!",
                    }
                ]
            }

        days = args.get("days", 7)
        category_filter = args.get("category", "all")

        # Collect recent thought files
        thought_files = sorted(thoughts_dir.glob("thoughts_*.md"), reverse=True)[:days]

        if not thought_files:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No thoughts found in the last {days} days.",
                    }
                ]
            }

        # Read and combine
        all_thoughts = ""
        for file in thought_files:
            content = file.read_text()

            # Filter by category if specified
            if category_filter != "all":
                lines = content.split('\n')
                filtered_lines = []
                include_section = False

                for line in lines:
                    if line.startswith("##"):
                        include_section = category_filter.lower() in line.lower()
                    if include_section or line.startswith("#"):
                        filtered_lines.append(line)

                content = '\n'.join(filtered_lines)

            all_thoughts += content + "\n\n"

        if not all_thoughts.strip():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No thoughts found with category '{category_filter}' in the last {days} days.",
                    }
                ]
            }

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"📚 Your Recent Thoughts\n\n{all_thoughts}",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error reading thoughts: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error reading thoughts: {str(e)}",
                }
            ]
        }


@tool(
    name="log_activity",
    description="Log a significant activity or milestone (automatically tracked for retrospection)",
    input_schema={
        "type": "object",
        "properties": {
            "activity": {
                "type": "string",
                "description": "Description of the activity or milestone",
            },
            "status": {
                "type": "string",
                "enum": ["started", "in_progress", "completed", "blocked", "cancelled"],
                "description": "Status of the activity",
            },
            "details": {
                "type": "string",
                "description": "Additional details (optional)",
            },
        },
        "required": ["activity", "status"],
    },
)
async def log_activity(args: Dict[str, Any]) -> Dict[str, Any]:
    """Log an activity for tracking"""

    try:
        project_root = Path(__file__).parent.parent.parent
        activity_log = project_root / "data" / "activity_log.md"
        activity_log.parent.mkdir(parents=True, exist_ok=True)

        activity = args["activity"]
        status = args["status"]
        details = args.get("details", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Status emoji mapping
        status_emoji = {
            "started": "🚀",
            "in_progress": "⚙️",
            "completed": "✅",
            "blocked": "🚫",
            "cancelled": "❌",
        }

        emoji = status_emoji.get(status, "📍")

        # Create entry
        entry = f"\n### {emoji} {status.upper()} - {activity}\n"
        entry += f"**Time:** {timestamp}\n"
        if details:
            entry += f"**Details:** {details}\n"
        entry += "\n---\n"

        # Append to log
        with open(activity_log, "a") as f:
            # Add header if new file
            if not activity_log.exists() or activity_log.stat().st_size == 0:
                f.write(f"# Activity Log\n\nGenerated by Autonomous Claude Agent\n\n")
            f.write(entry)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"{emoji} Activity logged!\n\n"
                    f"Activity: {activity}\n"
                    f"Status: {status}\n"
                    f"Time: {timestamp}",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error logging activity: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error logging activity: {str(e)}",
                }
            ]
        }
