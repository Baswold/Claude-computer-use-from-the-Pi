"""Timer tool for scheduling future actions"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict
from claude_agent_sdk import tool


# Global timer storage (in production, use database)
scheduled_timers = []


@tool(
    name="set_timer",
    description="Schedule a timer to wake you up at a specific time with a prompt",
    input_schema={
        "type": "object",
        "properties": {
            "delay_minutes": {
                "type": "integer",
                "description": "Number of minutes from now to set the timer",
                "minimum": 1,
            },
            "prompt": {
                "type": "string",
                "description": "The prompt/reminder for when the timer goes off",
            },
        },
        "required": ["delay_minutes", "prompt"],
    },
)
async def set_timer(args: Dict[str, Any]) -> Dict[str, Any]:
    """Set a timer to prompt Claude at a future time"""
    delay = args["delay_minutes"]
    prompt = args["prompt"]

    # Calculate when timer should trigger
    trigger_time = datetime.now() + timedelta(minutes=delay)

    # Store timer (in production, persist to database)
    timer_id = len(scheduled_timers)
    scheduled_timers.append(
        {"id": timer_id, "trigger_time": trigger_time, "prompt": prompt, "active": True}
    )

    return {
        "content": [
            {
                "type": "text",
                "text": f"Timer set! ID: {timer_id}\n"
                f"Will trigger at: {trigger_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Prompt: {prompt}",
            }
        ]
    }


def get_due_timers() -> list:
    """Get all timers that are due to trigger"""
    now = datetime.now()
    due_timers = []

    for timer in scheduled_timers:
        if timer["active"] and timer["trigger_time"] <= now:
            timer["active"] = False  # Mark as triggered
            due_timers.append(timer)

    return due_timers
