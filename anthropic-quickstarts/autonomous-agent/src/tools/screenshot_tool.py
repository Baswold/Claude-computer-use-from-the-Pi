"""Screenshot tool for capturing the screen"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from claude_agent_sdk import tool

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False


SCREENSHOT_DIR = Path("data/screenshots")


@tool(
    name="take_screenshot",
    description="Take a screenshot of the current screen",
    input_schema={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Optional custom filename (without extension)",
            },
        },
    },
)
async def take_screenshot(args: Dict[str, Any]) -> Dict[str, Any]:
    """Take a screenshot"""

    if not MSS_AVAILABLE:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Screenshot tool not available. Install mss: pip install mss",
                }
            ]
        }

    # Create screenshot directory
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate filename
    if "filename" in args and args["filename"]:
        filename = f"{args['filename']}.png"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

    filepath = SCREENSHOT_DIR / filename

    # Take screenshot
    try:
        with mss.mss() as sct:
            # Capture the first monitor
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            # Save to file
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(filepath))

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Screenshot saved successfully!\n"
                    f"Location: {filepath}\n"
                    f"Size: {filepath.stat().st_size} bytes",
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error taking screenshot: {str(e)}",
                }
            ]
        }
