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
   ║         C O M P U T E R   U S E   F R O M   P I           ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
```

# Claude Autonomous Agent for Raspberry Pi

### Give Claude true ownership of a computer. Watch it create, learn, and operate autonomously.

[![Status](https://img.shields.io/badge/status-production-success.svg)]()
[![Version](https://img.shields.io/badge/version-3.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

**An experimental system that gives Claude independent control of a Raspberry Pi (or any Linux computer), enabling it to work on projects, set timers, browse the web, and operate as an autonomous developer.**

</div>

---

## Quick Start (3 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/Baswold/Claude-computer-use-from-the-Pi.git
cd Claude-computer-use-from-the-Pi

# 2. Run the automated setup (installs everything)
./install.sh

# 3. Start the agent
cd anthropic-quickstarts/autonomous-agent
./scripts/start_agent.sh
```

That's it! Claude will start running autonomously on your machine.

**Optional**: Start the web dashboard to monitor Claude's activities:
```bash
./scripts/start_dashboard.sh
# Open http://localhost:8080 in your browser
```

---

## What Is This?

This project gives Claude **true autonomy** on a computer. Unlike a typical chatbot that waits for prompts, this Claude:

- **Works independently**: Checks in periodically asking itself "What should I work on?"
- **Creates projects**: Can conceive ideas and execute on them without human direction
- **Sets timers**: Schedules future work and manages its own time
- **Has persistent memory**: Remembers everything across sessions via CLAUDE.md files
- **Controls the system**: Full access to file operations, code execution, web browsing, and more
- **Self-monitors**: Tracks its own projects, status, and learnings

### Example Use Cases

- **Autonomous Developer**: "Hire" Claude as a developer that works on projects independently
- **Research Assistant**: Claude can research topics, compile findings, and schedule follow-ups
- **System Monitor**: Have Claude check on system health and report issues
- **Learning Companion**: Claude can learn new technologies and document findings
- **Task Automation**: Set up recurring tasks that Claude handles autonomously

---

## Features

### Core Capabilities

- **Autonomous Operation**: Hourly check-ins where Claude decides what to work on
- **15 Powerful Tools**: File ops, code execution, web access, screenshots, system monitoring, and more
- **Project Management**: Claude creates and tracks its own projects
- **Timer System**: Schedule future actions and recurring tasks
- **Persistent Memory**: CLAUDE.md files maintain context across all sessions
- **Web Dashboard**: Beautiful real-time monitoring interface
- **Cost Optimized**: ~90% cost reduction through prompt caching
- **Production Ready**: Error recovery, logging, session persistence

### Tools Claude Has Access To

<details>
<summary><b>Click to see all 15 tools</b></summary>

1. **Read** - Read any file on the system
2. **Write** - Create new files
3. **Edit** - Modify existing files
4. **Bash** - Execute shell commands
5. **Glob** - Find files by pattern
6. **Grep** - Search file contents
7. **WebFetch** - Fetch and analyze web pages
8. **WebSearch** - Search the internet
9. **Timer** - Set scheduled callbacks
10. **CreateProject** - Initialize new projects
11. **UpdateProject** - Manage project status
12. **ListProjects** - View all projects
13. **UpdateMemory** - Persist notes across sessions
14. **Screenshot** - Capture screen state
15. **SystemHealth** - Monitor CPU, memory, disk usage

</details>

---

## System Requirements

<table>
<tr>
<td width="50%">

**Minimum Requirements**
- Python 3.10 or higher
- Node.js 18 or higher (for Claude CLI)
- 2GB RAM (4GB recommended)
- Linux, macOS, or WSL2 on Windows
- Active internet connection

</td>
<td width="50%">

**Recommended Setup**
- Raspberry Pi 4 (4GB or 8GB)
- Debian/Ubuntu-based OS
- 20GB+ free disk space
- Monitor and keyboard (for setup)

</td>
</tr>
</table>

---

## Installation

### Automated Installation (Recommended)

The easiest way to get started:

```bash
git clone https://github.com/Baswold/Claude-computer-use-from-the-Pi.git
cd Claude-computer-use-from-the-Pi
chmod +x install.sh
./install.sh
```

The install script will:
- Check all prerequisites (Python, Node.js)
- Install Claude CLI if needed
- Set up Python virtual environment
- Install all dependencies
- Create necessary directories
- Guide you through authentication
- Verify everything works

### Manual Installation

If you prefer manual setup:

```bash
# 1. Navigate to the agent directory
cd anthropic-quickstarts/autonomous-agent

# 2. Run setup
./scripts/setup.sh

# 3. Install Claude CLI (if not already installed)
npm install -g @anthropic-ai/claude-code

# 4. Authenticate
claude --print "/login"
```

---

## Usage

### Starting the Agent

```bash
cd anthropic-quickstarts/autonomous-agent
./scripts/start_agent.sh
```

Claude will:
1. Initialize and read its memory
2. Check for active projects
3. Perform an initial check-in
4. Continue with periodic check-ins (default: every 60 minutes)
5. Execute on any timers or scheduled tasks

### Monitoring Claude

**Option 1: Web Dashboard (Recommended)**
```bash
./scripts/start_dashboard.sh
```
Then visit http://localhost:8080 to see:
- Real-time agent status
- Live activity stream
- Active projects list
- System health

**Option 2: Log Files**
```bash
tail -f data/logs/agent.log
```

**Option 3: Screenshots**
```bash
ls -lt data/screenshots/
```

### Configuring the Agent

Edit `config/agent_config.yaml`:

```yaml
agent:
  check_in_interval: 60  # Minutes between autonomous check-ins
  max_turns_per_checkin: 50  # Max conversation turns per session

  system_prompt: |
    You are an autonomous AI agent with independent ownership of this computer.
    You can work on projects, learn new things, and manage your own time.
```

---

## Project Structure

```
Claude-computer-use-from-the-Pi/
├── install.sh                          # One-command installer
├── README.md                           # This file
├── QUICKSTART.md                       # Quick reference guide
├── Makefile                            # Common operations
│
├── anthropic-quickstarts/
│   └── autonomous-agent/               # Main agent system
│       ├── scripts/
│       │   ├── setup.sh                # Setup dependencies
│       │   ├── start_agent.sh          # Launch agent
│       │   ├── start_dashboard.sh      # Launch web UI
│       │   └── test_tools.sh           # Test all tools
│       │
│       ├── src/
│       │   ├── autonomous_agent.py     # Main orchestration
│       │   ├── timer_manager.py        # Scheduling system
│       │   ├── project_manager.py      # Project tracking
│       │   ├── session_manager.py      # State persistence
│       │   └── tools/                  # Custom MCP tools
│       │
│       ├── web/
│       │   └── app.py                  # Dashboard backend
│       │
│       ├── config/
│       │   └── agent_config.yaml       # Configuration
│       │
│       ├── data/                       # Generated at runtime
│       │   ├── logs/                   # Activity logs
│       │   ├── screenshots/            # Screen captures
│       │   ├── projects.json           # Project data
│       │   └── session_state.json      # Agent state
│       │
│       ├── CLAUDE.md                   # Agent's persistent memory
│       └── README.md                   # Detailed documentation
│
└── vision.md                           # Project philosophy
```

---

## Running as a Service (Advanced)

To have Claude start automatically on boot:

```bash
cd anthropic-quickstarts/autonomous-agent

# Install as systemd service
sudo cp claude-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable claude-agent
sudo systemctl start claude-agent

# Check status
sudo systemctl status claude-agent
```

---

## Testing

Verify all tools work correctly:

```bash
cd anthropic-quickstarts/autonomous-agent
./scripts/test_tools.sh
```

This comprehensive test will:
- Test all file operations
- Test search and grep
- Test web browsing (opens Chromium)
- Test project management
- Test memory persistence
- Test screenshots
- Generate a detailed report

---

## Troubleshooting

### Agent won't start

**Problem**: `Virtual environment not found`
```bash
cd anthropic-quickstarts/autonomous-agent
./scripts/setup.sh
```

**Problem**: `Claude CLI not found`
```bash
npm install -g @anthropic-ai/claude-code
claude --print "/login"
```

**Problem**: `Authentication failed`
```bash
claude --print "/logout"
claude --print "/login"
```

### Dashboard not accessible

**Problem**: Port 8080 already in use
```bash
# Check what's using the port
sudo lsof -i :8080
# Kill the process or change the port in .env
```

**Problem**: Can't connect from another device
```bash
# Make sure WEB_HOST is set to 0.0.0.0 in .env
echo "WEB_HOST=0.0.0.0" >> .env
```

### Common Issues

<details>
<summary><b>Python version too old</b></summary>

```bash
python3 --version  # Should be 3.10+

# On Debian/Ubuntu:
sudo apt update
sudo apt install python3.10 python3.10-venv

# On macOS:
brew install python@3.10
```
</details>

<details>
<summary><b>Node.js version too old</b></summary>

```bash
node --version  # Should be 18+

# Install via nvm (recommended):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```
</details>

<details>
<summary><b>Permission denied errors</b></summary>

```bash
# Make scripts executable
chmod +x install.sh
chmod +x anthropic-quickstarts/autonomous-agent/scripts/*.sh
```
</details>

---

## Cost & API Usage

Claude uses the Anthropic API which charges per token. However, this system is highly optimized:

**Prompt Caching**: Reduces costs by ~90% by caching:
- System prompt and instructions
- CLAUDE.md memory file
- Configuration and context

**Typical costs** (with caching):
- Hourly check-in: ~$0.01-0.05
- Active work session: ~$0.10-0.50
- **Daily operation**: ~$1-5 depending on activity

**Without your own API key**: Use Claude CLI which requires an Anthropic account but handles billing automatically.

---

## Safety & Limitations

### Built-in Safety Features

- Command timeout limits (max 5 minutes per bash command)
- Blocked dangerous commands (`rm -rf /`, `mkfs`, etc.)
- Sandboxed execution environment
- File operation approval (configurable)
- Rate limiting on API calls
- All actions logged for review

### What Claude Can't Do (By Design)

- Access files outside the project directory (unless configured)
- Make irreversible system changes without explicit permission
- Access sensitive system directories
- Run as root (not recommended)

### Recommendations

- **Start in a VM or Raspberry Pi**: Don't run on your main production machine initially
- **Monitor initially**: Watch the dashboard/logs for the first few days
- **Review CLAUDE.md**: Check what Claude is thinking and planning
- **Set conservative limits**: Use shorter check-in intervals initially
- **Backup important data**: As with any automated system

---

## Use Cases & Examples

### 1. Autonomous Developer

Let Claude work on coding projects independently:

```bash
# Claude might:
# - Read your project files
# - Identify bugs or improvements
# - Write tests
# - Refactor code
# - Update documentation
# - Set timers to check build status
```

### 2. Learning Companion

Have Claude learn and document technologies:

```bash
# Claude might:
# - Research WebAssembly
# - Create practice projects
# - Document findings in CLAUDE.md
# - Build example code
# - Schedule follow-up learning sessions
```

### 3. System Monitor

Monitor your Raspberry Pi's health:

```bash
# Claude might:
# - Check system resources hourly
# - Alert if disk space is low
# - Monitor long-running processes
# - Take screenshots of dashboards
# - Log findings for review
```

---

## Philosophy

This project explores **AI autonomy** - moving beyond chatbots to genuine AI agency:

- **Autonomy over Assistance**: Claude as operator, not just helper
- **Continuous Operation**: Always available, always thinking
- **Transparency**: All actions logged and observable
- **Safety with Freedom**: Guardrails that don't restrict creativity
- **Experimentation**: A platform for exploring what's possible

See [vision.md](vision.md) for the complete vision.

---

## Contributing

This is an experimental project exploring AI autonomy. Contributions welcome:

- Report bugs via GitHub Issues
- Suggest features or improvements
- Submit pull requests
- Share your experiences and use cases

---

## Documentation

- **[README.md](README.md)** - This file (overview and quick start)
- **[QUICKSTART.md](QUICKSTART.md)** - Fast reference guide
- **[anthropic-quickstarts/autonomous-agent/README.md](anthropic-quickstarts/autonomous-agent/README.md)** - Detailed agent documentation
- **[vision.md](vision.md)** - Project philosophy and vision
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Technical architecture

---

## Credits & License

Built with:
- [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic Claude](https://www.anthropic.com)
- FastAPI, APScheduler, and other open-source tools

**License**: MIT

---

## Support

- **Documentation**: Check the docs in this repository
- **Issues**: Report bugs on GitHub Issues
- **Community**: Share experiences in Discussions

---

<div align="center">

**Ready to give Claude true autonomy?**

```bash
git clone https://github.com/Baswold/Claude-computer-use-from-the-Pi.git
cd Claude-computer-use-from-the-Pi
./install.sh
```

**Then watch it create, learn, and operate independently.**

</div>
