#!/bin/bash

echo "╔══════════════════════════════════════╗"
echo "║                                      ║"
echo "║   FILE TO LINK BOT - STARTUP         ║"
echo "║                                      ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env file with your credentials"
    echo "   Then run this script again"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "🐍 Python version: $python_version"

# Install requirements
echo ""
echo "📦 Installing requirements..."
pip3 install -r requirements.txt

# Run the bot
echo ""
echo "🚀 Starting the bot..."
python3 bot.py
