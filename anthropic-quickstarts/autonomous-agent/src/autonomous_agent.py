"""Main autonomous agent that runs continuously"""

import asyncio
import logging
import sys
import yaml
from pathlib import Path
from typing import Optional

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server

# Import custom tools
from tools.timer_tool import set_timer, get_due_timers
from tools.project_tool import create_project, update_project, list_projects
from tools.screenshot_tool import take_screenshot

# Import managers
from timer_manager import TimerManager
from project_manager import ProjectManager
from session_manager import SessionManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/logs/agent.log"),
    ],
)

logger = logging.getLogger(__name__)


class AutonomousAgent:
    """Autonomous Claude agent with self-management capabilities"""

    def __init__(self, config_path: str = "config/agent_config.yaml"):
        self.config = self.load_config(config_path)

        # Initialize managers
        self.timer_manager = TimerManager()
        self.project_manager = ProjectManager(
            data_file=self.config["projects"]["data_file"]
        )
        self.session_manager = SessionManager()

        # Agent state
        self.running = False
        self.client: Optional[ClaudeSDKClient] = None

        logger.info("Autonomous agent initialized")

    def load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        config_file = Path(config_path)
        if not config_file.exists():
            logger.error(f"Config file not found: {config_path}")
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        logger.info(f"Loaded configuration from {config_path}")
        return config

    def create_mcp_server(self):
        """Create MCP server with custom tools"""
        return create_sdk_mcp_server(
            name="agent_tools",
            version="1.0.0",
            tools=[
                set_timer,
                create_project,
                update_project,
                list_projects,
                take_screenshot,
            ],
        )

    async def check_in(self, custom_prompt: Optional[str] = None):
        """
        Perform a check-in with Claude

        Args:
            custom_prompt: Optional custom prompt (e.g., from a timer)
        """
        logger.info("=" * 60)
        logger.info("AGENT CHECK-IN STARTING")
        logger.info("=" * 60)

        self.session_manager.record_checkin()

        # Check for due timers
        due_timers = get_due_timers()
        timer_prompts = []
        if due_timers:
            logger.info(f"Found {len(due_timers)} due timers")
            timer_prompts = [
                f"⏰ Timer alert: {timer['prompt']}" for timer in due_timers
            ]

        # Get active projects
        active_projects = self.project_manager.get_active_projects()
        project_summary = f"\nYou currently have {len(active_projects)} active project(s)."

        if active_projects:
            project_summary += "\nActive projects:"
            for proj in active_projects[:3]:  # Show max 3
                project_summary += f"\n  - {proj['name']}: {proj['description']}"

        # Build the check-in prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = (
                "It's time for your periodic check-in.\n\n"
                "Do you want to work on anything right now? You could:\n"
                "- Start a new project\n"
                "- Continue working on an existing project\n"
                "- Browse the web or learn something new\n"
                "- Set a timer to check something later\n"
                "- Or just say 'no' if you don't have anything to do\n\n"
                f"{project_summary}\n"
            )

        # Add timer alerts
        if timer_prompts:
            prompt = "\n".join(timer_prompts) + "\n\n" + prompt

        logger.info(f"Sending check-in prompt (length: {len(prompt)} chars)")
        self.session_manager.add_message("system", prompt)

        # Create MCP server and configure options
        mcp_server = self.create_mcp_server()

        options = ClaudeAgentOptions(
            system_prompt=self.config["agent"]["system_prompt"],
            max_turns=self.config["agent"]["max_turns_per_checkin"],
            allowed_tools=self.config["tools"]["allowed"],
            mcp_servers={"agent_tools": mcp_server},
            permission_mode="acceptEdits",  # Auto-accept file edits
        )

        # Query Claude
        try:
            async with ClaudeSDKClient(options=options) as client:
                self.client = client
                await client.query(prompt)

                # Stream the response
                logger.info("Receiving response from Claude...")
                full_response = []

                async for msg in client.receive_response():
                    # Log the message
                    logger.info(f"Message type: {type(msg).__name__}")

                    # Extract text content
                    if hasattr(msg, "content"):
                        for block in msg.content:
                            if hasattr(block, "text"):
                                logger.info(f"Claude: {block.text}")
                                full_response.append(block.text)
                                self.session_manager.add_message(
                                    "assistant", block.text
                                )
                            elif hasattr(block, "tool_use"):
                                logger.info(
                                    f"Tool use: {block.tool_use.get('name', 'unknown')}"
                                )

                self.client = None

                logger.info("Check-in completed successfully")
                logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Error during check-in: {e}", exc_info=True)
            self.session_manager.add_message("system", f"Error during check-in: {e}")
            logger.info("=" * 60)

    async def timer_callback(self, prompt: str = ""):
        """Callback for timer events"""
        logger.info(f"Timer triggered with prompt: {prompt}")
        await self.check_in(custom_prompt=prompt)

    async def start(self):
        """Start the autonomous agent"""
        if self.running:
            logger.warning("Agent is already running")
            return

        self.running = True
        self.session_manager.set_agent_running(True)

        logger.info("Starting autonomous agent...")
        logger.info(
            f"Check-in interval: {self.config['agent']['check_in_interval']} minutes"
        )

        # Start timer manager
        self.timer_manager.start()

        # Schedule periodic check-ins
        self.timer_manager.schedule_check_in(
            interval_minutes=self.config["agent"]["check_in_interval"],
            callback=self.check_in,
        )

        logger.info("Autonomous agent is now running!")
        logger.info("Press Ctrl+C to stop")

        # Perform initial check-in
        await self.check_in()

        # Keep running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            await self.stop()

    async def stop(self):
        """Stop the autonomous agent"""
        if not self.running:
            return

        logger.info("Stopping autonomous agent...")
        self.running = False
        self.session_manager.set_agent_running(False)

        # Stop timer manager
        self.timer_manager.stop()

        logger.info("Autonomous agent stopped")


async def main():
    """Main entry point"""
    # Ensure data directories exist
    Path("data/logs").mkdir(parents=True, exist_ok=True)

    # Create and start agent
    agent = AutonomousAgent()

    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
