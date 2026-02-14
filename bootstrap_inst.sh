#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt-get &>/dev/null; then
    echo "Error: apt-get not found. This script requires Ubuntu/Debian."
    exit 1
fi

if ! command -v curl &>/dev/null; then
    echo "Installing curl..."
    if [ "$(id -u)" -eq 0 ]; then
        apt-get update -qq && apt-get install -y -qq curl
    else
        sudo apt-get update -qq && sudo apt-get install -y -qq curl
    fi
fi

if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec uv run "$SCRIPT_DIR/install.py"
