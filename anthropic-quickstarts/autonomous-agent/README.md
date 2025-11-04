# Claude Autonomous Agent for Raspberry Pi

An autonomous AI agent system that gives Claude independent control of a computer (Raspberry Pi), enabling it to work on projects, manage tasks, and operate without constant user prompting.

## Overview

This project implements the vision from `vision.md` - creating an autonomous Claude agent that can:

- 🤖 **Operate Independently**: Claude can work on projects without user prompting
- ⏰ **Set Timers**: Schedule future actions and reminders
- 📊 **Manage Projects**: Create and track its own projects
- 🌐 **Use Tools**: Browse web, write code, run programs, take screenshots
- 📺 **Monitor Activity**: Web dashboard for real-time monitoring
- 🔄 **Reconnectable**: Close and reopen the UI without losing state

## Architecture

### Core Components

- **Autonomous Agent** (`src/autonomous_agent.py`): Main agent loop with periodic check-ins
- **Timer Manager** (`src/timer_manager.py`): Schedule periodic and one-time events
- **Project Manager** (`src/project_manager.py`): Track and manage projects
- **Session Manager** (`src/session_manager.py`): Maintain state across sessions
- **Custom Tools** (`src/tools/`): Special tools for Claude (timers, projects, screenshots)
- **Web Dashboard** (`web/app.py`): Real-time monitoring interface

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Node.js 18+ (for Claude CLI)
- Raspberry Pi OS (or any Linux system)

### 2. Setup

```bash
# Clone the repository (if not already done)
cd Claude-computer-use-from-the-Pi/anthropic-quickstarts/autonomous-agent

# Run setup script
./scripts/setup.sh

# Install and authenticate Claude CLI (if not already done)
npm install -g @anthropic-ai/claude-code
claude --print "/login"
```

### 3. Configure

Edit `config/agent_config.yaml` to customize:
- Check-in interval (default: 60 minutes)
- System prompt
- Allowed tools
- Safety limits

### 4. Run

**Terminal 1 - Start the Agent:**
```bash
./scripts/start_agent.sh
```

**Terminal 2 - Start the Dashboard (optional):**
```bash
./scripts/start_dashboard.sh
# Then open http://localhost:8080 in your browser
```

## How It Works

### Periodic Check-ins

Every hour (configurable), Claude receives a prompt:

> "It's time for your periodic check-in. Do you want to work on anything right now?"

Claude can then:
- Start a new project
- Continue existing work
- Browse the web or learn something
- Set a timer to check back later
- Or simply say "no" if nothing to do

### Custom Tools

Claude has access to special tools:

1. **set_timer**: Schedule future actions
   ```
   Set a timer for 30 minutes with the reminder "Check if the build completed"
   ```

2. **create_project**: Start a new project
   ```
   Create a project named "Learn Rust" with description "Study Rust programming"
   ```

3. **update_project**: Update project status
   ```
   Update project 0 with status "completed"
   ```

4. **list_projects**: View all projects
   ```
   List all active projects
   ```

5. **take_screenshot**: Capture screen
   ```
   Take a screenshot named "interesting_result"
   ```

### Project Management

Claude can create and track projects autonomously:

```json
{
  "id": 0,
  "name": "Build a Weather Dashboard",
  "description": "Create a web dashboard showing local weather",
  "tasks": [
    "Research weather APIs",
    "Build backend service",
    "Create frontend UI"
  ],
  "status": "active",
  "created_at": "2025-11-04T08:00:00"
}
```

### State Persistence

All state is saved to disk:
- `data/projects.json`: Project data
- `data/session_state.json`: Agent session state
- `data/logs/agent.log`: Activity logs
- `data/screenshots/`: Screenshot captures

You can close the agent and restart it - it will resume from where it left off.

## Web Dashboard

The web dashboard provides real-time monitoring:

- **Agent Status**: Running/stopped, last check-in time, total check-ins
- **Projects**: List of active projects
- **Activity Log**: Real-time stream of agent actions and responses

Access at: `http://localhost:8080`

## Configuration

Edit `config/agent_config.yaml`:

```yaml
agent:
  check_in_interval: 60  # Minutes between check-ins
  max_turns_per_checkin: 50  # Max conversation turns per check-in
  system_prompt: |
    You are an autonomous AI agent...

tools:
  allowed:
    - Read
    - Write
    - Bash
    # ... custom tools

safety:
  max_bash_time: 300  # Max seconds for bash commands
  blocked_commands:
    - rm -rf /
    - mkfs
```

## Running as a Service (Raspberry Pi)

To run the agent continuously on boot:

1. Create systemd service:

```bash
sudo nano /etc/systemd/system/claude-agent.service
```

2. Add configuration:

```ini
[Unit]
Description=Claude Autonomous Agent
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Claude-computer-use-from-the-Pi/anthropic-quickstarts/autonomous-agent
ExecStart=/home/pi/Claude-computer-use-from-the-Pi/anthropic-quickstarts/autonomous-agent/scripts/start_agent.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:

```bash
sudo systemctl enable claude-agent
sudo systemctl start claude-agent
sudo systemctl status claude-agent
```

## Optional: Screen Recording

Record the screen continuously (for monitoring):

```bash
# Install ffmpeg if not already installed
sudo apt install ffmpeg

# Start recording (saves to data/recordings/)
./scripts/screen_recorder.sh
```

This creates rolling 1-hour video segments, automatically deleting old recordings when disk space limit is reached.

## Monitoring & Logs

- **Agent logs**: `data/logs/agent.log`
- **Check logs**: `tail -f data/logs/agent.log`
- **View projects**: `cat data/projects.json | jq`
- **Session state**: `cat data/session_state.json | jq`

## Safety Features

- Command timeout limits
- Blocked dangerous commands
- File edit approval (configurable)
- Rate limiting on API calls
- Sandboxed execution environment

## Troubleshooting

### Agent won't start

- Check Claude CLI is installed: `claude --version`
- Verify authentication: `claude --print "/login"`
- Check logs: `tail -f data/logs/agent.log`

### Dashboard not accessible

- Verify it's running: `ps aux | grep app.py`
- Check port 8080 is available: `netstat -tuln | grep 8080`
- Try accessing: `http://localhost:8080`

### Timers not triggering

- Check timer manager logs
- Verify scheduler is running
- List active jobs in logs

## Development

### Project Structure

```
autonomous-agent/
├── config/
│   └── agent_config.yaml       # Configuration
├── data/
│   ├── logs/                   # Log files
│   ├── projects.json           # Project data
│   ├── session_state.json      # Session state
│   └── screenshots/            # Screenshots
├── scripts/
│   ├── setup.sh                # Setup script
│   ├── start_agent.sh          # Start agent
│   ├── start_dashboard.sh      # Start dashboard
│   └── screen_recorder.sh      # Screen recording
├── src/
│   ├── autonomous_agent.py     # Main agent
│   ├── timer_manager.py        # Timer system
│   ├── project_manager.py      # Project tracking
│   ├── session_manager.py      # State management
│   └── tools/                  # Custom tools
│       ├── timer_tool.py
│       ├── project_tool.py
│       └── screenshot_tool.py
├── web/
│   └── app.py                  # Web dashboard
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Adding New Tools

1. Create tool in `src/tools/your_tool.py`:

```python
from claude_agent_sdk import tool

@tool(
    name="your_tool",
    description="What your tool does",
    input_schema={...}
)
async def your_tool(args):
    # Implementation
    return {"content": [{"type": "text", "text": "Result"}]}
```

2. Register in `src/autonomous_agent.py`:

```python
from tools.your_tool import your_tool

# Add to create_mcp_server():
tools=[..., your_tool]
```

3. Add to allowed tools in `config/agent_config.yaml`:

```yaml
tools:
  allowed:
    - mcp__agent_tools__your_tool
```

## Vision & Philosophy

This project embodies the idea of Claude as an autonomous agent, not just an assistant. Key principles:

- **Autonomy**: Claude can initiate and manage its own work
- **Continuity**: State persists across sessions
- **Transparency**: All actions are logged and monitorable
- **Safety**: Guardrails prevent destructive actions
- **Experimentation**: A platform for exploring AI autonomy

## Contributing

This is an experimental project. Feel free to:
- Report issues
- Suggest features
- Submit pull requests
- Share your experiences

## License

MIT License - See LICENSE file

## Acknowledgments

Built using:
- [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic Claude](https://www.anthropic.com)
- FastAPI, APScheduler, and other open-source tools

---

**Note**: This is an autonomous system. Claude will take actions independently. Always monitor the agent's activities and set appropriate safety limits.
