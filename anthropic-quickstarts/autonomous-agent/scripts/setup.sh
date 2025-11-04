#!/usr/bin/env bash
# Setup script for the autonomous agent

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Setting up Claude Autonomous Agent..."
echo "Project directory: $PROJECT_DIR"

cd "$PROJECT_DIR"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directories
echo "Creating data directories..."
mkdir -p data/logs
mkdir -p data/screenshots

# Check for Claude CLI
if ! command -v claude &> /dev/null; then
    echo "WARNING: Claude CLI not found!"
    echo "Please install it with: npm install -g @anthropic-ai/claude-code"
    echo "Then authenticate with: claude --print '/login'"
else
    echo "✓ Claude CLI found"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To start the agent:"
echo "  ./scripts/start_agent.sh"
echo ""
echo "To start the web dashboard:"
echo "  ./scripts/start_dashboard.sh"
echo ""
