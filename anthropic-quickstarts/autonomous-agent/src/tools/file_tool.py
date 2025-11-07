"""File search and navigation tools"""

import logging
from pathlib import Path
from typing import Any, Dict
from claude_agent_sdk import tool

logger = logging.getLogger(__name__)


@tool(
    name="find_files",
    description="Search for files by name pattern. Much faster than using Glob for simple searches.",
    input_schema={
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "File name pattern to search for (e.g., '*.py', 'config', 'README')",
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in (default: current project)",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results (default: 50)",
                "default": 50,
            },
        },
        "required": ["pattern"],
    },
)
async def find_files(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search for files quickly"""

    try:
        project_root = Path(__file__).parent.parent.parent

        search_dir = args.get("directory")
        if search_dir:
            search_path = Path(search_dir)
            if not search_path.is_absolute():
                search_path = project_root / search_path
        else:
            search_path = project_root

        pattern = args["pattern"]
        max_results = args.get("max_results", 50)

        # Search for files
        matches = []
        try:
            for file_path in search_path.rglob(pattern):
                if file_path.is_file():
                    try:
                        rel_path = file_path.relative_to(project_root)
                    except ValueError:
                        rel_path = file_path

                    matches.append({
                        "path": str(rel_path),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                    })

                    if len(matches) >= max_results:
                        break
        except Exception as e:
            logger.warning(f"Error during file search: {e}")

        if not matches:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No files found matching pattern: {pattern}",
                    }
                ]
            }

        # Sort by modification time
        matches.sort(key=lambda x: x["modified"], reverse=True)

        # Format output
        result = f"🔍 Found {len(matches)} file(s) matching '{pattern}'\n\n"

        for i, match in enumerate(matches[:20], 1):  # Show first 20
            size_kb = match["size"] / 1024
            result += f"{i}. {match['path']}\n"
            result += f"   Size: {size_kb:.1f} KB\n\n"

        if len(matches) > 20:
            result += f"\n... and {len(matches) - 20} more files"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result,
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error finding files: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error finding files: {str(e)}",
                }
            ]
        }


@tool(
    name="quick_note",
    description="Quickly save a note or snippet to a file. Great for saving interesting code, URLs, or ideas.",
    input_schema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Content to save",
            },
            "name": {
                "type": "string",
                "description": "Name for this note (optional, auto-generated if not provided)",
            },
            "category": {
                "type": "string",
                "description": "Category/folder for the note (e.g., 'code', 'ideas', 'urls')",
                "default": "general",
            },
        },
        "required": ["content"],
    },
)
async def quick_note(args: Dict[str, Any]) -> Dict[str, Any]:
    """Quickly save a note"""

    try:
        project_root = Path(__file__).parent.parent.parent
        notes_dir = project_root / "data" / "notes"

        category = args.get("category", "general")
        category_dir = notes_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        content = args["content"]

        # Generate name
        if "name" in args and args["name"]:
            name = args["name"]
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"note_{timestamp}"

        # Ensure .md extension
        if not name.endswith(".md"):
            name += ".md"

        note_file = category_dir / name

        # Add header
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_content = f"# {name.replace('.md', '').replace('_', ' ').title()}\n\n"
        full_content += f"*Created: {timestamp_str}*\n\n"
        full_content += f"{content}\n"

        note_file.write_text(full_content)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"📝 Note saved successfully!\n\n"
                    f"Name: {name}\n"
                    f"Category: {category}\n"
                    f"Location: data/notes/{category}/{name}\n"
                    f"Size: {len(content)} characters",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error saving note: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error saving note: {str(e)}",
                }
            ]
        }
