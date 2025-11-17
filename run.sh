#!/bin/bash
# Simple script to run the Christmas Treasure Hunt application

echo "🎄 Starting Christmas Treasure Hunt..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo "=================================="
echo "🎁 Starting server..."
echo "Access the game at: http://localhost:8000"
echo "Press CTRL+C to stop the server"
echo "=================================="
python3.11 app.py
