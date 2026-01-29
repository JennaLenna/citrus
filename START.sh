#!/bin/bash
echo "========================================"
echo "  🍊 Citrus AI - Starting..."
echo "========================================"
echo ""
echo "Starting the AI server..."
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Run the server
python3 simple_server.py

# Keep window open
read -p "Press Enter to close..."
