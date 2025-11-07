#!/usr/bin/env bash
# Test all Claude tools

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "Claude Tools Test Script"
echo "========================================="
echo "Project directory: $PROJECT_DIR"
echo ""

cd "$PROJECT_DIR"

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found at .venv"
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate venv
source .venv/bin/activate

# Run the test script
python scripts/test_tools.py

echo ""
echo "========================================="
echo "Test Complete!"
echo "========================================="
