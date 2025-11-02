#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$ROOT_DIR/anthropic-quickstarts"
VENV_DIR="$PROJECT_DIR/computer-use-demo/.venv"

printf '\n>>> Setting up Claude autonomous environment\n\n'

# Ensure project directory exists
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Expected directory '$PROJECT_DIR' not found. Abort." >&2
  exit 1
fi

cd "$PROJECT_DIR"

# Create virtual environment if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating virtual environment at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# Upgrade pip and install Claude Agent SDK
pip install --upgrade pip >/dev/null
pip install --upgrade claude-agent-sdk >/dev/null

echo "✓ Python virtualenv ready with claude-agent-sdk installed"

# Ensure Claude CLI is installed
if ! command -v claude >/dev/null 2>&1; then
  echo "Installing Claude Code CLI via npm (requires sudo)..."
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is not available on PATH. Please install Node.js 18+ and rerun." >&2
    exit 1
  fi
  sudo npm install -g @anthropic-ai/claude-code
else
  echo "✓ Claude CLI already installed"
fi

echo
echo "Refreshing Claude CLI authentication (follow the login instructions that appear next)..."
echo
claude --print "/login" || {
  echo "Login failed. Run 'claude --print \"/login\"' manually after resolving the issue." >&2
  exit 1
}

echo -e "\n✓ Claude CLI authentication refreshed"

# Guidance for optional screen recording setup
if ! command -v ffmpeg >/dev/null 2>&1; then
  cat <<'MSG'

NOTE: 'ffmpeg' is not installed. If you plan to use record_screen.sh for rolling
screen capture, install it with:
  sudo apt install ffmpeg
MSG
else
  echo "✓ ffmpeg detected (screen recording helper ready)"
fi

echo -e "\nAll set! Activate the venv whenever you work with this project:
  source $VENV_DIR/bin/activate
"
