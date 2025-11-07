#!/usr/bin/env bash
# Setup script for Claude Autonomous Agent
# Prepares the environment and installs dependencies

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
echo -e "${GREEN}"
cat << "EOF"
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║             ⚙️   S E T U P   &   I N S T A L L            ║
   ║                                                           ║
   ║         Claude Autonomous Agent System v2.0               ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${BOLD}Environment Setup${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${ORANGE}▸${NC} Project directory: ${GREEN}$PROJECT_DIR${NC}"
echo

cd "$PROJECT_DIR"

# Create virtual environment
echo -e "${ORANGE}▸${NC} Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GRAY}  Already exists, skipping${NC}"
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
echo -e "${ORANGE}▸${NC} Upgrading pip..."
pip install --quiet --upgrade pip
echo -e "${GREEN}✓${NC} Pip upgraded"

# Install dependencies
echo -e "${ORANGE}▸${NC} Installing Python dependencies..."
pip install --quiet -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Create data directories
echo -e "${ORANGE}▸${NC} Creating data directories..."
mkdir -p data/logs
mkdir -p data/screenshots
mkdir -p data/recordings
mkdir -p .claude
echo -e "${GREEN}✓${NC} Directories created"

# Check for Claude CLI
echo -e "${ORANGE}▸${NC} Checking for Claude CLI..."
if ! command -v claude &> /dev/null; then
    echo -e "${ORANGE}⚠${NC}  Claude CLI not found"
    echo
    echo -e "${GRAY}  To install:${NC}"
    echo -e "    ${BLUE}npm install -g @anthropic-ai/claude-code${NC}"
    echo
    echo -e "${GRAY}  Then authenticate:${NC}"
    echo -e "    ${BLUE}claude --print '/login'${NC}"
    echo
else
    CLAUDE_VERSION=$(claude --version 2>&1 || echo "unknown")
    echo -e "${GREEN}✓${NC} Claude CLI found (${CLAUDE_VERSION})"
fi

echo
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${GREEN}✓ Setup complete!${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

echo -e "${BOLD}Next steps:${NC}"
echo
echo -e "  ${ORANGE}1.${NC} ${GRAY}Start the agent:${NC}"
echo -e "     ${BLUE}./scripts/start_agent.sh${NC}"
echo
echo -e "  ${ORANGE}2.${NC} ${GRAY}Start the web dashboard (optional):${NC}"
echo -e "     ${BLUE}./scripts/start_dashboard.sh${NC}"
echo -e "     ${GRAY}Then visit:${NC} ${GREEN}http://localhost:8080${NC}"
echo
echo -e "  ${ORANGE}3.${NC} ${GRAY}Run tool tests (optional):${NC}"
echo -e "     ${BLUE}./scripts/test_tools.sh${NC}"
echo

echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
