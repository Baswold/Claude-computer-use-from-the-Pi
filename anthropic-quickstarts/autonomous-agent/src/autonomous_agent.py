"""Main autonomous agent that runs continuously"""

import asyncio
import logging
import signal
import sys
import yaml
from pathlib import Path
from typing import Optional

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server

# Import custom tools
from tools.timer_tool import set_timer, get_due_timers
from tools.project_tool import create_project, update_project, list_projects
from tools.screenshot_tool import take_screenshot, list_screenshots
from tools.memory_tool import update_memory, read_memory
from tools.system_tool import check_system_health, list_processes
from tools.journal_tool import log_thought, read_thoughts, log_activity
from tools.file_tool import find_files, quick_note

# Import managers
from timer_manager import TimerManager
from project_manager import ProjectManager
from session_manager import SessionManager

# Logger will be configured in main()
logger = logging.getLogger(__name__)


class AutonomousAgent:
    """Autonomous Claude agent with self-management capabilities"""

    def __init__(self, config_path: str = "config/agent_config.yaml"):
        self.config = self.load_config(config_path)

        # Set working directory to project root
        self.project_root = Path(__file__).parent.parent

        # Initialize managers
        self.timer_manager = TimerManager()
        self.project_manager = ProjectManager(
            data_file=str(self.project_root / self.config["projects"]["data_file"])
        )
        self.session_manager = SessionManager(
            state_file=str(self.project_root / "data/session_state.json")
        )

        # Agent state
        self.running = False
        self.client: Optional[ClaudeSDKClient] = None

        logger.info("Autonomous agent initialized")
        logger.info(f"Project root: {self.project_root}")

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
            version="3.0.0",  # Bumped for major tool expansion
            tools=[
                # Timer management (1 tool)
                set_timer,
                # Project management (3 tools)
                create_project,
                update_project,
                list_projects,
                # Memory management (2 tools)
                update_memory,
                read_memory,
                # System monitoring (2 tools)
                check_system_health,
                list_processes,
                # Screenshots & documentation (2 tools)
                take_screenshot,
                list_screenshots,
                # Journal & activity logging (3 tools)
                log_thought,
                read_thoughts,
                log_activity,
                # File utilities (2 tools)
                find_files,
                quick_note,
            ],
        )
        # Total: 15 powerful tools for autonomous operation

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

        # Configure options with memory and prompt caching support
        options = ClaudeAgentOptions(
            system_prompt=self.config["agent"]["system_prompt"],
            max_turns=self.config["agent"]["max_turns_per_checkin"],
            allowed_tools=self.config["tools"]["allowed"],
            mcp_servers={"agent_tools": mcp_server},
            permission_mode="acceptEdits",  # Auto-accept file edits
            cwd=str(self.project_root),  # Set working directory
            setting_sources=["project"],  # Enable CLAUDE.md memory file for persistence
        )

        logger.info("Agent configured with CLAUDE.md memory support")

        # Query Claude with retry logic
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                async with ClaudeSDKClient(options=options) as client:
                    self.client = client
                    await client.query(prompt)

                    # Stream the response
                    logger.info("Receiving response from Claude...")
                    full_response = []
                    tool_count = 0

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
                                    tool_count += 1
                                    tool_name = block.tool_use.get('name', 'unknown')
                                    logger.info(f"Tool use #{tool_count}: {tool_name}")

                    self.client = None

                    logger.info(f"Check-in completed successfully ({tool_count} tools used)")
                    logger.info("=" * 60)
                    break  # Success, exit retry loop

            except KeyboardInterrupt:
                raise  # Don't catch Ctrl+C
            except Exception as e:
                logger.error(f"Error during check-in (attempt {attempt + 1}/{max_retries}): {e}", exc_info=True)

                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error("Max retries reached. Check-in failed.")
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
    # Get project root
    project_root = Path(__file__).parent.parent

    # Ensure all required directories exist
    (project_root / "data/logs").mkdir(parents=True, exist_ok=True)
    (project_root / "data/screenshots").mkdir(parents=True, exist_ok=True)
    (project_root / ".claude").mkdir(parents=True, exist_ok=True)

    # Configure logging with absolute paths
    log_file = project_root / "data/logs/agent.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(str(log_file)),
        ],
        force=True,  # Override any previous configuration
    )

    # Beautiful startup banner
    logger.info("=" * 70)
    logger.info("   ╔═══════════════════════════════════════════════════════════╗")
    logger.info("   ║                                                           ║")
    logger.info("   ║      ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗   ║")
    logger.info("   ║     ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝   ║")
    logger.info("   ║     ██║     ██║     ███████║██║   ██║██║  ██║█████╗     ║")
    logger.info("   ║     ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝     ║")
    logger.info("   ║     ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗   ║")
    logger.info("   ║      ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝   ║")
    logger.info("   ║                                                           ║")
    logger.info("   ║            A U T O N O M O U S   A G E N T                ║")
    logger.info("   ║                       v 2.0                               ║")
    logger.info("   ║                                                           ║")
    logger.info("   ╚═══════════════════════════════════════════════════════════╝")
    logger.info("=" * 70)
    logger.info("")
    logger.info("⚙️  Configuration")
    logger.info(f"   • Project root:  {project_root}")
    logger.info(f"   • Log file:      {log_file}")
    logger.info(f"   • Memory file:   {project_root / 'CLAUDE.md'}")
    logger.info("")
    logger.info("✨ Features")
    logger.info("   • Persistent Memory (CLAUDE.md)")
    logger.info("   • Automatic Prompt Caching (~90% cost reduction)")
    logger.info("   • System Monitoring & Health Checks")
    logger.info("   • Intelligent Retry Logic")
    logger.info("   • Project Management")
    logger.info("   • Timer System")
    logger.info("")
    logger.info("=" * 70)

    # Create and start agent
    agent = AutonomousAgent()

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}. Initiating graceful shutdown...")
        asyncio.create_task(agent.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        await agent.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        await agent.stop()
        sys.exit(1)
    finally:
        logger.info("Agent shutdown complete")
        logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
