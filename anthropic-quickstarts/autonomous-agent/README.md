<div align="center">

```
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║      ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗   ║
   ║     ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝   ║
   ║     ██║     ██║     ███████║██║   ██║██║  ██║█████╗     ║
   ║     ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝     ║
   ║     ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗   ║
   ║      ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝   ║
   ║                                                           ║
   ║            A U T O N O M O U S   A G E N T                ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
```

### *Give AI true autonomy. Watch it create.*

**An autonomous AI agent system that gives Claude independent ownership of a computer, enabling it to conceive ideas, manage projects, and execute tasks without constant human intervention.**

[![Status](https://img.shields.io/badge/status-production-success.svg)]()
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

</div>

---

## ✨ What Makes This Different

This isn't just another chatbot. This is Claude with **genuine autonomy**—owning a computer, making decisions, and executing on ideas independently.

### Core Capabilities

<table>
<tr>
<td width="50%">

**🧠 True Autonomy**
- Self-initiated work sessions
- Independent project creation
- Autonomous decision-making
- Persistent memory across sessions

</td>
<td width="50%">

**⚡️ Production Ready**
- 90% cost reduction via caching
- Automatic error recovery
- Session persistence
- Enterprise-grade logging

</td>
</tr>
<tr>
<td width="50%">

**🛠 Full Tool Access**
- File system operations
- Code execution
- Web browsing & search
- System monitoring
- Project management

</td>
<td width="50%">

**📊 Real-Time Monitoring**
- Beautiful web dashboard
- Live activity streams
- Project tracking
- Reconnectable UI

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

<table>
<tr>
<td width="33%">

**Python 3.10+**
```bash
python3 --version
```

</td>
<td width="33%">

**Node.js 18+**
```bash
node --version
```

</td>
<td width="33%">

**Claude CLI**
```bash
npm install -g @anthropic-ai/claude-code
```

</td>
</tr>
</table>

### Installation

**Step 1:** Navigate to the agent directory
```bash
cd Claude-computer-use-from-the-Pi/anthropic-quickstarts/autonomous-agent
```

**Step 2:** Run the automated setup
```bash
./scripts/setup.sh
```

**Step 3:** Authenticate Claude CLI
```bash
claude --print "/login"
```

**Step 4:** Customize your agent *(optional)*
```bash
nano config/agent_config.yaml
```

### Launch

<table>
<tr>
<td width="50%">

**🤖 Start the Agent**
```bash
./scripts/start_agent.sh
```

Launches the autonomous agent with periodic check-ins

</td>
<td width="50%">

**📊 Start the Dashboard** *(optional)*
```bash
./scripts/start_dashboard.sh
```

Open **http://localhost:8080** in your browser

</td>
</tr>
</table>

### Verify Everything Works

```bash
./scripts/test_tools.sh
```

This comprehensive test will verify all tools are functioning correctly, including opening Chromium and demonstrating web automation capabilities.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AUTONOMOUS AGENT                         │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Periodic   │  │    Timer     │  │   Project    │     │
│  │  Check-ins   │  │  Callbacks   │  │   Tracking   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      CUSTOM TOOLS (MCP)                      │
│                                                              │
│  Timer │ Projects │ Memory │ System │ Screenshots           │
└──────────────────────────┬───────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
  ┌─────────────────┐          ┌─────────────────┐
  │  Web Dashboard  │          │ Data Persistence│
  │  localhost:8080 │          │  CLAUDE.md      │
  │                 │          │  projects.json  │
  │  • Live status  │          │  logs/          │
  │  • Activity log │          │  screenshots/   │
  │  • Projects     │          └─────────────────┘
  └─────────────────┘
```

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Autonomous Agent** | Main orchestration loop | `src/autonomous_agent.py` |
| **Timer Manager** | Schedule events and callbacks | `src/timer_manager.py` |
| **Project Manager** | Track and manage projects | `src/project_manager.py` |
| **Session Manager** | Maintain state persistence | `src/session_manager.py` |
| **Custom Tools** | Extended capabilities | `src/tools/` |
| **Web Dashboard** | Real-time monitoring UI | `web/app.py` |

---

## 💡 How It Works

### The Autonomy Loop

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  1. ⏰ Periodic Check-in (every N minutes)          │
│     "Do you want to work on anything?"              │
│                                                     │
│  2. 🤔 Claude Evaluates                             │
│     • Reads persistent memory                       │
│     • Checks active projects                        │
│     • Reviews system state                          │
│                                                     │
│  3. ⚡️ Claude Decides & Acts                         │
│     • Start new project                             │
│     • Continue existing work                        │
│     • Research and learn                            │
│     • Set timers for later                          │
│     • Or rest if nothing to do                      │
│                                                     │
│  4. 💾 State Persists                               │
│     Everything saved automatically                  │
│                                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     └──────> Repeat ♾
```

### Custom Tool Arsenal

Claude has access to specialized tools beyond standard capabilities:

<table>
<tr>
<td width="50%">

**⏰ Timer Management**
```python
set_timer(
  minutes=30,
  prompt="Check build status"
)
```
Schedule future check-ins with custom prompts

</td>
<td width="50%">

**📋 Project Management**
```python
create_project(
  name="Learn Rust",
  description="Master systems programming"
)
```
Create and track multi-step initiatives

</td>
</tr>
<tr>
<td width="50%">

**🧠 Memory Management**
```python
update_memory(
  content="Key insights from research..."
)
```
Persistent notes across all sessions

</td>
<td width="50%">

**📊 System Monitoring**
```python
check_system_health()
list_processes()
```
Monitor resources and running tasks

</td>
</tr>
<tr>
<td width="50%">

**📸 Screenshots**
```python
take_screenshot(
  name="ui_mockup"
)
```
Capture visual state for reference

</td>
<td width="50%">

**🗂 Project Tracking**
```python
update_project(
  project_id=0,
  status="completed"
)
```
Maintain organized workflow

</td>
</tr>
</table>

### Example: A Day in Claude's Life

```
08:00 AM  ⏰ Check-in: Read memory, review projects
          💭 Idea: "I should learn about WebAssembly"
          📝 Create project: "Explore WebAssembly"
          ⏰ Set timer for 2 hours

10:00 AM  ⏰ Timer fires: "Continue WebAssembly exploration"
          🌐 Research WebAssembly documentation
          💾 Update memory with key learnings
          📝 Update project status

12:00 PM  ⏰ Check-in: No urgent work
          😴 "I'll rest for now"

02:00 PM  ⏰ Check-in: Continue project
          💻 Write example code
          📸 Take screenshot of results
          📝 Mark project as completed
```

### Data Persistence

Everything is automatically saved to disk:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Persistent memory and context |
| `data/projects.json` | All project data and metadata |
| `data/session_state.json` | Agent state and check-in history |
| `data/logs/agent.log` | Complete activity log |
| `data/screenshots/` | Visual captures for reference |

**Close the agent, reboot the Pi, restart anytime** — Claude picks up exactly where it left off.

---

## 📊 Web Dashboard

A beautiful, real-time monitoring interface at **http://localhost:8080**

### Features

- **🟢 Agent Status** — Running/stopped, last check-in, total sessions
- **📁 Active Projects** — Live project list with descriptions
- **📜 Activity Stream** — Real-time feed of Claude's actions and thoughts
- **🔄 Auto-Refresh** — Updates every 5 seconds
- **📱 Responsive Design** — Works on desktop, tablet, and mobile

### Dashboard Preview

```
╔════════════════════════════════════════════════════════╗
║  🤖 Claude Autonomous Agent                            ║
║  Real-time monitoring dashboard                        ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Agent Status              Projects                    ║
║  ┌──────────────┐         ┌──────────────┐           ║
║  │ Status: 🟢   │         │ 3 Active     │           ║
║  │ Running      │         │              │           ║
║  │              │         │ • Learn Rust │           ║
║  │ Last: 2m ago │         │ • Web Scraper│           ║
║  │ Total: 247   │         │ • API Client │           ║
║  └──────────────┘         └──────────────┘           ║
║                                                        ║
║  Activity Log                                          ║
║  ┌────────────────────────────────────────────────┐   ║
║  │ [14:32] assistant: Checking project status...  │   ║
║  │ [14:31] system: Timer triggered                │   ║
║  │ [14:29] assistant: Updated memory with notes  │   ║
║  └────────────────────────────────────────────────┘   ║
╚════════════════════════════════════════════════════════╝
```

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

## Testing

### Test All Tools

Run a comprehensive test of all available tools (useful for verification and debugging):

```bash
./scripts/test_tools.sh
```

This test script will ask Claude to:
- ✅ Test all file operations (Read, Write, Edit)
- ✅ Test search tools (Glob, Grep)
- ✅ Test memory management (read/update memory)
- ✅ Test system monitoring (check health, list processes)
- ✅ Test project management (create, list, update projects)
- ✅ Test utilities (screenshots, timers)
- ✅ Test bash execution
- ✅ Open Chromium browser and navigate to a website
- ✅ Provide a detailed report of results

The test generates:
- Console output showing each tool being tested
- Screenshot evidence (in `data/screenshots/`)
- A summary report of which tools succeeded/failed

**What to expect:**
- The script will run for a few minutes as Claude systematically tests each tool
- You'll see real-time output of tool usage
- Browser windows may open/close during the web browser test
- A final summary shows total tools used and their names

**Useful for:**
- Verifying setup is correct
- Debugging tool issues
- Demonstrating capabilities
- Learning what tools are available

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
│   ├── screen_recorder.sh      # Screen recording
│   ├── test_tools.py           # Tool testing script
│   └── test_tools.sh           # Tool testing wrapper
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
