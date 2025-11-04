# Implementation Plan: Autonomous Claude Agent for Raspberry Pi

## Overview
Build an autonomous agent system where Claude can independently control a Raspberry Pi, take on projects, set timers, and operate without constant user prompting.

## Architecture

### Core Components

1. **Autonomous Agent Loop** (`autonomous_agent.py`)
   - Main agent loop using Claude Agent SDK
   - Periodic timer system (hourly check-ins)
   - State persistence between sessions
   - Project queue management

2. **Timer System** (`timer_manager.py`)
   - Schedule periodic prompts
   - Support for custom timers Claude can set
   - Wake agent from sleep at scheduled times

3. **Project Manager** (`project_manager.py`)
   - Track ongoing projects
   - Store project state
   - Allow Claude to create/manage its own projects

4. **Logging & Monitoring** (`monitor.py`)
   - Stream tool calls to log files
   - Screenshot capture system
   - Real-time log viewing interface
   - Web-based dashboard for monitoring

5. **Session Manager** (`session_manager.py`)
   - Handle UI disconnect/reconnect
   - Maintain agent state across sessions
   - Allow multiple viewers

6. **Screen Recording** (optional, `screen_recorder.sh`)
   - Rolling screen capture with ffmpeg
   - Automatic cleanup/rollover
   - Storage management

## Implementation Steps

### Phase 1: Core Agent Setup
- [ ] Create basic autonomous agent using Claude Agent SDK
- [ ] Implement state persistence (SQLite or JSON)
- [ ] Set up project directory structure
- [ ] Configure Claude CLI authentication

### Phase 2: Timer System
- [ ] Build timer manager with schedule library
- [ ] Implement hourly check-in system
- [ ] Add custom timer API for Claude to use
- [ ] Create timer persistence across restarts

### Phase 3: Project Management
- [ ] Design project data model
- [ ] Create project CRUD operations
- [ ] Build project tracking interface
- [ ] Integrate with agent loop

### Phase 4: Monitoring & Logging
- [ ] Set up structured logging system
- [ ] Implement tool call streaming
- [ ] Create screenshot capture tool
- [ ] Build log aggregation

### Phase 5: Web Dashboard
- [ ] Create Flask/FastAPI web server
- [ ] Build real-time log viewer (WebSocket)
- [ ] Display current agent status
- [ ] Show project queue
- [ ] Stream tool calls and screenshots

### Phase 6: Session Management
- [ ] Implement detachable sessions
- [ ] Allow UI to close/reopen
- [ ] Support multiple concurrent viewers
- [ ] Handle reconnection gracefully

### Phase 7: Screen Recording (Optional)
- [ ] Create ffmpeg rolling recording script
- [ ] Implement storage management
- [ ] Add recording controls to dashboard

## Technology Stack

- **Language**: Python 3.10+
- **Agent SDK**: claude-agent-sdk
- **CLI**: @anthropic-ai/claude-code
- **Scheduling**: APScheduler or schedule library
- **Web Framework**: FastAPI (async) or Flask
- **WebSocket**: python-socketio or websockets
- **Database**: SQLite for state persistence
- **Screen Recording**: ffmpeg
- **Process Management**: systemd (for Raspberry Pi service)

## File Structure

```
Claude-computer-use-from-the-Pi/
├── anthropic-quickstarts/
│   └── autonomous-agent/
│       ├── src/
│       │   ├── __init__.py
│       │   ├── autonomous_agent.py      # Main agent loop
│       │   ├── timer_manager.py         # Timer/scheduler
│       │   ├── project_manager.py       # Project tracking
│       │   ├── session_manager.py       # Session handling
│       │   ├── monitor.py               # Logging/monitoring
│       │   └── tools/
│       │       ├── __init__.py
│       │       ├── timer_tool.py        # Custom timer tool for Claude
│       │       ├── project_tool.py      # Project management tool
│       │       └── screenshot_tool.py   # Screenshot capture
│       ├── web/
│       │   ├── __init__.py
│       │   ├── app.py                   # Web dashboard
│       │   ├── static/                  # CSS/JS
│       │   └── templates/               # HTML templates
│       ├── data/
│       │   ├── state.db                 # Agent state
│       │   ├── projects.json            # Project data
│       │   └── logs/                    # Log files
│       ├── scripts/
│       │   ├── screen_recorder.sh       # Screen recording
│       │   └── start_agent.sh           # Agent startup
│       ├── config/
│       │   └── agent_config.yaml        # Configuration
│       ├── requirements.txt
│       └── README.md
├── setup_claude_env.sh
└── vision.md
```

## Custom Tools for Claude

Claude will have access to these custom tools:

1. **SetTimer**
   - Input: datetime, prompt
   - Allows Claude to schedule future actions

2. **CreateProject**
   - Input: name, description, tasks
   - Create a new project to work on

3. **UpdateProject**
   - Input: project_id, updates
   - Update project status/tasks

4. **TakeScreenshot**
   - Input: filename (optional)
   - Capture current screen state

## Configuration

Key configuration options:
- Check-in frequency (default: 1 hour)
- Max concurrent projects
- Log retention period
- Screenshot storage location
- Web dashboard port
- Enable/disable screen recording

## Deployment (Raspberry Pi)

1. Create systemd service for autonomous agent
2. Auto-start on boot
3. Restart on failure
4. Log to journal

## Security Considerations

- Limit filesystem access appropriately
- Sandbox potentially dangerous operations
- Rate limit API calls
- Secure web dashboard (authentication)
- Store API keys securely

## Testing Strategy

- Unit tests for each component
- Integration tests for agent loop
- Mock Claude responses for testing
- Test timer triggering
- Test session reconnection

## Next Steps

1. Start with Phase 1: Core Agent Setup
2. Create basic autonomous_agent.py
3. Test simple hourly check-in
4. Iterate and add features
