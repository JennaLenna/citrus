#!/bin/bash
# Start Citrus AI Web Interface

echo "=========================================="
echo "  🍊 Citrus AI Web Interface 🍊"
echo "=========================================="
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting web server..."
echo ""
echo "👉 Open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python web_app.py
