#!/usr/bin/env bash
# Comprehensive tool testing for Claude Autonomous Agent
# Tests all available tools and demonstrates capabilities

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
echo -e "${ORANGE}"
cat << "EOF"
   ╔═══════════════════════════════════════════════════════════╗
   ║                                                           ║
   ║              🧪  T O O L   T E S T I N G                  ║
   ║                                                           ║
   ║         Comprehensive Validation Suite v2.0               ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${BOLD}Claude Tools Comprehensive Test${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${GRAY}This test will verify:${NC}"
echo -e "  ${ORANGE}▸${NC} File operations (Read, Write, Edit)"
echo -e "  ${ORANGE}▸${NC} Search tools (Glob, Grep)"
echo -e "  ${ORANGE}▸${NC} Memory management"
echo -e "  ${ORANGE}▸${NC} System monitoring"
echo -e "  ${ORANGE}▸${NC} Project management"
echo -e "  ${ORANGE}▸${NC} Screenshots and timers"
echo -e "  ${ORANGE}▸${NC} Bash execution"
echo -e "  ${ORANGE}▸${NC} Web browser automation (Chromium → Apple.com)"
echo

echo -e "${ORANGE}▸${NC} Project directory: ${GREEN}$PROJECT_DIR${NC}"
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

echo
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${GREEN}🚀 Starting test suite...${NC}"
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${GRAY}Claude will now systematically test each tool...${NC}"
echo

# Run the test script
python scripts/test_tools.py

# Check exit code
EXIT_CODE=$?

echo
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${BOLD}${GREEN}✓ Test suite completed successfully!${NC}"
    echo
    echo -e "${GRAY}Check the following for results:${NC}"
    echo -e "  ${ORANGE}▸${NC} Console output above"
    echo -e "  ${ORANGE}▸${NC} ${GREEN}data/screenshots/${NC} for captured images"
    echo -e "  ${ORANGE}▸${NC} ${GREEN}data/logs/agent.log${NC} for detailed logs"
else
    echo -e "${BOLD}${RED}✗ Test suite encountered errors${NC}"
    echo
    echo -e "${GRAY}Check the output above for details${NC}"
fi

echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

exit $EXIT_CODE
