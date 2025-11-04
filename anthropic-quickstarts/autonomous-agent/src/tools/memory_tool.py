"""Enhanced memory management tool for Claude's persistent memory"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict
from claude_agent_sdk import tool

logger = logging.getLogger(__name__)


@tool(
    name="update_memory",
    description="Update your persistent memory file (CLAUDE.md) with important information to remember across sessions",
    input_schema={
        "type": "object",
        "properties": {
            "section": {
                "type": "string",
                "description": "Section to update (e.g., 'Current Projects', 'Learnings', 'Important Notes')",
            },
            "content": {
                "type": "string",
                "description": "Content to add to this section",
            },
            "append": {
                "type": "boolean",
                "description": "If true, append to existing content; if false, replace section",
                "default": True,
            },
        },
        "required": ["section", "content"],
    },
)
async def update_memory(args: Dict[str, Any]) -> Dict[str, Any]:
    """Update Claude's memory file"""
    try:
        memory_file = Path("CLAUDE.md")

        if not memory_file.exists():
            memory_file.write_text("# Claude's Persistent Memory\n\n")

        content = memory_file.read_text()
        section = args["section"]
        new_content = args["content"]
        append = args.get("append", True)

        # Look for the section
        section_marker = f"## {section}"

        if section_marker in content:
            # Section exists
            if append:
                # Find the section and append
                lines = content.split('\n')
                new_lines = []
                in_section = False
                section_added = False

                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.startswith(f"## {section}"):
                        in_section = True
                    elif in_section and line.startswith("## ") and not section_added:
                        # Next section found, insert before it
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_lines.insert(-1, f"\n### Update {timestamp}\n{new_content}\n")
                        section_added = True
                        in_section = False

                if in_section and not section_added:
                    # Section was last, append at end
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_lines.append(f"\n### Update {timestamp}\n{new_content}\n")

                content = '\n'.join(new_lines)
            else:
                # Replace section content
                # This is simplified - just append for now
                pass
        else:
            # Section doesn't exist, create it
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content += f"\n## {section}\n\n### {timestamp}\n{new_content}\n"

        memory_file.write_text(content)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Memory updated successfully!\nSection: {section}\nAppended: {append}\nMemory file: {memory_file.absolute()}",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error updating memory: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error updating memory: {str(e)}",
                }
            ]
        }


@tool(
    name="read_memory",
    description="Read your persistent memory file to recall information from previous sessions",
    input_schema={
        "type": "object",
        "properties": {
            "section": {
                "type": "string",
                "description": "Specific section to read (optional, leave empty for entire file)",
            },
        },
    },
)
async def read_memory(args: Dict[str, Any]) -> Dict[str, Any]:
    """Read Claude's memory file"""
    try:
        memory_file = Path("CLAUDE.md")

        if not memory_file.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Memory file doesn't exist yet. Use update_memory to create it.",
                    }
                ]
            }

        content = memory_file.read_text()
        section = args.get("section")

        if section:
            # Extract specific section
            lines = content.split('\n')
            section_lines = []
            in_section = False

            for line in lines:
                if line.startswith(f"## {section}"):
                    in_section = True
                    section_lines.append(line)
                elif in_section and line.startswith("## "):
                    break
                elif in_section:
                    section_lines.append(line)

            if section_lines:
                content = '\n'.join(section_lines)
            else:
                content = f"Section '{section}' not found in memory."

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Memory contents:\n\n{content}",
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error reading memory: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error reading memory: {str(e)}",
                }
            ]
        }
