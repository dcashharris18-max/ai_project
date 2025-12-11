#!/bin/bash
# Startup script for AI Multi-Domain Trading System

echo "AI Multi-Domain Trading System - Starting Web Application"
echo "=========================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using defaults."
    echo "Copy .env.example to .env and configure your API keys for full functionality."
fi

# Install dependencies if needed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the application
echo "Starting web server on http://localhost:5000"
python3 app.py
