#!/usr/bin/env bash
# One-command installer for Claude Autonomous Agent
# This script sets up everything needed to run Claude on your Raspberry Pi or Linux machine

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$SCRIPT_DIR/anthropic-quickstarts/autonomous-agent"

# Track if we need to install anything
NEEDS_INSTALL=false

# Helper functions
print_header() {
    echo -e "${CYAN}"
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
   ║              O N E - C O M M A N D   S E T U P            ║
   ║                                                           ║
   ║         Claude Autonomous Agent for Raspberry Pi          ║
   ║                                                           ║
   ╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}▸${NC} $1"
}

print_step() {
    echo -e "\n${BOLD}${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get version of a command
get_version() {
    case "$1" in
        python3)
            python3 --version 2>&1 | awk '{print $2}'
            ;;
        node)
            node --version 2>&1 | sed 's/v//'
            ;;
        npm)
            npm --version 2>&1
            ;;
        claude)
            claude --version 2>&1 | head -n1 || echo "unknown"
            ;;
    esac
}

# Compare versions (returns 0 if version1 >= version2)
version_ge() {
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

# Main installation
main() {
    clear
    print_header

    print_step "Step 1: System Requirements Check"

    # Check Python 3.10+
    print_info "Checking Python version..."
    if command_exists python3; then
        PYTHON_VERSION=$(get_version python3)
        if version_ge "$PYTHON_VERSION" "3.10"; then
            print_success "Python $PYTHON_VERSION found"
        else
            print_error "Python $PYTHON_VERSION is too old (need 3.10+)"
            echo
            echo "Please install Python 3.10 or higher:"
            echo "  Ubuntu/Debian: sudo apt install python3.10 python3.10-venv"
            echo "  macOS: brew install python@3.10"
            exit 1
        fi
    else
        print_error "Python 3 not found"
        echo
        echo "Please install Python 3.10 or higher:"
        echo "  Ubuntu/Debian: sudo apt install python3.10 python3.10-venv"
        echo "  macOS: brew install python@3.10"
        exit 1
    fi

    # Check Node.js 18+
    print_info "Checking Node.js version..."
    if command_exists node; then
        NODE_VERSION=$(get_version node)
        NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
        if [ "$NODE_MAJOR" -ge 18 ]; then
            print_success "Node.js $NODE_VERSION found"
        else
            print_warning "Node.js $NODE_VERSION found, but 18+ is recommended"
            echo
            echo "To upgrade Node.js:"
            echo "  Using nvm: nvm install 18 && nvm use 18"
            echo "  Or visit: https://nodejs.org/"
            echo
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_error "Node.js not found"
        echo
        echo "Please install Node.js 18 or higher:"
        echo "  Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install nodejs"
        echo "  macOS: brew install node@18"
        echo "  Or use nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && nvm install 18"
        exit 1
    fi

    # Check npm
    print_info "Checking npm..."
    if command_exists npm; then
        NPM_VERSION=$(get_version npm)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm not found (should come with Node.js)"
        exit 1
    fi

    print_step "Step 2: Claude CLI Setup"

    # Check/install Claude CLI
    if command_exists claude; then
        CLAUDE_VERSION=$(get_version claude)
        print_success "Claude CLI already installed ($CLAUDE_VERSION)"
    else
        print_warning "Claude CLI not found"
        echo
        read -p "Install Claude CLI globally? (requires sudo) [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            print_info "Installing Claude CLI..."
            if sudo npm install -g @anthropic-ai/claude-code; then
                print_success "Claude CLI installed successfully"
                NEEDS_INSTALL=true
            else
                print_error "Failed to install Claude CLI"
                echo
                echo "Try manually with: sudo npm install -g @anthropic-ai/claude-code"
                exit 1
            fi
        else
            print_error "Claude CLI is required. Please install it manually:"
            echo "  npm install -g @anthropic-ai/claude-code"
            exit 1
        fi
    fi

    print_step "Step 3: Agent Directory Setup"

    # Navigate to agent directory
    if [ ! -d "$AGENT_DIR" ]; then
        print_error "Agent directory not found: $AGENT_DIR"
        exit 1
    fi

    print_info "Agent directory: $AGENT_DIR"
    cd "$AGENT_DIR"
    print_success "Changed to agent directory"

    print_step "Step 4: Python Environment"

    # Create virtual environment
    print_info "Setting up Python virtual environment..."
    if [ ! -d ".venv" ]; then
        if python3 -m venv .venv; then
            print_success "Virtual environment created"
        else
            print_error "Failed to create virtual environment"
            echo "You may need to install python3-venv:"
            echo "  sudo apt install python3-venv"
            exit 1
        fi
    else
        print_success "Virtual environment already exists"
    fi

    # Activate venv
    print_info "Activating virtual environment..."
    source .venv/bin/activate
    print_success "Virtual environment activated"

    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --quiet --upgrade pip
    print_success "pip upgraded"

    # Install dependencies
    print_info "Installing Python dependencies (this may take a minute)..."
    if pip install --quiet -r requirements.txt; then
        print_success "Dependencies installed"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi

    print_step "Step 5: Directory Structure"

    # Create necessary directories
    print_info "Creating data directories..."
    mkdir -p data/logs
    mkdir -p data/screenshots
    mkdir -p data/recordings
    mkdir -p .claude
    print_success "Directories created"

    # Check for config file
    print_info "Verifying configuration files..."
    if [ ! -f "config/agent_config.yaml" ]; then
        print_error "Configuration file not found"
        exit 1
    fi
    print_success "Configuration verified"

    print_step "Step 6: Authentication"

    # Claude authentication
    echo -e "${YELLOW}${BOLD}Important: You need to authenticate with Claude CLI${NC}\n"
    echo "This will open a browser window for you to log in with your Anthropic account."
    echo
    read -p "Authenticate now? [Y/n] " -n 1 -r
    echo
    echo

    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        if claude --print "/login"; then
            echo
            print_success "Authentication successful"
        else
            echo
            print_warning "Authentication failed or skipped"
            echo
            echo "You can authenticate later with:"
            echo "  claude --print '/login'"
        fi
    else
        print_warning "Skipping authentication - you'll need to do this before running the agent:"
        echo "  claude --print '/login'"
    fi

    print_step "Step 7: Verification"

    # Make sure scripts are executable
    print_info "Setting script permissions..."
    chmod +x scripts/*.sh 2>/dev/null || true
    print_success "Script permissions set"

    # Quick system check
    print_info "Checking optional dependencies..."
    if command_exists ffmpeg; then
        print_success "ffmpeg found (screen recording available)"
    else
        print_warning "ffmpeg not found (screen recording disabled)"
        echo "  Install with: sudo apt install ffmpeg"
    fi

    print_step "✨ Installation Complete! ✨"

    echo -e "${GREEN}${BOLD}Everything is set up and ready to go!${NC}\n"

    echo -e "${BOLD}Quick Start:${NC}\n"
    echo -e "  ${CYAN}# Start the autonomous agent${NC}"
    echo -e "  cd $AGENT_DIR"
    echo -e "  ./scripts/start_agent.sh\n"

    echo -e "  ${CYAN}# (Optional) Start the web dashboard${NC}"
    echo -e "  ./scripts/start_dashboard.sh"
    echo -e "  ${BOLD}Then visit: ${GREEN}http://localhost:8080${NC}\n"

    echo -e "  ${CYAN}# (Optional) Test all tools${NC}"
    echo -e "  ./scripts/test_tools.sh\n"

    echo -e "${BOLD}What happens next:${NC}\n"
    echo "  1. Claude will perform an initial check-in"
    echo "  2. Claude will check in every hour (configurable)"
    echo "  3. Claude can create projects, set timers, and work autonomously"
    echo "  4. All activity is logged to data/logs/agent.log"
    echo "  5. Memory persists in CLAUDE.md\n"

    echo -e "${BOLD}Documentation:${NC}\n"
    echo "  README.md - Project overview"
    echo "  QUICKSTART.md - Quick reference"
    echo "  anthropic-quickstarts/autonomous-agent/README.md - Detailed docs\n"

    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}${BOLD}Ready to give Claude autonomy? Run:${NC}"
    echo -e "${BOLD}cd $AGENT_DIR && ./scripts/start_agent.sh${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Run main function
main "$@"
