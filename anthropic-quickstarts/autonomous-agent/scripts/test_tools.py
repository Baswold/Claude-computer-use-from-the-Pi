#!/usr/bin/env python3
"""Test script that asks Claude to test all available tools"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server

# Import custom tools
from tools.timer_tool import set_timer, get_due_timers
from tools.project_tool import create_project, update_project, list_projects
from tools.screenshot_tool import take_screenshot
from tools.memory_tool import update_memory, read_memory
from tools.system_tool import check_system_health, list_processes


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def create_mcp_server():
    """Create MCP server with all custom tools"""
    return create_sdk_mcp_server(
        name="agent_tools",
        version="2.0.0",
        tools=[
            # Timer management
            set_timer,
            # Project management
            create_project,
            update_project,
            list_projects,
            # Memory management
            update_memory,
            read_memory,
            # System monitoring
            check_system_health,
            list_processes,
            # Utilities
            take_screenshot,
        ],
    )


async def run_test():
    """Run the tool test"""
    logger = logging.getLogger(__name__)

    logger.info("=" * 70)
    logger.info("CLAUDE TOOLS TEST SCRIPT")
    logger.info("=" * 70)

    # Get project root
    project_root = Path(__file__).parent.parent

    # Ensure required directories exist
    (project_root / "data/logs").mkdir(parents=True, exist_ok=True)
    (project_root / "data/screenshots").mkdir(parents=True, exist_ok=True)
    (project_root / ".claude").mkdir(parents=True, exist_ok=True)

    # Create MCP server with custom tools
    mcp_server = create_mcp_server()

    # System prompt
    system_prompt = """You are Claude, an AI assistant helping to test all available tools.
You have access to both standard tools and custom MCP tools.

AVAILABLE TOOLS:
Standard Tools:
- Read: Read files
- Write: Write files
- Edit: Edit files
- Bash: Execute bash commands
- Glob: Find files by pattern
- Grep: Search file contents
- WebFetch: Fetch web content
- WebSearch: Search the web

Custom MCP Tools (prefixed with mcp__agent_tools__):
- set_timer: Set a timer for future events
- create_project: Create a new project
- update_project: Update project status
- list_projects: List all projects
- update_memory: Update persistent memory
- read_memory: Read persistent memory
- check_system_health: Check system resources
- list_processes: List running processes
- take_screenshot: Capture a screenshot

Your task is to systematically test these tools and provide a comprehensive report.
"""

    # Test prompt
    test_prompt = """Please test all your available tools in the following way:

1. **File Tools**: Create a test file, read it, edit it, and verify the changes
2. **Search Tools**: Use Glob to find Python files, use Grep to search for a pattern
3. **Memory Tools**: Read your memory, then update it with test information
4. **System Tools**: Check system health and list some processes
5. **Project Tools**: Create a test project, list projects, then update the project status
6. **Screenshot Tool**: Take a screenshot named "test_screenshot"
7. **Timer Tool**: Set a test timer for 5 minutes in the future
8. **Bash Tool**: Execute a simple bash command like 'echo "Test successful"'
9. **Web Browser**: Open Chromium browser and navigate to Apple.com
10. **Report**: After completing all tests, provide a summary of:
    - Which tools worked successfully
    - Any tools that failed or had issues
    - Information about each tool's capabilities
    - Screenshots or evidence of the browser test

IMPORTANT: For the browser test (#9), use the Bash tool to:
- Launch Chromium browser with: chromium-browser --new-window https://apple.com
- Wait a few seconds for it to load
- Take a screenshot to show it worked
- Then you can close it

When you're done, say "I have completed testing all tools!" and provide your detailed report.
"""

    # Configure options
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        max_turns=100,  # Allow plenty of turns for testing
        allowed_tools=[
            # Standard tools
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Glob",
            "Grep",
            "WebFetch",
            "WebSearch",
            # Custom MCP tools
            "mcp__agent_tools__set_timer",
            "mcp__agent_tools__create_project",
            "mcp__agent_tools__update_project",
            "mcp__agent_tools__list_projects",
            "mcp__agent_tools__update_memory",
            "mcp__agent_tools__read_memory",
            "mcp__agent_tools__check_system_health",
            "mcp__agent_tools__list_processes",
            "mcp__agent_tools__take_screenshot",
        ],
        mcp_servers={"agent_tools": mcp_server},
        permission_mode="acceptEdits",
        cwd=str(project_root),
        setting_sources=["project"],
    )

    logger.info("Starting tool test session...")
    logger.info(f"Project root: {project_root}")
    logger.info("=" * 70)

    try:
        async with ClaudeSDKClient(options=options) as client:
            # Send the test prompt
            await client.query(test_prompt)

            # Stream and log the response
            logger.info("\n" + "=" * 70)
            logger.info("CLAUDE'S RESPONSE:")
            logger.info("=" * 70 + "\n")

            full_response = []
            tool_count = 0
            tools_used = []

            async for msg in client.receive_response():
                if hasattr(msg, "content"):
                    for block in msg.content:
                        if hasattr(block, "text"):
                            # Print text responses
                            print(block.text)
                            full_response.append(block.text)
                        elif hasattr(block, "tool_use"):
                            tool_count += 1
                            tool_name = block.tool_use.get("name", "unknown")
                            tools_used.append(tool_name)
                            logger.info(f"\n[Tool #{tool_count}] Using: {tool_name}")

            logger.info("\n" + "=" * 70)
            logger.info("TEST SUMMARY")
            logger.info("=" * 70)
            logger.info(f"Total tools used: {tool_count}")
            logger.info(f"Tools invoked: {', '.join(set(tools_used))}")
            logger.info("=" * 70)

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)
        sys.exit(1)


async def main():
    """Main entry point"""
    setup_logging()
    await run_test()
    logging.info("\nTest script completed!")


if __name__ == "__main__":
    asyncio.run(main())
