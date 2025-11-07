"""Enhanced screenshot tool with organization and context"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from claude_agent_sdk import tool

logger = logging.getLogger(__name__)

try:
    import mss
    import mss.tools
    from PIL import Image
    MSS_AVAILABLE = True
    PIL_AVAILABLE = True
except ImportError as e:
    MSS_AVAILABLE = False
    PIL_AVAILABLE = False
    logger.warning(f"Screenshot dependencies not available: {e}")


@tool(
    name="take_screenshot",
    description="Take a screenshot of the current screen. Useful for capturing UI state, errors, or interesting findings.",
    input_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Optional custom filename (without extension)",
            },
            "description": {
                "type": "string",
                "description": "Optional description of what you're capturing (helps organize screenshots)",
            },
            "create_thumbnail": {
                "type": "boolean",
                "description": "Create a thumbnail version (default: True)",
                "default": True,
            },
        },
    },
)
async def take_screenshot(args: Dict[str, Any]) -> Dict[str, Any]:
    """Take a screenshot with organization and context"""

    if not MSS_AVAILABLE:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "❌ Screenshot tool not available.\n\nInstall dependencies:\npip install mss pillow",
                }
            ]
        }

    try:
        # Get project root
        project_root = Path(__file__).parent.parent.parent

        # Organize by date
        today = datetime.now().strftime("%Y-%m-%d")
        screenshot_dir = project_root / "data" / "screenshots" / today
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%H%M%S")
        if "filename" in args and args["filename"]:
            base_name = args["filename"]
        else:
            base_name = f"screenshot_{timestamp}"

        filename = f"{base_name}.png"
        filepath = screenshot_dir / filename

        # Take screenshot
        with mss.mss() as sct:
            # Capture the first monitor
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            screenshot = sct.grab(monitor)

            # Save to file
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(filepath))

        # Get file info
        file_size = filepath.stat().st_size
        file_size_kb = file_size / 1024

        # Create thumbnail if requested
        thumbnail_path = None
        if args.get("create_thumbnail", True) and PIL_AVAILABLE:
            try:
                with Image.open(filepath) as img:
                    img.thumbnail((320, 180))
                    thumbnail_path = screenshot_dir / f"{base_name}_thumb.png"
                    img.save(thumbnail_path)
            except Exception as e:
                logger.warning(f"Could not create thumbnail: {e}")

        # Save metadata
        description = args.get("description", "")
        if description:
            metadata_file = screenshot_dir / f"{base_name}_meta.txt"
            metadata_file.write_text(
                f"Timestamp: {datetime.now().isoformat()}\n"
                f"Description: {description}\n"
                f"File: {filename}\n"
                f"Size: {file_size_kb:.1f} KB\n"
            )

        result = f"📸 Screenshot captured successfully!\n\n"
        result += f"📁 Location: {filepath.relative_to(project_root)}\n"
        result += f"📊 Size: {file_size_kb:.1f} KB\n"
        result += f"📅 Date: {today}\n"
        result += f"🕐 Time: {timestamp}\n"

        if description:
            result += f"📝 Description: {description}\n"

        if thumbnail_path:
            result += f"🖼️  Thumbnail: {thumbnail_path.name}\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result,
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error taking screenshot: {str(e)}",
                }
            ]
        }


@tool(
    name="list_screenshots",
    description="List recent screenshots with their descriptions",
    input_schema={
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "Number of days to look back (default: 7)",
                "default": 7,
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of screenshots to return (default: 20)",
                "default": 20,
            },
        },
    },
)
async def list_screenshots(args: Dict[str, Any]) -> Dict[str, Any]:
    """List recent screenshots"""

    try:
        project_root = Path(__file__).parent.parent.parent
        screenshots_dir = project_root / "data" / "screenshots"

        if not screenshots_dir.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No screenshots directory found. Take a screenshot first!",
                    }
                ]
            }

        days = args.get("days", 7)
        limit = args.get("limit", 20)

        # Collect all screenshots
        screenshots = []
        for date_dir in sorted(screenshots_dir.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue

            for file in sorted(date_dir.glob("*.png"), reverse=True):
                if "_thumb" in file.name:
                    continue  # Skip thumbnails

                # Check for metadata
                meta_file = file.with_suffix("").with_name(f"{file.stem}_meta.txt")
                description = ""
                if meta_file.exists():
                    try:
                        meta_content = meta_file.read_text()
                        for line in meta_content.split('\n'):
                            if line.startswith("Description:"):
                                description = line.replace("Description:", "").strip()
                    except:
                        pass

                screenshots.append({
                    "file": file,
                    "date": date_dir.name,
                    "name": file.name,
                    "size": file.stat().st_size / 1024,
                    "description": description,
                })

                if len(screenshots) >= limit:
                    break

            if len(screenshots) >= limit:
                break

        if not screenshots:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No screenshots found in the last {} days.".format(days),
                    }
                ]
            }

        # Format output
        result = f"📸 Recent Screenshots ({len(screenshots)} found)\n\n"

        for i, shot in enumerate(screenshots, 1):
            result += f"{i}. {shot['name']}\n"
            result += f"   📅 {shot['date']}\n"
            result += f"   📊 {shot['size']:.1f} KB\n"
            if shot['description']:
                result += f"   📝 {shot['description']}\n"
            result += "\n"

        return {
            "content": [
                {
                    "type": "text",
                    "text": result,
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error listing screenshots: {e}", exc_info=True)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error listing screenshots: {str(e)}",
                }
            ]
        }
