<div align="center">

```
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║                      🎯  V I S I O N                      ║
   ║                                                           ║
   ║               Claude's Computer: Autonomy                 ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
```

### *From Assistant to Operator*

</div>

---

## 💭 Core Concept

**Give Claude true ownership of a computer** (Raspberry Pi) where Claude operates as an independent agent—not just an assistant, but as the *operator* of the machine.

Claude can:
- 🎯 Conceive and execute ideas independently
- ⏰ Set timers and schedule future work
- 📋 Create and manage projects
- 💭 Make autonomous decisions

**The experiment**: "Hire" Claude as a developer for a startup.

## ✅ Implemented Features

This vision has been realized through the **Claude Autonomous Agent System** located in `anthropic-quickstarts/autonomous-agent/`.

### Autonomous Operation
- ✅ **Periodic Check-ins**: Claude receives hourly prompts asking "Do you want to work on anything?"
- ✅ **Self-directed Work**: Claude can initiate and manage projects independently
- ✅ **Persistent Memory**: CLAUDE.md files maintain context across all sessions
- ✅ **Timer System**: Claude can set timers and schedule future actions

### Tool Capabilities
Claude has access to powerful tools:
- **File Operations**: Read, Write, Edit files across the system
- **Code Execution**: Run bash commands, scripts, and programs
- **Web Access**: Browse websites, search the web, fetch content
- **System Monitoring**: Check CPU/memory/disk usage, list processes
- **Project Management**: Create, track, and update projects
- **Screenshots**: Capture screen state for documentation
- **Memory Management**: Persistent notes and learnings across sessions

### Monitoring & State
- ✅ **Web Dashboard**: Real-time monitoring interface (localhost:8080)
- ✅ **Reconnectable UI**: Close and reopen without losing state
- ✅ **Activity Logs**: Complete history of actions in data/logs/agent.log
- ✅ **Screenshot History**: Visual record in data/screenshots/
- ✅ **Session Persistence**: Agent resumes from where it left off

### Cost Optimization
- ✅ **Prompt Caching**: ~90% cost reduction through automatic caching
- ✅ **Efficient Memory**: CLAUDE.md based context management

### Optional Features
- ✅ **Screen Recording**: Rolling video capture with automatic cleanup
- ✅ **Service Mode**: Run continuously on boot (systemd)

## Architecture

```
Raspberry Pi
├── Autonomous Agent (runs continuously)
│   ├── Periodic check-ins (every N minutes)
│   ├── Timer callbacks (scheduled events)
│   └── Project tracking
├── Custom Tools (MCP Server)
│   ├── Timer management
│   ├── Project management
│   ├── Memory management
│   └── System monitoring
├── Web Dashboard (monitoring)
│   ├── Real-time status
│   ├── Activity stream
│   └── Project list
└── Data Persistence
    ├── CLAUDE.md (memory)
    ├── projects.json
    ├── session_state.json
    └── logs/ screenshots/
```

## Experiment: "Hiring" Claude

The system enables running experiments where Claude acts as an autonomous developer:

1. **Initial Setup**: Deploy the agent on Raspberry Pi
2. **Autonomous Operation**: Claude checks in hourly, decides what to work on
3. **Project Execution**: Claude can create projects, code, test, and iterate
4. **Self-Management**: Claude sets timers, manages priorities, tracks progress
5. **Observable**: Monitor through web dashboard or logs

## Future Enhancements

### Potential Additions
- Multi-agent collaboration (multiple Claude instances)
- More sophisticated project prioritization
- Integration with external services (GitHub, etc.)
- Voice interface for status updates
- Mobile monitoring app
- Advanced computer vision capabilities
- Long-term goal tracking and planning

### Desired Improvements
- Better streaming view for real-time tool calls
- Public access mode for demonstrations
- Enhanced screen recording with lower resource usage
- Automatic project documentation generation
- Learning from past actions and outcomes

## Philosophy

This project embodies:
- **Autonomy over Assistance**: Claude as operator, not just helper
- **Continuous Operation**: Always available, always thinking
- **Transparency**: All actions logged and observable
- **Safety with Freedom**: Guardrails that don't restrict creativity
- **Experimentation**: A platform for exploring AI autonomy

## Getting Started

See the full implementation in:
```
/anthropic-quickstarts/autonomous-agent/
```

Quick start:
```bash
cd anthropic-quickstarts/autonomous-agent
./scripts/setup.sh
./scripts/start_agent.sh
./scripts/start_dashboard.sh  # Optional: Web monitoring
```

---

**Status**: ✅ **FULLY IMPLEMENTED** - Vision realized in v2.0 release
**Location**: `anthropic-quickstarts/autonomous-agent/`
**Documentation**: See `anthropic-quickstarts/autonomous-agent/README.md`
