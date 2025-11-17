# Quick Start Guide

> Fast reference for getting Claude running autonomously on your machine

## Installation (1 Command)

```bash
git clone https://github.com/Baswold/Claude-computer-use-from-the-Pi.git
cd Claude-computer-use-from-the-Pi
./install.sh
```

## Running Claude

### Start the Agent

```bash
cd anthropic-quickstarts/autonomous-agent
./scripts/start_agent.sh
```

**Or use Make:**
```bash
make start
```

### Start the Dashboard (Optional)

```bash
./scripts/start_dashboard.sh
```
**Then visit:** http://localhost:8080

**Or use Make:**
```bash
make dashboard
```

## Common Operations

### Using Make Commands

```bash
make help        # Show all available commands
make install     # Full installation
make start       # Start the agent
make dashboard   # Start web dashboard
make test        # Test all tools
make status      # Check agent status
make logs        # View logs (live)
make stop        # Stop all processes
```

### Manual Commands

```bash
# View logs
tail -f anthropic-quickstarts/autonomous-agent/data/logs/agent.log

# Check status
ps aux | grep autonomous_agent.py

# Stop agent
pkill -f autonomous_agent.py

# View projects
cat anthropic-quickstarts/autonomous-agent/data/projects.json

# View memory
cat anthropic-quickstarts/autonomous-agent/CLAUDE.md
```

## Configuration

Edit `anthropic-quickstarts/autonomous-agent/config/agent_config.yaml`:

```yaml
agent:
  check_in_interval: 60          # Minutes between check-ins
  max_turns_per_checkin: 50      # Max conversation turns
```

## File Locations

```
Claude-computer-use-from-the-Pi/
├── install.sh                  # One-command installer
├── Makefile                    # Quick commands
│
└── anthropic-quickstarts/autonomous-agent/
    ├── scripts/
    │   ├── start_agent.sh      # Start agent
    │   ├── start_dashboard.sh  # Start dashboard
    │   └── test_tools.sh       # Test everything
    │
    ├── config/
    │   └── agent_config.yaml   # Configuration
    │
    ├── data/
    │   ├── logs/               # Activity logs
    │   ├── screenshots/        # Screen captures
    │   ├── projects.json       # Project data
    │   └── session_state.json  # Agent state
    │
    └── CLAUDE.md               # Claude's memory
```

## Troubleshooting

### Agent Won't Start

```bash
# Re-run setup
cd anthropic-quickstarts/autonomous-agent
./scripts/setup.sh

# Check Claude CLI
claude --version
claude --print "/login"
```

### Dashboard Not Working

```bash
# Check if it's running
ps aux | grep app.py

# Check port
sudo lsof -i :8080

# Restart
pkill -f app.py
./scripts/start_dashboard.sh
```

### Authentication Issues

```bash
# Re-authenticate
claude --print "/logout"
claude --print "/login"
```

## What Happens When Running?

1. **Initial Check-in**: Claude reads memory and evaluates current state
2. **Periodic Check-ins**: Every hour (configurable), Claude asks "What should I work on?"
3. **Autonomous Work**: Claude can:
   - Create and manage projects
   - Set timers for future work
   - Browse the web
   - Write code
   - Take screenshots
   - Update its memory
4. **Logging**: All actions logged to `data/logs/agent.log`
5. **Persistence**: Everything saved automatically

## Tips

- **Monitor Initially**: Watch the dashboard/logs for the first day
- **Review CLAUDE.md**: See what Claude is thinking
- **Start Small**: Use short check-in intervals at first
- **Use the Dashboard**: It's the easiest way to monitor
- **Check Logs**: `make logs` shows real-time activity

## Quick Reference

| Task | Command |
|------|---------|
| Install | `./install.sh` |
| Start agent | `make start` |
| Start dashboard | `make dashboard` |
| View logs | `make logs` |
| Check status | `make status` |
| Test tools | `make test` |
| Stop everything | `make stop` |
| View projects | `make projects` |
| View memory | `make memory` |

## Next Steps

- Read the full [README.md](README.md)
- Check [vision.md](vision.md) for the project philosophy
- Read detailed docs in [anthropic-quickstarts/autonomous-agent/README.md](anthropic-quickstarts/autonomous-agent/README.md)
- Configure `agent_config.yaml` to your preferences
- Set up as a systemd service for auto-start on boot

## Support

- Check the documentation files
- Look at existing issues on GitHub
- Test with `make test` to verify setup

---

**That's it! You now have Claude running autonomously. Watch the magic happen! ✨**
