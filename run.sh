#!/bin/bash
# Quick run script for sticker-to-emoji

set -e

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import telethon" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Install package in editable mode
pip install -e . > /dev/null 2>&1

# Run the converter
python -m sticker_to_emoji "$@"
