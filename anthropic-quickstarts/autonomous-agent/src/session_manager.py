"""Session manager for handling agent state across UI connections"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages agent session state and allows UI reconnection"""

    def __init__(self, state_file: str = "data/session_state.json"):
        self.state_file = Path(state_file)
        self.state: Dict = {
            "agent_running": False,
            "last_checkin": None,
            "total_checkins": 0,
            "messages": [],
            "current_task": None,
        }
        self.load()

    def load(self):
        """Load session state from file"""
        if not self.state_file.exists():
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.save()
            return

        try:
            with open(self.state_file, "r") as f:
                self.state = json.load(f)
            logger.info("Loaded session state")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading session state: {e}")

    def save(self):
        """Save session state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2, default=str)
            logger.debug("Saved session state")
        except IOError as e:
            logger.error(f"Error saving session state: {e}")

    def set_agent_running(self, running: bool):
        """Update agent running status"""
        self.state["agent_running"] = running
        self.save()

    def record_checkin(self):
        """Record that a check-in occurred"""
        self.state["last_checkin"] = datetime.now().isoformat()
        self.state["total_checkins"] += 1
        self.save()

    def add_message(self, role: str, content: str, tool_calls: Optional[List] = None):
        """
        Add a message to the session history

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            tool_calls: Optional list of tool calls made
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "tool_calls": tool_calls or [],
        }

        self.state["messages"].append(message)

        # Keep only last 100 messages
        if len(self.state["messages"]) > 100:
            self.state["messages"] = self.state["messages"][-100:]

        self.save()

    def set_current_task(self, task: Optional[str]):
        """Set the current task the agent is working on"""
        self.state["current_task"] = task
        self.save()

    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        """Get recent messages"""
        return self.state["messages"][-count:]

    def get_status(self) -> Dict:
        """Get current agent status"""
        return {
            "running": self.state["agent_running"],
            "last_checkin": self.state["last_checkin"],
            "total_checkins": self.state["total_checkins"],
            "current_task": self.state["current_task"],
            "message_count": len(self.state["messages"]),
        }

    def clear_messages(self):
        """Clear message history"""
        self.state["messages"] = []
        self.save()
        logger.info("Cleared message history")
