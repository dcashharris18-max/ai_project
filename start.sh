#!/usr/bin/env bash
# Startup script for AI Multi-Domain Trading System

echo "AI Multi-Domain Trading System - Starting Web Application"
echo "=========================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using defaults."
    echo "Copy .env.example to .env and configure your API keys for full functionality."
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip show flask gunicorn flask-cors numpy pyyaml tensorflow >/dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Dependencies already installed."
fi

# Start the application
echo "Starting web server on http://localhost:5000"
python3 app.py
