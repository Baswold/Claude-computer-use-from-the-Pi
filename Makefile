# Makefile for Claude Autonomous Agent
# Provides convenient commands for common operations

.PHONY: help install setup start dashboard stop test clean status logs

# Default target - show help
help:
	@echo ""
	@echo "  ╔═══════════════════════════════════════════════════════════╗"
	@echo "  ║                                                           ║"
	@echo "  ║              Claude Autonomous Agent                      ║"
	@echo "  ║                   Quick Commands                          ║"
	@echo "  ║                                                           ║"
	@echo "  ╚═══════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Setup & Installation:"
	@echo "    make install     - Run complete installation (one command setup)"
	@echo "    make setup       - Set up Python environment and dependencies"
	@echo ""
	@echo "  Running the Agent:"
	@echo "    make start       - Start the autonomous agent"
	@echo "    make dashboard   - Start the web dashboard (http://localhost:8080)"
	@echo "    make stop        - Stop all running processes"
	@echo ""
	@echo "  Testing & Verification:"
	@echo "    make test        - Run comprehensive tool tests"
	@echo "    make status      - Check agent status"
	@echo "    make logs        - View agent logs (tail -f)"
	@echo ""
	@echo "  Maintenance:"
	@echo "    make clean       - Remove generated files and caches"
	@echo "    make update      - Update dependencies"
	@echo ""
	@echo "  Quick Start:"
	@echo "    1. make install"
	@echo "    2. make start"
	@echo "    3. make dashboard  (optional)"
	@echo ""

# Complete installation
install:
	@chmod +x install.sh
	@./install.sh

# Set up environment (lighter than full install)
setup:
	@cd anthropic-quickstarts/autonomous-agent && chmod +x scripts/setup.sh && ./scripts/setup.sh

# Start the autonomous agent
start:
	@echo "Starting Claude Autonomous Agent..."
	@cd anthropic-quickstarts/autonomous-agent && chmod +x scripts/start_agent.sh && ./scripts/start_agent.sh

# Start the web dashboard
dashboard:
	@echo "Starting web dashboard at http://localhost:8080"
	@cd anthropic-quickstarts/autonomous-agent && chmod +x scripts/start_dashboard.sh && ./scripts/start_dashboard.sh

# Stop all processes
stop:
	@echo "Stopping all Claude agent processes..."
	@pkill -f "autonomous_agent.py" || true
	@pkill -f "web/app.py" || true
	@echo "All processes stopped"

# Run tests
test:
	@echo "Running comprehensive tool tests..."
	@cd anthropic-quickstarts/autonomous-agent && chmod +x scripts/test_tools.sh && ./scripts/test_tools.sh

# Check status
status:
	@echo ""
	@echo "=== Claude Agent Status ==="
	@echo ""
	@echo "Agent process:"
	@pgrep -f "autonomous_agent.py" > /dev/null && echo "  ✓ Running (PID: $$(pgrep -f 'autonomous_agent.py'))" || echo "  ✗ Not running"
	@echo ""
	@echo "Dashboard process:"
	@pgrep -f "web/app.py" > /dev/null && echo "  ✓ Running (PID: $$(pgrep -f 'web/app.py'))" || echo "  ✗ Not running"
	@echo ""
	@echo "Last check-in:"
	@if [ -f anthropic-quickstarts/autonomous-agent/data/session_state.json ]; then \
		echo "  $$(cat anthropic-quickstarts/autonomous-agent/data/session_state.json | grep -o '"last_checkin": "[^"]*"' | cut -d'"' -f4 || echo 'Unknown')"; \
	else \
		echo "  No session data found"; \
	fi
	@echo ""
	@echo "Active projects:"
	@if [ -f anthropic-quickstarts/autonomous-agent/data/projects.json ]; then \
		PROJECT_COUNT=$$(cat anthropic-quickstarts/autonomous-agent/data/projects.json | grep -o '"status": "active"' | wc -l); \
		echo "  $$PROJECT_COUNT active project(s)"; \
	else \
		echo "  No project data found"; \
	fi
	@echo ""

# View logs
logs:
	@echo "Viewing agent logs (Ctrl+C to exit)..."
	@echo ""
	@if [ -f anthropic-quickstarts/autonomous-agent/data/logs/agent.log ]; then \
		tail -f anthropic-quickstarts/autonomous-agent/data/logs/agent.log; \
	else \
		echo "No logs found. Agent may not have run yet."; \
	fi

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -rf anthropic-quickstarts/autonomous-agent/.venv
	@rm -rf anthropic-quickstarts/autonomous-agent/data/logs/*
	@rm -rf anthropic-quickstarts/autonomous-agent/data/screenshots/*
	@rm -rf anthropic-quickstarts/autonomous-agent/data/recordings/*
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete"

# Update dependencies
update:
	@echo "Updating dependencies..."
	@cd anthropic-quickstarts/autonomous-agent && \
		source .venv/bin/activate && \
		pip install --upgrade pip && \
		pip install --upgrade -r requirements.txt
	@echo "Dependencies updated"

# Quick check of prerequisites
check:
	@echo ""
	@echo "=== System Requirements Check ==="
	@echo ""
	@echo "Python 3:"
	@python3 --version 2>&1 || echo "  ✗ Not found"
	@echo ""
	@echo "Node.js:"
	@node --version 2>&1 || echo "  ✗ Not found"
	@echo ""
	@echo "npm:"
	@npm --version 2>&1 || echo "  ✗ Not found"
	@echo ""
	@echo "Claude CLI:"
	@claude --version 2>&1 || echo "  ✗ Not found"
	@echo ""

# View recent activity
activity:
	@echo "Recent agent activity (last 20 lines):"
	@echo ""
	@if [ -f anthropic-quickstarts/autonomous-agent/data/logs/agent.log ]; then \
		tail -n 20 anthropic-quickstarts/autonomous-agent/data/logs/agent.log; \
	else \
		echo "No activity logs found"; \
	fi

# View projects
projects:
	@echo ""
	@echo "=== Active Projects ==="
	@echo ""
	@if [ -f anthropic-quickstarts/autonomous-agent/data/projects.json ]; then \
		cat anthropic-quickstarts/autonomous-agent/data/projects.json | grep -A 3 '"status": "active"' || echo "No active projects"; \
	else \
		echo "No project data found"; \
	fi
	@echo ""

# View memory
memory:
	@echo ""
	@echo "=== Claude's Memory (CLAUDE.md) ==="
	@echo ""
	@if [ -f anthropic-quickstarts/autonomous-agent/CLAUDE.md ]; then \
		cat anthropic-quickstarts/autonomous-agent/CLAUDE.md; \
	else \
		echo "No memory file found"; \
	fi
	@echo ""
