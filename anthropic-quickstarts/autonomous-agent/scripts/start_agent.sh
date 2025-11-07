#!/usr/bin/env bash
# Start the Claude Autonomous Agent
# Part of the Claude Autonomous Agent System v2.0

set -euo pipefail

# Colors for beautiful output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Beautiful banner
clear
echo -e "${BLUE}"
cat << "EOF"
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
EOF
echo -e "${NC}"

echo -e "${BOLD}Starting Autonomous Agent...${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Display environment info
echo -e "${ORANGE}▸${NC} Project directory: ${GREEN}$PROJECT_DIR${NC}"
echo -e "${ORANGE}▸${NC} Version: ${GREEN}2.0${NC}"
echo -e "${ORANGE}▸${NC} Date: ${GREEN}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo

cd "$PROJECT_DIR"

# Check if venv exists
echo -e "${ORANGE}▸${NC} Checking virtual environment..."
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗${NC} Virtual environment not found at .venv"
    echo
    echo -e "${GRAY}Please run the setup script first:${NC}"
    echo -e "${BLUE}  ./scripts/setup.sh${NC}"
    echo
    exit 1
fi
echo -e "${GREEN}✓${NC} Virtual environment found"

# Activate venv
echo -e "${ORANGE}▸${NC} Activating environment..."
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Environment activated"

# Check for required files
echo -e "${ORANGE}▸${NC} Verifying configuration..."
if [ ! -f "config/agent_config.yaml" ]; then
    echo -e "${RED}✗${NC} Configuration file not found"
    exit 1
fi
echo -e "${GREEN}✓${NC} Configuration verified"

echo
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${GREEN}🚀 Launching agent...${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${GRAY}Press Ctrl+C to stop${NC}"
echo

# Run the agent
python src/autonomous_agent.py
